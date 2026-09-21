# Onboarding Context

You are helping someone understand the `cisco.ios` collection structure, the Resource Module pattern, or how modules work end-to-end.

## Read These Files (in order)

1. **Architecture** — `../rm_architecture.md` — The 5-file RM pattern, how all pieces fit together, base classes and dependencies
2. **Want/Have Logic** — `../want_have_logic.md` — Plain-language walkthrough of the module flow, state comparison tables, list_to_dict concept
3. **Cheatsheet** — `../cheatsheet.md` — Directory quick-find, data flow trace diagram, state behavior summary, common commands

## Supporting Files (read only if needed)

4. **IOS CLI Reference** — `../ios_commands.md` — Only if asked about specific IOS commands or CLI structure

## Key Reminders

- Start with the plain-language explanation in `want_have_logic.md` (section: "How a Resource Module Works").
- Use the Data Flow Trace diagram in `cheatsheet.md` to show the end-to-end flow.
- Point to `ios_hostname` as a simple concrete example to walk through.
- Tailor depth to the person's experience — don't overwhelm newcomers with every detail.
