#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bgp_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bgp_global
short_description: Resource module to configure BGP.
description: This module configures and manages the attributes of global bgp on Cisco IOS.
version_added: 1.3.0
author:
  - Sumit Jaiswal (@justjais)
  - Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSv Version 15.2.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of options for bgp configurations.
    type: dict
    suboptions:
      as_number:
        description: Autonomous system number
        type: str
      aggregate_address:
        description:
        - Configure BGP aggregate entry
        - This option is DEPRECATED and is replaced with aggregate_addresses which
          accepts list of dict as input, this attribute will be removed after 2024-06-01.
        type: dict
        suboptions:
          address:
            description: Specify aggregate address
            type: str
          netmask:
            description: Specify aggregate mask
            type: str
          advertise_map:
            description: Set condition to advertise attribute
            type: str
          as_confed_set:
            description: Generate AS confed set path information
            type: bool
          as_set:
            description: Generate AS set path information
            type: bool
          attribute_map:
            description: Set attributes of aggregate
            type: str
          summary_only:
            description: Filter more specific routes from updates
            type: bool
          suppress_map:
            description: Conditionally filter more specific routes from updates
            type: str
      aggregate_addresses:
        description: Configure BGP aggregate entries
        type: list
        elements: dict
        suboptions:
          address:
            description: Specify aggregate address
            type: str
          netmask:
            description: Specify aggregate mask
            type: str
          advertise_map:
            description: Set condition to advertise attribute
            type: str
          as_confed_set:
            description: Generate AS confed set path information
            type: bool
          as_set:
            description: Generate AS set path information
            type: bool
          attribute_map:
            description: Set attributes of aggregate
            type: str
          summary_only:
            description: Filter more specific routes from updates
            type: bool
          suppress_map:
            description: Conditionally filter more specific routes from updates
            type: str
      auto_summary:
        description: Enable automatic network number summarization
        type: bool
      bgp:
        description: Enable address family and enter its config mode
        type: dict
        suboptions:
          additional_paths:
            description: Additional paths in the BGP table
            type: dict
            suboptions:
              install:
                description: Additional paths to install into RIB
                type: bool
              receive:
                description: Receive additional paths from neighbors
                type: bool
              select:
                description: Selection criteria to pick the paths
                type: dict
                suboptions:
                  all:
                    description: Select all available paths
                    type: bool
                  best:
                    description: Select best N paths (2-3).
                    type: int
                  best_external:
                    description: Select best-external path
                    type: bool
                  group_best:
                    description: Select group-best path
                    type: bool
              send:
                description: Send additional paths to neighbors
                type: bool
          advertise_best_external:
            description: Advertise best external path to internal peers
            type: bool
          aggregate_timer:
            description:
              - Configure Aggregation Timer
              - Please refer vendor documentation for valid values
            type: int
          always_compare_med:
            description: Allow comparing MED from different neighbors
            type: bool
          asnotation:
            description:
              - Change the default asplain notation
              - asdot notation
            type: bool
          bestpath:
            description:
            - Change the default bestpath selection
            - This option is DEPRECATED and replaced with bestpath_options of type dict,
              this attribute will be removed after 2024-06-01.
            type: list
            elements: dict
            suboptions:
              aigp:
                description:
                  - if both paths doesn't have aigp ignore on bestpath comparision
                  - ignore
                type: bool
              compare_routerid:
                description: Compare router-id for identical EBGP paths
                type: bool
              cost_community:
                description: cost community
                type: bool
              igp_metric:
                description:
                  - igp metric
                  - Ignore igp metric in bestpath selection
                type: bool
              med:
                description: MED attribute
                type: dict
                suboptions:
                  confed:
                    description: Compare MED among confederation paths
                    type: bool
                  missing_as_worst:
                    description: Treat missing MED as the least preferred one
                    type: bool
          bestpath_options:
            description:
            - Change the default bestpath selection
            type: dict
            suboptions:
              aigp:
                description:
                  - if both paths doesn't have aigp ignore on bestpath comparision
                  - ignore
                type: bool
              compare_routerid:
                description: Compare router-id for identical EBGP paths
                type: bool
              cost_community:
                description: cost community
                type: bool
              igp_metric:
                description:
                  - igp metric
                  - Ignore igp metric in bestpath selection
                type: bool
              med:
                description: MED attribute
                type: dict
                suboptions:
                  confed:
                    description: Compare MED among confederation paths
                    type: bool
                  missing_as_worst:
                    description: Treat missing MED as the least preferred one
                    type: bool
          client_to_client:
            description: Configure client to client route reflection
            type: dict
            suboptions:
              set:
                description: set reflection of routes allowed
                type: bool
              all:
                description: inter-cluster and intra-cluster (default)
                type: bool
              intra_cluster:
                description:
                  - intra cluster reflection
                  - intra-cluster reflection for cluster-id
                type: str
          cluster_id:
            description:
              - Configure Route-Reflector Cluster-id (peers may reset)
              - A.B.C.D/Please refer vendor documentation for valid Route-Reflector Cluster-id
            type: str
          confederation:
            description: AS confederation parameters
            type: dict
            suboptions:
              identifier:
                description:
                  - Set routing domain confederation AS
                  - AS number
                type: str
              peers:
                description:
                  - Peer ASs in BGP confederation
                  - AS number
                type: str
          consistency_checker:
            description: Consistency-checker
            type: dict
            suboptions:
              auto_repair:
                description: Auto-Repair
                type: dict
                suboptions:
                  set:
                    description: Enable Auto-Repair
                    type: bool
                  interval:
                    description:
                      - Set the bgp consistency checker
                      - Please refer vendor documentation for valid values
                    type: int
              error_message:
                description: Log Error-Msg
                type: dict
                suboptions:
                  set:
                    description: Enable Error-Msg
                    type: bool
                  interval:
                    description:
                      - Set the bgp consistency checker
                      - Please refer vendor documentation for valid values
                    type: int
          dampening:
            description: Enable route-flap dampening
            type: dict
            suboptions:
              penalty_half_time:
                description:
                  - Half-life time for the penalty
                  - Please refer vendor documentation for valid values
                type: int
              reuse_route_val:
                description:
                  - Value to start reusing a route
                  - Please refer vendor documentation for valid values
                type: int
              suppress_route_val:
                description:
                  - Value to start suppressing a route
                  - Please refer vendor documentation for valid values
                type: int
              max_suppress:
                description:
                  - Maximum duration to suppress a stable route
                  - Please refer vendor documentation for valid values
                type: int
              route_map:
                description: Route-map to specify criteria for dampening
                type: str
          deterministic_med:
            description: Pick the best-MED path among paths advertised from the neighboring AS
            type: bool
          dmzlink_bw:
            description: Use DMZ Link Bandwidth as weight for BGP multipaths
            type: bool
          enforce_first_as:
            description: Enforce the first AS for EBGP routes(default)
            type: bool
          enhanced_error:
            description: Enabled BGP Enhanced error handling
            type: bool
          fast_external_fallover:
            description: Immediately reset session if a link to a directly connected external peer goes down
            type: bool
          graceful_restart:
            description: Graceful restart capability parameters
            type: dict
            suboptions:
              set:
                description: Set Graceful-Restart
                type: bool
              extended:
                description: Enable Graceful-Restart Extension
                type: bool
              restart_time:
                description:
                  - Set the max time needed to restart and come back up
                  - Please refer vendor documentation for valid values
                type: int
              stalepath_time:
                description:
                  - Set the max time to hold onto restarting peer's stale paths
                  - Please refer vendor documentation for valid values
                type: int
          graceful_shutdown:
            description: Graceful shutdown capability parameters
            type: dict
            suboptions:
              neighbors:
                description: Gracefully shut down all neighbors
                type: dict
                suboptions:
                  time:
                    description:
                      - time in seconds
                      - Please refer vendor documentation for valid values
                    type: int
                  activate:
                    description: Activate graceful shutdown of all neighbors
                    type: bool
              vrfs:
                description: Gracefully shut down all vrf neighbors
                type: dict
                suboptions:
                  time:
                    description:
                      - time in seconds
                      - Please refer vendor documentation for valid values
                    type: int
                  activate:
                    description: Activate graceful shutdown of all neighbors
                    type: bool
              community:
                description:
                  - Set Community for Gshut routes
                  - community number/community number in aa:nn format
                type: str
              local_preference:
                description:
                  - Set Local Preference for Gshut routes
                  - Please refer vendor documentation for valid values
                type: int
          inject_map:
            description:
            - Routemap which specifies prefixes to inject
            - This option is DEPRECATED and is updated with inject_maps which is a
              list of dict, this attribute will be removed after 2024-06-01.
            type: dict
            suboptions:
              name:
                description: route-map name
                type: str
              exist_map_name:
                description: route-map name
                type: str
              copy_attributes:
                description: Copy attributes from aggregate
                type: bool
          inject_maps:
            description: Routemap which specifies prefixes to inject
            type: list
            elements: dict
            suboptions:
              name:
                description: route-map name
                type: str
              exist_map_name:
                description: route-map name
                type: str
              copy_attributes:
                description: Copy attributes from aggregate
                type: bool
          listen:
            description: Neighbor subnet range listener
            type: dict
            suboptions:
              limit:
                description:
                  - Set the max limit for the dynamic subnet range neighbors
                  - Please refer vendor documentation for valid values
                type: int
              range:
                description: Subnet network range
                type: dict
                suboptions:
                  ipv4_with_subnet:
                    description:
                    - IPv4 subnet range(A.B.C.D/nn)
                    - This option is DEPRECATED and is updated with host_with_subnet which is a
                      common attribute for address, this attribute will be removed after 2024-06-01.
                    type: str
                  ipv6_with_subnet:
                    description:
                    - IPv6 subnet range(X:X:X:X::X/<0-128>)
                    - This option is DEPRECATED and is updated with host_with_subnet which is a
                      common attribute for address attribute will be removed after 2024-06-01.
                    type: str
                  host_with_subnet:
                    description:
                    - IPv4 subnet range(A.B.C.D/nn)
                    - IPv6 subnet range(X:X:X:X::X/<0-128>)
                    type: str
                  peer_group:
                    description: Member of the peer-group
                    type: str
          log_neighbor_changes:
            description: Log neighbor up/down and reset reason
            type: bool
          maxas_limit:
            description:
              - Allow AS-PATH attribute from any neighbor imposing a limit on number of ASes
              - Please refer vendor documentation for valid values
            type: int
          maxcommunity_limit:
            description:
              - Allow COMMUNITY attribute from any neighbor imposing a limit on number of communities
              - Please refer vendor documentation for valid values
            type: int
          maxextcommunity_limit:
            description:
              - Allow EXTENDED COMMUNITY attribute from any neighbor imposing a limit on number of extended communities
              - Please refer vendor documentation for valid values
            type: int
          nexthop:
            description: Nexthop tracking commands
            type: dict
            suboptions:
              route_map:
                description: Route map for valid nexthops
                type: str
              trigger:
                description: nexthop trackings
                type: dict
                suboptions:
                  delay:
                    description:
                      - Set the delay to trigger nexthop tracking
                      - Please refer vendor documentation for valid values
                    type: int
                  enable:
                    description: Enable nexthop tracking
                    type: bool
          nopeerup_delay:
            description:
            - Set how long BGP will wait for the first peer to come up before beginning the update delay or
              graceful restart timers (in seconds)
            - This option is DEPRECATED and is replaced with nopeerup_delay_options which is of type dict,
              this attribute will be removed after 2024-06-01.
            type: list
            elements: dict
            suboptions:
              cold_boot:
                description:
                  - How long to wait for the first peer to come up upon a cold boot
                  - Please refer vendor documentation for valid values
                type: int
              nsf_switchover:
                description:
                  - How long to wait for the first peer, post NSF switchover
                  - Please refer vendor documentation for valid values
                type: int
              post_boot:
                description:
                  - How long to wait for the first peer to come up once the system is already
                    booted and all peers go down
                  - Please refer vendor documentation for valid values
                type: int
              user_initiated:
                description:
                  - How long to wait for the first peer, post a manual clear of BGP peers by the admin user
                  - Please refer vendor documentation for valid values
                type: int
          nopeerup_delay_options:
            description: Set how long BGP will wait for the first peer to come up before beginning the update delay or
              graceful restart timers (in seconds)
            type: dict
            suboptions:
              cold_boot:
                description:
                  - How long to wait for the first peer to come up upon a cold boot
                  - Please refer vendor documentation for valid values
                type: int
              nsf_switchover:
                description:
                  - How long to wait for the first peer, post NSF switchover
                  - Please refer vendor documentation for valid values
                type: int
              post_boot:
                description:
                  - How long to wait for the first peer to come up once the system is already
                    booted and all peers go down
                  - Please refer vendor documentation for valid values
                type: int
              user_initiated:
                description:
                  - How long to wait for the first peer, post a manual clear of BGP peers by the admin user
                  - Please refer vendor documentation for valid values
                type: int
          recursion:
            description:
              - recursion rule for the nexthops
              - recursion via host for the nexthops
            type: bool
          redistribute_internal:
            description: Allow redistribution of iBGP into IGPs (dangerous)
            type: bool
          refresh:
            description: refresh
            type: dict
            suboptions:
              max_eor_time:
                description:
                  - Configure refresh max-eor time
                  - Please refer vendor documentation for valid values
                type: int
              stalepath_time:
                description:
                  - Configure refresh stale-path time
                  - Please refer vendor documentation for valid values
                type: int
          regexp:
            description:
              - Select regular expression engine
              - Enable bounded-execution-time regular expression engine
            type: bool
          route_map:
            description:
              - route-map control commands
              - Have route-map set commands take priority over BGP commands such as next-hop unchanged
            type: bool
          router_id:
            description: Override configured router identifier (peers will reset)
            type: dict
            suboptions:
              address:
                description: Manually configured router identifier(A.B.C.D)
                type: str
              interface:
                description: Use IPv4 address on interface
                type: str
              vrf:
                description:
                  - vrf-specific router id configuration
                  - Automatically assign per-vrf bgp router id
                type: bool
          scan_time:
            description:
              - Configure background scanner interval
              - Please refer vendor documentation for valid values
            type: int
          slow_peer:
            description: Configure slow-peer
            type: dict
            suboptions:
              detection:
                description: Slow-peer detection
                type: dict
                suboptions:
                  set:
                    description: Slow-peer detection
                    type: bool
                  threshold:
                    description:
                      - Set the slow-peer detection threshold
                      - Please refer vendor documentation for valid values
                    type: int
              split_update_group:
                description: Configure slow-peer split-update-group
                type: dict
                suboptions:
                  dynamic:
                    description: Dynamically split the slow peer to slow-update group
                    type: bool
                  permanent:
                    description: Keep the slow-peer permanently in slow-update group
                    type: bool
          snmp:
            description:
              - BGP SNMP options
              - BGP SNMP trap options
              - Use cbgp Peer2Type as part of index for traps
            type: bool
          sso:
            description:
              - Stateful Switchover
              - Enable SSO only for Route-Refresh capable peers
            type: bool
          soft_reconfig_backup:
            description: Use soft-reconfiguration inbound only when route-refresh is not negotiated
            type: bool
          suppress_inactive:
            description: Suppress routes that are not in the routing table
            type: bool
          transport:
            description:
              - Global enable/disable transport session parameters
              - Transport path MTU discovery
            type: bool
          update_delay:
            description:
              - Set the max initial delay for sending update
              - Please refer vendor documentation for valid values
            type: int
          update_group:
            description:
              - Manage peers in bgp update groups
              - Split update groups based on Policy
              - Keep peers with as-override in different update groups
            type: bool
          upgrade_cli:
            description: Upgrade to hierarchical AFI mode
            type: dict
            suboptions:
              set:
                description: enable upgrade to hierarchical AFI mode
                type: bool
              af_mode:
                description: Upgrade to AFI mode
                type: bool
      bmp:
        description: BGP Monitoring Protocol
        type: dict
        suboptions:
          buffer_size:
            description:
              - BMP Buffer Size
              - Please refer vendor documentation for valid values
            type: int
          initial_refresh:
            description: Initial Refresh options
            type: dict
            suboptions:
              delay:
                description: Delay before Initial Refresh
                type: int
              skip:
                description: skip all refreshes
                type: bool
          server:
            description:
              - Server Information
              - Please refer vendor documentation for valid values
            type: int
          server_options:
            description: bmp server options
            type: dict
            suboptions:
              activate:
                description: activate server
                type: bool
              address:
                description: skip all refreshes
                type: dict
                suboptions:
                  host:
                    description: host address
                    type: str
                  port:
                    description: port number BMP server
                    type: int
      default_information:
        description:
          - Control distribution of default information
          - Distribute a default route
        type: bool
      default_metric:
        description:
          - Set metric of redistributed routes
          - Please refer vendor documentation for valid values
        type: int
      distance:
        description: Define an administrative distance
        type: dict
        suboptions:
          admin:
            description: Administrative distance
            type: dict
            suboptions:
              distance:
                description:
                  - Administrative distance
                  - Please refer vendor documentation for valid values
                type: int
              address:
                description: IP Source address (A.B.C.D)
                type: str
              wildcard_bit:
                description: Wildcard bits (A.B.C.D)
                type: str
              acl:
                description:
                  - IP Standard access list number
                  - IP Standard expanded access list number
                  - Standard access-list name
                type: str
          bgp:
            description: BGP distance
            type: dict
            suboptions:
              routes_external:
                description:
                  - Distance for routes external to the AS
                  - Please refer vendor documentation for valid values
                type: int
              routes_internal:
                description:
                  - Distance for routes internal to the AS
                  - Please refer vendor documentation for valid values
                type: int
              routes_local:
                description:
                  - Distance for local routes
                  - Please refer vendor documentation for valid values
                type: int
          mbgp:
            description: MBGP distance
            type: dict
            suboptions:
              routes_external:
                description:
                  - Distance for routes external to the AS
                  - Please refer vendor documentation for valid values
                type: int
              routes_internal:
                description:
                  - Distance for routes internal to the AS
                  - Please refer vendor documentation for valid values
                type: int
              routes_local:
                description:
                  - Distance for local routes
                  - Please refer vendor documentation for valid values
                type: int
      distributes:
        description: Filter networks in routing updates
        type: list
        elements: dict
        suboptions:
          prefix:
            description: Filtering incoming updates based on gateway
            type: str
          gateway:
            description: Filter prefixes in routing updates
            type: str
          acl:
            description: IP access list number/name
            type: str
          in:
            description: Filter incoming routing updates
            type: bool
          out:
            description: Filter outgoing routing updates
            type: bool
          interface:
            description: interface details
            type: str
      distribute_list:
        description:
        - Filter networks in routing updates
        - This option is DEPRECATED and is replaced with distributes which is of type list of dict,
          this attribute will be removed after 2024-06-01.
        type: dict
        suboptions:
          acl:
            description: IP access list number/name
            type: str
          in:
            description: Filter incoming routing updates
            type: bool
          out:
            description: Filter outgoing routing updates
            type: bool
          interface:
            description: interface details
            type: str
      maximum_paths:
        description: Forward packets over multiple paths
        type: dict
        suboptions:
          paths:
            description: Number of paths
            type: int
          eibgp:
            description: Both eBGP and iBGP paths as multipath
            type: int
          ibgp:
            description: iBGP-multipath
            type: int
      maximum_secondary_paths:
        description: Maximum secondary paths
        type: dict
        suboptions:
          paths:
            description: Number of secondary paths
            type: int
          eibgp:
            description: Both eBGP and iBGP paths as secondary multipath
            type: int
          ibgp:
            description: iBGP-secondary-multipath
            type: int
      neighbors:
        description: Specify a neighbor router
        type: list
        elements: dict
        aliases:
          - neighbor
        suboptions:
          neighbor_address:
            description:
            - Neighbor address (A.B.C.D)
            - Neighbor tag
            - Neighbor ipv6 address (X:X:X:X::X)
            type: str
          address:
            description:
            - Neighbor address (A.B.C.D)
            - This option is DEPRECATED and replaced with neighbor_address,
              this attribute will be removed after 2024-06-01.
            type: str
          tag:
            description:
            - Neighbor tag
            - This option is DEPRECATED and replaced with neighbor_address,
              this attribute will be removed after 2024-06-01.
            type: str
          ipv6_adddress:
            description:
            - Neighbor ipv6 address (X:X:X:X::X)
            - This option is DEPRECATED and replaced with neighbor_address,
              this attribute will be removed after 2024-06-01.
            type: str
          activate:
            description: Enable the Address Family for this Neighbor
            type: bool
          additional_paths:
            description: Negotiate additional paths capabilities with this neighbor
            type: dict
            suboptions:
              disable:
                description: Disable additional paths for this neighbor
                type: bool
              receive:
                description: Receive additional paths from neighbors
                type: bool
              send:
                description: Send additional paths to neighbors
                type: bool
          advertise:
            description: Advertise to this neighbor
            type: dict
            suboptions:
              additional_paths:
                description: Advertise additional paths
                type: dict
                suboptions:
                  all:
                    description: Select all available paths
                    type: bool
                  best:
                    description: Select best N paths (2-3).
                    type: int
                  group_best:
                    description: Select group-best path
                    type: bool
              best_external:
                description: Advertise best-external (at RRs best-internal) path
                type: bool
              diverse_path:
                description: Advertise additional paths
                type: dict
                suboptions:
                  backup:
                    description: Diverse path can be backup path
                    type: bool
                  mpath:
                    description: Diverse path can be multipath
                    type: bool
          advertise_map:
            description: specify route-map for conditional advertisement
            type: dict
            suboptions:
              name:
                description: advertise route-map name
                type: str
              exist_map:
                description:
                  - advertise prefix only if prefix is in the condition exists
                  - condition route-map name
                type: str
              non_exist_map:
                description:
                  - advertise prefix only if prefix in the condition does not exist
                  - condition route-map name
                type: str
          advertisement_interval:
            description: Minimum interval between sending BGP routing updates
            type: int
          aigp:
            description: AIGP on neighbor
            type: dict
            suboptions:
              enable:
                description: Enable AIGP
                type: bool
              send:
                description: Cost community or MED carrying AIGP VALUE
                type: dict
                suboptions:
                  cost_community:
                    description: Cost extended community carrying AIGP Value
                    type: dict
                    suboptions:
                      id:
                        description:
                          - Community ID
                          - Please refer vendor documentation for valid values
                        type: int
                      poi:
                        description: Point of Insertion
                        type: dict
                        suboptions:
                          igp_cost:
                            description:  Point of Insertion After IGP
                            type: bool
                          pre_bestpath:
                            description: Point of Insertion At Beginning
                            type: bool
                          transitive:
                            description: Cost community is Transitive
                            type: bool
                  med:
                    description: Med carrying AIGP Value
                    type: bool
          allow_policy:
            description: Enable the policy support for this IBGP Neighbor
            type: bool
          allowas_in:
            description: Accept as-path with my AS present in it
            type: int
          as_override:
            description:
              - Override matching AS-number while sending update
              - Maintain Split Horizon while sending update
            type: bool
          bmp_activate:
            description: Activate the BMP monitoring for a BGP peer
            type: dict
            suboptions:
              all:
                description: Activate BMP monitoring for all servers
                type: bool
              server:
                description:
                  - Activate BMP for server
                  - BMP Server Number
                  - Please refer vendor documentation for valid values
                type: int
          capability:
            description:
              - Advertise capability to the peer
              - Advertise ORF capability to the peer
              - Advertise prefix-list ORF capability to this neighbor
            type: dict
            suboptions:
              both:
                description: Capability to SEND and RECEIVE the ORF to/from this neighbor
                type: bool
              receive:
                description: Capability to RECEIVE the ORF from this neighbor
                type: bool
              send:
                description: Capability to SEND the ORF to this neighbor
                type: bool
          cluster_id:
            description:
              - Configure Route-Reflector Cluster-id (peers may reset)
              - Route-Reflector Cluster-id as 32 bit quantity, or
                Route-Reflector Cluster-id in IP address format (A.B.C.D)
            type: str
          default_originate:
            description: Originate default route to this neighbor
            type: dict
            suboptions:
              set:
                description: Originate default route to this neighbor
                type: bool
              route_map:
                description: Route-map to specify criteria to originate default
                type: str
          description:
            description: Neighbor specific description
            type: str
          disable_connected_check:
            description: one-hop away EBGP peer using loopback address
            type: bool
          distribute_list:
            description: Filter updates to/from this neighbor
            type: dict
            suboptions:
              acl:
                description: IP access list number/name
                type: str
              in:
                description: Filter incoming updates
                type: bool
              out:
                description: Filter outgoing updates
                type: bool
          dmzlink_bw:
            description: Propagate the DMZ link bandwidth
            type: bool
          ebgp_multihop:
            description: Allow EBGP neighbors not on directly connected networks
            type: dict
            suboptions:
              enable:
                description: Allow EBGP neighbors not on directly connected networks
                type: bool
              hop_count:
                description:
                  - Maximum hop count
                  - Please refer vendor documentation for valid values
                type: int
          fall_over:
            description: Session fall on peer route lost
            type: dict
            suboptions:
              bfd:
                description: Use BFD to detect failure
                type: dict
                suboptions:
                  set:
                    description: set bfd
                    type: bool
                  multi_hop:
                    description: Force BFD multi-hop to detect failure
                    type: bool
                  single_hop:
                    description: Force BFD single-hop to detect failure
                    type: bool
              route_map:
                description: Route map for peer route
                type: str
          filter_list:
            description: Establish BGP filters
            type: dict
            suboptions:
              path_acl:
                description: AS path access list
                type: str
              in:
                description: Filter incoming updates
                type: bool
              out:
                description: Filter outgoing updates
                type: bool
          ha_mode:
            description: high availability mode
            type: dict
            suboptions:
              set:
                description: set ha-mode and graceful-restart for this peer
                type: bool
              disable:
                description: disable graceful-restart
                type: bool
          inherit:
            description:
              - Inherit a template
              - Inherit a peer-session template and Template name
            type: str
          local_as:
            description: Specify a local-as number
            type: dict
            suboptions:
              set:
                description: set local-as number
                type: bool
              number:
                description:
                  - AS number used as local AS
                  - Please refer vendor documentation for valid values
                type: int
              dual_as:
                description: Accept either real AS or local AS from the ebgp peer
                type: bool
              no_prepend:
                description: Do not prepend local-as to updates from ebgp peers
                type: dict
                suboptions:
                  set:
                    description: Set prepend
                    type: bool
                  replace_as:
                    description: Replace real AS with local AS in the EBGP updates
                    type: bool
          log_neighbor_changes:
            description: Log neighbor up/down and reset reason
            type: dict
            suboptions:
              set:
                description: set Log neighbor up/down and reset
                type: bool
              disable:
                description: disable Log neighbor up/down and reset
                type: bool
          maximum_prefix:
            description: Maximum number of prefixes accepted from this peer
            type: dict
            suboptions:
              max_no:
                description: maximum no. of prefix limit
                type: int
              threshold_val:
                description: Threshold value (%) at which to generate a warning msg
                type: int
              restart:
                description: Restart bgp connection after limit is exceeded
                type: int
              warning_only:
                description: Only give warning message when limit is exceeded
                type: bool
          next_hop_self:
            description: Disable the next hop calculation for this neighbor
            type: dict
            suboptions:
              set:
                description: Enable next-hop-self
                type: bool
              all:
                description: Enable next-hop-self for both eBGP and iBGP received paths
                type: bool
          next_hop_unchanged:
            description:
              - Propagate next hop unchanged for iBGP paths to this neighbor
              - Propagate next hop unchanged for all paths (iBGP and eBGP) to this neighbor
            type: dict
            suboptions:
              set:
                description: Enable next-hop-unchanged
                type: bool
              allpaths:
                description: Propagate next hop unchanged for all paths (iBGP and eBGP) to this neighbor
                type: bool
          password:
            description:
            - Set a password
            - This option is DEPRECATED and is replaced with password_options which
              accepts dict as input, this attribute will be removed after 2024-06-01.
            type: str
          password_options:
            description: Set a password with encryption type
            type: dict
            suboptions:
              encryption:
                description: Encryption type (0 to disable encryption, 7 for proprietary)
                type: int
              pass_key:
                description: The password
                type: str
          path_attribute:
            description: BGP optional attribute filtering
            type: dict
            suboptions:
              discard:
                description: Discard matching path-attribute for this neighbor
                type: dict
                suboptions:
                  type:
                    description:
                      - path attribute type
                      - Please refer vendor documentation for valid values
                    type: int
                  range:
                    description: path attribute range
                    type: dict
                    suboptions:
                      start:
                        description:
                          - path attribute range start value
                          - Please refer vendor documentation for valid values
                        type: int
                      end:
                        description:
                          - path attribute range end value
                          - Please refer vendor documentation for valid values
                        type: int
                  in:
                    description: Perform inbound path-attribute filtering
                    type: bool
              treat_as_withdraw:
                description: Treat-as-withdraw matching path-attribute for this neighbor
                type: dict
                suboptions:
                  type:
                    description:
                      - path attribute type
                      - Please refer vendor documentation for valid values
                    type: int
                  range:
                    description: path attribute range
                    type: dict
                    suboptions:
                      start:
                        description:
                          - path attribute range start value
                          - Please refer vendor documentation for valid values
                        type: int
                      end:
                        description:
                          - path attribute range end value
                          - Please refer vendor documentation for valid values
                        type: int
                  in:
                    description: Perform inbound path-attribute filtering
                    type: bool
          peer_group:
            description: Member of the peer-group
            type: str
          remote_as:
            description:
              - Specify a BGP neighbor
              - AS of remote neighbor
            type: str
          remove_private_as:
            description: Remove private AS number from outbound updates
            type: dict
            suboptions:
              set:
                description: Remove private AS number
                type: bool
              all:
                description: Remove all private AS numbers
                type: bool
              replace_as:
                description: Replace all private AS numbers with local AS
                type: bool
          route_map:
            description:
            - Apply route map to neighbor
            - This option is DEPRECATED and is replaced with route_maps which
              accepts list of dict as input, this attribute will be removed after 2024-06-01.
            type: dict
            suboptions:
              name:
                description: Replace all private AS numbers with local AS
                type: str
              in:
                description: Apply map to incoming routes
                type: bool
              out:
                description: Apply map to outbound routes
                type: bool
          route_maps:
            description: Apply a list of route maps to neighbor
            type: list
            elements: dict
            suboptions:
              name:
                description: Replace all private AS numbers with local AS
                type: str
              in:
                description: Apply map to incoming routes
                type: bool
              out:
                description: Apply map to outbound routes
                type: bool
          route_reflector_client:
            description: Configure a neighbor as Route Reflector client
            type: bool
          route_server_client:
            description: Configure a neighbor as Route Server client
            type: dict
            suboptions:
              set:
                description: Set Route Server client
                type: bool
              context:
                description:
                  - Specify Route Server context for neighbor
                  - Route Server context name
                type: str
          send_community:
            description: Send Community attribute to this neighbor
            type: dict
            suboptions:
              set:
                description: Set send Community attribute to this neighbor
                type: bool
              both:
                description: Send Standard and Extended Community attributes
                type: bool
              extended:
                description: Send Extended Community attribute
                type: bool
              standard:
                description: Send Standard Community attribute
                type: bool
          send_label:
            description: Send NLRI + MPLS Label to this peer
            type: dict
            suboptions:
              set:
                description: Set send NLRI + MPLS Label to this peer
                type: bool
              explicit_null:
                description: Advertise Explicit Null label in place of Implicit Null
                type: bool
          shutdown:
            description: Administratively shut down this neighbor
            type: dict
            suboptions:
              set:
                description: shut down
                type: bool
              graceful:
                description:
                  - Gracefully shut down this neighbor
                  - time in seconds
                  - Please refer vendor documentation for valid values
                type: int
              community:
                description: Set Community for Gshut routes
                type: int
              local_preference:
                description: Set Local Preference for Gshut routes
                type: bool
          slow_peer:
            description: Configure slow-peer
            type: dict
            suboptions:
              detection:
                description: Configure slow-peer
                type: dict
                suboptions:
                  enable:
                    description: Enable slow-peer detection
                    type: bool
                  disable:
                    description: Disable slow-peer detection
                    type: bool
                  threshold:
                    description: Set the slow-peer detection threshold
                    type: int
              split_update_group:
                description: Configure slow-peer split-update-group
                type: dict
                suboptions:
                  dynamic:
                    description: Dynamically split the slow peer to slow-update group
                    type: dict
                    suboptions:
                      enable:
                        description: Enable slow-peer detection
                        type: bool
                      disable:
                        description: Disable slow-peer detection
                        type: bool
                      permanent:
                        description: Keep the slow-peer permanently in slow-update group
                        type: bool
                  static:
                    description: Static slow-peer
                    type: bool
          soft_reconfiguration:
            description:
              - Per neighbor soft reconfiguration
              - Allow inbound soft reconfiguration for this neighbor
            type: bool
          timers:
            description: BGP per neighbor timers
            type: dict
            suboptions:
              interval:
                description: Keepalive interval
                type: int
              holdtime:
                description: Holdtime
                type: int
              min_holdtime:
                description: Minimum hold time from neighbor
                type: int
          translate_update:
            description: Translate Update to MBGP format
            type: dict
            suboptions:
              set:
                description: Set Translate Update
                type: bool
              nlri:
                description: Specify type of nlri to translate to
                type: dict
                suboptions:
                  multicast:
                    description: Translate Update to multicast nlri
                    type: bool
                  unicast:
                    description: Process Update as unicast nlri
                    type: bool
          transport:
            description: Transport options
            type: dict
            suboptions:
              connection_mode:
                description: Specify passive or active connection
                type: dict
                suboptions:
                  active:
                    description: Actively establish the TCP session
                    type: bool
                  passive:
                    description: Passively establish the TCP session
                    type: bool
              multi_session:
                description: Use Multi-session for transport
                type: bool
              path_mtu_discovery:
                description: Use transport path MTU discovery
                type: dict
                suboptions:
                  set:
                    description: Use path MTU discovery
                    type: bool
                  disable:
                    description: disable
                    type: bool
          ttl_security:
            description:
              - BGP ttl security check
              - maximum number of hops
              - Please refer vendor documentation for valid values
            type: int
          unsuppress_map:
            description:
              - Route-map to selectively un-suppress suppressed routes
              - Name of route map
            type: str
          update_source:
            description: Source of routing updates
            type: str
          version:
            description:
              - Set the BGP version to match a neighbor
              - Neighbor's BGP version
              - Please refer vendor documentation for valid values
            type: int
          weight:
            description: Set default weight for routes from this neighbor
            type: int
      networks:
        description:  Specify a network to announce via BGP
        type: list
        elements: dict
        suboptions:
          address:
            description: Specify network address
            type: str
          netmask:
            description: Specify network mask
            type: str
          route_map:
            description: Route-map to modify the attributes
            type: str
          backdoor:
            description:  Specify a BGP backdoor route
            type: bool
      redistribute:
        description: Redistribute information from another routing protocol
        type: list
        elements: dict
        suboptions:
          application:
            description: Application
            type: dict
            suboptions:
              name:
                description: Application name
                type: str
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          bgp:
            description: Border Gateway Protocol (BGP)
            type: dict
            suboptions:
              as_number:
                description: Autonomous system number
                type: str
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          connected:
            description: Connected
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          eigrp:
            description: Enhanced Interior Gateway Routing Protocol (EIGRP)
            type: dict
            suboptions:
              as_number:
                description: Autonomous system number
                type: str
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          isis:
            description: ISO IS-IS
            type: dict
            suboptions:
              area_tag:
                description: ISO routing area tag
                type: str
              clns:
                description: Redistribution of OSI dynamic routes
                type: bool
              ip:
                description: Redistribution of IP dynamic routes
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          iso_igrp:
            description: IGRP for OSI networks
            type: dict
            suboptions:
              area_tag:
                description: ISO routing area tag
                type: str
              route_map:
                description: Route map reference
                type: str
          lisp:
            description: Locator ID Separation Protocol (LISP)
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          mobile:
            description: Mobile routes
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          odr:
            description: On Demand stub Routes
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          ospf:
            description: Open Shortest Path First (OSPF)
            type: dict
            suboptions:
              process_id:
                description: Process ID
                type: int
              match:
                description: On Demand stub Routes
                type: dict
                suboptions:
                  external:
                    description: Redistribute OSPF external routes
                    type: bool
                  internal:
                    description: Redistribute OSPF internal routes
                    type: bool
                  nssa_external:
                    description: Redistribute OSPF NSSA external routes
                    type: bool
                  type_1:
                    description: Redistribute NSSA external type 1 routes
                    type: bool
                  type_2:
                    description: Redistribute NSSA external type 2 routes
                    type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
              vrf:
                description: VPN Routing/Forwarding Instance
                type: str
          ospfv3:
            description: OSPFv3
            type: dict
            suboptions:
              process_id:
                description: Process ID
                type: int
              match:
                description: On Demand stub Routes
                type: dict
                suboptions:
                  external:
                    description: Redistribute OSPF external routes
                    type: bool
                  internal:
                    description: Redistribute OSPF internal routes
                    type: bool
                  nssa_external:
                    description: Redistribute OSPF NSSA external routes
                    type: bool
                  type_1:
                    description: Redistribute NSSA external type 1 routes
                    type: bool
                  type_2:
                    description: Redistribute NSSA external type 2 routes
                    type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          rip:
            description: Routing Information Protocol (RIP)
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          static:
            description: Static routes
            type: dict
            suboptions:
              set:
                description: Set the top level attribute
                type: bool
              clns:
                description: Redistribution of OSI static routes
                type: bool
              ip:
                description: Redistribution of IP static routes
                type: bool
              metric:
                description: Metric for redistributed routes
                type: int
              route_map:
                description: Route map reference
                type: str
          vrf:
            description: Specify a source VRF
            type: dict
            suboptions:
              name:
                description: Source VRF name
                type: str
              global:
                description: global VRF
                type: bool
      route_server_context:
        description:
        - Enter route server context command mode
        - This option is DEPRECATED as it is out of scope of the module,
          this attribute will be removed after 2024-06-01.
        type: dict
        suboptions:
          name:
            description: Name of route server context
            type: str
          address_family:
            description: Enter address family command mode
            type: dict
            suboptions:
              afi:
                description: Address family
                type: str
                choices: ['ipv4', 'ipv6']
              modifier:
                description: Address Family modifier
                type: str
                choices: ['multicast', 'unicast']
              import_map:
                description:
                  - Import matching routes using a route map
                  - Name of route map
                type: str
          description:
            description: Textual description of the router server context
            type: str
      scope:
        description:
        - Enter scope command mode
        - This option is DEPRECATED as is not valid within the scope of module,
          this attribute will be removed after 2024-06-01.
        type: dict
        suboptions:
          global:
            description: Global scope
            type: bool
          vrf:
            description:
              - VRF scope
              - VPN Routing/Forwarding instance name
            type: str
      synchronization:
        description: Perform IGP synchronization
        type: bool
      table_map:
        description: Map external entry attributes into routing table
        type: dict
        suboptions:
          name:
            description: route-map name
            type: str
          filter:
            description: Selective route download
            type: bool
      template:
        description:
        - Enter template command mode
        - This option is DEPRECATED as is not valid within the scope of module,
          this attribute will be removed after 2024-06-01.
        type: dict
        suboptions:
          peer_policy:
            description: Template configuration for policy parameters
            type: str
          peer_session:
            description: Template configuration for session parameters
            type: str
      timers:
        description:
          - Adjust routing timers
          - BGP timers
        type: dict
        suboptions:
          keepalive:
            description: Keepalive interval
            type: int
          holdtime:
            description: Holdtime
            type: int
          min_holdtime:
            description: Minimum hold time from neighbor
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
    choices:
      - merged
      - replaced
      - deleted
      - purged
      - gathered
      - rendered
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
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""


EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp

- name: Merge provided configuration with device configuration
  cisco.ios.ios_bgp_global:
    config:
      as_number: 65000
      bgp:
        advertise_best_external: true
        bestpath:
          - compare_routerid: true
        dampening:
          penalty_half_time: 1
          reuse_route_val: 1
          suppress_route_val: 1
          max_suppress: 1
        graceful_shutdown:
          neighbors:
            time: 50
          community: 100
          local_preference: 100
        log_neighbor_changes: true
        nopeerup_delay:
          - post_boot: 10
      networks:
        - address: 192.0.2.3
        - address: 192.0.2.2
      neighbor:
        - address: 192.0.2.1
          description: merge neighbor
          remote_as: 100
          aigp:
            send:
              cost_community:
                id: 100
                poi:
                  igp_cost: true
                  transitive: true
          route_map:
            name: test-route
            out: true
      redistribute:
        - connected:
            metric: 10
      timers:
        keepalive: 100
        holdtime: 200
        min_holdtime: 150
    state: merged

# Task Output:
# ---------------

# after:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       compare_routerid: true
#     dampening:
#       max_suppress: 1
#       penalty_half_time: 1
#       reuse_route_val: 1
#       suppress_route_val: 1
#     graceful_shutdown:
#       community: '100'
#       local_preference: 100
#       neighbors:
#         time: 50
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       post_boot: 10
#   neighbors:
#   - aigp:
#       send:
#         cost_community:
#           id: 100
#           poi:
#             igp_cost: true
#             transitive: true
#     description: merge neighbor
#     neighbor_address: 192.0.2.1
#     remote_as: '100'
#     route_maps:
#     - name: test-route
#       out: true
#   networks:
#   - address: 192.0.2.2
#   - address: 192.0.2.3
#   redistribute:
#   - connected:
#       metric: 10
#       set: true
#   timers:
#     holdtime: 200
#     keepalive: 100
#     min_holdtime: 150

