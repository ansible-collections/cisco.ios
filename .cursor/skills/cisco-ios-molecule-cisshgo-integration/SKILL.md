---
name: cisco-ios-molecule-cisshgo-integration
description: >-
  Scaffold or debug cisco.ios Molecule scenarios using cisshgo (transcript_map,
  cisshgo_inventory, converge plays, verify). Activate when adding cisshgo_* scenarios,
  fixing Unknown command / % Invalid input in .cisshgo.log, aligning emit order with
  CML or -vvv, or capturing show output for fixtures. Ground transcripts in lab Ansible
  first; run molecule test to exit 0 before declaring done. Never edit collection
  plugins/ or tests/integration — only extensions/molecule, helpers/, and docs/ here.
compatibility:
  - Cursor
metadata:
  tags:
    - ansible
    - cisco-ios
    - molecule
    - cisshgo
    - network_cli
---

# cisco.ios Molecule + cisshgo integration

## When to use this skill

- Adding or extending **`cisshgo_*`** scenarios under `ansible_collections/cisco/ios/extensions/molecule/`.
- Debugging **cisshgo** desyncs: **`Unknown command`**, **`% Invalid input`**, wrong **`show`** bodies, or assertion mismatches on **`before`/`after`/`gathered`**.
- Capturing **CLI emit order** and **literal device output** from **CML (or any `network_cli` lab)** for transcripts.

**Acceptance gate:** a full green **`molecule test -s <scenario>`** (create, converge, verify, destroy). **Authoring** fixtures should be anchored in **lab Ansible + `-vvv`/`-vvvv`** whenever possible.

## MANDATORY pre-flight (do not skip)

Complete **every** item below before creating or editing **any** scenario file. These are hard prerequisites enforced by the Cursor rule at **`.cursor/rules/cisshgo-molecule-preflight.mdc`**. Skipping any item is a defect.

### Pre-flight 1 — Read bundled docs for operational details

**`Read`** the file **`docs/Molecule + Cisshgo.md`** (co-located next to this SKILL.md). Extract and use:

- **`CISSHGO_BIN_PATH`** from **section 2.2** — the exact filesystem path to the pre-built cisshgo binary. Use this value for all `molecule test` runs. **Do NOT search the filesystem** for the binary; the path is documented.
- **`CISSHGO_PORT`** from **section 2.2** — the default starting port.

Also read **`docs/Cisshgo scenario.md`** if this is your first time working with platform vs scenario fixture structure.

### Pre-flight 2 — CML capture or verified artifacts

Before authoring **`transcript_map.yaml`** or **any** transcript **`.txt`** file, you **MUST** do one of:

**(a)** Run **`helpers/capture_cml.yml`** against a real CML / IOS-XE lab node (see **Step 1** in the workflow below) to produce fresh artifacts under **`captured/<module>/`**.

**(b)** Verify that **`captured/<module>/`** artifacts **already exist** for the target module, **confirm with the user** that they are current, and **explicitly state** in your response that you are reusing pre-existing captures.

If CML is unavailable **and** no captured artifacts exist: **STOP** and tell the user. Do **not** invent transcript content from module source or `vars/main.yaml` alone without the user explicitly acknowledging the risk.

---

## Bundled reference docs (verbatim copies)

Long-form material lives in **`docs/`** next to this file so you can **`Read`** it on demand (progressive disclosure). These files are **full copies** of the repo’s `docs/` sources at the time they were added to the skill bundle:

| Doc | Role |
|-----|------|
| [docs/User Guide.md](docs/User%20Guide.md) | **Start here for humans:** architecture diagram, how skill pieces connect to Molecule/cisshgo/collection, data flow, agent prompt template, then env vars and `molecule test` examples. |
| [docs/Molecule Cisshgo multi-module.md](docs/Molecule%20Cisshgo%20multi-module.md) | Multiple scenarios, ports, how to run, pointers to collection README. |
| [docs/Molecule + Cisshgo.md](docs/Molecule%20+%20Cisshgo.md) | Full POC: Molecule layout, `create`/`converge`/`verify`/`destroy`, env vars, file examples. |
| [docs/Cisshgo scenario.md](docs/Cisshgo%20scenario.md) | Full cisshgo guide: platform vs scenario, sequence pointer, inventory, interactive mode. |

**Helpers** (capture playbook, validator, Molecule wrapper): **`helpers/`**.

Collection index (stays in-repo): [extensions/molecule/README.md](../../../ansible_collections/cisco/ios/extensions/molecule/README.md).

## Do not edit the collection or integration tests

**Never modify** upstream `cisco.ios` sources to make Molecule pass, including:

- `ansible_collections/cisco/ios/plugins/` (modules, module_utils, cliconf, etc.)
- `ansible_collections/cisco/ios/tests/` (`tests/integration/`, `tests/unit/`, or any test target under the collection)

**Structured expectations** (what `before` / `after` / `gathered` should contain) come from **`tests/integration/targets/<module>/vars/main.yaml`** and the integration playbooks. **CLI emit order, exact command strings, and literal `show` output** must match what Ansible actually does on a device; integration **`commands`** lists are often **order-insensitive** and sometimes **do not match** multiset emit order or delta commands the module produces.

### Source-of-truth hierarchy (use in this order)

1. **Lab Ansible on CML (or equivalent `network_cli` lab)** -- Run the same tasks the integration target runs (or the Molecule `converge` tasks) against a real IOS/XE node in CML. Capture **literal `show` output** for platform transcripts and **`-vvv` / `-vvvv` task output** for the exact configuration command sequence and order. This is the **primary** ground truth for `transcript_map.yaml` sequences and `*.txt` bodies. If you skip this and guess from YAML key order or vars `commands` alone, cisshgo will **`% Invalid input`** or desync.
2. **Module source** (`plugins/module_utils/network/ios/config/<module>/<module>.py`: `self.parsers`, `_compare()`, `compare_list()`, etc.) when the lab is unavailable or to explain a specific ordering rule.
3. **Integration vars** for dict shape and symmetric-difference targets on **`before` / `after` / `gathered`** -- not for assuming **CLI line order** inside a stanza or **transcript_map step order**.

