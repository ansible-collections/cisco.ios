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
                description: IP Multicast configuration
                type: dict
                suboptions:
                  multitopology:
                    description:  Enable Multicast-Specific RPF Topology
                    type: bool
          ipv6:
            description: VRF IPv6 configuration
            type: dict
            suboptions:
              multicast:
                description: IP Multicast configuration
                type: dict
                suboptions:
                  multitopology:
                    description:  Enable Multicast-Specific RPF Topology
                    type: bool
          rd:
            description: Specify Route Distinguisher (RD).
            type: str
          route_target:
            description: Specify Target VPN Extended Communities.
            type: dict
            suboptions:
              export:
                description: Export Target-VPN community.
                type: str
              import_config:
                description: Export Target-VPN community.
                type: str
              both:
                description: Both export and import Target-VPN community
                type: str
          vnet:
            description: Virtual NETworking configuration.
            type: dict
            suboptions:
              tag:
                description: Identifier used to tag packets associated with this VNET
                type: int
          vpn:
            description: Configure VPN ID for the VRF as specified in RFC 2685
            type: dict
            suboptions:
              id:
                description: Configure VPN ID in RFC 2685 format
                type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config vrf).
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
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(sh running-config | section vrf).
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using merged
# Before state:
# -------------
# admin#show running-config | section ^vrf
#
- name: Merge provided configuration with device configuration
  hosts: ios
  gather_facts: false
  tasks:
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
                export: "23.1.3.4:400"
                import_config: "10.1.3.4:400"
              vpn:
                id: "2:45"
              vnet:
                tag: 200
        state: merged
# Task output
# -------------
# commands:
# - vrf definition VRF2
# - description This is a test VRF for merged state
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 2:3
# - route-target export 23.1.3.4:400
# - route-target import 10.1.3.4:400
# - vnet tag 200
# - vpn id 2:45
#
#
# after:
#   name: VRF2
#   description: This is a test VRF for merged state
#   ipv4:
#     multicast:
#       multitopology: true
#   ipv6:
#     multicast:
#       multitopology: true
#   rd: "2:3"
#   route_target:
#     export: "23.1.3.4:400"
#     import_config: "10.1.3.4:400"
#   vnet:
#     tag: 200
#   vpn:
#     id: "2:45"
#
# After state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 23.1.3.4:400
#  route-target import 10.1.3.4:400

#
# Using replaced
# Before state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 23.1.3.4:400
#  route-target import 10.1.3.4:400
#
#
- name: Replace the provided configuration with the existing running configuration
  hosts: ios
  gather_facts: false
  tasks:
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
                export: "23.1.3.4:500"
                import_config: "12.1.3.4:400"
              vpn:
                id: "2:45"
              vnet:
                tag: 300
        state: replaced

# -------------
# commands:
# - vrf definition VRF7
# - description VRF7 description
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 7:8
# - route-target export 23.1.3.4:500
# - route-target import 12.1.3.4:400
# - vnet tag 300
# - vpn id 2:45
#
# after:
#   name: VRF2
#   description: This is a test VRF for merged state
#   ipv4:
#     multicast:
#       multitopology: true
#   ipv6:
#     multicast:
#       multitopology: true
#   rd: "2:3"
#   route_target:
#     export: "23.1.3.4:400"
#     import_config: "10.1.3.4:400"
#   vnet:
#     tag: 200
#   vpn:
#     id: "2:45
#   name: VRF7
#   description: VRF7 description
#   ipv4:
#     multicast:
#       multitopology: true
#   ipv6:
#     multicast:
#       multitopology: true
#   rd: "7:8"
#   route_target:
#     export: "23.1.3.4:500"
#     import_config: "12.1.3.4:400"
#   vnet:
#     tag: 300
#   vpn:
#     id: "2:45"
#
# After state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 23.1.3.4:400
#  route-target import 10.1.3.4:400
# vrf definition VRF7
#  vnet tag 300
#  description VRF7 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 7:8
#  route-target export 23.1.3.4:500
#  route-target import 12.1.3.4:400

#
# Using overridden
# Before state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
#  vnet tag 200
#  description This is a test VRF for merged state
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 2:3
#  vpn id 2:45
#  route-target export 23.1.3.4:400
#  route-target import 10.1.3.4:400
# vrf definition VRF7
#  vnet tag 300
#  description VRF7 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 7:8
#  route-target export 23.1.3.4:500
#  route-target import 12.1.3.4:400

