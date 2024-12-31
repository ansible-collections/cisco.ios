#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_acls
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
author:
  - Sumit Jaiswal (@justjais)
  - Sagar Paul (@KB-perByte)
description: This module configures and manages the named or numbered ACLs on IOS platforms.
module: ios_acls
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - Module behavior is not idempotent when sequence for aces are not mentioned
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A list of ACL configuration options.
    elements: dict
    suboptions:
      acls:
        description:
          - A list of Access Control Lists (ACL) attributes.
        elements: dict
        suboptions:
          aces:
            description: The entries within the ACL.
            elements: dict
            suboptions:
              destination:
                description: Specify the packet destination.
                suboptions:
                  address:
                    description: Host address to match, or any single host address.
                    type: str
                  any:
                    description: Match any source address.
                    type: bool
                  host:
                    description: A single destination host
                    type: str
                  object_group:
                    description: Destination network object group
                    type: str
                  port_protocol:
                    description:
                      - Specify the destination port along with protocol.
                      - Note, Valid with TCP/UDP protocol_options
                    suboptions:
                      eq:
                        description: Match only packets on a given port number.
                        type: str
                      gt:
                        description: Match only packets with a greater port number.
                        type: str
                      lt:
                        description: Match only packets with a lower port number.
                        type: str
                      neq:
                        description: Match only packets not on a given port number.
                        type: str
                      range:
                        description: Port group.
                        suboptions:
                          end:
                            description: Specify the end of the port range.
                            type: int
                          start:
                            description: Specify the start of the port range.
                            type: int
                        type: dict
                    type: dict
                  wildcard_bits:
                    description: Destination wildcard bits, valid with IPV4 address.
                    type: str
                type: dict
              dscp:
                description: Match packets with given dscp value.
                type: str
              evaluate:
                description: Evaluate an access list
                type: str
              enable_fragments:
                description: Enable non-initial fragments.
                type: bool
              grant:
                choices:
                  - permit
                  - deny
                description: Specify the action.
                type: str
              log:
                description: Log matches against this entry.
                suboptions:
                  set:
                    description: Enable Log matches against this entry
                    type: bool
                  user_cookie:
                    description: User defined cookie (max of 64 char)
                    type: str
                type: dict
              log_input:
                description: Log matches against this entry, including input interface.
                suboptions:
                  set:
                    description: Enable Log matches against this entry, including input interface.
                    type: bool
                  user_cookie:
                    description: User defined cookie (max of 64 char)
                    type: str
                type: dict
              option:
                description:
                  - Match packets with given IP Options value.
                  - Valid only for named acls.
                suboptions:
                  add_ext:
                    description: Match packets with Address Extension Option (147).
                    type: bool
                  any_options:
                    description: Match packets with ANY Option.
                    type: bool
                  com_security:
                    description: Match packets with Commercial Security Option (134).
                    type: bool
                  dps:
                    description: Match packets with Dynamic Packet State Option (151).
                    type: bool
                  encode:
                    description: Match packets with Encode Option (15).
                    type: bool
                  eool:
                    description: Match packets with End of Options (0).
                    type: bool
                  ext_ip:
                    description: Match packets with Extended IP Option (145).
                    type: bool
                  ext_security:
                    description: Match packets with Extended Security Option (133).
                    type: bool
                  finn:
                    description: Match packets with Experimental Flow Control Option (205).
                    type: bool
                  imitd:
                    description: Match packets with IMI Traffic Desriptor Option (144).
                    type: bool
                  lsr:
                    description: Match packets with Loose Source Route Option (131).
                    type: bool
                  mtup:
                    description: Match packets with MTU Probe Option (11).
                    type: bool
                  mtur:
                    description: Match packets with MTU Reply Option (12).
                    type: bool
                  no_op:
                    description: Match packets with No Operation Option (1).
                    type: bool
                  nsapa:
                    description: Match packets with NSAP Addresses Option (150).
                    type: bool
                  record_route:
                    description: Match packets with Record Route Option (7).
                    type: bool
                  router_alert:
                    description: Match packets with Router Alert Option (148).
                    type: bool
                  sdb:
                    description: Match packets with Selective Directed Broadcast Option (149).
                    type: bool
                  security:
                    description: Match packets with Basic Security Option (130).
                    type: bool
                  ssr:
                    description: Match packets with Strict Source Routing Option (137).
                    type: bool
                  stream_id:
                    description: Match packets with Stream ID Option (136).
                    type: bool
                  timestamp:
                    description: Match packets with Time Stamp Option (68).
                    type: bool
                  traceroute:
                    description: Match packets with Trace Route Option (82).
                    type: bool
                  ump:
                    description: Match packets with Upstream Multicast Packet Option (152).
                    type: bool
                  visa:
                    description: Match packets with Experimental Access Control Option (142).
                    type: bool
                  zsu:
                    description: Match packets with Experimental Measurement Option (10).
                    type: bool
                type: dict
              precedence:
                description: Match packets with given precedence value.
                type: str
              protocol:
                description:
                  - Specify the protocol to match.
                  - Refer to vendor documentation for valid values.
                type: str
              protocol_options:
                description: protocol type.
                suboptions:
                  ahp:
                    description: Authentication Header Protocol.
                    type: bool
                  eigrp:
                    description: Cisco's EIGRP routing protocol.
                    type: bool
                  esp:
                    description: Encapsulation Security Payload.
                    type: bool
                  gre:
                    description: Cisco's GRE tunneling.
                    type: bool
                  hbh:
                    description: Hop by Hop options header. Valid for IPV6
                    type: bool
                  icmp:
                    description: Internet Control Message Protocol.
                    suboptions:
                      administratively_prohibited:
                        description: Administratively prohibited
                        type: bool
                      alternate_address:
                        description: Alternate address
                        type: bool
                      conversion_error:
                        description: Datagram conversion
                        type: bool
                      dod_host_prohibited:
                        description: Host prohibited
                        type: bool
                      dod_net_prohibited:
                        description: Net prohibited
                        type: bool
                      echo:
                        description: Echo (ping)
                        type: bool
                      echo_reply:
                        description: Echo reply
                        type: bool
                      general_parameter_problem:
                        description: Parameter problem
                        type: bool
                      host_isolated:
                        description: Host isolated
                        type: bool
                      host_precedence_unreachable:
                        description: Host unreachable for precedence
                        type: bool
                      host_redirect:
                        description: Host redirect
                        type: bool
                      host_tos_redirect:
                        description: Host redirect for TOS
                        type: bool
                      host_tos_unreachable:
                        description: Host unreachable for TOS
                        type: bool
                      host_unknown:
                        description: Host unknown
                        type: bool
                      host_unreachable:
                        description: Host unreachable
                        type: bool
                      information_reply:
                        description: Information replies
                        type: bool
                      information_request:
                        description: Information requests
                        type: bool
                      mask_reply:
                        description: Mask replies
                        type: bool
                      mask_request:
                        description: mask_request
                        type: bool
                      mobile_redirect:
                        description: Mobile host redirect
                        type: bool
                      net_redirect:
                        description: Network redirect
                        type: bool
                      net_tos_redirect:
                        description: Net redirect for TOS
                        type: bool
                      net_tos_unreachable:
                        description: Network unreachable for TOS
                        type: bool
                      net_unreachable:
                        description: Net unreachable
                        type: bool
                      network_unknown:
                        description: Network unknown
                        type: bool
                      no_room_for_option:
                        description: Parameter required but no room
                        type: bool
                      option_missing:
                        description: Parameter required but not present
                        type: bool
                      packet_too_big:
                        description: Fragmentation needed and DF set
                        type: bool
                      parameter_problem:
                        description: All parameter problems
                        type: bool
                      port_unreachable:
                        description: Port unreachable
                        type: bool
                      precedence_unreachable:
                        description: Precedence cutoff
                        type: bool
                      protocol_unreachable:
                        description: Protocol unreachable
                        type: bool
                      reassembly_timeout:
                        description: Reassembly timeout
                        type: bool
                      redirect:
                        description: All redirects
                        type: bool
                      router_advertisement:
                        description: Router discovery advertisements
                        type: bool
                      router_solicitation:
                        description: Router discovery solicitations
                        type: bool
                      source_quench:
                        description: Source quenches
                        type: bool
                      source_route_failed:
                        description: Source route failed
                        type: bool
                      time_exceeded:
                        description: All time exceededs
                        type: bool
                      timestamp_reply:
                        description: Timestamp replies
                        type: bool
                      timestamp_request:
                        description: Timestamp requests
                        type: bool
                      traceroute:
                        description: Traceroute
                        type: bool
                      ttl_exceeded:
                        description: TTL exceeded
                        type: bool
                      unreachable:
                        description: All unreachables
                        type: bool
                    type: dict
                  igmp:
                    description: Internet Gateway Message Protocol.
                    suboptions:
                      dvmrp:
                        description: Distance Vector Multicast Routing Protocol(2)
                        type: bool
                      host_query:
                        description: IGMP Membership Query(0)
                        type: bool
                      mtrace_resp:
                        description: Multicast Traceroute Response(7)
                        type: bool
                      mtrace_route:
                        description: Multicast Traceroute(8)
                        type: bool
                      pim:
                        description: Protocol Independent Multicast(3)
                        type: bool
                      trace:
                        description: Multicast trace(4)
                        type: bool
                      v1host_report:
                        description: IGMPv1 Membership Report(1)
                        type: bool
                      v2host_report:
                        description: IGMPv2 Membership Report(5)
                        type: bool
                      v2leave_group:
                        description: IGMPv2 Leave Group(6)
                        type: bool
                      v3host_report:
                        description: IGMPv3 Membership Report(9)
                        type: bool
                    type: dict
                  ip:
                    description: Any Internet Protocol.
                    type: bool
                  ipinip:
                    description: IP in IP tunneling.
                    type: bool
                  ipv6:
                    description: Any IPv6.
                    type: bool
                  nos:
                    description: KA9Q NOS compatible IP over IP tunneling.
                    type: bool
                  ospf:
                    description: OSPF routing protocol.
                    type: bool
                  pcp:
                    description: Payload Compression Protocol.
                    type: bool
                  pim:
                    description: Protocol Independent Multicast.
                    type: bool
                  protocol_number:
                    description: An IP protocol number
                    type: int
                  sctp:
                    description: Stream Control Transmission Protocol.
                    type: bool
                  tcp:
                    description: Match TCP packet flags
                    suboptions:
                      ack:
                        description: Match on the ACK bit
                        type: bool
                      established:
                        description: Match established connections
                        type: bool
                      fin:
                        description: Match on the FIN bit
                        type: bool
                      psh:
                        description: Match on the PSH bit
                        type: bool
                      rst:
                        description: Match on the RST bit
                        type: bool
                      syn:
                        description: Match on the SYN bit
                        type: bool
                      urg:
                        description: Match on the URG bit
                        type: bool
                    type: dict
                  udp:
                    description: User Datagram Protocol.
                    type: bool
                type: dict
              remarks:
                description:
                  - The remarks/description of the ACL.
                  - The remarks attribute used within an ace with or without a
                    sequence number will produce remarks that are pushed
                    before the ace entry.
                  - Remarks entry used as the only key in as the list option
                    will produce non ace specific remarks, these remarks would be
                    pushed at the end of all the aces for an acl.
                  - Remarks is treated a block, for every single remarks updated for
                    an ace all the remarks are negated and added back to maintain the
                    order of remarks mentioned.
                  - As the appliance deletes all the remarks once the ace is updated,
                    the set of remarks would be re-applied that is an expected behavior.
                elements: str
                type: list
              sequence:
                description:
                  - Sequence Number for the Access Control Entry(ACE).
                  - Refer to vendor documentation for valid values.
                type: int
              source:
                description: Specify the packet source.
                suboptions:
                  address:
                    description: Source network address.
                    type: str
                  any:
                    description: Match any source address.
                    type: bool
                  host:
                    description: A single source host
                    type: str
                  object_group:
                    description: Source network object group
                    type: str
                  port_protocol:
                    description:
                      - Specify the source port along with protocol.
                      - Note, Valid with TCP/UDP protocol_options
                    suboptions:
                      eq:
                        description: Match only packets on a given port number.
                        type: str
                      gt:
                        description: Match only packets with a greater port number.
                        type: str
                      lt:
                        description: Match only packets with a lower port number.
                        type: str
                      neq:
                        description: Match only packets not on a given port number.
                        type: str
                      range:
                        description: Port group.
                        suboptions:
                          end:
                            description: Specify the end of the port range.
                            type: int
                          start:
                            description: Specify the start of the port range.
                            type: int
                        type: dict
                    type: dict
                  wildcard_bits:
                    description: Source wildcard bits, valid with IPV4 address.
                    type: str
                type: dict
              time_range:
                description: Specify a time-range.
                type: str
              tos:
                description:
                  - Match packets with given TOS value.
                  - Note, DSCP and TOS are mutually exclusive
                suboptions:
                  max_reliability:
                    description: Match packets with max reliable TOS (2).
                    type: bool
                  max_throughput:
                    description: Match packets with max throughput TOS (4).
                    type: bool
                  min_delay:
                    description: Match packets with min delay TOS (8).
                    type: bool
                  min_monetary_cost:
                    description: Match packets with min monetary cost TOS (1).
                    type: bool
                  normal:
                    description: Match packets with normal TOS (0).
                    type: bool
                  service_value:
                    description: Type of service value
                    type: int
                type: dict
              ttl:
                description: Match packets with given TTL value.
                suboptions:
                  eq:
                    description: Match only packets on a given TTL number.
                    type: int
                  gt:
                    description: Match only packets with a greater TTL number.
                    type: int
                  lt:
                    description: Match only packets with a lower TTL number.
                    type: int
                  neq:
                    description: Match only packets not on a given TTL number.
                    type: int
                  range:
                    description: Match only packets in the range of TTLs.
                    suboptions:
                      end:
                        description: Specify the end of the port range.
                        type: int
                      start:
                        description: Specify the start of the port range.
                        type: int
                    type: dict
                type: dict
            type: list
          acl_type:
            choices:
              - extended
              - standard
            description:
              - ACL type
              - Note, it's mandatory and required for Named ACL, but for Numbered ACL it's not mandatory.
            type: str
          name:
            description: The name or the number of the ACL.
            required: true
            type: str
        type: list
      afi:
        choices:
          - ipv4
          - ipv6
        description:
          - The Address Family Indicator (AFI) for the Access Control Lists (ACL).
        required: true
        type: str
    type: list
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from
        the IOS device by executing the command B(sh access-list).
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
      - gathered
      - rendered
      - parsed
    default: merged
    description:
      - The state the configuration should be left in
      - The state I(merged) is the default state which merges the want and
        have config, but for ACL module as the IOS platform doesn't allow
        update of ACE over an pre-existing ACE sequence in ACL, same way ACLs
        resource module will error out for respective scenario and only addition
        of new ACE over new sequence will be allowed with merge state.
      - The states I(rendered), I(gathered) and I(parsed) does not perform any
        change on the device.
      - The state I(rendered) will transform the configuration in C(config)
        option to platform specific CLI commands which will be returned in
        the I(rendered) key within the result. For state I(rendered) active
        connection to remote host is not required.
      - The state I(gathered) will fetch the running configuration from device
        and transform it into structured data in the format as per the resource
        module argspec and the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option
        and transforms it into JSON format as per the resource module parameters
        and the value is returned in the I(parsed) key within the result. The
        value of C(running_config) option should be the same format as the output
        of commands I(sh running-config | section access-list) for all acls related information
        and I(sh access-lists | include access list) to obtain configuration specific of
        an empty acls, the following commands are executed on
        device. Config data from both the commands should be kept together one after
        another for the parsers to pick the commands correctly.
        For state I(parsed) active connection to remote host is not required.
      - The state I(overridden), modify/add the ACLs defined, deleted all other ACLs.
      - The state I(replaced), modify/add only the ACEs of the ACLs defined only.
        It does not perform any other change on the device.
      - The state I(deleted), deletes only the specified ACLs, or all if not specified.
    type: str
