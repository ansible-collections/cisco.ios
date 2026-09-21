# Testing Context

You are writing unit tests, molecule tests, or finding test coverage gaps.

## Read This File

1. **Testing Patterns** — `../testing.md` — Unit test boilerplate, molecule test pattern, coverage gap detection, writing missing test cases

## Supporting Files (read only if needed)

2. **CI Debugging** — `../ci_debugging.md` — If tests fail in CI and you need to debug the pipeline
3. **Cheatsheet** — `../cheatsheet.md` — Quick reference for test commands and file paths

## Key Reminders

- Every module needs tests for all 7 states + idempotency for each stateful state (minimum 11 test methods).
- Always include an idempotency test (second run: `changed=false`).
- For molecule tests, update `transcript_map.yaml` and add CISSHGO transcript files.
- Run `pytest tests/unit/modules/network/ios/test_ios_<resource>.py -v` to verify locally.
