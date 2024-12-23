#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vrf_address_family
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_vrf_address_family
short_description: Resource module to configure VRF definitions.
description: This module provides declarative management of VRF definitions on Cisco IOS.
version_added: 10.0.0
author: Ruchi Pakhle (@Ruchip16)
notes:
  - Tested against Cisco IOSXE version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A list of device configurations for VRF.
    type: list
    elements: dict
    suboptions:
      name:
        description: Name of the VRF.
        type: str
        required: true
      address_families:
        description: Enable address family and enter its config mode - AFI/SAFI configuration
        type: list
        elements: dict
        suboptions:
          afi:
            description: Address Family Identifier (AFI)
            type: str
            choices: ['ipv4', 'ipv6']
          safi:
            description: Address Family modifier
            type: str
            choices: ['multicast', 'unicast']
          bgp: &bgp01
            description: Commands pertaining to BGP configuration.
            type: dict
            suboptions:
              next_hop:
                description: Next-hop for the routes of a VRF in the backbone.
                type: dict
                suboptions:
                  loopback:
                    description: Loopback interface for next-hop
                    type: int
          export: &export
            description: VRF export
            type: dict
            suboptions:
              map:
                description: Route-map name
                type: str
              ipv4:
                description: Address family based VRF export
                type: dict
                suboptions:
                  multicast:
                    description: Export prefixes to IPv4 Multicast table
                    type: dict
                    suboptions:
                      prefix:
                        description: Upper limit on export prefixes without hogging memory
                        type: int
                      map:
                        description: Route-map name
                        type: str
                  unicast:
                    description: Export prefixes to IPv4 Unicast table
                    type: dict
                    suboptions:
                      prefix:
                        description: Upper limit on export prefixes without hogging memory
                        type: int
                      map:
                        description: Route-map name
                        type: str
                      allow_evpn:
                        description: Allow EVPN routes into global table
                        type: bool
          import_config: &import01
            description: VRF import
            type: dict
            suboptions:
              map:
                description: Route-map name
                type: str
              ipv4:
                description: Address family based VRF import
                type: dict
                suboptions:
                  multicast:
                    description: Import prefixes from IPv4 Multicast table
                    type: dict
                    suboptions:
                      prefix:
                        description: Upper limit on import prefixes without hogging memory
                        type: int
                      map:
                        description: Route-map name
                        type: str
                  unicast:
                    description: Import prefixes from IPv4 Unicast table
                    type: dict
                    suboptions:
                      limit:
                        description: Upper limit on import prefixes without hogging memory
                        type: int
                      map:
                        description: Route-map based VRF import
                        type: str
                      allow_evpn:
                        description: allow Global->VRF routes into EVPN
                        type: bool
          maximum: &maximum
            description: Set a limit to a routing table
            type: dict
            suboptions:
              routes:
                description: Maximum number of routes allowed in the routing table
                type: dict
                suboptions:
                  limit:
                    description: Maximum number of routes allowed
                    type: int
                  threshold:
                    description: Threshold value (%) at which to generate a warning msg
                    type: int
                  reinstall:
                    description: Reinstall previous rejected route due to over maximum route limit
                    type: dict
                    suboptions:
                      threshold:
                        description: Threshold value (%) at which to reinstall routes back to VRF
                        type: int
                  warning_only:
                    description: Only give a warning message if limit is exceeded
                    type: bool
          inter_as_hybrid: &inter_as_hybrid
            description: Inter AS hybrid mode
            type: dict
            suboptions:
              csc:
                description: Carrier Supporting Carrier
                type: dict
                suboptions:
                  next_hop: &next_hop
                    description: Next-hop for the routes of a VRF in the backbone.
                    type: str
              next_hop: *next_hop
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
    choices: [parsed, gathered, deleted, merged, replaced, rendered, overridden]
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
        option should be the same format as the output of command I(show running-config vrf).
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# RP/0/0/CPU0:ios#show running-config | section ^vrf
# vrf defnition test
#