short_description: Resource module to configure ACLs.
version_added: 1.0.0
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list extended 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10

- name: Merge provided configuration with device configuration
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: std_acl
            acl_type: standard
            aces:
              - grant: deny
                source:
                  address: 192.168.1.200
              - grant: deny
                source:
                  address: 192.168.2.0
                  wildcard_bits: 0.0.0.255
          - name: 110
            aces:
              - sequence: 10
                protocol_options:
                  icmp:
                    traceroute: true
                source:
                  address: 192.168.3.0
                  wildcard_bits: 255.255.255.0
                destination:
                  any: true
                grant: permit
              - grant: deny
                protocol_options:
                  tcp:
                    ack: true
                source:
                  host: 198.51.100.0
                destination:
                  host: 198.51.110.0
                  port_protocol:
                    eq: telnet
          - name: extended_acl_1
            acl_type: extended
            aces:
              - grant: deny
                protocol_options:
                  tcp:
                    fin: true
                source:
                  address: 192.0.2.0
                  wildcard_bits: 0.0.0.255
                destination:
                  address: 192.0.3.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: www
                option:
                  traceroute: true
                ttl:
                  eq: 10
          - name: 123
            aces:
              - remarks:
                  - "remarks for extended ACL 1"
                  - "check ACL"
              - grant: deny
                protocol_options:
                  tcp:
                    ack: true
                source:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                destination:
                  address: 198.51.101.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                tos:
                  service_value: 12
              - grant: deny
                protocol_options:
                  tcp:
                    ack: true
                source:
                  address: 192.0.3.0
                  wildcard_bits: 0.0.0.255
                destination:
                  address: 192.0.4.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: www
                dscp: ef
                ttl:
                  lt: 20
      - afi: ipv6
        acls:
          - name: R1_TRAFFIC
            aces:
              - grant: deny
                protocol_options:
                  tcp:
                    ack: true
                source:
                  any: true
                  port_protocol:
                    eq: www
                destination:
                  any: true
                  port_protocol:
                    eq: telnet
                dscp: af11
    state: merged

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            echo: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: '100'
#    afi: ipv4
# commands:
#  - ip access-list extended 110
#  - deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
#  - 30 permit icmp 192.168.3.0 255.255.255.0 any traceroute
#  - ip access-list extended extended_acl_1
#  - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
#  - ip access-list standard std_acl
#  - deny 192.168.1.20
#  - deny 192.168.2.0 0.0.0.255
#  - ip access-list extended 123
#  - deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#  - deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
#  - remark remarks for extended ACL 1
#  - remark check ACL
#  - ipv6 access-list R1_TRAFFIC
#  - deny tcp any eq www any eq telnet ack dscp af11
# after:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            echo: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      - destination:
#          any: true
#        grant: permit
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 30
#        source:
#          address: 0.0.0.0
#          wildcard_bits: 255.255.255.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      - remarks:
#        - remarks for extended ACL 1
#        - check ACL
#      acl_type: extended
#      name: '123'
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: extended_acl_1
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.20
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    afi: ipv4
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6

