#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bfd_interfaces
short_description: Resource module to configure bfd in interfaces.
description: This module manages the bfd configuration in interface of Cisco IOS network devices.
version_added: 11.3.0
author:
  - Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A list of interface options, to configure bfd.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of interface, e.g. GigabitEthernet0/2, loopback999.
          - Short interface names like Gi0/2, Lo999 may impact idempotency.
        type: str
        required: true
      echo:
        description:
          - Use echo adjunct as bfd detection mechanism.
        type: bool
      bfd:
        description:
          - Enable or disable bfd for the interface.
          - Default value for appliance might impact idempotency.
        type: bool
      template:
        description:
          - BFD template (might impact other BFD configuration),
          - Ansible won't guarantee state operations.
        type: str
      local_address:
        description:
          - BFD local address.
        type: str
      jitter:
        description:
          - Enable BFD interval transmit jittering.
        type: bool
      interval:
        description:
          - Transmit interval between BFD packets
        type: dict
        suboptions:
          input:
            description:
              - Interval between transmitted BFD control packets 50 - 9999 Milliseconds
            type: int
          min_rx:
            description:
              - Minimum receive interval capability 50 - 9999 Milliseconds
            type: int
          multiplier:
            description:
              - Detection multiplier 3 - 50
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS XE device by
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
        | section interface) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet3
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto


- name: Apply the provided BFD configuration to interfaces
  cisco.ios.ios_bfd_interfaces:
    config:
      - name: GigabitEthernet1
        bfd: true
        jitter: false
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
        local_address: 10.0.1.2
        template: ANSIBLE
      - name: GigabitEthernet2
        bfd: true
        jitter: true
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
      - name: GigabitEthernet4
        template: ANSIBLE_Tempalte
    state: merged

# Commands Fired:
# ---------------

# after:
# -   interval:
#         input: 100
#         min_rx: 100
#         multiplier: 3
#     jitter: false
#     local_address: 10.0.1.2
#     name: GigabitEthernet1
# -   interval:
#         input: 100
#         min_rx: 100
#         multiplier: 3
#     name: GigabitEthernet2
# -   name: GigabitEthernet3
# -   name: GigabitEthernet4
#     template: ANSIBLE_Tempalte
# before:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
# -   name: GigabitEthernet3
# -   name: GigabitEthernet4
# changed: true
# commands:
# - interface GigabitEthernet1
# - bfd enable
# - bfd local-address 10.0.1.2
# - bfd interval 100 min_rx 100 multiplier 3
# - bfd template ANSIBLE
# - no bfd jitter
# - interface GigabitEthernet2
# - bfd enable
# - bfd jitter
# - bfd interval 100 min_rx 100 multiplier 3
# - interface GigabitEthernet4
# - bfd template ANSIBLE_Tempalte

# After state:
# ------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
#  bfd local-address 10.0.1.2
#  bfd interval 100 min_rx 100 multiplier 3
#  no bfd jitter
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
#  bfd interval 100 min_rx 100 multiplier 3
# interface GigabitEthernet3
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
#  bfd template ANSIBLE_Tempalte

# Using state: replaced

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
#  bfd local-address 10.0.1.2
#  bfd interval 100 min_rx 100 multiplier 3
#  no bfd jitter
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
#  bfd interval 100 min_rx 100 multiplier 3
# interface GigabitEthernet3
#  no ip address
#  shutdown
#  negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
#  bfd template ANSIBLE_Tempalte


- name: Replace BFD configuration for specified interfaces
  cisco.ios.ios_bfd_interfaces:
    config:
      - name: GigabitEthernet1
        bfd: true
        echo: true
        jitter: true
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
        local_address: 10.0.1.2
        template: ANSIBLE
      - name: GigabitEthernet2
        bfd: true
        echo: true
        jitter: true
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
      - name: GigabitEthernet6
        template: ANSIBLE_3Tempalte
    state: replaced

# Commands Fired:
# ---------------

# "commands": [
#       "interface GigabitEthernet1",
#       "bfd enable",
#       "bfd echo",
#       "bfd jitter",
#       "bfd local-address 10.0.1.2",
#       "bfd interval 100 min_rx 100 multiplier 3",
#       "bfd template ANSIBLE",
#       "interface GigabitEthernet2",
#       "bfd enable",
#       "bfd echo",
#       "bfd jitter",
#       "bfd interval 100 min_rx 100 multiplier 3",
#       "no bfd template OLD_TEMPLATE",
#       "interface GigabitEthernet6",
#       "bfd template ANSIBLE_3Tempalte"
#     ]

# After state:
# ------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd enable
#  bfd echo
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 100 min_rx 100 multiplier 3
#  bfd template ANSIBLE
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd enable
#  bfd echo
#  bfd jitter
#  bfd interval 100 min_rx 100 multiplier 3
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3
# interface GigabitEthernet6
#  bfd template ANSIBLE_3Tempalte

# Using state: overridden

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd local-address 10.0.0.1
#  bfd interval 57 min_rx 66 multiplier 45
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd template OLD_TEMPLATE
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

- name: Override all BFD configuration with provided configuration
  cisco.ios.ios_bfd_interfaces:
    config:
      - name: GigabitEthernet1
        bfd: true
        echo: true
        jitter: true
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
        local_address: 10.0.1.2
        template: ANSIBLE
      - name: GigabitEthernet2
        bfd: true
        echo: true
        jitter: true
        interval:
          input: 100
          min_rx: 100
          multiplier: 3
      - name: GigabitEthernet6
        template: ANSIBLE_3Tempalte
    state: overridden

