#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2026, Divesh (@vishnusingh2700)
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: ios_atomic_vlan_migration
short_description: Atomic migration of Management IP and Trunk Cleanup on Cisco IOS.
description:
  - This module automates the migration of a management IP from VLAN 1 to a target VLAN.
  - It uses Cisco EEM (Event Manager) to ensure the migration is atomic, preventing lockouts.
  - It specifically handles the removal of VLAN 1 from trunk allowed lists and sets a new native VLAN.
version_added: "1.0.0"
author:
  - Divesh (@vishnusingh2700)
options:
  config:
    description: The configuration objects for the network resource.
    type: dict
    suboptions:
      applet_name:
        description: Name of the EEM applet to be created.
        type: str
        default: MIGRATE_MGMT
      new_ip:
        description: The new Management IP address for the target VLAN.
        type: str
      mgmt_gateway:
        description: The default gateway for the new management network.
        type: str
      vlan_id:
        description: The ID of the new Management VLAN.
        type: int
        default: 99
      vrf:
        description: VRF name for management.
        type: str
        default: MGMT
      trunks:
        description: List of trunk interfaces to be updated.
        type: list
        elements: str
      native_vlan:
        description: The new native VLAN ID (Blackhole VLAN).
        type: int
        default: 999
      mgmt_iface:
        description: Physical interface for management if needed.
        type: str
  state:
    description: The state of the configuration.
    type: str
    choices: [merged, replaced, overridden, deleted, gathered, rendered, parsed]
    default: merged
"""

EXAMPLES = r"""
- name: Migrate Management to VLAN 99 (Merged)
  cisco.ios.ios_atomic_vlan_migration:
    config:
      new_ip: "192.168.100.10"
      mgmt_gateway: "192.168.100.1"
      vlan_id: 99
      trunks: ["GigabitEthernet0/0", "GigabitEthernet0/1"]
    state: merged

- name: Gather current EEM status
  cisco.ios.ios_atomic_vlan_migration:
    state: gathered

- name: Render commands without pushing to switch
  cisco.ios.ios_atomic_vlan_migration:
    config:
      new_ip: "192.168.100.10"
      mgmt_gateway: "192.168.100.1"
      trunks: ["Gi0/1"]
    state: rendered
"""

RETURN = r"""
gathered:
  description: The current configuration of the EEM applet.
  returned: when state is gathered
  type: dict
  sample: {"raw_config": "event manager applet MIGRATE_MGMT...", "status": "Applet found"}
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)


def generate_eem_commands(params):
    """EEM Script logic - Takes data from config dictionary"""
    if not params:
        return []

    applet_name = params.get("applet_name", "MIGRATE_MGMT")
    new_ip = params.get("new_ip")
    mgmt_gateway = params.get("mgmt_gateway")
    vlan_id = params.get("vlan_id", 99)
    vrf_name = params.get("vrf", "MGMT")
    mgmt_iface = params.get("mgmt_iface")

    trunk_list = params.get("trunks", [])
    trunks = ", ".join(trunk_list) if isinstance(trunk_list, list) else trunk_list

    native_vlan = params.get("native_vlan", 999)

    commands = [
        "no event manager applet {0}".format(applet_name),
        "event manager applet {0}".format(applet_name),
        " event none",
        ' action 1.0 cli command "enable"',
        ' action 1.1 cli command "conf t"',
        ' action 1.2 cli command "ip vrf {0}"'.format(vrf_name),
        ' action 1.3 cli command "rd 1:1"',
        ' action 1.4 cli command "exit"',
        ' action 2.0 cli command "interface Vlan1"',
        ' action 2.1 cli command "no ip address dhcp"',
        ' action 2.2 cli command "no ip address"',
        ' action 2.3 cli command "shutdown"',
        ' action 3.0 cli command "interface Vlan{0}"'.format(vlan_id),
        ' action 3.1 cli command "ip vrf forwarding {0}"'.format(vrf_name),
        ' action 3.2 cli command "ip address {0} 255.255.255.0"'.format(new_ip),
        ' action 3.3 cli command "no shutdown"',
        ' action 3.4 cli command "exit"',
        ' action 3.5 cli command "ip route vrf {0} 0.0.0.0 0.0.0.0 {1}"'.format(
            vrf_name, mgmt_gateway
        ),
    ]

    if mgmt_iface:
        commands.extend(
            [
                ' action 4.0 cli command "interface {0}"'.format(mgmt_iface),
                ' action 4.1 cli command "switchport mode access"',
                ' action 4.2 cli command "switchport access vlan {0}"'.format(vlan_id),
            ]
        )

    commands.extend(
        [
            ' action 5.0 cli command "interface range {0}"'.format(trunks),
            ' action 5.1 cli command "switchport trunk allowed vlan add {0},{1}"'.format(
                vlan_id, native_vlan
            ),
            ' action 5.2 cli command "switchport trunk allowed vlan remove 1"',
            ' action 5.3 cli command "switchport trunk native vlan {0}"'.format(native_vlan),
            ' action 6.0 cli command "exit"',
            ' action 6.1 cli command "conf t"',
            ' action 6.2 cli command "no event manager applet {0}"'.format(applet_name),
            ' action 6.3 cli command "do write memory"',
            ' action 7.0 cli command "end"',
        ]
    )

    return commands


def main():
    module_args = dict(
        config=dict(
            type="dict",
            options=dict(
                applet_name=dict(type="str", default="MIGRATE_MGMT"),
                new_ip=dict(type="str", required=False),
                mgmt_gateway=dict(type="str", required=False),
                vlan_id=dict(type="int", default=99),
                vrf=dict(type="str", default="MGMT"),
                trunks=dict(type="list", elements="str", required=False),
                native_vlan=dict(type="int", default=999),
                mgmt_iface=dict(type="str", required=False),
            ),
        ),
        state=dict(
            type="str",
            choices=[
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            default="merged",
        ),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    state = module.params.get("state")
    config = module.params.get("config") or {}

    if state not in ["deleted", "gathered"]:
        missing = [k for k in ["new_ip", "mgmt_gateway", "trunks"] if not config.get(k)]
        if missing:
            module.fail_json(msg="State {0} requires: {1}".format(state, ", ".join(missing)))

    if state == "parsed":
        module.exit_json(parsed=config)

    if state == "rendered":
        cmds = generate_eem_commands(config)
        module.exit_json(rendered=cmds)

    if state == "gathered":
        current_config = get_config(module, flags="| section event manager")
        gathered_data = {
            "raw_config": current_config,
            "status": (
                "Applet found" if "event manager applet" in current_config else "No applet found"
            ),
        }
        module.exit_json(gathered=gathered_data, msg="Successfully fetched data from switch")

    if state == "deleted":
        applet = config.get("applet_name", "MIGRATE_MGMT")
        cleanup_cmds = ["no event manager applet {0}".format(applet)]
        load_config(module, cleanup_cmds)
        module.exit_json(changed=True, msg="Applet deleted", commands=cleanup_cmds)

    else:
        commands = generate_eem_commands(config)
        if not module.check_mode:
            load_config(module, commands)
            module.exit_json(
                changed=True, msg="Resource {0} applied via EEM".format(state), commands=commands
            )
        else:
            module.exit_json(changed=False, msg="Check mode: commands generated but not pushed")


if __name__ == "__main__":
    main()
