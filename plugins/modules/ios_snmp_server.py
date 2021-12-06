#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_snmp_server
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author:
  - Sagar Paul (@KB-perByte)
description:
  - This module provides declarative management of SNMP server on Cisco IOS devices.
module: ios_snmp_server
notes:
  - Tested against Cisco IOSv Version 15.6.
  - This module works with connection C(network_cli).
options:
  config:
    description: A dictionary of SNMP server configuration
    suboptions:
      accounting:
        description: SNMP Accounting parameters
        suboptions:
          command:
            description: For SNMP set commands
            type: str
        type: dict
      cache:
        description: Enable SNMP cache and MIB expiry interval
        type: int
      chassis_id:
        description: String to uniquely identify this chassis (Hexadecimal)
        type: str
      communities:
        description: Community name configuration.
        elements: dict
        suboptions:
          acl_v4:
            description: standard access-list name
            type: str
          acl_v6:
            description: IPv6 access list name
            type: str
          name:
            description: Community name (default RO)
            type: str
          ro:
            description: Only reads are permitted
            type: bool
          rw:
            description: Read-write access
            type: bool
          view:
            description: MIB view name
            type: str
        type: list
      contact:
        description: Text for mib object sysContact
        type: str
      context:
        description: Create/Delete a context apart from default
        elements: str
        type: list
      drop:
        description: Silently drop SNMP packets
        suboptions:
          unknown_user:
            description: Silently drop unknown v3 user packets
            type: bool
          vrf_traffic:
            description: Silently drop SNMP packets that come on VRF interfaces
            type: bool
        type: dict
      engine_id:
        description: Configure a local or remote SNMPv3 engineID
        elements: dict
        suboptions:
          id:
            description: engine ID octet string
            type: str
          local:
            description: Local SNMP agent
            type: bool
          remote:
            description: Remote SNMP agent
            suboptions:
              host:
                description: Hostname or IP address of remote SNMP notification host
                type: str
              udp_port:
                description: The remote SNMP notification host's UDP port number.
                type: int
              vrf:
                description: The remote notification host's VPN routing instance
                type: str
            type: dict
        type: list
      file_transfer:
        description: File transfer related commands
        suboptions:
          access_group:
            description: Access control for file transfers
            type: str
          protocol:
            description: Access control protocol for file transfers
            type: list
            elements: str
        type: dict
      groups:
        description: Define a User Security Model group
        elements: dict
        suboptions:
          context:
            description: Specify a context to associate with the group
            type: str
          version_option:
            choices:
              - auth
              - noauth
              - priv
            description: community name to the host.
            type: str
          group:
            description: SNMP group for the user
            type: str
          notify:
            description: View to restrict notifications
            type: str
          read:
            description: View to restrict read access
            type: str
          version:
            choices:
              - v1
              - v3
              - v2c
            description: snmp security group version
            type: str
          write:
            description: View to restrict write access
            type: str
          acl_v4:
            description: specify an access-list associated with this group
            type: str
          acl_v6:
            description: specify an access-list associated with this group
            type: str
        type: list
      hosts:
        description: Specify hosts to receive SNMP notifications
        elements: dict
        suboptions:
          host:
            description: Hostname or IP address of SNMP notification host.
            type: str
          informs:
            description: Use SNMP inform messages.
            type: bool
          community_string:
            description: SNMPv1/v2c community string or SNMPv3 user name
            type: str
          traps:
            description: Use SNMP trap messages
            type: list
            elements: str
          version:
            choices:
              - '1'
              - 2c
              - '3'
            description: Notification message SNMP version.
            type: str
          version_option:
            choices:
              - auth
              - noauth
              - priv
            description: community name to the host.
            type: str
          vrf:
            description: Specify the VRF in which the host is configured
            type: str
        type: list
      if_index:
        description: Enable ifindex persistence
        type: bool
      inform:
        description: Configure SNMP Informs options
        suboptions:
          pending:
            description: Set number of unacked informs to hold
            type: int
          retries:
            description: Set retry count for informs
            type: int
          timeout:
            description: Set timeout for informs
            type: int
        type: dict
      ip:
        description: IP ToS configuration for SNMP traffic
        suboptions:
          dscp:
            description: IP DSCP value for SNMP traffic
            type: int
          precedence:
            description: IP Precedence value for SNMP traffic
            type: int
        type: dict
      location:
        description: Text for mib object sysLocation
        type: str
      manager:
        description: Modify SNMP manager parameters
        type: int
      packet_size:
        description: Largest SNMP packet size
        type: int
      password_policy:
        description: SNMP v3 users password policy
        elements: dict
        suboptions:
          change:
            description: Number of Character changes b/w old and new password
            type: int
          digits:
            description: Number of digits
            type: int
          lower_case:
            description: Number of lower-case characters
            type: int
          max_len:
            description: Maximum password length
            type: int
          min_len:
            description: Minimum password length
            type: int
          policy_name:
            description: Name of the policy
            type: str
          special_char:
            description: Number of special case character
            type: int
          upper_case:
            description: Number of upper-case characters
            type: int
          username:
            description: Name of the user
            type: str
        type: list
      queue_length:
        description: Message queue length for each TRAP host
        type: int
      source_interface:
        description: Source interface to be used for sending out SNMP notifications.
        type: str
      system_shutdown:
        description: Enable use of the SNMP reload command
        type: bool
      trap_source:
        description: Assign an interface for the source address of all traps
        type: str
      trap_timeout:
        description: Set timeout for TRAP message retransmissions
        type: int
      traps:
        description: Enable SNMP Traps
        suboptions:
          auth_framework:
            description: Enable SNMP CISCO-AUTH-FRAMEWORK-MIB traps
            suboptions:
              sec_violation:
                description: Mode sec_violation
                type: bool
              enable:
                description: Enable/disable auth framework
                type: bool
            type: dict
          bfd:
            description: Allow SNMP BFD traps
            suboptions:
              enable:
                description: Enable/disable bfd
                type: bool
              session_down:
                description: Enable BFD session down traps
                type: bool
              session_up:
                description: Enable BFD session up traps
                type: bool
            type: dict
          bgp:
            description: Allow bgp traps
            suboptions:
              cbgp2:
                description: Enable BGP MIBv2 traps
                type: bool
              enable:
                description: Enable/disable bgp traps
                type: bool
              state_changes:
                description: Traps for FSM state changes
                suboptions:
                  all:
                    description: CISCO specific trap for all fsm state changes
                    type: bool
                  backward_trans:
                    description: CISCO specific trap for backward transition
                    type: bool
                  limited:
                    description: Trap for standard backward transition and established
                    type: bool
                  enable:
                    description: Enable/disable bgp state_changes traps
                    type: bool
                type: dict
              threshold:
                description: Mode threshold
                suboptions:
                  prefix:
                    description: Enable/disable bgp threshold traps
                    type: bool
                type: dict
            type: dict
          bridge:
            description: Allow bridge related traps
            suboptions:
              newroot:
                description: Enable SNMP STP Bridge MIB newroot traps
                type: bool
              enable:
                description: Enable/disable bridge traps
                type: bool
              topologychange:
                description: Enable SNMP STP Bridge MIB topologychange traps
                type: bool
            type: dict
          casa:
            description: Enable SNMP config casa traps
            type: bool
          cef:
            description: Allow cef related traps
            suboptions:
              inconsistency:
                description: Enable SNMP CEF Inconsistency traps
                type: bool
              peer_fib_state_change:
                description: Enable SNMP CEF Peer FIB State change traps
                type: bool
              peer_state_change:
                description: Enable SNMP CEF Peer state change traps
                type: bool
              resource_failure:
                description: Enable SNMP CEF Resource Failure traps
                type: bool
              enable:
                description: Enable/disable cef traps
                type: bool
            type: dict
          cnpd:
            description: Enable SNMP cnpd traps
            type: bool
          config:
            description: Enable SNMP config traps
            type: bool
          config_copy:
            description: Enable SNMP config copy traps
            type: bool
          config_ctid:
            description: Enable SNMP config ctid traps
            type: bool
          cpu:
            description: Allow CPU related traps
            suboptions:
              enable:
                description: Enable/disable cpu traps
                type: bool
              threshold:
                description: Mode threshold
                type: bool
            type: dict
          dhcp:
            description: Enable SNMP dhcp traps
            type: bool
          dlsw:
            description: Allow dlsw related traps
            suboptions:
              circuit:
                description: Enable SNMP dlsw circuit traps
                type: bool
              enable:
                description: Enable/disable cef traps
                type: bool
              tconn:
                description: Enable SNMP dlsw peer transport connection traps
                type: bool
            type: dict
          eigrp:
            description: Enable SNMP eigrp traps
            type: bool
          entity:
            description: Enable SNMP entity traps
            type: bool
          energywise:
            description: Enable SNMP energywise traps
            type: bool
          ethernet:
            description: Allow ethernet traps
            suboptions:
              cfm:
                description: Enable SNMP Ethernet CFM traps
                suboptions:
                  alarm:
                    description: Enable SNMP Ethernet CFM fault alarm trap
                    type: bool
                  cc:
                    description: Enable SNMP Ethernet CC trap
                    type: dict
                    suboptions:
                      config:
                        description: Enable SNMP Ethernet CFM configuration error traps
                        type: bool
                      cross_connect:
                        description: Enable SNMP Ethernet CFM cross-connect traps
                        type: bool
                      loop:
                        description: Enable SNMP Ethernet CFM loop traps
                        type: bool
                      mep_down:
                        description: Enable SNMP Ethernet CFM CC Down traps
                        type: bool
                      mep_up:
                        description: Enable SNMP Ethernet CFM CC Up traps
                        type: bool
                  crosscheck:
                    description: Enable SNMP Ethernet CC crosscheck trap
                    type: dict
                    suboptions:
                      mep_missing:
                        description: Enable SNMP Ethernet CC crosscheck missing trap
                        type: bool
                      mep_unknown:
                        description: Enable SNMP Ethernet CC crosscheck unknown traps
                        type: bool
                      service_up:
                        description: Enable SNMP Ethernet CC crosscheck service traps
                        type: bool
                type: dict
              evc:
                description: Enable SNMP Ethernet EVC traps
                suboptions:
                  create:
                    description: Enable SNMP Ethernet EVC create traps
                    type: bool
                  delete:
                    description: Enable SNMP Ethernet EVC delete traps
                    type: bool
                  status:
                    description: Enable SNMP Ethernet EVC status traps
                    type: bool
                type: dict
            type: dict
          event_manager:
            description: Enable SNMP event-manager traps
            type: bool
          flowmon:
            description: Enable SNMP flowmon traps
            type: bool
          firewall:
            description: Enable SNMP firewall traps
            suboptions:
              enable:
                description: Enable/disable firewall traps
                type: bool
              serverstatus:
                description: Enable firewall server status change trap
                type: bool
            type: dict
          frame_relay:
            description: Allow frame-relay traps
            suboptions:
              enable:
                description: Enable/disable frame-relay traps
                type: bool
              subif:
                description: Enable SNMP frame-relay subinterface traps
                suboptions:
                  count:
                    description: Maximum number of traps sent per interval
                    type: int
                  interval:
                    description: Interval duration in which to limit the number of traps sent
                    type: int
                  enable:
                    description: Enable/disable subif traps
                    type: bool
                type: dict
            type: dict
          fru_ctrl:
            description: Enable SNMP fru-ctrl traps
            type: bool
          hsrp:
            description: Enable SNMP hsrp traps
            type: bool
          ike:
            description: Allow ike traps
            suboptions:
              policy:
                description: Enable IKE Policy traps
                suboptions:
                  add:
                    description: Enable IKE Policy add trap
                    type: bool
                  delete:
                    description: Enable IKE Policy delete trap
                    type: bool
                type: dict
              tunnel:
                description: Enable IKE Tunnel traps
                suboptions:
                  start:
                    description: Enable IKE Tunnel start trap
                    type: bool
                  stop:
                    description: Enable IKE Tunnel stop trap
                    type: bool
                type: dict
            type: dict
          ipmulticast:
            description: Enable SNMP ip multi cast traps
            type: bool
          ipsec:
            description: Allow ike traps
            suboptions:
              cryptomap:
                description: Enable IPsec Cryptomap traps
                suboptions:
                  add:
                    description: Enable IPsec Cryptomap add trap
                    type: bool
                  attach:
                    description: Enable IPsec Cryptomap Attach trap
                    type: bool
                  delete:
                    description: Enable IPsec Cryptomap delete trap
                    type: bool
                  detach:
                    description: Enable IPsec Cryptomap Detach trap
                    type: bool
                type: dict
              too_many_sas:
                description: Enable IPsec Tunnel Start trap
                type: bool
              tunnel:
                description: Enable IPsec Tunnel traps
                suboptions:
                  start:
                    description: Enable IPsec Tunnel start trap
                    type: bool
                  stop:
                    description: Enable IPsec Tunnel stop trap
                    type: bool
                type: dict
            type: dict
          ipsla:
            description: Enable SNMP ipsla traps
            type: bool
          l2tun:
            description: Allow SNMP l2tun traps
            suboptions:
              pseudowire_status:
                description: Enable BFD pseudo wire status traps
                type: bool
              session:
                description: Enable BFD session traps
                type: bool
            type: dict
          msdp:
            description: Enable SNMP msdp traps
            type: bool
          mvpn:
            description: Enable SNMP mvpn traps
            type: bool
          mpls_vpn:
            description: Enable SNMP mpls traps
            type: bool
          ospf:
            description: Allow ospf related traps
            suboptions:
              cisco_specific:
                description: Cisco specific traps
                suboptions:
                  error:
                    description: error traps
                    type: bool
                  lsa:
                    description: Lsa related traps
                    type: bool
                  retransmit:
                    description: Packet retransmit traps
                    type: bool
                  state_change:
                    description: state change traps
                    suboptions:
                      nssa_trans_change:
                        description: Nssa translator state changes
                        type: bool
                      shamlink:
                        description: Config mismatch errors on virtual interfaces
                        suboptions:
                          interface:
                            description: Sham link interface state changes
                            type: bool
                          neighbor:
                            description: Sham link neighbor state changes
                            type: bool
                        type: dict
                    type: dict
                type: dict
              error:
                description: Enable error traps
                type: bool
              retransmit:
                description: Enable/disable ospf retransmit traps
                type: bool
              lsa:
                description: Enable/disable ospf lsa traps
                type: bool
              state_change:
                description: Enable/disable state change traps
                type: bool
            type: dict
          pim:
            description: Allow PIM traps
            suboptions:
              invalid_pim_message:
                description: Enable invalid pim message trap
                type: bool
              neighbor_change:
                description: Enable neighbor change trap
                type: bool
              rp_mapping_change:
                description: Enable rp mapping change trap
                type: bool
              enable:
                description: Enable/disable PIM traps
                type: bool
            type: dict
          vrfmib:
            description: Allow vrfmib traps
            suboptions:
              vrf_up:
                description: Enable vrf-up trap
                type: bool
              vrf_down:
                description: Enable vrf-down trap
                type: bool
              vnet_trunk_up:
                description: Enable vnet-trunk-up trap
                type: bool
              vnet_trunk_down:
                description: Enable vnet-trunk-down traps
                type: bool
            type: dict
          pki:
            description: Enable SNMP pki traps
            type: bool
          rsvp:
            description: Enable SNMP RSVP traps
            type: bool
          isis:
            description: Enable SNMP isis traps
            type: bool
          pw_vc:
            description: Enable SNMP pw vc traps
            type: bool
          snmp:
            description: Enable SNMP traps
            suboptions:
              authentication:
                description: Enable authentication trap
                type: bool
              coldstart:
                description: Enable coldStart trap
                type: bool
              linkdown:
                description: Enable linkDown trap
                type: bool
              linkup:
                description: Enable linkUp trap
                type: bool
              warmstart:
                description: Enable warmStart trap
                type: bool
            type: dict
          syslog:
            description: Enable SNMP syslog traps
            type: bool
          transceiver_all:
            description: Enable SNMP transceiver traps
            type: bool
          tty:
            description: Enable SNMP tty TCP connection traps
            type: bool
          vrrp:
            description: Enable SNMP vrrp traps
            type: bool
        type: dict
      users:
        description: Define a user who can access the SNMP engine
        elements: dict
        suboptions:
          acl_v6:
            description: Access list ipv6 associated
            type: str
          acl_v4:
            description: Access list ipv4 associated
            type: str
          group:
            description: SNMP group for the user.
            type: str
          remote:
            description: System where an SNMPv3 user is hosted
            type: str
          udp_port:
            description: UDP port used by the remote SNMP system
            type: int
          username:
            description: SNMP user name
            type: str
          version:
            choices:
              - v1
              - v2c
              - v3
            description: SNMP security version
            type: str
          version_option:
            choices:
              - auth
              - access
              - encrypted
            description: community name to the host.
            type: str
          vrf:
            description: The remote SNMP entity's VPN Routing instance
            type: str
        type: list
      views:
        description: Define an SNMPv2 MIB view
        elements: dict
        suboptions:
          excluded:
            description: MIB family is excluded from the view
            type: bool
          family_name:
            description: MIB view family name
            type: str
          included:
            description: MIB family is included in the view
            type: bool
          name:
            description: Name of the view
            type: str
        type: list
    type: dict
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | include snmp-server).
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
      - parsed
      - gathered
      - rendered
    default: merged
    description:
      - The state the configuration should be left in.
      - Refer to examples for more details.
      - The states I(replaced) and I(overridden) have identical
        behaviour for this module.
    type: str
