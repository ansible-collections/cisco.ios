#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_l2_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_l2_interfaces
short_description: Resource module to configure L2 interfaces.
description:
  This module provides declarative management of Layer-2 interface on Cisco
  IOS devices.
version_added: 1.0.0
author:
  - Sagar Paul (@KB-petByte)
  - Sumit Jaiswal (@justjais)
  - Nikhil Bhasin (@nickbhasin)
notes:
  - Tested against Cisco IOSv Version 15.2 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary of Layer-2 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface excluding any logical unit
            number, i.e GigabitEthernet0/1.
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
      private_vlan:
        description:
          - Set the private VLAN configuration.
        type: dict
        suboptions:
          association:
            description:
              - Set the private VLAN association.
            type: bool
          host_association:
            description:
              - Set the private VLAN host association.
            type: bool
          mapping:
            description:
              - Set the private VLAN promiscuous mapping.
            type: bool
          host:
            description:
              - Set the private VLAN host association.
            type: bool
          primary_range:
            description:
              - Primary extended/normal range VLAN ID of the private VLAN promiscuous port mapping.
            type: int
          secondary_range:
            description:
              - Secondary extended/normal range VLAN ID of the private VLAN promiscuous port mapping.
            type: int
          add:
            description:
              - Add a VLAN to private VLAN list.
            type: bool
          remove:
            description:
              - Remove a VLAN from private VLAN list.
            type: bool
          secondary_vlan_id:
            description:
              - Secondary VLAN IDs of the private VLAN promiscuous port mapping.
            type: str
      app_interface:
        description:
          - Enabling port for Application Hosting (switchport app-interface)
        type: bool
      nonegotiate:
        description:
          - Device will not engage in negotiation protocol on this interface (switchport nonegotiate)
        type: bool
      vepa:
        description:
          - Reflective relay configuration (switchport vepa enabled)
        type: bool
      host:
        description:
          - Set port host (switchport host)
        type: bool
      protected:
        description:
          - Configure an interface to be a protected port (switchport protected)
        type: bool
      block_options:
        description:
          - Disable forwarding of unknown uni/multi cast addresses.
        type: dict
        suboptions:
          multicast:
            description:
              - Block unknown multicast addresses
            type: bool
          unicast:
            description:
              - Block unknown unicast addresses
            type: bool
      spanning_tree:
        description:
          - Spanning tree options
        type: dict
        suboptions:
          bpdufilter:
            description: Don't send or receive BPDUs on this interface
            type: dict
            suboptions:
              enabled:
                description:
                  - Enable BPDU filtering for this interface
                type: bool
              disabled:
                description:
                  - Disable BPDU filtering for this interface
                type: bool
          bpduguard:
            description: Don't accept BPDUs on this interface
            type: dict
            suboptions:
              enabled:
                description:
                  - Enable BPDU guard for this interface
                type: bool
              disabled:
                description:
                  - Disable BPDU guard for this interface
                type: bool
          cost:
            description: Change an interface's spanning tree port path cost
            type: int
          guard:
            description: Change an interface's spanning tree guard mode
            type: dict
            suboptions:
              loop:
                description:
                  - Set guard mode to loop guard on interface
                type: bool
              none:
                description:
                  - Set guard mode to none
                type: bool
              root:
                description:
                  - Set guard mode to root guard on interface
                type: bool
          link_type:
            description: Specify a link type for spanning tree protocol use
            type: dict
            suboptions:
              point_to_point:
                description:
                  - Consider the interface as point-to-point
                type: bool
              shared:
                description:
                  - Consider the interface as shared
                type: bool
          mst:
            description: Multiple spanning tree
            type: dict
            suboptions:
              instance_range:
                description:
                  - MST instance list, example 0,2-4,6,8-12
                type: str
              cost:
                description:
                  - <1-200000000>  Change the interface spanning tree path cost for an instance
                type: str
              port_priority:
                description:
                  - Change the spanning tree port priority for an instance
                type: int
          port_priority:
            description: Change an interface's spanning tree port priority
            type: int
          portfast:
            description: Enable an interface to move directly to forwarding on link up
            type: dict
            suboptions:
              disabled:
                description:
                  - Disable portfast for this interface
                type: bool
              trunk:
                description:
                  - Enable portfast on the interface even in trunk mode
                type: bool
          rootguard:
            description: Enable root guard protection on the interface
            type: bool
          vlan:
            description: VLAN Switch Spanning Tree
            type: dict
            suboptions:
              vlan_range:
                description:
                  - MST instance list, example 1,3-5,7,9-11
                type: str
              cost:
                description:
                  - <1-200000000>  Change the interface spanning tree path cost for an instance
                type: str
              port_priority:
                description:
                  - Change the spanning tree port priority for an instance
                type: int
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
      - The state I(gathered) will fetch the running configuration from device and
        transform it into structured data in the format as per the resource module
        argspec and the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of
        C(running_config) option should be the same format as the output of
        command I(show running-config | include ip route|ipv6 route) executed on device.
        For state I(parsed) active connection to remote host is not required.
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

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
# commands:
# - interface GigabitEthernet0/1
# - switchport access vlan 10
# - switchport voice vlan 40
# - switchport mode access
# - interface GigabitEthernet0/2
# - switchport mode trunk
# - switchport trunk encapsulation dot1q
# - switchport trunk native vlan 20
# - switchport trunk allowed vlan 10-20,40
# - switchport trunk pruning vlan 10,20
# after:
# - access:
#     vlan: 10
#   mode: access
#   name: GigabitEthernet0/1
#   voice:
#     vlan: 40
# - mode: trunk
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 10-20
#     - '40'
#     encapsulation: dot1q
#     native_vlan: 20
#     pruning_vlans:
#     - '10'
#     - '20'

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

