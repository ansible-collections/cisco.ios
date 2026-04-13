# Molecule scenarios (cisco.ios)

| Scenario | Module | Listeners (`cisshgo_port_count`) | States exercised |
|----------|--------|----------------------------------|------------------|
| `cisshgo_ios_hostname` | `ios_hostname` | 3 | gathered, merged, deleted, parsed, rendered |
| `cisshgo_ios_interfaces` | `ios_interfaces` | 6 | gathered, merged, replaced, overridden, deleted, parsed, rendered, **rtt** |
| `cisshgo_ios_l2_interfaces` | `ios_l2_interfaces` | 6 | gathered, merged + merged_again, replaced, overridden, deleted, parsed, rendered, **rtt** |
| `cisshgo_ios_l3_interfaces` | `ios_l3_interfaces` | 6 | gathered, merged, replaced, overridden, deleted, parsed, rendered, **rtt** |
| `cisshgo_ios_acl_interfaces` | `ios_acl_interfaces` | 6 | gathered, merged, replaced, overridden, deleted, parsed, rendered, **rtt** |
| `cisshgo_ios_ntp_global` | `ios_ntp_global` | 5 | gathered, merged, overridden, deleted, parsed, rendered, **rtt** |
| `cisshgo_ios_lldp_global` | `ios_lldp_global` | 4 | gathered, merged, replaced, deleted, parsed, rendered |
| `cisshgo_ios_logging_global` | `ios_logging_global` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_prefix_lists` | `ios_prefix_lists` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_snmp_server` | `ios_snmp_server` | 4 | gathered, merged, overridden, deleted, parsed, rendered |
| `cisshgo_ios_static_routes` | `ios_static_routes` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_ospfv2` | `ios_ospfv2` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_ospfv3` | `ios_ospfv3` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_ospf_interfaces` | `ios_ospf_interfaces` | 5 | gathered, merged, replaced, overridden, deleted, parsed, rendered |
| `cisshgo_ios_bgp_global` | `ios_bgp_global` | 5 | gathered, merged, replaced, deleted, purged, parsed, rendered |

Run from `ansible_collections/cisco/ios/extensions/`:

```bash
export ANSIBLE_COLLECTIONS_PATH="$(pwd)/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export CISSHGO_BIN_PATH=/path/to/cisshgo   # or CISSHGO_REPO_PATH for go build
molecule test -s cisshgo_ios_hostname
molecule test -s cisshgo_ios_interfaces
molecule test -s cisshgo_ios_l2_interfaces
molecule test -s cisshgo_ios_l3_interfaces
molecule test -s cisshgo_ios_acl_interfaces
molecule test -s cisshgo_ios_ntp_global
molecule test -s cisshgo_ios_lldp_global
molecule test -s cisshgo_ios_logging_global
molecule test -s cisshgo_ios_prefix_lists
molecule test -s cisshgo_ios_snmp_server
molecule test -s cisshgo_ios_static_routes
molecule test -s cisshgo_ios_ospfv2
molecule test -s cisshgo_ios_ospfv3
molecule test -s cisshgo_ios_ospf_interfaces
molecule test -s cisshgo_ios_bgp_global
```

See [MULTI_MODULE_CISSHGO.md](MULTI_MODULE_CISSHGO.md) for port conventions, `ANSIBLE_COLLECTIONS_PATH`, and multi-scenario notes.

## CML Lab Devices

Two CML devices are available for deriving ground-truth emit order:

| Device | Type | Inventory file | Port | Use for |
|--------|------|---------------|------|---------|
| IOSv (L3 router) | `cisco.iosv` | `inventory.ini` | 2033 | Tier 1 L3 modules (ospf, bgp, static_routes, prefix_lists, etc.) |
| IOSvL2 (L2 switch) | `cisco.iosvl2` | `inventory for ios l2.ini` | 2193 | **Tier 2 L2 modules** (vlans, lag_interfaces, lacp_interfaces, l2_interfaces, etc.) |

Both on CML host `54.190.208.146`, user `admin`.

**Important for Tier 2 modules**: Previously classified as "source-derived (no CML support)",
the following modules CAN now use the IOSvL2 device for CML-derived emit order:
- `ios_vlans`, `ios_lag_interfaces`, `ios_lacp_interfaces`
- `ios_evpn_evi`, `ios_evpn_global` (if supported on IOSvL2)
- `ios_hsrp_interfaces` (if supported on IOSvL2)
- `ios_vxlan_vtep` (if supported on IOSvL2)

Use the capture playbook with `-i "inventory for ios l2.ini"` for these modules.

## Skill bundle (helpers + docs)

Everything for this workflow is co-located under the Cursor skill:

```
.cursor/skills/cisco-ios-molecule-cisshgo-integration/
├── README.md
├── SKILL.md
├── docs/
│   ├── README.md
│   ├── User Guide.md
│   ├── Molecule Cisshgo multi-module.md   # verbatim copy
│   ├── Molecule + Cisshgo.md               # verbatim copy (long)
│   └── Cisshgo scenario.md                 # verbatim copy (long)
└── helpers/
    ├── capture_cml.yml
    ├── validate_transcript_map.py
    └── run_scenario.sh
```

See [SKILL.md](../../../../../.cursor/skills/cisco-ios-molecule-cisshgo-integration/SKILL.md) (**Recommended workflow**) for commands and the full step-by-step.
