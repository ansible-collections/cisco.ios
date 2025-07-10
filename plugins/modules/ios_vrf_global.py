#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vrf_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_vrf_global
short_description: Resource module to configure global VRF definitions.
description: This module provides declarative management of VRF definitions on Cisco IOS.
version_added: 8.0.0
author: Ruchi Pakhle (@Ruchip16)
notes:
  - Tested against Cisco IOS-XE version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary containing device configurations for VRF, including a list of VRF definitions.
    type: dict
    suboptions:
      vrfs:
        description: List of VRF definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the VRF.
            type: str
            required: true
          description:
            description: VRF specific description
            type: str
          ipv4:
            description: VRF IPv4 configuration
            type: dict
            suboptions:
              multicast:
                description: IPv4 multicast configuration
                type: dict
                suboptions:
                  multitopology:
                    description: Enable multicast-specific topology
                    type: bool
          ipv6:
            description: VRF IPv6 configuration
            type: dict
            suboptions:
              multicast:
                description: IPv6 multicast configuration
                type: dict
                suboptions:
                  multitopology:
                    description:  Enable multicast-specific topology
                    type: bool
          rd:
            description: Specify route distinguisher (RD).
            type: str
          route_target:
            description: Specify target VPN extended configurations.
            type: dict
            suboptions:
              export:
                description:
                  - This option is DEPRECATED and is replaced with exports which
                    accepts list as input.
                type: str
              exports:
                description: Export target-VPN configuration.
                type: list
                elements: str
              import_config:
                description:
                  - This option is DEPRECATED and is replaced with imports which
                    accepts list as input.
                type: str
              imports:
                description: Import target-VPN configuration.
                type: list
                elements: str
              both:
                description:
                  - This option is DEPRECATED and is replaced with both_options which
                    accepts list as input.
                type: str
              both_options:
                description: Both export and import target-VPN configuration.
                type: list
                elements: str
          vnet:
            description: Virtual networking configuration.
            type: dict
            suboptions:
              tag:
                description: Identifier used to tag packets associated with this VNET.
                type: int
          vpn:
            description: Configure vpn-id for the VRF as specified in RFC 2685.
            type: dict
            suboptions:
              id:
                description: Configure vpn-id in RFC 2685 format.
                type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^vrf).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices: [parsed, gathered, deleted, merged, replaced, rendered, overridden, purged]
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
        transforms it into JSON format as per the module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config | section vrf).
        connection to remote host is not required.
      - The state I(deleted) only removes the VRF attributes that this module
        manages and does not negate the VRF completely. Thereby, preserving
        address-family related configurations under VRF context.
      - The state I(purged) removes all the VRF definitions from the
        target device. Use caution with this state.
      - Refer to examples for more details.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# admin#show running-config | section ^vrf

- name: Merge provided configuration with device configuration
  cisco.ios.ios_vrf_global:
    config:
      vrfs:
        - name: VRF2
          description: This is a test VRF for merged state
          ipv4:
            multicast:
              multitopology: true
          ipv6:
            multicast:
              multitopology: true
          rd: "2:3"
          route_target:
            exports: "192.0.2.0:100"
            imports: "192.0.2.3:200"
          vpn:
            id: "2:45"
          vnet:
            tag: 200
    state: merged

# Task output
# -------------
#
# before: {}
#
# commands:
#   - vrf definition VRF2
#   - description This is a test VRF for merged state
#   - ipv4 multicast multitopology
#   - ipv6 multicast multitopology
#   - rd 2:3
#   - route-target export 192.0.2.0:100
#   - route-target import 192.0.2.3:200
#   - vnet tag 200
#   - vpn id 2:45
#
# after:
#   - name: VRF2
#     description: This is a test VRF for merged state
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "2:3"
#     route_target:
#       exports: "192.0.2.0:100"
#       imports: "192.0.2.3:200"
#     vnet:
#       tag: 200
#     vpn:
#       id: "2:45"

# After state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.3:200

# Using replaced

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.3:200

- name: Replace the provided configuration with the existing running configuration
  cisco.ios.ios_vrf_global:
    config:
      vrfs:
        - name: VRF7
          description: VRF7 description
          ipv4:
            multicast:
              multitopology: true
          ipv6:
            multicast:
              multitopology: true
          rd: "7:8"
          route_target:
            exports: "198.51.100.112:500"
            imports: "192.0.2.4:400"
          vpn:
            id: "5:45"
          vnet:
            tag: 300
    state: replaced