# After state:
# ------------
#
# vios#sh running-config | section access-list
# ip access-list standard std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 100
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
# ip access-list extended 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ipv6 access-list R1_TRAFFIC
#    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

# vios#show running-config | include ip(v6)* access-list|remark
# ip access-list standard std_acl
# ip access-list extended extended_acl_1
# ip access-list extended 110
# ip access-list extended 123
#  remark remarks for extended ACL 1
#  remark check ACL
# ipv6 access-list R1_TRAFFIC

# Using merged (update existing ACE - will fail)

# Before state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list extended 100
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10

- name: Merge provided configuration with device configuration
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: 100
            aces:
              - sequence: 10
                protocol_options:
                  icmp:
                    traceroute: true
    state: merged

# After state:
# ------------
#
# Play Execution fails, with error:
# Cannot update existing sequence 10 of ACLs 100 with state merged.
# Please use state replaced or overridden.

# Using replaced

# Before state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list standard std_acl
#     10 deny   192.168.1.200
#     20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended R1_TRAFFIC
#     10 deny tcp any eq www any eq telnet ack dscp af11
# ip access-list extended test
#     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

- name: Replaces device configuration of listed acls with provided configuration
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: 110
            aces:
              - grant: deny
                protocol_options:
                  tcp:
                    syn: true
                source:
                  address: 192.0.2.0
                  wildcard_bits: 0.0.0.255
                destination:
                  address: 192.0.3.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: www
                dscp: ef
                ttl:
                  eq: 10
          - name: 150
            aces:
              - grant: deny
                sequence: 20
                protocol_options:
                  tcp:
                    syn: true
                source:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                destination:
                  address: 198.51.110.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                dscp: ef
                ttl:
                  eq: 10
    state: replaced

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      acl_type: extended
#      name: R1_TRAFFIC
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4
# commands:
#  - ip access-list extended 110
#  - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#  - no 20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
#  - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
#  - ip access-list extended 150
#  - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
# after:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            syn: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - destination:
#          address: 198.51.110.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            syn: true
#        sequence: 20
#        source:
#          address: 198.51.100.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: '150'
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      acl_type: extended
#      name: R1_TRAFFIC
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4