If a transcript, scenario map, or converge assertion does not match the lab + vars + module behavior, **change only our side**:

- `ansible_collections/cisco/ios/extensions/molecule/<scenario>/` (playbooks, `cisshgo_fixtures/`, inventory, Molecule-only `vars/*.yml` when asserts need stable expected data without touching integration)
- Project docs under `docs/` and this skill

**Do not** edit integration `vars/main.yaml`, tests, or collection code to make Molecule pass.

## Completion rule (non-negotiable): iterate until `molecule test` is green

**Stopping early is a failure mode.** Do not end the task, hand off a summary, or mark work complete until **`molecule test -s <scenario_name>` exits 0** from the correct directory, including **create**, **converge**, **verify**, and **destroy**. If the last command you ran was editing files but not Molecule, you are not done.

After every meaningful change to **`transcript_map.yaml`**, scenario **`*.txt`**, **`molecule.yml`**, or inventory, run a full test (or at minimum **`molecule converge`** then **`molecule verify`** in the same session policy your workflow allows). On failure: read **`.cisshgo.log`**, fix fixtures or asserts, **`molecule destroy -s <scenario>`** when ports or cisshgo state are stale (see **Reloading cisshgo after fixture edits**), and **repeat** until green.

```bash
cd ansible_collections/cisco/ios/extensions
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH
molecule test -s <scenario_name>
```

Forbidden shortcuts: declaring success from "should work" reasoning, only running linters, only reading files without executing Molecule, or stopping after a single failed run without another full **`molecule test`** proving green.

## Recommended workflow for a new module scenario

> **BLOCKED by pre-flight.** You must have completed **both** items in **MANDATORY pre-flight** above (read docs for `CISSHGO_BIN_PATH`, and CML capture or verified artifacts) before entering this workflow. If you have not, go back now.

### Step 1 — Capture on CML (or verify existing captures)

This step satisfies **Pre-flight 2**. If you already verified existing `captured/<module>/` artifacts during pre-flight, reference that verification here and proceed to Step 2. Otherwise, run the **CML capture playbook** against a real IOS/XE lab node to produce ground-truth artifacts:

```bash
SKILL_HELPERS=".cursor/skills/cisco-ios-molecule-cisshgo-integration/helpers"

cd ansible_collections/cisco/ios/extensions/molecule
ansible-playbook "$SKILL_HELPERS/capture_cml.yml" \
  -i /path/to/inventory.ini \
  -e module_name=ios_l3_interfaces \
  -e "states=gathered,merged,replaced,overridden,deleted" \
  -e capture_dir=captured \
  -vvvv 2>&1 | tee captured/ios_l3_interfaces/run.log
```

All helper tools live alongside this skill at **`helpers/`** (relative to this SKILL.md):

- `helpers/capture_cml.yml` — CML capture playbook
- `helpers/validate_transcript_map.py` — transcript pre-validation
- `helpers/run_scenario.sh` — Molecule wrapper

This produces per-state `before.txt`, `after.txt`, `commands_ordered.txt`, and `result.yml` under `captured/<module>/`. The **`-vvvv` console log** (`run.log`) is the primary source for transcript_map command ordering.

If CML is unavailable, state explicitly that you are deriving order from module source only (see **Determining emit order from module source**) and expect more iteration.

### Step 2 — Scaffold scenario directory

Copy the **gold template** (`cisshgo_ios_interfaces/`) and rename. Adjust `molecule.yml`, `inventory/hosts.yml`, `create.yml`, `destroy.yml`, `cisshgo_inventory.yaml` per the **Artifact checklist**. Set **`PYTHONHASHSEED: "0"`** in `molecule.yml` if merged adds multiple new interfaces.

### Step 3 — Author transcript_map + transcript files from captured artifacts

- Copy `before.txt` / `after.txt` from `captured/` into `cisshgo_fixtures/transcripts/scenarios/`.
- Build `transcript_map.yaml` **`sequence`** entries by reading `commands_ordered.txt` and the **`-vvvv`** log. Prefer the log for exact order; `commands_ordered.txt` is a cross-reference.
- Build platform `command_transcripts` from the `gathered/show_section.txt` capture and `show_version.txt` from the device.

### Step 4 — Pre-validate

```bash
python "$SKILL_HELPERS/validate_transcript_map.py" \
  cisshgo_<module>/cisshgo_fixtures/ \
  --module <module_short_name>
```

Fix any **ERRORS** (missing files, inventory mismatches). Review **WARNINGS** (parser-order) — most are legitimate runtime reorder; investigate any you do not recognize.

### Step 5 — Run with the wrapper

```bash
cd ansible_collections/cisco/ios/extensions
bash "$SKILL_HELPERS/run_scenario.sh" cisshgo_<module>
```

The wrapper handles `molecule destroy` first, sets `PYTHONHASHSEED`, checks env, and tails `.cisshgo.log` on failure. Run from the **`extensions/`** directory (or set `EXTENSIONS_DIR`).

### Step 6 — Iterate until green

See **Iteration playbook** below. Fix, destroy, re-run. Do not stop until **exit 0**.

### Step 7 — Mark complete

Only after a green `molecule test` in this session. See **Definition of done**.

## Where to document (do not duplicate `MULTI_MODULE_CISSHGO.md`)

- **This skill (`SKILL.md`)** is the **canonical** place for workflow, port math, emit-order rules, RTT sequencing, gathered transcript rules, and the iteration loop above.
- **`extensions/molecule/README.md`** may keep a **short** scenario index and copy-paste env vars.
- **`extensions/molecule/MULTI_MODULE_CISSHGO.md`**: keep as a **stub** that points here; **avoid** maintaining long scenario matrices or duplicating skill content there (reduces drift).