# Task Output:
# ------------
#
# before:
#   - name: VRF2
#     description: This is a test VRF for merged state
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "2:3"
#     route_target:
#       exports: "192.0.2.0:100"
#       imports: "192.0.2.3:200"
#     vnet:
#       tag: 200
#     vpn:
#       id: "2:45
#
# commands:
# - vrf definition VRF7
# - description VRF7 description
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 7:8
# - route-target export 198.51.100.112:500
# - route-target import 192.0.2.4:400
# - vnet tag 300
# - vpn id 5:45
#
# after:
#   - name: VRF2
#     description: This is a test VRF for merged state
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "2:3"
#     route_target:
#       exports: "192.0.2.0:100"
#       imports: "192.0.2.3:200"
#     vnet:
#       tag: 200
#     vpn:
#       id: "2:45
#   - name: VRF7
#     description: VRF7 description
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "7:8"
#     route_target:
#       exports: "198.51.100.112:500"
#       imports: "192.0.2.4:400"
#     vnet:
#       tag: 300
#     vpn:
#       id: "5:45"
#
# After state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.3:200
# vrf definition VRF7
#  vnet tag 300
#  description VRF7 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 7:8
#  route-target export 198.51.100.112:500
#  route-target import 192.0.2.4:400
#  vpn id 5:45

# Using Overridden

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.3:200
# vrf definition VRF7
#  vnet tag 300
#  description VRF7 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 7:8
#  route-target export 198.51.100.112:500
#  route-target import 192.0.2.4:400
#  vpn id 5:45

- name: Override the provided configuration with the existing running configuration
  cisco.ios.ios_vrf_global:
    config:
      vrfs:
        - name: VRF6
          description: VRF6 description
          ipv4:
            multicast:
              multitopology: true
          ipv6:
            multicast:
              multitopology: true
          rd: "6:7"
          route_target:
            exports: "198.51.0.2:400"
            imports: "198.51.0.5:200"
          vpn:
            id: "4:5"
          vnet:
            tag: 500
    state: overridden

# Task Output:
# ------------
#
# before:
#   - name: VRF2
#     description: This is a test VRF for merged state
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "2:3"
#     route_target:
#       exports: "192.0.2.0:100"
#       imports: "192.0.2.3:200"
#     vnet:
#       tag: 200
#     vpn:
#       id: "2:45
#   - name: VRF7
#     description: VRF7 description
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "7:8"
#     route_target:
#       exports: "198.51.100.112:500"
#       imports: "192.0.2.4:400"
#     vnet:
#       tag: 300
#     vpn:
#       id: "5:45"
#
# commands:
# - vrf definition VRF2
# - no description This is a test VRF for merged state
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 2:3
# - no route-target export 192.0.2.0:100
# - no route-target import 192.0.2.3:200
# - no vnet tag 200
# - no vpn id 2:45
# - vrf definition VRF7
# - no description VRF7 description
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 7:8
# - no route-target export 198.51.100.112:500
# - no route-target import 192.0.2.4:400
# - no vnet tag 300
# - no vpn id 5:45
# - vrf definition VRF6
# - description VRF6 description
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 6:7
# - route-target export 198.51.0.2:400
# - route-target import 198.51.0.5:200
# - vnet tag 500
# - vpn id 4:5
#
# after:
#   - name: VRF2
#   - name: VRF6
#     description: VRF6 description
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "6:7"
#     route_target:
#       exports: "198.51.0.2:400"
#       imports: "198.51.0.5:200"
#     vnet:
#       tag: 500
#     vpn:
#       id: "4:5
#   - name: VRF7

# After state:
# ------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
#  vnet tag 500
#  description VRF6 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 6:7
#  vpn id 4:5
#  route-target export 198.51.0.2:400
#  route-target import 198.51.0.5:200
# vrf definition VRF7

# Using Deleted

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
#  vnet tag 500
#  description VRF6 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 6:7
#  vpn id 4:5
#  route-target export 198.51.0.2:400
#  route-target import 198.51.0.5:200
# vrf definition VRF7

- name: Delete the provided configuration when config is given
  cisco.ios.ios_vrf_global:
    config:
      vrfs:
        - name: VRF2
        - name: VRF6
        - name: VRF7
    state: deleted

# Task Output:
# ------------
#
# before:
#   - name: VRF2
#   - name: VRF6
#     description: VRF6 description
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "6:7"
#     route_target:
#       exports: "198.51.0.2:400"
#       imports: "198.51.0.5:200"
#     vnet:
#       tag: 500
#     vpn:
#       id: "4:5"
#   - name: VRF7
#
# commands:
# - vrf definition VRF2
# - vrf definition VRF6
# - no description VRF6 description
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 6:7
# - no route-target export 198.51.0.2:400
# - no route-target import 198.51.0.5:200
# - no vnet tag 500
# - no vpn id 4:5
# - vrf definition VRF7
#
# after:
#   - name: VRF2
#   - name: VRF6
#   - name: VRF7

# After state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
# vrf definition VRF7

