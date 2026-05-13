# cisco.ios Molecule + CISSHGO test harness

Each subdirectory of `extensions/molecule/` is one molecule scenario that
exercises a single `cisco.ios.ios_<module>` resource module against the
[CISSHGO](https://github.com/tbotnz/cisshgo) Go SSH fixture server.

## Layout

```
extensions/molecule/
├── README.md                          (this file)
├── _shared/                           shared lifecycle playbooks
│   ├── create.yml                     resolve + start cisshgo
│   ├── destroy.yml                    stop cisshgo, free ports
│   └── verify.yml                     scan log for FATAL/panic
├── cisshgo_fixtures/                  shared test data
│   ├── CISSHGO_VERSION                pinned cisshgo release tag
│   ├── transcript_map.yaml            command -> transcript mapping
│   ├── inventories/
│   │   ├── ansible/                   ansible-playbook --inventory files
│   │   │   ├── interfaces.yaml
│   │   │   └── l2_interfaces.yaml
│   │   └── cisshgo/                   cisshgo --inventory files (Go server)
│   │       ├── interfaces.yaml
│   │       └── l2_interfaces.yaml
│   └── transcripts/                   captured device output
└── <scenario>/                        one per resource module
    ├── molecule.yml                   driver/provisioner/test_sequence
    ├── vars.yml                       inputs for _shared playbooks
    └── converge.yml                   actual integration test plays
```

## Run a scenario locally

```bash
cd cisco/ios/extensions
molecule test -s interfaces
```

The shared `create.yml` resolves the cisshgo binary in this order:

1. `$CISSHGO_BIN` if set (developer override)
2. `../../../../../cisshgo/cisshgo` — sibling checkout of the cisshgo repo
3. Downloaded release archive pinned by `cisshgo_fixtures/CISSHGO_VERSION`

Set `CISSHGO_VERSION=v1.2.3` to override the pin without editing the file.

## CI

`.github/workflows/molecule.yml` auto-discovers every scenario directory and
runs each one in its own matrix job. Adding a new scenario does **not**
require a workflow edit.

## Adding a new resource-module scenario

1. Capture transcripts on a real device (or hand-craft them) and drop them
   under `cisshgo_fixtures/transcripts/cisco/ios/`.
2. Register the command -> transcript mapping in
   `cisshgo_fixtures/transcript_map.yaml`. Stateful operations (`merged`,
   `replaced`, `deleted`) go under the `scenarios:` block; gathered/parsed
   stays under `command_transcripts:`.
3. Create two inventories, both keyed by `<module>.yaml`:
   - `cisshgo_fixtures/inventories/cisshgo/<module>.yaml` — cisshgo-format
     (`devices:` list of `platform:`/`scenario:` entries with a `count`).
     Consumed by the Go server via `--inventory`.
   - `cisshgo_fixtures/inventories/ansible/<module>.yaml` — ansible-style
     (`all.children.ios_cisshgo.children.<group>.hosts`). Consumed by
     ansible-playbook during converge. Ports start at 10000 and match the
     order of entries in the cisshgo inventory above.
4. Create `extensions/molecule/<module>/`:
   - `vars.yml` with `scenario_name` and `listener_ports`
   - `molecule.yml` (copy from `interfaces/molecule.yml`, change names +
     the `--inventory=` path to `inventories/ansible/<module>.yaml`)
   - `converge.yml` with the test plays — typically `vars_files`-include the
     module's existing
     `tests/integration/targets/ios_<module>/vars/main.yaml`
5. `molecule test -s <module>` locally, then open a PR. CI runs the new
   scenario automatically.

Every scenario uses `--starting-port 10000` because the molecule lifecycle
frees the listeners between scenarios. CI parallelism happens at the job
level, not the port level.
