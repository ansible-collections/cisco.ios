#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_templates
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bfd_templates
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Bidirectional Forwarding Detection (BFD) templates configurations
description:
   - Manages Bidirectional Forwarding Detection (BFD) templates configurations
version_added: 11.3.0
author:
  - Komal Desai (@komaldesai13)
notes:
  - Tested against Cisco IOS XE Software, Version 17.13.01a on CML
  - This module works with connection C(network_cli)
options:
  config:
    description: A dictionary of bfd template options
    type: list
    elements: dict
    suboptions:
      name:
        description: name of the BFD template to be used
        required: true
        type: str
      hop:
        description: type of template to be used
        required: true
        choices:
          - single_hop
          - multi_hop
        type: str
      interval:
        description: defines transmit interval between BFD packets
        type: dict
        suboptions:
          min_tx:
            description: The minimum interval in milliseconds that the local system desires for transmitting BFD control packets
            type: int
          min_rx:
            description: The minimum interval in milliseconds that the local system is capable of supporting between received BFD control packets
            type: int
          multiplier:
            description: Specifies the number of consecutive BFD control packets that must be missed from a BFD peer before BFD declares\
                         that the peer is unavailable and the Layer 3 BFD peer is informed of the failure.
            type: int
      dampening:
        description: enables session dampening
        type: dict
        suboptions:
          half_life_period:
            description: half-life period for the exponential decay algorithm, in minutes.
            type: int
          reuse_threshold:
            description: The threshold at which a dampened session is allowed to be reused (taken out of dampening), in milliseconds.
            type: int
          suppress_threshold:
            description: The threshold at which a session is suppressed (put into dampening), in milliseconds.
            type: int
          max_suppress_time:
            description: The maximum amount of time a session can be suppressed, in minutes.
            type: int
      echo:
        description: enables the BFD echo function for all interfaces which uses this specific template.
        type: bool
      authentication:
        description: Configure authentication for the BFD template
        type: dict
        suboptions:
          type:
            description: Authentication type to use for BFD sessions
            type: str
            choices:
              - sha_1
              - md5
              - meticulous_md5
              - meticulous_sha_1
          keychain:
            description: Name of the key chain to use for authentication
            type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^bfd-template).
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
        | section ^bfd-template) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state C(deleted) does not support or guarantee granular deletion of configuration
        the playbook should act as source of truth, and the desired state of the resouce is what
        the playbook should reflect. Use C(overridden) or C(replaced) to get extra configuration
        removed.
      - The state I(purged) removes BFD templates completely using a single top-level
        C(no bfd-template) command, which removes the entire template definition at once.
    type: str
"""

EXAMPLES = """
# Using merged
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# (no BFD templates configured)

- name: Merge provided configuration with device configuration
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
        interval:
          min_tx: 200
          min_rx: 200
          multiplier: 3
        authentication:
          type: sha_1
          keychain: bfd_keychain
        echo: true
      - name: template2
        hop: multi_hop
        interval:
          min_tx: 500
          min_rx: 500
          multiplier: 5
        dampening:
          half_life_period: 30
          reuse_threshold: 2000
          suppress_threshold: 5000
          max_suppress_time: 120
    state: merged

# Commands Fired:
# ---------------
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
#  authentication sha-1 keychain bfd_keychain
#  echo
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5
#  dampening 30 2000 5000 120

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
#  authentication sha-1 keychain bfd_keychain
#  echo
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5
#  dampening 30 2000 5000 120

# Using replaced
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
#  authentication sha-1 keychain bfd_keychain
#  echo
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

- name: Replace device configuration of specified BFD templates with provided configuration
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
        interval:
          min_tx: 300
          min_rx: 300
          multiplier: 4
        authentication:
          type: sha_1
          keychain: new_keychain
    state: replaced

# Commands Fired:
# ---------------
# bfd-template single-hop template1
#  no echo
#  interval min-tx 300 min-rx 300 multiplier 4
#  no authentication sha-1 keychain bfd_keychain
#  authentication sha-1 keychain new_keychain

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 300 min-rx 300 multiplier 4
#  authentication sha-1 keychain new_keychain
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

# Using overridden
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5
# bfd-template single-hop template3
#  echo

- name: Override device configuration with provided configuration
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
        interval:
          min_tx: 300
          min_rx: 300
          multiplier: 5
        authentication:
          type: md5
          keychain: secure_key
    state: overridden

# Commands Fired:
# ---------------
# no bfd-template multi-hop template2
# no bfd-template single-hop template3
# bfd-template single-hop template1
#  interval min-tx 300 min-rx 300 multiplier 5
#  authentication md5 keychain secure_key

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 300 min-rx 300 multiplier 5
#  authentication md5 keychain secure_key