- name: Replaces device configuration with provided configuration
  cisco.ios.ios_l2_interfaces:
    config:
      - name: GigabitEthernet0/2
        trunk:
          allowed_vlans: 20-25,40
          native_vlan: 20
          pruning_vlans: 10
          encapsulation: isl
    state: replaced

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
# commands:
# - interface GigabitEthernet0/2
# - no switchport access vlan
# - switchport trunk encapsulation isl
# - switchport trunk native vlan 20
# - switchport trunk allowed vlan 20-25,40
# - switchport trunk pruning vlan 10
# after:
# - access:
#     vlan: 20
#   name: GigabitEthernet0/1
# - name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-25
#     - '40'
#     encapsulation: isl
#     native_vlan: 20
#     pruning_vlans:
#     - '10'

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

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet0/1
#   trunk:
#     encapsulation: dot1q
#     native_vlan: 20
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     encapsulation: dot1q
#     native_vlan: 20
# commands:
# - interface GigabitEthernet0/1
# - no switchport trunk encapsulation
# - no switchport trunk native vlan
# - interface GigabitEthernet0/2
# - switchport voice vlan 40
# - no switchport trunk encapsulation
# - no switchport trunk native vlan
# after:
# - name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   voice:
#     vlan: 40

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

# Using deleted

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

# Task Output
# -----------
#
# before:
# - access:
#     vlan: 20
#   name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-40
#     - '60'
#     - '80'
#     encapsulation: dot1q
#     native_vlan: 10
#     pruning_vlans:
#     - '10'
# commands:
# - interface GigabitEthernet0/1
# - no switchport access vlan
# after:
# - name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-40
#     - '60'
#     - '80'
#     encapsulation: dot1q
#     native_vlan: 10
#     pruning_vlans:
#     - '10'

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

# Using deleted without config - delete all configuration

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

# Task Output
# -----------
#
# before:
# - access:
#     vlan: 20
#   name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-40
#     - '60'
#     - '80'
#     encapsulation: dot1q
#     native_vlan: 10
#     pruning_vlans:
#     - '10'
# commands:
# - interface GigabitEthernet0/1
# - no switchport access vlan
# - interface GigabitEthernet0/2
# - no switchport access vlan
# - no switchport trunk encapsulation
# - no switchport trunk native vlan
# - no switchport trunk allowed vlan
# - no switchport trunk pruning vlan
# after:
# - name: GigabitEthernet0/1
# - name: GigabitEthernet0/2

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

# Using gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
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

- name: Gather facts for l2 interfaces
  cisco.ios.ios_l2_interfaces:
    config:
    state: gathered

# Task Output
# -----------
#
# gathered:
# - access:
#     vlan: 20
#   name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-40
#     - '60'
#     - '80'
#     encapsulation: dot1q
#     native_vlan: 10
#     pruning_vlans:
#     - '10'

# Using rendered

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

# Task Output
# -----------
#
# rendered:
# - interface GigabitEthernet0/1
# - switchport access vlan 30
# - interface GigabitEthernet0/2
# - switchport trunk encapsulation dot1q
# - switchport trunk native vlan 20
# - switchport trunk allowed vlan 10-20,40
# - switchport trunk pruning vlan 10,20

# Using Parsed

# File: parsed.cfg
# ----------------
#
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

- name: Parse the commands for provided configuration
  cisco.ios.ios_l2_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
# - access:
#     vlan: 20
#   name: GigabitEthernet0/1
# - access:
#     vlan: 20
#   name: GigabitEthernet0/2
#   trunk:
#     allowed_vlans:
#     - 20-40
#     - '60'
#     - '80'
#     encapsulation: dot1q
#     native_vlan: 10
#     pruning_vlans:
#     - '10'
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
    - interface GigabitEthernet0/2
    - switchport trunk allowed vlan 15-20,40
    - switchport trunk encapsulation dot1q
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet0/1
    - switchport access vlan 30
    - switchport trunk encapsulation dot1q
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

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l2_interfaces.l2_interfaces import (
    L2_interfaces,
)


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
