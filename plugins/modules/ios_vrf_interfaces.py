#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vrf_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: ios_vrf_interfaces
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Manages VRF configuration on interfaces.
description:
  - Manages Virtual Routing and Forwarding (VRF) configuration on interfaces of Cisco IOS devices.
version_added: "1.0.0"
author: "AAYUSH ANAND (@username)"
notes:
  - Tested against Cisco IOS XE Version X.X
  - VRF must exist before assigning to an interface
  - When removing VRF from interface, associated IP addresses will be removed
options:
  config:
    description: A list of interface VRF configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface to be configured.
          - Example - GigabitEthernet0/1, FastEthernet0/0
        type: str
        required: true
      vrf:
        description:
          - Name of the VRF to be configured on the interface.
          - When configured, applies 'vrf forwarding <vrf_name>' under the interface.
        type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by executing
        the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and transforms
        it into Ansible structured data as per the resource module's argspec and the value
        is then returned in the I(parsed) key within the result.
    type: str
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_interfaces.vrf_interfaces import (
    Vrf_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vrf_interfaces.vrf_interfaces import (
    Vrf_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vrf_interfacesArgs.argument_spec,
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

    result = Vrf_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
