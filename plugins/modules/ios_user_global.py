#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_user_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_user_global
short_description: Resource module to configure user and enable
description:
  - This module provides declarative management of user and enable on Cisco IOS devices
version_added: 4.7.0
author:
  - Ambroise Rosset (@earendilfr)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
options:
  config:
    description: A dictionary of user and enable options
    type: dict
    suboptions:
      enable:
        description: A dictionary of options for enable password
        elements: dict
        suboptions:
          password:
            description:
              - Define the password or secret for enable role (MAX of 25 characters)
            type: dict
            suboptions:
              type:
                description:
                  - Choose the type of password
                  - I(password) for the old reversible algorythn
                  - I(secret) to use the more recent and secure algorithm
                choices:
                  - password
                  - secret
                default: secret
                type: str
              hash:
                description:
                  - Specifies the type of hash used in password provided
                  - C(0) - UNENCRYPTED password (I(Default))
                  - C(5) - MD5 HASHED secret
                  - C(6) - ENCRYPTED password (require a crypto-key on device)
                  - C(7) - HIDDEN password
                  - C(8) - PBKDF2 HASHED secret
                  - C(9) - SCRYPT HASHED secret
                choices: [ 0, 5, 6, 7, 8, 9 ]
                default: 0
                type: int
              value:
                description:
                  - The actual hashed password to be configured on the device
                  - The password should be complient with the C(hash) parameter choose
                    previously
                type: str
                required: true
          level:
            description:
              - Set exec level password
              - The I(level) valu should be between C(1) and C(15)
            type: int
        type: list
      users:
        description: Define a user
        elements: dict
        suboptions:
          name:
            description:
              - The name of the user
            type: str
            required: true
          description:
            description:
              - Add description to MAC user (MAX of 128 characters)
            type: str
          password:
            description:
              -  Define the password or secret for user (MAX of 25 characters)
            type: dict
            suboptions:
              type:
                description:
                  - Choose the type of password
                  - I(password) for the old reversible algorythn
                  - I(secret) to use the more recent and secure algorithm
                choices:
                  - password
                  - secret
                default: secret
                type: str
              hash:
                description:
                  - Specifies the type of hash used in password provided
                  - C(0) - UNENCRYPTED password (I(Default))
                  - C(5) - MD5 HASHED secret
                  - C(6) - ENCRYPTED password (require a crypto-key on device)
                  - C(7) - HIDDEN password
                  - C(8) - PBKDF2 HASHED secret
                  - C(9) - SCRYPT HASHED secret
                choices: [ 0, 5, 6, 7, 8, 9 ]
                default: 0
                type: int
              value:
                description:
                  - The actual hashed password to be configured on the device
                  - The password should be complient with the C(hash) parameter choose
                    previously
                type: str
                required: true
          privilege:
            description:
              - Set user privilege level
              - The I(privilege) value should be between C(1) and C(15)
            type: int
        type: list
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^username|^enable).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
      - merged
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
        option should be the same format as the output of command
        I(show running-config | section ^username|^enable) executed on device. For state I(parsed)
        active connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section ^username|^enable
# --------------------- EMPTY -----------------

# Merged play:
# ------------

- name: Apply the provided configuration
  cisco.ios.ios_user_global:
    config:
      enable:
        - password:
            hash: 0
            type: myenablepassword
      users:
        - name: johndoe
          privilege: 15
          password:
            hash: 0
            type: johndoepwd
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#         "enable secret 0 myenablepassword",
#         "username johndoe privilege 15 secret 0 johndoepwd",
# ],

# After state:
# ------------

# router-ios#show running-config | section ^username|^enable
# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username johndoe privilege 15 secret 9 $9$mUv1uo8NTi0u/U$1bu/NzyGL37xR0oLq0hCWXE1tVlZ97BILpo9aswAykQ

# Using state: deleted

# router-ios#show running-config | section ^username|^enable
# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg
# username johndoe privilege 15 secret 9 $9$mUv1uo8NTi0u/U$1bu/NzyGL37xR0oLq0hCWXE1tVlZ97BILpo9aswAykQ

# Deleted play:
# -------------

- name: Remove all existing configuration
  cisco.ios.ios_user_global:
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#         "no enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
#         "no username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
#         "no username johndoe privilege 15 secret 9 $9$mUv1uo8NTi0u/U$1bu/NzyGL37xR0oLq0hCWXE1tVlZ97BILpo9aswAykQ",
# ]

# After state:
# ------------

# router-ios#show running-config | section ^username|^enable
# --------------------- EMPTY -----------------

# Using state: replaced

# Before state:
# -------------

# router-ios#show running-config | section ^username|^enable
# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username johndoe privilege 15 secret 9 $9$mUv1uo8NTi0u/U$1bu/NzyGL37xR0oLq0hCWXE1tVlZ97BILpo9aswAykQ

# Overridden play:
# --------------

- name: Override commands with provided configuration
  cisco.ios.ios_user_global:
    config:
      enable:
        - password:
            type: secret
            hash: 9
            value: "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo"
      users:
        - name: admin
          privilege: 15
          password:
            type: secret
            hash: 9
            value: "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg"
    state: overridden

# Commands Fired:
# ---------------
# "commands": [
#         "no username johndoe privilege 15 secret 9 $9$mUv1uo8NTi0u/U$1bu/NzyGL37xR0oLq0hCWXE1tVlZ97BILpo9aswAykQ",
#         "username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
# ]

# After state:
# ------------

# router-ios#show running-config | section ^username|^enable
# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg

# Using state: gathered

# Before state:
# -------------

# router-ios#show running-config | section ^username|^enable
# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg

# Gathered play:
# --------------

- name: Gather listed snmp config
  cisco.ios.ios_user_global:
    state: gathered

# Module Execution Result:
# ------------------------

#   "gathered": {
#        "enable": [
#           {
#               "password": {
#                   "type": "secret",
#                   "hash": 9,
#                   "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
#               },
#           },
#        ],
#        "users": [
#            {
#                "name": "admin",
#                "password": {
#                    "type": "secret",
#                    "hash": 9,
#                    "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
#                },
#            },
#        ],
#   }

# Using state: rendered

# Rendered play:
# --------------

- name: Render the commands for provided configuration
  cisco.ios.ios_user_global:
    config:
      enable:
        - password:
            type: secret
            hash: 9
            value: "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo"
      users:
        - name: admin
          privilege: 15
          password:
            type: secret
            hash: 9
            value: "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg"
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#     "enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo"
#     "username admin privilege 15 secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
# ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
# username admin privilege 15 secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg

# Parsed play:
# ------------

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_user_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------

# "parsed": {
#     "enable": [
#         {
#             "password": {
#                 "type": "secret",
#                 "hash": 9,
#                 "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
#             },
#         },
#     ],
#     "users": [
#         {
#             "name": "admin",
#             "privilege": 15,
#             "password": {
#                 "type": "secret",
#                 "hash": 9,
#                 "value: "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
#             },
#         },
#     ],
# }
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.user_global.user_global import (
    User_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.user_global.user_global import (
    User_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=User_globalArgs.argument_spec,
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

    result = User_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
