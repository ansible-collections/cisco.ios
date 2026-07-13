# Resource Module Development — cisco.ios

## The 7-File Pattern

Every resource module in cisco.ios consists of exactly 7 tightly-coupled files plus
a registration edit. All must stay consistent — changing one without the others causes
silent failures or runtime errors.

```
plugins/
  modules/
    ios_<rm>.py                                      # 1. Entry point + DOCUMENTATION
  module_utils/network/ios/
    argspec/<rm>/<rm>.py                             # 2. ArgumentSpec class
    argspec/<rm>/__init__.py                         # 3. Package init (empty)
    config/<rm>/<rm>.py                              # 4. Config class (CRUD logic)
    config/<rm>/__init__.py                          # 5. Package init (empty)
    rm_templates/<rm>.py                             # 6. Parser templates
    facts/<rm>/<rm>.py                               # 7. Facts class
    facts/facts.py                                   # EDIT: register new Facts class
tests/
  unit/modules/network/ios/test_ios_<rm>.py         # Unit test scaffold
```

## Class Naming Convention

Underscores are **kept** in class names — do not camel-case across underscores.

| Resource        | Module class    | ArgSpec             | Facts                | Template                |
| --------------- | --------------- | ------------------- | -------------------- | ----------------------- |
| `vlans`         | `Vlans`         | `VlansArgs`         | `VlansFacts`         | `VlansTemplate`         |
| `bgp_global`    | `Bgp_global`    | `Bgp_globalArgs`    | `Bgp_globalFacts`    | `Bgp_globalTemplate`    |
| `l2_interfaces` | `L2_interfaces` | `L2_interfacesArgs` | `L2_interfacesFacts` | `L2_interfacesTemplate` |

## Resource Types

### Dict-based (single-instance)

For resources where there is exactly one instance on the device: `hostname`, `logging_global`, `ntp_global`.

- `self.want` / `self.have` are dicts
- `generate_commands()` compares two dicts
- Facts returns a single dict

### List-based (multi-instance)

For resources where multiple entries are identified by a key: `vlans`, `interfaces`, `acls`, `bgp_address_family`.

- Indexed by `list_key` (e.g. `vlan_id`, `name`, `afi`)
- `wantd = {entry[list_key]: entry for entry in conf_want}`
- `generate_commands()` iterates keyed entries
- Facts returns a list of dicts

## rm_templates: The Most Common Bug Source

The `rm_templates` file defines parser templates using `NetworkTemplate` from netcommon.

```python
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_templates import (
    NetworkTemplate,
)

class VlansTemplate(NetworkTemplate):
    PARSERS = [
        {
            "name": "vlan_id",
            "getval": re.compile(r"^vlan (?P<vlan_id>\d+)"),
            "setval": "vlan {{ vlan_id }}",
            "compval": "vlan_id",          # ← MUST match key in result dict
            "result": {
                "vlans": {
                    "{{ vlan_id }}": {
                        "vlan_id": "{{ vlan_id }}",
                    }
                }
            },
        },
    ]
```

### compval Pitfall

`compval` must match the **dot-path** to the value inside `result`. If it doesn't match,
comparisons silently return no diff and no commands are generated.

```python
# WRONG — compval doesn't match nesting
"compval": "name",
"result": {"vlans": {"{{ vlan_id }}": {"name": "{{ name }}"}}}

# CORRECT — compval matches the path into result
"compval": "vlans.{{ vlan_id }}.name",
```

When reviewing a PR, always cross-check `compval` against the `result` structure.

## States Supported

All resource modules must support these states:

| State        | Behavior                                               |
| ------------ | ------------------------------------------------------ |
| `merged`     | Merge want into have — add/update, no deletes          |
| `replaced`   | Replace specific entries — delete entries not in want  |
| `overridden` | Replace ALL entries — delete anything not in want      |
| `deleted`    | Delete specified entries (or all if none specified)    |
| `gathered`   | Parse running config into structured data (no changes) |
| `rendered`   | Render CLI from want without connecting to device      |
| `parsed`     | Parse provided text into structured data (offline)     |

## Registering a New Facts Class

After creating `facts/<rm>/<rm>.py`, edit `facts/facts.py`:

```python
# Add import (alphabetical order)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.<rm>.<rm> import (
    <Rm>Facts,
)

# Add to FACT_RESOURCE_SUBSETS dict (alphabetical order)
FACT_RESOURCE_SUBSETS = dict(
    ...
    <rm>=<Rm>Facts,
    ...
)
```

Forgetting this step causes `ModuleNotFoundError` at runtime.