# After state:
# -------------
#
# vios#sh access-lists
# ip access-list standard std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
# ip access-list extended 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended 150
#    20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
# ip access-list extended test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ipv6 access-list R1_TRAFFIC
#    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

# Using replaced - example remarks specific

# Before state:
# -------------
#
# vios#show running-config | section access-list
# ip access-list extended TEST
#  10 remark FIRST REMARK BEFORE LINE 10
#  10 remark ============
#  10 remark ALLOW HOST FROM TEST 10
#  10 permit ip host 1.1.1.1 any
#  20 remark FIRST REMARK BEFORE LINE 20
#  20 remark ============
#  20 remark ALLOW HOST remarks AFTER LINE  20
#  20 permit ip host 2.2.2.2 any
#  30 remark FIRST REMARK BEFORE LINE 30
#  30 remark ============
#  30 remark ALLOW HOST remarks AFTER LINE  30
#  30 permit ip host 3.3.3.3 any

- name: Replace remarks of ace with sequence 10
  # check_mode: true
  cisco.ios.ios_acls:
    state: replaced
    config:
      - acls:
          - aces:
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - The new first remarks before 10
                  - ============new
                  - The new second remarks before 10
                sequence: 10
                source:
                  host: 1.1.1.1
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - FIRST REMARK BEFORE LINE 20
                  - ============
                  - ALLOW HOST remarks AFTER LINE  20
                sequence: 20
                source:
                  host: 2.2.2.2
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - FIRST REMARK BEFORE LINE 30
                  - ============
                  - ALLOW HOST remarks AFTER LINE  30
                sequence: 30
                source:
                  host: 3.3.3.3
            acl_type: extended
            name: TEST
        afi: ipv4

