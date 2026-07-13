# Known CI Failure Patterns — cisco.ios

Check this file before investigating any CI failure. Most failures match a known pattern.

---

## Pattern 1: Galaxy Version Lag

**Symptom:** `unit-galaxy` job fails, `unit-source` job passes.

**Why:** `unit-galaxy` installs `ansible.netcommon` from Galaxy (last release).
`unit-source` installs from the GitHub `main` branch. If a bug was fixed in netcommon main
but a new Galaxy release hasn't been cut yet, galaxy tests fail.

**Diagnosis:**
```bash
# Check if fix exists in netcommon main but isn't released
gh pr list --repo ansible-collections/ansible.netcommon --state merged --limit 10
# Compare with Galaxy release date
```

**Fix:** Request a netcommon Galaxy release. If urgent, temporarily pin the test to git source.

---

## Pattern 2: Persistent Connection Timeout Leak (`commit_confirm`)

**Symptom:** Error `ansible_command_timeout can't be greater than commit_confirm_timeout`
appears on the task **after** the deliberate timeout test — not on the test itself.

**Root Cause (4-step trace):**
1. `include_tasks vars: ansible_command_timeout: 61` — task_executor passes 61 to the
   persistent daemon via `conn.set_options(direct=options)`
2. The daemon caches `persistent_command_timeout = 61` in memory
3. The `include_tasks` scope ends — but **the daemon does NOT reset**; it retains 61
4. The next task's `ios.py configure()` reads `get_option("persistent_command_timeout")` → 61,
   then checks `61 > 60` → raises `ValueError`

**Files Involved:**
- `plugins/cliconf/ios.py` line ~294 — validation that raises the error
- `tests/integration/targets/ios_cliconf/tests/common/commit_conf.yaml` — where to add fix
- `tests/integration/targets/ios_cliconf/vars/main.yaml` — baseline `ansible_command_timeout: 30`
- `ansible.netcommon/plugins/connection/network_cli.py` lines ~1172/1321 — daemon timeout handling

**Fix:**
```yaml
# Add after the assert task in commit_conf.yaml
- name: Reset persistent connection to clear cached timeout
  ansible.builtin.meta: reset_connection
```

This forces `_connect()` to re-run, reading the fresh 30s value instead of the cached 61s.

---

## Pattern 3: `remove_internal_keys` Error

**Symptom:** Test fails with `AttributeError` or `KeyError` related to `remove_internal_keys`.

**Why:** Same as Pattern 1 — bug fixed in netcommon main, not yet released to Galaxy.

**Fix:** Same as Pattern 1 — request netcommon release.

---

## Pattern 4: `devel` / `milestone` Only Failure

**Symptom:** Only the `devel` or `milestone` ansible-core version jobs fail.
Stable versions (2.16, 2.18, 2.19) all pass.

**Why:** ansible-core introduced a deprecation or API change that we haven't adapted to yet.
Common examples:
- `exit_json(warnings=[...])` deprecated → use `module.warn()` instead
- Python version requirement bumped (devel requires ≥3.13)
- Internal plugin API changed

**Diagnosis:**
```bash
# Check ansible-core changelog for the failing version
gh release list --repo ansible/ansible --limit 5
# Or check the PR that introduced the change
gh search issues --repo ansible/ansible "deprecation" --label "changelog"
```

**Fix:** Update the affected code to support the new API. If the change isn't released yet,
mark as `needs_revision` and track with a follow-up issue.

---

## Pattern 5: Missing `Depends-On` Between PRs

**Symptom:** PR passes CI on its own but fails when merged because a required
upstream change (usually in netcommon) isn't merged yet.

**Fix:** Add a `Depends-On: <PR URL>` line to the PR description. Merge in correct order:
netcommon first, then cisco.ios.

---

## Pattern 6: Sonar Not a Required Status Check

**Symptom:** PR merges despite Sonar quality gate failure.

**Why:** Sonar is not configured as a required status check in branch protection.

**Fix:** If this matters for the PR, flag it in review. Add Sonar as required check in
Settings → Branches if the team decides to enforce it.

---

## Pattern 7: Python Version Mismatch (devel only)

**Symptom:**
```
ERROR: Package 'ansible-core' requires a different Python: 3.12.x not in '>=3.13'
```

**Why:** ansible-core `devel` branch bumped its minimum Python requirement to 3.13,
but the GitHub Actions runner still uses Python 3.12 by default.

**Fix:** Update `.github/workflows/tests.yml` to use Python 3.13 when testing against devel:
```yaml
python-version: "${{ matrix.ansible == 'devel' && '3.13' || '3.12' }}"
```
