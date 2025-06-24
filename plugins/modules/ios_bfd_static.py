#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_static
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
---
module: ios_bfd_static
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Manages global BFD peer configurations for static routes.
description:
  - This module configures global BFD peers using the C(ip route static bfd) command family on Cisco IOS devices.
  - It supports both interface-based (e.g., C(ip route static bfd GigabitEthernet0/1 ...))) and IP-based (e.g., C(ip route static bfd 1.1.1.1 2.2.2.2 ...))) peer definitions.
version_added: "1.0.0"
author: "AAYUSH ANAND (@AAYUSH2091)"
notes:
  - Each peer configuration in the C(config) list must specify either an C(interface) or a C(source_ip), but not both. The module will fail if both or neither are provided.
  - The C(passive) option is only valid when C(source_ip) and C(group_name) are also defined for the same peer.

options:
  config:
    description: A list of BFD static peer configurations.
    type: list
    elements: dict
    suboptions:
      destination_ip:
        description: The destination IPv4 address of the BFD peer. This parameter is always required.
        type: str
        required: true
      interface:
        description:
          - The full name of the egress interface for an interface-based peer.
          - The module treats this as a single string, so names with spaces are supported.
          - Example - C(GigabitEthernet0/1), C(Tunnel10), C(ACR 3), C(Port-channel5).
          - This parameter cannot be used with C(source_ip).
        type: str
      source_ip:
        description:
          - The source IPv4 address for an IP-based peer.
          - This parameter cannot be used with C(interface).
        type: str
      vrf:
        description:
          - The name of the VRF context for this peer configuration.
          - For IP-based peers, this generates the syntax C(...<dest_ip> vrf <vrf_name> <src_ip>...).
          - For interface-based peers, this generates C(...vrf <vrf_name> <interface>...).
        type: str
      group_name:
        description:
          - The name of the BFD group to which this peer should be assigned.
          - Corresponds to the C(group <name>) keyword in the command.
        type: str
      log:
        description:
          - If set to C(true), this enables logging for BFD up/down events for this peer.
          - Corresponds to the C(log) keyword.
        type: bool
        default: false
      unassociate:
        description:
          - If set to C(true), the static route will not be associated with the BFD session state.
          - Corresponds to the C(unassociate) keyword.
        type: bool
        default: false
      passive:
        description:
          - If set to C(true), this peer will be configured as a passive member of its group.
          - This option is ONLY valid for IP-based peers (when C(source_ip) is defined) and requires C(group_name) to also be set.
        type: bool
        default: false

  state:
    description:
      - The state the configuration should be left in.
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_static.bfd_static import (
    Bfd_staticArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bfd_static.bfd_static import (
    Bfd_static,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_staticArgs.argument_spec,
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

    result = Bfd_static(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