# Task Output
# -----------
#
# before:
# - acls:
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 10
#       - ===========1=
#       - ALLOW HOST FROM TEST 10
#       sequence: 10
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 20
#       - ============
#       - ALLOW HOST remarks AFTER LINE  20
#       sequence: 20
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 30
#       - ============
#       - ALLOW HOST remarks AFTER LINE  30
#       sequence: 30
#       source:
#         host: 3.3.3.3
#     acl_type: extended
#     name: TEST
#   afi: ipv4
# commands:
# - ip access-list extended TEST
# - no 10 remark
# - 10 remark The new first remarks before 10
# - 10 remark ============new
# - 10 remark The new second remarks before 10
# after:
# - acls:
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - The new first remarks before 10
#       - ============new
#       - The new second remarks before 10
#       sequence: 10
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 20
#       - ============
#       - ALLOW HOST remarks AFTER LINE  20
#       sequence: 20
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 30
#       - ============
#       - ALLOW HOST remarks AFTER LINE  30
#       sequence: 30
#       source:
#         host: 3.3.3.3
#     acl_type: extended
#     name: TEST
#   afi: ipv4

# After state:
# -------------
#
# foo#show running-config | section access-list
# ip access-list extended TEST
#  10 remark The new first remarks before 10
#  10 remark ============new
#  10 remark The new second remarks before 10
#  10 permit ip host 1.1.1.1 any
#  20 remark FIRST REMARK BEFORE LINE 20
#  20 remark ============
#  20 remark ALLOW HOST remarks AFTER LINE  20
#  20 permit ip host 2.2.2.2 any
#  30 remark FIRST REMARK BEFORE LINE 30
#  30 remark ============
#  30 remark ALLOW HOST remarks AFTER LINE  30
#  30 permit ip host 3.3.3.3 any

# Using replaced - example remarks specific on targeted sequence

# Before state:
# -------------
#
# vios#show running-config | section access-list
# ip access-list extended TEST
#  10 permit ip host 1.1.1.1 any
#  20 remark FIRST REMARK BEFORE LINE 20
#  20 remark ============
#  20 remark ALLOW HOST remarks AFTER LINE  20
#  20 permit ip host 2.2.2.2 any
#  30 remark FIRST REMARK BEFORE LINE 30
#  30 remark ============
#  30 remark ALLOW HOST remarks AFTER LINE  30
#  30 permit ip host 3.3.3.3 any

- name: Replace remarks of ace with sequence 10
  # check_mode: true
  cisco.ios.ios_acls:
    state: replaced
    config:
      - acls:
          - aces:
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - The new first remarks before 10
                  - ============new
                  - The new second remarks before 10
                sequence: 10
                source:
                  host: 1.1.1.1
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - FIRST REMARK BEFORE LINE 20
                  - ============
                  - ALLOW HOST remarks AFTER LINE  20
                sequence: 20
                source:
                  host: 2.2.2.2
              - destination:
                  any: true
                grant: permit
                protocol: ip
                remarks:
                  - FIRST REMARK BEFORE LINE 30
                  - ============
                  - ALLOW HOST remarks AFTER LINE  30
                sequence: 30
                source:
                  host: 3.3.3.3
            acl_type: extended
            name: TEST
        afi: ipv4

# Task Output
# -----------
#
# before:
# - acls:
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       sequence: 10
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 20
#       - ============
#       - ALLOW HOST remarks AFTER LINE  20
#       sequence: 20
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 30
#       - ============
#       - ALLOW HOST remarks AFTER LINE  30
#       sequence: 30
#       source:
#         host: 3.3.3.3
#     acl_type: extended
#     name: TEST
#   afi: ipv4
# commands:
# - ip access-list extended TEST
# - 10 remark The new first remarks before 10
# - 10 remark ============new
# - 10 remark The new second remarks before 10
# after:
# - acls:
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - The new first remarks before 10
#       - ============new
#       - The new second remarks before 10
#       sequence: 10
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 20
#       - ============
#       - ALLOW HOST remarks AFTER LINE  20
#       sequence: 20
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE LINE 30
#       - ============
#       - ALLOW HOST remarks AFTER LINE  30
#       sequence: 30
#       source:
#         host: 3.3.3.3
#     acl_type: extended
#     name: TEST
#   afi: ipv4

