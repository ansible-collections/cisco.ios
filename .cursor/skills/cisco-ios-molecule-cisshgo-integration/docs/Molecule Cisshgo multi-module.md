# Molecule + cisshgo: multiple resource modules

**Canonical** workflow, port math, emit-order rules, RTT sequencing, gathered transcript validation, and the **mandatory "run Molecule until green"** loop are maintained in:

**[../SKILL.md](../SKILL.md)**

For a **short** list of scenario directories and commands, see **[`ansible_collections/cisco/ios/extensions/molecule/README.md`](../../../../ansible_collections/cisco/ios/extensions/molecule/README.md)**.

The collection stub **[`MULTI_MODULE_CISSHGO.md`](../../../../ansible_collections/cisco/ios/extensions/molecule/MULTI_MODULE_CISSHGO.md)** only points at the skill and README; avoid duplicating long tables there.

## How to run

From `ansible_collections/cisco/ios/extensions/`:

```shell
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../.."
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH to build from source

molecule test -s <scenario_name>
```

Run scenarios **one after another** so each `destroy` releases ports (default base port `CISSHGO_PORT=10000`).
