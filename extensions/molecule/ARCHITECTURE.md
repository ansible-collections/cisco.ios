# cisco.ios Molecule + CISSHGO — Architecture & Workflow Reference

This document is the long-form companion to the per-directory `README.md`.
It explains **every file** in `extensions/molecule/`, **why it exists**, the
**naming conventions** that tie them together, and a full **end-to-end walk**
through what happens on `molecule test -s <scenario>` (locally and in CI).

Target audience: a new contributor (or future us) who needs to add a new
resource-module scenario, debug a failing run, or port this harness to
another network collection.

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

## 2. Why two test layers? (cisshgo vs. resource module)

The cisco.ios collection already ships a large `tests/integration/` tree —
those targets assume a live device and are intended for CML/vIOS in
nightly CI. This harness is **complementary**, not a replacement:

| Layer                             | Driver                     | Network              | Use cases                |
| --------------------------------- | -------------------------- | -------------------- | ------------------------ |
| `tests/integration/targets/ios_*` | `ansible-test integration` | real device (CML)    | nightly + release gating |
| `extensions/molecule/<module>/`   | `molecule test`            | cisshgo on 127.0.0.1 | every PR, fast feedback  |

The molecule layer **reuses** the resource module's `vars/main.yaml` from
the integration target (via `vars_files`) so the expected/desired state
stays in one place. The transcripts are chosen so the parser output
matches those existing vars.

---