## State classification (resource-module states vs cisshgo)

Use this table when deciding **listeners**, **scenario rows**, and **transcript files**. Replace "interface" with the section command your module uses (often `show running-config | section ^interface`).

| State | Scenario listener? | before/after transcript files? | Initial "device" state in first `show ... \| section` |
|-------|--------------------|--------------------------------|------------------------------------------------------|
| **gathered** | No -- platform only | No -- platform `command_transcripts` entry for the section command | **Populated** -- match `gathered['config']` in vars (integration often uses `_populate_config.yaml` on real hardware; cisshgo encodes that in the platform section transcript). |
| **merged** | Yes | Yes -- `before.txt` / `after.txt` for first apply | **Clean** -- `merged.before` in vars (often bare `interface` stanzas). |
| **merged_again** | Same listener as **merged** | Yes -- extend sequence with extra `configure`/`end` block and **`after_again.txt`** for `merged_again.after` | Logical state after first merge (`merged.after`). |
| **replaced** | Yes | Yes | **Populated** -- `replaced.before` (same baseline integration builds with `_populate_config.yaml`). |
| **overridden** | Yes | Yes | **Populated** -- `overridden.before` (same pattern). |
| **deleted** | Yes | Yes | **Populated** -- `deleted.before`. |
| **parsed** | No scenario pointer | No -- offline | N/A -- `running_config:` from `tests/integration/targets/<module>/tests/cli/_parsed.cfg` (or sibling). |
| **rendered** | No scenario pointer | No -- offline | N/A -- module renders from inline `config:` only. |
| **rtt** | Yes (multi-phase) | Yes -- multiple shows and configure blocks | **Advanced** -- merge then ios_facts then override then revert; skip in first pass unless requested. |

**Key insight:** **replaced**, **overridden**, and **deleted** integration tests start from a **populated** layer-2 config. On hardware that is `_populate_config.yaml` + `cli_config`. In cisshgo, the scenario's first **`show running-config | section ...`** transcript (`before.txt`) must already reflect that populated config (equivalent to **`<state>.before`** structured dict rendered as IOS).

## Port count formula

```
cisshgo_port_count = 1 + <number of scenario rows in cisshgo_inventory.yaml>
```

Typically **1** platform row (`platform: ios`, `count: 1`) plus **one scenario row per stateful state** that needs its own SSH listener (merged, replaced, overridden, deleted each get a row if they each use a dedicated scenario name).

**Example:** gathered + merged (+ merged_again in same play) + replaced + overridden + deleted + parsed + rendered = **5** listeners = `cisshgo_port_count: 5` (platform + 4 scenarios). **`create.yml`**, **`destroy.yml`**, and **`inventory/hosts.yml`** must all use the same count and sequential ports from `CISSHGO_PORT` (default **10000**).

## ansible_net_version and `show version`

Integration tests under `tests/integration/targets/<module>/tests/cli/*.yaml` often wrap device traffic in `when: ansible_net_version == "15.6(2)T"`. **Molecule `converge.yml` playbooks usually omit those guards** so cisshgo runs unconditionally.

If a converge play uses **`cisco.ios.ios_facts`** or asserts on **`ansible_net_version`**, the platform transcript for **`show version`** must contain a string facts can parse consistently with those tests. When in doubt, align `show_version.txt` with what the integration lab image reports.

## Before / after transcript bodies from `vars/main.yaml`

Turn structured **`<state>.before`** / **`<state>.after`** / **`gathered.config`** into IOS **`show running-config | section ...`** style text:

1. Each list element is one interface: emit `interface <name>` then child lines, then `!` before the next interface.
2. **Name only** -- dict is `{name: GigabitEthernetX}` only = stanza is `interface ...` then `!` (no L2 lines).
3. **Reverse-map keys to CLI** (examples): `access.vlan` = ` switchport access vlan <n>`; `voice.vlan` = ` switchport voice vlan <n>`; `mode: trunk` with `trunk.*` = ` switchport trunk encapsulation dot1q|isl`, ` switchport trunk native vlan`, ` switchport trunk allowed vlan ...`, ` switchport trunk pruning vlan ...`, ` switchport mode trunk`; `private_vlan` host association = ` switchport private-vlan association host ...`. Match spelling from integration **`_populate_config.yaml`** / **`_parsed.cfg`** where possible.
4. **Order of lines inside a stanza** must match **real IOS** `show running-config` output, **not** the key order inside the YAML dict. Confirm with a device capture or **`tests/cli/_populate_config.yaml`** / **`-vvv`**.
5. **Gathered platform file** -- include **only** interfaces that appear in **`gathered['config']`**; extra stanzas become extra parsed interfaces and break `symmetric_difference` asserts.

**`ios_l3_interfaces` gathered:** `Facts` + `validate_config` normalize **IPv6** child order and **address case** (e.g. `2001:DB8:...`). A common cisshgo failure is **`ipv6 address autoconfig` before the static `ipv6 address 2001:DB8:...` line** in the show transcript while **`gathered['config']`** lists the static address **first**—swap line order and use **`2001:DB8`** so `result.gathered | symmetric_difference(gathered['config'])` is empty.

**Concrete example (`ios_l2_interfaces` / `replaced.before`):**

Vars list: `GigabitEthernet0/0` (name only), `GigabitEthernet2` (`access.vlan: 10`), `GigabitEthernet3` (`mode: trunk` + trunk fields as in vars).

```text
interface GigabitEthernet0/0
!
interface GigabitEthernet2
 switchport access vlan 10
!
interface GigabitEthernet3
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 10
 switchport trunk allowed vlan 10-20,40
 switchport trunk pruning vlan 10,20
 switchport mode trunk
!
```

