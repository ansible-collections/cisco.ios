# Cisco IOS Collection — Quick Reference Cheatsheet

## Directory Quick-Find

| I need to... | Look at |
|---|---|
| Add a new module | `plugins/modules/ios_<resource>.py` |
| Define argument spec | `plugins/module_utils/network/ios/argspec/<resource>/<resource>.py` |
| Write config logic | `plugins/module_utils/network/ios/config/<resource>/<resource>.py` |
| Write CLI parsers | `plugins/module_utils/network/ios/rm_templates/<resource>.py` |
| Write facts class | `plugins/module_utils/network/ios/facts/<resource>/<resource>.py` |
| Register new resource | `plugins/module_utils/network/ios/facts/facts.py` (FACT_RESOURCE_SUBSETS) |
| Add action plugin | `plugins/action/ios_<resource>.py` |
| Add runtime routing | `meta/runtime.yml` |
| Write unit tests | `tests/unit/modules/network/ios/test_ios_<resource>.py` |
| Write molecule tests | `extensions/molecule/<resource>/` |
| Add CISSHGO transcripts | `extensions/molecule/cisshgo_fixtures/` |
| Add changelog | `changelogs/fragments/<slug>.yaml` |
| Check CI config | `.github/workflows/tests.yml` |
| See collection metadata | `galaxy.yml` |
| Shared utilities | `plugins/module_utils/network/ios/utils/utils.py` |
| Connection helpers | `plugins/module_utils/network/ios/ios.py` |

## New Resource Module — File Checklist

```
[ ] plugins/modules/ios_<resource>.py
[ ] plugins/module_utils/network/ios/argspec/<resource>/__init__.py
[ ] plugins/module_utils/network/ios/argspec/<resource>/<resource>.py
[ ] plugins/module_utils/network/ios/config/<resource>/__init__.py
[ ] plugins/module_utils/network/ios/config/<resource>/<resource>.py
[ ] plugins/module_utils/network/ios/rm_templates/<resource>.py
[ ] plugins/module_utils/network/ios/facts/<resource>/__init__.py
[ ] plugins/module_utils/network/ios/facts/<resource>/<resource>.py
[ ] plugins/module_utils/network/ios/facts/facts.py  (add import + FACT_RESOURCE_SUBSETS entry)
[ ] plugins/action/ios_<resource>.py
[ ] meta/runtime.yml  (add action + module redirect)
[ ] tests/unit/modules/network/ios/test_ios_<resource>.py
[ ] extensions/molecule/<resource>/molecule.yml
[ ] extensions/molecule/<resource>/converge.yml
[ ] extensions/molecule/<resource>/vars.yml
[ ] extensions/molecule/cisshgo_fixtures/transcript_map.yaml  (add platform entry)
[ ] extensions/molecule/cisshgo_fixtures/transcripts/ios_<resource>/  (add show output files)
[ ] extensions/molecule/cisshgo_fixtures/inventories/ansible/<resource>.yaml
[ ] extensions/molecule/cisshgo_fixtures/inventories/cisshgo/<resource>.yaml
[ ] changelogs/fragments/<resource>.yaml
```

## Common Commands

```bash
# Run unit tests for a specific module
python -m pytest tests/unit/modules/network/ios/test_ios_<resource>.py -v

# Run all unit tests
python -m pytest tests/unit/ -v

# Run sanity tests
ansible-test sanity --docker default

# Run a specific sanity test
ansible-test sanity --test validate-modules plugins/modules/ios_<resource>.py

# Run molecule test
cd extensions/molecule && molecule test -s <resource>

# Check a GitHub issue
gh issue view <number> --repo ansible-collections/cisco.ios

# View CI run logs
gh run view <run_id> --repo ansible-collections/cisco.ios
gh run view <run_id> --repo ansible-collections/cisco.ios --log-failed

# List recent CI runs
gh run list --repo ansible-collections/cisco.ios --limit 10

# Check upstream netcommon changes
gh api repos/ansible-collections/ansible.netcommon/commits?per_page=5
```

## Data Flow Trace

