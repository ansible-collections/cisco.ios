#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_spanning_tree
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_spanning_tree
short_description: Resource module to configure Spanning Tree.
description:
  - This module provides declarative management of Spanning tree on Cisco IOS network devices.
version_added: 1.0.0
author: Timur Nizharadze (@tnizharadze)
notes:
  - Tested against Cisco IOS Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of spanning tree options.
    type: dict
    suboptions:
      backbonefast:
        description:
          - Use the spanning-tree backbonefast global configuration command on the switch
          - stack or on a standalone switch to enable the BackboneFast feature.
        type: bool
      bridge_assurance:
        description:
          - Enables Bridge Assurance on all network ports on the switch.
          - Bridge Assurance is enabled by default.
        type: bool
      etherchannel_guard_misconfig:
        description:
          - Enable EtherChannel guard to detect an EtherChannel misconfiguration if your
          - switch is running PVST+, Rapid PVST+, or MSTP. Enabled by default.
        type: bool
      logging:
        description:
          - Enable logging of spanning-tree changes.
        type: bool
      loopguard_default:
        description:
          - To enable loop guard as a default on all ports of a given bridge
        type: bool
      mode:
        description:
          - To switch between Per-VLAN Spanning Tree+ (PVST+), Rapid-PVST+, and Multiple
          - Spanning Tree (MST) modes.
        type: str
        choices: ["mst", "pvst", "rapid-pvst"]
      pathcost_method:
        description:
          - To set the default path-cost calculation method.
          - The long path-cost calculation method utilizes all 32 bits for path-cost
          - calculation and yields values in the range of 1 through 200,000,000.
          - The short path-cost calculation method (16 bits) yields values in the range
          - of 1 through 65535.
        type: str
        choices: ["long", "short"]
      transmit_hold_count:
        description:
          - Number of bridge protocol data units (BPDUs) that can be sent before pausing
          - for 1 second. The range is from 1 to 20.
        type: int
      portfast:
        description: Portfast configurations.
        type: dict
        suboptions:
          default:
            description:
              - Immediately brings an STP port configured as an access or trunk port to the forwarding state.
            type: bool
          network_default:
            description:
              - Enables PortFast network mode by default on all switch access ports. Command for old IOS support.
            type: bool
          edge_default:
            description:
              - Enables PortFast edge mode by default on all switch access ports. Command for old IOS support.
            type: bool
          bpdufilter_default:
            description:
              - Enables PortFast BPDU filter by default on all PortFast ports.
            type: bool
          edge_bpdufilter_default:
            description:
              - Enables PortFast edge BPDU filter by default on all PortFast edge ports. Command for old IOS support.
            type: bool
          bpduguard_default:
            description:
              - Enables PortFast BPDU guard by default on all PortFast ports.
            type: bool
          edge_bpduguard_default:
            description:
              - Enables PortFast edge BPDU guard by default on all PortFast edge ports. Command for old IOS support.
            type: bool
      uplinkfast:
        description: UplinkFast feature
        type: dict
        suboptions:
          enabled:
            description:
              - Use to to enable UplinkFast
            type: bool
          max_update_rate:
            description:
              - Set the rate at which update packets are sent. The range is from 0 to 32000
            type: int
      forward_time:
        description: Sets the STP forward delay time.
        type: list
        elements: dict
        suboptions:
          vlan_list:
            description: List of VLAN identification numbers. The range is from 1 to 4094.
            type: str
          value:
            description: The range is from 4 to 30 seconds
            type: int
      hello_time:
        description:
          - Specifies the duration, in seconds, between the generation of configuration messages
          - by the root switch.
        type: list
        elements: dict
        suboptions:
          vlan_list:
            description: List of VLAN identification numbers. The range is from 1 to 4094.
            type: str
          value:
            description: The range is from 1 to 10 seconds
            type: int
      max_age:
        description:
          - Sets the maximum number of seconds the information in a bridge packet data unit (BPDU)
          - is valid.
        type: list
        elements: dict
        suboptions:
          vlan_list:
            description: List of VLAN identification numbers. The range is from 1 to 4094.
            type: str
          value:
            description: The range is from 6 to 40 seconds
            type: int
      priority:
        description:
          - Sets the STP bridge priority.
        type: list
        elements: dict
        suboptions:
          vlan_list:
            description: List of VLAN identification numbers. The range is from 1 to 4094.
            type: str
          value:
            description: Bridge priority in increments of 4096
            type: int
            choices: [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440]
      mst:
        description:
          - Option for multiple spanning-tree global configurations.
        type: dict
        suboptions:
          simulate_pvst_global:
            description:
              - Set to enable Per-VLAN Spanning Tree (PVST) simulation globally.
              - PVST simulation is enabled by default so that all interfaces on the device interoperate between
              - Multiple Spanning Tree (MST) and Rapid Per-VLAN Spanning Tree Plus (PVST+). To prevent an accidental
              - connection to a device that does not run MST as the default Spanning Tree Protocol (STP) mode,
              - you can disable PVST simulation.
            type: bool
          hello_time:
            description:
              - Specifies the duration, in seconds, between the generation of configuration messages
              - by the root switch. The range is from 1 to 10 seconds.
            type: int
          forward_time:
            description: Sets the STP forward delay time. The range is from 4 to 30 seconds.
            type: int
          max_age:
            description:
              - Sets the maximum number of seconds the information in a bridge packet data unit (BPDU)
              - is valid. The range is from 6 to 40 seconds.
            type: int
          max_hops:
            description:
              - Number of possible hops in the region before a BPDU is discarded; valid values are from 1 to 255 hops.
            type: int
          priority:
            description:
              - Sets the MST instance priority.
            type: list
            elements: dict
            suboptions:
              instance:
                description: List of MST instances.
                type: str
              value:
                description: STP priority value.
                type: int
                choices: [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440]
          configuration:
            description: Options for multiple spanning-tree region configuration.
            type: dict
            suboptions:
              name:
                description: Sets the name of an MST region.
                type: str
              revision:
                description: Sets the revision number for the MST configuration.
                type: int
              instances:
                description: List of configured instances.
                type: list
                elements: dict
                suboptions:
                  instance:
                    description: MST instance number.
                    type: int
                  vlan_list:
                    description: List of VLANs assosiated to MST instance.
                    type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
    type: str
  state:
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
        | section ^spanning-tree|^no spanning-tree) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - rendered
    - parsed
    - gathered
    default: merged
