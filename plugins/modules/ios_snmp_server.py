#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_snmp_server
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
author:
  - Sagar Paul (@KB-perByte)
description:
  - This module provides declarative management of SNMP server on Cisco IOS devices.
module: ios_snmp_server
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
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
              - "1"
              - 2c
              - "3"
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
          envmon:
            description: Allow envmon related traps
            suboptions:
              fan:
                description: Enable SNMP envmon fan traps
                suboptions:
                  shutdown:
                    description: Enable SNMP environmental monitor shutdown traps
                    type: bool
                  enable:
                    description: Enable/disable fan traps
                    type: bool
                  status:
                    description: Enable SNMP environmental status change traps
                    type: bool
                  supply:
                    description: Enable SNMP environmental monitor supply traps
                    type: bool
                  temperature:
                    description: Enable SNMP environmental monitor temperature traps
                    type: bool
                type: dict
              shutdown:
                description: Enable SNMP environmental monitor shutdown traps
                type: bool
              status:
                description: Enable SNMP environmental status change traps
                type: bool
              supply:
                description: Enable SNMP environmental monitor supply traps
                type: bool
              temperature:
                description: Enable SNMP environmental monitor temperature traps
                type: bool
            type: dict
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
          authentication:
            description:
              - Authentication parameters for the user.
              - Effects idempotency of module as configuration applied is not reflected
                in running-config.
            type: dict
            suboptions:
              algorithm:
                description: Select algorithm for authentication.
                type: str
                choices: ["md5", "sha"]
              password:
                description:
                  - Authentication password for user.
                type: str
          encryption:
            description:
              - Encryption parameters for the user.
              - Effects idempotency of module as configuration applied is not reflected
                in running-config.
            type: dict
            suboptions:
              priv:
                description: Select algorithm for encryption.
                type: str
                choices: ["3des", "aes", "des"]
              priv_option:
                description: Add extra option for specific priv if any.
                type: str
              password:
                description:
                  - Authentication password for user.
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
              - encrypted
            description: Enable encrypted version option.
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
short_description: Resource module to configure snmp server.
version_added: 2.6.0
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section ^snmp-server
# --------------------- EMPTY -----------------

# Merged play:
# ------------

- name: Apply the provided configuration
  cisco.ios.ios_snmp_server:
    config:
      communities:
        - acl_v4: testACL
          name: mergedComm
          rw: true
      contact: contact updated using merged
      engine_id:
        - id: AB0C5342FF0F
          remote:
            host: 172.16.0.12
            udp_port: 25
      groups:
        - group: mergedGroup
          version: v3
          version_option: auth
      file_transfer:
        access_group: test
        protocol:
          - ftp
      hosts:
        - community_string: mergedComm
          host: 172.16.2.9
          informs: true
          traps:
            - msdp
            - stun
            - pki
          version: 2c
        - community_string: mergedComm
          host: 172.16.2.9
          traps:
            - slb
            - pki
      password_policy:
        - change: 3
          digits: 23
          lower_case: 12
          max_len: 24
          policy_name: MergedPolicy
          special_char: 32
          upper_case: 12
        - change: 43
          min_len: 12
          policy_name: MergedPolicy2
          special_char: 22
          upper_case: 12
        - change: 11
          digits: 23
          max_len: 12
          min_len: 12
          policy_name: policy3
          special_char: 22
          upper_case: 12
      traps:
        cef:
          enable: true
          inconsistency: true
          peer_fib_state_change: true
          peer_state_change: true
          resource_failure: true
        msdp: true
        ospf:
          cisco_specific:
            error: true
            lsa: true
            retransmit: true
            state_change:
              nssa_trans_change: true
              shamlink:
                interface: true
                neighbor: true
          error: true
          lsa: true
          retransmit: true
          state_change: true
        syslog: true
        tty: true
      users:
        - acl_v4: "24"
          group: dev
          username: userPaul
          version: v1
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#         "snmp-server contact contact updated using merged",
#         "snmp-server file-transfer access-group test protocol ftp",
#         "snmp-server enable traps msdp",
#         "snmp-server enable traps syslog",
#         "snmp-server enable traps tty",
#         "snmp-server enable traps ospf cisco-specific errors",
#         "snmp-server enable traps ospf cisco-specific retransmit",
#         "snmp-server enable traps ospf cisco-specific lsa",
#         "snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
#         "snmp-server enable traps ospf cisco-specific state-change shamlink interface",
#         "snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
#         "snmp-server enable traps ospf errors",
#         "snmp-server enable traps ospf retransmit",
#         "snmp-server enable traps ospf lsa",
#         "snmp-server enable traps ospf state-change",
#         "snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
#         "snmp-server host 172.16.2.9 informs version 2c mergedComm msdp stun pki",
#         "snmp-server host 172.16.2.9 mergedComm slb pki",
#         "snmp-server group mergedGroup v3 auth",
#         "snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F",
#         "snmp-server community mergedComm rw testACL",
#         "snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
#         "snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43",
#         "snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
#         "snmp-server user userPaul dev v1 access 24"
# ],

