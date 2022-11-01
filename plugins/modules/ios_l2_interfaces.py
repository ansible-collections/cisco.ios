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
author: Sumit Jaiswal (@justjais)
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
