# -*- coding: utf-8 -*-

# (c) 2026, Divesh (@vishnusingh2700)
# GNU General Public License v3.0+

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
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
  applet_name:
    description: Name of the EEM applet to be created on the switch.
    type: str
    default: MIGRATE_MGMT
  new_ip:
    description: The new Management IP address for the target VLAN.
    type: str
    required: true
  mgmt_gateway:
    description: The default gateway for the new management network.
    type: str
    required: true
  vlan_id:
    description: The ID of the new Management VLAN.
    type: int
    default: 99
  trunks:
    description: List of trunk interfaces to be updated.
    type: list
    elements: str
    required: true
  native_vlan:
    description: The new native VLAN ID (Blackhole VLAN).
    type: int
    default: 999
  is_root:
    description: Set to true if the switch is the Root Bridge/Gateway.
    type: bool
    default: false
  mgmt_iface:
    description: Physical interface for management if is_root is true.
    type: str
'''

EXAMPLES = r'''
- name: Migrate Management to VLAN 99
  cisco.ios.ios_atomic_vlan_migration:
    new_ip: "192.168.100.10"
    mgmt_gateway: "192.168.100.1"
    vlan_id: 99
    trunks: ["GigabitEthernet0/0", "GigabitEthernet0/1"]
    native_vlan: 999
'''

RETURN = r'''
msg:
  description: The status of the EEM applet creation.
  returned: always
  type: str
  sample: "EEM Applet MIGRATE_MGMT created successfully"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import load_config

def generate_eem_commands(params):
    """EEM Script generate karne ka logic (Bulletproof Version)"""
    applet_name = params['applet_name']
    new_ip = params['new_ip']
    mgmt_gateway = params['mgmt_gateway']
    vlan_id = params['vlan_id']
    mgmt_iface = params['mgmt_iface']
    is_root = params['is_root']
    trunks = ",".join(params['trunks'])
    native_vlan = params['native_vlan']

    commands = [
        f"no event manager applet {applet_name}",
        f"event manager applet {applet_name}",
        " event timer countdown time 3600",
        ' action 1.0 cli command "enable"',
        ' action 1.1 cli command "conf t"',
        ' action 2.0 cli command "interface Vlan1"',
        ' action 2.1 cli command "no ip address dhcp"',
        ' action 2.2 cli command "no ip address"',
        ' action 2.3 cli command "shutdown"',
        f' action 3.0 cli command "interface Vlan{vlan_id}"',
        f' action 3.1 cli command "ip address {new_ip} 255.255.255.0"',
        ' action 3.2 cli command "no shutdown"',
        ' action 3.3 cli command "exit"',
        f' action 3.4 cli command "ip default-gateway {mgmt_gateway}"'
    ]

    if is_root and mgmt_iface:
        commands.extend([
            f' action 4.0 cli command "interface {mgmt_iface}"',
            ' action 4.1 cli command "switchport mode access"',
            f' action 4.2 cli command "switchport access vlan {vlan_id}"',
            ' action 4.3 cli command "no switchport port-security"',
            ' action 4.4 cli command "no spanning-tree bpduguard"'
        ])
    else:
        commands.extend([
            f' action 4.0 cli command "interface Vlan{vlan_id}"',
            ' action 4.1 cli command "no shutdown"',
            ' action 4.2 cli command "exit"'
        ])

    commands.extend([
        f' action 4.6 cli command "interface range {trunks}"',
        f' action 4.7 cli command "switchport trunk allowed vlan add {vlan_id},999"',
        ' action 4.8 cli command "switchport trunk allowed vlan remove 1"',
        f' action 4.9 cli command "switchport trunk native vlan {native_vlan}"',
        ' action 5.0 cli command "exit"',
        f' action 5.1 cli command "no event manager applet {applet_name}"',
        ' action 5.2 cli command "do write memory"',
        ' action 6.0 cli command "end"'
    ])
    
    return commands

def main():
    module_args = dict(
        applet_name=dict(type='str', default='MIGRATE_MGMT'),
        new_ip=dict(type='str', required=True),
        vlan_id=dict(type='int', default=99),
        mgmt_iface=dict(type='str', required=False),
        mgmt_gateway=dict(type='str', required=True),
        is_root=dict(type='bool', default=False),
        trunks=dict(type='list', required=True),
        native_vlan=dict(type='int', default=999)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    commands = generate_eem_commands(module.params)

    if not module.check_mode:
        load_config(module, commands)
        module.exit_json(changed=True, msg=f"EEM Applet {module.params['applet_name']} created successfully")
    else:
        module.exit_json(changed=False, msg="Check mode: Commands generated but not pushed")

if __name__ == '__main__':
    main()