## 3. Directory layout (every file explained)

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
│   ├── CISSHGO_VERSION                  pinned release tag (e.g. v0.5.0)
│   ├── transcript_map.yaml              command -> transcript mapping
│   ├── inventories/
│   │   ├── ansible/                     ansible-playbook --inventory
│   │   │   ├── interfaces.yaml
│   │   │   └── l2_interfaces.yaml
│   │   └── cisshgo/                     cisshgo --inventory (Go-server)
│   │       ├── interfaces.yaml
│   │       └── l2_interfaces.yaml
│   └── transcripts/                     raw captured device output
│       ├── common/
│       │   ├── show_privilege.txt       `show privilege`
│       │   └── show_version.txt         `show version`
│       ├── generic_empty_return.txt     reply for no-op exec cmds
│       ├── ios_interfaces/
│       │   ├── gathered.txt             stateless `show run | section ^interface`
│       │   └── scenarios/
│       │       ├── merged/{before,after}.txt
│       │       └── replaced/{before,after}.txt
│       └── ios_l2_interfaces/
│           ├── gathered.txt
│           └── scenarios/
│               └── merged/{before,after}.txt
│
├── interfaces/                          scenario: cisco.ios.ios_interfaces
│   ├── molecule.yml                     driver/provisioner/test_sequence
│   ├── vars.yml                         inputs for _shared/*.yml
│   └── converge.yml                     actual test plays
│
└── l2_interfaces/                       scenario: cisco.ios.ios_l2_interfaces
    ├── molecule.yml
    ├── vars.yml
    └── converge.yml
```

### 3.1 Naming contract (important)

The harness is glued together by **one identifier** per scenario:
`scenario_name`. Everything else is derived from it.

| artefact          | path                                                             |
| ----------------- | ---------------------------------------------------------------- |
| scenario dir      | `extensions/molecule/<scenario_name>/`                           |
| ansible inventory | `cisshgo_fixtures/inventories/ansible/<scenario_name>.yaml`      |
| cisshgo inventory | `cisshgo_fixtures/inventories/cisshgo/<scenario_name>.yaml`      |
| cisshgo log       | `/tmp/cisshgo-<scenario_name>.log`                               |
| pgrep match       | `cisshgo.*--inventory.*inventories/cisshgo/<scenario_name>.yaml` |

This is why the two inventory files must share the scenario name — the
shared `create.yml` builds both paths from `vars.scenario_name` alone.

---

## 4. File-by-file walkthrough

### 4.1 `_shared/create.yml` — start cisshgo

Runs on `localhost` with `connection: local`. It:

1. **Gathers platform-only facts** via an explicit `ansible.builtin.setup`
   with `gather_subset: [!all, !min, platform]`. We avoid implicit
   `gather_facts: true` because if any inventory leaked
   `ansible_network_os` onto `all:`, Ansible would dispatch
   `cisco.ios.ios_facts` against localhost and fail with
   `socket_path must be a value`.
2. **Hard-overrides** `ansible_network_os: ""` and
   `ansible_connection: local` in play vars — belt-and-braces against the
   same leakage.
3. **Resolves the cisshgo binary** in order:
   - `$CISSHGO_BIN` env var (developer override — fastest iteration loop
     when hacking on cisshgo itself).
   - `../../../../../cisshgo/cisshgo` sibling repo checkout.
   - Pinned release download from
     `github.com/tbotnz/cisshgo/releases/download/<CISSHGO_VERSION>/` — the
     CI and fresh-clone path.
     Falls into a `stat` + `assert` that the resolved path is a **regular
     file** (catches the common mistake of `export CISSHGO_BIN=…/cisshgo`
     pointing at the _repo_ instead of the binary inside it).
4. **Kills stale processes** for this scenario via
   `pkill -f "cisshgo.*--inventory.*inventories/cisshgo/<scenario_name>.yaml"`.
5. **Starts cisshgo** via `nohup` — `cd`-ing into `cisshgo_fixtures/`
   first so relative transcript paths in `transcript_map.yaml` resolve
   correctly — and redirects stdout/stderr to `/tmp/cisshgo-<scenario>.log`.
6. **Snapshots the log** 2 seconds later and fails fast on any of
   `FATAL` / `panic:` / `Permission denied` / `no such file or directory`
   / `command not found`. This is what surfaces misconfigurations before
   the `wait_for` timeout.
7. **Waits for every listener port** declared in `listener_ports`. On
   timeout, dumps the full log into the Ansible output so CI logs contain
   the cisshgo reason.

### 4.2 `_shared/destroy.yml` — stop cisshgo

Same `localhost / connection: local` pattern. `pgrep` by the same
scenario-matching signature, `kill` each PID, `wait_for: state: stopped`
on every listener port (with `failed_when: false` so a clean run doesn't
fail the destroy if the ports are already released).

### 4.3 `_shared/verify.yml` — log sanity

Cats `/tmp/cisshgo-<scenario>.log`, echoes it (so CI artefacts contain it
even on green runs when `--log` isn't collected), and asserts no
`FATAL`/`panic`.

### 4.4 `cisshgo_fixtures/CISSHGO_VERSION`

A single line with the pinned release tag (e.g. `v0.5.0`). Bumped in a
single PR when upgrading cisshgo; CI passes the value as `CISSHGO_VERSION`
env so `_shared/create.yml` uses the pinned release on clean checkouts.

### 4.5 `cisshgo_fixtures/transcript_map.yaml`

The cisshgo server's routing table. Two top-level blocks:

- `platforms:` — **stateless** devices. Each command always returns the
  same transcript. Used for `gathered` / `parsed` / `rendered`.
- `scenarios:` — **stateful** devices with an ordered `sequence:` of
  `(command, transcript)` pairs. The first `show running-config …` call
  returns `before.txt`; after the config commands run, the **same**
  command returns `after.txt`. Used for `merged` / `replaced` /
  `overridden` / `deleted`.

Transcript paths in this file are **relative to `cisshgo_fixtures/`**,
which is exactly the directory the `_shared/create.yml` `cd`s into
before launching cisshgo.

### 4.6 `cisshgo_fixtures/transcripts/**`

Plain text captures of device output. Naming is `<module>/<type>.txt` for
stateless and `<module>/scenarios/<state>/<phase>.txt` for stateful
(`phase ∈ {before, after}`).

`common/show_privilege.txt`, `common/show_version.txt`, and
`generic_empty_return.txt` are shared across all platforms because
`network_cli` issues the same boilerplate during session setup regardless
of module.

### 4.7 The two inventory files

We deliberately split the ansible and cisshgo inventories because they
are **different formats** even though they describe the same fixture.

#### `cisshgo_fixtures/inventories/cisshgo/<scenario>.yaml`

Consumed by the cisshgo Go binary via `--inventory`. Schema:

```yaml
devices:
  - platform: <platform_id_from_transcript_map> # stateless
    count: 1
  - scenario: <scenario_id_from_transcript_map> # stateful
    count: 1
```

`cisshgo` binds each entry to a TCP port starting at `--starting-port`,
**in order**. So the first entry becomes `:10000`, the second `:10001`,
and so on. This is why the Ansible inventory's port numbers must line
up.

#### `cisshgo_fixtures/inventories/ansible/<scenario>.yaml`

Consumed by `ansible-playbook` during `converge`. Schema:

```yaml
all:
  children:
    ios_cisshgo: # <-- network vars live here
      vars:
        ansible_connection: ansible.netcommon.network_cli
        ansible_network_os: cisco.ios.ios
        ansible_user: admin
        ansible_password: admin
        ansible_host: 127.0.0.1
        ansible_become: true
        ansible_become_method: enable
        ansible_become_password: admin
        ansible_ssh_common_args: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
      children:
        <module>_gathered:
          hosts:
            cisshgo-<short>-gathered:
              ansible_port: 10000
        <module>_merged:
          hosts:
            cisshgo-<short>-merged:
              ansible_port: 10001
        # … one child group per stateful scenario
```

**Why the `ios_cisshgo` child group instead of `all.vars`?**
`ansible_network_os` and `ansible_connection` must **not** apply to
`localhost` (the host the shared playbooks run on). If we scope them to
`all`, implicit localhost inherits them and Ansible dispatches
`ios_facts` on it, which fails because there's no `socket_path`. Scoping
to a child group keeps the network context where it belongs — on the
cisshgo hosts only.

### 4.8 `<scenario>/vars.yml`

The **only** per-scenario input for `_shared/*.yml`. Two keys:

```yaml
scenario_name: <name> # e.g. interfaces, l2_interfaces
listener_ports: # must match the cisshgo inventory order
  - 10000
  - 10001
```

The scenario name drives both inventory paths and the log/pgrep signature
(see §3.1). `listener_ports[0]` is used as `--starting-port`; the rest
are only used by `wait_for` in `create.yml` and `destroy.yml`.

### 4.9 `<scenario>/molecule.yml`

A minimal molecule config:

```yaml
driver:
  name: default # we manage infra ourselves

platforms:
  - name: cisshgo-<short>-gathered
  - name: cisshgo-<short>-merged
  # … (names for display only; molecule requires the list)

ansible:
  executor:
    args:
      ansible_playbook:
        - --inventory=${MOLECULE_SCENARIO_DIRECTORY}/../cisshgo_fixtures/inventories/ansible/<scenario>.yaml

provisioner:
  name: ansible
  playbooks:
    create: ../_shared/create.yml
    converge: converge.yml
    verify: ../_shared/verify.yml
    destroy: ../_shared/destroy.yml

scenario:
  test_sequence: [create, converge, verify, destroy]

prerun: false
verifier:
  name: ansible
```

Key points:

- `driver: default` — we're not using docker/podman/vagrant, so molecule
  must not try to manage infra.
- The `--inventory=` arg is pushed onto every `ansible-playbook` invocation
  molecule makes, so `converge.yml` sees the cisshgo fixture hosts.
- `MOLECULE_SCENARIO_DIRECTORY` is set by molecule itself and points to
  the current `<scenario>/` dir. All path lookups hang off it so running
  from any cwd works.

### 4.10 `<scenario>/converge.yml`

The actual **test logic** — the only file that changes meaningfully
between modules. It contains one play per state being tested:

- `gathered` — runs against `<module>_gathered` (port 10000).
- `merged` (+ idempotency check) — runs against `<module>_merged`
  (port 10001). Asserts `before`, `after`, and the generated command
  list, then re-applies to assert `changed: false`.
- `replaced` / `overridden` / `deleted` — each against its own port/child
  group with its own `before`/`after` transcripts.
- `parsed` — `state: parsed` against a `.cfg` file from the real
  integration target. **Runs against `<module>_gathered`**, not
  `localhost`, because the resource-module action plugin rejects
  `connection: local` even for offline states.
- `rendered` — same rationale as `parsed`.

`converge.yml` always `vars_files`-includes the real integration
target's `vars/main.yaml` so the expected state is shared between the
two test layers.

### 4.11 `.github/workflows/molecule.yml`

Three jobs, job-level parallelism:

1. **`discover`** — checks out the collection, runs
   `find -mindepth 2 -maxdepth 2 -name molecule.yml` inside
   `extensions/molecule`, strips `_shared` and `cisshgo_fixtures`, and
   emits a JSON matrix of scenario names as job output. Also reads
   `CISSHGO_VERSION` and exposes it as an output.
2. **`molecule`** — matrix job, one per scenario × python × ansible.
   Installs ansible (`stable-2.20` tarball), `molecule>=24.0`, plus
   `ansible.netcommon` / `ansible.utils` from git. Runs
   `molecule test -s "${{ matrix.scenario }}"` from
   `cisco/ios/extensions`. On failure, uploads `/tmp/cisshgo-*.log` plus
   `molecule/<scenario>/molecule.log` as an artefact with 7-day retention.
3. **`molecule-summary`** — single rollup check. Fails if any matrix
   entry failed. This is the one to mark "required" in branch protection.

Triggers: push to `main`, `pull_request_target` to `main`, manual dispatch,
and nightly at 01:00 UTC (offset from the existing `tests.yml` schedule).

---

## 5. End-to-end run walkthrough

### 5.1 Local: `molecule test -s interfaces`

```text
cwd = cisco/ios/extensions

1. molecule reads extensions/molecule/interfaces/molecule.yml
   - sets MOLECULE_SCENARIO_DIRECTORY=<…>/extensions/molecule/interfaces
   - picks up the --inventory=… arg from ansible.executor.args

2. scenario.test_sequence = [create, converge, verify, destroy]

3. create  → ansible-playbook ../_shared/create.yml
            + --inventory=<…>/inventories/ansible/interfaces.yaml
            + -e "MOLECULE_SCENARIO_DIRECTORY=…"
   - loads interfaces/vars.yml (scenario_name=interfaces,
     listener_ports=[10000,10001,10002])
   - resolves cisshgo binary (env / sibling / download)
   - pkill stale, then nohup cisshgo … > /tmp/cisshgo-interfaces.log &
   - waits for 10000, 10001, 10002 to be LISTEN

4. converge → ansible-playbook converge.yml (same --inventory)
   Plays, in order:
     a) ios_interfaces — gathered
        host: cisshgo-ios-gathered (port 10000)
        module: cisco.ios.ios_interfaces state=gathered
        → cisshgo answers "show running-config | section ^interface"
          with transcripts/ios_interfaces/gathered.txt
        → module returns facts; play asserts match
     b) ios_interfaces — merged
        host: cisshgo-ios-merged (port 10001)
        cisshgo sequence:
          show run|section → before.txt
          configure terminal → empty
          interface Gi2 / description … → empty
          interface Gi3 / … / end → empty
          show run|section → after.txt
        → module returns before, commands, after
        → play asserts all three
        → re-apply: same call returns after.txt again, module returns
          changed=false (idempotency)
     c) ios_interfaces — replaced  (same shape, port 10002)
     d) ios_interfaces — parsed    (port 10000, parses _parsed.cfg file)
     e) ios_interfaces — rendered  (port 10000, no network I/O)

5. verify  → _shared/verify.yml
   - cat /tmp/cisshgo-interfaces.log
   - assert no FATAL / panic lines

6. destroy → _shared/destroy.yml
   - pgrep cisshgo for scenario → kill
   - wait_for ports stopped
```

### 5.2 CI: pushed to main / PR

```text
discover (runs-on: ubuntu-latest)
  find -name molecule.yml in extensions/molecule
  → matrix = ["interfaces", "l2_interfaces"]
  CISSHGO_VERSION = contents of cisshgo_fixtures/CISSHGO_VERSION

molecule [scenario=interfaces, scenario=l2_interfaces]   (parallel)
  checkout collection to cisco/ios
  setup-python@v5 (3.12, pip cache)
  pip install ansible(stable-2.20) molecule>=24.0 …
  ansible-galaxy install netcommon + utils from git
  cd cisco/ios/extensions
  molecule test -s "$scenario"     ← same steps as §5.1
  on failure: upload-artifact /tmp/cisshgo-*.log + molecule.log

molecule-summary
  if any matrix entry != success → ::error:: + exit 1
  else → "OK"
```

### 5.3 Data flow per play (gathered)

```
converge.yml (ansible-playbook)
  │
  │ --inventory=inventories/ansible/interfaces.yaml
  │ host: cisshgo-ios-gathered, port: 10000
  │
  ▼
ansible.netcommon.network_cli
  │  SSH to 127.0.0.1:10000 as admin/admin
  ▼
cisshgo (Go, launched by _shared/create.yml)
  │  --inventory inventories/cisshgo/interfaces.yaml (Go-format)
  │  first device (platform: ios_interfaces) bound to :10000
  │  --transcript-map transcript_map.yaml
  │
  │  cmd: "show running-config | section ^interface"
  │  lookup in platforms.ios_interfaces.command_transcripts
  ▼
transcripts/ios_interfaces/gathered.txt   ← returned as raw stdout

  │
  ▼
network_cli parses back → ios_interfaces action plugin →
ios_interfaces facts parser → result['gathered']

  │
  ▼
assert gathered['config'] | symmetric_difference(result['gathered']) == []
(gathered var comes from tests/integration/targets/ios_interfaces/vars/main.yaml)
```

---

## 6. Adding a new module (checklist)

For a hypothetical `cisco.ios.ios_vlans` with merged + gathered:

1. **Capture transcripts** (or copy from the integration target's
   `_parsed.cfg` / runtime outputs):

   ```
   cisshgo_fixtures/transcripts/ios_vlans/gathered.txt
   cisshgo_fixtures/transcripts/ios_vlans/scenarios/merged/before.txt
   cisshgo_fixtures/transcripts/ios_vlans/scenarios/merged/after.txt
   ```

2. **Register in `transcript_map.yaml`**:
   - Add `platforms.ios_vlans:` with the stateless `command_transcripts:`.
   - Add `scenarios.ios-vlans-merged:` with the ordered `sequence:`.

3. **Create both inventories, keyed `vlans.yaml`**:
   - `inventories/cisshgo/vlans.yaml` — `devices:` list referencing
     `platform: ios_vlans` and `scenario: ios-vlans-merged`.
   - `inventories/ansible/vlans.yaml` — `ios_cisshgo` child group with
     `ios_vlans_gathered` (10000) and `ios_vlans_merged` (10001).

4. **Create the scenario dir**:

   ```
   extensions/molecule/vlans/
     vars.yml       scenario_name: vlans, listener_ports: [10000, 10001]
     molecule.yml   copy from interfaces/, update --inventory= path
     converge.yml   copy-shape, update module name + vars_files path
   ```

5. **Local smoke**:

   ```bash
   cd cisco/ios/extensions
   molecule test -s vlans
   ```

6. **Push** — CI's `discover` job auto-adds it to the matrix.

---

## 7. Troubleshooting

| symptom                                                                         | cause                                                                        | fix                                                                                                                   |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `'molecule/*/molecule.yml' glob failed`                                         | running from wrong cwd                                                       | `cd extensions` first                                                                                                 |
| `socket_path must be a value` on localhost                                      | `ansible_network_os` leaked to `all:`                                        | keep network vars on the `ios_cisshgo` child group only                                                               |
| `nohup: …/cisshgo: Permission denied`                                           | `CISSHGO_BIN` pointed at the repo dir instead of the binary                  | `export CISSHGO_BIN=/path/to/cisshgo-repo/cisshgo`                                                                    |
| `yaml: unmarshal errors: line 11: field all not found in type config.Inventory` | passed the ansible-format inventory to cisshgo                               | ensure `--inventory` points at `inventories/cisshgo/<name>.yaml`                                                      |
| `Connection type local is not valid for this module` on `parsed`/`rendered`     | action plugin needs network_cli context                                      | run the play against the gathered host, not `localhost`                                                               |
| `Timeout when waiting for 127.0.0.1:10000`                                      | cisshgo crashed on startup                                                   | look at the printed startup log snapshot, then `/tmp/cisshgo-<scenario>.log`                                          |
| gathered/after assertion fails                                                  | transcript parses to a dict that doesn't match the expected `vars/main.yaml` | align the transcript (preferred) — `vars/main.yaml` is shared with the real integration suite and is the ground truth |