# After state:
# ------------

# router-ios#show running-config | section ^snmp-server
# snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F
# snmp-server user userPaul dev v1 access 24
# snmp-server group mergedGroup v3 auth
# snmp-server community mergedComm RW testACL
# snmp-server contact contact updated using merged
# snmp-server enable traps tty
# snmp-server enable traps ospf state-change
# snmp-server enable traps ospf errors
# snmp-server enable traps ospf retransmit
# snmp-server enable traps ospf lsa
# snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
# snmp-server enable traps ospf cisco-specific state-change shamlink interface
# snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
# snmp-server enable traps ospf cisco-specific errors
# snmp-server enable traps ospf cisco-specific retransmit
# snmp-server enable traps ospf cisco-specific lsa
# snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
# snmp-server enable traps msdp
# snmp-server enable traps syslog
# snmp-server host 172.16.2.9 informs version 2c mergedComm  msdp stun pki
# snmp-server host 172.16.2.9 mergedComm  slb pki
# snmp-server file-transfer access-group test protocol ftp
# snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
# snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43
# snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11

# Using state: deleted

# Before state:
# -------------

# router-ios#show running-config | section ^snmp-server
# snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F
# snmp-server user userPaul dev v1 access 24
# snmp-server group mergedGroup v3 auth
# snmp-server community mergedComm RW testACL
# snmp-server contact contact updated using merged
# snmp-server enable traps tty
# snmp-server enable traps ospf state-change
# snmp-server enable traps ospf errors
# snmp-server enable traps ospf retransmit
# snmp-server enable traps ospf lsa
# snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
# snmp-server enable traps ospf cisco-specific state-change shamlink interface
# snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
# snmp-server enable traps ospf cisco-specific errors
# snmp-server enable traps ospf cisco-specific retransmit
# snmp-server enable traps ospf cisco-specific lsa
# snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
# snmp-server enable traps msdp
# snmp-server enable traps syslog
# snmp-server host 172.16.2.9 informs version 2c mergedComm  msdp stun pki
# snmp-server host 172.16.2.9 mergedComm  slb pki
# snmp-server file-transfer access-group test protocol ftp
# snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
# snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43
# snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11

# Deleted play:
# -------------

