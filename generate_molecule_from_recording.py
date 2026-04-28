#!/usr/bin/env python3
"""
Generate a complete Molecule scenario from a network_cli transcript recording.

Takes the JSONL file produced by ANSIBLE_NETWORK_CLI_RECORD=1 and creates:
  - cisshgo_fixtures/transcripts/<module>/gathered.txt
  - cisshgo_fixtures/transcripts/<module>/scenarios/<state>/before.txt
  - cisshgo_fixtures/transcripts/<module>/scenarios/<state>/after.txt
  - cisshgo_fixtures/inventories/cisshgo/<scenario>.yaml
  - cisshgo_fixtures/inventories/ansible/<scenario>.yaml
  - cisshgo_fixtures/transcript_map_fragment.yaml  (to merge into transcript_map.yaml)
  - <scenario>/molecule.yml
  - <scenario>/vars.yml
  - <scenario>/converge.yml

Phase matching strategy:
  The recording captures ALL configure-terminal blocks including setup/teardown
  (_remove_config, _populate_config). To identify which phases are actual test
  operations, we read the integration test vars/main.yaml and match each state's
  expected `commands` list against the recorded config commands in each phase.
  Only matched phases produce transcripts and scenario entries.

Usage:
    python generate_molecule_from_recording.py \\
        /tmp/recordings/54.190.208.146_2193.jsonl \\
        --module ios_hostname \\
        --show-command "show running-config | section ^hostname" \\
        --collection cisco.ios \\
        --state-names merged,deleted

    python generate_molecule_from_recording.py \\
        /tmp/recordings/54.190.208.146_2193.jsonl \\
        --module ios_interfaces \\
        --show-command "show running-config | section ^interface" \\
        --collection cisco.ios \\
        --state-names gathered,merged,replaced
"""

import argparse
import json
import os
import sys

from pathlib import Path


try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ======================================================================
# Constants
# ======================================================================

BOILERPLATE_COMMANDS = {
    "terminal length 0",
    "terminal width 512",
    "terminal width 0",
    "show privilege",
    "show version",
    "enable",
}

# States that don't pass a config block to the module
NO_CONFIG_STATES = {"deleted", "gathered"}

# States that are offline (no device interaction needed for the test,
# but still need a network_cli context via cisshgo)
OFFLINE_STATES = {"parsed", "rendered"}


# ======================================================================
# JSONL loading
# ======================================================================


def load_recording(path):
    """Load JSONL recording into a list of {command, response, timestamp} dicts."""
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


# ======================================================================
# Vars / test-task loading
# ======================================================================


