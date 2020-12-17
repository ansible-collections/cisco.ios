#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_bgp_global
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_bgp_global
short_description: Global BGP resource module
description: This module configures and manages the attributes of global bgp on Cisco IOS.
version_added: 1.2.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A list of configurations for global bgp.
    type: dict
    suboptions:
      asn:
        description: Autonomous system number.
        type: str
        required: true
      bgp:
        description: Enable address family and enter its config mode
        type: dict
        suboptions:
          always_compare_med:
            description: Allow comparing MED from different neighbors
            type: bool
          asnotation:
            description:
              - Change the default asplain notation
              - asdot notation
            type: bool
          bestpath:
            description: Change the default bestpath selection
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
              med:
                description: MED attribute
                type: dict
                suboptions:
                  confed:
                    description: Compare MED among confederation paths
                    type: bool
                  missing_as_worst: Treat missing MED as the least preferred one
                    type: bool
          client_to_client:
            description:
              - Configure client to client route reflection
              - reflection of routes allowed
            type: dict
            suboptions:
              all:
                description: inter-cluster and intra-cluster (default)
                type: bool
              intra_cluster:
                description: intra cluster reflection
                type: bool
          cluster_id:
            description:
              - Configure Route-Reflector Cluster-id (peers may reset)
              - A.B.C.D/Please refer vendor documentation for valid Route-Reflector Cluster-id
            type: bool
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
                  enable:
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
                  enable:
                    description: Enable Error-Msg
                    type: bool
                  interval:
                    description:
                      - Set the bgp consistency checker
                      - Please refer vendor documentation for valid values
                    type: int
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
            description: Routemap which specifies prefixes to inject
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
                  v4address_with_subnet:
                    description: IPv4 subnet range(A.B.C.D/nn)
                    type: str
                  v6address_with_subnet:
                    description: IPv6 subnet range(X:X:X:X::X/<0-128>)
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
          nopeerup_delay:
            description:
              - Set how long BGP will wait for the first peer to come up before beginning the update delay or
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
                type: str
          scan_time:
            description:
              - Configure background scanner interval
              - Please refer vendor documentation for valid values
            type: int
          snmp:
            description:
              - BGP SNMP options
              - BGP SNMP trap options
              - Use cbgpPeer2Type as part of index for traps
            type: bool
          sso:
            description:
              - Stateful Switchover
              - Enable SSO only for Route-Refresh capable peers
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
            type: bool
          update_group:
            description:
              - Manage peers in bgp update groups
              - Split update groups based on Policy
              - Keep peers with as-override in different update groups
            type: bool
      bmp:
        description: BGP Monitoring Protocol)
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
      neighbor:
        description: Specify a neighbor router
        type: dict
        suboptions:
          address:
            description: Neighbor address (A.B.C.D)
            type: str
          tag:
            description: Neighbor tag
            type: str
          ipv6_adddress:
            description: Neighbor ipv6 address (X:X:X:X::X)
            type: str
          bmp_activate:
            description:
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
          cluster_id:
            description:
              - Configure Route-Reflector Cluster-id (peers may reset)
              - Route-Reflector Cluster-id as 32 bit quantity, or
                Route-Reflector Cluster-id in IP address format (A.B.C.D)
            type: str
          description:
            description: Neighbor specific description
            type: str
          disable_connected_check:
            description: one-hop away EBGP peer using loopback address
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
          password:
            description: Set a password
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
            type: int
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
          version:
            description:
              - Set the BGP version to match a neighbor
              - Neighbor's BGP version
              - Please refer vendor documentation for valid values
            type: int
      route_server_context:
        description: Enter route server context command mode
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
        description: Enter scope command mode
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
      template:
        description: Enter template command mode
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
      - The module, by default, will connect to the remote device and retrieve the current
        running-config to use as a base for comparing against the contents of source.
        There are times when it is not desirable to have the task get the current running-config
        for every task in a playbook.  The I(running_config) argument allows the implementer
        to pass in the configuration to use as the base config for comparison.
    type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
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
    state: merged

# Commands fired:
# ---------------
#
#

# After state:
# ------------
#
# vios#sh running-config | section ^router bgp


# Using replaced

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp


- name: Replaces device configuration of listed global BGP with provided configuration
  cisco.ios.ios_bgp_global:
    config:
    
    state: replaced

# Commands fired:
# ---------------
#


# After state:
# -------------
#
# vios#sh running-config | section ^router bgp


# Using overridden

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp

- name: Override device configuration of all global BGP with provided configuration
  cisco.ios.ios_bgp_global:
    config:
    
    state: overridden

# Commands fired:
# ---------------
#

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp

# Using Deleted

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp

- name: "Delete global BGP (Note: This won't delete the all configured global BGP)"
  cisco.ios.ios_bgp_global:
    config:
    
    state: deleted

# Commands fired:
# ---------------
#


# After state:
# -------------
#
# vios#sh running-config | section ^router bgp


# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp


- name: "Delete global BGP based on AFI (Note: This won't delete the all configured global BGP)"
  cisco.ios.ios_bgp_global:
    config:
    
    state: deleted

# Commands fired:
# ---------------
#


# After state:
# -------------
#
# vios#sh running-config | section ^router bgp


# Using Deleted without any config passed
#"(NOTE: This will delete all of configured global BGP)"

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp


- name: 'Delete ALL of configured global BGP (Note: This WILL delete the all configured
    global BGP)'
  cisco.ios.ios_bgp_global:
    state: deleted

# Commands fired:
# ---------------
#


# After state:
# -------------
#
# vios#sh running-config | section ^router bgp

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp


- name: Gather listed global BGP with provided configurations
  cisco.ios.ios_bgp_global:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#

# Using Rendered

- name: Rendered the provided configuration with the exisiting running configuration
  cisco.ios.ios_bgp_global:
    config:
    
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#

- name: Parse the commands for provided configuration
  cisco.ios.ios_bgp_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#     ]
"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device
  returned: always
  type: list
  sample: []
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
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=Bgp_globalArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Bgp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
