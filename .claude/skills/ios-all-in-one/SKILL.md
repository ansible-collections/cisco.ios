---
name: ios-all-in-one
description: >
  Cisco IOS collection all-in-one skill — provides full context about collection structure,
  resource module development, IOS CLI commands, GitHub issue triage, CI failure debugging,
  documentation review, test coverage gaps, and plain-language explanation of the RM flow.
  Trigger when the user mentions:
  "new module", "resource module", "add module", "create module", "implement module",
  "github issue", "reproduce issue", "triage issue", "validate issue", "check issue",
  "CI failure", "CI failing", "upstream test", "test failure", "pipeline failure", "build failed",
  "onboard", "ramp up", "collection structure", "how does this work", "walk me through",
  "fix bug", "fix typo", "documentation", "fix docs", "update docs", "missing example",
  "missing test", "test coverage", "add test", "write test", "missing testcase",
  "parser", "rm_templates", "argspec", "facts class", "config class", "getval", "setval",
  "IOS command", "show running-config", "cisco ios", "IOS-XE", "cisco command",
  "molecule test", "unit test", "sanity test", "CISSHGO", "transcript",
  "explain resource module", "how does module work", "module flow",
  "idempotency", "idempotent", "changed true on second run",
  "action plugin", "runtime.yml", "facts registry",
  "changelog", "changelog fragment", "release",
  or any task involving cisco.ios module development, debugging, review, or onboarding.
---

# Cisco IOS Ansible Collection — Skill

You are working in the `cisco.ios` Ansible network collection (`ansible_collections/cisco/ios`).
Repository: https://github.com/ansible-collections/cisco.ios
This collection manages Cisco IOS and IOS-XE device configuration via `network_cli` connection.

## Reference Files

Detailed context is split into topic-specific files. Read the relevant file(s) for the task at hand:

| Topic | File | When to read |
|-------|------|-------------|
| RM architecture, 5-file pattern, creating new modules, coding conventions | `rm_architecture.md` | Creating/modifying resource modules |
| Want/have state logic, comparison tables, list_to_dict, compval, plain-language flow | `want_have_logic.md` | Understanding or debugging state behavior |
| IOS CLI commands, show commands, parser generation guide | `ios_commands.md` | Building parsers, mapping CLI to structured data |
| Reproduce & validate GitHub issues | `reproduce_github_issue.md` | Reproducing or validating a reported issue |
| CI failure debugging | `ci_debugging.md` | Diagnosing test/build/lint failures |
| Testing patterns & coverage gaps | `testing.md` | Writing or finding missing tests |
| Documentation review & typo fixing | `documentation_review.md` | Fixing docs, examples, or RETURN blocks |
| Quick-reference cheatsheet | `cheatsheet.md` | Fast lookup of directories, commands, patterns |

All files are in `.claude/skills/ios-all-in-one/`.

---

## Collection Overview

- **Namespace**: `cisco.ios` (version 11.5.0)
- **Dependencies**: `ansible.netcommon` >= 8.5.2, `ansible.utils`
- **Connection**: `network_cli` (SSH via libssh or paramiko)
- **Python**: 3.9+
- **CI**: GitHub Actions (`.github/workflows/tests.yml`) — sanity, unit, molecule (CISSHGO)

## Directory Structure

```
cisco/ios/
├── galaxy.yml                           # namespace: cisco, name: ios
├── plugins/
│   ├── modules/                         # All modules: ios_<resource>.py
│   ├── module_utils/network/ios/
│   │   ├── argspec/<resource>/          # ArgumentSpec classes
│   │   ├── config/<resource>/           # Config classes (ResourceModule)
│   │   ├── facts/<resource>/            # Facts classes
│   │   ├── facts/facts.py              # Central facts registry
│   │   ├── rm_templates/<resource>.py   # Parser templates (NetworkTemplate)
│   │   └── utils/utils.py              # Shared helpers
│   ├── action/                          # Action plugins (boilerplate per module)
│   ├── cliconf/                         # CLI conf plugin
│   └── terminal/                        # Terminal plugin
├── tests/
│   ├── unit/modules/network/ios/        # Unit tests
│   └── integration/targets/             # Integration targets
├── extensions/molecule/                 # Molecule tests (CISSHGO-based)
│   ├── cisshgo_fixtures/                # Transcripts, inventories, transcript_map.yaml
│   └── <resource>/                      # Per-resource scenarios
├── .github/workflows/                   # CI workflows
├── meta/runtime.yml                     # Plugin routing
└── changelogs/fragments/                # Changelog entries
```

## Existing Modules (42)

| Category | Modules |
|----------|---------|
| **Interfaces** | `ios_interfaces`, `ios_l2_interfaces`, `ios_l3_interfaces` |
| **Routing** | `ios_bgp_global`, `ios_bgp_address_family`, `ios_ospfv2`, `ios_ospfv3`, `ios_ospf_interfaces`, `ios_static_routes` |
| **Policy** | `ios_route_maps`, `ios_prefix_lists`, `ios_acls`, `ios_acl_interfaces` |
| **L2 Switching** | `ios_vlans`, `ios_lag_interfaces`, `ios_lacp`, `ios_lacp_interfaces`, `ios_lldp_global`, `ios_lldp_interfaces` |
| **System** | `ios_hostname`, `ios_service`, `ios_banner`, `ios_system`, `ios_user` |
| **Management** | `ios_snmp_server`, `ios_logging_global`, `ios_ntp_global` |
| **VRF** | `ios_vrf`, `ios_vrf_global`, `ios_vrf_address_family`, `ios_vrf_interfaces` |
| **Overlay** | `ios_vxlan_vtep`, `ios_evpn_global`, `ios_evpn_evi`, `ios_evpn_ethernet` |
| **HA** | `ios_hsrp_interfaces`, `ios_bfd_interfaces`, `ios_bfd_templates` |
| **Utility** | `ios_command`, `ios_config`, `ios_facts`, `ios_ping` |

## Notes for the Agent

### Token Efficiency
- SKILL.md is the entry point — read only the topic file(s) relevant to the current task.
- Don't re-read reference files on every invocation if you already have the context.
- For issue triage, read only the specific module files involved in the bug report.
- For CI debugging, go straight to `gh run view` — don't re-read workflow files.

### Adaptive Behavior
- **New contributor**: Point them to `rm_architecture.md` and `want_have_logic.md` for the full picture.
- **Experienced contributor**: Jump straight to the task — they know the pattern.
- **Issue reporter**: Follow `github_issue_triage.md`. Focus on reproduction and root cause.
- **CI debugger**: Follow `ci_debugging.md`. Identify the failed job and read logs.
- **Doc fixer**: Follow `documentation_review.md`. Check DOCUMENTATION/EXAMPLES/RETURN blocks.
- **Test writer**: Follow `testing.md`. Find gaps and write missing test cases.

### When Reproducing GitHub Issues
1. Always fetch the issue first with `gh issue view`
2. Ask for device details (IOS version, platform) if not provided
3. Use `state: parsed` and `state: rendered` for offline validation — no device needed
4. Write a failing unit test that demonstrates the bug before fixing
5. After fixing, verify all existing tests still pass

### When Debugging CI
1. Use `gh run view <id> --log-failed` to get just the failure output
2. For upstream test failures (`unit-source` fails but `unit-galaxy` passes), check netcommon HEAD
3. For molecule failures, check transcript_map.yaml for missing commands
4. For sanity failures, the error message usually tells you exactly what to fix
