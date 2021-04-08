#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for cisco.ios_route_maps
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_route_maps
short_description: Route maps resource module
description:
  - This module configures and manages the attributes of Route maps on Cisco IOS.
version_added: 2.1.0
author: Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSv Version 15.2 on VIRL
  - This module works with connection C(network_cli).
    See L(IOS Platform Options,../network/user_guide/platform_ios.html)
options:
  config:
    description: A list of configurations for Route maps.
    type: list
    elements: dict
    suboptions:
      route_map:
        description: Route map tag/name
        type: str
      entries:
        description: A list of configurations entries for Route maps.
        type: list
        elements: dict
        suboptions:
          sequence:
            description:
              - Sequence to insert to/delete from existing route-map entry
              - Please refer vendor documentation for valid values
            type: int
          action:
            description: Route map set operations
            type: str
            choices: ['deny', 'permit']
          continue:
            description: Continue on a different entry within the route-map
            type: dict
            suboptions:
              set:
                description: Set continue
                type: bool
              entry_sequence:
                description:
                  - Route-map entry sequence number
                  - Please refer vendor documentation for valid values
                type: int
          description:
            description: Route-map comment
            type: str
          match:
            description: Match values from routing table
            type: dict
            suboptions:
              additional_paths:
                description:
                  - BGP Add-Path match policie
                  - BGP Add-Path advertise-set policy
                type: dict
                suboptions:
                  all:
                    description: BGP Add-Path advertise all paths
                    type: bool
                  best:
                    description: BGP Add-Path advertise best n paths (1-3)
                    type: int
                  best_range:
                    description: BGP Add-Path advertise best paths (range m to n)
                    type: dict
                    suboptions:
                      lower_limit:
                        description: BGP Add-Path best paths to advertise (lower limit) (1-3)
                        type: int
                      upper_limit:
                        description: BGP Add-Path best paths to advertise (upper limit) (1-3)
                        type: int
                  group_best:
                    description: BGP Add-Path advertise group-best path
                    type: bool
              as_path:
                description: Match BGP AS path list
                type: dict
                suboptions:
                  set:
                    description: Set AS path list
                    type: bool
                  acl: &acl
                    description:
                      - AS path access-list
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
              clns:
                description: CLNS information
                type: dict
                suboptions:
                  address:
                    description: Match address of route or match packet
                    type: str
                  next_hop:
                    description: Match next-hop address of route
                    type: str
                  route_source:
                    description: Match advertising source address of route
                    type: str
              community:
                description: Match BGP community list
                type: dict
                suboptions:
                  name:
                    description:
                      - Community-list number/Community-list name
                      - Please refer vendor documentation for valid values
                    type: str
                  exact_match:
                    description: Do exact matching of communities
                    type: str
              extcommunity:
                description:
                  - Match BGP/VPN extended community list
                  - Extended community-list number
                  - Please refer vendor documentation for valid values
                type: str
              interface:
                description: Match first hop interface of route
                type: list
                elements: str
              ip:
                description: IP specific information
                type: dict
                suboptions:
                  address:
                    description: Match address of route or match packet
                    type: dict
                    suboptions:
                      acl: *acl
                      prefix_list: &prefix_list
                        description:
                          - Match entries of prefix-lists
                          - IP prefix-list name
                        type: list
                        elements: str
                  flowspec:
                    description: Match src/dest prefix component of flowspec prefix
                    type: dict
                    suboptions:
                      dest_pfx:
                        description: Match dest prefix component of flowspec prefix
                        type: bool
                      src_pfx:
                        description: Match source prefix component of flowspec prefix
                        type: bool
                      acl: *acl
                      prefix_list: *prefix_list
                  next_hop:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      set:
                        description: Set next-hop address
                        type: bool
                      acl: *acl
                      prefix_list: *prefix_list
                  redistribution_source:
                    description: route redistribution source (EIGRP only)
                    type: dict
                    suboptions:
                      set:
                        description: Set redistribution-source
                        type: bool
                      acl: *acl
                      prefix_list: *prefix_list
                  route_source:
                    description: Match advertising source address of route
                    type: dict
                    suboptions:
                      set:
                        description: Set redistribution-source
                        type: bool
                      redistribution_source:
                        description: route redistribution source (EIGRP only)
                        type: bool
                      acl: *acl
                      prefix_list: *prefix_list
              ipv6:
                description: IPv6 specific information
                type: dict
                suboptions:
                  address:
                    type: dict
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  flowspec:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      dest_pfx:
                        description: Match dest prefix component of flowspec prefix
                        type: bool
                      src_pfx:
                        description: Match source prefix component of flowspec prefix
                        type: bool
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  next_hop:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  route_source:
                    description: Match advertising source address of route
                    type: dict
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
              length:
                description: Packet length
                type: dict
                suboptions:
                  minimum:
                    description:
                      - Minimum packet length
                      - Please refer vendor documentation for valid values
                    type: int
                  maximum:
                    description:
                      - Maximum packet length
                      - Please refer vendor documentation for valid values
                    type: int
              local_preference:
                description: Local preference for route
                type: dict
                suboptions:
                  set:
                    description: Set the Local preference for route
                    type: bool
                  value:
                    description:
                      - Local preference value
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: str
              mdt_group:
                description: Match routes corresponding to MDT group
                type: dict
                suboptions:
                  set:
                    description: Set and Match routes corresponding to MDT group
                    type: bool
                  acl:
                    description:
                      - IP access-list number/IP standard access-list name
                      - Please refer vendor documentation for valid values
                    type: str
              metric:
                description: Match metric of route
                type: dict
                suboptions:
                  value:
                    description:
                      - Metric value
                      - Please refer vendor documentation for valid values
                    type: int
                  external:
                    description: Match route using external protocol metric
                    type: bool
                  deviation:
                    description: Deviation option to match metric in a range
                    choices: ['plus', 'minus']
                    type: str
                  deviation_value:
                    description:
                      - deviation value, 500 +- 10 creates the range 490 - 510
                      - Please refer vendor documentation for valid values
                    type: int
              mpls_label:
                description: Match routes which have MPLS labels
                type: bool
              policy_list:
                description: Match IP policy list
                type: list
                elements: str
              route_type:
                description: Match route-type of route
                type: dict
                suboptions:
                  external:
                    description: external route (BGP, EIGRP and OSPF type 1/2)
                    type: dict
                    suboptions:
                      set:
                        description: Set external route
                        type: bool
                      type_1:
                        description: OSPF external type 1 route
                        type: bool
                      type_2:
                        description: OSPF external type 2 route
                        type: bool
                  internal:
                    description: internal route (including OSPF intra/inter area)
                    type: bool
                  level_1:
                    description: IS-IS level-1 route
                    type: bool
                  level_2:
                    description: IS-IS level-2 route
                    type: bool
                  local:
                    description: locally generated route
                    type: bool
                  nssa_external:
                    description: nssa-external route (OSPF type 1/2)
                    type: dict
                    suboptions:
                      set:
                        description: Set nssa-external route
                        type: bool
                      type_1:
                        description: OSPF external type 1 route
                        type: bool
                      type_2:
                        description: OSPF external type 2 route
                        type: bool
              rpki:
                description: Match RPKI state of route
                type: dict
                suboptions:
                  invalid:
                    description: RPKI Invalid State
                    type: bool
                  not_found:
                    description: RPKI Not Found State
                    type: bool
                  valid:
                    description: RPKI Valid State
                    type: bool
              security_group:
                description: Security Group
                type: dict
                suboptions:
                  source:
                    description:
                      - Source Security Group, source Security tag
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
                  destination:
                    description:
                      - Destination Security Group, destination Security tag
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
              source_protocol:
                description: Match source-protocol of route
                type: dict
                suboptions:
                  bgp:
                    description:
                      - Border Gateway Protocol (BGP)
                      - Autonomous system number
                      - Please refer vendor documentation for valid values
                    type: str
                  connected:
                    description: Connected
                    type: bool
                  eigrp:
                    description:
                      - Enhanced Interior Gateway Routing Protocol (EIGRP)
                      - Autonomous system number
                      - Please refer vendor documentation for valid values
                    type: int
                  isis:
                    description: ISO IS-IS
                    type: bool
                  lisp:
                    description: Locator ID Separation Protocol (LISP)
                    type: bool
                  mobile:
                    description: Mobile routes
                    type: bool
                  ospf:
                    description:
                      - Open Shortest Path First (OSPF) Process ID
                      - Please refer vendor documentation for valid values
                    type: int
                  ospfv3:
                    description:
                      - OSPFv3 Process ID
                      - Please refer vendor documentation for valid values
                    type: int
                  rip:
                    description: Routing Information Protocol (RIP)
                    type: bool
                  static:
                    description: Static routes
                    type: bool
              tag:
                description: Match tag of route
                type: dict
                suboptions:
                  value:
                    description: Tag value/Tag in Dotted Decimal eg, 10.10.10.10
                    type: list
                    elements: str
                  list:
                    description: Route Tag List/Tag list name
                    type: list
                    elements: str
              track:
                description: tracking object
                type: int
          set:
            description: Match source-protocol of route
            type: dict
            suboptions:
              aigp_metric:
                description: accumulated metric value
                type: dict
                suboptions:
                  value:
                    description: manual value
                    type: int
                  igp_metric:
                    description: metric value from rib
                    type: bool
              as_path:
                description: Prepend string for a BGP AS-path attribute
                type: dict
                suboptions:
                  prepend:
                    description: Prepend to the as-path
                    type: dict
                    suboptions:
                      as_number:
                        description:
                          - AS number
                          - Please refer vendor documentation for valid values
                        type: str
                      last_as:
                        description:
                          - Prepend last AS to the as-path
                          - Number of last-AS prepends
                          - Please refer vendor documentation for valid values
                        type: int
                  tag:
                    description: Set the tag as an AS-path attribute
                    type: bool
              automatic_tag:
                description: Automatically compute TAG value
                type: bool
              clns:
                description:
                  - OSI summary address
                  - Next hop address
                  - CLNS summary prefix
                type: str
              comm_list:
                description:
                  - set BGP community list (for deletion)
                  - Community-list name/number
                  - Delete matching communities
                type: str
              community:
                description: BGP community attribute
                type: dict
                suboptions:
                  number:
                    description:
                      - community number
                      - community number in aa:nn format
                      - Please refer vendor documentation for valid values
                    type: str
                  additive:
                    description: Add to the existing community
                    type: bool
                  gshut:
                    description: Graceful Shutdown (well-known community)
                    type: bool
                  internet:
                    description: Internet (well-known community)
                    type: bool
                  local_as:
                    description: Do not send outside local AS (well-known community)
                    type: bool
                  no_advertise:
                    description: Do not advertise to any peer (well-known community)
                    type: bool
                  no_export:
                    description: Do not export to next AS (well-known community)
                    type: bool
                  none:
                    description: No community attribute
                    type: bool
              dampening:
                description: Set BGP route flap dampening parameters
                type: dict
                suboptions:
                  penalty_half_time:
                    description:
                      - half-life time for the penalty
                      - Please refer vendor documentation for valid values
                    type: int
                  reuse_route_val:
                    description:
                      - Penalty to start reusing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  suppress_route_val:
                    description:
                      - Penalty to start suppressing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  max_suppress:
                    description:
                      - Maximum duration to suppress a stable route
                      - Please refer vendor documentation for valid values
                    type: int
              default:
                description:
                  - Set default information
                  - Default output interface
                type: str
              extcomm_list:
                description:
                  - Set BGP/VPN extended community list (for deletion)
                  - Extended community-list number/name
                  - Delete matching extended communities
                type: str
              extcommunity:
                description: BGP extended community attribute
                type: dict
                suboptions:
                  cost:
                    description: Cost extended community
                    type: dict
                    suboptions:
                      id:
                        description:
                          - Community ID
                          - Please refer vendor documentation for valid values
                        type: int
                      cost:
                        description:
                          - Cost Value (No-preference Cost = 2147483647)
                          - Please refer vendor documentation for valid values
                        type: int
                      igp:
                        description: Compare following IGP cost comparison
                        type: bool
                      pre_bestpath:
                        description: Compare before all other steps in bestpath calculation
                        type: bool
                  rt:
                    description: Route Target extended community
                    type: dict
                    suboptions:
                      address:
                        description: VPN extended community
                        type: str
                      range:
                        description: Specify a range of extended community
                        type: bool
                  soo:
                    description: Site-of-Origin extended community
                    type: str
                  vpn_distinguisher:
                    description: VPN Distinguisher
                    type: dict
                    suboptions:
                      address:
                        description: VPN extended community
                        type: str
                      range:
                        description: Specify a range of extended community
                        type: bool
                      additive:
                        description: Add to the existing extcommunity
                        type: bool
              global:
                description: Set to global routing table
                type: bool
              interface:
                description: Output interface
                type: str
              ip:
                description: IP specific information
                type: dict
                suboptions:
                  address:
                    description:
                      - Specify IP address
                      - Prefix-list name to set ip address
                    type: str
                  default:
                    description: Set default information
                    type: bool
                  df:
                    description: Set DF bit
                    choices: [0, 1]
                    type: int
                  global:
                    description: global routing table
                    type: bool
                    suboptions:
                      address:
                        description: IP address of next hop
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: IP address of next hop
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  next_hop:
                    description: Next hop address
                    type: dict
                    suboptions:
                      address:
                        description: IP address of next hop
                        type: str
                      dynamic:
                        description:
                          - application dynamically sets next hop
                          - DHCP learned next hop
                        type: bool
                      encapsulate:
                        description:
                          - Encapsulation profile for VPN nexthop
                          - L3VPN
                          - Encapsulation profile name
                        type: str
                      peer_address:
                        description: Use peer address (for BGP only)
                        type: bool
                      recursive:
                        description: Recursive next-hop
                        type: dict
                        suboptions:
                          address:
                            description: IP address of recursive next hop
                            type: str
                          global:
                            description: global routing table
                            type: str
                          vrf:
                            description: VRF
                            type: dict
                            suboptions:
                              name:
                                description: VRF name
                                type: str
                              address:
                                description: IP address of recursive next hop
                                type: str
                      self:
                        description: Use self address (for BGP only)
                        type: bool
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          set:
                            description: Set and Verify if nexthop is reachable
                            type: bool
                          address:
                            description: IP address of next hop
                            ype: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  precedence:
                    description: Set precedence field
                    type: dict
                    suboptions:
                      set:
                        description: Just set precedence field
                        type: bool
                      critical:
                        description: Set critical precedence (5)
                        type: bool
                      flash:
                        description: Set flash precedence (3)
                        type: bool
                      flash_override:
                        description: Set flash override precedence (4)
                        type: bool
                      immediate:
                        description: Set immediate precedence (2)
                        type: bool
                      internet:
                        description: Set internetwork control precedence (6)
                        type: bool
                      network:
                        description: Set network control precedence (7)
                        type: bool
                      priority:
                        description: Set priority precedence (1)
                        type: bool
                      routine:
                        description: Set routine precedence (0)
                        type: bool
                  qos_group:
                    description:
                      - Set QOS Group ID
                      - Please refer vendor documentation for valid values
                    type: int
                  tos:
                    description: Set type of service field
                    type: dict
                    suboptions:
                      set:
                        description: Just set type of service field
                        type: bool
                      max_reliability:
                        description: Set max reliable TOS (2)
                        type: bool
                      max_throughput:
                        description: Set max throughput TOS (4)
                        type: bool
                      min_delay:
                        description: Set min delay TOS (8)
                        type: bool
                      min_monetary_cost:
                        description: Set min monetary cost TOS (1)
                        type: bool
                      normal:
                        description: Set normal TOS (0)
                        type: bool
                  vrf:
                    description: VRF
                    type: dict
                    suboptions:
                      name:
                        description: VRF name
                        type: str
                      address:
                        description: IP address of next hop
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          set:
                            description: Set and Verify if nexthop is reachable
                            type: bool
                          address:
                            description: IP address of next hop
                            ype: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
              ipv6:
                description: IPv6 specific information
                type: dict
                suboptions:
                  address:
                    description:
                      - IPv6 address
                      - IPv6 prefix-list
                    type: str
                  default:
                    description: Set default information
                    type: bool
                  global:
                    description: global routing table
                    type: dict
                    suboptions:
                      address:
                        description: Next hop address (X:X:X:X::X)
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: Next hop address (X:X:X:X::X)
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  next_hop:
                    description: IPv6 Next hop
                    type: dict
                    suboptions:
                      address:
                        description: Next hop address (X:X:X:X::X)
                        type: str
                      encapsulate:
                        description:
                          - Encapsulation profile for VPN nexthop
                          - L3VPN
                          - Encapsulation profile name
                        type: str
                      peer_address:
                        description: Use peer address (for BGP only)
                        type: bool
                      recursive:
                        description:
                          - Recursive next-hop
                          - IPv6 address of recursive next-hop
                        type: str
                  precedence:
                    description:
                      - Set precedence field
                      - Precedence value
                      - Please refer vendor documentation for valid values
                    type: int
                  vrf:
                    description: VRF name
                    type: dict
                    suboptions:
                      name:
                        description: VRF name
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: IPv6 address of next hop
                            ype: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
              level:
                description: Where to import route
                type: dict
                suboptions:
                  level_1:
                    description: Import into a level-1 area
                    type: bool
                  level_1_2:
                    description: Import into level-1 and level-2
                    type: bool
                  level_2:
                    description: Import into level-2 sub-domain
                    type: bool
                  nssa_only:
                    description: Import only into OSPF NSSA areas and don't propagate
                    type: bool
              lisp:
                description:
                  - Locator ID Separation Protocol specific information
                  - Specify a locator-set to use in LISP route-import
                  - The name of the locator set
                type: str
              local_preference:
                description:
                  - BGP local preference path attribute
                  - Please refer vendor documentation for valid values
                type: int
              metric:
                description: Metric value for destination routing protocol
                type: dict
                suboptions:
                  deviation:
                    description: Add or subtract metric
                    choices: ['plus', 'minus']
                    type: str
                  metric_value:
                    description:
                      - Metric value or Bandwidth in Kbits per second
                      - Please refer vendor documentation for valid values
                    type: int
                  eigrp_delay:
                    description:
                      - EIGRP delay metric, in 10 microsecond units
                      - Please refer vendor documentation for valid values
                    type: int
                  metric_reliability:
                    description:
                      - EIGRP reliability metric where 255 is 100 reliable
                      - Please refer vendor documentation for valid values
                    type: int
                  metric_bandwidth:
                    description:
                      - EIGRP Effective bandwidth metric (Loading) where 255 is 100 loaded
                      - Please refer vendor documentation for valid values
                    type: int
                  mtu:
                    description:
                      - EIGRP MTU of the path
                      - Please refer vendor documentation for valid values
                    type: int
              metric_type:
                description: Type of metric for destination routing protocol
                type: dict
                suboptions:
                  external:
                    description: IS-IS external metric
                    type: bool
                  internal:
                    description: IS-IS internal metric or Use IGP metric as the MED for BGP
                    type: bool
                  type_1:
                    description: OSPF external type 1 metric
                    type: bool
                  type_2:
                    description: OSPF external type 2 metric
                    type: bool
              mpls_label:
                description: Set MPLS label for prefix
                type: bool
              origin:
                description: BGP origin code
                type: dict
                suboptions:
                  igp:
                    description: local IGP
                    type: bool
                  incomplete:
                    description: unknown heritage
                    type: bool
              tag:
                description:
                  - Tag value for destination routing protocol
                  - Tag value A.B.C.D(dotted decimal format)/Tag value
                type: str
              traffic_index:
                description:
                  - BGP traffic classification number for accounting
                  - Please refer vendor documentation for valid values
                type: int
              vrf:
                description:
                  - Define VRF name
                  - VPN Routing/Forwarding instance name
                type: str
              weight:
                description:
                  - BGP weight for routing table
                  - Please refer vendor documentation for valid values
                type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(sh running-config | section ^router bgp).
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - parsed
      - rendered
    default: merged
required_if:
- ["state", "merged", ["config",]]
- ["state", "replaced", ["config",]]
- ["state", "overridden", ["config",]]
- ["state", "rendered", ["config",]]
- ["state", "parsed", ["running_config",]]
mutually_exclusive:
- ["config", "running_config"]
supports_check_mode: True
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.route_maps.route_maps import (
    Route_mapsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.route_maps.route_maps import (
    Route_maps,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Route_mapsArgs.argument_spec,
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

    result = Route_maps(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