short_description: snmp_server resource module
version_added: 2.6.0
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section ^ntp
# --------------------- EMPTY -----------------

# Merged play:
# ------------

- name: Apply the provided configuration
  cisco.ios.ios_ntp_global:
    config:
      access_group:
        peer:
          - access_list: DHCP-Server
            ipv4: true
            kod: true
          - access_list: preauth_ipv6_acl
            ipv6: true
            kod: true
          - access_list: '2'
            kod: true
        query_only:
          - access_list: '10'
      allow:
        control:
          rate_limit: 4
        private: true
      authenticate: true
      authentication_keys:
        - algorithm: md5
          encryption: 22
          id: 2
          key: SomeSecurePassword
      broadcast_delay: 22
      clock_period: 5
      logging: true
      master:
        stratum: 4
      max_associations: 34
      max_distance: 3
      min_distance: 10
      orphan: 4
      panic_update: true
      peers:
        - peer: 172.16.1.10
          version: 2
        - key: 2
          minpoll: 5
          peer: 172.16.1.11
          prefer: true
          version: 2
        - peer: checkPeerDomainIpv4.com
          prefer: true
          use_ipv4: true
        - peer: checkPeerDomainIpv6.com
          use_ipv6: true
        - peer: testPeerDomainIpv6.com
          prefer: true
          use_ipv6: true
      servers:
        - server: 172.16.1.12
          version: 2
        - server: checkServerDomainIpv6.com
          use_ipv6: true
        - server: 172.16.1.13
          source: GigabitEthernet0/1
      source: GigabitEthernet0/1
      trusted_keys:
        - range_end: 3
          range_start: 3
        - range_start: 21
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#     "ntp allow mode control 4",
#     "ntp allow mode private",
#     "ntp authenticate",
#     "ntp broadcastdelay 22",
#     "ntp clock-period 5",
#     "ntp logging",
#     "ntp master 4",
#     "ntp max-associations 34",
#     "ntp maxdistance 3",
#     "ntp mindistance 10",
#     "ntp orphan 4",
#     "ntp panic update",
#     "ntp source GigabitEthernet0/1",
#     "ntp access-group ipv4 peer DHCP-Server kod",
#     "ntp access-group ipv6 peer preauth_ipv6_acl kod",
#     "ntp access-group peer 2 kod",
#     "ntp access-group query-only 10",
#     "ntp authentication-key 2 md5 SomeSecurePassword 22",
#     "ntp peer 172.16.1.10 version 2",
#     "ntp peer 172.16.1.11 key 2 minpoll 5 prefer  version 2",
#     "ntp peer ip checkPeerDomainIpv4.com prefer",
#     "ntp peer ipv6 checkPeerDomainIpv6.com",
#     "ntp peer ipv6 testPeerDomainIpv6.com prefer",
#     "ntp server 172.16.1.12 version 2",
#     "ntp server ipv6 checkServerDomainIpv6.com",
#     "ntp server 172.16.1.13 source GigabitEthernet0/1",
#     "ntp trusted-key 3 - 3",
#     "ntp trusted-key 21"
# ],


