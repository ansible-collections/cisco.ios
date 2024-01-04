#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vlan_configuration
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_vlan_configurations
short_description: Resource module for vlan configuration options.
description: This module provides declarative management of vlan configuration options on Cisco IOS network
  devices.
version_added: 6.1.0
author: Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
notes:
  - Tested against Cisco IOS device with Version 17.13.01 on Cat9k on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of L2VPN Ethernet Virtual Private Network (EVPN) EVI configuration
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
          - ID of the VLAN. Range 1-4094
        type: int
        required: true
      member:
        description:
          - Members of VLAN
        type: dict
        suboptions:
          vni:
            description:
              - VXLAN vni
            type: int
            required: true
          evi:
            description:
              - Ethernet Virtual Private Network (EVPN)
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(show running-config | sec ^vlan configuration .+).
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
# vlan configuration 101
#  member evpn-instance 101 vni 10101
# vlan configuration 102
#  member evpn-instance 102 vni 10102
# vlan configuration 201
#  member evpn-instance 201 vni 10201
# vlan configuration 202
#  member evpn-instance 202 vni 10202
# vlan configuration 901
#  member vni 50901
# vlan configuration 902
#  member vni 50902

- name: Merge provided configuration with device configuration
  cisco.ios.ios_vlans:
    config:
      - vlan_id: 102
        member:
          vni: 10102
          evi: 102
      - vlan_id: 901
        member:
          vni: 50901
    configuration: true
    state: merged

# After state:
# ------------
#
# Leaf-01#show run nve | sec ^vlan configuration
# vlan configuration 101
#  member evpn-instance 101 vni 10101
# vlan configuration 102
#  member evpn-instance 102 vni 10102
# vlan configuration 201
#  member evpn-instance 201 vni 10201
# vlan configuration 901
#  member vni 50901
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
    - vlan configuration 202
    - member evpn-instance 202 vni 10202
    - member vni 50901
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - vlan configuration 202
    - member evpn-instance 202 vni 10202
    - member vni 50901
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlan_configurations.vlan_configurations import (
    Vlan_configurationsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vlan_configurations.vlan_configurations import (
    Vlan_configurations,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vlan_configurationsArgs.argument_spec,
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

    result = Vlan_configurations(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
