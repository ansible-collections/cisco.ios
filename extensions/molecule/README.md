# Molecule scenarios (cisco.ios)

| Scenario | Module | Listeners (`cisshgo_port_count`) | States exercised |
|----------|--------|----------------------------------|------------------|
| `cisshgo_ios_interfaces` | `ios_interfaces` | 3 | gathered, merged, replaced, parsed, rendered |
| `cisshgo_ios_l2_interfaces` | `ios_l2_interfaces` | 5 | gathered, merged + merged_again, replaced, overridden, deleted, parsed, rendered |

Run from `ansible_collections/cisco/ios/extensions/`:

```bash
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH for go build
molecule test -s cisshgo_ios_l2_interfaces
```

See [MULTI_MODULE_CISSHGO.md](MULTI_MODULE_CISSHGO.md) for port conventions, `ANSIBLE_COLLECTIONS_PATH`, and multi-scenario notes.