## Cisshgo scenario `sequence` template (stateful states)

Each **scenario** block in `transcript_map.yaml` is an ordered list. **Every** command the client sends while attached to that scenario's listener must appear **once**, in **emit order**, or cisshgo desyncs (`Unknown command`, **`% Invalid input`**).

### Generic pattern (one apply + idempotency)

For **merged**, **replaced**, **overridden**, **deleted** (single apply + idempotent rerun):

1. `show running-config | section ^interface` -> `scenarios/<name>/before.txt`
2. `configure terminal` -> empty transcript
3. Each configuration line the module sends (see **emit order** below) -> empty
4. `end` -> empty
5. `show running-config | section ^interface` -> `after.txt`
6. `show running-config | section ^interface` -> `after.txt` again (idempotent read; device unchanged)

### merged_again (same scenario listener as merged)

After step 6, append:

7. `show running-config | section ^interface` -> still **`merged.after`** body (`after.txt`) -- start of second module call ("before" for `merged_again` equals **`merged.after`**).
8. `configure terminal` -> empty
9. Lines from **`merged_again`** in **emit order** -> empty. **WARNING:** for vlan list commands, the module emits `switchport trunk ... vlan add <delta>` (NOT the full vlan list from vars `commands`). See **VLAN list commands** section.
10. `end` -> empty
11. `show ...` -> **`after_again.txt`** matching **`merged_again.after`** (see **After transcript files must match vars exactly**)
12. `show ...` -> **`after_again.txt`** (idempotent)

### Emit order vs vars `commands`

Converge often asserts `vars['<state>']['commands'] | symmetric_difference(result['commands'])` -- that is **order-insensitive**. **`transcript_map.yaml` `sequence` is order-sensitive.** Do **not** assume vars list order equals device emit order.

**Canonical emit order (pick whichever is available):**

1. **`state: rendered`** with the **same `config:`** as the Molecule task (for greenfield commands). Ignores `have`; good for tuning **merged**-style sequences.
2. **`-vvv` / `-vvvv`** on a **CML / lab** run where **`have`** matches your **`before.txt`** -- required when commands depend on existing config (**replaced**, **overridden**, **deleted**).
3. **Read `self.parsers` from the module source** -- always available when no lab is reachable; second choice after captured **`-vvv`**. See **Determining emit order from module source** below.

**NEVER use vars `commands` order directly for the transcript_map sequence.** It is an unordered set for assertion purposes. The real order comes from `self.parsers` + `compare_list()` in the module's config class.

### Determining emit order from module source (no lab required)

When no lab or `-vvv` output is available, the **module source code** is the definitive reference. Every `cisco.ios` resource module has a config class at:

```
plugins/module_utils/network/ios/config/<module>/<module>.py
```

**Procedure:**

1. **Open the config class** and find `self.parsers = [...]` in `__init__`. This list defines the order `ResourceModule.compare()` walks the templates. Each entry maps to a `setval` / `remval` template in `rm_templates/<module>.py`.

2. **Note the `_compare()` method** -- it may reorder parsers for certain states. Look for `reverse_order` logic.

3. **Note `compare_list()`** -- list-type attributes (e.g. `allowed_vlans`, `pruning_vlans`) are handled **after** `compare()` and appended to the end of the command list.

4. The module inserts **`interface <name>`** at the beginning of each interface's command block (line `self.commands.insert(begin, ...)`).

**Example: `ios_l2_interfaces`** (from `config/l2_interfaces/l2_interfaces.py`):

`self.parsers` order (relevant entries only):

```
access.vlan -> access.vlan_name -> voice.vlan -> voice.vlan_tag ->
voice.vlan_name -> trunk.encapsulation -> MODE -> trunk.native_vlan ->
private_vlan -> ...
```

Then `compare_list()` appends: **allowed_vlans** then **pruning_vlans** (see **VLAN list commands** below for critical `add`/`remove` details).

So for a **merged** trunk interface (GE3) from a **clean** device (no existing vlans), the emit order is:

```
interface GigabitEthernet3
switchport trunk encapsulation dot1q   <- trunk.encapsulation (parser index 6)
switchport mode trunk                  <- mode (parser index 7)
switchport trunk native vlan 20        <- trunk.native_vlan (parser index 8)
switchport trunk allowed vlan 15-20,40 <- compare_list: allowed_vlans (no "add" -- have is empty)
switchport trunk pruning vlan 10,20    <- compare_list: pruning_vlans (no "add" -- have is empty)
```

**`reverse_order` for replaced / overridden / deleted:**

`_compare()` sets `reverse_order = True` when:
- State is **deleted** or **purged** (always), OR
- State is **replaced** or **overridden** AND `have_mode == "trunk"` AND (`want_mode != "trunk"` OR `have_trunk_encap != want_trunk_encap`)

When `reverse_order` is true, `trunk.encapsulation` moves to **after** `mode` in the effective parser list. So the module emits removal of `mode` **before** touching `trunk.encapsulation`.

For **replaced** GE3 (have is trunk + dot1q, want drops mode but keeps dot1q encap):

```
interface GigabitEthernet3
no switchport mode                            <- compare: mode (now before encap)
switchport trunk native vlan 20               <- compare: trunk.native_vlan
no switchport trunk allowed vlan              <- compare_list: allowed removal (want has none)
switchport trunk pruning vlan add 11-19,30    <- compare_list: pruning addition ("add" -- have has vlans!)
```

For **overridden** GE3 (have is trunk + dot1q, want changes encap to isl + different vlans):

```
interface GigabitEthernet3
no switchport mode                            <- compare: mode
switchport trunk encapsulation isl            <- compare: trunk.encapsulation (changed)
switchport trunk native vlan 30               <- compare: trunk.native_vlan
switchport trunk allowed vlan remove 10-20    <- compare_list: allowed removal (partial -- 40 stays)
switchport trunk allowed vlan add 30-35       <- compare_list: allowed addition (new vlans only)
no switchport trunk pruning vlan              <- compare_list: pruning removal (want has none)
```