- name: Merge provided configuration with device configuration
  cisco.ios.ios_vrf_address_family:
    config:
      - name: test1
        address_families:
          - afi: "ipv4"
            safi: "unicast"
            bgp:
              next_hop:
                loopback: 40
            export:
              ipv4:
                multicast:
                  map: "single"
                  prefix: 345
                unicast:
                  allow_evpn: true
                  map: "test-map"
                  prefix: 67
              map: "testing-map"
            import_config:
              ipv4:
                multicast:
                  map: "import-map"
                  prefix: 89
                unicast:
                  allow_evpn: true
                  limit: 12
                  map: "ran-map"
              map: "import-map"
    state: merged

# Task Output:
# ------------
#
# before: []
#
# commands:
# - vrf definition test1
# - address-family ipv4 unicast
# - bgp next-hop loopback 40
# - export map "testing-map"
# - export ipv4 multicast 345 map "single"
# - export ipv4 unicast 67 map "test-map" allow-evpn
# - import map "import-map"
# - import ipv4 multicast 89 map "import-map"
# - import ipv4 unicast 12 map "ran-map" allow-evpn
#
# after:
# - name: test1
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 40
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 345
#           unicast:
#             allow_evpn: true
#             map: "test-map"
#             prefix: 67
#         map: "testing-map"
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map"
#             prefix: 89
#           unicast:
#             allow_evpn: true
#             limit: 12
#             map: "ran-map"
#       map: "import-map"
#
# After state:
# ------------
#
# RP/0/0/CPU0:ios#show running-config | section ^vrf
# vrf definition test1
#  address-family ipv4 unicast
#   bgp next-hop loopback 40
#   export map "testing-map"
#   export ipv4 multicast 345 map "single"
#   export ipv4 unicast 67 map "test-map" allow-evpn
#   import map "import-map"
#   import ipv4 multicast 89 map "import-map"
#   import ipv4 unicast 12 map "ran-map" allow-evpn

# Using replaced
#
# Before state:
# -------------
#
# RP/0/0/CPU0:ios#show running-config | section ^vrf
# vrf definition test1
#  address-family ipv4 unicast
#   bgp next-hop loopback 40
#   export map "testing-map"
#   export ipv4 multicast 345 map "single"
#   export ipv4 unicast 67 map "test-map" allow-evpn
#   import map "import-map"
#   import ipv4 multicast 89 map "import-map"
#   import ipv4 unicast 12 map "ran-map" allow-evpn

- name: Replace the provided configuration with the existing running configuration
  cisco.ios.ios_vrf_address_family:
    config:
      - name: test1
        address_families:
          - afi: "ipv4"
            safi: "unicast"
            bgp:
              next_hop:
                loopback: 40
            export:
              ipv4:
                multicast:
                  map: "single"
                  prefix: 345
                unicast:
                  allow_evpn: true
                  map: "test-map"
                  prefix: 67
              map: "testing-map"
            import_config:
              ipv4:
                multicast:
                  map: "import-map"
                  prefix: 89
                unicast:
                  allow_evpn: true
                  limit: 12
                  map: "ran-map"
              map: "import-map"
    state: replaced

# Task Output:
# ------------
#
# before:
# - name: test1
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 40
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 345
#           unicast:
#             allow_evpn: true
#             map: "test-map"
#             prefix: 67
#         map: "testing-map"
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map"
#             prefix: 89
#           unicast:
#             allow_evpn: true
#             limit: 12
#             map: "ran-map"
#       map: "import-map"
#
# commands:
# - vrf definition test1
# - address-family ipv4 unicast
# - bgp next-hop loopback 40
# - export map "testing-map"
# - export ipv4 multicast 345 map "single"
# - export ipv4 unicast 67 map "test-map" allow-evpn
# - import map "import-map"
# - import ipv4 multicast 89 map "import-map"
# - import ipv4 unicast 12 map "ran-map" allow-evpn
#
# after:
# - name: VRF1
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 23
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 33
#           unicast:
#             allow_evpn: true
#             map: "test-map1"
#             prefix: 7
#         map: "testing-map"
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map1"
#             prefix: 89
#           unicast:
#             allow_evpn: true
#             limit: 12
#             map: "ran-map"
#       map: "import-map"
#
# After state:
# ------------
#
# RP/0/RP0/CPU0:ios(config)#show running-config vrf
# vrf definition VRF1
#  address-family ipv4 unicast
#   bgp next-hop loopback 23
#   export map "testing-map"
#   export ipv4 multicast 345 map "single"
#   export ipv4 unicast 67 map "test-map1" allow-evpn
#   import map "import-map"
#   import ipv4 multicast 89 map "import-map1"
#   import ipv4 unicast 12 map "ran-map" allow-evpn