- name: Override the provided configuration with the existing running configuration
  hosts: ios
  gather_facts: false
  tasks:
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
                export: "3.1.3.4:400"
                import_config: "1.12.3.4:200"
              vpn:
                id: "4:5"
              vnet:
                tag: 500
        state: overridden

# Task output
# -------------
# commands:
# - vrf definition VRF2
# - no description This is a test VRF for merged state
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 2:3
# - no route-target export 23.1.3.4:400
# - no route-target import 10.1.3.4:400
# - no vnet tag 200
# - no vpn id 2:45
# - vrf definition VRF7
# - no description VRF7 description
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 7:8
# - no route-target export 23.1.3.4:500
# - no route-target import 12.1.3.4:400
# - no vnet tag 300
# - vrf definition VRF6
# - description VRF6 description
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 6:7
# - route-target export 3.1.3.4:400
# - route-target import 1.12.3.4:200
# - vnet tag 500
# - vpn id 4:5
#
# After state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
#  vnet tag 500
#  description VRF6 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 6:7
#  vpn id 4:5
#  route-target export 3.1.3.4:400
#  route-target import 1.12.3.4:200
# vrf definition VRF7
#
#
# Using deleted
# Before state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
#  vnet tag 500
#  description VRF6 description
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 6:7
#  vpn id 4:5
#  route-target export 3.1.3.4:400
#  route-target import 1.12.3.4:200
# vrf definition VRF7
#
- name: Delete the provided configuration
  hosts: ios
  gather_facts: false
  tasks:
    - name: Delete the provided configuration
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF2
            - name: VRF6
            - name: VRF7
        state: deleted
# Task output
# -------------
# commands:
# - vrf definition VRF2
# - vrf definition VRF6
# - no description VRF6 description
# - no ipv4 multicast multitopology
# - no ipv6 multicast multitopology
# - no rd 6:7
# - no route-target export 3.1.3.4:400
# - no route-target import 1.12.3.4:200
# - no vnet tag 500
# - no vpn id 4:5
# - vrf definition VRF7
#
# After state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
# vrf definition VRF7
#
# Using purged
# Before state:
# -------------
# admin#show running-config | section ^vrf
# vrf definition VRF2
# vrf definition VRF6
# vrf definition VRF7
#
- name: Purge all the configuration from the device
  hosts: ios
  gather_facts: false
  tasks:
    - name: Purge all the configuration from the device
      cisco.ios.ios_vrf_global:
        state: purged
# Task output
# -------------
# commands:
# - no vrf definition VRF2
# - no vrf definition VRF6
# - no vrf definition VRF7
#
# After state:
# -------------
# admin#show running-config | section ^vrf
# -
#
# Using rendered
# ----------------
- name: Render provided configuration with device configuration
  hosts: ios
  gather_facts: false
  tasks:
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
                export: "23.1.3.4:400"
                import_config: "10.1.3.4:400"
              vpn:
                id: "2:45"
              vnet:
                tag: 200
        state: rendered

# Task output
# -------------
# commands:
# - vrf definition VRF2
# - description This is a test VRF for merged state
# - ipv4 multicast multitopology
# - ipv6 multicast multitopology
# - rd 2:3
# - route-target export 23.1.3.4:400
# - route-target import 10.1.3.4:400
# - vnet tag 200
# - vpn id 2:45
#
# Using gathered
# -------------
- name: Display existing running configuration
  hosts: ios
  gather_facts: false
  tasks:
    - name: Gather existing running configuration
      cisco.ios.ios_vrf_global:
        state: gathered

# gathered:
#
# name: VRF2
# name: VRF6
# name: VRF7
#
# Using parsed
#
# parsed.cfg
# ------------
# vrf definition test
#  vnet tag 34
#  description This is test VRF
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 10.2.3.4:300
#  vpn id 3:4
#  route-target export 23.1.3.4:400
#  route-target import 123.3.4.5:700
# vrf definition test2
#  vnet tag 35
#  description This is test VRF
#  ipv4 multicast multitopology
#  ipv6 multicast multitopology
#  rd 1.2.3.4:500
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