"""

EXAMPLES = """
# Using gathered

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# no spanning-tree bridge assurance
# spanning-tree transmit hold-count 5
# spanning-tree loopguard default
# spanning-tree logging
# spanning-tree portfast default
# spanning-tree portfast bpduguard default
# spanning-tree portfast bpdufilter default
# no spanning-tree etherchannel guard misconfig
# spanning-tree extend system-id
# spanning-tree uplinkfast max-update-rate 32
# spanning-tree uplinkfast
# spanning-tree backbonefast
# spanning-tree pathcost method long
# no spanning-tree mst simulate pvst global
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20
# spanning-tree mst hello-time 4
# spanning-tree mst forward-time 25
# spanning-tree mst max-age 33
# spanning-tree mst max-hops 33
# spanning-tree mst 0 priority 12288
# spanning-tree mst 1 priority 4096
# spanning-tree mst 5,7-9 priority 57344
# spanning-tree vlan 1,3-5,7,9-11 priority 24576
# spanning-tree vlan 1,3,9 hello-time 4
# spanning-tree vlan 4,6-8 hello-time 5
# spanning-tree vlan 5 hello-time 6
# spanning-tree vlan 1,7-20 forward-time 20
# spanning-tree vlan 1-2,4-5 max-age 38

- name: Gather facts for spanning_tree
  cisco.ios.ios_spanning_tree:
    state: gathered

# Task Output:
# ------------
#
# gathered:
#     backbonefast: true
#     bridge_assurance: false
#     etherchannel_guard_misconfig: false
#     forward_time:
#     -   value: 20
#         vlan_list: 1,7-20
#     hello_time:
#     -   value: 4
#         vlan_list: 1,3,9
#     -   value: 5
#         vlan_list: 4,6-8
#     -   value: 6
#         vlan_list: '5'
#     logging: true
#     loopguard_default: true
#     max_age:
#     -   value: 38
#         vlan_list: 1-2,4-5
#     mode: mst
#     mst:
#         configuration:
#             instances:
#             -   instance: 1
#                 vlan_list: 40-50
#             -   instance: 2
#                 vlan_list: 10-20
#             name: NAME
#             revision: 34
#         forward_time: 25
#         hello_time: 4
#         max_age: 33
#         max_hops: 33
#         priority:
#         -   instance: '0'
#             value: 12288
#         -   instance: '1'
#             value: 4096
#         -   instance: 5,7-9
#             value: 57344
#         simulate_pvst_global: false
#     pathcost_method: long
#     portfast:
#         bpdufilter_default: true
#         bpduguard_default: true
#         default: true
#     priority:
#     -   value: 24576
#         vlan_list: 1,3-5,7,9-11
#     transmit_hold_count: 5
#     uplinkfast:
#         enabled: true
#         max_update_rate: 32