# After state:
# ------------

# router-ios#show running-config | section ^ntp
# ntp max-associations 34
# ntp logging
# ntp allow mode control 4
# ntp panic update
# ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
# ntp authenticate
# ntp trusted-key 3 - 3
# ntp trusted-key 21
# ntp orphan 4
# ntp mindistance 10
# ntp maxdistance 3
# ntp broadcastdelay 22
# ntp source GigabitEthernet0/1
# ntp access-group peer 2 kod
# ntp access-group ipv6 peer preauth_ipv6_acl kod
# ntp master 4
# ntp peer 172.16.1.10 version 2
# ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
# ntp server 172.16.1.12 version 2
# ntp server 172.16.1.13 source GigabitEthernet0/1
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp peer ipv6 checkPeerDomainIpv6.com
# ntp peer ipv6 testPeerDomainIpv6.com prefer
# ntp server ipv6 checkServerDomainIpv6.com

# Using state: deleted

# Before state:
# -------------

# router-ios#show running-config | section ^ntp
# ntp max-associations 34
# ntp logging
# ntp allow mode control 4
# ntp panic update
# ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
# ntp authenticate
# ntp trusted-key 3 - 3
# ntp trusted-key 21
# ntp orphan 4
# ntp mindistance 10
# ntp maxdistance 3
# ntp broadcastdelay 22
# ntp source GigabitEthernet0/1
# ntp access-group peer 2 kod
# ntp access-group ipv6 peer preauth_ipv6_acl kod
# ntp master 4
# ntp peer 172.16.1.10 version 2
# ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
# ntp server 172.16.1.12 version 2
# ntp server 172.16.1.13 source GigabitEthernet0/1
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp peer ipv6 checkPeerDomainIpv6.com
# ntp peer ipv6 testPeerDomainIpv6.com prefer
# ntp server ipv6 checkServerDomainIpv6.com