# commands:
# - router bgp 65000
# - timers bgp 100 200 150
# - bgp advertise-best-external
# - bgp bestpath compare-routerid
# - bgp dampening 1 1 1 1
# - bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
# - bgp log-neighbor-changes
# - bgp nopeerup-delay post-boot 10
# - network 192.0.2.3
# - network 192.0.2.2
# - neighbor 192.0.2.1 remote-as 100
# - neighbor 192.0.2.1 description merge neighbor
# - neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
# - neighbor 192.0.2.1 route-map test-route out
# - redistribute connected metric 10

# After state:
# ------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  bgp advertise-best-external
#  network 192.0.2.2
#  network 192.0.2.3
#  timers bgp 100 200 150
#  redistribute connected metric 10
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description merge neighbor
#  neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 192.0.2.1 route-map test-route out


# Using replaced

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  network 192.0.2.2
#  network 192.0.2.3
#  bgp advertise-best-external
#  neighbor 198.0.2.1 remote-as 100
#  neighbor 198.0.2.1 description merge neighbor
#  neighbor 198.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 198.0.2.1 route-map test-route out


- name: Replaces device configuration of listed global BGP with provided configuration
  cisco.ios.ios_bgp_global:
    config:
      as_number: 65000
      bgp:
        advertise_best_external: true
        bestpath:
          - med:
              confed: true
        log_neighbor_changes: true
        nopeerup_delay:
          - post_boot: 10
            cold_boot: 20
      networks:
        - address: 192.0.2.4
      neighbor:
        - address: 192.0.2.5
          description:  replace neighbor
          remote_as: 100
          slow_peer:
            detection:
              disable: true
    state: replaced

