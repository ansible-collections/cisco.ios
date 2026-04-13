# User guide: **cisco-ios-molecule-cisshgo-integration**

This document is the **human-facing** guide to **what the skill is**, **how its pieces work together**, and **how they connect** to Molecule, cisshgo, and the `cisco.ios` collection. Operational commands (env vars, `molecule test`, capture) come **after** that mental model.

**Canonical workflow for authors/agents** (preflight, emit order, iteration until green): **[../SKILL.md](../SKILL.md)**. Long references: **[Molecule + Cisshgo.md](Molecule%20+%20Cisshgo.md)**, **[Cisshgo scenario.md](Cisshgo%20scenario.md)**.

---

## 1. How everything fits together

You (or CI) drive **Molecule**. Molecule drives **cisshgo** over SSH. **cisshgo** pretends to be IOS using **fixtures**. **`cisco.ios` resource modules** run unchanged—the same code paths as on real hardware—so tests prove the module + Ansible behaviour against **known** CLI transcripts.

```text
┌─────────────────────────────────────────────────────────────────┐
│  You (or CI)                                                     │
│    molecule test  OR  helpers/run_scenario.sh                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Molecule (extensions/molecule/<scenario>/)                      │
│    create.yml   → starts cisshgo, waits on ports                 │
│    converge.yml → Ansible talks to localhost:ports as "IOS"      │
│    verify.yml   → scans .cisshgo.log for Unknown command         │
│    destroy.yml  → stops cisshgo, frees ports                     │
└────────────────────────────┬────────────────────────────────────┘
                             │  SSH (network_cli)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  cisshgo (local process)                                         │
│    Reads transcript_map.yaml + cisshgo_inventory.yaml          │
│    Platform listener  → static answers (show version, etc.)      │
│    Scenario listeners → ordered command → transcript steps       │
└────────────────────────────┬────────────────────────────────────┘
                             │  returns canned CLI / show text
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  cisco.ios resource modules (unchanged in this workflow)         │
│    Same code path as real hardware; asserts use integration vars │
└─────────────────────────────────────────────────────────────────┘
```

**Takeaway:** the skill does **not** replace the collection’s Python. It supplies **transcripts + ordering** so Molecule can run **offline** with predictable I/O.

---

## 2. How skill components work with each other

Everything for this workflow lives under **`.cursor/skills/cisco-ios-molecule-cisshgo-integration/`** (or your copy of that tree). The **collection** adds scenarios under **`ansible_collections/cisco/ios/extensions/molecule/`**.

| Piece | Role | Works with |
|-------|------|------------|
| **[SKILL.md](../SKILL.md)** | Single source of truth: when to use the skill, **mandatory pre-flight**, capture vs reuse, scaffold steps, emit-order rules, **completion = `molecule test` exit 0**, what not to edit. | You read it first; agents follow it literally. |
| **This User Guide** | Big picture + diagram + how to prompt an agent + copy-paste shell examples. | Points to SKILL + long docs. |
| **[Molecule + Cisshgo.md](Molecule%20+%20Cisshgo.md)** | Molecule layout, **`CISSHGO_BIN_PATH`**, ports, `create`/`converge` patterns, env vars. | Molecule + cisshgo operators. |
| **[Cisshgo scenario.md](Cisshgo%20scenario.md)** | Platform vs **scenario** listeners, **per-session sequence pointer**, interactive SSH vs exec. | Anyone authoring **`transcript_map.yaml`**. |
| **[Molecule Cisshgo multi-module.md](Molecule%20Cisshgo%20multi-module.md)** | Multiple listeners, ports, pointers to collection README. | Multi-scenario layouts. |
| **[../helpers/](../helpers/)** | **`capture_cml.yml`** — lab Ansible → captured CLI/show; **`validate_transcript_map.py`** — sanity-check fixtures; **`run_scenario.sh`** — destroy + env + `molecule test`. | Lab capture and local test runs. |
| **`.cursor/rules/cisshgo-molecule-preflight.mdc`** | When editing **`extensions/molecule/cisshgo_*`**, Cursor reminds you to read bundled docs + capture policy. | Editor guardrail. |
| **`extensions/molecule/cisshgo_ios_*`** (in repo) | **`molecule.yml`**, **`create.yml`** / **`destroy.yml`** / **`converge.yml`** / **`verify.yml`**, **`inventory/hosts.yml`**, **`cisshgo_fixtures/`** (`transcript_map.yaml`, **`transcripts/**`**, **`cisshgo_inventory.yaml`**). | Loaded by Molecule; cisshgo reads the fixture dir you pass at startup. |