# Using parsed

# File: parsed.cfg
# ----------------
#
# spanning-tree mode mst
# no spanning-tree bridge assurance
# spanning-tree transmit hold-count 5
# spanning-tree loopguard default
# spanning-tree logging
# spanning-tree portfast default
# spanning-tree portfast bpduguard default
# spanning-tree portfast bpdufilter default
# no spanning-tree etherchannel guard misconfig
# spanning-tree extend system-id
# spanning-tree uplinkfast max-update-rate 32
# spanning-tree uplinkfast
# spanning-tree backbonefast
# spanning-tree pathcost method long
# no spanning-tree mst simulate pvst global
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20
# spanning-tree mst hello-time 4
# spanning-tree mst forward-time 25
# spanning-tree mst max-age 33
# spanning-tree mst max-hops 33
# spanning-tree mst 0 priority 12288
# spanning-tree mst 1 priority 4096
# spanning-tree mst 5,7-9 priority 57344
# spanning-tree vlan 1,3-5,7,9-11 priority 24576
# spanning-tree vlan 1,3,9 hello-time 4
# spanning-tree vlan 4,6-8 hello-time 5
# spanning-tree vlan 5 hello-time 6
# spanning-tree vlan 1,7-20 forward-time 20
# spanning-tree vlan 1-2,4-5 max-age 38

- name: Parse the commands for provided configuration
  cisco.ios.ios_spanning_tree:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
#
# parsed:
#     backbonefast: true
#     bridge_assurance: false
#     etherchannel_guard_misconfig: false
#     forward_time:
#     -   value: 20
#         vlan_list: 1,7-20
#     hello_time:
#     -   value: 4
#         vlan_list: 1,3,9
#     -   value: 5
#         vlan_list: 4,6-8
#     -   value: 6
#         vlan_list: '5'
#     logging: true
#     loopguard_default: true
#     max_age:
#     -   value: 38
#         vlan_list: 1-2,4-5
#     mode: mst
#     mst:
#         configuration:
#             instances:
#             -   instance: 1
#                 vlan_list: 40-50
#             -   instance: 2
#                 vlan_list: 10-20
#             name: NAME
#             revision: 34
#         forward_time: 25
#         hello_time: 4
#         max_age: 33
#         max_hops: 33
#         priority:
#         -   instance: '0'
#             value: 12288
#         -   instance: '1'
#             value: 4096
#         -   instance: 5,7-9
#             value: 57344
#         simulate_pvst_global: false
#     pathcost_method: long
#     portfast:
#         bpdufilter_default: true
#         bpduguard_default: true
#         default: true
#     priority:
#     -   value: 24576
#         vlan_list: 1,3-5,7,9-11
#     transmit_hold_count: 5
#     uplinkfast:
#         enabled: true
#         max_update_rate: 32

# Using Rendered

- name: Rendered the provided configuration with the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: rendered
    config:
      backbonefast: true
      bridge_assurance: false
      etherchannel_guard_misconfig: false
      forward_time:
        - value: 20
          vlan_list: '1,7-20'
      hello_time:
        - value: 4
          vlan_list: '1,3,9'
        - value: 5
          vlan_list: '4,6-8'
        - value: 6
          vlan_list: '5'
      logging: true
      loopguard_default: true
      max_age:
        - value: 38
          vlan_list: '1-2,4-5'
      mode: mst
      mst:
        configuration:
          instances:
            - instance: 1
              vlan_list: 40-50
            - instance: 2
              vlan_list: 10-20
          name: NAME
          revision: 34
        forward_time: 25
        hello_time: 4
        max_age: 33
        max_hops: 33
        priority:
          - instance: '0'
            value: 12288
          - instance: '1'
            value: 4096
          - instance: '5,7-9'
            value: 57344
        simulate_pvst_global: false
      pathcost_method: long
      portfast:
        edge_bpdufilter_default: true
        edge_bpduguard_default: true
        edge_default: true
      priority:
        - value: 24576
          vlan_list: '1,3-5,7,9-11'
      transmit_hold_count: 5
      uplinkfast:
        enabled: true
        max_update_rate: 32