# Using Deleted with empty config

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
#  vnet tag 500
#  description VRF6 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 6:7
#  vpn id 4:5
#  route-target export 198.51.0.2:400
#  route-target import 198.51.0.5:200
# vrf definition VRF7

- name: Delete the provided configuration when config is empty
  cisco.ios.ios_vrf_global:
    config:
    state: deleted

# Task Output:
# ------------
#
# before:
#   - name: VRF2
#   - name: VRF6
#     description: VRF6 description
#     ipv4:
#       multicast:
#         multitopology: true
#     ipv6:
#       multicast:
#         multitopology: true
#     rd: "6:7"
#     route_target:
#       exports: "198.51.0.2:400"
#       imports: "198.51.0.5:200"
#     vnet:
#       tag: 500
#     vpn:
#       id: "4:5"
#   - name: VRF7

# commands:
# - vrf definition VRF2
# - vrf definition VRF6
# - no description VRF6 description
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 6:7
# - no route-target export 198.51.0.2:400
# - no route-target import 198.51.0.5:200
# - no vnet tag 500
# - no vpn id 4:5
# - vrf definition VRF7
#
# after:
#   - name: VRF2
#   - name: VRF6
#   - name: VRF7

# After state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
# vrf definition VRF7

# Using purged - would delete all the VRF definitions

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
# vrf definition VRF7

- name: Purge all the configuration from the device
  cisco.ios.ios_vrf_global:
    state: purged

# Task Output:
# ------------
#
# before:
#   - name: VRF2
#   - name: VRF6
#   - name: VRF7
# commands:
# - no vrf definition VRF2
# - no vrf definition VRF6
# - no vrf definition VRF7
# after: {}

# After state:
# -------------
#
# admin#show running-config | section ^vrf

# Using Rendered

- name: Render provided configuration with device configuration
  cisco.ios.ios_vrf_global:
    config:
      vrfs:
        - name: VRF2
          description: This is a test VRF for merged state
          ipv4:
            multicast:
              multitopology: true
          ipv6:
            multicast:
              multitopology: true
          rd: "2:3"
          route_target:
            exports: "192.0.2.0:100"
            imports: "192.0.2.3:200"
          vpn:
            id: "2:45"
          vnet:
            tag: 200
    state: rendered

# Task Output:
# ------------
#
# rendered:
# - vrf definition VRF2
# - description This is a test VRF for merged state
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 2:3
# - route-target export 192.0.2.0:100
# - route-target import 192.0.2.3:200
# - vnet tag 200
# - vpn id 2:45

# Using Gathered

# Before state:
# -------------
#
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.3:200

- name: Gather existing running configuration
  cisco.ios.ios_vrf_global:
    config:
    state: gathered

# Task Output:
# ------------
#
# gathered:
#   vrfs:
#     - name: VRF2
#       description: This is a test VRF for merged state
#       ipv4:
#         multicast:
#           multitopology: true
#       ipv6:
#         multicast:
#           multitopology: true
#       rd: "2:3"
#       route_target:
#         exports: "192.0.2.0:100"
#         imports: "192.0.2.3:200"
#       vnet:
#         tag: 200
#       vpn:
#         id: "2:45"

# Using parsed

# File: parsed.cfg
# ----------------
#
# vrf definition test
#  vnet tag 34
#  description This is test VRF
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 192.0.2.0:300
#  vpn id 3:4
#  route-target export 192.0.2.0:100
#  route-target import 192.0.2.2:300
# vrf definition test2
#  vnet tag 35
#  description This is test VRF
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 192.0.2.3:300

- name: Parse the provided configuration
  cisco.ios.ios_vrf_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
#
# parsed:
#   vrfs:
#     - name: test
#       description: This is test VRF
#       ipv4:
#         multicast:
#           multitopology: true
#       ipv6:
#         multicast:
#           multitopology: true
#       rd: "192.0.2.0:300"
#       route_target:
#         exports: "192.0.2.0:100"
#         imports: "192.0.2.2:300"
#       vnet:
#         tag: 34
#       vpn:
#         id: "3:4"
#     - name: test2
#       description: This is test VRF
#       ipv4:
#         multicast:
#           multitopology: true
#       ipv6:
#         multicast:
#           multitopology: true
#       rd: "192.0.2.3:300"
#       vnet:
#         tag: 35
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
    - "vrf definition test"
    - "description This is a test VRF"
    - "rd: 2:3"
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - "vrf definition management"
    - "description This is a test VRF"
    - "rd: 2:3"
    - "route-target export 190.0.2.3:400"
    - "route-target import 190.0.2.1:300"
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_global.vrf_global import (
    Vrf_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vrf_global.vrf_global import (
    Vrf_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vrf_globalArgs.argument_spec,
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

    result = Vrf_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
