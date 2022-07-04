#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_hostname
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_hostname
short_description: Resource module to configure hostname.
description:
- This module provides declarative management of hostname on Cisco IOS devices.
version_added: 2.7.0
author:
- Sagar Paul (@KB-perByte)
notes:
- Tested against Cisco IOSv Version 15.6.
- This module works with connection C(network_cli).
options:
  config:
    description: A dictionary of hostname options
    type: dict
    suboptions:
      hostname:
        description: set hostname for IOS
        type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^hostname).
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
      - The states I(merged), I(replaced) and I(overridden) have identical
        behaviour for this module.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command
        I(show running-config | section ^hostname) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section ^hostname
# hostname Router

# Merged play:
# ------------

- name: Apply the provided configuration
  cisco.ios.ios_hostname:
    config:
      hostname: Router1
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#         "hostname Router1",
# ],


# After state:
# ------------

# router-ios#show running-config | section ^hostname
# hostname Router1

# Using state: deleted

# Before state:
# -------------

# router-ios#show running-config | section ^hostname
# hostname RouterTest

# Deleted play:
# -------------

- name: Remove all existing configuration
  cisco.ios.ios_hostname:
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#     "no hostname RouterTest",
# ],

# After state:
# ------------

# router-ios#show running-config | section ^hostname
# hostname Router

# Using state: overridden

# Before state:
# -------------

# router-ios#show running-config | section ^hostname
# hostname Router

# Overridden play:
# ----------------

- name: Override commands with provided configuration
  cisco.ios.ios_hostname:
    config:
      hostname: RouterTest
    state: overridden


# Commands Fired:
# ---------------
# "commands": [
#       "hostname RouterTest",
#     ],

# After state:
# ------------

# router-ios#show running-config | section ^hostname
# hostname RouterTest


# Using state: replaced

# Before state:
# -------------

# router-ios#show running-config | section ^hostname
# hostname RouterTest

# Replaced play:
# --------------

- name: Replace commands with provided configuration
  cisco.ios.ios_hostname:
    config:
      hostname: RouterTest
    state: replaced

# Commands Fired:
# ---------------

# "commands": [],

# After state:
# ------------

# router-ios#show running-config | section ^hostname
# hostname RouterTest

# Using state: gathered

# Before state:
# -------------

#router-ios#show running-config | section ^hostname
# hostname RouterTest

# Gathered play:
# --------------

- name: Gather listed hostname config
  cisco.ios.ios_hostname:
    state: gathered

# Module Execution Result:
# ------------------------

#   "gathered": {
#      "hostname": "RouterTest"
#     },

# Using state: rendered

# Rendered play:
# --------------

- name: Render the commands for provided configuration
  cisco.ios.ios_hostname:
    config:
      hostname: RouterTest
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#     "hostname RouterTest",
# ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# hostname RouterTest


# Parsed play:
# ------------

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_hostname:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------

#  "parsed": {
#     "hostname": "RouterTest"
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
    - hostname Router1
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - hostname Switch1
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.hostname.hostname import (
    HostnameArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.hostname.hostname import (
    Hostname,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=HostnameArgs.argument_spec,
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

    result = Hostname(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