- name: Remove all existing configuration
  cisco.ios.ios_snmp_server:
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#     "no snmp-server contact contact updated using merged",
#     "no snmp-server file-transfer access-group test protocol ftp",
#     "no snmp-server enable traps msdp",
#     "no snmp-server enable traps syslog",
#     "no snmp-server enable traps tty",
#     "no snmp-server enable traps ospf cisco-specific errors",
#     "no snmp-server enable traps ospf cisco-specific retransmit",
#     "no snmp-server enable traps ospf cisco-specific lsa",
#     "no snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
#     "no snmp-server enable traps ospf cisco-specific state-change shamlink interface",
#     "no snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
#     "no snmp-server enable traps ospf errors",
#     "no snmp-server enable traps ospf retransmit",
#     "no snmp-server enable traps ospf lsa",
#     "no snmp-server enable traps ospf state-change",
#     "no snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
#     "no snmp-server host 172.16.2.9 informs version 2c mergedComm msdp stun pki",
#     "no snmp-server host 172.16.2.9 mergedComm slb pki",
#     "no snmp-server group mergedGroup v3 auth",
#     "no snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F",
#     "no snmp-server community mergedComm rw testACL",
#     "no snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
#     "no snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43",
#     "no snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
#     "no snmp-server user userPaul dev v1 access 24"
# ],

# After state:
# ------------

# router-ios#show running-config | section ^snmp-server
# --------------------- EMPTY -----------------

# Using state: overridden

# Before state:
# -------------

# router-ios#show running-config | section ^snmp-server
# snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F
# snmp-server user userPaul dev v1 access 24
# snmp-server group mergedGroup v3 auth
# snmp-server community mergedComm RW testACL
# snmp-server contact contact updated using merged
# snmp-server enable traps tty
# snmp-server enable traps ospf state-change
# snmp-server enable traps ospf errors
# snmp-server enable traps ospf retransmit
# snmp-server enable traps ospf lsa
# snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
# snmp-server enable traps ospf cisco-specific state-change shamlink interface
# snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
# snmp-server enable traps ospf cisco-specific errors
# snmp-server enable traps ospf cisco-specific retransmit
# snmp-server enable traps ospf cisco-specific lsa
# snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
# snmp-server enable traps msdp
# snmp-server enable traps syslog
# snmp-server host 172.16.2.9 informs version 2c mergedComm  msdp stun pki
# snmp-server host 172.16.2.9 mergedComm  slb pki
# snmp-server file-transfer access-group test protocol ftp
# snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
# snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43
# snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11

# Overridden play:
# ----------------

- name: Override commands with provided configuration
  cisco.ios.ios_snmp_server:
    config:
      location: "location entry for snmp"
      packet_size: 500
      communities:
        - acl_v4: acl_uq
          name: communityOverriden
          rw: true
    state: overridden

# Commands Fired:
# ---------------
# "commands": [
#       "no snmp-server contact contact updated using merged",
#       "no snmp-server file-transfer access-group test protocol ftp",
#       "snmp-server location location entry for snmp",
#       "snmp-server packetsize 500",
#       "no snmp-server enable traps msdp",
#       "no snmp-server enable traps syslog",
#       "no snmp-server enable traps tty",
#       "no snmp-server enable traps ospf cisco-specific errors",
#       "no snmp-server enable traps ospf cisco-specific retransmit",
#       "no snmp-server enable traps ospf cisco-specific lsa",
#       "no snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
#       "no snmp-server enable traps ospf cisco-specific state-change shamlink interface",
#       "no snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
#       "no snmp-server enable traps ospf errors",
#       "no snmp-server enable traps ospf retransmit",
#       "no snmp-server enable traps ospf lsa",
#       "no snmp-server enable traps ospf state-change",
#       "no snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
#       "no snmp-server host 172.16.2.9 informs version 2c mergedComm msdp stun pki",
#       "no snmp-server host 172.16.2.9 mergedComm slb pki",
#       "no snmp-server group mergedGroup v3 auth",
#       "no snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F",
#       "snmp-server community communityOvverriden rw acl_uq",
#       "no snmp-server community mergedComm rw testACL",
#       "no snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
#       "no snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43",
#       "no snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
#       "no snmp-server user userPaul dev v1 access 24"
#     ],

# After state:
# ------------

# router-ios#show running-config | section ^snmp-server
# snmp-server community communityOverriden RW acl_uq
# snmp-server packetsize 500
# snmp-server location location entry for snmp