For **deleted** GE3 (have is trunk, want is empty):

```
interface GigabitEthernet3
no switchport mode                     <- mode (first due to reverse_order)
no switchport trunk encapsulation      <- trunk.encapsulation (moved after mode)
no switchport trunk native vlan        <- trunk.native_vlan
no switchport trunk allowed vlan       <- compare_list removal
no switchport trunk pruning vlan       <- compare_list removal
```

**For other modules:** follow the same procedure -- open `config/<module>/<module>.py`, read `self.parsers`, check `_compare()` for reorder logic, note any `compare_list()` or custom post-processing.

### VLAN list commands: `add`, `remove`, and full-replace (CRITICAL)

**This is the #1 source of cisshgo sequence desyncs for vlan-heavy modules.** The `compare_list()` method in `l2_interfaces.py` (and similar modules) does NOT simply emit `switchport trunk allowed vlan <full-list>`. It generates **delta** commands based on `have` vs `want`:

**The `generate_switchport_trunk(type, have_vlans, new_vlans_range)` function:**

- If `have_vlans` is **empty** (first merge on clean device): emits `switchport trunk <type> vlan <vlans>` (no prefix).
- If `have_vlans` is **non-empty** (device already has vlans): emits `switchport trunk <type> vlan add <new-vlans>` (only the delta).
- If there are multiple chunks (>220 chars), subsequent chunks always get `add`.

**The removal logic (for replaced/overridden, NOT merged):**

- If `want` has **no** vlans for this type and `have` does: `no switchport trunk <type> vlan` (full removal).
- If `want` has vlans but some in `have` should be removed: `switchport trunk <type> vlan remove <excess-vlans>` (partial removal).
- Then additions follow (with `add` prefix since have still has vlans).

**Concrete examples:**

| Scenario | have allowed | want allowed | Commands generated |
|----------|-------------|--------------|-------------------|
| First merge (clean) | `[]` | `[15-20,40]` | `switchport trunk allowed vlan 15-20,40` |
| merged_again (adding) | `[15-20,40]` | `[200]` (after dict_merge: `[15-20,40,200]`) | `switchport trunk allowed vlan add 200` |
| replaced (full removal) | `[10-20,40]` | `[]` | `no switchport trunk allowed vlan` |
| overridden (partial swap) | `[10-20,40]` | `[30-35,40]` | `switchport trunk allowed vlan remove 10-20` then `switchport trunk allowed vlan add 30-35` |

**NEVER assume the transcript_map command is `switchport trunk ... vlan <full-list>`.** Always derive the actual command from the module's `compare_list()` + `generate_switchport_trunk()` logic based on the specific `have` and `want` for that scenario.

### `dict_merge` for merged state combines lists (not replaces)

The `dict_merge` from `ansible.netcommon` used in `generate_commands()` for `state: merged` **combines** list values using `list(set(chain(base, other)))`. This means:

- `have.trunk.allowed_vlans = [15,16,...,20,40]` + `want.trunk.allowed_vlans = [200]` -> merged want = `[15,...,20,40,200]` (union, not replacement)
- `compare_list()` then computes `cmd_always = set(merged_want) - set(have)` = `{200}` (just the delta)
- Since `have` is non-empty, the module emits `switchport trunk allowed vlan add 200`

This is why `merged_again` commands look different from what you might expect from the vars `commands` list.

### `dict_merge` key order for **new** top-level interfaces (`merged`)

For **`state: merged`**, `ansible.netcommon.utils.dict_merge` merges structured `want` with `have`. Keys that exist only in `want` are appended using **`set(other.keys()).difference(base.keys())`**, so **iteration order is not YAML order** and can vary with **Python hash randomization** across processes. That changes the order of **`interface <name>`** blocks the module emits when several new interfaces appear in one task.

**Mitigation used in cisshgo scenarios:** set a fixed hash seed for the Ansible process so emit order matches a transcript captured once, e.g. in **`molecule.yml`** under **`provisioner.env`**:

```yaml
env:
  PYTHONHASHSEED: "0"
```

**Preferred:** capture **`-vvv`** from a real run (CML) with stable Python, then lock **`transcript_map.yaml`** sequence to that order. Do not assume alphabetical or YAML key order for new interfaces.

### Vars `commands` vs actual module `result['commands']` for vlan operations

The vars `commands` list is used with `symmetric_difference` (order-insensitive, set comparison). For vlan list operations, **vars `commands` may show the full vlan list** (e.g. `switchport trunk allowed vlan 200,15-20,40`) while the **module actually emits delta commands** (e.g. `switchport trunk allowed vlan add 200`).

**In converge.yml assertions:** For states where vlan list commands differ between vars and actual module output (typically `merged_again`, `replaced`, `overridden`), **do NOT use `symmetric_difference` on the commands list**. Instead, assert:

```yaml
- result['changed'] == true
- result['commands'] | length > 0
```

Or assert on specific known commands if needed. The `before`/`after` dict assertions (which compare parsed device state, not CLI commands) remain reliable and should still use `symmetric_difference`.

### When integration `commands` / `before` order does not match parsed facts

Integration **`vars/main.yaml`** may list **`commands`** or nested list order that does not match what **`ios_facts`** / the module returns (e.g. IPv6 **`no`** order, helper vs address order). **Do not change integration vars.** Add **Molecule-only** YAML under **`extensions/molecule/<scenario>/vars/`** (e.g. `replaced_commands_expected.yml`) and point **`vars_files`** + asserts in **`converge.yml`** at those files. Keep transcripts aligned with **module emit order** and **parsed** fixture shape.

### After transcript files must match vars `<state>.after` exactly

