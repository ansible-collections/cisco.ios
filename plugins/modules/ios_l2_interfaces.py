#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_l2_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_l2_interfaces
short_description: Resource Module to configure L2 interfaces.
description: This module provides declarative management of Layer-2 interface on Cisco
  IOS devices.
version_added: 1.0.0
author:
  - Sagar Paul (@KB-petByte)
  - Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSv Version 15.2 on VIRL.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of Layer-2 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.
        type: str
        required: true
      access:
        description:
        - Switchport mode access command to configure the interface as a layer 2 access.
        type: dict
        suboptions:
          vlan:
            description:
            - Configure given VLAN in access port. It's used as the access VLAN ID.
            type: int
          vlan_name:
            description:
            - Set VLAN when interface is in access mode.
            type: str
      voice:
        description:
        - Switchport mode voice command to configure the interface with a voice vlan.
        type: dict
        suboptions:
          vlan:
            description:
            - Configure given voice VLAN on access port. It's used as the voice VLAN
              ID.
            type: int
          vlan_tag:
            description:
            - Set VLAN Tag.
              dot1p (Priority tagged on PVID)
              none (Don't tell telephone about voice vlan)
              untagged (Untagged on PVID)
            choices:
            - dot1p
            - none
            - untagged
            type: str
          vlan_name:
            description:
            - Set VLAN when interface is in access mode.
            type: str
      trunk:
        description:
        - Switchport mode trunk command to configure the interface as a Layer 2 trunk.
          Note The encapsulation is always set to dot1q.
        type: dict
        suboptions:
          allowed_vlans:
            description:
            - List of allowed VLANs in a given trunk port. These are the only VLANs
              that will be configured on the trunk.
            type: list
            elements: str
          native_vlan:
            description:
            - Native VLAN to be configured in trunk port. It's used as the trunk native
              VLAN ID.
            type: int
          encapsulation:
            description:
            - Trunking encapsulation when interface is in trunking mode.
            choices:
            - dot1q
            - isl
            - negotiate
            type: str
          pruning_vlans:
            description:
            - Pruning VLAN to be configured in trunk port. It's used as the trunk
              pruning VLAN ID.
            type: list
            elements: str
      mode:
        description:
        - Mode in which interface needs to be configured.
        - An interface whose trunk encapsulation is "Auto" can not be configured to
          "trunk" mode.
        type: str
        choices:
        - access
        - trunk
        - dot1q_tunnel
        - dynamic
        - dynamic_auto
        - dynamic_desirable
        - private_vlan_host
        - private_vlan_promiscuous
        - private_vlan_trunk
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - rendered
    - gathered
    - parsed
    default: merged
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  media-type rj45
#  negotiation auto

- name: Merge provided configuration with device configuration
  cisco.ios.ios_l2_interfaces:
    config:
    - name: GigabitEthernet0/1
      mode: access
      access:
        vlan: 10
      voice:
        vlan: 40
    - name: GigabitEthernet0/2
      mode: trunk
      trunk:
        allowed_vlans: 10-20,40
        native_vlan: 20
        pruning_vlans: 10,20
        encapsulation: dot1q
    state: merged

# After state:
# ------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport access vlan 10
#  switchport voice vlan 40
#  switchport mode access
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport trunk allowed vlan 10-20,40
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 20
#  switchport trunk pruning vlan 10,20
#  switchport mode trunk
#  media-type rj45
#  negotiation auto

# Using replaced

# Before state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport access vlan 20
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  media-type rj45
#  negotiation auto

- name: Replaces device configuration of listed l2 interfaces with provided configuration
  cisco.ios.ios_l2_interfaces:
    config:
    - name: GigabitEthernet0/2
      trunk:
        allowed_vlans: 20-25,40
        native_vlan: 20
        pruning_vlans: 10
        encapsulation: isl
    state: replaced

# After state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport access vlan 20
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport trunk allowed vlan 20-25,40
#  switchport trunk encapsulation isl
#  switchport trunk native vlan 20
#  switchport trunk pruning vlan 10
#  media-type rj45
#  negotiation auto

# Using overridden

# Before state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 20
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 20
#  media-type rj45
#  negotiation auto

- name: Override device configuration of all l2 interfaces with provided configuration
  cisco.ios.ios_l2_interfaces:
    config:
    - name: GigabitEthernet0/2
      access:
        vlan: 20
      voice:
        vlan: 40
    state: overridden

# After state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  switchport voice vlan 40
#  media-type rj45
#  negotiation auto

# Using Deleted

# Before state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport access vlan 20
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  switchport trunk allowed vlan 20-40,60,80
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 10
#  switchport trunk pruning vlan 10
#  media-type rj45
#  negotiation auto

- name: Delete IOS L2 interfaces as in given arguments
  cisco.ios.ios_l2_interfaces:
    config:
    - name: GigabitEthernet0/1
    state: deleted

# After state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  switchport trunk allowed vlan 20-40,60,80
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 10
#  switchport trunk pruning vlan 10
#  media-type rj45
#  negotiation auto


# Using Deleted without any config passed
#"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

# Before state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  switchport access vlan 20
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  switchport access vlan 20
#  switchport trunk allowed vlan 20-40,60,80
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 10
#  switchport trunk pruning vlan 10
#  media-type rj45
#  negotiation auto

- name: Delete IOS L2 interfaces as in given arguments
  cisco.ios.ios_l2_interfaces:
    state: deleted

# After state:
# -------------
#
# viosl2#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  negotiation auto
# interface GigabitEthernet0/2
#  description This is test
#  media-type rj45
#  negotiation auto

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  switchport access vlan 10
# interface GigabitEthernet0/2
#  switchport trunk allowed vlan 10-20,40
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 10
#  switchport trunk pruning vlan 10,20
#  switchport mode trunk

- name: Gather listed l2 interfaces with provided configurations
  cisco.ios.ios_l2_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "name": "GigabitEthernet0/0"
#         },
#         {
#             "access": {
#                 "vlan": 10
#             },
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "mode": "trunk",
#             "name": "GigabitEthernet0/2",
#             "trunk": {
#                 "allowed_vlans": [
#                     "10-20",
#                     "40"
#                 ],
#                 "encapsulation": "dot1q",
#                 "native_vlan": 10,
#                 "pruning_vlans": [
#                     "10",
#                     "20"
#                 ]
#             }
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  switchport access vlan 10
# interface GigabitEthernet0/2
#  switchport trunk allowed vlan 10-20,40
#  switchport trunk encapsulation dot1q
#  switchport trunk native vlan 10
#  switchport trunk pruning vlan 10,20
#  switchport mode trunk

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_l2_interfaces:
    config:
    - name: GigabitEthernet0/1
      access:
        vlan: 30
    - name: GigabitEthernet0/2
      trunk:
        allowed_vlans: 10-20,40
        native_vlan: 20
        pruning_vlans: 10,20
        encapsulation: dot1q
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "switchport access vlan 30",
#         "interface GigabitEthernet0/2",
#         "switchport trunk encapsulation dot1q",
#         "switchport trunk native vlan 20",
#         "switchport trunk allowed vlan 10-20,40",
#         "switchport trunk pruning vlan 10,20"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# switchport mode access
# switchport access vlan 30
# interface GigabitEthernet0/2
# switchport trunk allowed vlan 15-20,40
# switchport trunk encapsulation dot1q
# switchport trunk native vlan 20
# switchport trunk pruning vlan 10,20

- name: Parse the commands for provided configuration
  cisco.ios.ios_l2_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "access": {
#                 "vlan": 30
#             },
#             "mode": "access",
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "name": "GigabitEthernet0/2",
#             "trunk": {
#                 "allowed_vlans": [
#                     "15-20",
#                     "40"
#                 ],
#                 "encapsulation": "dot1q",
#                 "native_vlan": 20,
#                 "pruning_vlans": [
#                     "10",
#                     "20"
#                 ]
#             }
#         }
#     ]
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

import debugpy

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l2_interfaces.l2_interfaces import (
    L2_interfaces,
)


debugpy.listen(3000)
debugpy.wait_for_client()


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L2_interfacesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