# Using deleted
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
#  authentication sha-1 keychain bfd_keychain
#  echo
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

- name: Delete specified BFD template
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
    state: deleted

# Commands Fired:
# ---------------
# bfd-template single-hop template1
#  no echo
#  no interval min-tx 200 min-rx 200 multiplier 3
#  no authentication sha-1 keychain bfd_keychain

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

# Using deleted (to delete all BFD templates )
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

- name: Delete all BFD template configurations
  cisco.ios.ios_bfd_templates:
    state: deleted

# Commands Fired:
# ---------------
# bfd-template single-hop template1
#  no interval min-tx 200 min-rx 200 multiplier 3
# bfd-template multi-hop template2
#  no interval min-tx 500 min-rx 500 multiplier 5

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
# bfd-template multi-hop template2

# Using purged
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

- name: Purge specified BFD template configurations (complete removal)
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
    state: purged

# Commands Fired:
# ---------------
# no bfd-template single-hop template1

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5

# Using purged (to remove all BFD templates)
# Before state:
# -------------
# router-ios#show running-config | section ^bfd-template
# bfd-template single-hop template1
#  interval min-tx 200 min-rx 200 multiplier 3
#  authentication sha-1 keychain bfd_keychain
# bfd-template multi-hop template2
#  interval min-tx 500 min-rx 500 multiplier 5
# bfd-template single-hop template3
#  echo

- name: Purge all BFD template configurations (complete removal)
  cisco.ios.ios_bfd_templates:
    config: []
    state: purged

# Commands Fired:
# ---------------
# no bfd-template single-hop template1
# no bfd-template multi-hop template2
# no bfd-template single-hop template3

# After state:
# ------------
# router-ios#show running-config | section ^bfd-template
# (no BFD templates configured)

# Using rendered
- name: Render platform specific commands from task input using rendered state
  cisco.ios.ios_bfd_templates:
    config:
      - name: template1
        hop: single_hop
        interval:
          min_tx: 200
          min_rx: 200
          multiplier: 3
        authentication:
          type: meticulous_sha_1
          keychain: secure_chain
        echo: true
    state: rendered

# Module Execution Result:
# ------------------------
# "rendered": [
#     "bfd-template single-hop template1",
#     "interval min-tx 200 min-rx 200 multiplier 3",
#     "authentication meticulous-sha-1 keychain secure_chain",
#     "echo"
# ]

# Using gathered
- name: Gather BFD template configuration from the device
  cisco.ios.ios_bfd_templates:
    state: gathered

# Module Execution Result:
# ------------------------
# "gathered": [
#     {
#         "name": "template1",
#         "hop": "single_hop",
#         "interval": {
#             "min_tx": 200,
#             "min_rx": 200,
#             "multiplier": 3
#         },
#         "authentication": {
#             "type": "sha_1",
#             "keychain": "bfd_keychain"
#         },
#         "echo": true
#     }
# ]

# Using parsed
- name: Parse the provided configuration to structured format
  cisco.ios.ios_bfd_templates:
    running_config: |
      bfd-template single-hop template1
       interval min-tx 200 min-rx 200 multiplier 3
       authentication sha-1 keychain bfd_keychain
       echo
      bfd-template multi-hop template2
       dampening 30 2000 5000 120
    state: parsed

# Module Execution Result:
# ------------------------
# "parsed": [
#     {
#         "name": "template1",
#         "hop": "single_hop",
#         "interval": {
#             "min_tx": 200,
#             "min_rx": 200,
#             "multiplier": 3
#         },
#         "authentication": {
#             "type": "sha_1",
#             "keychain": "bfd_keychain"
#         },
#         "echo": true
#     },
#     {
#         "name": "template2",
#         "hop": "multi_hop",
#         "dampening": {
#             "half_life_period": 30,
#             "reuse_threshold": 2000,
#             "suppress_threshold": 5000,
#             "max_suppress_time": 120
#         }
#     }
# ]
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
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
  returned: always
  type: list
  sample:
    - bfd-template single-hop template1
    - interval min-tx 200 min-rx 200 multiplier 3
    - authentication sha-1 keychain bfd_keychain
    - echo
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - bfd-template single-hop template1
    - interval min-tx 200 min-rx 200 multiplier 3
    - authentication sha-1 keychain bfd_keychain
    - echo
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_templates.bfd_templates import (
    Bfd_templatesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bfd_templates.bfd_templates import (
    Bfd_templates,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_templatesArgs.argument_spec,
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

    result = Bfd_templates(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