# Deleted play:
# -------------

- name: Remove all existing configuration
  cisco.ios.ios_ntp_global:
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#     "no ntp allow mode control 4",
#     "no ntp authenticate",
#     "no ntp broadcastdelay 22",
#     "no ntp logging",
#     "no ntp master 4",
#     "no ntp max-associations 34",
#     "no ntp maxdistance 3",
#     "no ntp mindistance 10",
#     "no ntp orphan 4",
#     "no ntp panic update",
#     "no ntp source GigabitEthernet0/1",
#     "no ntp access-group peer 2 kod",
#     "no ntp access-group ipv6 peer preauth_ipv6_acl kod",
#     "no ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7",
#     "no ntp peer 172.16.1.10 version 2",
#     "no ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
#     "no ntp peer ip checkPeerDomainIpv4.com prefer",
#     "no ntp peer ipv6 checkPeerDomainIpv6.com",
#     "no ntp peer ipv6 testPeerDomainIpv6.com prefer",
#     "no ntp server 172.16.1.12 version 2",
#     "no ntp server 172.16.1.13 source GigabitEthernet0/1",
#     "no ntp server ipv6 checkServerDomainIpv6.com",
#     "no ntp trusted-key 21",
#     "no ntp trusted-key 3 - 3"
# ],

# After state:
# ------------