# Using state: replaced

# Before state:
# -------------

# router-ios#show running-config | section ^snmp-server
# snmp-server community communityOverriden RW acl_uq
# snmp-server packetsize 500
# snmp-server location location entry for snmp

# Replaced play:
# --------------

- name: Replace commands with provided configuration
  cisco.ios.ios_snmp_server:
    config:
      location: "updated location entry"
      packet_size: 500
      communities:
        - acl_v4: acl_uq
          name: communityOverriden
          rw: true
    state: replaced

# Commands Fired:
# ---------------

# "commands": [
#     "snmp-server location updated location entry"
#     ],

# After state:
# ------------

# router-ios#show running-config | section ^snmp-server
# snmp-server community communityOverriden RW acl_uq
# snmp-server packetsize 500
# snmp-server location updated location entry

# Using state: gathered

# Before state:
# -------------

#router-ios#show running-config | section ^snmp-server
# snmp-server engineID remote 172.16.0.12 udp-port 25 AB0C5342FF0F
# snmp-server user userPaul dev v1 access 24
# snmp-server group mergedGroup v3 auth
# snmp-server community communityOvverriden RW acl_uq
# snmp-server community mergedComm RW testACL
# snmp-server packetsize 500
# snmp-server location updated location entry
# snmp-server contact contact updated using merged
# snmp-server enable traps tty
# snmp-server enable traps ospf state-change
# snmp-server enable traps ospf errors
# snmp-server enable traps ospf retransmit
# snmp-server enable traps ospf lsa
# snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
# snmp-server enable traps ospf cisco-specific state-change shamlink interface
# snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
# snmp-server enable traps ospf cisco-specific errors
# snmp-server enable traps ospf cisco-specific retransmit
# snmp-server enable traps ospf cisco-specific lsa
# snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
# snmp-server enable traps msdp
# snmp-server enable traps syslog
# snmp-server host 172.16.2.9 informs version 2c mergedComm  msdp stun pki
# snmp-server host 172.16.2.9 mergedComm  slb pki
# snmp-server file-transfer access-group test protocol ftp
# snmp-server password-policy MergedPolicy define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
# snmp-server password-policy MergedPolicy2 define min-len 12 upper-case 12 special-char 22 change 43
# snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11

# Gathered play:
# --------------

- name: Gather listed snmp config
  cisco.ios.ios_snmp_server:
    state: gathered

# Module Execution Result:
# ------------------------

