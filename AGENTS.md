# AGENTS.md — cisco.ios

This file provides guidance to Claude Code and other AI tools when working in this repository.

**For human developers:** See the [Ansible Network Collection Guide](https://docs.ansible.com/ansible/latest/network/dev_guide/).

---

## ⚠️ CRITICAL: Read Before Any Task

1. **Use TodoWrite** to track steps for any multi-step task
2. **Check `context/ci-patterns.md`** before diagnosing CI failures — the answer is probably already there
3. **All 7 RM files must stay consistent** — never edit one without checking the others
4. **netcommon dependency is upstream** — fixes to connection/parsing bugs must go to netcommon first

---

## Quick Reference

```bash
# Sanity tests
ansible-test sanity --docker default

# Unit tests (Galaxy deps — what CI runs)
python -m tox --ansible -e sanity-py3.12-2.19 --conf tox-ansible.ini

# Unit tests (source deps — latest netcommon main)
pip install git+https://github.com/ansible-collections/ansible.netcommon.git
pytest tests/unit

# CI status
gh pr checks <number>
gh run view <run-id> --log-failed
```

| What | Where |
|------|-------|
| 45 resource modules | `plugins/modules/ios_*.py` |
| RM shared logic | `plugins/module_utils/network/ios/` |
| CLI connection plugin | `plugins/cliconf/ios.py` |
| Integration tests | `tests/integration/targets/ios_*/` |
| Main CI | `.github/workflows/tests.yml` |

---

## ⚠️ CI Failures — Check Patterns First

Before investigating any CI failure, read **`context/ci-patterns.md`**.

Known patterns (quick reference):

| Symptom | Pattern | Fix |
|---------|---------|-----|
| `unit-galaxy` fails, `unit-source` passes | Galaxy version lag | Cut netcommon release |
| `ansible_command_timeout > commit_confirm_timeout` on task AFTER the timeout test | Persistent connection state leak | Add `meta: reset_connection` in `commit_conf.yaml` |
| `remove_internal_keys` error | netcommon Galaxy lag | Same as pattern 1 |
| Only `devel`/`milestone` fails | ansible-core API change | Adapt to new API |

---

## ⚠️ Resource Module Changes — 7-File Rule

Every resource module (`ios_vlans`, `ios_interfaces`, etc.) spans **7 tightly coupled files**.
Changing one without updating the others causes silent failures.

```
plugins/modules/ios_<rm>.py                                    ← entry point
plugins/module_utils/network/ios/argspec/<rm>/<rm>.py          ← arg spec
plugins/module_utils/network/ios/config/<rm>/<rm>.py           ← CRUD logic
plugins/module_utils/network/ios/rm_templates/<rm>.py          ← parsers
plugins/module_utils/network/ios/facts/<rm>/<rm>.py            ← facts
plugins/module_utils/network/ios/facts/facts.py                ← registration (EDIT)
tests/unit/modules/network/ios/test_ios_<rm>.py                ← unit tests
```

See **`context/resource-modules.md`** for the full pattern.

---

## PR Review Checklist

```text
□ Create TodoWrite list for review steps
□ Get diff: gh pr diff <number>
□ If RM change — verify all 7 files are touched
□ Changelog fragment exists in changelogs/fragments/
□ Unit tests cover the changed code path
□ rm_templates compval matches result key structure
□ No hardcoded timeout values (use ansible_command_timeout var)
□ Check for cross-collection impact (netcommon/utils dep change?)
□ Run: ansible-test sanity --docker default <changed files>
```

---

## Available Skills

Installed via Carbonite from harness + content-ai-skills:

| Trigger | Skill | What it does |
|---------|-------|--------------|
| `triage network issue` | network-triage-workflow | Triage CI failures and GitHub issues with known patterns |
| `run collection tests` | network-test-workflow | Run sanity/unit/integration with ansible-test |
| `fix bug` | bugfix-workflow | Root cause → fix → regression test → PR |
| `implement story` | story-implementation-workflow | Jira story → code → PR |
| `review PR` | review-pr-workflow | Structured PR review with severity findings |
| `scan network issues` | network-collection-triage | Weekly bulk triage across all network repos |

---

## Context Files

Read these on-demand for deeper guidance:

- [`context/resource-modules.md`](context/resource-modules.md) — 7-file RM pattern, compval pitfalls, naming rules
- [`context/ci-patterns.md`](context/ci-patterns.md) — All known CI failure patterns with root causes and fixes
- [`context/testing.md`](context/testing.md) — ansible-test, tox-ansible, CML integration tests
- [`context/dependencies.md`](context/dependencies.md) — netcommon/utils dependency chain and cascade risks
