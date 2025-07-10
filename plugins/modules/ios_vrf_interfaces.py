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
author: "AAYUSH ANAND (@AAYUSH2091)"
notes:
  - Tested against Cisco IOS XE Version 17.13.01a
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
          - Example - GigabitEthernet1, Loopback24
        type: str
        required: true
      vrf_name:
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
# Using merged

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Merge provided configuration with device configuration
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: GigabitEthernet1
      - name: GigabitEthernet2
        vrf_name: vrf_D
      - name: GigabitEthernet3
      - name: GigabitEthernet4
    state: merged

# Task Output:
# ------------
#
# before:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#
# commands:
#   - interface GigabitEthernet2
#   - vrf forwarding vrf_D
#
# after:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_D"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  vrf forwarding vrf_D
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using overridden

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  vrf forwarding vrf_B
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Override device configuration with provided configuration
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: GigabitEthernet1
      - name: GigabitEthernet2
      - name: GigabitEthernet3
      - name: GigabitEthernet4
    state: overridden

# Task Output:
# ------------
#
# before:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_B"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#
# commands:
#   - interface GigabitEthernet2
#   - no vrf forwarding vrf_B
#
# after:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using gathered

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  vrf forwarding vrf_B
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Gather listed VRF interfaces
  cisco.ios.ios_vrf_interfaces:
    state: gathered

# Task Output:
# ------------
#
# gathered:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_B"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"

# Using rendered

- name: Render VRF configuration
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: GigabitEthernet1
      - name: GigabitEthernet2
        vrf_name: vrf_D
      - name: GigabitEthernet3
      - name: GigabitEthernet4
    state: rendered

# Task Output:
# ------------
#
# rendered:
#   - interface GigabitEthernet2
#   - vrf forwarding vrf_D

# Using parsed

# File: parsed.cfg
# ---------------
#
# interface GigabitEthernet1
#  vrf vrf_C
#  shutdown
# !
# interface GigabitEthernet2
#  vrf vrf_D
#  shutdown
# !
# interface GigabitEthernet3
#  shutdown
# !
# interface GigabitEthernet4
#  shutdown
# !

- name: Parse configuration from device running config
  cisco.ios.ios_vrf_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
#
# parsed:
#   - name: "GigabitEthernet1"
#     vrf_name: "vrf_C"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_D"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"

# Using replaced

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  vrf forwarding vrf_A
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  vrf forwarding vrf_B
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  vrf forwarding vrf_C
#  no ip address
#  shutdown
#  negotiation auto

- name: Replace device configuration of listed VRF interfaces with provided configuration
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: GigabitEthernet1
        vrf_name: vrf_D
      - name: GigabitEthernet2
        vrf_name: vrf_E
    state: replaced

# Task Output:
# ------------
#
# before:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#     vrf_name: "vrf_A"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_B"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#     vrf_name: "vrf_C"
#
# commands:
#   - interface GigabitEthernet1
#   - no vrf forwarding vrf_A
#   - vrf forwarding vrf_D
#   - interface GigabitEthernet2
#   - no vrf forwarding vrf_B
#   - vrf forwarding vrf_E
#
# after:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#     vrf_name: "vrf_D"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_E"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#     vrf_name: "vrf_C"

# Using deleted

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  vrf forwarding vrf_A
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  vrf forwarding vrf_B
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  vrf forwarding vrf_C
#  no ip address
#  shutdown
#  negotiation auto

- name: Delete VRF configuration of specified interfaces
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: GigabitEthernet1
      - name: GigabitEthernet2
    state: deleted

# Task Output:
# ------------
#
# before:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#     vrf_name: "vrf_A"
#   - name: "GigabitEthernet2"
#     vrf_name: "vrf_B"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#     vrf_name: "vrf_C"
#
# commands:
#   - interface GigabitEthernet1
#   - no vrf forwarding vrf_A
#   - interface GigabitEthernet2
#   - no vrf forwarding vrf_B
#
# after:
#   - name: "Loopback24"
#   - name: "GigabitEthernet1"
#   - name: "GigabitEthernet2"
#   - name: "GigabitEthernet3"
#   - name: "GigabitEthernet4"
#     vrf_name: "vrf_C"

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Loopback24
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  negotiation auto
# interface GigabitEthernet4
#  vrf forwarding vrf_C
#  no ip address
#  shutdown
#  negotiation auto
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted)
  type: list
  sample: >
    [
        {
            "name": "Loopback24"
        },
        {
            "name": "GigabitEthernet1"
        },
        {
            "name": "GigabitEthernet2",
            "vrf_name": "vrf_B"
        },
        {
            "name": "GigabitEthernet3"
        },
        {
            "name": "GigabitEthernet4"
        }
    ]

after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    [
        {
            "name": "Loopback24"
        },
        {
            "name": "GigabitEthernet1"
        },
        {
            "name": "GigabitEthernet2",
            "vrf_name": "vrf_D"
        },
        {
            "name": "GigabitEthernet3"
        },
        {
            "name": "GigabitEthernet4"
        }
    ]

commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted)
  type: list
  sample:
    - "interface GigabitEthernet2"
    - "vrf forwarding vrf_D"
    - "no vrf forwarding vrf_B"

rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - "interface GigabitEthernet1"
    - "vrf forwarding vrf_C"
    - "interface GigabitEthernet2"
    - "vrf forwarding vrf_D"

gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    [
        {
            "name": "Loopback24"
        },
        {
            "name": "GigabitEthernet1"
        },
        {
            "name": "GigabitEthernet2",
            "vrf_name": "vrf_B"
        },
        {
            "name": "GigabitEthernet3"
        },
        {
            "name": "GigabitEthernet4"
        }
    ]

parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    [
        {
            "name": "GigabitEthernet1",
            "vrf_name": "vrf_C"
        },
        {
            "name": "GigabitEthernet2",
            "vrf_name": "vrf_D"
        },
        {
            "name": "GigabitEthernet3"
        },
        {
            "name": "GigabitEthernet4"
        }
    ]
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
