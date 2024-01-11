#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_evpn_evi
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_evpn_evi
short_description: Resource module to configure L2VPN EVPN EVI.
description: This module provides declarative management of L2VPN EVPN EVI on Cisco IOS network
  devices.
version_added: 5.3.0
author: Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
notes:
  - Tested against Cisco IOS-XE device with Version 17.13.01 on Cat9k on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of L2VPN Ethernet Virtual Private Network (EVPN) EVI configuration
    type: list
    elements: dict
    suboptions:
      evi:
        description: EVPN instance value
        type: int
        required: True
      default_gateway:
        description: Default Gateway parameters
        type: dict
        suboptions:
          advertise:
            description: Advertise Default Gateway MAC/IP routes
            type: dict
            suboptions:
              enable:
                description: Enable advertisement of Default Gateway MAC/IP routes
                type: bool
              disable:
                description: Disable advertisement of Default Gateway MAC/IP routes
                type: bool
      ip:
        description: IP parameters
        type: dict
        suboptions:
          local_learning:
            description: IP local learning
            type: dict
            suboptions:
              enable:
                description: Enable IP local learning
                type: bool
              disable:
                description: Disable IP local learning
                type: bool
      encapsulation:
        description: EVPN encapsulation type
        type: str
        choices:
        - vxlan
        default: vxlan
      replication_type:
        description: Method for replicating BUM traffic
        type: str
        choices:
        - ingress
        - static
      route_distinguisher:
        description: EVPN Route Distinguisher
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

# Using state merged

# Before state:
# -------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type ingress

# - name: Merge provided configuration with device configuration
#   cisco.ios.ios_evpn_evi:
#     config:
#       - evi: 101
#         replication_type: ingress
#         route_distinguisher: '1:1'
#         default_gateway:
#           advertise:
#             enable: False
#         ip:
#           local_learning:
#             enable: True
#
#       - evi: 202
#         replication_type: static
#         default_gateway:
#           advertise:
#             enable: True
#         ip:
#           local_learning:
#             disable: True
#     state: merged

# Commands Fired:
# ---------------
# "commands": [
#     "l2vpn evpn instance 101 vlan-based",
#     "ip local-learning enable",
#     "replication-type ingress",
#     "rd 1:1",
#     "l2vpn evpn instance 202 vlan-based",
#     "default-gateway advertise enable",
#     "ip local-learning disable",
#     "replication-type static"
#     ],

# After state:
# ------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  rd 1:1
#  replication-type ingress
#  ip local-learning enable
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  ip local-learning disable
#  default-gateway advertise enable


# Using state replaced

# Before state:
# -------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  rd 1:1
#  replication-type ingress
#  ip local-learning enable
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  ip local-learning disable
#  default-gateway advertise enable

# - name: Replaces the device configuration with the provided configuration
#   cisco.ios.ios_evpn_evi:
#     config:
#       - evi: 101
#         replication_type: ingress
#         default_gateway:
#           advertise:
#             enable: True
#       - evi: 202
#         replication_type: ingress
#     state: replaced

# Commands Fired:
# ---------------
# "commands": [
#     "l2vpn evpn instance 101 vlan-based",
#     "default-gateway advertise enable",
#     "no ip local-learning enable",
#     "no rd 1:1",
#     "l2vpn evpn instance 202 vlan-based",
#     "no default-gateway advertise enable",
#     "no ip local-learning disable",
#     "replication-type ingress"
#     ],

# After state:
# ------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type ingress
#  default-gateway advertise enable
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type ingress

# Using state overridden

# Before state:
# -------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type ingress
#  default-gateway advertise enable
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type ingress

# - name: Override the device configuration with provided configuration
#   cisco.ios.ios_evpn_evi:
#     config:
#       - evi: 101
#         replication_type: ingress
#         default_gateway:
#           advertise:
#             enable: True
#       - evi: 202
#         replication_type: static
#         default_gateway:
#           advertise:
#             enable: True
#     state: overridden

