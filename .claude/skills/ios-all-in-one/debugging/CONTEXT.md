# Triage & Debugging Context

You are reproducing a GitHub issue, debugging a CI failure, or investigating a test failure.

## For GitHub Issue Triage

Read: `../reproduce_github_issue.md` — 7-step triage workflow (fetch issue, understand, reproduce, root-cause, validate fix)

## For CI Failure Debugging

Read: `../ci_debugging.md` — CI pipeline structure, common failure patterns per job, running checks locally

## Supporting Files (read as needed)

- **Cheatsheet** — `../cheatsheet.md` — Common bug patterns table, CI job quick reference, shell commands
- **Want/Have Logic** — `../want_have_logic.md` — Only if the bug involves state comparison or idempotency

## Key Reminders

- Always start with `gh issue view <number>` or `gh run view <id> --log-failed`.
- Use `state: parsed` and `state: rendered` for offline validation — no device needed.
- Ask for device details (IOS version, platform) if not provided in the issue.
- For upstream failures (`unit-source` fails but `unit-galaxy` passes), check netcommon HEAD.
- Write a failing unit test that demonstrates the bug before fixing.
