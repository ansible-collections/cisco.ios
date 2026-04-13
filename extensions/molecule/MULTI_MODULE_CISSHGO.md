# Molecule + cisshgo: multiple resource modules (this collection)

This file is a **short pointer** for clone consumers. **Authoritative** workflow, port math, RTT notes, emit-order rules, and the **mandatory “run Molecule until green”** loop live in the Cursor skill:

**[`.cursor/skills/cisco-ios-molecule-cisshgo-integration/SKILL.md`](../../../../../.cursor/skills/cisco-ios-molecule-cisshgo-integration/SKILL.md)** (repo root; adjust if your clone nests `ansible_collections` differently)

**Skill overview + how to run Molecule:** **[`docs/User Guide.md`](../../../../../.cursor/skills/cisco-ios-molecule-cisshgo-integration/docs/User%20Guide.md)** in that same skill folder.

For a **compact list of scenario directories** and copy-paste commands, see **[`extensions/molecule/README.md`](README.md)** under this repo’s collection layout.

## How to run

From `extensions/`:

```bash
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH to build from source

molecule test -s <scenario_name>
```

Run cisshgo scenarios **one after another** so each `destroy` releases ports. Default base port is **`CISSHGO_PORT=10000`**.

## Do not edit integration tests or plugins for Molecule

If a transcript or converge assertion does not match module behavior, change **only** files under `extensions/molecule/<scenario>/`, not `tests/` or `plugins/`.
