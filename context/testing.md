# Testing Guide — cisco.ios

## Test Types and When to Use Each

| Type | Command | When |
|------|---------|------|
| Sanity | `ansible-test sanity` | Always — runs on every PR |
| Unit | `tox --ansible` or `pytest` | Always — mocked, no device needed |
| Integration | CML lab or `-e` flags | For new modules or RM changes |

---

## Sanity Tests

```bash
# Default (runs in docker, matches CI exactly)
ansible-test sanity --docker default

# Specific files only (faster for focused checks)
ansible-test sanity --docker default plugins/modules/ios_vlans.py

# Without docker (if docker not available)
ansible-test sanity --venv
```

Sanity checks run: PEP8 lint, import validation, DOCUMENTATION block validation,
ignore file consistency.

**Sanity ignore files:** `tests/sanity/ignore-*.txt` — Add known acceptable violations here
(e.g. `plugins/module_utils/network/ios/ios.py use-argspec-type-path # legacy`).

---

## Unit Tests

### Galaxy variant (matches `unit-galaxy` CI job)
Uses the last published Galaxy release of netcommon:
```bash
python -m tox --ansible -e sanity-py3.12-2.19 --conf tox-ansible.ini
```

### Source variant (matches `unit-source` CI job)
Uses the latest `main` branch of netcommon:
```bash
pip install git+https://github.com/ansible-collections/ansible.netcommon.git
pytest tests/unit -v
```

If `unit-source` passes but `unit-galaxy` fails → **Pattern 1 (Galaxy Version Lag)**.
See `ci-patterns.md`.

### Running a single unit test
```bash
pytest tests/unit/modules/network/ios/test_ios_vlans.py -v
```

### Unit test structure
```
tests/unit/modules/network/ios/
  test_ios_<rm>.py          # One file per module
  fixtures/                 # Text files with sample device output
    ios_<rm>.cfg            # Sample running-config snippets
```

Unit tests use `unittest.mock` to mock the device connection — no real device needed.

---

## Integration Tests

Integration tests run against **real CML lab devices** (IOS / IOS-XE).

### Structure
```
tests/integration/targets/ios_<rm>/
  tasks/
    main.yml                # Entry point
  tests/
    ios/
      overridden.yaml       # overridden state tests
      merged.yaml           # merged state tests
      replaced.yaml         # replaced state tests
      deleted.yaml          # deleted state tests
      gathered.yaml         # gathered state tests
      rendered.yaml         # rendered state tests (offline)
      parsed.yaml           # parsed state tests (offline)
  vars/
    main.yml                # Test variables
  defaults/
    main.yml                # Default values
```

### Running integration tests locally (with device access)
```bash
# Requires access to CML lab
ansible-test integration ios_vlans -v \
  --inventory tests/integration/inventory.networking \
  -e "ansible_network_os=cisco.ios.ios"
```

### Offline tests (rendered/parsed — no device needed)
```bash
ansible-test integration ios_vlans -v \
  --tags rendered,parsed
```

---

## CI Ansible Version Matrix

Tests run against all of these ansible-core versions:

```
stable-2.16    (LTS)
stable-2.18
stable-2.19    (current stable)
milestone      (pre-release)
devel          (main branch)
```

Two transport variants per version:
- `libssh` (primary — more sensitive to stale connection state)
- `paramiko` (parallel CI for coverage)

---

## Debugging a Test Failure

```bash
# View failed CI log
gh run view <run-id> --log-failed

# Download full log for large failures
gh run download <run-id>

# Re-run failed jobs only
gh run rerun <run-id> --failed

# Get the exact ansible-test command CI uses
# Look in .github/workflows/tests.yml under the failing job
```

### Common pytest flags for debugging
```bash
pytest tests/unit/modules/network/ios/test_ios_vlans.py \
  -v \                      # verbose
  -s \                      # show stdout (print statements)
  -k "test_merged_state" \  # run only tests matching name
  --tb=long                 # long traceback format
  --pdb                     # drop into debugger on failure
```