# router-ios#show running-config | section ^ntp
# --------------------- EMPTY -----------------

# Using state: overridden

# Before state:
# -------------

# router-ios#show running-config | section ^ntp
# ntp panic update
# ntp authentication-key 2 md5 00371C0B01680E051A33497E080A16001D1908 7
# ntp authenticate
# ntp trusted-key 3 - 4
# ntp trusted-key 21
# ntp source GigabitEthernet0/1
# ntp peer 172.16.1.10 version 2
# ntp server 172.16.1.12 version 2
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp server ipv6 checkServerDomainIpv6.com

# Overridden play:
# ----------------

- name: Override commands with provided configuration
  cisco.ios.ios_ntp_global:
    config:
      peers:
        - peer: ipv6DomainNew.com
          use_ipv6: true
        - peer: 172.16.1.100
          prefer: true
          use_ipv4: true
      access_group:
        peer:
        - access_list: DHCP-Server
          ipv6: true
    state: overridden

# Commands Fired:
# ---------------
# "commands": [
#       "no ntp authenticate",
#       "no ntp panic update",
#       "no ntp source GigabitEthernet0/1",
#       "ntp access-group ipv6 peer DHCP-Server",
#       "no ntp authentication-key 2 md5 00371C0B01680E051A33497E080A16001D1908 7",
#       "ntp peer ipv6 ipv6DomainNew.com",
#       "ntp peer 172.16.1.100 prefer",
#       "no ntp peer 172.16.1.10 version 2",
#       "no ntp peer ip checkPeerDomainIpv4.com prefer",
#       "no ntp server 172.16.1.12 version 2",
#       "no ntp server ipv6 checkServerDomainIpv6.com",
#       "no ntp trusted-key 21",
#       "no ntp trusted-key 3 - 4"
#     ],