Each `after.txt` (and `after_again.txt`) is what the module reads as post-change device state. The module parses it into the `result['after']` dict, which is then compared with `vars['<state>']['after']` via `symmetric_difference`.

**Rules:**

1. **Every key present in vars `<state>.after` for an interface must have a corresponding CLI line in the transcript.** Missing lines = missing keys in parsed result = assertion failure.
2. **Every CLI line in the transcript creates a parsed key.** Extra lines create extra keys not in vars = assertion failure.
3. **If vars `<state>.after` does NOT include a key that was present in a previous state's `after` (e.g. `merged.after` has `voice.vlan: 40` for GE2 but `merged_again.after` does not), then the transcript must NOT include that CLI line** even if logically the device would still have it. Always match the transcript to what vars says, not to what you think the device state should be.
4. **Cross-check:** for each interface in `<state>.after`, reverse-map the dict keys to CLI lines (see **Before / after transcript bodies**) and verify every line is present, and no extra lines exist.

## Offline states (parsed / rendered)

- **No** dedicated scenario listener row is required for these; they do not walk a scenario `sequence`.
- Runs typically target the **platform** host group (same as **gathered**) so `ANSIBLE_COLLECTIONS_PATH` and SSH still resolve if the play uses `network_cli`.
- **parsed:** `running_config: "{{ lookup('file', '.../_parsed.cfg') }}"` -- use a path relative to the playbook or an absolute path under `tests/integration/targets/<module>/tests/cli/_parsed.cfg`.
- **rendered:** inline `config:` exactly as in `tests/cli/rendered.yaml` (or equivalent); assert `result.rendered` vs **`rendered.commands`** in vars.

## Compound state: rtt (round-trip)

**rtt** (`tests/cli/rtt.yaml` where present) chains **apply base -> `cisco.ios.ios_facts` with `gather_network_resources` -> drift (often `replaced` or partial `overridden`) -> revert with `state: overridden` and `config: "{{ ansible_facts['network_resources'][...] }}"`**.

### Listener and port count

Add **one** `scenario:` row (e.g. `ios-l3-interfaces-rtt`, `ios-interfaces-rtt`) and bump **`cisshgo_port_count`** by **1**. RTT is **not** offline: it walks the same `show running-config | section ^interface` (or resource-specific getter) **multiple times** per play—each phase must have the correct **`before` / `after` / `after_drift`** transcript body.

### Transcript sequence (order-critical)

1. **Base apply:** `show` (baseline) → `configure` → commands from **merged** (or RTT base merge) → `end` → `show` (post-base; used again as **`ios_facts`** input).
2. **`ios_facts`:** usually **one** extra `show` with the **same** body as post-base (unless legacy subsets pull more commands—then add platform entries for each).
3. **Drift:** `show` (still base if drift task gathers first—match actual Ansible order) → `configure` → drift commands → `end` → `show` (**after_drift**).
4. **Revert:** `show` (**after_drift**) → `configure` → revert commands → `end` → `show` (back to base / **after.txt**).

**Revert command list** is often in **`rtt['commands']`** in `vars/main.yaml` for modules that ship RTT in integration (e.g. `ios_l3_interfaces`). For modules without **`rtt`** in vars (e.g. `ios_interfaces`), put **expected revert CLI** only under **`extensions/molecule/<scenario>/`** (play `vars:` or a fixture YAML)—**do not** add keys to integration `vars/main.yaml`.

**When integration `rtt.commands` / drift vars do not match module emit** (common on **`ios_l2_interfaces`** when the module emits **`switchport trunk allowed vlan remove` / `add`** deltas but vars show a single **full** allowed-vlan line), keep **integration** vars untouched and define **`l2_rtt_drift_expected` / `l2_rtt_revert_expected`** (or equivalent) **only in Molecule** `converge.yml`, aligned with **`ResourceModule.generate_commands`** output (patched `gather_current` in Python or **`-vvv`** on a lab run).

### Deriving emit order without a lab

For RTT **configure** blocks, use the same approach as other states: **`ResourceModule.generate_commands`** with **`gather_current` patched** to return structured **`before` / `have`** lists parsed from your transcript **`show`** bodies (or hand-built dicts that match facts shape). That yields **exact** command order for **base**, **drift**, and **revert** without guessing from **`vars['commands']`** order.

## What to collect from the user before starting

1. **cisshgo binary** -- `CISSHGO_BIN_PATH`, or **`CISSHGO_REPO_PATH`** if building with `go build`.
2. **Target module** -- e.g. `ios_l2_interfaces`; which **states** to cover (see **State classification**).
3. **Listener count** -- compute **`cisshgo_port_count`** (see **Port count formula**); align **`cisshgo_inventory.yaml`**, **`inventory/hosts.yml`**, **`molecule.yml` `platforms`**, **`create.yml`**, **`destroy.yml`**.
4. **Base port** -- default `CISSHGO_PORT=10000`; override only if the port is busy.
5. **CML / lab inventory (for transcript authoring)** -- inventory and vault that reach a real IOS/XE node (Cisco Modeling Lab or equivalent); host/group for **`ansible_network_os: cisco.ios`**; image version if **`ansible_net_version`** guards matter. Repo example: [`inventory.ini`](../../../inventory.ini). **Plan to run Ansible there before locking cisshgo sequences** unless the task is explicitly source-only.
6. **Fixture layout** -- prefer **self-contained** `cisshgo_fixtures/` per scenario.

## Artifact checklist (first-time scaffold)

Use **[`extensions/molecule/cisshgo_ios_interfaces/`](../../../ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/)** as the **gold template** when filenames or structure are unclear.

