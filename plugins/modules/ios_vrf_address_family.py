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
version_added: 7.0.0
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
          mdt:
            description: Backbone Multicast Distribution Tree
            type: dict
            suboptions:
              auto_discovery:
                description: BGP auto-discovery for MVPN
                type: dict
                suboptions:
                  ingress_replication:
                    description: BGP auto-discovery for Ingress-Replication
                    type: dict
                    suboptions:
                      inter_as:
                        description: Enable Inter-AS BGP auto-discovery
                        type: dict
                        suboptions:
                          mdt_hello_enable: &mdt_hello_enable
                            description: Enable PIM Hellos over MDT interface
                            type: bool
                      mdt_hello_enable: *mdt_hello_enable
                  pim:
                    description: BGP auto-discovery for PIM
                    type: dict
                    suboptions:
                      inter_as:
                        description: Enable Inter-AS BGP auto-discovery
                        type: dict
                        suboptions:
                          mdt_hello_enable: *mdt_hello_enable
                          pim_tlv_announce: &pim_tlv_announce
                            description: Announce PIM TLV for data MDT
                            type: dict
                            suboptions:
                              mdt_hello_enable: *mdt_hello_enable
                      mdt_hello_enable: *mdt_hello_enable
                      pim_tlv_announce: *pim_tlv_announce
                  receiver_site:
                    description: BGP receiver only site for MVPN
                    type: bool
              data:
                description: MDT data trees
                type: dict
                suboptions:
                  ingress_replication:
                    description: Use Ingress-Replication to create the data MDT
                    type: dict
                    suboptions:
                      number:
                        description: Number of data MDT
                        type: int
                      immediate_swich:
                        description: Switch immediately to Data MDT tree
                        type: bool
                      list: &list
                        description: Access-list
                        type: dict
                        suboptions:
                          access_list_number:
                            description: Access-list number
                            type: int
                          name:
                            description: IP Named Extended Access list
                            type: str
                  list: *list
                  threshold:
                    description: MDT switching threshold
                    type: int
              default:
                description: Default MDT configuration
                type: dict
                suboptions:
                  ingress_replication:
                    description: Use Ingress-Replication for the default MDT
                    type: bool
              direct:
                description: Direct MDT's
                type: bool
              log_reuse:
                description: Event logging for data MDT reuse
                type: bool
              mode:
                description: The type of encapsulation
                type: bool
                choices: ['gre', 'GRE']
              mtu:
                description: The MTU
                type: int
              overlay:
                description: MDT overlay Protocol
                type: dict
                suboptions:
                  bgp:
                    description: BGP Overlay signalling
                    type: dict
                    suboptions:
                      shared_tree_prune_delay:
                        description: Delay before shared tree is pruned at C-RP PE
                        type: dict
                        suboptions:
                          delay:
                            description: Delay (in secs)
                            type: int
                      source_tree_prune_delay:
                        description: Delay before source tree is pruned at C-S PE
                        type: dict
                        suboptions:
                          delay:
                            description: Delay (in secs)
                            type: int
                  use_bgp:
                    description: Use BGP for MDT overlay signaling
                    type: dict
                    suboptions:
                      spt_only:
                        description: Enable SPT-only ASM mode
                        type: bool
              partitioned:
                description: Partitioned Multicast Distribution Tree
                type: dict
                suboptions:
                  ingress_replication:
                    description: Use Ingress-Replication for the partitioned MDT
                    type: bool
              strict_rpf:
                description: Enable strict RPF check
                type: dict
                suboptions:
                  interface:
                    description: Interface based strict RPF check
                    type: bool
          protection:
            description: Configure local repair
            type: dict
            suboptions:
              local_prefixes:
                description: Enable protection for local prefixes
                type: bool
          route_replicate: &route_replicate
            description: Replicate (import) routes from another topology (and another VRF)
            type: dict
            suboptions:
              recursion_policy:
                description: Route replication recursion policy
                type: dict
                suboptions:
                  destination:
                    description: Recurse in destination topology
                    type: bool
              from_config:
                description: Replicate routes from another VRF
                type: dict
                suboptions:
                  multicast:
                    description: Multicast SAFI
                    type: dict
                    suboptions:
                      all: &all
                        description: All routes
                        type: dict
                        suboptions:
                          route_map: &route_map
                            description: Route-map reference
                            type: str
                      bgp: &bgp
                        description: Border Gateway Protocol (BGP)
                        type: dict
                        suboptions:
                          as_number:
                            description: Autonomous System Number
                            type: int
                          route_map: *route_map
                      eigrp: &eigrp
                        description: Enhanced Interior Gateway Routing Protocol (EIGRP)
                        type: dict
                        suboptions:
                          as_number:
                            description: Autonomous System Number
                            type: int
                          route_map: *route_map
                      isis: &isis
                        description: Intermediate System-to-Intermediate System (ISIS)
                        type: dict
                        suboptions:
                          iso_tag:
                            description: ISO routing area tag
                            type: str
                          route_map: *route_map
                      mobile: &mobile
                        description: Mobile routes
                        type: dict
                        suboptions:
                          route_map: *route_map
                      odr: &odr
                        description: On-Demand Stub routes
                        type: dict
                        suboptions:
                          route_map: *route_map
                      ospf: &ospf
                        description: Open Shortest Path First (OSPF)
                        type: dict
                        suboptions:
                          process_id:
                            description: OSPF process ID
                            type: int
                          route_map: *route_map
                      rip: &rip
                        description: Routing Information Protocol (RIP)
                        type: dict
                        suboptions:
                          route_map: *route_map
                      static: &static
                        description: Static routes
                        type: dict
                        suboptions:
                          route_map: *route_map
                      topology: &topology
                        description: Topology name
                        type: dict
                        suboptions:
                          base:
                            description: Base topology
                            type: dict
                            suboptions:
                              all: *all
                              bgp: *bgp
                              eigrp: *eigrp
                              isis: *isis
                              mobile: *mobile
                              odr: *odr
                              ospf: *ospf
                              rip: *rip
                              static: *static
                  unicast:
                    description: Unicast SAFI
                    type: dict
                    suboptions:
                      all: *all
                      bgp: *bgp
                      connected:
                        description: Connected routes
                        type: dict
                        suboptions:
                          route_map: *route_map
                      eigrp: *eigrp
                      isis: *isis
                      mobile: *mobile
                      odr: *odr
                      ospf: *ospf
                      rip: *rip
                      static: *static
                  vrf:
                    description: Specify a source VRF
                    type: dict
                    suboptions:
                      name:
                        description: Source VRF name
                        type: str
                      global:
                        description: global VRF
                        type: dict
                        suboptions:
                          multicast:
                            description: Multicast SAFI
                            type: dict
                            suboptions:
                              all: *all
                              bgp: *bgp
                              eigrp: *eigrp
                              isis: *isis
                              mobile: *mobile
                              odr: *odr
                              ospf: *ospf
                              rip: *rip
                              static: *static
                              topology: *topology
                          unicast:
                            description: Unicast SAFI
                            type: dict
                            suboptions:
                              all: *all
                              bgp: *bgp
                              connected:
                                description: Connected routes
                                type: dict
                                suboptions:
                                  route_map: *route_map
                              eigrp: *eigrp
                              isis: *isis
                              mobile: *mobile
                              odr: *odr
                              ospf: *ospf
                              rip: *rip
                              static: *static
          route_replicate_distance: &route_replicate_distance
            description: Route replicate distance
            type: dict
            suboptions:
              from_config:
                description: Route replicate distance from another VRF
                type: dict
                suboptions:
                  multicast:
                    description: Multicast SAFI
                    type: dict
                    suboptions:
                      distance:
                        description: Route replicate distance range
                        type: int
                      topology: &id001
                        description: Specify a Routing Topology
                        type: dict
                        suboptions:
                          base:
                            description: Base routing topology
                            type: dict
                            suboptions:
                              distance:
                                description: Route replicate distance range
                                type: int
                  unicast:
                    description: Unicast SAFI
                    type: dict
                    suboptions:
                      distance:
                        description: Route replicate distance range
                        type: int
                      topology: *id001
          route_target: &route_target
            description: Specify Target VPN Extended Communities.
            type: dict
            suboptions:
              export:
                description: Export Target-VPN community.
                type: str
              stitching:
                    description: VXLAN route target set.
                    type: bool
              import_config:
                description: Export Target-VPN community.
                type: str
              both:
                description: Both export and import Target-VPN community
                type: str
          snmp: &snmp
            description: Modify snmp parameters
            type: dict
            suboptions:
              context:
                description: Configure a SNMP context
                type: dict
                suboptions:
                  name:
                    description: SNMP context name
                    type: str
                  community:
                    description: Configure a SNMP v2c Community string and access privileges.
                    type: dict
                    suboptions:
                      name:
                        description: SNMP community string
                        type: str
                      access_number:
                        description: Access-list number
                        type: int
                      access_name:
                        description: Access-list name
                        type: str
                      ipv6:
                        description: Specify IPv6 Named Access-List
                        type: str
                      mode:
                        description: SNMP community mode
                        type: str
                        choices: ['ro', 'rw']
                  user:
                    description: Configure a SNMP v3 user
                    type: dict
                    suboptions:
                      name:
                        description: SNMP user name
                        type: str
                      access: &access
                        description: Specify an access-list associated with this group
                        type: dict
                        suboptions:
                          number:
                            description: Access-list number
                            type: int
                          name:
                            description: Access-list name
                            type: str
                          ipv6:
                            description: Specify IPv6 Named Access-List
                            type: str
                      auth:
                        description: SNMP user authentication parameters
                        type: dict
                        suboptions:
                          md5:
                            description: Use HMAC MD5 algorithm for authentication
                            type: dict
                            suboptions:
                              password:
                                description: authentication password for user
                                type: str
                              access: *access
                              priv: &priv
                                description: encryption parameters for the user
                                type: dict
                                suboptions:
                                  3des:
                                    description: Use 168 bit 3DES algorithm for encryption
                                    type: dict
                                    suboptions:
                                      password:
                                        description: SNMP user password
                                        type: str
                                      access: *access
                                  des:
                                    description: Use 56 bit DES algorithm for encryption
                                    type: dict
                                    suboptions:
                                      password:
                                        description: SNMP user password
                                        type: str
                                      access: *access
                                  aes:
                                    description: Use AES algorithm for encryption
                                    type: dict
                                    suboptions:
                                      128:
                                        description: Use 128 bit AES algorithm for encryption
                                        type: dict
                                        suboptions:
                                          password:
                                            description: privacy password for user
                                            type: str
                                          access: *access
                                      192:
                                        description: Use 192 bit AES algorithm for encryption
                                        type: dict
                                        suboptions:
                                          password:
                                            description: privacy password for user
                                            type: str
                                          access: *access
                                      256:
                                        description: Use 256 bit AES algorithm for encryption
                                        type: dict
                                        suboptions:
                                          password:
                                            description: privacy password for user
                                            type: str
                                          access: *access
                                  des56:
                                    description: Use 56 bit DES algorithm for encryption
                                    type: dict
                                    suboptions:
                                      password:
                                        description: SNMP user password
                                        type: str
                                      access: *access
                              encrypted:
                                description: Specify passwords as MD5 or SHA digests
                                type: bool
                          sha:
                            description: Use HMAC MD5 algorithm for authentication
                            type: dict
                            suboptions:
                              password:
                                description: SNMP user password
                                type: str
                              access: *access
                              priv: *priv
                      credential:
                        description: If the user password is already configured and saved
                        type: str
                      encrypted:
                        description: Specifying passwords as MD5 or SHA digests
                        type: bool
          topology:
            description: Configure a VRF topology
            type: dict
            suboptions:
              base:
                description: Base topology
                type: str
              name:
                description: Topology name
                type: str
              all_interfaces:
                description: Associate a non-base routing topology with all interfaces
                type: bool
              bgp: *bgp01
              export: *export
              import_config: *import01
              maximum: *maximum
              snmp: *snmp
              route_replicate: *route_replicate
              route_replicate_distance: *route_replicate_distance
              route_target: *route_target
              inter_as_hybrid: *inter_as_hybrid
              use_topology:
                description: Configure the unicast topology to be used
                type: dict
                suboptions:
                  unicast:
                    description: Sub Address Family
                    type: dict
                    suboptions:
                      base:
                        description: Base topology
                        type: bool
                      name:
                        description: Topology name
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
