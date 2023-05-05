#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_lag_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_lag_interfaces
short_description: Resource module to configure LAG interfaces.
description:
  This module manages properties of Link Aggregation Group on Cisco IOS
  devices.
version_added: 1.0.0
author:
  - Sagar Paul (@KB-perByte)
  - Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A list of link aggregation group configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - ID of Ethernet Channel of interfaces.
          - Refer to vendor documentation for valid port values.
        type: str
        required: true
      members:
        description:
          - Interface options for the link aggregation group.
        type: list
        elements: dict
        suboptions:
          member:
            description:
              - Interface member of the link aggregation group.
            type: str
          mode:
            description:
              - Etherchannel Mode of the interface for link aggregation.
              - On mode has to be quoted as 'on' or else pyyaml will convert
                to True before it gets to Ansible.
            type: str
            choices:
              - auto
              - "on"
              - desirable
              - active
              - passive
          link:
            description:
              - Assign a link identifier used for load-balancing.
              - Refer to vendor documentation for valid values.
              - NOTE, parameter only supported on Cisco IOS XE platform.
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
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
      - overridden
      - deleted
      - rendered
      - parsed
      - gathered
    default: merged
"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown
# interface GigabitEthernet0/4
#  shutdown

- name: Merge provided configuration with device configuration
  cisco.ios.ios_lag_interfaces:
    config:
      - name: Port-channel10
        members:
          - member: GigabitEthernet0/1
            mode: auto
          - member: GigabitEthernet0/2
            mode: auto
      - name: Port-channel20
        members:
          - member: GigabitEthernet0/3
            mode: on
      - name: Port-channel30
        members:
          - member: GigabitEthernet0/4
            mode: active
    state: merged

# Task Output:
# ---------------

# commands:
# - interface GigabitEthernet0/1
# - channel-group 10 mode auto
# - interface GigabitEthernet0/2
# - channel-group 10 mode auto
# - interface GigabitEthernet0/3
# - channel-group 20 mode on
# - interface GigabitEthernet0/4
# - channel-group 30 mode active

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode on
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

# Using overridden
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode on
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_lag_interfaces:
    config:
      - name: Port-channel20
        members:
          - member: GigabitEthernet0/2
            mode: auto
          - member: GigabitEthernet0/3
            mode: auto
    state: overridden

# Task Output:
# ---------------

# commands:
# - interface GigabitEthernet0/1
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/2
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/4
# - no channel-group 30 mode active
# - interface GigabitEthernet0/2
# - channel-group 20 mode auto
# - interface GigabitEthernet0/3
# - channel-group 20 mode auto

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 20 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode auto
# interface GigabitEthernet0/4
#  shutdown

# Using replaced
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode on
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_lag_interfaces:
    config:
      - name: Port-channel30
        members:
          - member: GigabitEthernet0/3
            mode: auto
    state: replaced

# Task Output:
# ---------------

# commands:
# - interface GigabitEthernet0/3
# - channel-group 30 mode auto
# - interface GigabitEthernet0/4
# - no channel-group 30 mode active

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 30 mode auto
# interface GigabitEthernet0/4
#  shutdown

# Using Deleted
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode on
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

- name: "Delete LAG attributes of given interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lag_interfaces:
    config:
      - name: Port-channel10
      - name: Port-channel20
    state: deleted

# Task Output:
# ---------------

# commands:
# - interface GigabitEthernet0/1
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/2
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/3
# - no channel-group 20 mode on

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured LLDP module attributes)"

#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/2
#  shutdown
#  channel-group 10 mode auto
# interface GigabitEthernet0/3
#  shutdown
#  channel-group 20 mode on
# interface GigabitEthernet0/4
#  shutdown
#  channel-group 30 mode active

- name: "Delete all configured LAG attributes for interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lag_interfaces:
    state: deleted

# Task Output:
# ---------------

# commands:
# - interface GigabitEthernet0/1
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/2
# - no channel-group 10 mode auto
# - interface GigabitEthernet0/3
# - no channel-group 20 mode on
# - interface GigabitEthernet0/4
# - no channel-group 30 mode active

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown
# interface GigabitEthernet0/4
#  shutdown

# Using Gathered

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#   shutdown
#   channel-group 10 mode auto
# interface GigabitEthernet0/2
#   shutdown
#   channel-group 10 mode auto
# interface GigabitEthernet0/3
#   shutdown
#   channel-group 20 mode on
# interface GigabitEthernet0/4
#   shutdown
#   channel-group 30 mode active

- name: Gather listed LAG interfaces with provided configurations
  cisco.ios.ios_lag_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
# {
#     "members": [
#         {
#             "member": "GigabitEthernet0/1",
#             "mode": "auto"
#         },
#         {
#             "member": "GigabitEthernet0/2",
#             "mode": "auto"
#         }
#     ],
#     "name": "Port-channel10"
# },
# {
#     "members": [
#         {
#             "member": "GigabitEthernet0/3",
#             "mode": "on"
#         }
#     ],
#     "name": "Port-channel20"
# },
# {
#     "members": [
#         {
#             "member": "GigabitEthernet0/4",
#             "mode": "active"
#         }
#     ],
#     "name": "Port-channel30"
# }
# ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#   shutdown
#   channel-group 10 mode auto
# interface GigabitEthernet0/2
#   shutdown
#   channel-group 10 mode auto
# interface GigabitEthernet0/3
#   shutdown
#   channel-group 20 mode on
# interface GigabitEthernet0/4
#   shutdown
#   channel-group 30 mode active

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_lag_interfaces:
    config:
      - name: Port-channel11
        members:
          - member: GigabitEthernet0/1
            mode: active
      - name: Port-channel22
        members:
          - member: GigabitEthernet0/2
            mode: passive
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "channel-group 11 mode active",
#         "interface GigabitEthernet0/2",
#         "channel-group 22 mode passive",
#     ]

# Using Parsed

#  File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# channel-group 11 mode active
# interface GigabitEthernet0/2
# channel-group 22 mode passive

- name: Parse the commands for provided configuration
  cisco.ios.ios_lag_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#     {
#         "members": [
#             {
#                 "member": "GigabitEthernet0/1",
#                 "mode": "active"
#             }
#         ],
#         "name": "Port-channel11"
#     },
#     {
#         "members": [
#             {
#                 "member": "GigabitEthernet0/2",
#                 "mode": "passive"
#             }
#         ],
#         "name": "Port-channel22"
#     }
# ]
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
    - interface GigabitEthernet0/1
    - channel-group 10 mode auto
    - channel-group 10 mode active link 20
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet0/2
    - channel-group 20 mode auto
    - channel-group 20 mode active link 60
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.lag_interfaces.lag_interfaces import (
    Lag_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.lag_interfaces.lag_interfaces import (
    Lag_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Lag_InterfacesArgs.argument_spec,
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

    result = Lag_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
