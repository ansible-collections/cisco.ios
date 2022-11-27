#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_interfaces
short_description: Resource module to configure interfaces.
description: This module manages the interface attributes of Cisco IOS network devices.
version_added: 1.0.0
author:
- Sumit Jaiswal (@justjais)
- Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, e.g. GigabitEthernet0/2, loopback999.
        type: str
        required: true
      description:
        description:
        - Interface description.
        type: str
      enabled:
        description:
        - Administrative state of the interface.
        - Set the value to C(true) to administratively enable the interface or C(false)
          to disable it.
        type: bool
        default: true
      speed:
        description:
        - Interface link speed. Applicable for Ethernet interfaces only.
        type: str
      mtu:
        description:
        - MTU for a specific interface. Applicable for Ethernet interfaces only.
        - Refer to vendor documentation for valid values.
        type: int
      duplex:
        description:
        - Interface link status. Applicable for Ethernet interfaces only, either in
          half duplex, full duplex or in automatic state which negotiates the duplex
          automatically.
        type: str
        choices:
        - full
        - half
        - auto
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
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  no ip address
#  duplex auto
#  speed auto

- name: Merge provided configuration with device configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
      description: Configured and Merged by Ansible Network
      enabled: true
    - name: GigabitEthernet0/3
      description: Configured and Merged by Ansible Network
      mtu: 2800
      enabled: false
      speed: 100
      duplex: full
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#       "interface GigabitEthernet0/2",
#       "description Configured and Merged by Ansible Network",
#       "no shutdown",
#       "interface GigabitEthernet0/3",
#       "description Configured and Merged by Ansible Network",
#       "mtu 2800",
#       "duplex full",
#       "shutdown",
#     ],

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured and Merged by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Merged by Ansible Network
#  mtu 2800
#  no ip address
#  shutdown
#  duplex full
#  speed 100

# Using replaced

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  mtu 2000
#  no ip address
#  shutdown
#  duplex full
#  speed 100

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/3
      description: Configured and Replaced by Ansible Network
      enabled: false
      duplex: auto
      mtu: 2500
      speed: 1000
    state: replaced

# Commands Fired:
# ---------------

# "commands": [
#       "interface GigabitEthernet0/3",
#       "description Configured and Replaced by Ansible Network",
#       "mtu 2500",
#       "duplex auto",
#       "speed 1000",
#     ],

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Replaced by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex auto
#  speed 1000

# Using overridden

# Before state:
# -------------
#
# vios#show running-config | section ^interface#
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible
#  mtu 2800
#  no ip address
#  shutdown
#  duplex full
#  speed 100

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
      description: Configured and Overridden by Ansible Network
      speed: 1000
    - name: GigabitEthernet0/3
      description: Configured and Overridden by Ansible Network
      enabled: false
      duplex: full
      mtu: 2000
    state: overridden

# "commands": [
#       "interface GigabitEthernet0/1",
#       "no description description Configured by Ansible",
#       "no duplex auto",
#       "no speed auto",
#       "interface GigabitEthernet0/2",
#       "description Configured and Overridden by Ansible Network",
#       "interface GigabitEthernet0/3",
#       "description Configured and Overridden by Ansible Network",
#       "mtu 2000",
#     ],

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured and Overridden by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Overridden by Ansible Network
#  mtu 2000
#  no ip address
#  shutdown
#  duplex full
#  speed auto

# Using Deleted

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

- name: "Delete module attributes of given interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
    state: deleted

# "commands": [
#       "interface GigabitEthernet0/2",
#       "no description description Configured by Ansible Network",
#       "no duplex auto",
#       "no speed 1000",
#     ],

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

# Using Purged

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
# interface Port-channel10
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

- name: "Purge given interfaces (Note: This will delete the interface itself)"
  cisco.ios.ios_interfaces:
    config:
    - name: Loopback888
    - name: Port-channel10
    state: purged

# "commands": [
#       "no interface Loopback888",
#       "no interface Port-channel10",
#     ],

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000


# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  description this is interface1
#  mtu 65
#  duplex auto
#  speed 10
# interface GigabitEthernet0/2
#  description this is interface2
#  mtu 110
#  shutdown
#  duplex auto
#  speed 100

- name: Gather listed interfaces with provided configurations
  cisco.ios.ios_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "description": "this is interface1",
#             "duplex": "auto",
#             "enabled": true,
#             "mtu": 65,
#             "name": "GigabitEthernet0/1",
#             "speed": "10"
#         },
#         {
#             "description": "this is interface2",
#             "duplex": "auto",
#             "enabled": false,
#             "mtu": 110,
#             "name": "GigabitEthernet0/2",
#             "speed": "100"
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  description this is interface1
#  mtu 65
#  duplex auto
#  speed 10
# interface GigabitEthernet0/2
#  description this is interface2
#  mtu 110
#  shutdown
#  duplex auto
#  speed 100

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/1
      description: Configured by Ansible-Network
      mtu: 110
      enabled: true
      duplex: half
    - name: GigabitEthernet0/2
      description: Configured by Ansible-Network
      mtu: 2800
      enabled: false
      speed: 100
      duplex: full
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "description Configured by Ansible-Network",
#         "mtu 110",
#         "duplex half",
#         "no shutdown",
#         "interface GigabitEthernet0/2",
#         "description Configured by Ansible-Network",
#         "mtu 2800",
#         "speed 100",
#         "duplex full",
#         "shutdown"
#         ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# description interfaces 0/1
# mtu 110
# duplex half
# no shutdown
# interface GigabitEthernet0/2
# description interfaces 0/2
# mtu 2800
# speed 100
# duplex full
# shutdown

- name: Parse the commands for provided configuration
  cisco.ios.ios_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "description": "interfaces 0/1",
#             "duplex": "half",
#             "enabled": true,
#             "mtu": 110,
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "description": "interfaces 0/2",
#             "duplex": "full",
#             "enabled": true,
#             "mtu": 2800,
#             "name": "GigabitEthernet0/2",
#             "speed": "100"
#         }
#     ]
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
    - interface GigabitEthernet2
    - speed 1200
    - mtu 1800
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet1
    - description Interface description
    - shutdown
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.interfaces.interfaces import (
    Interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=InterfacesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "purged", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