---

## 8. Design decisions worth keeping

- **Two inventories, one scenario name.** The naming contract makes the
  shared playbooks trivially generic — no scenario passes file paths to
  `_shared/*`; `scenario_name` is enough.
- **`_shared` / `cisshgo_fixtures` live under `extensions/molecule/`.**
  This keeps everything molecule-related in one place and lets the
  `find -maxdepth 2 -name molecule.yml` discovery expression stay simple.
  They're excluded from the scenario matrix by name.
- **Pin cisshgo by release, not by sha.** Release tarballs are signed by
  goreleaser and cached per version in `/tmp/cisshgo-release/<ver>/`.
  `$CISSHGO_BIN` always wins locally for fast iteration.
- **Resource modules always talk to cisshgo over `network_cli`.** Even
  for offline `parsed`/`rendered`, we use a cisshgo host instead of
  `connection: local` because resource-module action plugins require a
  network context to load.
- **`vars/main.yaml` is the ground truth.** When a transcript doesn't
  parse to match, we edit the transcript, not the vars. That keeps this
  harness congruent with the existing `ansible-test integration` suite.

---

## 9. Related files outside this tree

- `.github/workflows/molecule.yml` — the CI runner (auto-discovery).
- `tests/integration/targets/ios_<module>/vars/main.yaml` — ground truth
  for expected/desired state; `vars_files`-included by `converge.yml`.
- `tests/integration/targets/ios_<module>/tests/cli/_parsed.cfg` — the
  fixture for `state: parsed` plays.
- `github.com/tbotnz/cisshgo` — the Go SSH server binary + release
  workflow (goreleaser → `cisshgo_<ver>_<os>_<arch>.tar.gz`).