# Commands Fired:
# ---------------

# "commands": [
#       "interface GigabitEthernet3",
#       "no bfd jitter",
#       "no bfd local-address 10.0.1.2",
#       "no bfd interval 50 min_rx 50 multiplier 3",
#       "interface GigabitEthernet1",
#       "bfd enable",
#       "bfd echo",
#       "bfd jitter",
#       "bfd local-address 10.0.1.2",
#       "bfd interval 100 min_rx 100 multiplier 3",
#       "bfd template ANSIBLE",
#       "interface GigabitEthernet2",
#       "bfd enable",
#       "bfd echo",
#       "bfd jitter",
#       "bfd interval 100 min_rx 100 multiplier 3",
#       "no bfd template OLD_TEMPLATE",
#       "interface GigabitEthernet6",
#       "bfd template ANSIBLE_3Tempalte"
#     ]

# After state:
# ------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd enable
#  bfd echo
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 100 min_rx 100 multiplier 3
#  bfd template ANSIBLE
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd enable
#  bfd echo
#  bfd jitter
#  bfd interval 100 min_rx 100 multiplier 3
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
# interface GigabitEthernet6
#  bfd template ANSIBLE_3Tempalte

# Using state: deleted

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd local-address 10.0.0.1
#  bfd interval 57 min_rx 66 multiplier 45
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd template OLD_TEMPLATE
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

- name: Delete BFD configuration for specified interfaces
  cisco.ios.ios_bfd_interfaces:
    config:
      - name: GigabitEthernet1
      - name: GigabitEthernet2
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#       "interface GigabitEthernet1",
#       "no bfd local-address 10.0.0.1",
#       "no bfd interval 57 min_rx 66 multiplier 45",
#       "interface GigabitEthernet2",
#       "no bfd template OLD_TEMPLATE"
#     ]

# After state:
# ------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

# Using state: gathered

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd local-address 10.0.0.1
#  bfd interval 57 min_rx 66 multiplier 45
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd template OLD_TEMPLATE
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

- name: Gather listed BFD interfaces config
  cisco.ios.ios_bfd_interfaces:
    state: gathered

# Module Execution Result:
# ------------------------

# "gathered": [
#     {
#         "name": "GigabitEthernet1",
#         "local_address": "10.0.0.1",
#         "interval": {
#             "input": 57,
#             "min_rx": 66,
#             "multiplier": 45
#         }
#     },
#     {
#         "name": "GigabitEthernet2",
#         "template": "OLD_TEMPLATE"
#     },
#     {
#         "name": "GigabitEthernet3",
#         "jitter": true,
#         "local_address": "10.0.1.2",
#         "interval": {
#             "input": 50,
#             "min_rx": 50,
#             "multiplier": 3
#         }
#     }
# ]

# After state:
# -------------

# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd local-address 10.0.0.1
#  bfd interval 57 min_rx 66 multiplier 45
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd template OLD_TEMPLATE
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

# Using state: rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_bfd_interfaces:
    config:
      - name: GigabitEthernet1
        local_address: 10.0.0.1
        interval:
          input: 57
          min_rx: 66
          multiplier: 45
      - name: GigabitEthernet2
        template: OLD_TEMPLATE
      - name: GigabitEthernet3
        jitter: true
        local_address: 10.0.1.2
        interval:
          input: 50
          min_rx: 50
          multiplier: 3
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#     "interface GigabitEthernet1",
#     "bfd local-address 10.0.0.1",
#     "bfd interval 57 min_rx 66 multiplier 45",
#     "interface GigabitEthernet2",
#     "bfd template OLD_TEMPLATE",
#     "interface GigabitEthernet3",
#     "bfd jitter",
#     "bfd local-address 10.0.1.2",
#     "bfd interval 50 min_rx 50 multiplier 3"
# ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# interface GigabitEthernet1
#  description Ansible UT interface 1
#  no shutdown
#  bfd local-address 10.0.0.1
#  bfd interval 57 min_rx 66 multiplier 45
# interface GigabitEthernet2
#  description Ansible UT interface 2
#  ip address dhcp
#  bfd template OLD_TEMPLATE
# interface GigabitEthernet3
#  description Ansible UT interface 3
#  no ip address
#  shutdown
#  no bfd jitter
#  bfd local-address 10.0.1.2
#  bfd interval 50 min_rx 50 multiplier 3

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_bfd_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------

# "parsed": [
#     {
#         "name": "GigabitEthernet1",
#         "local_address": "10.0.0.1",
#         "interval": {
#             "input": 57,
#             "min_rx": 66,
#             "multiplier": 45
#         }
#     },
#     {
#         "name": "GigabitEthernet2",
#         "template": "OLD_TEMPLATE"
#     },
#     {
#         "name": "GigabitEthernet3",
#         "jitter": false,
#         "local_address": "10.0.1.2",
#         "interval": {
#             "input": 50,
#             "min_rx": 50,
#             "multiplier": 3
#         }
#     }
# ]
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - interface GigabitEthernet0/2
    - no bfd jitter
    - bfd interval 100 min_rx 100 multiplier 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet0/2
    - bfd echo
    - bfd jitter
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_interfaces.bfd_interfaces import (
    Bfd_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bfd_interfaces.bfd_interfaces import (
    Bfd_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_interfacesArgs.argument_spec,
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

    result = Bfd_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
