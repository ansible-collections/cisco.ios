# CI Failure Debugging

## CI Pipeline Structure (`.github/workflows/tests.yml`)

The CI runs these jobs via reusable workflows:

| Job | Reusable Workflow | What it checks |
|-----|------------------|----------------|
| `changelog` | `ansible-content-actions/.../changelog.yaml` | PR has a changelog fragment |
| `build-import` | `ansible-content-actions/.../build_import.yaml` | Collection builds and imports cleanly |
| `ansible-lint` | `ansible-content-actions/.../ansible_lint.yaml` | Ansible-lint passes |
| `sanity` | `ansible-content-actions/.../sanity.yaml` | `ansible-test sanity` (pep8, import, docs, etc.) |
| `unit-galaxy` | `ansible-content-actions/.../unit.yaml` | Unit tests via galaxy install |
| `unit-source` | `ansible-network/github_actions/.../unit_source.yml` | Unit tests from source (with netcommon+utils from git) |
| `molecule` | `ansible-network/github_actions/.../molecule.yml` | CISSHGO Molecule integration tests (libssh + paramiko) |
| `all_green` | (inline) | Gate check — fails if any above job failed |

## Debugging Steps

### 1. Check which job failed
```bash
gh run view <run_id> --repo ansible-collections/cisco.ios
gh run view <run_id> --repo ansible-collections/cisco.ios --log-failed
```

### 2. Common failure patterns

**Sanity failures:**
- `compile` — syntax error in Python file
- `import` — missing or circular import
- `pep8` — style violations (line length, whitespace)
- `validate-modules` — module documentation doesn't match argspec
- `pylint` — code quality issues
- Fix: run locally with `ansible-test sanity --test <test_name> plugins/modules/ios_<resource>.py`

**Unit test failures:**
- Assertion error in command comparison — expected commands don't match generated
- Fixture mismatch — running config fixture doesn't match what parser expects
- Fix: run locally with `python -m pytest tests/unit/modules/network/ios/test_ios_<resource>.py -v`

**Molecule failures:**
- CISSHGO transcript missing a command — add transcript entry
- Assertion error — expected values in vars.yml don't match actual
- Connection timeout — CISSHGO startup issue (usually CI infra, not code)
- Fix: check `extensions/molecule/cisshgo_fixtures/transcript_map.yaml` for missing entries

**Changelog missing:**
- PR needs a changelog fragment in `changelogs/fragments/`

**Build/import failures:**
- `galaxy.yml` syntax error
- Missing `__init__.py` in new directories
- Import error in module or module_utils

### 3. Upstream test context
The `report-status` job runs on schedule (daily cron `0 0 * * *`) and uploads results.
The `unit-source` job installs `ansible.netcommon` and `ansible.utils` from git (source),
so failures here can indicate upstream breaking changes in those dependencies.

If `unit-source` fails but `unit-galaxy` passes:
- A breaking change was introduced in netcommon or utils HEAD
- Check recent commits: `gh api repos/ansible-collections/ansible.netcommon/commits?per_page=5`

### 4. Running CI checks locally
```bash
# Sanity
ansible-test sanity --docker default

# Unit tests
python -m pytest tests/unit/ -v

# Molecule (requires CISSHGO)
cd extensions/molecule
molecule test -s <resource>
```