#   "gathered": {
#         "communities": [
#             {
#                 "acl_v4": "acl_uq",
#                 "name": "communityOvverriden",
#                 "rw": true
#             },
#             {
#                 "acl_v4": "testACL",
#                 "name": "mergedComm",
#                 "rw": true
#             }
#         ],
#         "contact": "contact updated using merged",
#         "engine_id": [
#             {
#                 "id": "AB0C5342FF0F",
#                 "remote": {
#                     "host": "172.16.0.12",
#                     "udp_port": 25
#                 }
#             }
#         ],
#         "file_transfer": {
#             "access_group": "test",
#             "protocol": [
#                 "ftp"
#             ]
#         },
#         "groups": [
#             {
#                 "group": "mergedGroup",
#                 "version": "v3",
#                 "version_option": "auth"
#             }
#         ],
#         "hosts": [
#             {
#                 "community_string": "mergedComm",
#                 "host": "172.16.2.9",
#                 "informs": true,
#                 "traps": [
#                     "msdp",
#                     "stun",
#                     "pki"
#                 ],
#                 "version": "2c"
#             },
#             {
#                 "community_string": "mergedComm",
#                 "host": "172.16.2.9",
#                 "traps": [
#                     "slb",
#                     "pki"
#                 ]
#             }
#         ],
#         "location": "updated location entry",
#         "packet_size": 500,
#         "password_policy": [
#             {
#                 "change": 3,
#                 "digits": 23,
#                 "lower_case": 12,
#                 "max_len": 24,
#                 "policy_name": "MergedPolicy",
#                 "special_char": 32,
#                 "upper_case": 12
#             },
#             {
#                 "change": 43,
#                 "min_len": 12,
#                 "policy_name": "MergedPolicy2",
#                 "special_char": 22,
#                 "upper_case": 12
#             },
#             {
#                 "change": 11,
#                 "digits": 23,
#                 "max_len": 12,
#                 "min_len": 12,
#                 "policy_name": "policy3",
#                 "special_char": 22,
#                 "upper_case": 12
#             }
#         ],
#         "traps": {
#             "cef": {
#                 "enable": true,
#                 "inconsistency": true,
#                 "peer_fib_state_change": true,
#                 "peer_state_change": true,
#                 "resource_failure": true
#             },
#             "msdp": true,
#             "ospf": {
#                 "cisco_specific": {
#                     "error": true,
#                     "lsa": true,
#                     "retransmit": true,
#                     "state_change": {
#                         "nssa_trans_change": true,
#                         "shamlink": {
#                             "interface": true,
#                             "neighbor": true
#                         }
#                     }
#                 },
#                 "error": true,
#                 "lsa": true,
#                 "retransmit": true,
#                 "state_change": true
#             },
#             "syslog": true,
#             "tty": true
#         },
#         "users": [
#             {
#                 "acl_v4": "24",
#                 "group": "dev",
#                 "username": "userPaul",
#                 "version": "v1"
#             }
#         ]
#     },

# Using state: rendered

# Rendered play:
# --------------