# Task Output:
# ---------------
#
# before:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       compare_routerid: true
#     dampening:
#       max_suppress: 1
#       penalty_half_time: 1
#       reuse_route_val: 1
#       suppress_route_val: 1
#     graceful_shutdown:
#       community: '100'
#       local_preference: 100
#       neighbors:
#         time: 50
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       post_boot: 10
#   neighbors:
#   - aigp:
#       send:
#         cost_community:
#           id: 100
#           poi:
#             igp_cost: true
#             transitive: true
#     description: merge neighbor
#     neighbor_address: 198.0.2.1
#     remote_as: '100'
#     route_maps:
#     - name: test-route
#       out: true
#   networks:
#   - address: 192.0.2.2
#   - address: 192.0.2.3

# after:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       med:
#         confed: true
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       cold_boot: 20
#       post_boot: 10
#   neighbors:
#   - description: replace neighbor
#     neighbor_address: 192.0.2.5
#     remote_as: '100'
#     slow_peer:
#       detection:
#         disable: true
#   networks:
#   - address: 192.0.2.4

# commands:
# - router bgp 65000
# - no bgp bestpath compare-routerid
# - bgp bestpath med confed
# - no bgp dampening 1 1 1 1
# - no bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
# - bgp nopeerup-delay cold-boot 20
# - network 192.0.2.4
# - no network 192.0.2.2
# - no network 192.0.2.3
# - neighbor 192.0.2.5 remote-as 100
# - neighbor 192.0.2.5 description replace neighbor
# - neighbor 192.0.2.5 slow-peer detection disable
# - no neighbor 198.0.2.1

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  bgp nopeerup-delay post-boot 10
#  bgp bestpath med confed
#  bgp advertise-best-external
#  network 192.0.2.4
#  neighbor 192.0.2.5 remote-as 100
#  neighbor 192.0.2.5 description replace neighbor
#  neighbor 192.0.2.5 slow-peer detection disable