# Commands Fired:
# ---------------
# "commands": [
#     "no l2vpn evpn instance 102 vlan-based",
#     "no l2vpn evpn instance 201 vlan-based",
#     "l2vpn evpn instance 202 vlan-based",
#     "default-gateway advertise enable",
#     "replication-type static"
#     ],

# After state:
# ------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type ingress
#  default-gateway advertise enable
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  default-gateway advertise enable


# Using state Deleted

# Before state:
# -------------
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type ingress
#  default-gateway advertise enable
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  default-gateway advertise enable

# - name: "Delete the given EVI(s)"
#   cisco.ios.ios_evpn_evi:
#     config:
#       - evi: 101
#     state: deleted

# Commands Fired:
# ---------------
# "commands": [
#       "no l2vpn evpn instance 101 vlan-based"
#       ],

# After state:
# -------------
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  default-gateway advertise enable

# Using state Deleted without any config passed

# Before state:
# -------------
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type static
#  default-gateway advertise enable

# - name: "Delete ALL EVIs"
#   cisco.ios.ios_evpn_evi:
#     state: deleted

# Commands Fired:
# ---------------
# "commands": [
#     "no l2vpn evpn instance 102 vlan-based",
#     "no l2vpn evpn instance 202 vlan-based"
#     ],

# After state:
# -------------
# !

# Using gathered

# Before state:
# -------------
#
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !
# l2vpn evpn instance 201 vlan-based
#  encapsulation vxlan
#  replication-type static
# !
# l2vpn evpn instance 202 vlan-based
#  encapsulation vxlan
#  replication-type ingress

# - name: Gather facts for evpn_evi
#   cisco.ios.ios_evpn_evi:
#     config:
#     state: gathered

# Task Output:
# ------------
#
# gathered:
#   - evi: 101
#     encapsulation: vxlan
#     replication_type: static
#   - evi: 102
#     encapsulation: vxlan
#     replication_type: ingress
#   - evi: 201
#     encapsulation: vxlan
#     replication_type: static
#   - evi: 202
#     encapsulation: vxlan
#     replication_type: ingress

# Using Rendered

# - name: Rendered the provided configuration with the existing running configuration
#   cisco.ios.ios_evpn_evi:
#     config:
#       - evi: 101
#         replication_type: ingress
#         default_gateway:
#           advertise:
#             enable: True
#       - evi: 202
#         replication_type: ingress
#     state: rendered

# Task Output:
# ------------
#
# rendered:
# - l2vpn evpn instance 101 vlan-based
# - default-gateway advertise enable
# - replication-type ingress
# - l2vpn evpn instance 202 vlan-based
# - replication-type ingress


# Using parsed

# File: parsed.cfg
# ----------------
#
# l2vpn evpn instance 101 vlan-based
#  encapsulation vxlan
#  replication-type ingress
#  default-gateway advertise enable
# !
# l2vpn evpn instance 102 vlan-based
#  encapsulation vxlan
#  replication-type ingress
# !

# - name: Parse the commands for provided configuration
#   cisco.ios.ios_evpn_evi:
#     running_config: "{{ lookup('file', 'parsed.cfg') }}"
#     state: parsed

# Task Output:
# ------------
#
# parsed:
#   - evi: 101
#     encapsulation: vxlan
#     replication_type: ingress
#     default_gateway:
#       advertise:
#         enable: true
#   - evi: 102
#     encapsulation: vxlan
#     replication_type: ingress
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
    - "l2vpn evpn instance 101 vlan-based"
    - "encapsulation vxlan"
    - "replication-type ingress"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.evpn_evi.evpn_evi import (
    Evpn_eviArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.evpn_evi.evpn_evi import (
    Evpn_evi,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Evpn_eviArgs.argument_spec,
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

    result = Evpn_evi(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