- name: Render the commands for provided configuration
  cisco.ios.ios_snmp_server:
    config:
      accounting:
        command: default
      cache: 2
      chassis_id: entry for chassis id
      communities:
        - acl_v6: te
          name: test
          ro: true
          view: terst1
        - acl_v4: "1322"
          name: wete
          ro: true
        - acl_v4: paul
          name: weteww
          rw: true
      contact: details contact
      context:
        - contextA
        - contextB
      engine_id:
        - id: AB0C5342FA0A
          local: true
        - id: AB0C5342FAAB
          remote:
            host: 172.16.0.2
            udp_port: 23
        - id: AB0C5342FAAA
          remote:
            host: 172.16.0.1
            udp_port: 22
      file_transfer:
        access_group: testAcl
        protocol:
          - ftp
          - rcp
      groups:
        - group: grpFamily
          version: v3
          version_option: auth
        - context: mycontext
          group: grpFamily
          version: v1
        - acl_v4: "2"
          group: grp1
          notify: me
          version: v1
        - group: newtera
          version: v3
          version_option: priv
        - group: relaplacing
          version: v3
          version_option: noauth
      hosts:
        - community_string: check
          host: 172.16.2.99
          informs: true
          traps:
            - msdp
            - stun
          version: 2c
        - community_string: check
          host: 172.16.2.99
          traps:
            - slb
            - pki
        - community_string: checktrap
          host: 172.16.2.99
          traps:
            - isis
            - hsrp
        - community_string: newtera
          host: 172.16.2.1
          traps:
            - rsrb
            - pim
            - rsvp
            - slb
            - pki
          version: "3"
          version_option: priv
        - community_string: relaplacing
          host: 172.16.2.1
          traps:
            - slb
            - pki
          version: "3"
          version_option: noauth
        - community_string: trapsac
          host: 172.16.2.1
          traps:
            - tty
            - bgp
          version: 2c
        - community_string: www
          host: 172.16.1.1
          traps:
            - tty
            - bgp
          version: "3"
          version_option: auth
      inform:
        pending: 2
      ip:
        dscp: 2
      location: "entry for snmp location"
      packet_size: 500
      password_policy:
        - change: 3
          digits: 23
          lower_case: 12
          max_len: 24
          policy_name: policy1
          special_char: 32
          upper_case: 12
        - change: 9
          min_len: 12
          policy_name: policy2
          special_char: 22
          upper_case: 12
        - change: 11
          digits: 23
          max_len: 12
          min_len: 12
          policy_name: policy3
          special_char: 22
          upper_case: 12
      queue_length: 2
      source_interface: Loopback999
      system_shutdown: true
      trap_source: GigabitEthernet0/0
      trap_timeout: 2
      traps:
        auth_framework:
          enable: true
        bgp:
          cbgp2: true
          enable: true
        bfd:
          enable: true
          session_down: true
          session_up: true
        bridge:
          enable: true
          newroot: true
          topologychange: true
        casa: true
        cef:
          enable: true
          inconsistency: true
          peer_fib_state_change: true
          peer_state_change: true
          resource_failure: true
        dlsw:
          enable: true
        eigrp: true
        ethernet:
          cfm:
            alarm: true
          evc:
            status: true
        event_manager: true
        flowmon: true
        frame_relay:
          enable: true
          subif:
            enable: true
        hsrp: true
        ike:
          policy:
            add: true
            delete: true
          tunnel:
            start: true
            stop: true
        ipmulticast: true
        ipsec:
          cryptomap:
            add: true
            attach: true
            delete: true
            detach: true
          too_many_sas: true
          tunnel:
            start: true
            stop: true
        ipsla: true
        l2tun:
          pseudowire_status: true
          session: true
        msdp: true
        ospf:
          cisco_specific:
            error: true
            lsa: true
            retransmit: true
            state_change:
              nssa_trans_change: true
              shamlink:
                interface: true
                neighbor: true
          error: true
          lsa: true
          retransmit: true
          state_change: true
        pim:
          enable: true
          invalid_pim_message: true
          neighbor_change: true
          rp_mapping_change: true
        pki: true
        rsvp: true
        snmp:
          authentication: true
          coldstart: true
          linkdown: true
          linkup: true
          warmstart: true
        syslog: true
        tty: true
      users:
        - acl_v4: "24"
          group: groupFamily
          username: paul
          version: v1
        - acl_v4: ipv6
          group: groupFamily
          username: domnic
          version: v3
        - group: relaplacing
          username: relaplacing
          version: v3
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#     "snmp-server accounting commands default",
#     "snmp-server cache interval 2",
#     "snmp-server chassis-id entry for chassis id",
#     "snmp-server contact details contact",
#     "snmp-server file-transfer access-group testAcl protocol ftp rcp",
#     "snmp-server inform pending 2",
#     "snmp-server ip dscp 2",
#     "snmp-server location entry for snmp location",
#     "snmp-server packetsize 500",
#     "snmp-server queue-length 2",
#     "snmp-server trap timeout 2",
#     "snmp-server source-interface informs Loopback999",
#     "snmp-server trap-source GigabitEthernet0/0",
#     "snmp-server system-shutdown",
#     "snmp-server enable traps auth-framework",
#     "snmp-server enable traps bfd session-down session-up",
#     "snmp-server enable traps bgp cbgp2",
#     "snmp-server enable traps bridge newroot topologychange",
#     "snmp-server enable traps casa",
#     "snmp-server enable traps eigrp",
#     "snmp-server enable traps event-manager",
#     "snmp-server enable traps flowmon",
#     "snmp-server enable traps hsrp",
#     "snmp-server enable traps ipsla",
#     "snmp-server enable traps msdp",
#     "snmp-server enable traps pki",
#     "snmp-server enable traps rsvp",
#     "snmp-server enable traps syslog",
#     "snmp-server enable traps tty",
#     "snmp-server enable traps ipmulticast",
#     "snmp-server enable traps ike policy add",
#     "snmp-server enable traps ike policy delete",
#     "snmp-server enable traps ike tunnel start",
#     "snmp-server enable traps ike tunnel stop",
#     "snmp-server enable traps ipsec cryptomap add",
#     "snmp-server enable traps ipsec cryptomap delete",
#     "snmp-server enable traps ipsec cryptomap attach",
#     "snmp-server enable traps ipsec cryptomap detach",
#     "snmp-server enable traps ipsec tunnel start",
#     "snmp-server enable traps ipsec tunnel stop",
#     "snmp-server enable traps ipsec too-many-sas",
#     "snmp-server enable traps ospf cisco-specific errors",
#     "snmp-server enable traps ospf cisco-specific retransmit",
#     "snmp-server enable traps ospf cisco-specific lsa",
#     "snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
#     "snmp-server enable traps ospf cisco-specific state-change shamlink interface",
#     "snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
#     "snmp-server enable traps ospf errors",
#     "snmp-server enable traps ospf retransmit",
#     "snmp-server enable traps ospf lsa",
#     "snmp-server enable traps ospf state-change",
#     "snmp-server enable traps l2tun pseudowire status",
#     "snmp-server enable traps l2tun session",
#     "snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message",
#     "snmp-server enable traps snmp authentication linkdown linkup warmstart coldstart",
#     "snmp-server enable traps frame-relay",
#     "snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
#     "snmp-server enable traps dlsw",
#     "snmp-server enable traps ethernet evc status",
#     "snmp-server enable traps ethernet cfm alarm",
#     "snmp-server host 172.16.2.99 informs version 2c check msdp stun",
#     "snmp-server host 172.16.2.99 check slb pki",
#     "snmp-server host 172.16.2.99 checktrap isis hsrp",
#     "snmp-server host 172.16.2.1 version 3 priv newtera rsrb pim rsvp slb pki",
#     "snmp-server host 172.16.2.1 version 3 noauth relaplacing slb pki",
#     "snmp-server host 172.16.2.1 version 2c trapsac tty bgp",
#     "snmp-server host 172.16.1.1 version 3 auth www tty bgp",
#     "snmp-server group grpFamily v1 context mycontext",
#     "snmp-server group grp1 v1 notify me access 2",
#     "snmp-server group newtera v3 priv",
#     "snmp-server group relaplacing v3 noauth",
#     "snmp-server engineID local AB0C5342FA0A",
#     "snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB",
#     "snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA",
#     "snmp-server community test view terst1 ro ipv6 te",
#     "snmp-server community wete ro 1322",
#     "snmp-server community weteww rw paul",
#     "snmp-server context contextA",
#     "snmp-server context contextB",
#     "snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
#     "snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9",
#     "snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
#     "snmp-server user paul groupFamily v1 access 24",
#     "snmp-server user domnic groupFamily v3 access ipv6",
#     "snmp-server user relaplacing relaplacing v3"
# ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# snmp-server engineID local AB0C5342FA0A
# snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
# snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA
# snmp-server user newuser newfamily v1 access 24
# snmp-server user paul familypaul v3 access ipv6 ipv6acl
# snmp-server user replaceUser replaceUser v3
# snmp-server group group0 v3 auth
# snmp-server group group1 v1 notify me access 2
# snmp-server group group2 v3 priv
# snmp-server group replaceUser v3 noauth
# snmp-server community commu1 view view1 RO ipv6 te
# snmp-server community commu2 RO 1322
# snmp-server community commu3 RW paul
# snmp-server trap timeout 2
# snmp-server trap-source GigabitEthernet0/0
# snmp-server source-interface informs Loopback999
# snmp-server packetsize 500
# snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down
# snmp-server host 172.16.2.99 informs version 2c check  msdp stun
# snmp-server host 172.16.2.1 version 2c trapsac  tty bgp
# snmp-server host 172.16.1.1 version 3 auth group0  tty bgp
# snmp-server context contextWord1
# snmp-server context contextWord2
# snmp-server file-transfer access-group testAcl protocol ftp
# snmp-server file-transfer access-group testAcl protocol rcp
# snmp-server cache interval 2
# snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9
# snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11
# snmp-server accounting commands default
# snmp-server inform pending 2