**Data contract:** **`cisshgo_inventory.yaml`** maps each Molecule host group to a **port** and either **platform** (static `command_transcripts`) or **scenario** (ordered **`sequence`**). **`transcript_map.yaml`** must list **every** command Ansible sends on that port **in order** for that scenario—including extra **`show`** calls (e.g. `get_device_info` → extra `show vlan`, or ResourceModule **`result`** refetch). Wrong order → **`% Invalid input`** or **`Unknown command`** in **`.cisshgo.log`**.

---

## 3. Data flow for one stateful play

1. Ansible opens SSH to a **scenario** port on **localhost**.
2. Module sends **`show …`** → cisshgo returns the matching **sequence** step (or a **platform** default transcript).
3. Module sends **`configure terminal`**, config lines, **`end`** → cisshgo advances **one sequence step per matching command** (often empty `+` replies).
4. Module sends **`show …`** again → **after** transcripts (sometimes **many** getter rounds: preview, check_mode, apply, idempotent—each **new TCP session** resets the scenario pointer to step 0).
5. Mismatch → **`% Invalid input`** / **`Unknown command`**; use **`.cisshgo.log`** and SKILL troubleshooting.

---

## 4. Two ways to use this skill

| Mode | What you do | Inventory? |
|------|-------------|--------------|
| **Run tests** | `cd` to **`ios/extensions`**, set **`CISSHGO_BIN_PATH`** + **`ANSIBLE_COLLECTIONS_PATH`**, **`molecule test -s cisshgo_ios_…`**. | **No.** Molecule uses generated localhost + ports. |
| **Author fixtures** | Run **`helpers/capture_cml.yml`** against CML/lab, then edit **`transcript_map.yaml`** + **`transcripts/**`**; follow SKILL. | **Yes.** **`-i /path/to/inventory.ini`** for real **`network_cli`** targets. |

Running tests does **not** use your lab inventory. Capturing emit order and literal **`show`** output **does**.

---

## 5. Example prompt for an AI agent (Cursor, Codex, etc.)

Give the agent **paths + binary + task + rules** so it can execute **SKILL.md** without inventing locations.

### Checklist

| Include | Why |
|---------|-----|
| **Skill** | “Follow **`.cursor/skills/cisco-ios-molecule-cisshgo-integration/SKILL.md`**” (or enable the skill in the product). |
| **Task** | One line, e.g. scaffold **`cisshgo_ios_foo`**, fix **`cisshgo_ios_acls`**, or align transcripts to CML. |
| **Paths** | Collection root, **`.../ios/extensions`** for Molecule, **`helpers/`** absolute path. |
| **CISSHGO_BIN_PATH** | Documented in **Molecule + Cisshgo.md** § 2.2 — paste the real path. |
| **Lab** | Only if capturing: **`-i …/inventory.ini`**, **`module_name`**, optional **`states`**. |
| **Constraints** | Edits only **`extensions/molecule/`** (+ skill **helpers/docs**); **never** **`plugins/`** or **`tests/integration/`**; **`molecule test -s <scenario>`** must exit **0**. |

### Copy-paste template

```text
Use the cisco-ios-molecule-cisshgo-integration skill and follow SKILL.md end-to-end (including MANDATORY pre-flight).

Task: [e.g. Add a green Molecule cisshgo scenario for ios_<module> matching integration vars/main.yaml.]

Paths:
- Collection root: /ABSOLUTE/path/to/ansible_collections/cisco/ios
- Run molecule from: /ABSOLUTE/path/to/ansible_collections/cisco/ios/extensions
- Skill helpers: /ABSOLUTE/path/to/.cursor/skills/cisco-ios-molecule-cisshgo-integration/helpers

Environment (every shell that runs molecule):
- export CISSHGO_BIN_PATH="/ABSOLUTE/path/to/cisshgo/cisshgo"
- cd /ABSOLUTE/path/to/ansible_collections/cisco/ios/extensions
- export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"

Lab (only if capturing for fixtures):
- ansible-playbook .../helpers/capture_cml.yml -i /ABSOLUTE/path/to/inventory.ini -e module_name=ios_<module> -e "states=gathered,merged,deleted" -e capture_dir=captured -vvvv

Rules:
- Do not edit plugins/ or tests/integration/.
- Iterate until: molecule test -s cisshgo_ios_<module> exits 0 (create, converge, verify, destroy).
- After fixture edits: molecule destroy -s cisshgo_ios_<module> then molecule test again if stale.
```