# Task Output:
# ------------
#
# rendered:
# - spanning-tree backbonefast
# - no spanning-tree bridge assurance
# - no spanning-tree etherchannel guard misconfig
# - spanning-tree logging
# - spanning-tree loopguard default
# - spanning-tree mode mst
# - spanning-tree pathcost method long
# - spanning-tree transmit hold-count 5
# - spanning-tree portfast edge default
# - spanning-tree portfast edge bpdufilter default
# - spanning-tree portfast edge bpduguard default
# - spanning-tree uplinkfast
# - spanning-tree uplinkfast max-update-rate 32
# - no spanning-tree mst simulate pvst global
# - spanning-tree vlan 1,7-20 forward-time 20
# - spanning-tree vlan 5 hello-time 6
# - spanning-tree vlan 4,6-8 hello-time 5
# - spanning-tree vlan 1,3,9 hello-time 4
# - spanning-tree vlan 1-2,4-5 max-age 38
# - spanning-tree vlan 1,3-5,7,9-11 priority 24576
# - spanning-tree mst hello-time 4
# - spanning-tree mst forward-time 25
# - spanning-tree mst max-age 33
# - spanning-tree mst max-hops 33
# - spanning-tree mst 5,7-9 priority 57344
# - spanning-tree mst 1 priority 4096
# - spanning-tree mst 0 priority 12288
# - spanning-tree mst configuration
# - name NAME
# - revision 34
# - instance 2 vlan 10-20
# - instance 1 vlan 40-50
# - exit

# Using Merged
# Example #1

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode rapid-pvst
# spanning-tree extend system-id

- name: Merged the provided configuration with the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: merged
    config:
      mst:
        forward_time: 25
        hello_time: 4
        max_age: 33
        max_hops: 33

# No commands will be sent out because STP mode is not mst (neither want nor have)

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode rapid-pvst
# spanning-tree extend system-id

# Using Merged
# Example #2

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode rapid-pvst
# spanning-tree extend system-id

- name: Merged the provided configuration with the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: merged
    config:
      mode: mst
      mst:
        forward_time: 25
        hello_time: 4
        max_age: 33
        max_hops: 33

# Task Output:
# ------------
#
# commands:
#     - spanning-tree mode mst
#     - spanning-tree mst hello-time 4
#     - spanning-tree mst forward-time 25
#     - spanning-tree mst max-age 33
#     - spanning-tree mst max-hops 33

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst hello-time 4
# spanning-tree mst forward-time 25
# spanning-tree mst max-age 33
# spanning-tree mst max-hops 33

# Using Merged
# Example #3

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20
# spanning-tree mst 1 priority 4096
# spanning-tree mst 5,7-9 priority 57344

- name: Merged the provided configuration with the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: merged
    config:
      mst:
        priority:
          - instance: 1
            value: 4096
          - instance: '5-7,9'
            value: 57344
        configuration:
          instances:
            - instance: 1
              vlan_list: 40-50
            - instance: 2
              vlan_list: 20-30

# Task Output:
# ------------
#
# commands:
#   - spanning-tree mst 6 priority 57344
#   - spanning-tree mst configuration
#   - instance 2 vlan 21-30
#   - exit

# After state:
# -------------
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-30
# spanning-tree mst 1 priority 4096
# spanning-tree mst 5-9 priority 57344

# Using Replaced

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# no spanning-tree bridge assurance
# spanning-tree transmit hold-count 10
# spanning-tree loopguard default
# spanning-tree portfast default
# spanning-tree portfast bpduguard default
# spanning-tree portfast bpdufilter default
# no spanning-tree etherchannel guard misconfig
# spanning-tree extend system-id
# spanning-tree uplinkfast max-update-rate 32
# spanning-tree uplinkfast
# spanning-tree backbonefast
# spanning-tree pathcost method long
# no spanning-tree mst simulate pvst global
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20
# spanning-tree mst hello-time 4
# spanning-tree mst forward-time 25
# spanning-tree mst max-age 33
# spanning-tree mst max-hops 33
# spanning-tree mst 0 priority 12288
# spanning-tree mst 1 priority 4096
# spanning-tree mst 5-9 priority 57344
# spanning-tree vlan 1,3-5,7,9-11 priority 24576
# spanning-tree vlan 1,3,9 hello-time 4
# spanning-tree vlan 4,6-8 hello-time 5
# spanning-tree vlan 5 hello-time 6
# spanning-tree vlan 1,7-20 forward-time 20
# spanning-tree vlan 1-2,4-5 max-age 38

