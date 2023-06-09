#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_ospf_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_ospf_interfaces
short_description: Resource module to configure OSPF interfaces.
description:
  This module configures and manages the Open Shortest Path First (OSPF)
  version 2 on IOS platforms.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of OSPF interfaces options.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface excluding any logical unit number,
            i.e. GigabitEthernet0/1.
        type: str
        required: true
      address_family:
        description:
          - OSPF interfaces settings on the interfaces in address-family
            context.
        type: list
        elements: dict
        suboptions:
          afi:
            description:
              - Address Family Identifier (AFI) for OSPF interfaces settings
                on the interfaces.
            type: str
            choices:
              - ipv4
              - ipv6
            required: true
          process:
            description: OSPF interfaces process config
            type: dict
            suboptions:
              id:
                description:
                  - Address Family Identifier (AFI) for OSPF interfaces settings
                    on the interfaces. Please refer vendor documentation of Valid
                    values.
                type: int
              area_id:
                description:
                  - OSPF interfaces area ID as a decimal value. Please
                    refer vendor documentation of Valid values.
                  - OSPF interfaces area ID in IP address format(e.g.
                    A.B.C.D)
                type: str
              secondaries:
                description:
                  - Include or exclude secondary IP addresses.
                  - Valid only with IPv4 config
                type: bool
              instance_id:
                description:
                  - Set the OSPF instance based on ID
                  - Valid only with IPv6 OSPF config
                type: int
          adjacency:
            description: Adjacency staggering
            type: bool
          authentication:
            description: Enable authentication
            type: dict
            suboptions:
              key_chain:
                description: Use a key-chain for cryptographic
                  authentication keys
                type: str
              message_digest:
                description: Use message-digest authentication
                type: bool
              "null":
                description: Use no authentication
                type: bool
          bfd:
            description:
              - BFD configuration commands
              - Enable/Disable BFD on this interface
            type: bool
          cost:
            description: Interface cost
            type: dict
            suboptions:
              interface_cost:
                description: Interface cost or Route cost of this interface
                type: int
              dynamic_cost:
                description:
                  - Specify dynamic cost options
                  - Valid only with IPv6 OSPF config
                type: dict
                suboptions:
                  default:
                    description: Specify default link metric value
                    type: int
                  hysteresis:
                    description: Specify hysteresis value for LSA dampening
                    type: dict
                    suboptions:
                      percent:
                        description: Specify hysteresis percent changed.
                          Please refer vendor documentation of Valid values.
                        type: int
                      threshold:
                        description: Specify hysteresis threshold value.
                          Please refer vendor documentation of Valid values.
                        type: int
                  weight:
                    description: Specify weight to be placed on individual
                      metrics
                    type: dict
                    suboptions:
                      l2_factor:
                        description:
                          - Specify weight to be given to L2-factor metric
                          - Percentage weight of L2-factor metric. Please refer
                            vendor documentation of Valid values.
                        type: int
                      latency:
                        description:
                          - Specify weight to be given to latency metric.
                          - Percentage weight of latency metric. Please refer
                            vendor documentation of Valid values.
                        type: int
                      oc:
                        description:
                          - Specify weight to be given to cdr/mdr for oc
                          - Give 100 percent weightage for current data rate(0
                            for maxdatarate)
                        type: bool
                      resources:
                        description:
                          - Specify weight to be given to resources metric
                          - Percentage weight of resources metric. Please refer
                            vendor documentation of Valid values.
                        type: int
                      throughput:
                        description:
                          - Specify weight to be given to throughput metric
                          - Percentage weight of throughput metric. Please refer
                            vendor documentation of Valid values.
                        type: int
          database_filter:
            description: Filter OSPF LSA during synchronization and flooding
            type: bool
          dead_interval:
            description: Interval after which a neighbor is declared dead
            type: dict
            suboptions:
              time:
                description: time in seconds
                type: int
              minimal:
                description:
                  - Set to 1 second and set multiplier for Hellos
                  - Number of Hellos sent within 1 second. Please refer
                    vendor documentation of Valid values.
                  - Valid only with IP OSPF config
                type: int
          demand_circuit:
            description: OSPF Demand Circuit, enable or disable
              the demand circuit'
            type: dict
            suboptions:
              enable:
                description: Enable Demand Circuit
                type: bool
              ignore:
                description: Ignore demand circuit auto-negotiation requests
                type: bool
              disable:
                description:
                  - Disable demand circuit on this interface
                  - Valid only with IPv6 OSPF config
                type: bool
          flood_reduction:
            description: OSPF Flood Reduction
            type: bool
          hello_interval:
            description:
              - Time between HELLO packets
              - Please refer vendor documentation of Valid values.
            type: int
          lls:
            description:
              - Link-local Signaling (LLS) support
              - Valid only with IP OSPF config
            type: bool
          manet:
            description:
              - Mobile Adhoc Networking options
              - MANET Peering options
              - Valid only with IPv6 OSPF config
            type: dict
            suboptions:
              cost:
                description: Redundant path cost improvement required to peer
                type: dict
                suboptions:
                  percent:
                    description: Relative incremental path cost.
                      Please refer vendor documentation of Valid values.
                    type: int
                  threshold:
                    description: Absolute incremental path cost.
                      Please refer vendor documentation of Valid values.
                    type: int
              link_metrics:
                description: Redundant path cost improvement required to peer
                type: dict
                suboptions:
                  set:
                    description: Enable link-metrics
                    type: bool
                  cost_threshold:
                    description: Minimum link cost threshold.
                      Please refer vendor documentation of Valid values.
                    type: int
          mtu_ignore:
            description: Ignores the MTU in DBD packets
            type: bool
          multi_area:
            description:
              - Set the OSPF multi-area ID
              - Valid only with IP OSPF config
            type: dict
            suboptions:
              id:
                description:
                  - OSPF multi-area ID as a decimal value. Please refer vendor
                    documentation of Valid values.
                  - OSPF multi-area ID in IP address format(e.g. A.B.C.D)
                type: int
              cost:
                description: Interface cost
                type: int
          neighbor:
            description:
              - OSPF neighbor link-local IPv6 address (X:X:X:X::X)
              - Valid only with IPv6 OSPF config
            type: dict
            suboptions:
              address:
                description: Neighbor link-local IPv6 address
                type: str
              cost:
                description: OSPF cost for point-to-multipoint neighbor
                type: int
              database_filter:
                description: Filter OSPF LSA during synchronization and flooding for point-to-multipoint neighbor
                type: bool
              poll_interval:
                description: OSPF dead-router polling interval
                type: int
              priority:
                description: OSPF priority of non-broadcast neighbor
                type: int
          network:
            description: Network type
            type: dict
            suboptions:
              broadcast:
                description: Specify OSPF broadcast multi-access network
                type: bool
              manet:
                description:
                  - Specify MANET OSPF interface type
                  - Valid only with IPv6 OSPF config
                type: bool
              non_broadcast:
                description: Specify OSPF NBMA network
                type: bool
              point_to_multipoint:
                description: Specify OSPF point-to-multipoint network
                type: bool
              point_to_point:
                description: Specify OSPF point-to-point network
                type: bool
          prefix_suppression:
            description: Enable/Disable OSPF prefix suppression
            type: bool
          priority:
            description: Router priority. Please refer vendor documentation
              of Valid values.
            type: int
          resync_timeout:
            description: Interval after which adjacency is reset if oob-resync
              is not started. Please refer vendor documentation of Valid values.
            type: int
          retransmit_interval:
            description: Time between retransmitting lost link state
              advertisements. Please refer vendor documentation of Valid values.
            type: int
          shutdown:
            description: Set OSPF protocol's state to disable under
              current interface
            type: bool
          transmit_delay:
            description: Link state transmit delay.
              Please refer vendor documentation of Valid values.
            type: int
          ttl_security:
            description:
              - TTL security check
              - Valid only with IPV4 OSPF config
            type: dict
            suboptions:
              set:
                description: Enable TTL Security on all interfaces
                type: bool
              hops:
                description:
                  - Maximum number of IP hops allowed
                  - Please refer vendor documentation of Valid values.
                type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(sh running-config | section
        ^interface).
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any
        change on the device.
      - The state I(rendered) will transform the configuration in C(config)
        option to platform specific CLI commands which will be returned in the
        I(rendered) key within the result. For state I(rendered) active
        connection to remote host is not required.
      - The state I(gathered) will fetch the running configuration from device
        and transform it into structured data in the format as per the resource
        module argspec and the value is returned in the I(gathered) key within
        the result.
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into JSON format as per the resource module
        parameters and the value is returned in the I(parsed) key within the
        result. The value of C(running_config) option should be the same format
        as the output of command I(show running-config | include ip route|ipv6
        route) executed on device. For state I(parsed) active connection to
        remote host is not required.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using deleted

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ipv6 ospf 55 area 105
#  ipv6 ospf priority 20
#  ipv6 ospf transmit-delay 30
#  ipv6 ospf adjacency stagger disable
# interface GigabitEthernet0/2
#  ip ospf priority 40
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf 10 area 20
#  ip ospf cost 30