# After state:
# ------------

# router-ios#show running-config | section ^ntp
# ntp access-group ipv6 peer DHCP-Server
# ntp peer ipv6 ipv6DomainNew.com
# ntp peer 172.16.1.100 prefer

# Using state: replaced

# Before state:
# -------------

# router-ios#show running-config | section ^ntp
# ntp access-group ipv6 peer DHCP-Server
# ntp peer ipv6 ipv6DomainNew.com
# ntp peer 172.16.1.100 prefer

# Replaced play:
# --------------

- name: Replace commands with provided configuration
  cisco.ios.ios_ntp_global:
    config:
      broadcast_delay: 22
      clock_period: 5
      logging: true
      master:
        stratum: 4
      max_associations: 34
      max_distance: 3
      min_distance: 10
      orphan: 4
    state: replaced

# Commands Fired:
# ---------------

# "commands": [
#        "ntp broadcastdelay 22",
#        "ntp clock-period 5",
#        "ntp logging",
#        "ntp master 4",
#        "ntp max-associations 34",
#        "ntp maxdistance 3",
#        "ntp mindistance 10",
#        "ntp orphan 4",
#        "no ntp access-group ipv6 peer DHCP-Server",
#        "no ntp peer 172.16.1.100 prefer",
#        "no ntp peer ipv6 ipv6DomainNew.com"
#     ],

# After state:
# ------------

# router-ios#show running-config | section ^ntp
# ntp max-associations 34
# ntp logging
# ntp orphan 4
# ntp mindistance 10
# ntp maxdistance 3
# ntp broadcastdelay 22
# ntp master 4

# Using state: gathered

# Before state:
# -------------

#router-ios#show running-config | section ^ntp
# ntp max-associations 34
# ntp logging
# ntp allow mode control 4
# ntp panic update
# ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
# ntp authenticate
# ntp trusted-key 3 - 3
# ntp trusted-key 21
# ntp orphan 4
# ntp mindistance 10
# ntp maxdistance 3
# ntp broadcastdelay 22
# ntp source GigabitEthernet0/1
# ntp access-group peer 2 kod
# ntp access-group ipv6 peer preauth_ipv6_acl kod
# ntp master 4
# ntp update-calendar
# ntp peer 172.16.1.10 version 2
# ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
# ntp server 172.16.1.12 version 2
# ntp server 172.16.1.13 source GigabitEthernet0/1
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp peer ipv6 checkPeerDomainIpv6.com
# ntp peer ipv6 testPeerDomainIpv6.com prefer
# ntp server ipv6 checkServerDomainIpv6.com

