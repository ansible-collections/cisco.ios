#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_evpn_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_evpn_global
short_description: Resource module to configure L2VPN EVPN.
description: This module provides declarative management of L2VPN EVPN on Cisco IOS network
  devices.
version_added: 5.3.0
author: Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
notes:
  - Tested against Cisco IOS-XE device with Version 17.13.01 on Cat9k on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of L2VPN Ethernet Virtual Private Network (EVPN) configuration
    type: dict
    suboptions:
      default_gateway:
        description: Default gateway parameters
        type: dict
        suboptions:
          advertise:
            description: Advertise Default Gateway MAC/IP routes
            type: bool
      flooding_suppression:
        description: Suppress flooding of broadcast, multicast, and/or unknown unicast packets
        type: dict
        suboptions:
          address_resolution:
            description: Suppress flooding of Address Resolution and Neighbor Discovery Protocol packets
            type: dict
            suboptions:
              disable:
                description: Disable flooding suppression
                type: bool
      ip:
        description: IP parameters
        type: dict
        suboptions:
          local_learning:
            description: IP local learning
            type: dict
            suboptions:
              disable:
                description: Disable IP local learning
                type: bool
      replication_type:
        description: Method for replicating BUM traffic
        type: str
        choices:
        - ingress
        - static
      route_target:
        description: Route Target VPN Extended Communities
        type: dict
        suboptions:
          auto:
            description: Automatically set a route-target
            type: dict
            suboptions:
              vni:
                description: Set vni-based route-target
                type: bool
      router_id:
        description: EVPN router ID
        type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(sh running-config nve | section ^l2vpn evpn$).
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""


EXAMPLES = """

# Using merged

# Before state:
# -------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type static
#  router-id Loopback1
#  default-gateway advertise

- name: Merge provided configuration with device configuration
  cisco.ios.ios_evpn_global:
    config:
      replication_type: ingress
      route_target:
        auto:
          vni: true
      default_gateway:
        advertise: false
      ip:
        local_learning:
          disable: true
      flooding_suppression:
        address_resolution:
          disable: false
    state: merged

# Task Output
# -----------
#
# before:
# - replication_type: static
#   router_id: Loopback1
#   default_gateway:
#     advertise: true
# commands:
# - l2vpn evpn
#   no default-gateway advertise
#   replication-type ingress
#   route-target auto vni
#   ip local-learning disable
# after:
# - replication_type: ingress
#   router_id: Loopback1
#   route_target:
#     auto:
#       vni: true
#   ip:
#     local_learning:
#       disable: true

# After state:
# ------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type ingress
#  router-id Loopback1
#  ip local-learning disable
#  route-target auto vni

# Using replaced

# Before state:
# -------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type ingress
#  router-id Loopback1
#  ip local-learning disable
#  route-target auto vni

- name: Replaces device configuration for EVPN global with provided configuration
  cisco.ios.ios_evpn_global:
    config:
      replication_type: static
      router_id: Loopback2
      default_gateway:
        advertise: true
      flooding_suppression:
        address_resolution:
          disable: true
    state: replaced

# Task Output
# -----------
#
# before:
# - replication_type: ingress
#   router_id: Loopback1
#   route_target:
#     auto:
#       vni: true
#   ip:
#     local_learning:
#       disable: true
# commands:
# - l2vpn evpn
# - default-gateway advertise
# - flooding-suppression address-resolution disable
# - no ip local-learning disable
# - replication-type static
# - no route-target auto vni
# - router-id Loopback2
# after:
# - replication_type: ingress
#   router_id: Loopback2
#   default_gateway:
#     advertise: true
#   flooding_suppression:
#     address_resolution:
#      disable: true

# After state:
# ------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type static
#  flooding-suppression address-resolution disable
#  router-id Loopback2
#  default-gateway advertise

# Using Deleted

# Before state:
# -------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type static
#  flooding-suppression address-resolution disable
#  router-id Loopback2
#  default-gateway advertise

- name: Delete EVPN global
  cisco.ios.ios_evpn_global:
    config:
    state: deleted

# before:
# - replication_type: ingress
#   router_id: Loopback2
#   default_gateway:
#     advertise: true
#   flooding_suppression:
#     address_resolution:
#      disable: true
# commands:
# - no l2vpn evpn
# after:
#

# After state:
# -------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
#

# Using gathered

# Before state:
# -------------
#
# Leaf-01#show running-config nve | section ^l2vpn evpn$
# l2vpn evpn
#  replication-type ingress
#  router-id Loopback1
#  ip local-learning disable
#  route-target auto vni

- name: Gather facts of l2vpn evpn
  cisco.ios.ios_evpn_global:
    config:
    state: gathered

# Task Output:
# ------------
#
# gathered:
# - replication_type: ingress
#   route_target:
#     auto:
#       vni: true
#   router_id: Loopback1
#   ip:
#     local_learning:
#       disable: true

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_evpn_global:
    config:
      replication_type: static
      route_target:
        auto:
          vni: true
    state: rendered

# Task Output:
# ------------
#
# rendered:
# - l2vpn evpn
# - replication-type static
# - route-target auto vni

# Using parsed

# File: parsed.cfg
# ----------------
#
# l2vpn evpn
#  replication-type ingress
#  router-id Loopback1
#  default-gateway advertise
#  route-target auto vni

- name: Parse the provided configuration
  cisco.ios.ios_evpn_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
#
# parsed:
# - replication_type: ingress
#   route_target:
#     auto:
#       vni: true
#   router_id: Loopback1
#   default_gateway:
#     advertise: true
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), or C(deleted)
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
  returned: when I(state) is C(merged), C(replaced), C(overridden), or C(deleted)
  type: list
  sample:
    - "l2vpn evpn"
    - "replication-type ingress"
    - "router_id Loopback1"
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - l2vpn evpn
    - replication-type static
    - route-target auto vni
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.evpn_global.evpn_global import (
    Evpn_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.evpn_global.evpn_global import (
    Evpn_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Evpn_globalArgs.argument_spec,
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

    result = Evpn_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