- name: Delete provided OSPF Interface config
  cisco.ios.ios_ospf_interfaces:
    config:
      - name: GigabitEthernet0/1
    state: deleted

#  Commands Fired:
#  ---------------
#
#  "commands": [
#         "interface GigabitEthernet0/1",
#         "no ipv6 ospf 55 area 105",
#         "no ipv6 ospf adjacency stagger disable",
#         "no ipv6 ospf priority 20",
#         "no ipv6 ospf transmit-delay 30"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
# interface GigabitEthernet0/2
#  ip ospf priority 40
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf 10 area 20
#  ip ospf cost 30

# Using deleted without any config passed (NOTE: This will delete all OSPF Interfaces configuration from device)

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ipv6 ospf 55 area 105
#  ipv6 ospf priority 20
#  ipv6 ospf transmit-delay 30
#  ipv6 ospf adjacency stagger disable
# interface GigabitEthernet0/2
#  ip ospf priority 40
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf 10 area 20
#  ip ospf cost 30

- name: Delete all OSPF config from interfaces
  cisco.ios.ios_ospf_interfaces:
    state: deleted

# Commands Fired:
# ---------------
#
#  "commands": [
#         "interface GigabitEthernet0/2",
#         "no ip ospf 10 area 20",
#         "no ip ospf adjacency stagger disable",
#         "no ip ospf cost 30",
#         "no ip ospf priority 40",
#         "no ip ospf ttl-security hops 50",
#         "interface GigabitEthernet0/1",
#         "no ipv6 ospf 55 area 105",
#         "no ipv6 ospf adjacency stagger disable",
#         "no ipv6 ospf priority 20",
#         "no ipv6 ospf transmit-delay 30"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
# interface GigabitEthernet0/2

