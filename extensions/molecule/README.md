# Molecule scenarios (`cisco.ios` extensions)

Run from this directory’s parent (`ansible_collections/cisco/ios/extensions`):

```bash
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../.."
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH for go build

molecule test -s cisshgo_ios_interfaces
molecule test -s cisshgo_ios_l2_interfaces
```

Scenarios:

- **`cisshgo_ios_interfaces`** — `ios_interfaces` (gathered, merged, replaced, parsed, rendered); **3** listener ports from `CISSHGO_PORT`.
- **`cisshgo_ios_l2_interfaces`** — `ios_l2_interfaces` (gathered, merged + idempotency); **2** listener ports.

Default base port is **10000** (`CISSHGO_PORT`). Run scenarios **sequentially** so `destroy` frees ports before the next scenario.

**Scaling to multiple modules**, port rules, authoring checklist, and cisshgo pitfalls: [MULTI_MODULE_CISSHGO.md](MULTI_MODULE_CISSHGO.md).

To run **all** Molecule scenarios from `extensions/`, set `ANSIBLE_COLLECTIONS_PATH` as above, then `molecule test --all` (each scenario’s `molecule.yml` must expose the collections path where needed).
