# Molecule + cisshgo: multiple resource modules (this collection)

This file lives in the collection so clone consumers have the same guidance as the fork. It extends the single-module POC with a **second** scenario and documents how to add more.

## Scenarios

| Scenario                    | Module                        | Listeners (default `CISSHGO_PORT=10000`) | Purpose                                      |
| --------------------------- | ----------------------------- | ---------------------------------------- | -------------------------------------------- |
| `cisshgo_ios_interfaces`    | `cisco.ios.ios_interfaces`    | 3 (platform + merged + replaced)         | gathered, merged, replaced, parsed, rendered |
| `cisshgo_ios_l2_interfaces` | `cisco.ios.ios_l2_interfaces` | 5 (platform + 4 scenario listeners)      | gathered, merged + merged_again, replaced, overridden, deleted, parsed, rendered |

Paths: `extensions/molecule/<scenario>/`.

## How to run

From `extensions/`:

```bash
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH to build from source

molecule test -s cisshgo_ios_interfaces
molecule test -s cisshgo_ios_l2_interfaces
```

Run **cisshgo** scenarios **one after another** so each `destroy` releases ports. Both reuse base port **10000** by default.

`molecule test --all` runs every scenario under `extensions/molecule/`. **Every** scenario’s `molecule.yml` (or legacy `ansible.env`) should set `ANSIBLE_COLLECTIONS_PATH` like the cisshgo scenarios, or export it in the shell before `--all`, so `cisco.ios` resolves for all plays.

## Port convention

- **`CISSHGO_PORT`**: default `10000`; each scenario uses `cisshgo_port_count` consecutive ports (`create.yml` / `destroy.yml` + `inventory/hosts.yml`).
- Reuse the same base port across modules: complete **`destroy`** before the next scenario.

## Do not edit integration tests or plugins for Molecule

**Source of truth** for assertions is `tests/integration/targets/<module>/vars/main.yaml`. If a transcript or scenario is wrong, change **only** files under `extensions/molecule/<scenario>/` (fixtures, playbooks), not `tests/` or `plugins/`.

## Gathered transcripts vs `vars`

The platform transcript for `show running-config | section ^interface` must parse to **exactly** what `gathered['config']` expects. Validate with `state: parsed` and `running_config: "{{ lookup('file', '…/that_transcript.txt') }}"` on a `network_cli` host. Omit empty `interface …` / `!` blocks that add extra `{name: …}` entries, and omit L2 lines that vars do not expect on the **gathered** fixture.

## Scenario `sequence` order vs `vars` `commands`

The **`sequence`** in `transcript_map.yaml` must match the **exact order** Ansible sends commands. Do **not** assume `merged['commands']` in vars matches emit order (and for vlan lists, vars may show full ranges while the module emits `switchport trunk ... vlan add` / `remove` deltas). Derive order from **`self.parsers`** and **`compare_list()`** in `plugins/module_utils/network/ios/config/<module>/<module>.py`, from **`state: rendered`**, or from **`-vvv`** on a lab run. Wrong order causes cisshgo desync and **`% Invalid input`**, which the ios terminal plugin treats as failure.

## Checklist: new `cisshgo_<module>` scenario

1. Copy `cisshgo_ios_l2_interfaces/` (or `cisshgo_ios_interfaces/`) and rename.
2. Update `molecule.yml` (scenario name, platforms / groups).
3. Set `cisshgo_port_count` in `create.yml` and `destroy.yml` (platform + one per scenario listener).
4. `inventory/hosts.yml`: `ansible_port` = base, base+1, …
5. Author `cisshgo_inventory.yaml` + `transcript_map.yaml` (platform + scenarios). See cisshgo upstream docs on **scenario** sequences (interactive mode, ordered steps).
6. `converge.yml`: `vars_files` from `tests/integration/targets/<module>/vars/main.yaml`; mirror integration assertions as needed.
7. `molecule test -s <scenario>`; extend `transcript_map.yaml` for any **Unknown command** lines in `.cisshgo.log`.

## Lint (Molecule YAML)

Collection **ansible-lint** uses `profile: production`. Name every play and task; use FQCN for builtins (`ansible.builtin.*`). Run `ansible-lint extensions/molecule/<scenario>/` from the collection root.