# Using merged

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# router-ios#

- name: Merge provided OSPF Interfaces configuration
  cisco.ios.ios_ospf_interfaces:
    config:
      - name: GigabitEthernet0/1
        address_family:
          - afi: ipv4
            process:
              id: 10
              area_id: 30
            adjacency: true
            bfd: true
            cost:
              interface_cost: 5
            dead_interval:
              time: 5
            demand_circuit:
              ignore: true
            network:
              broadcast: true
            priority: 25
            resync_timeout: 10
            shutdown: true
            ttl_security:
              hops: 50
          - afi: ipv6
            process:
              id: 35
              area_id: 45
            adjacency: true
            database_filter: true
            manet:
              link_metrics:
                cost_threshold: 10
            priority: 55
            transmit_delay: 45
    state: merged

#  Commands Fired:
#  ---------------
#
#   "commands": [
#         "interface GigabitEthernet0/1",
#         "ip ospf 10 area 30",
#         "ip ospf adjacency stagger disable",
#         "ip ospf bfd",
#         "ip ospf cost 5",
#         "ip ospf dead-interval 5",
#         "ip ospf demand-circuit ignore",
#         "ip ospf network broadcast",
#         "ip ospf priority 25",
#         "ip ospf resync-timeout 10",
#         "ip ospf shutdown",
#         "ip ospf ttl-security hops 50",
#         "ipv6 ospf 35 area 45",
#         "ipv6 ospf adjacency stagger disable",
#         "ipv6 ospf database-filter all out",
#         "ipv6 ospf manet peering link-metrics 10",
#         "ipv6 ospf priority 55",
#         "ipv6 ospf transmit-delay 45"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2

