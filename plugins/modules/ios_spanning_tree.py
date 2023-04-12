#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_spanning_tree
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_spanning_tree
short_description: Resource module to configure Spanning Tree.
description:
  - This module provides declarative management of Spanning tree on Cisco IOS
  - network devices.
version_added: 1.0.0
author: Timur Nizharadze (@tnizharadze)
notes:
  - Tested against Cisco IOS Version 15.2 on CML.
options:
  config:
    description: The provided configurations.
    type: dict
    suboptions:
      spanning_tree:
        description: Spanning Tree configurations.
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
          extend_system_id:
            description:
              - Use the spanning-tree extend system-id global configuration command on the switch
              - stack or on a standalone switch to enable the extended system ID feature.
            type: bool
          logging:
            description:
              - Enable logging of spanning tree changes.
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
            mutually_exclusive:
              - [ "network_default", "edge_default" ]
            suboptions:
              network_default:
                description:
                  - Enables PortFast network mode by default on all switch access ports.
                type: bool
              edge_default:
                description:
                  - Enables PortFast edge mode by default on all switch access ports.
                type: bool
              bpdufilter_default:
                description:
                  - Enables PortFast edge BPDU filter by default on all PortFast edge ports.
                type: bool
              bpduguard_default:
                description:
                  - Enables PortFast edge BPDU guard by default on all PortFast edge ports.
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
            description: Sets the STP forward delay time..
            type: dict
            required_together: ["vlan_list", "value"]
            suboptions:
              vlan_list:
                description: List of VLAN identification numbers. The range is from 1 to 4094.
                type: list
                elements: int
              value:
                description: The range is from 4 to 30 seconds
                type: int
          hello_time:
            description:
              - Specifies the duration, in seconds, between the generation of configuration messages
              - by the root switch..
            type: dict
            required_together: ["vlan_list", "value"]
            suboptions:
              vlan_list:
                description: List of VLAN identification numbers. The range is from 1 to 4094.
                type: list
                elements: int
              value:
                description: The range is from 1 to 10 seconds
                type: int
          max_age:
            description:
              - Sets the maximum number of seconds the information in a bridge packet data unit (BPDU)
              - is valid.
            type: dict
            required_together: ["vlan_list", "value"]
            suboptions:
              vlan_list:
                description: List of VLAN identification numbers. The range is from 1 to 4094.
                type: list
                elements: int
              value:
                description: The range is from 6 to 40 seconds
                type: int
          priority:
            description:
              - Sets the STP bridge priority..
            type: dict
            required_together: ["vlan_list", "value"]
            suboptions:
              vlan_list:
                description: List of VLAN identification numbers. The range is from 1 to 4094.
                type: list
                elements: int
              value:
                description: Bridge priority in increments of 4096
                type: int
                choices: [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440]
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
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
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
# Using merged
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
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Spanning_tree(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