# Gathered play:
# --------------

- name: Gather listed ntp config
  cisco.ios.ios_ntp_global:
    state: gathered

# Module Execution Result:
# ------------------------

# "gathered": {
#   "access_group": {
#       "peer": [
#           {
#               "access_list": "2",
#               "kod": true
#           },
#           {
#               "access_list": "preauth_ipv6_acl",
#               "ipv6": true,
#               "kod": true
#           }
#       ]
#   },
#   "allow": {
#       "control": {
#           "rate_limit": 4
#       }
#   },
#   "authenticate": true,
#   "authentication_keys": [
#       {
#           "algorithm": "md5",
#           "encryption": 7,
#           "id": 2,
#           "key": "0635002C497D0C1A1005173B0D17393C2B3A37"
#       }
#   ],
#   "broadcast_delay": 22,
#   "logging": true,
#   "master": {
#       "stratum": 4
#   },
#   "max_associations": 34,
#   "max_distance": 3,
#   "min_distance": 10,
#   "orphan": 4,
#   "panic_update": true,
#   "peers": [
#       {
#           "peer": "172.16.1.10",
#           "version": 2
#       },
#       {
#           "key": 2,
#           "minpoll": 5,
#           "peer": "172.16.1.11",
#           "prefer": true,
#           "version": 2
#       },
#       {
#           "peer": "checkPeerDomainIpv4.com",
#           "prefer": true,
#           "use_ipv4": true
#       },
#       {
#           "peer": "checkPeerDomainIpv6.com",
#           "use_ipv6": true
#       },
#       {
#           "peer": "testPeerDomainIpv6.com",
#           "prefer": true,
#           "use_ipv6": true
#       }
#   ],
#   "servers": [
#       {
#           "server": "172.16.1.12",
#           "version": 2
#       },
#       {
#           "server": "172.16.1.13",
#           "source": "GigabitEthernet0/1"
#       },
#       {
#           "server": "checkServerDomainIpv6.com",
#           "use_ipv6": true
#       }
#   ],
#   "source": "GigabitEthernet0/1",
#   "trusted_keys": [
#       {
#           "range_start": 21
#       },
#       {
#           "range_end": 3,
#           "range_start": 3
#       }
#   ],
#   "update_calendar": true
# },

# After state:
# -------------

# router-ios#show running-config | section ^ntp
# ntp max-associations 34
# ntp logging
# ntp allow mode control 4
# ntp panic update
# ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
# ntp authenticate
# ntp trusted-key 3 - 3
# ntp trusted-key 21
# ntp orphan 4
# ntp mindistance 10
# ntp maxdistance 3
# ntp broadcastdelay 22
# ntp source GigabitEthernet0/1
# ntp access-group peer 2 kod
# ntp access-group ipv6 peer preauth_ipv6_acl kod
# ntp master 4
# ntp update-calendar
# ntp peer 172.16.1.10 version 2
# ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
# ntp server 172.16.1.12 version 2
# ntp server 172.16.1.13 source GigabitEthernet0/1
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp peer ipv6 checkPeerDomainIpv6.com
# ntp peer ipv6 testPeerDomainIpv6.com prefer
# ntp server ipv6 checkServerDomainIpv6.com

# Using state: rendered

# Rendered play:
# --------------

