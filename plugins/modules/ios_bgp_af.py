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
The module file for ios_bgp_af
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_bgp_af
short_description: BGP Address family resource module
description: This module configures and manages the attributes of bgp address family on Cisco IOS.
version_added: 1.2.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A list of configurations for bgp address family.
    type: dict
    suboptions:
      afi:
        description: Address Family
        type: str
        choices: ['ipv4', 'ipv6', 'l2vpn', 'nsap', 'rtfilter', 'vpnv4', 'vpnv6']
      af_modifier:
        description: Address Family modifier
        type: str
        choices: ['flowspec', 'mdt', 'multicast', 'mvpn', 'unicast']
      vrf:
        description: Specify parameters for a VPN Routing/Forwarding instance
        type: str
      aggregate_address:
        description: Configure BGP aggregate entries
        type: dict
        suboptions:
          address:
            description: Aggregate address(A.B.C.D)
            type: str
          netmask:
            description: Aggregate mask(A.B.C.D)
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
          description: Configure BGP aggregate entries
          type: dict
          suboptions:
            additional_paths:
              description: Additional paths in the BGP table
              type: dict
              suboptions:
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
                    group_best:
                      description: Select group-best path
                      type: bool
                send:
                  description: Send additional paths to neighbors
                  type: bool
            aggregate_timer:
              description:
                - Configure Aggregation Timer
                - Please refer vendor documentation for valid values
              type: int
            dampening:
              description: Enable route-flap dampening
              type: dict
              suboptions:
                half_life:
                  description: Half-life time for the penalty
                  type: dict
                  suboptions:
                    value:
                      description:
                        - Half-life time value for the penalty
                        - Please refer vendor documentation for valid values
                      type: int
                    reuse_route:
                      description:
                        - Value to start reusing a route
                        - Please refer vendor documentation for valid values
                      type: int
                    suppress_route:
                      description:
                        - Value to start suppressing a route
                        - Please refer vendor documentation for valid values
                      type: int
                route_map:
                  description: Route-map to specify criteria for dampening
                  type: str
            dmzlink_bw:
              description: Use DMZ Link Bandwidth as weight for BGP multipaths
              type: bool
            nexthop:
              description: Nexthop tracking commands
              type: dict
              suboptions:
                route_map:
                  description: Route map for valid nexthops
                  type: str
                trigger:
                  description: Nexthop triggering
                  type: dict
                  suboptions:
                    delay:
                      description:
                        - Set the delay to tigger nexthop tracking
                        - Please refer vendor documentation for valid values
                      type: int
                    enable:
                      description: Enable nexthop tracking
                      type: bool
            redistribute_internal:
              description: Allow redistribution of iBGP into IGPs (dangerous)
              type: bool
            route_map:
              description:
                - route-map control commands
                - Have route-map set commands take priority over BGP commands such as next-hop unchanged
              type: bool
            scan_time:
              description:
                - Configure background scanner interval
                - Please refer vendor documentation for valid values
              type: int
            slow_peer:
              description: Nexthop triggering
              type: dict
              suboptions:
                detection:
                  description: Slow-peer detection
                  type: dict
                  suboptions:
                    enable:
                      description: Enable slow-peer detection
                      type: bool
                    threshold:
                      description:
                        - Set the slow-peer detection threshold
                        - Threshold value (seconds)
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
            soft_reconfig_backup:
              description: Use soft-reconfiguration inbound only when route-refresh is not negotiated
              type: bool
            update_group:
              description:
                - Manage peers in bgp update groups
                - Split update groups based on Policy
                - Keep peers with as-override in different update groups
              type: bool
        default:
          description: Set a command to its defaults
          type: bool
        default_metric:
          description: Set metric of redistributed routes
          type: int
        distance:
          description: Define an administrative distance
          type: dict
          suboptions:
            external:
              description: Distance for routes external to the AS
              type: int
            internal:
              description: Distance for routes internal to the AS
              type: int
            local:
              description: Distance for local routes
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
                  description: Send additional paths to this neighbor
                  type: bool
            advertise:
              description:
                - Advertise to this neighbor
                - Advertise additional paths
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
              description: Enable a AIGP on neighbor
              type: dict
              suboptions:
                enable:
                  description: Enable a AIGP on neighbor
                  type: str
                send:
                  description: Cost community or MED carrying AIGP VALUE
                  type: dict
                  suboptions:
                    cost_community:
                      description: Cost extended community carrying AIGP Value
                      type: int
                    poi:
                      description: Point of Insertion
                      type: dict
                      suboptions:
                        igp_cost:
                          description: Point of Insertion After IGP
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
              description:
                - Accept as-path with my AS present in it
                - Please refer vendor documentation for valid values
              type: int
            as_override:
              description: Override matching AS-number while sending update
              type: dict
              suboptions:
                set:
                  description: Enable AS override
                  type: bool
                split_horizon:
                  description: Maintain Split Horizon while sending update
                  type: bool
            capability:
              description:
                - Advertise capability to the peer
                - Advertise ORF capability to the peer
                - Advertise prefixlist ORF capability to this neighbor
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
            default_originate:
              description: Originate default route to this neighbor
              type: dict
              suboptions:
                set:
                  description: Set default route to this neighbor
                  type: bool
                route_map:
                  description: Route-map to specify criteria to originate default
                  type: str
            distribute_list:
              description: Filter updates to/from this neighbor
              type: dict
              suboptions:
                acl:
                  description: ACL id/name
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
            filter_list:
              description: Establish BGP filters
              type: dict
              suboptions:
                as_path_acl:
                  description:
                    - AS path access list
                    - Please refer vendor documentation for valid values
                  type: int
                in:
                  description: Filter incoming updates
                  type: bool
                out:
                  description: Filter outgoing updates
                  type: bool
            inherit:
              description:
                - Inherit a template
                - Inherit a peer-policy template
              type: str
            maximum_prefix:
              description: Establish BGP filters
              type: dict
              suboptions:
                number:
                  description:
                    - maximum no. of prefix limit
                    - Please refer vendor documentation for valid values
                  type: int
                threshold_value:
                  description:
                    - Threshold value (%) at which to generate a warning msg
                    - Please refer vendor documentation for valid values
                  type: int
                restart:
                  description: Restart bgp connection after limit is exceeded
                  type: int
                warning_only:
                  description: Only give warning message when limit is exceeded
                  type: bool
            next_hop_self:
              description: Disable the next hop calculation for this neighbor
              type: bool
            next_hop_unchanged:
              description: Propagate next hop unchanged for iBGP paths to this neighbor
              type: bool
            prefix_list:
              description: Filter updates to/from this neighbor
              type: dict
              suboptions:
                name:
                  description: Name of a prefix list
                  type: str
                in:
                  description: Filter incoming updates
                  type: bool
                out:
                  description: Filter outgoing updates
                  type: bool
            remove_private_as:
              description: Remove private AS number from outbound updates
              type: dict
              suboptions:
                set:
                  description: Remove private AS number from outbound updates
                  type: bool
                all:
                  description: Remove all private AS numbers
                  type: bool
                replace_as:
                  description: Replace all private AS numbers with local AS
                  type: bool
            route_map:
              description: Apply route map to neighbor
              type: dict
              suboptions:
                name:
                  description: Name of route map
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
              type: bool
            send_community:
              description: Send Community attribute to this neighbor
              type: dict
              suboptions:
                both:
                  description: Send Standard and Extended Community attributes
                  type: bool
                extended:
                  description: Send Extended Community attribute
                  type: bool
                standard:
                  description: Send Standard Community attribute
                  type: bool
            slow_peer:
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
            soft_reconfiguration:
              description:
                - Per neighbor soft reconfiguration
                - Allow inbound soft reconfiguration for this neighbor
              type: bool
            unsuppress_map:
              description: Route-map to selectively unsuppress suppressed routes
              type: str
            weight:
              description: Set default weight for routes from this neighbor
              type: int
        network:
          description: Specify a network to announce via BGP
          type: dict
          suboptions:
            address:
              description: Network number (A.B.C.D)
              type: str
            mask:
              description: Network mask (A.B.C.D)
              type: str
            backdoor:
              description: Specify a BGP backdoor route
              type: bool
            route_map:
              description: Route-map to modify the attributes
              type: str
            table_map:
              description: Map external entry attributes into routing table
              type: dict
              suboptions:
                name:
                  description: route-map name
                  type: str
                filter:
                  description: Selective route download
                  type: str
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
    config:
    state: gathered
# Module Execution Result:
# ------------------------
#
# Using Rendered
- name: Rendered the provided configuration with the exisiting running configuration
  cisco.ios.ios_bgp_af:
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
  cisco.ios.ios_bgp_af:
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_af.bgp_af import (
    Bgp_afArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bgp_af.bgp_af import (
    Bgp_af,
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
        argument_spec=Bgp_afArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Bgp_af(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()