# Using Deleted

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  bgp advertise-best-external
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description merge neighbor
#  neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 192.0.2.1 route-map test-route out

- name: "Delete global BGP (Note: This won't delete the configured global BGP)"
  cisco.ios.ios_bgp_global:
    config:
      as_number: 65000
    state: deleted

# Task Output:
# ---------------

# before:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       compare_routerid: true
#     dampening:
#       max_suppress: 1
#       penalty_half_time: 1
#       reuse_route_val: 1
#       suppress_route_val: 1
#     graceful_shutdown:
#       community: '100'
#       local_preference: 100
#       neighbors:
#         time: 50
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       post_boot: 10
#   neighbors:
#   - aigp:
#       send:
#         cost_community:
#           id: 100
#           poi:
#             igp_cost: true
#             transitive: true
#     description: merge neighbor
#     neighbor_address: 192.0.2.1
#     remote_as: '100'
#     route_maps:
#     - name: test-route
#       out: true

# after:
#   as_number: '65000'

# commands:
# - router bgp 65000
# - no bgp advertise-best-external
# - no bgp bestpath compare-routerid
# - no bgp dampening 1 1 1 1
# - no bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
# - no bgp log-neighbor-changes
# - no bgp nopeerup-delay post-boot 10
# - no neighbor 192.0.2.1

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000