# Using overridden
#
# Before state:
# -------------
#
# RP/0/RP0/CPU0:ios(config)#show running-config | section ^vrf
# vrf definition test1
#  address-family ipv4 unicast
#   bgp next-hop loopback 40
#   export map "testing-map"
#   export ipv4 multicast 345 map "single"
#   export ipv4 unicast 67 map "test-map" allow-evpn
#   import map "import-map"
#   import ipv4 multicast 89 map "import-map"
#   import ipv4 unicast 12 map "ran-map" allow-evpn

- name: Override the provided configuration with the existing running configuration
  cisco.ios.ios_vrf_address_family:
    state: overridden
    config:
      - name: VRF7
        address_families:
          - afi: "ipv4"
            safi: "unicast"
            bgp:
              next_hop:
                loopback: 89
            export:
              ipv4:
                multicast:
                  map: "single"
                  prefix: 345
                unicast:
                  allow_evpn: true
                  map: "test-map"
                  prefix: 67
              map: "testing-map"
            import_config:
              ipv4:
                multicast:
                  map: "import-map"
                  prefix: 89
                unicast:
                  allow_evpn: true
                  limit: 12
                  map: "ran-map"
              map: "import-map"
# Task Output:
# ------------
#
# before:
# - name: test1
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 40
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 345
#           unicast:
#             allow_evpn: true
#             map: "test-map"
#             prefix: 67
#         map: "testing-map"
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map"
#             prefix: 89
#           unicast:
#             allow_evpn: true
#             limit: 12
#             map: "ran-map"
#       map: "import-map"
#
# commands:
# - vrf definition VRF7
# - address-family ipv4 unicast
# - bgp next-hop loopback 89
# - export map "testing-map"
# - export ipv4 multicast 345 map "single"
# - export ipv4 unicast 67 map "test-map" allow-evpn
# - import map "import-map"
# - import ipv4 multicast 89 map "import-map"
# - import ipv4 unicast 12 map "ran-map" allow-evpn

#
# after:
# - name: VRF4
# - name: VRF7
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 89
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 345
#           unicast:
#             allow_evpn: true
#             map: "test-map"
#             prefix: 67
#         map: "testing-map"
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map1"
#             prefix: 89
#           unicast:
#             allow_evpn: true
#             limit: 12
#             map: "ran-map"
#       map: "import-map"
#
# After state:
# -------------
# RP/0/RP0/CPU0:ios(config)#show running-config vrf
# vrf definition VRF4
# vrf definition VRF7
#  address-family ipv4 unicast
#   bgp next-hop loopback 89
#   export map "testing-map"
#   export ipv4 multicast 345 map "single"
#   export ipv4 unicast 67 map "test-map" allow-evpn
#   import map "import-map"
#   import ipv4 multicast 89 map "import-map1"
#   import ipv4 unicast 12 map "ran-map" allow-evpn

# Using deleted
#
# Before state:
# -------------
#
# RP/0/RP0/CPU0:ios(config)#show running-config | section ^vrf
# vrf definition VRF4
# vrf definition VRF6
# address-family ipv4 unicast
#  bgp next-hop loopback 40
#  import map "import-map"
#  import ipv4 multicast 89 map "import-map"
#  import ipv4 unicast 12 map "ran-map" allow-evpn
#  export map "testing-map"
#  export ipv4 multicast 345 map "single"
#  export ipv4 unicast 67 map "test-map" allow-evpn
# vrf definition VRF7

- name: Delete the provided configuration
  cisco.ios.ios_vrf_address_family:
    config:
    state: deleted

# Task Output:
# ------------
#
# before:
# - name: VRF4
# - name: VRF6
#   address_families:
#     - afi: "ipv4"
#       safi: "unicast"
#       bgp:
#         next_hop:
#           loopback: 23
#       import_config:
#         ipv4:
#           multicast:
#             map: "import-map"
#             prefix: 89
#           unicast:
#             map: "ran-map"
#             limit: 12
#             allow_evpn: true
#         map: "import-map"
#       export:
#         ipv4:
#           multicast:
#             map: "single"
#             prefix: 345
#           unicast:
#             map: "test-map"
#             prefix: 67
#             allow_evpn: true
#         map: "testing-map"
# - name: VRF7