```
Playbook Task
    │
    ▼
Action Plugin (plugins/action/ios_<resource>.py)
    │  validates connection type = network_cli
    ▼
Module (plugins/modules/ios_<resource>.py)
    │  creates AnsibleModule with ArgSpec
    │  instantiates Config class
    ▼
Config Class (plugins/module_utils/.../config/<resource>/<resource>.py)
    │  extends ResourceModule
    │  calls execute_module()
    │     ├── Facts class gathers current config (self.have)
    │     ├── ArgSpec validates user input (self.want)
    │     ├── generate_commands() compares want vs have
    │     └── run_commands() applies changes to device
    ▼
Facts Class (plugins/module_utils/.../facts/<resource>/<resource>.py)
    │  runs show command on device via connection.get()
    │  passes output to RM Template parser
    ▼
RM Template (plugins/module_utils/.../rm_templates/<resource>.py)
    │  PARSERS list:
    │     getval regex  ──► parses CLI text → structured data
    │     setval jinja2  ──► generates CLI commands ← structured data
    ▼
Device (via ansible.netcommon network_cli connection)
```

## State Behavior Summary

| State | Reads Device? | Changes Device? | Requires `config`? | Requires `running_config`? |
|-------|:---:|:---:|:---:|:---:|
| merged | Yes | Yes | Yes | No |
| replaced | Yes | Yes | Yes | No |
| overridden | Yes | Yes | Yes | No |
| deleted | Yes | Yes | No* | No |
| purged | Yes | Yes | No* | No |
| gathered | Yes | No | No | No |
| rendered | No | No | Yes | No |
| parsed | No | No | No | Yes |

*deleted/purged: `config` is optional; if omitted, deletes ALL resources

## Common Bug Patterns

| Symptom | Likely Root Cause | Where to Fix |
|---------|------------------|--------------|
| Facts don't parse a config line | `getval` regex doesn't match the line format | `rm_templates/<resource>.py` |
| Wrong CLI command generated | `setval` Jinja2 template is incorrect | `rm_templates/<resource>.py` |
| Idempotency failure (changed on 2nd run) | Facts parse differently than command output | `rm_templates/<resource>.py` or `config/<resource>.py` |
| Missing config option | Not in argspec/parsers | Add to argspec + rm_templates + config parsers list |
| "not valid for this module" | Connection type wrong | Action plugin or user's inventory |
| KeyError in generate_commands | Missing key in want/have dict | `config/<resource>.py` |
| Version-specific failure | IOS version uses different CLI syntax | Add conditional regex in `rm_templates` |

## IOS CLI → Python Name Mapping Convention

| IOS CLI | Python Attribute | Argspec Key |
|---------|-----------------|-------------|
| `service-policy` | `service_policy` | `service_policy` |
| `ip access-group` | `ip_access_group` | `ip_access_group` |
| `GigabitEthernet0/1` | `GigabitEthernet0/1` | `name` (str) |
| `shutdown` / `no shutdown` | `enabled: False/True` | `enabled` (bool) |
| `no <command>` | Negate via `remval` or `setval` | Depends on parser |

## GitHub Issue Triage Workflow

```
1. gh issue view <number>
2. Identify: module, state, IOS version, running config
3. Read: rm_templates + config class for the affected module
4. Ask user for device details if not in issue
5. Reproduce with state: parsed (offline, no device needed)
6. Write failing unit test
7. Fix the root cause
8. Verify: all unit tests pass + idempotency
9. Create PR with changelog fragment
```

## CI Job Quick Reference

| Job Name | What It Checks | Common Fix |
|----------|---------------|------------|
| `changelog` | PR has fragment in `changelogs/fragments/` | Add YAML fragment |
| `build-import` | Collection builds + imports | Fix `galaxy.yml`, missing `__init__.py` |
| `ansible-lint` | Ansible-lint rules | Fix lint violations in playbooks/tasks |
| `sanity` | `ansible-test sanity` | Fix pep8/import/docs/validate-modules |
| `unit-galaxy` | Unit tests via galaxy install | Fix test assertions or module code |
| `unit-source` | Unit tests from git (netcommon+utils HEAD) | May be upstream breakage |
| `molecule` | CISSHGO integration tests | Fix transcripts/assertions/converge.yml |