- name: Render the commands for provided configuration
  cisco.ios.ios_ntp_global:
    config:
      access_group:
        peer:
          - access_list: DHCP-Server
            ipv4: true
            kod: true
          - access_list: preauth_ipv6_acl
            ipv6: true
            kod: true
          - access_list: '2'
            kod: true
        query_only:
          - access_list: '10'
      allow:
        control:
          rate_limit: 4
        private: true
      authenticate: true
      authentication_keys:
        - algorithm: md5
          encryption: 22
          id: 2
          key: SomeSecurePassword
      broadcast_delay: 22
      clock_period: 5
      logging: true
      master:
        stratum: 4
      max_associations: 34
      max_distance: 3
      min_distance: 10
      orphan: 4
      panic_update: true
      peers:
        - peer: 172.16.1.10
          version: 2
        - key: 2
          minpoll: 5
          peer: 172.16.1.11
          prefer: true
          version: 2
        - peer: checkPeerDomainIpv4.com
          prefer: true
          use_ipv4: true
        - peer: checkPeerDomainIpv6.com
          use_ipv6: true
        - peer: testPeerDomainIpv6.com
          prefer: true
          use_ipv6: true
      servers:
        - server: 172.16.1.12
          version: 2
        - server: checkServerDomainIpv6.com
          use_ipv6: true
        - server: 172.16.1.13
          source: GigabitEthernet0/1
      source: GigabitEthernet0/1
      trusted_keys:
        - range_end: 3
          range_start: 10
        - range_start: 21
      update_calendar: True
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#       "ntp allow mode control 4",
#       "ntp allow mode private",
#       "ntp authenticate",
#       "ntp broadcastdelay 22",
#       "ntp clock-period 5",
#       "ntp logging",
#       "ntp master 4",
#       "ntp max-associations 34",
#       "ntp maxdistance 3",
#       "ntp mindistance 10",
#       "ntp orphan 4",
#       "ntp panic update",
#       "ntp source GigabitEthernet0/1",
#       "ntp update-calendar",
#       "ntp access-group ipv4 peer DHCP-Server kod",
#       "ntp access-group ipv6 peer preauth_ipv6_acl kod",
#       "ntp access-group peer 2 kod",
#       "ntp access-group query-only 10",
#       "ntp authentication-key 2 md5 SomeSecurePassword 22",
#       "ntp peer 172.16.1.10 version 2",
#       "ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
#       "ntp peer ip checkPeerDomainIpv4.com prefer",
#       "ntp peer ipv6 checkPeerDomainIpv6.com",
#       "ntp peer ipv6 testPeerDomainIpv6.com prefer",
#       "ntp server 172.16.1.12 version 2",
#       "ntp server ipv6 checkServerDomainIpv6.com",
#       "ntp server 172.16.1.13 source GigabitEthernet0/1",
#       "ntp trusted-key 3 - 3",
#       "ntp trusted-key 21"
#     ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# ntp allow mode control 4
# ntp allow mode private
# ntp authenticate
# ntp broadcastdelay 22
# ntp clock-period 5
# ntp logging
# ntp master 4
# ntp max-associations 34
# ntp maxdistance 3
# ntp mindistance 10
# ntp orphan 4
# ntp panic update
# ntp source GigabitEthernet0/1
# ntp update-calendar
# ntp access-group ipv4 peer DHCP-Server kod
# ntp access-group ipv6 peer preauth_ipv6_acl kod
# ntp access-group peer 2 kod
# ntp access-group query-only 10
# ntp authentication-key 2 md5 SomeSecurePassword 22
# ntp peer 172.16.1.10 version 2
# ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
# ntp peer ip checkPeerDomainIpv4.com prefer
# ntp peer ipv6 checkPeerDomainIpv6.com
# ntp peer ipv6 testPeerDomainIpv6.com prefer
# ntp server 172.16.1.12 version 2
# ntp server ipv6 checkServerDomainIpv6.com
# ntp server 172.16.1.13 source GigabitEthernet0/1
# ntp trusted-key 3 - 13
# ntp trusted-key 21

# Parsed play:
# ------------

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_ntp_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------

# "parsed": {
#     "access_group": {
#         "peer": [
#             {
#                 "access_list": "2",
#                 "kod": true
#             },
#             {
#                 "access_list": "DHCP-Server",
#                 "ipv4": true,
#                 "kod": true
#             },
#             {
#                 "access_list": "preauth_ipv6_acl",
#                 "ipv6": true,
#                 "kod": true
#             }
#         ],
#         "query_only": [
#             {
#                 "access_list": "10"
#             }
#         ]
#     },
#     "allow": {
#         "control": {
#             "rate_limit": 4
#         },
#         "private": true
#     },
#     "authenticate": true,
#     "authentication_keys": [
#         {
#             "algorithm": "md5",
#             "encryption": 22,
#             "id": 2,
#             "key": "SomeSecurePassword"
#         }
#     ],
#     "broadcast_delay": 22,
#     "clock_period": 5,
#     "logging": true,
#     "master": {
#         "stratum": 4
#     },
#     "max_associations": 34,
#     "max_distance": 3,
#     "min_distance": 10,
#     "orphan": 4,
#     "panic_update": true,
#     "peers": [
#         {
#             "peer": "172.16.1.10",
#             "version": 2
#         },
#         {
#             "peer": "checkPeerDomainIpv6.com",
#             "use_ipv6": true
#         }
#     ],
#     "servers": [
#         {
#             "server": "172.16.1.12",
#             "version": 2
#         },
#         {
#             "server": "172.16.1.13",
#             "source": "GigabitEthernet0/1"
#         },
#         {
#             "server": "checkServerDomainIpv6.com",
#             "use_ipv6": true
#         }
#     ],
#     "source": "GigabitEthernet0/1",
#     "trusted_keys": [
#         {
#             "range_start": 21
#         },
#         {
#             "range_end": 13,
#             "range_start": 3
#         }
#     ],
#     "update_calendar": true
# }
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.snmp_server.snmp_server import (
    Snmp_serverArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.snmp_server.snmp_server import (
    Snmp_server,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Snmp_serverArgs.argument_spec,
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

    result = Snmp_server(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