| Order | Artifact | Purpose |
|-------|-----------|---------|
| 1 | **`molecule.yml`** | `scenario.name`, `test_sequence`, **`platforms:`** one entry per listener host group, `provisioner.inventory.links.hosts`, **`ANSIBLE_COLLECTIONS_PATH`**. For **`merged`** tasks that add multiple new interfaces, consider **`provisioner.env.PYTHONHASHSEED: "0"`** so **`dict_merge`** append order matches **`transcript_map.yaml`** (see **`dict_merge` key order**). |
| 2 | **`inventory/hosts.yml`** | Under `cisshgo_targets.children`, one group per play host type; **`ansible_port`** = `CISSHGO_PORT + offset`. Never put `network_cli` vars under `all.vars` (localhost plays). |
| 3 | **`create.yml`** / **`destroy.yml`** | **`cisshgo_port_count`** and **`wait_for`** / kill logic must match inventory listener count. Prefer a **numeric loop** for ports in destroy fallback (same count as create). |
| 4 | **`verify.yml`** | Scan `.cisshgo.log` for **Unknown command** (copy from gold). |
| 5 | **`cisshgo_fixtures/cisshgo_inventory.yaml`** | **`devices:`** list: first **`platform: ios`**, then one **`scenario: <kebab-name>`** row per stateful scenario name used in `transcript_map.yaml`. |
| 6 | **`cisshgo_fixtures/transcript_map.yaml`** | **`platforms.ios.command_transcripts`** -- all read-only commands Ansible may send (`show privilege`, `terminal length 0`, **`show version`**, **`show running-config`**, section command for gathered, `write memory`, etc.). **`scenarios.<name>.sequence`** -- stateful steps only (see **Cisshgo scenario sequence template**). **Use self.parsers order from the module source for command sequence -- see Determining emit order.** |
| 7 | **`cisshgo_fixtures/transcripts/**`** | Platform `*.txt` files + per-scenario **`scenarios/<name>/before.txt`**, **`after.txt`**, and **`after_again.txt`** if **merged_again** is included. |
| 8 | **`converge.yml`** | One play per **listener group** / concern: **gathered** (platform), each **stateful** group, **parsed** + **rendered** (platform group). **`vars_files:`** -> `tests/integration/targets/<module>/vars/main.yaml`. Mirror assertions from **`tests/cli/*.yaml`** (symmetric_difference / length / `changed`). |

### Helper tools (co-located at `helpers/` next to this SKILL.md)

All helpers live at **`.cursor/skills/cisco-ios-molecule-cisshgo-integration/helpers/`** — same directory as this skill.

| Tool | Purpose | When to use |
|------|---------|-------------|
| **`helpers/capture_cml.yml`** | Ansible playbook that runs each module state against a CML lab node with `-vvvv` and saves `before.txt`, `after.txt`, `commands_ordered.txt`, and full results per state. | **Before** authoring `transcript_map.yaml` — produces ground-truth artifacts. |
| **`helpers/validate_transcript_map.py`** | Python script that checks transcript file existence, inventory/map consistency, and parser-order heuristics. Auto-detects collection root from the fixtures path. | **After** writing or editing `transcript_map.yaml` — catches missing files and obvious ordering bugs before a Molecule run. |
| **`helpers/run_scenario.sh`** | Shell wrapper that verifies env, runs `molecule destroy` first (prevents stale cisshgo), sets `PYTHONHASHSEED=0`, and tails `.cisshgo.log` on failure. Auto-detects `extensions/` from cwd or `EXTENSIONS_DIR`. | **Every** Molecule run during development — replaces bare `molecule test`. |

## Aligning `gathered` transcripts with `tests/integration/.../vars/main.yaml`

Converge often asserts `gathered['config'] | symmetric_difference(result['gathered'])`. The **platform** transcript for the section command must parse to **exactly** that structure.

1. **Lab check on CML / hardware** -- `state: gathered` on **`network_cli`**; trim fixture to **vars** if asserts target vars.
2. **Validate with parsed** -- `state: parsed` + `lookup('file', '<section_transcript>')` on `network_cli`; compare to **`gathered['config']`**.
3. **No stray interfaces** -- empty `interface Foo` / `!` still yields `{name: Foo}`.
4. **No extra keys** -- lines create parser keys; remove lines not reflected in vars.

## Authoring transcripts: CML / lab Ansible first, then verbosity

**Do not invent** platform `show ...` bodies or scenario `sequence` steps from memory.

1. **Run Ansible against CML** (or your lab inventory that points at a real IOS/XE node): same resource module tasks, `have` equivalent to your **`before.txt`** where stateful. Use the repo or team **`inventory`** / group_vars the integration lab uses if available.
2. Capture **literal `show running-config | section ...`** (and any other reads the module issues) for platform **`command_transcripts`** bodies.
3. Capture **emit order** with **`-vvv` / `-vvvv`** on those tasks (or **`state: rendered`** when applicable, or module-source order as fallback). Save the log; transcribe commands **in order** into **`transcript_map.yaml`**.
4. **`check_mode: true`** can list commands in order, but advancing a cisshgo scenario pointer on the **same SSH session** as a subsequent normal run can desync fixtures; prefer fresh sessions / separate scenario design when mixing check and apply.
5. **Trim** transcripts to match integration **vars** for structured asserts; never edit **`tests/`** to weaken asserts.

**Spacing and spelling** (e.g. `GigabitEthernet2` vs `GigabitEthernet 0/2`) must match what Ansible sends -- verify from verbose logs.

If CML is not available, state explicitly that the sequence is **module-source-derived** or from a saved **`-vvv`** artifact, and still run **`molecule test`** until green.

## Ports and cleanup

- Default **shared** starting port **10000** across scenarios; run scenarios **sequentially** so `destroy` releases listeners.
- `destroy.yml` should kill the PID from `.cisshgo.pid`, **`wait_for`** each port in **`0 .. cisshgo_port_count - 1`**, optional **`lsof`** fallback over the **same** port range, and remove `.cisshgo.log`.

## Reloading cisshgo after fixture edits

