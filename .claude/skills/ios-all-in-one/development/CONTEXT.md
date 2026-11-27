# Development Context

You are creating a new resource module, fixing a bug, adding a feature, or modifying an existing module in the `cisco.ios` collection.

## Read These Files (in order)

1. **Architecture** — `../rm_architecture.md` — The 5-file RM pattern, step-by-step module creation guide, coding conventions
2. **Want/Have Logic** — `../want_have_logic.md` — State comparison (merged/replaced/overridden/deleted), list_to_dict, compval
3. **IOS CLI Reference** — `../ios_commands.md` — CLI hierarchy, show commands, parser generation guide. Read only the sections relevant to your target resource.

## Supporting Files (read only if needed)

4. **Documentation** — `../documentation_review.md` — When writing or fixing DOCUMENTATION/EXAMPLES/RETURN blocks
5. **Cheatsheet** — `../cheatsheet.md` — Quick lookup for directory paths, commands, common bug patterns

## Key Reminders

- Write a failing unit test before fixing a bug.
- After fixing, verify idempotency (second run: `changed=false`).
- Add a changelog fragment in `changelogs/fragments/`.
- For `ios_commands.md`, read only the feature section you need — don't load the full 1000-line file.