- name: Replaced the provided configuration with the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: replaced
    config:
      mode: rapid-pvst
      logging: true
      priority:
        - value: 24576
          vlan_list: '1,3-5'
      mst:
        priority:
          - instance: 7-9
            value: 57344

# provided mst configuration will be ignored since stp mode changed to rapid-pvst

# Task Output:
# ------------
#
# commands:
# no spanning-tree backbonefast
# spanning-tree bridge assurance
# spanning-tree etherchannel guard misconfig
# spanning-tree logging
# no spanning-tree loopguard default
# spanning-tree mode rapid-pvst
# no spanning-tree pathcost method long
# no spanning-tree transmit hold-count 10
# no spanning-tree portfast default
# no spanning-tree portfast bpdufilter default
# no spanning-tree portfast bpduguard default
# no spanning-tree uplinkfast
# no spanning-tree uplinkfast max-update-rate 32
# spanning-tree mst simulate pvst global
# no spanning-tree vlan 1,7-20 forward-time 20
# no spanning-tree vlan 5 hello-time 6
# no spanning-tree vlan 4,6-8 hello-time 5
# no spanning-tree vlan 1,3,9 hello-time 4
# no spanning-tree vlan 1-2,4-5 max-age 38
# no spanning-tree vlan 7,9-11 priority 24576
# no spanning-tree mst configuration

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode rapid-pvst
# spanning-tree logging
# spanning-tree extend system-id
# spanning-tree vlan 1,3-5 priority 24576

# Using Deleted
# Example #1

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20

- name: Delete the provided configuration from the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: deleted
    config:
      mst:
        configuration:
          name: NAME
          revision: 34
          instances:
            - instance: 1
              vlan_list: 40-50

# Task Output:
# ------------
#
# commands:
#  - spanning-tree mst configuration
#  - no name NAME
#  - no revision 34
#  - no instance 1 vlan 40-50
#  - exit

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst configuration
#  instance 2 vlan 10-20

# Using Deleted
# Example #2

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
# spanning-tree mst configuration
#  name NAME
#  revision 34
#  instance 1 vlan 40-50
#  instance 2 vlan 10-20

- name: Delete the provided configuration from the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: deleted
    config:
      mst:
        configuration:
          name: NAME
          revision: 34
          instances:
            - instance: 1
              vlan_list: 40-50
            - instance: 2
              vlan_list: 10-20

# Task Output:
# ------------
#
# commands:
#  - no spanning-tree mst configuration

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id

# Using Deleted
# Example #3

# Before state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# no spanning-tree bridge assurance
# no spanning-tree etherchannel guard misconfig
# spanning-tree extend system-id
# no spanning-tree mst simulate pvst global

- name: Delete the provided configuration from the existing running configuration
  cisco.ios.ios_spanning_tree:
    state: deleted
    config:
      bridge_assurance: false
      etherchannel_guard_misconfig: false
      mst:
        simulate_pvst_global: false

# Task Output:
# ------------
#
# commands:
#  - spanning-tree bridge assurance
#  - spanning-tree etherchannel guard misconfig
#  - spanning-tree mst simulate pvst global

# After state:
# -------------
#
# vios#show running-config | section ^spanning-tree|^no spanning-tree
# spanning-tree mode mst
# spanning-tree extend system-id
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced) or C(deleted)
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
  returned: when I(state) is C(merged), C(replaced) or C(deleted)
  type: list
  sample:
    - spanning-tree pathcost method long
    - no spanning-tree mst simulate pvst global
    - spanning-tree mst configuration
    - name NAME
    - revision 34
    - instance 1 vlan 40-50
    - exit
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - spanning-tree pathcost method long
    - no spanning-tree mst simulate pvst global
    - spanning-tree mst configuration
    - name NAME
    - revision 34
    - instance 1 vlan 40-50
    - exit
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.spanning_tree.spanning_tree import (
    Spanning_treeArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.spanning_tree.spanning_tree import (
    Spanning_tree,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Spanning_treeArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Spanning_tree(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