# After state:
# -------------
#
# foo#show running-config | section access-list
# ip access-list extended TEST
#  10 remark The new first remarks before 10
#  10 remark ============new
#  10 remark The new second remarks before 10
#  10 permit ip host 1.1.1.1 any
#  20 remark FIRST REMARK BEFORE LINE 20
#  20 remark ============
#  20 remark ALLOW HOST remarks AFTER LINE  20
#  20 permit ip host 2.2.2.2 any
#  30 remark FIRST REMARK BEFORE LINE 30
#  30 remark ============
#  30 remark ALLOW HOST remarks AFTER LINE  30
#  30 permit ip host 3.3.3.3 any

# Using overridden

# Before state:
# -------------
#
# vios#sh access-lists
# ip access-list standard std_acl
#     10 deny   192.168.1.200
#     20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended R1_TRAFFIC
#     10 deny tcp any eq www any eq telnet ack dscp af11
# ip access-list extended test
#     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

- name: Override device configuration of all acls with provided configuration
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: 110
            aces:
              - grant: deny
                sequence: 20
                protocol_options:
                  tcp:
                    ack: true
                source:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                destination:
                  address: 198.51.110.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: www
                dscp: ef
                ttl:
                  eq: 10
          - name: 150
            aces:
              - grant: deny
                sequence: 10
                protocol_options:
                  tcp:
                    syn: true
                source:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                destination:
                  address: 198.51.110.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                dscp: ef
                ttl:
                  eq: 10
    state: overridden

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      acl_type: extended
#      name: R1_TRAFFIC
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4
# commands:
#  - ip access-list extended 110
#  - no 20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
#  - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#  - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10
#  - ip access-list extended 150
#  - 10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
#  - no ip access-list extended 123
#  - no ip access-list extended R1_TRAFFIC
#  - no ip access-list standard std_acl
#  - no ip access-list extended test
# after:
#  - acls:
#    - aces:
#      - destination:
#          address: 198.51.110.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 198.51.100.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.110.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            syn: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: '150'
#    afi: ipv4

# After state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list extended 110
#     20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10
# ip access-list extended 150
#     10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

# Using overridden - example remarks specific on multiple sequence

# Before state:
# -------------
#
# vios#show running-config | section access-list
# ip access-list extended TEST
#  10 remark FIRST REMARK BEFORE SEQUENCE 10
#  10 remark ============
#  10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
#  20 remark FIRST REMARK BEFORE SEQUENCE 20
#  20 remark ============
#  20 remark ALLOW HOST FROM SEQUENCE 20
#  20 permit ip host 1.1.1.1 any
#  30 remark FIRST REMARK BEFORE SEQUENCE 30
#  30 remark ============
#  30 remark ALLOW HOST FROM SEQUENCE 30
#  30 permit ip host 2.2.2.2 any
#  40 remark FIRST REMARK BEFORE SEQUENCE 40
#  40 remark ============
#  40 remark ALLOW NEW HOST FROM SEQUENCE 40
#  40 permit ip host 3.3.3.3 any
#  remark Remark not specific to sequence
#  remark ============
#  remark End Remarks
# ip access-list extended test_acl
#  10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ip access-list extended 110
#  10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
# ip access-list extended 123
#  10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#  20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ipv6 access-list R1_TRAFFIC
#  sequence 10 deny tcp any eq www any eq telnet ack dscp af11

- name: Override remarks and ace configurations
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: TEST
            acl_type: extended
            aces:
              - sequence: 10
                remarks:
                  - "FIRST REMARK BEFORE SEQUENCE 10"
                  - "============"
                  - "REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE"
                grant: permit
                protocol: ip
                source:
                  host: 1.1.1.1
                destination:
                  any: true
              - sequence: 20
                remarks:
                  - "FIRST REMARK BEFORE SEQUENCE 20"
                  - "============"
                  - "ALLOW HOST FROM SEQUENCE 20"
                grant: permit
                protocol: ip
                source:
                  host: 192.168.0.1
                destination:
                  any: true
              - sequence: 30
                remarks:
                  - "FIRST REMARK BEFORE SEQUENCE 30"
                  - "============"
                  - "ALLOW HOST FROM SEQUENCE 30 updated"
                grant: permit
                protocol: ip
                source:
                  host: 2.2.2.2
                destination:
                  any: true
              - sequence: 40
                remarks:
                  - "FIRST REMARK BEFORE SEQUENCE 40"
                  - "============"
                  - "ALLOW NEW HOST FROM SEQUENCE 40"
                grant: permit
                protocol: ip
                source:
                  host: 3.3.3.3
                destination:
                  any: true
              - remarks:
                  - "Remark not specific to sequence"
                  - "============"
                  - "End Remarks 1"
    state: overridden