Replace **`ABSOLUTE`**, **`ios_<module>`**, **`cisshgo_ios_<module>`**, and the **Task** line.

---

## 6. What you need installed

| Requirement | Notes |
|-------------|--------|
| **cisshgo** | Pre-built binary or `go build` — path pattern in **Molecule + Cisshgo.md** § 2.2. |
| **Ansible + Molecule** | Versions your team uses for this collection. |
| **Collection checkout** | Full **`ansible_collections/cisco/ios`** tree so **`ANSIBLE_COLLECTIONS_PATH`** can include the parent of **`ansible_collections`**. |

---

## 7. Environment variables (for `molecule test`)

| Variable | Required? | Purpose |
|----------|-----------|---------|
| **CISSHGO_BIN_PATH** | Yes (typical) | Absolute path to the **cisshgo** executable. |
| **CISSHGO_REPO_PATH** | Alternative | Build cisshgo from source instead of a binary. |
| **ANSIBLE_COLLECTIONS_PATH** | Yes | Directory that **contains** **`ansible_collections`**. |
| **CISSHGO_PORT** | Optional | Default **10000**; change only with matching scenario ports (see long doc). |
| **PYTHONHASHSEED** | Optional | **`0`** for stable dict order; **`run_scenario.sh`** sets it. |

**`molecule test`** does not use **`ansible_host`** from a lab inventory—only **localhost** + scenario ports.

---

## 8. Where to run Molecule

```bash
cd /path/to/ansible_collections/cisco/ios/extensions
```

All examples below assume this directory.

---

## 9. Example: **`cisshgo_ios_interfaces`**

### Manual

```bash
cd ansible_collections/cisco/ios/extensions

export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH="/path/to/cisshgo/cisshgo"

molecule test -s cisshgo_ios_interfaces
```

### Helper script

```bash
cd ansible_collections/cisco/ios/extensions
export CISSHGO_BIN_PATH="/path/to/cisshgo/cisshgo"
bash /path/to/cisco-ios-molecule-cisshgo-integration/helpers/run_scenario.sh cisshgo_ios_interfaces
```

From **`extensions/`** inside this repo, helpers are often: **`../../../.cursor/skills/cisco-ios-molecule-cisshgo-integration/helpers/run_scenario.sh`**.

After editing **`transcript_map.yaml`** or transcripts, run **`molecule destroy -s cisshgo_ios_interfaces`** (or use **`run_scenario.sh`**) before the next full test so cisshgo reloads fixtures.

### Other scenarios

Names are **`cisshgo_ios_<module>`** (underscores). Index: **`ansible_collections/cisco/ios/extensions/molecule/README.md`**.

```bash
molecule test -s cisshgo_ios_<module_name>
molecule test --all
```

---

## 10. Lab inventory (capture only)

For **`helpers/capture_cml.yml`** — not for **`molecule test`**.

```bash
cd ansible_collections/cisco/ios/extensions/molecule

ansible-playbook /path/to/cisco-ios-molecule-cisshgo-integration/helpers/capture_cml.yml \
  -i /path/to/inventory.ini \
  -e module_name=ios_interfaces \
  -e "states=gathered,merged,replaced,overridden,deleted" \
  -e capture_dir=captured \
  -vvvv 2>&1 | tee captured/ios_interfaces/run.log
```

**`-i`** — lab inventory (e.g. group **`ios`**, **`ansible_network_os`**, credentials, port). **`module_name`** — integration target, e.g. **`ios_interfaces`**.

---

## 11. If something fails

| Symptom | What to check |
|---------|----------------|
| Missing **CISSHGO_BIN_PATH** / **CISSHGO_REPO_PATH** | §7. |
| **`% Invalid input`** / desync | **`.cisshgo.log`** vs **`transcript_map.yaml`** sequence; SKILL + **Cisshgo scenario.md**. |
| Stale after edits | **`molecule destroy -s <scenario>`** then **`molecule test`**. |
| Port in use | **`molecule destroy`**; optional **CISSHGO_PORT** (advanced). |

---

## 12. Paths in the collection repo

| What | Where |
|------|--------|
| Scenario dirs | `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_*/` |
| Scenario index | `ansible_collections/cisco/ios/extensions/molecule/README.md` |
| Author workflow | **[../SKILL.md](../SKILL.md)** |
| Helpers | **[../helpers/](../helpers/)** |