# Using Deleted without any config passed
#"(NOTE: This will delete all of configured global BGP)"

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  bgp advertise-best-external
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description merge neighbor
#  neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 192.0.2.1 route-map test-route out


- name: "Delete global BGP without config"
  cisco.ios.ios_bgp_global:
    state: deleted

# Task Output:
# ---------------

# before:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       compare_routerid: true
#     dampening:
#       max_suppress: 1
#       penalty_half_time: 1
#       reuse_route_val: 1
#       suppress_route_val: 1
#     graceful_shutdown:
#       community: '100'
#       local_preference: 100
#       neighbors:
#         time: 50
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       post_boot: 10
#   neighbors:
#   - aigp:
#       send:
#         cost_community:
#           id: 100
#           poi:
#             igp_cost: true
#             transitive: true
#     description: merge neighbor
#     neighbor_address: 192.0.2.1
#     remote_as: '100'
#     route_maps:
#     - name: test-route
#       out: true

# after:
#   as_number: '65000'

# commands:
# - router bgp 65000
# - no bgp advertise-best-external
# - no bgp bestpath compare-routerid
# - no bgp dampening 1 1 1 1
# - no bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
# - no bgp nopeerup-delay post-boot 10
# - no neighbor 198.51.100.1

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000

# Using Purged
#"(NOTE: This WILL delete the configured global BGP)"

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  bgp advertise-best-external
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description merge neighbor
#  neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 192.0.2.1 route-map test-route out


- name: 'Delete the configured global BGP (Note: This WILL delete the the configured
    global BGP)'
  cisco.ios.ios_bgp_global:
    state: purged

# Task Output:
# ---------------

# before:
#   as_number: '65000'
#   bgp:
#     advertise_best_external: true
#     bestpath_options:
#       compare_routerid: true
#     dampening:
#       max_suppress: 1
#       penalty_half_time: 1
#       reuse_route_val: 1
#       suppress_route_val: 1
#     graceful_shutdown:
#       community: '100'
#       local_preference: 100
#       neighbors:
#         time: 50
#     log_neighbor_changes: true
#     nopeerup_delay_options:
#       post_boot: 10
#   neighbors:
#   - aigp:
#       send:
#         cost_community:
#           id: 100
#           poi:
#             igp_cost: true
#             transitive: true
#     description: merge neighbor
#     neighbor_address: 192.0.2.1
#     remote_as: '100'
#     route_maps:
#     - name: test-route
#       out: true

# commands:
#  - no router bgp 65000

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp nopeerup-delay post-boot 10
#  bgp graceful-shutdown all neighbors 50 local-preference 100 community 100
#  bgp bestpath compare-routerid
#  bgp dampening 1 1 1 1
#  bgp advertise-best-external
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description merge neighbor
#  neighbor 192.0.2.1 aigp send cost-community 100 poi igp-cost transitive
#  neighbor 192.0.2.1 route-map test-route out


- name: Gather listed global BGP with provided configurations
  cisco.ios.ios_bgp_global:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": {
#         "as_number": "65000",
#         "bgp": {
#             "advertise_best_external": true,
#             "bestpath_options": {
#                 "compare_routerid": true
#             },
#             "dampening": {
#                 "max_suppress": 1,
#                 "penalty_half_time": 1,
#                 "reuse_route_val": 1,
#                 "suppress_route_val": 1
#             },
#             "graceful_shutdown": {
#                 "community": "100",
#                 "local_preference": 100,
#                 "neighbors": {
#                     "time": 50
#                 }
#             },
#             "nopeerup_delay_options": {
#                 "post_boot": 10
#             }
#         },
#         "neighbors": [
#             {
#                 "aigp": {
#                     "send": {
#                         "cost_community": {
#                             "id": 100,
#                             "poi": {
#                                 "igp_cost": true,
#                                 "transitive": true
#                             }
#                         }
#                     }
#                 },
#                 "description": "merge neighbor",
#                 "neighbor_address": "192.0.2.1",
#                 "remote_as": "100",
#                 "route_maps": [
#                     {
#                         "name": "test-route",
#                         "out": true
#                     }
#                 ]
#             }
#         ]
#     },
#     "invocation": {
#         "module_args": {
#             "config": null,
#             "running_config": null,
#             "state": "gathered"
#         }
#     }
# }

# Using Rendered