# Parsed play:
# ------------

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_snmp_server:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
#  "parsed": {
#     "accounting": {
#         "command": "default"
#     },
#     "cache": 2,
#     "communities": [
#         {
#             "acl_v6": "te",
#             "name": "commu1",
#             "ro": true,
#             "view": "view1"
#         },
#         {
#             "acl_v4": "1322",
#             "name": "commu2",
#             "ro": true
#         },
#         {
#             "acl_v4": "paul",
#             "name": "commu3",
#             "rw": true
#         }
#     ],
#     "context": [
#         "contextWord1",
#         "contextWord2"
#     ],
#     "engine_id": [
#         {
#             "id": "AB0C5342FA0A",
#             "local": true
#         },
#         {
#             "id": "AB0C5342FAAA",
#             "remote": {
#                 "host": "172.16.0.1",
#                 "udp_port": 22
#             }
#         },
#         {
#             "id": "AB0C5342FAAB",
#             "remote": {
#                 "host": "172.16.0.2",
#                 "udp_port": 23
#             }
#         }
#     ],
#     "file_transfer": {
#         "access_group": "testAcl",
#         "protocol": [
#             "rcp",
#             "ftp"
#         ]
#     },
#     "groups": [
#         {
#             "group": "group0",
#             "version": "v3",
#             "version_option": "auth"
#         },
#         {
#             "acl_v4": "2",
#             "group": "group1",
#             "notify": "me",
#             "version": "v1"
#         },
#         {
#             "group": "group2",
#             "version": "v3",
#             "version_option": "priv"
#         },
#         {
#             "group": "replaceUser",
#             "version": "v3",
#             "version_option": "noauth"
#         }
#     ],
#     "hosts": [
#         {
#             "community_string": "group0",
#             "host": "172.16.1.1",
#             "traps": [
#                 "tty",
#                 "bgp"
#             ],
#             "version": "3",
#             "version_option": "auth"
#         },
#         {
#             "community_string": "trapsac",
#             "host": "172.16.2.1",
#             "traps": [
#                 "tty",
#                 "bgp"
#             ],
#             "version": "2c"
#         },
#         {
#             "community_string": "check",
#             "host": "172.16.2.99",
#             "informs": true,
#             "traps": [
#                 "msdp",
#                 "stun"
#             ],
#             "version": "2c"
#         }
#     ],
#     "inform": {
#         "pending": 2
#     },
#     "packet_size": 500,
#     "password_policy": [
#         {
#             "change": 9,
#             "min_len": 12,
#             "policy_name": "policy2",
#             "special_char": 22,
#             "upper_case": 12
#         },
#         {
#             "change": 11,
#             "digits": 23,
#             "max_len": 12,
#             "min_len": 12,
#             "policy_name": "policy3",
#             "special_char": 22,
#             "upper_case": 12
#         }
#     ],
#     "source_interface": "Loopback999",
#     "trap_source": "GigabitEthernet0/0",
#     "trap_timeout": 2,
#     "traps": {
#         "vrfmib": {
#             "vnet_trunk_down": true,
#             "vnet_trunk_up": true,
#             "vrf_down": true,
#             "vrf_up": true
#         }
#     },
#     "users": [
#         {
#             "acl_v4": "24",
#             "group": "newfamily",
#             "username": "newuser",
#             "version": "v1"
#         },
#         {
#             "acl_v4": "ipv6",
#             "group": "familypaul",
#             "username": "paul",
#             "version": "v3"
#         },
#         {
#             "group": "replaceUser",
#             "username": "replaceUser",
#             "version": "v3"
#         }
#     ]
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
    - snmp-server host 172.16.2.99 informs version 2c check msdp stun
    - snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
    - snmp-server group grp1 v1 notify me access 2
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - snmp-server enable traps ipsec cryptomap attach
    - snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
    - snmp-server cache interval 2
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
