#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_evpn_ethernet
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_epvn_ethernet
short_description: Resource module to configure L2VPN EVPN Ethernet Segment.
description: This module manages the L2VPN EVPN Ethernet Segment attributes of Cisco IOS network devices.
version_added: 9.2.0
author:
  - Sagar Paul (@KB-perByte)
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOSXE Version 17.6 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary of L2VPN EVPN Ethernet Segment options
    type: list
    elements: dict
    suboptions:
      segment:
        description:
          - L2VPN EVPN Ethernet Segment, l2vpn evpn ethernet-segment 1
        type: str
        required: true
      default:
        description: Set a command to its defaults
        type: bool
      df_election:
        description: Designated forwarder election parameters
        type: dict
        suboptions:
          preempt_time:
            description: Preempt time before advertising routes
            type: int
          wait_time:
            description: Designated forwarder election wait time
            type: int
      identifier:
        description: Ethernet Segment Identifiers
        type: dict
        suboptions:
          identifier_type:
            description:
              - Type 0 (arbitrary 9-octet ESI value)
              - Type 3 (MAC-based ESI value)
            type: str
            choices:
              - '0'
              - '3'
          mac_address:
            description: system mac or 9-octet ESI value in hex
            type: str
      redundancy:
        description: Multi-homing redundancy parameters
        type: dict
        suboptions:
          all_active:
            description: Per-flow load-balancing between PEs on same Ethernet Segment
            type: bool
          single_active:
            description: Per-vlan load-balancing between PEs on same Ethernet Segment
            type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^l2vpn).
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
      - purged
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
        | section ^l2vpn) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
    type: str
"""

EXAMPLES = """

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
    - l2vpn evpn ethernet-segment 1
    - identifier type 0 00.00.00.00.00.00.00.00.01
    - redundancy single-active
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - l2vpn evpn ethernet-segment 1
    - identifier type 3 system-mac 0000.0000.0000.0001
    - redundancy all-active
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernetArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernet,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Evpn_ethernetArgs.argument_spec,
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

    result = Evpn_ethernet(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