def find_vars_file(module_name, cwd):
    """Auto-detect vars/main.yaml for the module under tests/integration/targets/."""
    candidates = [
        cwd / "tests" / "integration" / "targets" / module_name / "vars" / "main.yaml",
        cwd / "tests" / "integration" / "targets" / module_name / "vars" / "main.yml",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def load_vars(path):
    """Load vars/main.yaml — needs PyYAML."""
    if not HAS_YAML:
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def find_test_task_file(module_name, state_name, cwd):
    """Find the integration test task file for a given state."""
    candidates = [
        cwd
        / "tests"
        / "integration"
        / "targets"
        / module_name
        / "tests"
        / "cli"
        / ("%s.yaml" % state_name),
        cwd
        / "tests"
        / "integration"
        / "targets"
        / module_name
        / "tests"
        / "cli"
        / ("%s.yml" % state_name),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def extract_module_config_from_test(test_file_path, module_name, collection):
    """
    Parse the integration test YAML to extract the exact module invocation config.
    Returns (config_dict_or_list, state_str) or (None, state_str) for no-config states.
    """
    if not HAS_YAML or not test_file_path:
        return None, None

    with open(test_file_path) as f:
        tasks = yaml.safe_load(f)

    if not isinstance(tasks, list):
        return None, None

    fqcn = "%s.%s" % (collection, module_name)

    # Walk through tasks (may be nested in block/rescue/always)
    def search_tasks(task_list):
        for task in task_list:
            if not isinstance(task, dict):
                continue
            # Check if this task invokes our module
            if fqcn in task:
                module_args = task[fqcn]
                if isinstance(module_args, dict):
                    return module_args.get("config"), module_args.get("state")
            # Check inside block
            if "block" in task:
                result = search_tasks(task["block"])
                if result[1] is not None:
                    return result
        return None, None

    return search_tasks(tasks)


# ======================================================================
# Recording segmentation
# ======================================================================


def is_boilerplate(command):
    cmd = command.strip().lower()
    return any(cmd.startswith(bp.lower()) for bp in BOILERPLATE_COMMANDS)


def is_show_command(command, show_cmd):
    return command.strip().lower() == show_cmd.strip().lower()


def is_config_enter(command):
    return command.strip().lower().startswith("configure terminal")


def is_config_exit(command):
    return command.strip().lower() in ("end", "exit")


def segment_recording(entries, show_cmd):
    """
    Split the recording into phases:
      - gathered: show command only (no config block follows)
      - stateful: show → configure terminal → commands → end → show
    """
    phases = []
    i = 0

    while i < len(entries):
        entry = entries[i]
        cmd = entry["command"].strip()

        if is_boilerplate(cmd):
            i += 1
            continue

        if is_show_command(cmd, show_cmd):
            show_response = entry["response"]
            j = i + 1
            while j < len(entries) and is_boilerplate(entries[j]["command"].strip()):
                j += 1

            if j < len(entries) and is_config_enter(entries[j]["command"].strip()):
                config_commands = []
                k = j + 1
                while k < len(entries):
                    c = entries[k]["command"].strip()
                    if is_config_exit(c):
                        k += 1
                        break
                    if not is_boilerplate(c):
                        config_commands.append(c)
                    k += 1

                # Look for show-after
                show_after = None
                while k < len(entries):
                    c = entries[k]["command"].strip()
                    if is_show_command(c, show_cmd):
                        show_after = entries[k]["response"]
                        k += 1
                        break
                    if is_boilerplate(c):
                        k += 1
                        continue
                    break

                # Skip duplicate show commands
                if k < len(entries) and is_show_command(entries[k]["command"].strip(), show_cmd):
                    k += 1

                phases.append(
                    {
                        "type": "stateful",
                        "show_before": show_response,
                        "commands": config_commands,
                        "show_after": show_after or show_response,
                    }
                )
                i = k
            else:
                phases.append(
                    {
                        "type": "gathered",
                        "show_response": show_response,
                    }
                )
                i = j
        else:
            i += 1

    return phases


# ======================================================================
# Phase matching — the key improvement
# ======================================================================


def match_phases_to_states(phases, state_names, test_vars):
    """
    Match recorded phases to test states using expected commands from vars.

    For each state_name, look up test_vars[state_name]['commands'] and find the
    FIRST unmatched phase whose config commands match exactly.

    Returns: dict mapping state_name -> phase (only matched states)
    """
    if not test_vars:
        # Fallback: assign phases to states in order (old behavior)
        stateful = [p for p in phases if p["type"] == "stateful"]
        matched = {}
        for i, state in enumerate(state_names):
            if i < len(stateful):
                matched[state] = stateful[i]
        return matched

    matched = {}
    used_indices = set()
    stateful_phases = [(i, p) for i, p in enumerate(phases) if p["type"] == "stateful"]

    for state_name in state_names:
        state_vars = test_vars.get(state_name, {})
        expected_commands = state_vars.get("commands", [])

        if not expected_commands:
            continue

        # Normalize expected commands for comparison
        expected_normalized = [c.strip().lower() for c in expected_commands]

        for idx, phase in stateful_phases:
            if idx in used_indices:
                continue

            phase_normalized = [c.strip().lower() for c in phase["commands"]]

            if phase_normalized == expected_normalized:
                matched[state_name] = phase
                used_indices.add(idx)
                print(
                    "  Matched state '%s' to phase %d (commands: %s)"
                    % (state_name, idx, expected_commands),
                )
                break
        else:
            print(
                "  WARNING: No matching phase found for state '%s' (expected: %s)"
                % (state_name, expected_commands),
            )

    return matched


# ======================================================================
# File generation helpers
# ======================================================================


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


def module_to_scenario_name(module_name):
    """ios_hostname -> hostname"""
    parts = module_name.split("_", 1)
    return parts[1] if len(parts) > 1 else module_name


def module_to_scenario_id(module_name, state):
    """ios_hostname, merged -> ios-hostname-merged"""
    return "%s-%s" % (module_name.replace("_", "-"), state)


# ======================================================================
# Transcript map generation
# ======================================================================


def generate_platform_entry(module_name, show_cmd):
    return """  %s:
    vendor: "cisco"
    hostname: "cisshgo-ios"
    username: "admin"
    password: "admin"
    command_transcripts:
      "show privilege": "transcripts/common/show_privilege.txt"
      "terminal length 0": "transcripts/generic_empty_return.txt"
      "terminal width 512": "transcripts/generic_empty_return.txt"
      "terminal width 0": "transcripts/generic_empty_return.txt"
      "show version": "transcripts/common/show_version.txt"
      "%s": "transcripts/%s/gathered.txt"
      "write memory": "transcripts/generic_empty_return.txt"
      "write mem": "transcripts/generic_empty_return.txt"
    context_search:
      "configure terminal": "(config)#"
      "interface": "(config-if)#"
      "enable": "#"
      "base": "#"
    context_hierarchy:
      "(config-if)#": "(config)#"
      "(config)#": "#"
      "#": ">"
    end_context: "#"
""" % (
        module_name,
        show_cmd,
        module_name,
    )


def generate_scenario_entry(module_name, state_name, show_cmd, phase):
    """Generate a single scenario entry for the transcript map."""
    scenario_id = module_to_scenario_id(module_name, state_name)
    lines = []
    lines.append("  %s:" % scenario_id)
    lines.append("    platform: %s" % module_name)
    lines.append("    sequence:")
    lines.append('      - command: "%s"' % show_cmd)
    lines.append(
        '        transcript: "transcripts/%s/scenarios/%s/before.txt"' % (module_name, state_name),
    )
    lines.append('      - command: "configure terminal"')
    lines.append('        transcript: "transcripts/generic_empty_return.txt"')

    for cmd in phase["commands"]:
        escaped = cmd.replace('"', '\\"')
        lines.append('      - command: "%s"' % escaped)
        lines.append('        transcript: "transcripts/generic_empty_return.txt"')

    lines.append('      - command: "end"')
    lines.append('        transcript: "transcripts/generic_empty_return.txt"')
    lines.append('      - command: "%s"' % show_cmd)
    lines.append(
        '        transcript: "transcripts/%s/scenarios/%s/after.txt"' % (module_name, state_name),
    )
    lines.append('      - command: "%s"' % show_cmd)
    lines.append(
        '        transcript: "transcripts/%s/scenarios/%s/after.txt"' % (module_name, state_name),
    )

    return "\n".join(lines)


# ======================================================================
# Inventory generation
# ======================================================================


def generate_cisshgo_inventory(module_name, state_names):
    scenario_name = module_to_scenario_name(module_name)
    lines = [
        "---",
        "# CISSHGO server inventory for the %s scenario." % scenario_name,
        "# Port layout:",
        "#   10000 - %s platform (gathered / parsed / rendered)" % module_name,
    ]
    for idx, state in enumerate(state_names):
        scenario_id = module_to_scenario_id(module_name, state)
        lines.append("#   %d - %s" % (10001 + idx, scenario_id))

    lines.append("devices:")
    lines.append("  - platform: %s" % module_name)
    lines.append("    count: 1")
    for state in state_names:
        scenario_id = module_to_scenario_id(module_name, state)
        lines.append("  - scenario: %s" % scenario_id)
        lines.append("    count: 1")

    return "\n".join(lines) + "\n"


def generate_ansible_inventory(module_name, state_names):
    scenario_name = module_to_scenario_name(module_name)
    lines = [
        "---",
        "# Ansible inventory for the %s molecule scenario." % scenario_name,
        "# Network vars scoped to ios_cisshgo group to prevent localhost leakage.",
        "all:",
        "  children:",
        "    ios_cisshgo:",
        "      vars:",
        "        ansible_connection: ansible.netcommon.network_cli",
        "        ansible_network_os: cisco.ios.ios",
        "        ansible_user: admin",
        "        ansible_password: admin",
        "        ansible_host: 127.0.0.1",
        "        ansible_become: true",
        "        ansible_become_method: enable",
        "        ansible_become_password: admin",
        '        ansible_ssh_common_args: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"',
        "      children:",
    ]

    # Gathered (platform, port 10000)
    group = "%s_gathered" % module_name
    host = "cisshgo-%s-gathered" % scenario_name
    lines.append("        %s:" % group)
    lines.append("          hosts:")
    lines.append("            %s:" % host)
    lines.append("              ansible_port: 10000")

    # Stateful scenarios (ports 10001+)
    for idx, state in enumerate(state_names):
        group = "%s_%s" % (module_name, state)
        host = "cisshgo-%s-%s" % (scenario_name, state)
        lines.append("        %s:" % group)
        lines.append("          hosts:")
        lines.append("            %s:" % host)
        lines.append("              ansible_port: %d" % (10001 + idx))

    return "\n".join(lines) + "\n"


# ======================================================================
# Molecule scenario file generation
# ======================================================================


def generate_molecule_yml(module_name, scenario_name, state_names):
    platforms = ["  - name: cisshgo-%s-gathered" % scenario_name]
    for state in state_names:
        platforms.append("  - name: cisshgo-%s-%s" % (scenario_name, state))

    return """---
# Molecule scenario: %(scenario)s
# Runs cisco.ios.%(module)s integration tests against CISSHGO.
# Usage: cd cisco/ios/extensions && molecule test -s %(scenario)s

driver:
  name: default

platforms:
%(platforms)s

ansible:
  executor:
    args:
      ansible_playbook:
        - --inventory=${MOLECULE_SCENARIO_DIRECTORY}/../cisshgo_fixtures/inventories/ansible/%(scenario)s.yaml
  env:
    ANSIBLE_FORCE_COLOR: "true"
    ANSIBLE_HOST_KEY_CHECKING: "false"
    ANSIBLE_DEPRECATION_WARNINGS: "false"

provisioner:
  name: ansible
  playbooks:
    create: ../_shared/create.yml
    converge: converge.yml
    verify: ../_shared/verify.yml
    destroy: ../_shared/destroy.yml

scenario:
  test_sequence:
    - create
    - converge
    - verify
    - destroy

prerun: false

verifier:
  name: ansible
...
""" % {
        "scenario": scenario_name,
        "module": module_name,
        "platforms": "\n".join(platforms),
    }


def generate_vars_yml(scenario_name, state_names):
    port_lines = []
    port_lines.append("  - 10000   # gathered / parsed / rendered")
    for idx, state in enumerate(state_names):
        port_lines.append("  - %d   # %s" % (10001 + idx, state))

    return """---
# Inputs for the shared _shared/{create,destroy,verify}.yml playbooks.
scenario_name: %(scenario)s
listener_ports:
%(ports)s
""" % {
        "scenario": scenario_name,
        "ports": "\n".join(port_lines),
    }


def yaml_dump_config(config, indent=8):
    """
    Convert a config dict/list to YAML string with proper indentation.
    Uses PyYAML if available, otherwise does a simple serialisation.
    """
    if config is None:
        return ""

    if HAS_YAML:
        dumped = yaml.dump(config, default_flow_style=False).rstrip()
        # Indent each line
        prefix = " " * indent
        lines = dumped.split("\n")
        return "\n".join(prefix + line for line in lines)

    # Fallback: simple formatting for common structures
    if isinstance(config, dict):
        lines = []
        prefix = " " * indent
        for k, v in config.items():
            if isinstance(v, str):
                lines.append('%s%s: "%s"' % (prefix, k, v))
            else:
                lines.append("%s%s: %s" % (prefix, k, v))
        return "\n".join(lines)

    return " " * indent + str(config)


def generate_converge_yml(
    module_name,
    collection,
    state_names,
    matched_phases,
    test_vars,
    cwd,
):
    """
    Generate converge.yml with proper config blocks extracted from
    the actual integration test task files.
    """
    scenario_name = module_to_scenario_name(module_name)
    fqcn = "%s.%s" % (collection, module_name)
    vars_path = (
        "{{ playbook_dir }}/../../../tests/integration/targets/%s/vars/main.yaml" % module_name
    )

    plays = []

    # ------------------------------------------------------------------
    # Gathered play (always included)
    # ------------------------------------------------------------------
    # Determine assertion style: use symmetric_difference for list configs,
    # == for dict configs
    gathered_vars = test_vars.get("gathered", {}) if test_vars else {}
    gathered_config = gathered_vars.get("config")
    if isinstance(gathered_config, list):
        gathered_assert = (
            "          - \"{{ gathered['config'] "
            "| symmetric_difference(result['gathered']) | length == 0 }}\""
        )
    else:
        gathered_assert = "          - gathered['config'] == result['gathered']"

    plays.append(
        """# ====================================================================
# 1. GATHERED — stateless platform on port 10000
# ====================================================================
- name: "%(module)s — gathered"
  hosts: %(module)s_gathered
  gather_facts: false
  vars_files:
    - "%(vars_path)s"
  tasks:
    - name: Gather %(module)s facts
      register: result
      %(fqcn)s:
        state: gathered

    - name: Assert gathered config matches expected
      ansible.builtin.assert:
        that:
%(gathered_assert)s
          - result['changed'] == false
        fail_msg: "Gathered config does not match expected"
        success_msg: "Gathered config matches expected"
"""
        % {
            "module": module_name,
            "fqcn": fqcn,
            "vars_path": vars_path,
            "gathered_assert": gathered_assert,
        },
    )

    # ------------------------------------------------------------------
    # Stateful plays
    # ------------------------------------------------------------------
    section_num = 2
    for idx, state in enumerate(state_names):
        if state not in matched_phases:
            print("  Skipping converge play for '%s' — no matched phase" % state)
            continue

        phase = matched_phases[state]
        port = 10001 + idx

        # Try to extract exact config from the integration test task file
        test_file = find_test_task_file(module_name, state, cwd)
        extracted_config, _ = extract_module_config_from_test(test_file, module_name, collection)

        # Determine assertion style for before/after
        state_vars = test_vars.get(state, {}) if test_vars else {}
        has_before = "before" in state_vars
        has_after = "after" in state_vars
        has_commands = "commands" in state_vars

        # Check if before/after are lists (use symmetric_difference) or dicts (use ==)
        before_val = state_vars.get("before")
        after_val = state_vars.get("after")

        # Build config block
        if state in NO_CONFIG_STATES or extracted_config is None:
            config_block = ""
            if state not in NO_CONFIG_STATES and extracted_config is None:
                # Could not extract — leave a comment
                config_block = "        # config: <could not auto-extract — review manually>"
        else:
            # Format the config as YAML
            config_yaml = yaml_dump_config(extracted_config, indent=10)
            config_block = "        config:\n%s" % config_yaml

        # Build the module invocation
        if state in NO_CONFIG_STATES:
            module_call = "        state: %s" % state
        else:
            module_call = (
                "%s\n        state: %s" % (config_block, state)
                if config_block
                else "        state: %s" % state
            )

        # Build assertion tasks
        assertions = []

        if has_commands:
            if isinstance(state_vars.get("commands"), list) and len(state_vars["commands"]) > 1:
                assertions.append(
                    """
    - name: Assert that correct set of commands were generated
      ansible.builtin.assert:
        that:
          - "{{ %(state)s['commands'] | symmetric_difference(result['commands']) | length == 0 }}"
"""
                    % {"state": state},
                )
            else:
                assertions.append(
                    """
    - name: Assert that correct set of commands were generated
      ansible.builtin.assert:
        that:
          - "%(state)s['commands'] == result['commands']"
"""
                    % {"state": state},
                )

        if has_before:
            if isinstance(before_val, list):
                assertions.append(
                    """
    - name: Assert that before dicts are correctly generated
      ansible.builtin.assert:
        that:
          - "{{ %(state)s['before'] | symmetric_difference(result['before']) | length == 0 }}"
"""
                    % {"state": state},
                )
            else:
                assertions.append(
                    """
    - name: Assert that before dicts are correctly generated
      ansible.builtin.assert:
        that:
          - %(state)s['before'] == result['before']
"""
                    % {"state": state},
                )

        if has_after:
            if isinstance(after_val, list):
                assertions.append(
                    """
    - name: Assert that after dict is correctly generated
      ansible.builtin.assert:
        that:
          - "{{ %(state)s['after'] | symmetric_difference(result['after']) | length == 0 }}"
"""
                    % {"state": state},
                )
            else:
                assertions.append(
                    """
    - name: Assert that after dict is correctly generated
      ansible.builtin.assert:
        that:
          - %(state)s['after'] == result['after']
"""
                    % {"state": state},
                )

        assertions_str = "".join(assertions)

        # Build idempotency check
        idempotent_block = """
    - name: %(module_cap)s %(state)s (idempotent)
      register: result
      %(fqcn)s: *%(state)s_config

    - name: Assert that the previous task was idempotent
      ansible.builtin.assert:
        that:
          - result['changed'] == false
""" % {
            "module_cap": module_name.replace("_", " ").title(),
            "state": state,
            "fqcn": fqcn,
        }

        plays.append(
            """# ====================================================================
# %(num)d. %(STATE)s — stateful scenario on port %(port)d
# ====================================================================
- name: "%(module)s — %(state)s"
  hosts: %(module)s_%(state)s
  gather_facts: false
  vars_files:
    - "%(vars_path)s"
  tasks:
    - name: %(module_cap)s %(state)s
      register: result
      %(fqcn)s: &%(state)s_config
%(module_call)s
%(assertions)s%(idempotent)s"""
            % {
                "num": section_num,
                "STATE": state.upper(),
                "state": state,
                "module": module_name,
                "module_cap": module_name.replace("_", " ").title(),
                "fqcn": fqcn,
                "vars_path": vars_path,
                "port": port,
                "module_call": module_call,
                "assertions": assertions_str,
                "idempotent": idempotent_block,
            },
        )
        section_num += 1

    return "---\n" + "\n".join(plays) + "...\n"


# ======================================================================
# Main
# ======================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Generate a complete Molecule scenario from a network_cli transcript recording",
    )
    parser.add_argument("recording", help="Path to the JSONL recording file")
    parser.add_argument("--module", required=True, help="Module name (e.g., ios_hostname)")
    parser.add_argument(
        "--show-command",
        required=True,
        help='Show command (e.g., "show running-config | section ^hostname")',
    )
    parser.add_argument(
        "--collection",
        default="cisco.ios",
        help="Collection FQCN (default: cisco.ios)",
    )
    parser.add_argument(
        "--molecule-dir",
        help="Molecule extensions directory (default: auto-detect from cwd)",
    )
    parser.add_argument(
        "--state-names",
        help="Comma-separated stateful state names (default: auto-detect)",
    )
    parser.add_argument(
        "--vars-file",
        help="Path to vars/main.yaml (default: auto-detect from module name)",
    )

    args = parser.parse_args()

    cwd = Path.cwd()

    # ------------------------------------------------------------------
    # Resolve molecule dir
    # ------------------------------------------------------------------
    if args.molecule_dir:
        molecule_dir = Path(args.molecule_dir)
    else:
        candidates = [
            cwd / "extensions" / "molecule",
            cwd,
        ]
        molecule_dir = None
        for c in candidates:
            if (c / "_shared" / "create.yml").exists() or (c / "cisshgo_fixtures").exists():
                molecule_dir = c
                break
        if molecule_dir is None:
            molecule_dir = cwd / "extensions" / "molecule"
            print("Warning: Could not auto-detect molecule dir, using %s" % molecule_dir)

    # ------------------------------------------------------------------
    # Load the recording
    # ------------------------------------------------------------------
    entries = load_recording(args.recording)
    print("Loaded %d entries from %s" % (len(entries), args.recording))

    # ------------------------------------------------------------------
    # Load integration test vars
    # ------------------------------------------------------------------
    vars_path = None
    test_vars = None

    if args.vars_file:
        vars_path = Path(args.vars_file)
    else:
        vars_path = find_vars_file(args.module, cwd)

    if vars_path and vars_path.exists():
        test_vars = load_vars(vars_path)
        print("Loaded test vars from %s" % vars_path)
        if test_vars:
            available_states = [
                k
                for k in test_vars
                if isinstance(test_vars[k], dict) and "commands" in test_vars[k]
            ]
            print("  States with commands: %s" % ", ".join(available_states))
    else:
        print(
            "Warning: Could not find vars/main.yaml — phase matching will use positional fallback"
        )

    # ------------------------------------------------------------------
    # Determine state names
    # ------------------------------------------------------------------
    if args.state_names:
        state_names = args.state_names.split(",")
    elif test_vars:
        # Auto-detect: states that have 'commands' key and are not offline
        state_names = [
            k
            for k in test_vars
            if isinstance(test_vars[k], dict)
            and "commands" in test_vars[k]
            and k not in OFFLINE_STATES
        ]
        print("Auto-detected stateful states: %s" % ", ".join(state_names))
    else:
        state_names = ["merged", "replaced"]
        print("Using default state names: %s" % ", ".join(state_names))

    # ------------------------------------------------------------------
    # Segment the recording
    # ------------------------------------------------------------------
    phases = segment_recording(entries, args.show_command)
    gathered_phases = [p for p in phases if p["type"] == "gathered"]
    stateful_phases = [p for p in phases if p["type"] == "stateful"]
    print(
        "\nDetected %d phases total: %d gathered, %d stateful"
        % (len(phases), len(gathered_phases), len(stateful_phases)),
    )

    for i, phase in enumerate(phases):
        if phase["type"] == "gathered":
            print("  [%d] gathered (show: %d chars)" % (i, len(phase["show_response"])))
        else:
            cmds_str = ", ".join(phase["commands"][:3])
            if len(phase["commands"]) > 3:
                cmds_str += "..."
            print(
                "  [%d] stateful (cmds: [%s], before: %d chars, after: %d chars)"
                % (i, cmds_str, len(phase["show_before"]), len(phase["show_after"])),
            )

    # ------------------------------------------------------------------
    # Match phases to states using expected commands
    # ------------------------------------------------------------------
    print("\n--- Phase matching ---")
    matched_phases = match_phases_to_states(phases, state_names, test_vars)

    if not matched_phases:
        print("ERROR: No phases matched any states. Cannot generate scenario.")
        print("  Check that --show-command matches what appears in the recording")
        print("  and that --state-names correspond to states in vars/main.yaml")
        sys.exit(1)

    matched_state_names = [s for s in state_names if s in matched_phases]
    print("Matched %d of %d states" % (len(matched_state_names), len(state_names)))

    # ------------------------------------------------------------------
    # Generate outputs
    # ------------------------------------------------------------------
    scenario_name = module_to_scenario_name(args.module)
    fixtures_dir = molecule_dir / "cisshgo_fixtures"
    transcripts_dir = fixtures_dir / "transcripts" / args.module
    scenario_dir = molecule_dir / scenario_name

    # 1. Write transcript files
    print("\n--- Transcript files ---")

    # Gathered transcript
    if gathered_phases:
        write_text(transcripts_dir / "gathered.txt", gathered_phases[0]["show_response"])
        print("  Wrote transcripts/%s/gathered.txt" % args.module)
    elif matched_phases:
        # Use the first matched phase's before as gathered
        first_phase = list(matched_phases.values())[0]
        write_text(transcripts_dir / "gathered.txt", first_phase["show_before"])
        print("  Wrote transcripts/%s/gathered.txt (from first matched before)" % args.module)

    # Stateful transcripts — only for matched states
    for state in matched_state_names:
        phase = matched_phases[state]
        sdir = transcripts_dir / "scenarios" / state
        write_text(sdir / "before.txt", phase["show_before"])
        write_text(sdir / "after.txt", phase["show_after"])
        print(
            "  Wrote transcripts/%s/scenarios/%s/ (before.txt, after.txt) — commands: %s"
            % (args.module, state, phase["commands"]),
        )

    # 2. Transcript map fragment
    print("\n--- Transcript map ---")
    platform_entry = generate_platform_entry(args.module, args.show_command)
    scenario_entries = []
    for state in matched_state_names:
        scenario_entries.append(
            generate_scenario_entry(args.module, state, args.show_command, matched_phases[state]),
        )

    fragment = (
        "# Add this platform under 'platforms:' in transcript_map.yaml:\n\n"
        + platform_entry
        + "\n# Add these scenarios under 'scenarios:' in transcript_map.yaml:\n\n"
        + "\n\n".join(scenario_entries)
        + "\n"
    )

    fragment_path = fixtures_dir / ("transcript_map_fragment_%s.yaml" % scenario_name)
    write_text(fragment_path, fragment)
    print("  Wrote %s" % fragment_path.name)

    # 3. CISSHGO inventory
    print("\n--- CISSHGO inventory ---")
    cisshgo_inv = generate_cisshgo_inventory(args.module, matched_state_names)
    cisshgo_inv_path = fixtures_dir / "inventories" / "cisshgo" / ("%s.yaml" % scenario_name)
    write_text(cisshgo_inv_path, cisshgo_inv)
    print("  Wrote inventories/cisshgo/%s.yaml" % scenario_name)

    # 4. Ansible inventory
    print("\n--- Ansible inventory ---")
    ansible_inv = generate_ansible_inventory(args.module, matched_state_names)
    ansible_inv_path = fixtures_dir / "inventories" / "ansible" / ("%s.yaml" % scenario_name)
    write_text(ansible_inv_path, ansible_inv)
    print("  Wrote inventories/ansible/%s.yaml" % scenario_name)

    # 5. Molecule scenario files
    print("\n--- Molecule scenario ---")
    scenario_dir.mkdir(parents=True, exist_ok=True)

    mol_yml = generate_molecule_yml(args.module, scenario_name, matched_state_names)
    write_text(scenario_dir / "molecule.yml", mol_yml)
    print("  Wrote %s/molecule.yml" % scenario_name)

    vars_yml = generate_vars_yml(scenario_name, matched_state_names)
    write_text(scenario_dir / "vars.yml", vars_yml)
    print("  Wrote %s/vars.yml" % scenario_name)

    converge_yml = generate_converge_yml(
        args.module,
        args.collection,
        matched_state_names,
        matched_phases,
        test_vars,
        cwd,
    )
    write_text(scenario_dir / "converge.yml", converge_yml)
    print("  Wrote %s/converge.yml" % scenario_name)

    print("\nDone! Next steps:")
    print("  1. Merge %s into transcript_map.yaml" % fragment_path.name)
    print("  2. Review converge.yml for correctness")
    print("  3. Run: cd extensions && molecule test -s %s" % scenario_name)


if __name__ == "__main__":
    main()