# Using overridden

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2

- name: Override provided OSPF Interfaces configuration
  cisco.ios.ios_ospf_interfaces:
    config:
      - name: GigabitEthernet0/1
        address_family:
          - afi: ipv6
            process:
              id: 55
              area_id: 105
            adjacency: true
            priority: 20
            transmit_delay: 30
      - name: GigabitEthernet0/2
        address_family:
          - afi: ipv4
            process:
              id: 10
              area_id: 20
            adjacency: true
            cost:
              interface_cost: 30
            priority: 40
            ttl_security:
              hops: 50
    state: overridden

# Commands Fired:
# ---------------
#
#  "commands": [
#         "interface GigabitEthernet0/2",
#         "ip ospf 10 area 20",
#         "ip ospf adjacency stagger disable",
#         "ip ospf cost 30",
#         "ip ospf priority 40",
#         "ip ospf ttl-security hops 50",
#         "interface GigabitEthernet0/1",
#         "ipv6 ospf 55 area 105",
#         "no ipv6 ospf database-filter all out",
#         "no ipv6 ospf manet peering link-metrics 10",
#         "ipv6 ospf priority 20",
#         "ipv6 ospf transmit-delay 30",
#         "no ip ospf 10 area 30",
#         "no ip ospf adjacency stagger disable",
#         "no ip ospf bfd",
#         "no ip ospf cost 5",
#         "no ip ospf dead-interval 5",
#         "no ip ospf demand-circuit ignore",
#         "no ip ospf network broadcast",
#         "no ip ospf priority 25",
#         "no ip ospf resync-timeout 10",
#         "no ip ospf shutdown",
#         "no ip ospf ttl-security hops 50"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ipv6 ospf 55 area 105
#  ipv6 ospf priority 20
#  ipv6 ospf transmit-delay 30
#  ipv6 ospf adjacency stagger disable
# interface GigabitEthernet0/2
#  ip ospf priority 40
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf 10 area 20
#  ip ospf cost 30

# Using replaced

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2

- name: Replaced provided OSPF Interfaces configuration
  cisco.ios.ios_ospf_interfaces:
    config:
      - name: GigabitEthernet0/2
        address_family:
          - afi: ipv6
            process:
              id: 55
              area_id: 105
            adjacency: true
            priority: 20
            transmit_delay: 30
    state: replaced

# Commands Fired:
# ---------------
#  "commands": [
#         "interface GigabitEthernet0/2",
#         "ipv6 ospf 55 area 105",
#         "ipv6 ospf adjacency stagger disable",
#         "ipv6 ospf priority 20",
#         "ipv6 ospf transmit-delay 30"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2
#  ipv6 ospf 55 area 105
#  ipv6 ospf priority 20
#  ipv6 ospf transmit-delay 30
#  ipv6 ospf adjacency stagger disable

# Using Gathered

# Before state:
# -------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2

- name: Gather OSPF Interfaces provided configurations
  cisco.ios.ios_ospf_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
#  "gathered": [
#         {
#             "name": "GigabitEthernet0/2"
#         },
#         {
#             "address_family": [
#                 {
#                     "adjacency": true,
#                     "afi": "ipv4",
#                     "bfd": true,
#                     "cost": {
#                         "interface_cost": 5
#                     },
#                     "dead_interval": {
#                         "time": 5
#                     },
#                     "demand_circuit": {
#                         "ignore": true
#                     },
#                     "network": {
#                         "broadcast": true
#                     },
#                     "priority": 25,
#                     "process": {
#                         "area_id": "30",
#                         "id": 10
#                     },
#                     "resync_timeout": 10,
#                     "shutdown": true,
#                     "ttl_security": {
#                         "hops": 50
#                     }
#                 },
#                 {
#                     "adjacency": true,
#                     "afi": "ipv6",
#                     "database_filter": true,
#                     "manet": {
#                         "link_metrics": {
#                             "cost_threshold": 10
#                         }
#                     },
#                     "priority": 55,
#                     "process": {
#                         "area_id": "45",
#                         "id": 35
#                     },
#                     "transmit_delay": 45
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "name": "GigabitEthernet0/0"
#         }
#  ]