# commands:
# - vrf definition VRF4
# - vrf definition VRF6
# - no address-family ipv4 unicast
# - vrf definition VRF7
#
# after:
# - name: VRF4
# - name: VRF6
# - name: VRF7
#
# After state:
# ------------
#
# RP/0/RP0/CPU0:ios(config)#show running-config | section ^vrf
# vrf definition VRF4
# vrf definition VRF6
# vrf definition VRF7

# Using rendered
#
- name: Render provided configuration with device configuration
  cisco.ios.ios_vrf_address_family:
    config:
      - name: test
        address_families:
          - afi: "ipv4"
            safi: "unicast"
            bgp:
              next_hop:
                loopback: 23
            import_config:
              ipv4:
                multicast:
                  map: "import-map"
                  prefix: 89
                unicast:
                  map: "ran-map"
                  limit: 12
                  allow_evpn: true
              map: "import-map"
            export:
              ipv4:
                multicast:
                  map: "single"
                  prefix: 345
                unicast:
                  map: "test-map"
                  prefix: 67
                  allow_evpn: true
              map: "testing-map"
    state: rendered

# Task Output:
# ------------
#
# rendered:
# - vrf definition test
# - address-family ipv4 unicast
# - bgp next-hop loopback 23
# - import map "import-map"
# - import ipv4 multicast 89 map "import-map"
# - import ipv4 unicast 12 map "ran-map" allow-evpn
# - export map "testing-map"
# - export ipv4 multicast 345 map "single"
# - export ipv4 unicast 67 map "test-map" allow-evpn

# Using gathered
#
# Before state:
# -------------
#
# RP/0/RP0/CPU0:ios(config)#show running-config | section ^vrf
# vrf definition test1
# address-family ipv4 unicast
#  bgp next-hop loopback 40
#  import map "import-map"
#  import ipv4 multicast 89 map "import-map"
#  import ipv4 unicast 12 map "ran-map" allow-evpn
#  export map "testing-map"
#  export ipv4 multicast 345 map "single"
#  export ipv4 unicast 67 map "test-map" allow-evpn

- name: Gather existing running configuration
  cisco.ios.ios_vrf_address_family:
    state: gathered

# Task Output:
# ------------
#
# gathered:
# - name: test1
#   address_families:
#    - afi: "ipv4"
#      safi: "unicast"
#      bgp:
#        next_hop:
#          loopback: 40
#      export:
#        ipv4:
#          multicast:
#            map: "single"
#            prefix: 345
#          unicast:
#            allow_evpn: true
#            map: "test-map"
#            prefix: 67
#        map: "testing-map"
#      import_config:
#        ipv4:
#          multicast:
#            map: "import-map"
#            prefix: 89
#          unicast:
#            allow_evpn: true
#            limit: 12
#            map: "ran-map"
#        map: "import-map"

# Using parsed
#
# File: parsed.cfg
# ----------------
#
# vrf definition test
# address-family ipv4 unicast
#  bgp next-hop loopback 23
#  import map "import-map"
#  import ipv4 multicast 89 map "import-map"
#  import ipv4 unicast 12 map "ran-map" allow-evpn
#  export map "testing-map"
#  export ipv4 multicast 345 map "single"
#  export ipv4 unicast 67 map "test-map" allow-evpn

- name: Parse the provided configuration
  cisco.ios.ios_vrf_address_family:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
#
# parsed:
#   - address_families:
#     - afi: ipv4
#       bgp:
#         next_hop:
#           loopback: 40
#        export:
#          ipv4:
#            multicast:
#              map: "single"
#              prefix: 345
#            unicast:
#              allow_evpn: true
#              map: "test-map"
#              prefix: 67
#          map: "testing-map"
#        import_config:
#          ipv4:
#            multicast:
#              map: "import-map"
#              prefix: 89
#            unicast:
#              allow_evpn: true
#              limit: 12
#              map: "ran-map"
#       safi: unicast
#     name: test
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_address_family.vrf_address_family import (
    Vrf_address_familyArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vrf_address_family.vrf_address_family import (
    Vrf_address_family,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vrf_address_familyArgs.argument_spec,
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

    result = Vrf_address_family(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