- name: Rendered the provided configuration with the existing running configuration
  cisco.ios.ios_bgp_global:
    config: >-
        {{
            {
            "aggregate_addresses": [
                {
                    "address": "192.0.2.1",
                    "attribute_map": "testMap1",
                    "netmask": "255.255.255.0",
                    "summary_only": true
                },
                {
                    "address": "192.0.2.2",
                    "as_set": true,
                    "netmask": "255.255.255.0"
                },
                {
                    "address": "192.0.2.3",
                    "as_set": true,
                    "netmask": "255.255.255.0"
                }
            ],
            "as_number": "65000",
            "auto_summary": true,
            "bgp": {
                "additional_paths": {
                    "install": true,
                    "receive": true
                },
                "aggregate_timer": 0,
                "always_compare_med": true,
                "asnotation": true,
                "bestpath_options": {
                    "aigp": true,
                    "compare_routerid": true,
                    "med": {
                        "confed": true,
                        "missing_as_worst": true
                    }
                },
                "confederation": {
                    "identifier": "22"
                },
                "consistency_checker": {
                    "error_message": {
                        "interval": 10,
                        "set": true
                    }
                },
                "dampening": {
                    "route_map": "routeMap1Test"
                },
                "deterministic_med": true,
                "graceful_restart": {
                    "restart_time": 2,
                    "stalepath_time": 22
                },
                "graceful_shutdown": {
                    "community": "77",
                    "local_preference": 230,
                    "vrfs": {
                        "time": 31
                    }
                },
                "inject_maps": [
                    {
                        "copy_attributes": true,
                        "exist_map_name": "Testmap3",
                        "name": "map2"
                    },
                    {
                        "copy_attributes": true,
                        "exist_map_name": "Testmap2",
                        "name": "map1"
                    }
                ],
                "listen": {
                    "limit": 200,
                    "range": {
                        "host_with_subnet": "192.0.2.1/24",
                        "peer_group": "PaulNetworkGroup"
                    }
                },
                "log_neighbor_changes": true,
                "maxas_limit": 2,
                "maxcommunity_limit": 3,
                "maxextcommunity_limit": 3,
                "nexthop": {
                    "route_map": "RouteMap1",
                    "trigger": {
                        "delay": 2
                    }
                },
                "nopeerup_delay_options": {
                    "cold_boot": 2,
                    "nsf_switchover": 10,
                    "post_boot": 22,
                    "user_initiated": 22
                },
                "recursion": true,
                "redistribute_internal": true,
                "refresh": {
                    "max_eor_time": 700,
                    "stalepath_time": 800
                },
                "router_id": {
                    "vrf": true
                },
                "scan_time": 22,
                "slow_peer": {
                    "detection": {
                        "threshold": 345
                    },
                    "split_update_group": {
                        "dynamic": true,
                        "permanent": true
                    }
                },
                "sso": true,
                "suppress_inactive": true,
                "update_delay": 2,
                "update_group": true
            },
            "bmp": {
                "buffer_size": 22,
                "server": 2
            },
            "distance": {
                "bgp": {
                    "routes_external": 2,
                    "routes_internal": 3,
                    "routes_local": 4
                },
                "mbgp": {
                    "routes_external": 2,
                    "routes_internal": 3,
                    "routes_local": 5
                }
            },
            "distributes": [
                {
                    "in": true,
                    "prefix": "prefixTest"
                },
                {
                    "out": true,
                    "gateway": "gatewayTest"
                },
                {
                    "out": true,
                    "acl": "300",
                    "interface": "Loopback0"
                }
            ],
            "maximum_paths": {
                "ibgp": 2,
                "paths": 2
            },
            "maximum_secondary_paths": {
                "ibgp": 22,
                "paths": 22
            },
            "neighbors": [
                {
                    "advertise": {
                        "diverse_path": {
                            "backup": true
                        }
                    },
                    "neighbor_address": "192.0.2.8",
                    "route_reflector_client": true
                },
                {
                    "neighbor_address": "192.0.2.9",
                    "remote_as": 64500,
                    "update_source": "Loopback0",
                    "route_maps":[{
                        "name": "rmp1",
                        "in": true,
                    },{
                        "name": "rmp2",
                        "in": true,
                    },]
                },
                {
                    "neighbor_address": "192.0.2.10",
                    "remote_as": 64500,
                    "update_source": "Loopback1"
                },
                {
                    "activate": true,
                    "neighbor_address": "192.0.2.11",
                    "remote_as": 45000,
                    "send_community": {
                        "extended": true
                    }
                },
                {
                    "activate": true,
                    "neighbor_address": "192.0.2.12",
                    "remote_as": 45000
                },
                {
                    "neighbor_address": "192.0.2.13",
                    "remote_as": 6553601,
                    "shutdown": {
                        "set": true,
                        "graceful": 10,
                        "community": 20,
                    }
                },
                {
                    "activate": true,
                    "advertise": {
                        "additional_paths": {
                            "group_best": true
                        }
                    },
                    "neighbor_address": "2001:DB8::1037"
                },
                {
                    "neighbor_address": "testNebTag",
                    "peer_group": "5",
                    "soft_reconfiguration": true,
                    "version": 4
                }
            ],
            "networks": [
                {
                    "address": "192.0.2.15",
                    "backdoor": true,
                    "netmask": "55.255.255.0",
                    "route_map": "mp1"
                },
                {
                    "address": "192.0.2.16",
                    "backdoor": true,
                    "netmask": "255.255.255.0",
                    "route_map": "mp2"
                },
                {
                    "address": "192.0.2.17",
                    "backdoor": true,
                    "netmask": "255.255.255.0",
                    "route_map": "mp2"
                }
            ],
            "redistribute": [
                {
                    "static": {
                        "metric": 33,
                        "route_map": "rmp1"
                    }
                },
                {
                    "application": {
                        "metric": 22,
                        "name": "app1"
                    }
                },
                {
                    "application": {
                        "metric": 33,
                        "name": "app2",
                        "route_map": "mp1"
                    }
                },
                {
                    "connected": {
                        "metric": 22
                    }
                },
                {
                    "mobile": {
                        "metric": 211
                    }
                }
            ],
            "route_server_context": {
                "description": "checking description as line"
            }
        }
        }}
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "router bgp 65000",
#         "auto-summary",
#         "bmp buffer-size 22",
#         "bmp server 2",
#         "distance bgp 2 3 4",
#         "distance mbgp 2 3 5",
#         "maximum-paths 2",
#         "maximum-paths ibgp 2",
#         "maximum-secondary-paths 22",
#         "maximum-secondary-paths ibgp 22",
#         "description checking description as line",
#         "bgp additional-paths install receive",
#         "bgp aggregate-timer 0",
#         "bgp always-compare-med",
#         "bgp asnotation dot",
#         "bgp bestpath aigp ignore",
#         "bgp bestpath compare-routerid",
#         "bgp bestpath med confed missing-as-worst",
#         "bgp confederation identifier 22",
#         "bgp consistency-checker error-message interval 10",
#         "bgp dampening route-map routeMap1Test",
#         "bgp deterministic-med",
#         "bgp graceful-restart restart-time 2",
#         "bgp graceful-restart stalepath-time 22",
#         "bgp graceful-shutdown all vrfs 31 local-preference 230 community 77",
#         "bgp listen limit 200",
#         "bgp listen range 192.0.2.1/24 peer-group PaulNetworkGroup",
#         "bgp log-neighbor-changes",
#         "bgp maxas-limit 2",
#         "bgp maxcommunity-limit 3",
#         "bgp maxextcommunity-limit 3",
#         "bgp nexthop route-map RouteMap1",
#         "bgp nexthop trigger delay 2",
#         "bgp nopeerup-delay cold-boot 2",
#         "bgp nopeerup-delay post-boot 22",
#         "bgp nopeerup-delay nsf-switchover 10",
#         "bgp nopeerup-delay user-initiated 22",
#         "bgp recursion host",
#         "bgp redistribute-internal",
#         "bgp refresh max-eor-time 700",
#         "bgp refresh stalepath-time 800",
#         "bgp router-id vrf auto-assign",
#         "bgp scan-time 22",
#         "bgp slow-peer detection threshold 345",
#         "bgp slow-peer split-update-group dynamic permanent",
#         "bgp sso route-refresh-enable",
#         "bgp suppress-inactive",
#         "bgp update-delay 2",
#         "bgp update-group split as-override",
#         "bgp inject-map map2 exist-map Testmap3 copy-attributes",
#         "bgp inject-map map1 exist-map Testmap2 copy-attributes",
#         "distribute-list prefix prefixTest in",
#         "distribute-list gateway gatewayTest out",
#         "distribute-list 300 out Loopback0",
#         "aggregate-address 192.0.2.1 255.255.255.0 summary-only attribute-map testMap1",
#         "aggregate-address 192.0.2.2 255.255.255.0 as-set",
#         "aggregate-address 192.0.2.3 255.255.255.0 as-set",
#         "network 192.0.2.15 mask 55.255.255.0 route-map mp1 backdoor",
#         "network 192.0.2.16 mask 255.255.255.0 route-map mp2 backdoor",
#         "network 192.0.2.17 mask 255.255.255.0 route-map mp2 backdoor",
#         "neighbor 192.0.2.8 advertise diverse-path backup",
#         "neighbor 192.0.2.8 route-reflector-client",
#         "neighbor 192.0.2.9 remote-as 64500",
#         "neighbor 192.0.2.9 update-source Loopback0",
#         "neighbor 192.0.2.9 route-map rmp1 in",
#         "neighbor 192.0.2.9 route-map rmp2 in",
#         "neighbor 192.0.2.10 remote-as 64500",
#         "neighbor 192.0.2.10 update-source Loopback1",
#         "neighbor 192.0.2.11 remote-as 45000",
#         "neighbor 192.0.2.11 activate",
#         "neighbor 192.0.2.11 send-community extended",
#         "neighbor 192.0.2.12 remote-as 45000",
#         "neighbor 192.0.2.12 activate",
#         "neighbor 192.0.2.13 remote-as 6553601",
#         "neighbor 192.0.2.13 shutdown graceful 10 community 20",
#         "neighbor 2001:DB8::1037 activate",
#         "neighbor 2001:DB8::1037 advertise additional-paths group-best",
#         "neighbor testNebTag peer-group 5",
#         "neighbor testNebTag soft-reconfiguration inbound",
#         "neighbor testNebTag version 4",
#         "redistribute static metric 33 route-map rmp1",
#         "redistribute application app1 metric 22",
#         "redistribute application app2 metric 33 route-map mp1",
#         "redistribute connected metric 22",
#         "redistribute mobile metric 211"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# router bgp 65000
#  auto-summary
#  bmp buffer-size 22
#  bmp server 2
#  distance bgp 2 3 4
#  distance mbgp 2 3 5
#  maximum-paths 2
#  maximum-paths ibgp 2
#  maximum-secondary-paths 22
#  maximum-secondary-paths ibgp 22
#  description checking description as line
#  bgp additional-paths install receive
#  bgp aggregate-timer 0
#  bgp always-compare-med
#  bgp asnotation dot
#  bgp bestpath aigp ignore
#  bgp bestpath compare-routerid
#  bgp bestpath med confed missing-as-worst
#  bgp confederation identifier 22
#  bgp consistency-checker error-message interval 10
#  bgp dampening route-map routeMap1Test
#  bgp deterministic-med
#  bgp graceful-restart restart-time 2
#  bgp graceful-restart stalepath-time 22
#  bgp graceful-shutdown all vrfs 31 local-preference 230 community 77
#  bgp listen limit 200
#  bgp listen range 192.0.2.1/24 peer-group PaulNetworkGroup
#  bgp log-neighbor-changes
#  bgp maxas-limit 2
#  bgp maxcommunity-limit 3
#  bgp maxextcommunity-limit 3
#  bgp nexthop route-map RouteMap1
#  bgp nexthop trigger delay 2
#  bgp nopeerup-delay cold-boot 2
#  bgp nopeerup-delay post-boot 22
#  bgp nopeerup-delay nsf-switchover 10
#  bgp nopeerup-delay user-initiated 22
#  bgp recursion host
#  bgp redistribute-internal
#  bgp refresh max-eor-time 700
#  bgp refresh stalepath-time 800
#  bgp router-id vrf auto-assign
#  bgp scan-time 22
#  bgp slow-peer detection threshold 345
#  bgp slow-peer split-update-group dynamic permanent
#  bgp sso route-refresh-enable
#  bgp suppress-inactive
#  bgp update-delay 2
#  bgp update-group split as-override
#  bgp inject-map map2 exist-map Testmap3 copy-attributes
#  bgp inject-map map1 exist-map Testmap2 copy-attributes
#  distribute-list prefix prefixTest in
#  distribute-list gateway gatewayTest out
#  distribute-list 300 out Loopback0
#  aggregate-address 192.0.2.1 255.255.255.0 summary-only attribute-map testMap1
#  aggregate-address 192.0.2.2 255.255.255.0 as-set
#  aggregate-address 192.0.2.3 255.255.255.0 as-set
#  network 192.0.2.15 mask 55.255.255.0 route-map mp1 backdoor
#  network 192.0.2.16 mask 255.255.255.0 route-map mp2 backdoor
#  network 192.0.2.17 mask 255.255.255.0 route-map mp2 backdoor
#  neighbor 192.0.2.8 advertise diverse-path backup
#  neighbor 192.0.2.8 route-reflector-client
#  neighbor 192.0.2.9 remote-as 64500
#  neighbor 192.0.2.9 update-source Loopback0
#  neighbor 192.0.2.9 route-map rmp1 in
#  neighbor 192.0.2.9 route-map rmp2 in
#  neighbor 192.0.2.10 remote-as 64500
#  neighbor 192.0.2.10 update-source Loopback1
#  neighbor 192.0.2.11 remote-as 45000
#  neighbor 192.0.2.11 activate
#  neighbor 192.0.2.11 send-community extended
#  neighbor 192.0.2.12 remote-as 45000
#  neighbor 192.0.2.12 activate
#  neighbor 192.0.2.13 remote-as 6553601
#  neighbor 192.0.2.13 shutdown graceful 10 community 20
#  neighbor 2001:DB8::1037 activate
#  neighbor 2001:DB8::1037 advertise additional-paths group-best
#  neighbor testNebTag peer-group 5
#  neighbor testNebTag soft-reconfiguration inbound
#  neighbor testNebTag version 4
#  redistribute static metric 33 route-map rmp1
#  redistribute application app1 metric 22
#  redistribute application app2 metric 33 route-map mp1
#  redistribute connected metric 22
#  redistribute mobile metric 21

