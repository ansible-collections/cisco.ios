#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vxlan_vtep
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_vxlan_vtep
short_description: Resource module to configure VXLAN VTEP interface.
description: This module provides declarative management of VXLAN VTEP interface on Cisco IOS network
  devices.
version_added: 5.3.0
author: Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
notes:
  - Tested against Cisco IOS-XE device with Version 17.13.01 on Cat9k on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of VXLAN VTEP interface option
    type: list
    elements: dict
    suboptions:
      interface:
        description:
        - VXLAN VTEP interface
        type: str
        required: true
      source_interface:
        description:
        - Source interface for the VXLAN VTEP interface
        type: str
      host_reachability_bgp:
        description:
        - Host reachability using EVPN protocol
        type: bool
      member:
        description:
        - Configure VNI member
        type: dict
        suboptions:
          vni:
            description:
            - Configure VNI information
            type: dict
            suboptions:
              l2vni:
                description:
                - Associates L2VNI with the VXLAN VTEP interface
                type: list
                elements: dict
                suboptions:
                  vni:
                    description: VNI number
                    type: int
                  replication:
                    description: Replication type for the L2VNI
                    type: dict
                    suboptions:
                      type:
                        description: Replication type
                        type: str
                        choices: ['ingress', 'static']
                      mcast_group:
                        description: Configure multicast group for VNI(s)
                        type: dict
                        suboptions:
                          ipv4:
                            description: IPv4 multicast group
                            type: str
                          ipv6:
                            description: IPv6 multicast group
                            type: str
              l3vni:
                description:
                - Associates L3VNI with the VXLAN VTEP interface
                type: list
                elements: dict
                suboptions:
                  vni:
                    description: VNI number
                    type: int
                  vrf:
                    description: VRF name of the L3VNI
                    type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^interface nve).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
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
    - rendered
    - gathered
    - parsed
    default: merged
"""

EXAMPLES = """

# Using state merged

# Before state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback1
#  host-reachability protocol bgp
#  member vni 10101 mcast-group 225.0.0.101
#  member vni 10102 ingress-replication
#  member vni 50901 vrf green
#  member vni 10201 mcast-group 225.0.0.101
#  member vni 10202 ingress-replication
#  member vni 50902 vrf blue

# - name: Merge the provided configuration with the device configuration
#   cisco.ios.ios_vxlan_vtep:
#     config:
#     - interface: nve1
#       source_interface: loopback2
#       member:
#         vni:
#           l2vni:
#             - vni: 10101
#               replication:
#                 type: ingress
#             - vni: 10201
#               replication:
#                 type: static
#                 mcast_group:
#                   ipv4: 225.0.0.101
#                   ipv6: FF0E:225::101
#           l3vni:
#             - vni: 50901
#               vrf: blue
#     state: merged

# Commands Fired:
# ---------------
#   "commands": [
#         "interface nve1",
#         "source-interface loopback2",
#         "no member vni 10101 mcast-group 225.0.0.101",
#         "member vni 10101 ingress-replication",
#         "no member vni 10201 mcast-group 225.0.0.101",
#         "member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
#         "no member vni 50901 vrf green",
#         "no member vni 50902 vrf blue",
#         "member vni 50901 vrf blue"
#   ],

# After state:
# ------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10102 ingress-replication
#  member vni 10202 ingress-replication
#  member vni 10101 ingress-replication
#  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
#  member vni 50901 vrf blue

# Using state replaced

# Before state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10102 ingress-replication
#  member vni 10202 ingress-replication
#  member vni 10101 ingress-replication
#  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
#  member vni 50901 vrf blue

# - name: Replaces the device configuration with the provided configuration
#   cisco.ios.ios_vxlan_vtep:
#     config:
#     - interface: nve1
#       source_interface: Loopback2
#       member:
#         vni:
#           l2vni:
#             - vni: 10101
#               replication:
#                 type: static
#                 mcast_group:
#                   ipv6: FF0E:225::101
#             - vni: 10201
#               replication:
#                 type: static
#                 mcast_group:
#                   ipv6: FF0E:225::102
#     state: replaced

# Commands Fired:
# ---------------
#   "commands": [
#       "interface nve1",
#       "no member vni 10101 ingress-replication",
#       "member vni 10101 mcast-group FF0E:225::101",
#       "no member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
#       "member vni 10201 mcast-group FF0E:225::102",
#       "no member vni 10102 ingress-replication",
#       "no member vni 10202 ingress-replication",
#       "no member vni 50901 vrf blue"
#   ],

# After state:
# ------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10101 mcast-group FF0E:225::101
#  member vni 10201 mcast-group FF0E:225::102

# Using state Deleted

# Before state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10101 mcast-group FF0E:225::101
#  member vni 10201 mcast-group FF0E:225::102

# - name: "Delete VXLAN VTEP interface"
#   cisco.ios.ios_vxlan_vtep:
#     config:
#     - interface: nve1
#     state: deleted

# Commands Fired:
# ---------------
#   "commands": [
#       "interface nve1",
#       "no source-interface Loopback2",
#       "no host-reachability protocol bgp",
#       "no member vni 10101 mcast-group FF0E:225::101",
#       "no member vni 10201 mcast-group FF0E:225::102"
#   ],

# After state:
# -------------
# interface nve1
#  no ip address

# Using state Deleted with member VNIs

# Before state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10101 mcast-group FF0E:225::101
#  member vni 10102 mcast-group 225.0.0.101
#  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101

# - name: "Delete VXLAN VTEP interface with member VNIs"
#   cisco.ios.ios_vxlan_vtep:
#     config:
#     - interface: nve1
#       source_interface: Loopback2
#       member:
#         vni:
#           l2vni:
#             - vni: 10101
#             - vni: 10102
#     state: deleted

# Commands Fired:
# ---------------
#   "commands": [
#       "interface nve1",
#       "no member vni 10101 mcast-group FF0E:225::101",
#       "no member vni 10102 mcast-group 225.0.0.101"
#   ],

# After state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101

# Using state Deleted with no config

# Before state:
# -------------
# interface nve1
#  no ip address
#  source-interface Loopback2
#  host-reachability protocol bgp
#  member vni 10101 mcast-group FF0E:225::101
#  member vni 10201 mcast-group FF0E:225::102

# - name: "Delete VXLAN VTEP interface with no config"
#   cisco.ios.ios_vxlan_vtep:
#     state: deleted

# Commands Fired:
# ---------------
#   "commands": [
#       "interface nve1",
#       "no source-interface Loopback2",
#       "no host-reachability protocol bgp",
#       "no member vni 10101 mcast-group FF0E:225::101",
#       "no member vni 10201 mcast-group FF0E:225::102"
#   ],

# After state:
# -------------
# interface nve1
#  no ip address
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
    - 'interface nve1'
    - 'source-interface Loopback1'
    - 'host-reachability protocol bgp'
    - 'member vni 10101 ingress-replication'
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vxlan_vtep.vxlan_vtep import (
    Vxlan_vtepArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vxlan_vtep.vxlan_vtep import (
    Vxlan_vtep,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vxlan_vtepArgs.argument_spec,
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

    result = Vxlan_vtep(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