# Task Output
# -----------
#
# before:
# - acls:
#   - aces:
#     - destination:
#         address: 192.0.3.0
#         wildcard_bits: 0.0.0.255
#       dscp: ef
#       grant: deny
#       protocol: icmp
#       protocol_options:
#         icmp:
#           echo: true
#       sequence: 10
#       source:
#         address: 192.0.2.0
#         wildcard_bits: 0.0.0.255
#       ttl:
#         eq: 10
#     acl_type: extended
#     name: '110'
#   - aces:
#     - destination:
#         address: 198.51.101.0
#         port_protocol:
#           eq: telnet
#         wildcard_bits: 0.0.0.255
#       grant: deny
#       protocol: tcp
#       protocol_options:
#         tcp:
#           ack: true
#       sequence: 10
#       source:
#         address: 198.51.100.0
#         wildcard_bits: 0.0.0.255
#       tos:
#         service_value: 12
#     - destination:
#         address: 192.0.4.0
#         port_protocol:
#           eq: www
#         wildcard_bits: 0.0.0.255
#       dscp: ef
#       grant: deny
#       protocol: tcp
#       protocol_options:
#         tcp:
#           ack: true
#       sequence: 20
#       source:
#         address: 192.0.3.0
#         wildcard_bits: 0.0.0.255
#       ttl:
#         lt: 20
#     acl_type: extended
#     name: '123'
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 20
#       - ============
#       - ALLOW HOST FROM SEQUENCE 20
#       sequence: 20
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 30
#       - ============
#       - ALLOW HOST FROM SEQUENCE 30
#       sequence: 30
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 40
#       - ============
#       - ALLOW NEW HOST FROM SEQUENCE 40
#       sequence: 40
#       source:
#         host: 3.3.3.3
#     - remarks:
#       - FIRST REMARK BEFORE SEQUENCE 10
#       - ============
#       - REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
#       sequence: 10
#     - remarks:
#       - Remark not specific to sequence
#       - ============
#       - End Remarks
#     acl_type: extended
#     name: TEST
#   - aces:
#     - destination:
#         address: 192.0.3.0
#         port_protocol:
#           eq: www
#         wildcard_bits: 0.0.0.255
#       grant: deny
#       option:
#         traceroute: true
#       protocol: tcp
#       protocol_options:
#         tcp:
#           fin: true
#       sequence: 10
#       source:
#         address: 192.0.2.0
#         wildcard_bits: 0.0.0.255
#       ttl:
#         eq: 10
#     acl_type: extended
#     name: test_acl
#   afi: ipv4
# - acls:
#   - aces:
#     - destination:
#         any: true
#         port_protocol:
#           eq: telnet
#       dscp: af11
#       grant: deny
#       protocol: tcp
#       protocol_options:
#         tcp:
#           ack: true
#       sequence: 10
#       source:
#         any: true
#         port_protocol:
#           eq: www
#     name: R1_TRAFFIC
#   afi: ipv6
# commands:
# - no ipv6 access-list R1_TRAFFIC
# - ip access-list extended TEST
# - no 10  # removes all remarks and ace entry for sequence 10
# - no 20 permit ip host 1.1.1.1 any  # removing the ace automatically removes the remarks
# - no 30 remark  # just remove remarks for sequence 30
# - no remark  # remove all remarks at end of acl, that has no sequence
# - 10 remark FIRST REMARK BEFORE SEQUENCE 10
# - 10 remark ============
# - 10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
# - 10 permit ip host 1.1.1.1 any
# - 20 remark FIRST REMARK BEFORE SEQUENCE 20
# - 20 remark ============
# - 20 remark ALLOW HOST FROM SEQUENCE 20
# - 20 permit ip host 192.168.0.1 any
# - 30 remark FIRST REMARK BEFORE SEQUENCE 30
# - 30 remark ============
# - 30 remark ALLOW HOST FROM SEQUENCE 30 updated
# - remark Remark not specific to sequence
# - remark ============
# - remark End Remarks 1
# - no ip access-list extended 110
# - no ip access-list extended 123
# - no ip access-list extended test_acl
# after:
# - acls:
#   - aces:
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 10
#       - ============
#       - REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
#       sequence: 10
#       source:
#         host: 1.1.1.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 20
#       - ============
#       - ALLOW HOST FROM SEQUENCE 20
#       sequence: 20
#       source:
#         host: 192.168.0.1
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 30
#       - ============
#       - ALLOW HOST FROM SEQUENCE 30 updated
#       sequence: 30
#       source:
#         host: 2.2.2.2
#     - destination:
#         any: true
#       grant: permit
#       protocol: ip
#       remarks:
#       - FIRST REMARK BEFORE SEQUENCE 40
#       - ============
#       - ALLOW NEW HOST FROM SEQUENCE 40
#       sequence: 40
#       source:
#         host: 3.3.3.3
#     - remarks:
#       - Remark not specific to sequence
#       - ============
#       - End Remarks 1
#     acl_type: extended
#     name: TEST
#   afi: ipv4

# After state:
# -------------
#
# foo#show running-config | section access-list
# ip access-list extended TEST
#  10 remark FIRST REMARK BEFORE SEQUENCE 10
#  10 remark ============
#  10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
#  10 permit ip host 1.1.1.1 any
#  20 remark FIRST REMARK BEFORE SEQUENCE 20
#  20 remark ============
#  20 remark ALLOW HOST FROM SEQUENCE 20
#  20 permit ip host 192.168.0.1 any
#  30 remark FIRST REMARK BEFORE SEQUENCE 30
#  30 remark ============
#  30 remark ALLOW HOST FROM SEQUENCE 30 updated
#  30 permit ip host 2.2.2.2 any
#  40 remark FIRST REMARK BEFORE SEQUENCE 40
#  40 remark ============
#  40 remark ALLOW NEW HOST FROM SEQUENCE 40
#  40 permit ip host 3.3.3.3 any
#  remark Remark not specific to sequence
#  remark ============
#  remark End Remarks 1

# Using deleted - delete ACL(s)

# Before state:
# -------------
#
# vios#sh access-lists
# ip access-list standard std_acl
#     10 deny   192.168.1.200
#     20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended extended_acl_1
#     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

- name: "Delete ACLs (Note: This won't delete the all configured ACLs)"
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: extended_acl_1
            acl_type: extended
          - name: 110
    state: deleted

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: extended_acl_1
#    afi: ipv4
# commands:
#  - no ip access-list extended 110
#  - no ip access-list extended extended_acl_1
# after:
#  - acls:
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    afi: ipv4