# After state:
# ------------
#
# router-ios#sh running-config | section ^interface
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/2

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_ospf_interfaces:
    config:
      - name: GigabitEthernet0/1
        address_family:
          - afi: ipv4
            process:
              id: 10
              area_id: 30
            adjacency: true
            bfd: true
            cost:
              interface_cost: 5
            dead_interval:
              time: 5
            demand_circuit:
              ignore: true
            network:
              broadcast: true
            priority: 25
            resync_timeout: 10
            shutdown: true
            ttl_security:
              hops: 50
          - afi: ipv6
            process:
              id: 35
              area_id: 45
            adjacency: true
            database_filter: true
            manet:
              link_metrics:
                cost_threshold: 10
            priority: 55
            transmit_delay: 45
    state: rendered

# Module Execution Result:
# ------------------------
#
#  "rendered": [
#         "interface GigabitEthernet0/1",
#         "ip ospf 10 area 30",
#         "ip ospf adjacency stagger disable",
#         "ip ospf bfd",
#         "ip ospf cost 5",
#         "ip ospf dead-interval 5",
#         "ip ospf demand-circuit ignore",
#         "ip ospf network broadcast",
#         "ip ospf priority 25",
#         "ip ospf resync-timeout 10",
#         "ip ospf shutdown",
#         "ip ospf ttl-security hops 50",
#         "ipv6 ospf 35 area 45",
#         "ipv6 ospf adjacency stagger disable",
#         "ipv6 ospf database-filter all out",
#         "ipv6 ospf manet peering link-metrics 10",
#         "ipv6 ospf priority 55",
#         "ipv6 ospf transmit-delay 45"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/2
# interface GigabitEthernet0/1
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  ip ospf priority 25
#  ip ospf demand-circuit ignore
#  ip ospf bfd
#  ip ospf adjacency stagger disable
#  ip ospf ttl-security hops 50
#  ip ospf shutdown
#  ip ospf 10 area 30
#  ip ospf cost 5
#  ipv6 ospf 35 area 45
#  ipv6 ospf priority 55
#  ipv6 ospf transmit-delay 45
#  ipv6 ospf database-filter all out
#  ipv6 ospf adjacency stagger disable
#  ipv6 ospf manet peering link-metrics 10
# interface GigabitEthernet0/0

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_ospf_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
#  "parsed": [
#         },
#         {
#             "name": "GigabitEthernet0/2"
#         },
#         {
#             "address_family": [
#                 {
#                     "adjacency": true,
#                     "afi": "ipv4",
#                     "bfd": true,
#                     "cost": {
#                         "interface_cost": 5
#                     },
#                     "dead_interval": {
#                         "time": 5
#                     },
#                     "demand_circuit": {
#                         "ignore": true
#                     },
#                     "network": {
#                         "broadcast": true
#                     },
#                     "priority": 25,
#                     "process": {
#                         "area_id": "30",
#                         "id": 10
#                     },
#                     "resync_timeout": 10,
#                     "shutdown": true,
#                     "ttl_security": {
#                         "hops": 50
#                     }
#                 },
#                 {
#                     "adjacency": true,
#                     "afi": "ipv6",
#                     "database_filter": true,
#                     "manet": {
#                         "link_metrics": {
#                             "cost_threshold": 10
#                         }
#                     },
#                     "priority": 55,
#                     "process": {
#                         "area_id": "45",
#                         "id": 35
#                     },
#                     "transmit_delay": 45
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "name": "GigabitEthernet0/0"
#         }
#     ]
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.ospf_interfaces.ospf_interfaces import (
    Ospf_interfaces,
)

# import debugpy

# debugpy.listen(3000)
# debugpy.wait_for_client()


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ospf_interfacesArgs.argument_spec,
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

    result = Ospf_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