The cisshgo process loads **`transcript_map.yaml`** at startup. If you edit the map or scenario **`*.txt`** but reuse a running server (e.g. skipped **`molecule create`** or stale process), you can see **wrong transcripts**, **`Unknown command`**, or **`% Invalid input`** against old content.

**After changing fixtures:** run **`molecule destroy -s <scenario>`** then **`molecule test ...`** (or **`molecule create`** + converge) so cisshgo restarts with the updated map. When debugging, treat "I fixed the YAML" without a fresh create/destroy cycle as suspect until **`molecule test`** proves otherwise.

## Lint, naming, and YAML hygiene (Molecule playbooks)

The collection uses **ansible-lint** with **`profile: production`** (see [`ansible_collections/cisco/ios/.ansible-lint`](../../../ansible_collections/cisco/ios/.ansible-lint)).

| Area | Rule | Practice |
|------|------|----------|
| **Play names** | `name[casing]` | Every `name:` **must start with an uppercase letter**. Write `"Ios_acls — state: merged"` not `"ios_acls — state: merged"`. This applies to both play-level and task-level names. |
| **Task names** | `name[casing]` | Same rule — capitalize the first word: `"Merge ACL configuration"`, `"Assert gathered matches …"`. |
| **Line length** | `yaml[line-length]` | Lines must be **≤ 160 characters**. For long Jinja2 assertions, use YAML folded/literal scalars (`>-` / `|`) or split into multiple `that:` entries. |
| **FQCN** | `fqcn` | Use `ansible.builtin.*`, `cisco.ios.*`, etc. — never short module names. |
| **YAML** | `yaml[*]` | Valid YAML; no tabs; consistent indentation (2 spaces). |

Run **`ansible-lint`** on the new scenario directory before finishing:

```bash
cd ansible_collections/cisco/ios/extensions
ansible-lint molecule/cisshgo_ios_<module>/converge.yml
```

If any `name[casing]` or `yaml[line-length]` violations appear, fix them **before** committing.

## Troubleshooting

| Symptom | Action |
|--------|--------|
| `Unknown command` in `.cisshgo.log` | Add the exact command string to **`transcript_map.yaml`** (platform or scenario step). |
| Address already in use | `molecule destroy -s ...` or raise **`CISSHGO_PORT`**. |
| Assertion failures on `before`/`after`/`gathered` | Fix transcript `.txt` bodies to exactly match vars `<state>.after` structure. See **After transcript files must match vars exactly**. Use **`state: parsed`** + file lookup to diff against vars. |
| **`% Invalid input`** on a config command | **Sequence desync** -- the transcript_map sequence order does not match the module's emit order. Read `self.parsers` from the module source (see **Determining emit order**) and reorder the sequence. Do NOT just guess or use vars `commands` order. |
| **`% Invalid input`** on `switchport trunk ... vlan add ...` | The module uses `add`/`remove` subcommands for vlan lists when `have` already has vlans. See **VLAN list commands** section. Update the transcript_map to use `add <delta>` or `remove <excess>` instead of the full vlan list. |
| merged_again wrong `before` | Second merge's first **`show`** must still reflect **`merged.after`** body (`after.txt`). |
| merged_again `after` assertion fails | Check that `after_again.txt` matches `merged_again['after']` in vars exactly -- keys may differ from `merged['after']` (e.g. a key present in `merged.after` may be absent in `merged_again.after`). |
| `symmetric_difference` fails on `commands` for vlan states | Vars `commands` may list full vlan ranges while module emits `add`/`remove` deltas. Relax the command assertion to check `changed` and `length` instead. See **Vars commands vs actual module result**. |
| Wrong behavior after editing `transcript_map.yaml` only | **Stale cisshgo** -- see **Reloading cisshgo after fixture edits**; `molecule destroy` then full test. |
| **`merged`** emits interfaces in an order that changes between runs | **`dict_merge` new-key order** -- see **`dict_merge` key order for new top-level interfaces**; set **`PYTHONHASHSEED: "0"`** or re-capture **`-vvv`** on CML and lock sequence. |
| `check_mode` then normal apply desyncs | Use a **fresh** SSH session / scenario; do not assume check_mode and apply share the same cisshgo pointer without transcript design. |

## Iteration playbook (same rule as **Completion rule**)

Use this when **`molecule test`** fails; do not stop until step 6 succeeds.

1. **Run:** `molecule test -s <scenario>` from **`ansible_collections/cisco/ios/extensions`** with **`CISSHGO_BIN_PATH`** (or repo path) set.
2. **If converge fails with `% Invalid input`:** read **`.cisshgo.log`** (expected vs received). Fix **emit order** in **`transcript_map.yaml`** using **CML `-vvv`** > module **`self.parsers`** > never vars `commands` order alone. For vlan deltas, see **VLAN list commands**. Then **`molecule destroy -s <scenario>`** and **`molecule test`** again.
3. **If verify fails (`Unknown command`):** add the exact string to platform **`command_transcripts`** or scenario **`sequence`**; re-run full **`molecule test`**.
4. **If asserts fail on `before`/`after`/`gathered`:** fix **`*.txt`** to match vars structure and parser normalization (e.g. IPv6 casing); use **`state: parsed`** to diff. If vars **`commands`** order is wrong for multiset, use **Molecule-only vars** (see **When integration commands / before order**).
5. **Repeat** from step 1 until exit code **0**.
6. **Only then** mark the task complete or report success to the user.

## Definition of done

- **`molecule test -s <scenario>`** has been executed successfully in this session: **create**, **converge**, **verify**, **destroy**, **exit code 0**.
- `verify.yml` reports zero **Unknown command** lines in `.cisshgo.log`.
- No edits under collection **`plugins/`** or **`tests/`**; fixtures match integration **vars** (for structured data) and **lab/module** emit behavior for sequences.
- **`ansible-lint`** passes on the scenario tree.
- **`extensions/molecule/README.md`** (or collection doc) lists the scenario if it is new.
