# cisco.ios Molecule + CISSHGO — Architecture & Workflow Reference

This document is the long-form companion to the per-directory `README.md`.
It explains **every file** in `extensions/molecule/`, **why it exists**, the
**naming conventions** that tie them together, and a full **end-to-end walk**
through what happens on `molecule test -s <scenario>` (locally and in CI).

---

## 1. Goals of this harness

1. **Run real resource-module integration tests without a real device.**
   The cisco.ios collection has a large `tests/integration/targets/ios_*/`
   suite, which normally needs a CML / vIOS lab. Here we stand up
   [CISSHGO](https://github.com/tbotnz/cisshgo) — a Go SSH server that
   replays captured `show`/config-exec output — and point the resource
   modules at `127.0.0.1:<port>` over `network_cli`.
2. **Keep each module's test isolated.** Every resource module is a
   **molecule scenario** (`extensions/molecule/<module>/`) with its own
   `converge.yml`, inventory, and cisshgo process.
3. **Share all the plumbing.** Start, stop, log-scan, binary resolution,
   and version pinning live once under `_shared/` and `cisshgo_fixtures/`.
4. **Zero-edit onboarding for new modules.** CI auto-discovers scenarios,
   so adding `extensions/molecule/<new_module>/` is enough — the workflow
   picks it up on the next push.

---

## 2. Directory layout (every file explained)

```text
extensions/molecule/
├── README.md                            contributor quick-start (short)
├── ARCHITECTURE.md                      this file — long-form reference
│
├── _shared/                             shared lifecycle playbooks
│   ├── create.yml                       resolve + launch cisshgo
│   ├── destroy.yml                      stop cisshgo, free ports
│   └── verify.yml                       scan log for FATAL/panic
│
├── cisshgo_fixtures/                    shared test data (not a scenario)
│   ├── CISSHGO_VERSION                  pinned release tag (e.g. v0.2.0)
│   ├── transcript_map.yaml              command -> transcript mapping (all modules)
│   ├── inventories/
│   │   ├── ansible/                     ansible-playbook --inventory
│   │   │   ├── hostname.yaml
│   │   │   ├── interfaces.yaml
│   │   │   └── ...                      (one per module)
│   │   └── cisshgo/                     cisshgo --inventory (Go-server)
│   │       ├── hostname.yaml
│   │       ├── interfaces.yaml
│   │       └── ...                      (one per module)
│   └── transcripts/                     raw captured device output
│       ├── common/
│       │   ├── show_privilege.txt       `show privilege`
│       │   └── show_version.txt         `show version`
│       ├── generic_empty_return.txt     reply for no-op exec cmds
│       ├── ios_hostname/
│       │   ├── show_running-config.txt  gathered state transcript
│       │   └── scenarios/
│       │       ├── ios-hostname-merged/{before,after}.txt
│       │       └── ios-hostname-deleted/{before,after}.txt
│       ├── ios_interfaces/
│       │   ├── show_running-config_...  gathered state transcript
│       │   └── scenarios/
│       │       ├── ios-interfaces-merged/{before,after}.txt
│       │       └── ios-interfaces-replaced/{before,after}.txt
│       └── ...                          (one dir per module)
│
├── hostname/                            scenario: cisco.ios.ios_hostname
│   ├── molecule.yml                     driver/provisioner/test_sequence
│   ├── vars.yml                         inputs for _shared/*.yml
│   └── converge.yml                     actual test plays
│
├── interfaces/                          scenario: cisco.ios.ios_interfaces
│   ├── molecule.yml
│   ├── vars.yml
│   └── converge.yml
│
└── ...                                  (32 scenario dirs total)
```

### 2.1 Naming contract

The harness is glued together by **one identifier** per scenario:
`scenario_name` (set in `vars.yml`). Everything else is derived from it.

| Artefact | Path |
|----------|------|
| Scenario dir | `extensions/molecule/<scenario_name>/` |
| Ansible inventory | `cisshgo_fixtures/inventories/ansible/<scenario_name>.yaml` |
| Cisshgo inventory | `cisshgo_fixtures/inventories/cisshgo/<scenario_name>.yaml` |
| Cisshgo log | `/tmp/cisshgo-<scenario_name>.log` |
| pgrep match | `cisshgo.*--inventory.*inventories/cisshgo/<scenario_name>.yaml` |

---

## 3. File-by-file walkthrough

### 3.1 `_shared/create.yml` — start cisshgo

Runs on `localhost` with `connection: local`. It:

1. **Gathers platform-only facts** via explicit `ansible.builtin.setup`
   with `gather_subset: [!all, !min, platform]` to avoid triggering
   `ios_facts` if `ansible_network_os` leaks to localhost.
2. **Resolves the cisshgo binary** in order:
   - `$CISSHGO_BIN` env var (developer override)
   - `../../../../../cisshgo/cisshgo` sibling repo checkout
   - Pinned release download from GitHub releases
3. **Kills stale processes** for this scenario via pgrep/pkill.
4. **Starts cisshgo** via `nohup` from `cisshgo_fixtures/` directory
   (so relative transcript paths resolve correctly).
5. **Waits for every listener port** declared in `listener_ports`.

### 3.2 `_shared/destroy.yml` — stop cisshgo

Same pattern. `pgrep` by scenario signature, `kill`, `wait_for: stopped`.

### 3.3 `_shared/verify.yml` — log sanity

Reads `/tmp/cisshgo-<scenario>.log`, asserts no `FATAL`/`panic`.

### 3.4 `cisshgo_fixtures/CISSHGO_VERSION`

Single line with the pinned release tag (e.g. `v0.2.0`).

### 3.5 `cisshgo_fixtures/transcript_map.yaml`

The cisshgo server's routing table containing all 32 modules:

- `platforms:` — stateless devices (gathered/parsed/rendered).
  Each platform key is `ios_<module>` (e.g., `ios_hostname`, `ios_interfaces`).
- `scenarios:` — stateful devices with ordered `sequence:` of
  `(command, transcript)` pairs.

Transcript paths are **relative to `cisshgo_fixtures/`**.

### 3.6 `cisshgo_fixtures/transcripts/**`

Per-module directories (`ios_<module>/`) with scenario subdirs.
`common/show_privilege.txt`, `common/show_version.txt`, and
`generic_empty_return.txt` are shared across all modules.

### 3.7 The two inventory files per module

- `inventories/cisshgo/<module>.yaml` — Go binary format, consumed via
  `--inventory`. References platform and scenario IDs from transcript_map.
- `inventories/ansible/<module>.yaml` — Standard Ansible inventory with
  `ios_cisshgo` group containing per-host port assignments.

---

## 4. End-to-end run walkthrough

```text
cwd = cisco/ios/extensions

1. molecule reads extensions/molecule/<module>/molecule.yml
   - sets MOLECULE_SCENARIO_DIRECTORY
   - picks up --inventory= from ansible.executor.args

2. test_sequence = [create, converge, verify, destroy]

3. create  → _shared/create.yml
   - loads <module>/vars.yml (scenario_name, listener_ports)
   - resolves cisshgo binary
   - launches cisshgo from cisshgo_fixtures/ directory
   - waits for all listener ports

4. converge → <module>/converge.yml
   - gathered: show commands → parser → assert against vars/main.yaml
   - merged: before → config → after → assert + idempotency
   - replaced/overridden/deleted: same pattern
   - parsed/rendered: offline, no config push

5. verify  → _shared/verify.yml
   - asserts no FATAL/panic in cisshgo log

6. destroy → _shared/destroy.yml
   - kills cisshgo, frees ports
```

---

## 5. Adding a new module (checklist)

1. **Capture transcripts** on a real device and place under
   `cisshgo_fixtures/transcripts/ios_<module>/`.
2. **Register in `transcript_map.yaml`** — add platform entry under
   `platforms:` and scenario entries under `scenarios:`.
3. **Create both inventories** as `<module>.yaml` under
   `inventories/cisshgo/` and `inventories/ansible/`.
4. **Create scenario dir** `extensions/molecule/<module>/` with
   `vars.yml`, `molecule.yml`, and `converge.yml`.
5. **Local smoke**: `molecule test -s <module>`.
6. **Push** — CI auto-discovers it.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `glob failed` | Wrong cwd | `cd extensions` first |
| `socket_path must be a value` on localhost | `ansible_network_os` leaked to `all:` | Keep network vars on `ios_cisshgo` child group |
| `Permission denied` | `CISSHGO_BIN` points to directory | Point to the binary file inside the repo |
| `unmarshal errors` | Wrong inventory format for cisshgo | Use `inventories/cisshgo/` format, not ansible |
| `Timeout waiting for port` | cisshgo crashed | Check `/tmp/cisshgo-<scenario>.log` |
| Assertion fails | Transcript doesn't match expected vars | Align transcript; `vars/main.yaml` is ground truth |
| `% Invalid input` | Emit order mismatch in transcript_map | Re-capture emit order from CML with `check_mode: true` |