- name: Parse the commands for provided configuration
  cisco.ios.ios_bgp_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
#  "parsed": {
#         "aggregate_addresses": [
#             {
#                 "address": "192.0.2.1",
#                 "attribute_map": "testMap1",
#                 "netmask": "255.255.255.0",
#                 "summary_only": true
#             },
#             {
#                 "address": "192.0.2.2",
#                 "as_set": true,
#                 "netmask": "255.255.255.0"
#             },
#             {
#                 "address": "192.0.2.3",
#                 "as_set": true,
#                 "netmask": "255.255.255.0"
#             }
#         ],
#         "as_number": "65000",
#         "auto_summary": true,
#         "bgp": {
#             "additional_paths": {
#                 "install": true,
#                 "receive": true
#             },
#             "aggregate_timer": 0,
#             "always_compare_med": true,
#             "asnotation": true,
#             "bestpath_options": {
#                 "aigp": true,
#                 "compare_routerid": true,
#                 "med": {
#                     "confed": true,
#                     "missing_as_worst": true
#                 }
#             },
#             "confederation": {
#                 "identifier": "22"
#             },
#             "consistency_checker": {
#                 "error_message": {
#                     "interval": 10,
#                     "set": true
#                 }
#             },
#             "dampening": {
#                 "route_map": "routeMap1Test"
#             },
#             "deterministic_med": true,
#             "graceful_restart": {
#                 "restart_time": 2,
#                 "stalepath_time": 22
#             },
#             "graceful_shutdown": {
#                 "community": "77",
#                 "local_preference": 230,
#                 "vrfs": {
#                     "time": 31
#                 }
#             },
#             "inject_maps": [
#                 {
#                     "copy_attributes": true,
#                     "exist_map_name": "Testmap3",
#                     "name": "map2"
#                 },
#                 {
#                     "copy_attributes": true,
#                     "exist_map_name": "Testmap2",
#                     "name": "map1"
#                 }
#             ],
#             "listen": {
#                 "limit": 200,
#                 "range": {
#                     "host_with_subnet": "192.0.2.1/24",
#                     "peer_group": "PaulNetworkGroup"
#                 }
#             },
#             "log_neighbor_changes": true,
#             "maxas_limit": 2,
#             "maxcommunity_limit": 3,
#             "maxextcommunity_limit": 3,
#             "nexthop": {
#                 "route_map": "RouteMap1",
#                 "trigger": {
#                     "delay": 2
#                 }
#             },
#             "nopeerup_delay_options": {
#                 "cold_boot": 2,
#                 "nsf_switchover": 10,
#                 "post_boot": 22,
#                 "user_initiated": 22
#             },
#             "recursion": true,
#             "redistribute_internal": true,
#             "refresh": {
#                 "max_eor_time": 700,
#                 "stalepath_time": 800
#             },
#             "router_id": {
#                 "vrf": true
#             },
#             "scan_time": 22,
#             "slow_peer": {
#                 "detection": {
#                     "threshold": 345
#                 },
#                 "split_update_group": {
#                     "dynamic": true,
#                     "permanent": true
#                 }
#             },
#             "sso": true,
#             "suppress_inactive": true,
#             "update_delay": 2,
#             "update_group": true
#         },
#         "bmp": {
#             "buffer_size": 22,
#             "server": 2
#         },
#         "distance": {
#             "bgp": {
#                 "routes_external": 2,
#                 "routes_internal": 3,
#                 "routes_local": 4
#             },
#             "mbgp": {
#                 "routes_external": 2,
#                 "routes_internal": 3,
#                 "routes_local": 5
#             }
#         },
#         "distributes": [
#             {
#                 "in": true,
#                 "prefix": "prefixTest"
#             },
#             {
#                 "gateway": "gatewayTest",
#                 "out": true
#             },
#             {
#                 "acl": "300",
#                 "interface": "Loopback0",
#                 "out": true
#             }
#         ],
#         "maximum_paths": {
#             "ibgp": 2,
#             "paths": 2
#         },
#         "maximum_secondary_paths": {
#             "ibgp": 22,
#             "paths": 22
#         },
#         "neighbors": [
#             {
#                 "neighbor_address": "192.0.2.10",
#                 "remote_as": "64500",
#                 "update_source": "Loopback1"
#             },
#             {
#                 "activate": true,
#                 "neighbor_address": "192.0.2.11",
#                 "remote_as": "45000",
#                 "send_community": {
#                     "extended": true
#                 }
#             },
#             {
#                 "activate": true,
#                 "neighbor_address": "192.0.2.12",
#                 "remote_as": "45000"
#             },
#             {
#                 "neighbor_address": "192.0.2.13",
#                 "remote_as": "6553601"
#             },
#             {
#                 "advertise": {
#                     "diverse_path": {
#                         "backup": true
#                     }
#                 },
#                 "neighbor_address": "192.0.2.8",
#                 "route_reflector_client": true
#             },
#             {
#                 "neighbor_address": "192.0.2.9",
#                 "remote_as": "64500",
#                 "route_maps": [
#                     {
#                         "in": true,
#                         "name": "rmp1"
#                     },
#                     {
#                         "in": true,
#                         "name": "rmp2"
#                     }
#                 ],
#                 "update_source": "Loopback0"
#             },
#             {
#                 "activate": true,
#                 "advertise": {
#                     "additional_paths": {
#                         "group_best": true
#                     }
#                 },
#                 "neighbor_address": "2001:DB8::1037"
#             },
#             {
#                 "neighbor_address": "testNebTag",
#                 "peer_group": "5",
#                 "soft_reconfiguration": true,
#                 "version": 4
#             }
#         ],
#         "networks": [
#             {
#                 "address": "192.0.2.15",
#                 "backdoor": true,
#                 "netmask": "55.255.255.0",
#                 "route_map": "mp1"
#             },
#             {
#                 "address": "192.0.2.16",
#                 "backdoor": true,
#                 "netmask": "255.255.255.0",
#                 "route_map": "mp2"
#             },
#             {
#                 "address": "192.0.2.17",
#                 "backdoor": true,
#                 "netmask": "255.255.255.0",
#                 "route_map": "mp2"
#             }
#         ],
#         "redistribute": [
#             {
#                 "static": {
#                     "metric": 33,
#                     "route_map": "rmp1",
#                     "set": true
#                 }
#             },
#             {
#                 "application": {
#                     "metric": 22,
#                     "name": "app1"
#                 }
#             },
#             {
#                 "application": {
#                     "metric": 33,
#                     "name": "app2",
#                     "route_map": "mp1"
#                 }
#             },
#             {
#                 "connected": {
#                     "metric": 22,
#                     "set": true
#                 }
#             },
#             {
#                 "mobile": {
#                     "metric": 21,
#                     "set": true
#                 }
#             }
#         ]
#     }
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
    - "router bgp 65000"
    - "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive"
    - "bgp graceful-shutdown all neighbors 50 local-preference 100 community 100"
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - "router bgp 65000"
    - "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive"
    - "bgp graceful-shutdown all neighbors 50 local-preference 100 community 100"
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_global.bgp_global import (
    Bgp_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bgp_global.bgp_global import (
    Bgp_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_globalArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Bgp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