# After state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list standard std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20

# Using deleted - delete ACLs based on AFI

# Before state:
# -------------
#
# vios#sh running-config | section access-list
# ip access-list standard std_acl
#     10 deny   192.168.1.200
#     20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended test
#     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ipv6 access-list R1_TRAFFIC
#     sequence 10 deny tcp any eq www any eq telnet ack dscp af11

- name: "Delete ACLs based on AFI (Note: This won't delete the all configured ACLs)"
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
    state: deleted

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6
# commands:
#  - no ip access-list extended 110
#  - no ip access-list extended 123
#  - no ip access-list standard std_acl
#  - no ip access-list extended test
# after:
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6

# After state:
# -------------
#
# vios#sh running-config | section access-list
# ipv6 access-list R1_TRAFFIC
#    sequence 10 deny tcp any eq www any eq telnet ack dscp af11


# Using deleted - delete all ACLs

# Before state:
# -------------
#
# vios#sh access-lists
# ip access-list standard std_acl
#     10 deny   192.168.1.200
#     20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended test
#     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ipv6 access-list R1_TRAFFIC
#     sequence 10 deny tcp any eq www any eq telnet ack dscp af11

- name: Delete ALL of configured ACLs
  cisco.ios.ios_acls:
    state: deleted

# Task Output
# -----------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6
# commands:
#  - no ip access-list extended test
#  - no ip access-list extended 110
#  - no ip access-list extended 123
#  - no ip access-list extended test
#  - no ipv6 access-list R1_TRAFFIC
# after: []

# After state:
# -------------
#
# vios#sh running-config | section access-list


# Using gathered

# Before state:
# -------------
#
# vios#sh access-lists
# ip access-list standard std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0 0.0.0.255
# ip access-list extended 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# ip access-list extended 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# ip access-list extended test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# ipv6 access-list R1_TRAFFIC
#    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

- name: Gather ACLs configuration from target device
  cisco.ios.ios_acls:
    state: gathered

# Module Execution Result:
# ------------------------
#
# before:
#  - acls:
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: icmp
#        protocol_options:
#          icmp:
#            traceroute: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      - destination:
#          host: 198.51.110.0
#          port_protocol:
#            eq: telnet
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          host: 198.51.100.0
#      acl_type: extended
#      name: '110'
#    - aces:
#      - destination:
#          address: 198.51.101.0
#          port_protocol:
#            eq: telnet
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          address: 198.51.100.0
#          wildcard_bits: 0.0.0.255
#        tos:
#          service_value: 12
#      - destination:
#          address: 192.0.4.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        dscp: ef
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 20
#        source:
#          address: 192.0.3.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          lt: 20
#      acl_type: extended
#      name: '123'
#    - aces:
#      - grant: deny
#        sequence: 10
#        source:
#          host: 192.168.1.200
#      - grant: deny
#        sequence: 20
#        source:
#          address: 192.168.2.0
#          wildcard_bits: 0.0.0.255
#      acl_type: standard
#      name: std_acl
#    - aces:
#      - destination:
#          address: 192.0.3.0
#          port_protocol:
#            eq: www
#          wildcard_bits: 0.0.0.255
#        grant: deny
#        option:
#          traceroute: true
#        protocol: tcp
#        protocol_options:
#          tcp:
#            fin: true
#        sequence: 10
#        source:
#          address: 192.0.2.0
#          wildcard_bits: 0.0.0.255
#        ttl:
#          eq: 10
#      acl_type: extended
#      name: test
#    afi: ipv4
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6

# Using rendered

- name: Render the provided configuration into platform specific configuration lines
  cisco.ios.ios_acls:
    config:
      - afi: ipv4
        acls:
          - name: 110
            aces:
              - grant: deny
                sequence: 10
                protocol_options:
                  tcp:
                    syn: true
                source:
                  address: 192.0.2.0
                  wildcard_bits: 0.0.0.255
                destination:
                  address: 192.0.3.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: www
                dscp: ef
                ttl:
                  eq: 10
          - name: 150
            aces:
              - grant: deny
                protocol_options:
                  tcp:
                    syn: true
                source:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                destination:
                  address: 198.51.110.0
                  wildcard_bits: 0.0.0.255
                  port_protocol:
                    eq: telnet
                dscp: ef
                ttl:
                  eq: 10
    state: rendered

# Module Execution Result:
# ------------------------
#
# rendered:
#  - ip access-list extended 110
#  - 10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
#  - ip access-list extended 150
#  - deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

# Using Parsed

# File: parsed.cfg
# ----------------
#
# IPv6 access-list R1_TRAFFIC
# deny tcp any eq www any eq telnet ack dscp af11

- name: Parse the commands for provided configuration
  cisco.ios.ios_acls:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# parsed:
#  - acls:
#    - aces:
#      - destination:
#          any: true
#          port_protocol:
#            eq: telnet
#        dscp: af11
#        grant: deny
#        protocol: tcp
#        protocol_options:
#          tcp:
#            ack: true
#        sequence: 10
#        source:
#          any: true
#          port_protocol:
#            eq: www
#      name: R1_TRAFFIC
#    afi: ipv6
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
    - ip access-list extended 110
    - deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    - permit ip host 2.2.2.2 host 3.3.3.3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - ip access-list extended test
    - permit ip host 2.2.2.2 host 3.3.3.3
    - permit tcp host 1.1.1.1 host 5.5.5.5 eq www
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acls.acls import (
    AclsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.acls.acls import Acls


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=AclsArgs.argument_spec,
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

    result = Acls(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
