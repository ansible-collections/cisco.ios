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

## Classify the Task

Read the user's request and classify it into one of four contexts. Then read **only** the `CONTEXT.md` in the matching directory — it tells you exactly which reference files to load.

| Context | Directory | Pick when the user wants to... |
|---------|-----------|-------------------------------|
| Development | `development/` | Create/modify a module, fix a bug, add a feature, update parsers/argspec/config, fix docs |
| Onboarding | `onboarding/` | Understand the codebase, learn the RM pattern, ramp up, "how does this work", "walk me through" |
| Triage & Debugging | `debugging/` | Reproduce a GitHub issue, debug CI failure, investigate test failure, validate a bug report |
| Testing | `testing-ctx/` | Write unit/molecule tests, find test gaps, add test coverage |

If the task spans multiple contexts or is ambiguous, default to **Development** (broadest file set).

Do NOT read the reference files in this directory directly — each `CONTEXT.md` tells you exactly which files to read and in what order.
