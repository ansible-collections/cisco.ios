#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_hsrp_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_hsrp_interfaces
short_description: Resource module to configure HSRP on interfaces.
description:
  - >-
    This module provides declarative management of HSRP configuration on
    interface for Cisco IOS devices.
version_added: 10.1.0
author:
  - Sagar Paul (@KB-perByte)
  - Nikhil Bhasin (@nickbhasin)
notes:
  - Tested against Cisco IOSXE Version 17.16.
  - >-
    This module works with connection C(network_cli). See
    U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - >-
    The module examples uses callback plugin (callback_result_format=yaml) to
    generate task output in yaml format.
  - >-
    For idempotency, the module consieders that version defaults to 1 as it is implied
    by the applaince and not available in the running-config.
    Priority defaults to 100 if not specified in the configuration.
options:
  config:
    description: A list of HSP configuration options to add to interface
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - >-
            Full name of the interface excluding any logical unit number, i.e.
            GigabitEthernet0/1.
        type: str
        required: true
      bfd:
        description: Enable HSRP BFD
        type: bool
      delay:
        description: HSRP initialization delay
        type: dict
        suboptions:
          minimum:
            description: Delay at least this long
            type: int
          reload:
            description: Delay after reload
            type: int
      redirect:
        description: Redirect configuration
        type: dict
        suboptions:
          advertisement:
            description: >-
              Redirect advertisement messages (standby redirect advertisement
              authentication md5)
            type: dict
            suboptions:
              authentication:
                description: Authentication configuration
                type: dict
                suboptions:
                  key_chain:
                    description: Set key chain
                    type: str
                  key_string:
                    description: Set key string
                    type: str
                  encryption:
                    description: Set encryption 0 (unencrypted/default) or 7 (hidden)
                    type: str
                  time_out:
                    description: Set timeout
                    type: int
                  password_text:
                    description: Password text valid for plain text and and key-string
                    type: str
          timers:
            description: Adjust redirect timers
            type: dict
            suboptions:
              adv_timer:
                description: Passive router advertisement interval in seconds
                type: int
              holddown_timer:
                description: Passive router holddown interval in seconds
                type: int
      mac_refresh:
        description: >-
          Refresh MAC cache on switch by periodically sending packet from
          virtual mac address
        type: int
      use_bia:
        description: >-
          HSRP uses interface's burned in address (does not work with mac
          address)
        type: dict
        suboptions:
          scope:
            description: >-
              Use-bia applies to all groups on this interface or
              sub-interface
            type: bool
          set:
            description: Set use-bia
            type: bool
      version:
        description: HSRP version
        type: int
        choices:
          - 1
          - 2
      standby_options:
        description: Group number and group options for standby (HSRP)
        type: list
        elements: dict
        aliases:
          - standby_groups
        suboptions:
          group_no:
            description: Group number
            type: int
          follow:
            description: Enable HSRP BFD
            type: str
          ip:
            description: Enable HSRP IPv4 and set the virtual IP address
            type: list
            elements: dict
            suboptions:
              virtual_ip:
                description: Virtual IP address
                type: str
              secondary:
                description: Make this IP address a secondary virtual IP address
                type: bool
          ipv6:
            description: Enable HSRP IPv6 and set the IP address
            type: dict
            suboptions:
              autoconfig:
                description: Obtain address using autoconfiguration
                type: bool
              addresses:
                description: IPv6 link-local address or IPv6 prefix
                type: list
                elements: str
          mac_address:
            description: Virtual MAC address
            type: str
          group_name:
            description: Redundancy name string
            type: str
          authentication:
            description: Authentication configuration
            type: dict
            suboptions:
              key_chain:
                description: Set key chain
                type: str
              key_string:
                description: Set key string
                type: str
              encryption:
                description: Set encryption 0 (unencrypted/default) or 7 (hidden)
                type: int
              time_out:
                description: Set timeout
                type: int
              password_text:
                description: Password text valid for plain text and and key-string
                type: str
          preempt:
            description: Overthrow lower priority Active routers
            type: dict
            suboptions:
              enabled:
                description: Enables preempt, drives the lone `standby <grp_no> preempt` command
                type: bool
              minimum:
                description: Delay at least this long
                type: int
              reload:
                description: Delay after reload
                type: int
              sync:
                description: Wait for IP redundancy clients
                type: int
              delay:
                description: Wait before preempting
                type: bool
          priority:
            description: Priority level
            type: int
            default: 100
          timers:
            description: Overthrow lower priority Active routers
            type: dict
            suboptions:
              hello_interval:
                description: Hello interval in seconds
                type: int
              hold_time:
                description: Hold time in seconds
                type: int
              msec:
                description: Specify hello interval in milliseconds
                type: dict
                suboptions:
                  hello_interval:
                    description: <15-999>  Hello interval in milliseconds
                    type: int
                  hold_time:
                    description: <60-3000>  Hold time in milliseconds
                    type: int
          track:
            description: Priority tracking
            type: list
            elements: dict
            suboptions:
              track_no:
                description: Track object number
                type: int
              decrement:
                description: Priority decrement
                type: int
              shutdown:
                description: Shutdown Group
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - >-
        The value of this option should be the output received from the IOS
        device by executing the command B(show running-config | section
        ^interface).
      - >-
        The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - parsed
    default: merged
    description:
      - The state the configuration should be left in
      - >-
        The states I(rendered), I(gathered) and I(parsed) does not perform any
        change on the device.
      - >-
        The state I(rendered) will transform the configuration in C(config)
        option to platform specific CLI commands which will be returned in the
        I(rendered) key within the result. For state I(rendered) active
        connection to remote host is not required.
      - >-
        The state I(gathered) will fetch the running configuration from device
        and transform it into structured data in the format as per the resource
        module argspec and the value is returned in the I(gathered) key within
        the result.
      - >-
        The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into JSON format as per the resource module
        parameters and the value is returned in the I(parsed) key within the
        result. The value of C(running_config) option should be the same format
        as the output of command I(show running-config | section ^interface)
        executed on device. For state I(parsed) active connection to remote host
        is not required.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# Router#show running-config | section ^interface
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address


- name: Populate the device with HSRP interface configuration
  cisco.ios.hsrp_interfaces:
    state: merged
    config:
      - delay:
          minimum: 5555
          reload: 556
        mac_refresh: 45
        name: Vlan70
        redirect:
          advertisement:
            authentication:
              key_chain: HSRP_CHAIN
          timers:
            adv_timer: 10
            holddown_timer: 55
        standby_options:
          - authentication:
              encryption: 7
              key_string: 0123456789ABCDEF
            follow: MASTER_GROUP
            group_name: PRIMARY_GROUP
            group_no: 10
            ip:
              - secondary: true
                virtual_ip: 10.0.10.2
            preempt:
              delay: true
              enabled: true
              minimum: 100
              reload: 50
              sync: 30
            priority: 110
            timers:
              hold_time: 250
              msec:
                hello_interval: 200
            track:
              - decrement: 20
                track_no: 1
          - follow: MASTER_GROUP
            group_name: IPV6_GROUP
            group_no: 20
            ipv6:
              addresses:
                - '2001:db8:20::1/64'
              autoconfig: true
            mac_address: 0000.0000.0014
            priority: 120
        version: 2
      - delay:
          minimum: 100
          reload: 200
        name: Vlan100
        standby_options:
          - authentication:
              password_text: hello_secret
            group_name: BACKUP_GROUP
            group_no: 5
            ip:
              - virtual_ip: 192.168.1.1
            preempt:
              enabled: true
            priority: 150
            timers:
              hello_interval: 5
              hold_time: 15
            track:
              - decrement: 30
                track_no: 10
        version: 2
      - name: GigabitEthernet3
        standby_options:
          - group_no: 1
            ip:
              - virtual_ip: 172.16.1.1
            priority: 100
        version: 1
      - name: GigabitEthernet2
        standby_options:
          - authentication:
              key_chain: AUTH_CHAIN
            group_no: 2
            ip:
              - secondary: true
                virtual_ip: 172.16.2.1
            priority: 100
        version: 1


# Task Output
# -----------
#
# before:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
# -   name: GigabitEthernet3
# -   name: GigabitEthernet4
# -   name: Vlan70
# -   name: Vlan100
# commands:
# - interface Vlan70
# - standby version 2
# - standby delay minimum 5555 reload 556
# - standby mac-refresh 45
# - standby redirect timers 10 55
# - standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
# - standby 10 follow MASTER_GROUP
# - standby 10 name PRIMARY_GROUP
# - standby 10 preempt delay minimum 100 reload 50 sync 30
# - standby 10 priority 110
# - standby 10 authentication md5 key-string 7 0123456789ABCDEF
# - standby 10 ip 10.0.10.2 secondary
# - standby 10 track 1 decrement 20
# - standby 20 follow MASTER_GROUP
# - standby 20 mac-address 0000.0000.0014
# - standby 20 name IPV6_GROUP
# - standby 20 priority 120
# - standby 20 ipv6 autoconfig
# - standby 20 ipv6 2001:db8:20::1/64
# - interface Vlan100
# - standby version 2
# - standby delay minimum 100 reload 200
# - standby 5 name BACKUP_GROUP
# - standby 5 preempt
# - standby 5 priority 150
# - standby 5 authentication ********
# - standby 5 ip 192.168.1.1
# - standby 5 track 10 decrement 30
# - interface GigabitEthernet3
# - standby version 1
# - standby 1 priority 100
# - standby 1 ip 172.16.1.1
# - interface GigabitEthernet2
# - standby version 1
# - standby 2 priority 100
# - standby 2 authentication md5 key-chain AUTH_CHAIN
# - standby 2 ip 172.16.2.1 secondary
# after:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
#     standby_options:
#     -   authentication:
#             key_chain: AUTH_CHAIN
#         group_no: 2
#         ip:
#         -   secondary: true
#             virtual_ip: 172.16.2.1
#         priority: 100
# -   name: GigabitEthernet3
#     standby_options:
#     -   group_no: 1
#         ip:
#         -   virtual_ip: 172.16.1.1
#         priority: 100
# -   name: GigabitEthernet4
# -   delay:
#         minimum: 5555
#         reload: 556
#     mac_refresh: 45
#     name: Vlan70
#     redirect:
#         advertisement:
#             authentication:
#                 key_chain: HSRP_CHAIN
#         timers:
#             adv_timer: 10
#             holddown_timer: 55
#     standby_options:
#     -   authentication:
#             encryption: 7
#             key_string: 0123456789ABCDEF
#         follow: MASTER_GROUP
#         group_name: PRIMARY_GROUP
#         group_no: 10
#         ip:
#         -   secondary: true
#             virtual_ip: 10.0.10.2
#         preempt:
#             delay: true
#             enabled: true
#             minimum: 100
#             reload: 50
#             sync: 30
#         priority: 110
#         track:
#         -   decrement: 20
#             track_no: 1
#     -   follow: MASTER_GROUP
#         group_name: IPV6_GROUP
#         group_no: 20
#         ipv6:
#             addresses:
#             - 2001:DB8:20::1/64
#             autoconfig: true
#         mac_address: 0000.0000.0014
#         priority: 120
#     version: 2
# -   delay:
#         minimum: 100
#         reload: 200
#     name: Vlan100
#     standby_options:
#     -   group_name: BACKUP_GROUP
#         group_no: 5
#         ip:
#         -   virtual_ip: 192.168.1.1
#         preempt:
#             enabled: true
#         priority: 150
#         track:
#         -   decrement: 30
#             track_no: 10
#     version: 2

# After state:
# ------------
#
# Router#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# !
# interface GigabitEthernet2
#  no ip address
#  standby 2 ip 172.16.2.1 secondary
#  standby 2 authentication md5 key-chain AUTH_CHAIN
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet3
#  no ip address
#  standby 1 ip 172.16.1.1
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface Vlan70
#  description for test
#  no ip address
#  standby mac-refresh 45
#  standby redirect timers 10 55
#  standby delay minimum 5555 reload 556
#  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
#  standby version 2
#  standby 10 ip 10.0.10.2 secondary
#  standby 10 follow MASTER_GROUP
#  standby 10 priority 110
#  standby 10 preempt delay minimum 100 reload 50 sync 30
#  standby 10 authentication md5 key-string 7 0123456789ABCDEF
#  standby 10 name PRIMARY_GROUP
#  standby 10 track 1 decrement 20
#  standby 20 ipv6 autoconfig
#  standby 20 ipv6 2001:DB8:20::1/64
#  standby 20 follow MASTER_GROUP
#  standby 20 priority 120
#  standby 20 name IPV6_GROUP
#  standby 20 mac-address 0000.0000.0014
# !
# interface Vlan100
#  description for test
#  no ip address
#  standby delay minimum 100 reload 200
#  standby version 2
#  standby 5 ip 192.168.1.1
#  standby 5 priority 150
#  standby 5 preempt
#  standby 5 name BACKUP_GROUP
#  standby 5 track 10 decrement 30
# !


# Using replaced

# Before state:
# -------------
#
# Router#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  speed 1000
#  standby 22 ip 10.0.0.1 secondary
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  standby 0 priority 5
#  shutdown
#  negotiation auto

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_hsrp_interfaces:
    config:
      - name: GigabitEthernet3
        standby_groups:
          - group_no: 22
            ip:
              - virtual_ip: 10.0.0.1
                secondary: true
      - name: GigabitEthernet4
        standby_groups:
          - group_no: 0
            priority: 6
    state: replaced

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
#     standby_groups:
#       - group_no: 22
#         ip:
#           - virtual_ip: 192.168.0.2
#             secondary: True
# - name: GigabitEthernet4
#     standby_groups:
#       - group_no: 0
#         priority: 6
# - name: Loopback999
# - name: Loopback888
# commands:
# - interface GigabitEthernet3
# - standby 22 ip 10.0.0.1 secondary
# - interface GigabitEthernet4
# - standby 0 priority 5
# after:
#   name: GigabitEthernet1
#   name: GigabitEthernet2
#   name: GigabitEthernet3
#     standby_groups:
#       - group_no: 22
#         ip:
#           - virtual_ip: 192.168.0.2
#             secondary: True
# - name: GigabitEthernet4
#     standby_groups:
#       - group_no: 0
#         priority: 6
# - name: Loopback999
# - name: Loopback888

# After state:
# ------------
#
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  standby 22 ip 10.0.0.1 secondary
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  description Auto_Cable_Testing_Ansible
#  no ip address
#  standby 0 priority 6
#  shutdown
#  negotiation auto

# Using overridden

# Before state:
# -------------
#
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  standby 22 ip 10.0.0.1 secondary
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  description Auto_Cable_Testing_Ansible
#  no ip address
#  standby 0 priority 6
#  shutdown
#  negotiation auto

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_hsrp_interfaces:
    config:
      - name: GigabitEthernet4
        standby_groups:
          - group_no: 0
            priority: 10
    state: overridden

# Task Output
# -----------
# before:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
#     standby_groups:
#       - group_no: 22
#         ip:
#           - virtual_ip: 192.168.0.2
#             secondary: True
# - name: GigabitEthernet4
#     standby_groups:
#       - group_no: 0
#         priority: 6
# - name: Loopback999
# - name: Loopback888
# commands:
# - interface GigabitEthernet3
# - no standby 22 ip 10.0.0.1 secondary
# - interface GigabitEthernet4
# - no standby 0 priority 6
# - standby 0 priority 10
# after:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet4
#     standby_groups:
#       - group_no: 0
#         priority: 10
# - name: Loopback999
# - name: Loopback888

# After state:
# ------------
#
# router-ios#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  ip ospf network broadcast
#  ip ospf resync-timeout 10
#  ip ospf dead-interval 5
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  description Auto_Cable_Testing_Ansible
#  no ip address
#  standby 0 priority 10
#  shutdown
#  negotiation auto

# Using deleted

# Before state:
# -------------
#
# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# !
# interface GigabitEthernet2
#  no ip address
#  standby 2 ip 172.16.2.1 secondary
#  standby 2 authentication md5 key-chain AUTH_CHAIN
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet3
#  no ip address
#  standby 1 ip 172.16.1.1
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface Vlan70
#  description for test
#  no ip address
#  standby mac-refresh 45
#  standby redirect timers 10 55
#  standby delay minimum 5555 reload 556
#  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
#  standby version 2
#  standby 10 ip 10.0.10.2 secondary
#  standby 10 follow MASTER_GROUP
#  standby 10 priority 110
#  standby 10 preempt delay minimum 100 reload 50 sync 30
#  standby 10 authentication md5 key-string 7 0123456789ABCDEF
#  standby 10 name PRIMARY_GROUP
#  standby 10 track 1 decrement 20
#  standby 20 ipv6 autoconfig
#  standby 20 ipv6 2001:DB8:20::1/64
#  standby 20 follow MASTER_GROUP
#  standby 20 priority 120
#  standby 20 name IPV6_GROUP
#  standby 20 mac-address 0000.0000.0014
# !
# interface Vlan100
#  description for test
#  no ip address
#  standby delay minimum 100 reload 200
#  standby version 2
#  standby 5 ip 192.168.1.1
#  standby 5 priority 150
#  standby 5 preempt
#  standby 5 name BACKUP_GROUP
#  standby 5 track 10 decrement 30


- name: "Delete attributes of given interfaces (NOTE: This won't delete the interfaces)"
  cisco.ios.ios_hsrp_interfaces:
    state: deleted

# Task Output
# -----------
#
# before:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
#     standby_options:
#     -   authentication:
#             key_chain: AUTH_CHAIN
#         group_no: 2
#         ip:
#         -   secondary: true
#             virtual_ip: 172.16.2.1
#         priority: 100
# -   name: GigabitEthernet3
#     standby_options:
#     -   group_no: 1
#         ip:
#         -   virtual_ip: 172.16.1.1
#         priority: 100
# -   name: GigabitEthernet4
# -   delay:
#         minimum: 5555
#         reload: 556
#     mac_refresh: 45
#     name: Vlan70
#     redirect:
#         advertisement:
#             authentication:
#                 key_chain: HSRP_CHAIN
#         timers:
#             adv_timer: 10
#             holddown_timer: 55
#     standby_options:
#     -   authentication:
#             encryption: 7
#             key_string: 0123456789ABCDEF
#         follow: MASTER_GROUP
#         group_name: PRIMARY_GROUP
#         group_no: 10
#         ip:
#         -   secondary: true
#             virtual_ip: 10.0.10.2
#         preempt:
#             delay: true
#             enabled: true
#             minimum: 100
#             reload: 50
#             sync: 30
#         priority: 110
#         track:
#         -   decrement: 20
#             track_no: 1
#     -   follow: MASTER_GROUP
#         group_name: IPV6_GROUP
#         group_no: 20
#         ipv6:
#             addresses:
#             - 2001:DB8:20::1/64
#             autoconfig: true
#         mac_address: 0000.0000.0014
#         priority: 120
#     version: 2
# -   delay:
#         minimum: 100
#         reload: 200
#     name: Vlan100
#     standby_options:
#     -   group_name: BACKUP_GROUP
#         group_no: 5
#         ip:
#         -   virtual_ip: 192.168.1.1
#         preempt:
#             enabled: true
#         priority: 150
#         track:
#         -   decrement: 30
#             track_no: 10
#     version: 2
# commands:
# - interface GigabitEthernet2
# - no standby version 1
# - no standby 2
# - interface GigabitEthernet3
# - no standby version 1
# - no standby 1
# - interface Vlan70
# - no standby version 2
# - no standby delay minimum 5555 reload 556
# - no standby mac-refresh 45
# - no standby redirect timers 10 55
# - no standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
# - no standby 10
# - no standby 20
# - no standby version 2
# - interface Vlan100
# - no standby version 2
# - no standby delay minimum 100 reload 200
# - no standby 5
# - no standby version 2
# after:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
# -   name: GigabitEthernet3
# -   name: GigabitEthernet4
# -   name: Vlan70
# -   name: Vlan100

# After state:
# -------------
#
# router-ios#show running-config | section ^interface
# !
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# !
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet3
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface Vlan70
#  description for test
#  no ip address
# !
# interface Vlan100
#  description for test
#  no ip address
# !

# Using gathered

# Before state:
# -------------
# router-ios#show running-config | section ^interface
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# !
# interface GigabitEthernet2
#  no ip address
#  standby 2 ip 172.16.2.1 secondary
#  standby 2 authentication md5 key-chain AUTH_CHAIN
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet3
#  no ip address
#  standby 1 ip 172.16.1.1
#  shutdown
#  negotiation auto
# !
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# !
# interface Vlan70
#  description for test
#  no ip address
#  standby mac-refresh 45
#  standby redirect timers 10 55
#  standby delay minimum 5555 reload 556
#  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
#  standby version 2
#  standby 10 ip 10.0.10.2 secondary
#  standby 10 follow MASTER_GROUP
#  standby 10 priority 110
#  standby 10 preempt delay minimum 100 reload 50 sync 30
#  standby 10 authentication md5 key-string 7 0123456789ABCDEF
#  standby 10 name PRIMARY_GROUP
#  standby 10 track 1 decrement 20
#  standby 20 ipv6 autoconfig
#  standby 20 ipv6 2001:DB8:20::1/64
#  standby 20 follow MASTER_GROUP
#  standby 20 priority 120
#  standby 20 name IPV6_GROUP
#  standby 20 mac-address 0000.0000.0014
# !
# interface Vlan100
#  description for test
#  no ip address
#  standby delay minimum 100 reload 200
#  standby version 2
#  standby 5 ip 192.168.1.1
#  standby 5 priority 150
#  standby 5 preempt
#  standby 5 name BACKUP_GROUP
#  standby 5 track 10 decrement 30

- name: Gather facts for hsrp interfaces
  cisco.ios.ios_hsrp_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
# -   name: GigabitEthernet1
# -   name: GigabitEthernet2
#     standby_options:
#     -   authentication:
#             key_chain: AUTH_CHAIN
#         group_no: 2
#         ip:
#         -   secondary: true
#             virtual_ip: 172.16.2.1
#         priority: 100
# -   name: GigabitEthernet3
#     standby_options:
#     -   group_no: 1
#         ip:
#         -   virtual_ip: 172.16.1.1
#         priority: 100
# -   name: GigabitEthernet4
# -   delay:
#         minimum: 5555
#         reload: 556
#     mac_refresh: 45
#     name: Vlan70
#     redirect:
#         advertisement:
#             authentication:
#                 key_chain: HSRP_CHAIN
#         timers:
#             adv_timer: 10
#             holddown_timer: 55
#     standby_options:
#     -   authentication:
#             encryption: 7
#             key_string: 0123456789ABCDEF
#         follow: MASTER_GROUP
#         group_name: PRIMARY_GROUP
#         group_no: 10
#         ip:
#         -   secondary: true
#             virtual_ip: 10.0.10.2
#         preempt:
#             delay: true
#             enabled: true
#             minimum: 100
#             reload: 50
#             sync: 30
#         priority: 110
#         track:
#         -   decrement: 20
#             track_no: 1
#     -   follow: MASTER_GROUP
#         group_name: IPV6_GROUP
#         group_no: 20
#         ipv6:
#             addresses:
#             - 2001:DB8:20::1/64
#             autoconfig: true
#         mac_address: 0000.0000.0014
#         priority: 120
#     version: 2
# -   delay:
#         minimum: 100
#         reload: 200
#     name: Vlan100
#     standby_options:
#     -   group_name: BACKUP_GROUP
#         group_no: 5
#         ip:
#         -   virtual_ip: 192.168.1.1
#         preempt:
#             enabled: true
#         priority: 150
#         track:
#         -   decrement: 30
#             track_no: 10
#     version: 2

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_hsrp_interfaces:
    config:
      - delay:
          minimum: 5555
          reload: 556
        mac_refresh: 45
        name: Vlan70
        redirect:
          advertisement:
            authentication:
              key_chain: HSRP_CHAIN
          timers:
            adv_timer: 10
            holddown_timer: 55
        standby_options:
          - authentication:
              encryption: 7
              key_string: 0123456789ABCDEF
            follow: MASTER_GROUP
            group_name: PRIMARY_GROUP
            group_no: 10
            ip:
              - virtual_ip: 10.0.10.1
              - secondary: true
                virtual_ip: 10.0.10.2
              - secondary: true
                virtual_ip: 10.0.10.3
            mac_address: 0000.0c07.ac0a
            preempt:
              delay: true
              enabled: true
              minimum: 100
              reload: 50
              sync: 30
            priority: 110
            timers:
              hold_time: 250
              msec:
                hello_interval: 200
            track:
              - decrement: 20
                track_no: 1
              - shutdown: true
                track_no: 2
          - follow: MASTER_GROUP
            group_name: IPV6_GROUP
            group_no: 20
            ipv6:
              addresses:
                - 2001:db8:10::1/64
                - 2001:db8:20::1/64
              autoconfig: true
            mac_address: 0000.0c07.ac14
            priority: 120
        version: 2
      - delay:
          minimum: 100
          reload: 200
        name: Vlan100
        standby_options:
          - authentication:
              password_text: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
            group_name: BACKUP_GROUP
            group_no: 5
            ip:
              - virtual_ip: 192.168.1.1
            preempt:
              enabled: true
            priority: 150
            timers:
              hello_interval: 5
              hold_time: 15
            track:
              - decrement: 30
                track_no: 10
        version: 2
      - name: GigabitEthernet3
        standby_options:
          - group_no: 1
            ip:
              - virtual_ip: 172.16.1.1
            priority: 100
        use_bia:
          set: true
      - name: GigabitEthernet2
        standby_options:
          - authentication:
              key_chain: AUTH_CHAIN
            group_no: 2
            ip:
              - secondary: true
                virtual_ip: 172.16.2.1
            priority: 100
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface Vlan70
# - standby version 2
# - standby delay minimum 5555 reload 556
# - standby mac-refresh 45
# - standby redirect timers 10 55
# - standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
# - standby 10 follow MASTER_GROUP
# - standby 10 mac-address 0000.0c07.ac0a
# - standby 10 name PRIMARY_GROUP
# - standby 10 preempt delay minimum 100 reload 50 sync 30
# - standby 10 priority 110
# - standby 10 authentication md5 key-string 7 0123456789ABCDEF
# - standby 10 ip 10.0.10.1
# - standby 10 ip 10.0.10.2 secondary
# - standby 10 ip 10.0.10.3 secondary
# - standby 10 track 1 decrement 20
# - standby 10 track 2 shutdown
# - standby 20 follow MASTER_GROUP
# - standby 20 mac-address 0000.0c07.ac14
# - standby 20 name IPV6_GROUP
# - standby 20 priority 120
# - standby 20 ipv6 autoconfig
# - standby 20 ipv6 2001:db8:10::1/64
# - standby 20 ipv6 2001:db8:20::1/64
# - interface Vlan100
# - standby version 2
# - standby delay minimum 100 reload 200
# - standby 5 name BACKUP_GROUP
# - standby 5 preempt
# - standby 5 priority 150
# - standby 5 authentication ********
# - standby 5 ip 192.168.1.1
# - standby 5 track 10 decrement 30
# - interface GigabitEthernet3
# - standby version 1
# - standby use-bia scope interface
# - standby 1 priority 100
# - standby 1 ip 172.16.1.1
# - interface GigabitEthernet2
# - standby version 1
# - standby 2 priority 100
# - standby 2 authentication md5 key-chain AUTH_CHAIN
# - standby 2 ip 172.16.2.1 secondary

# Using parsed

# File: parsed.cfg
# ----------------
#
# interface Vlan70
#  no ip address
#  standby mac-refresh 45
#  standby redirect timers 10 55
#  standby delay minimum 5555 reload 556
#  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
#  standby version 2
#  standby 10 ip 10.0.10.1
#  standby 10 ip 10.0.10.2 secondary
#  standby 10 ip 10.0.10.3 secondary
#  standby 10 follow MASTER_GROUP
#  standby 10 timers msec 200 250
#  standby 10 priority 110
#  standby 10 preempt delay minimum 100 reload 50 sync 30
#  standby 10 authentication md5 key-string 7 0123456789ABCDEF
#  standby 10 name PRIMARY_GROUP
#  standby 10 mac-address 0000.0c07.ac0a
#  standby 10 track 1 decrement 20
#  standby 10 track 2 shutdown
#  standby 20 ipv6 2001:db8:10::1/64
#  standby 20 ipv6 2001:db8:20::1/64
#  standby 20 ipv6 autoconfig
#  standby 20 follow MASTER_GROUP
#  standby 20 priority 120
#  standby 20 name IPV6_GROUP
#  standby 20 mac-address 0000.0c07.ac14

# interface Vlan100
#  no ip address
#  standby bfd
#  standby delay minimum 100 reload 200
#  standby version 2
#  standby 5 ip 192.168.1.1
#  standby 5 timers 5 15
#  standby 5 priority 150
#  standby 5 preempt
#  standby 5 authentication hello_secret
#  standby 5 name BACKUP_GROUP
#  standby 5 track 10 decrement 30

# interface GigabitEthernet3
#  standby use-bia
#  standby 1 ip 172.16.1.1
#  standby 1 priority 100

# interface GigabitEthernet2
#  standby follow VLAN70_GROUP
#  standby 2 ip 172.16.2.1 secondary
#  standby 2 authentication md5 key-chain AUTH_CHAIN

# - name: Parse the provided configuration
#   cisco.ios.ios_hsrp_interfaces:
#     running_config: "{{ lookup('file', 'parsed.cfg') }}"
#     state: parsed

# Task Output
# -----------
#
# parsed:
# -   delay:
#         minimum: 5555
#         reload: 556
#     mac_refresh: 45
#     name: Vlan70
#     redirect:
#         advertisement:
#             authentication:
#                 key_chain: HSRP_CHAIN
#         timers:
#             adv_timer: 10
#             holddown_timer: 55
#     standby_options:
#     -   authentication:
#             encryption: 7
#             key_string: 0123456789ABCDEF
#         follow: MASTER_GROUP
#         group_name: PRIMARY_GROUP
#         group_no: 10
#         ip:
#         -   virtual_ip: 10.0.10.1
#         -   secondary: true
#             virtual_ip: 10.0.10.2
#         -   secondary: true
#             virtual_ip: 10.0.10.3
#         mac_address: 0000.0c07.ac0a
#         preempt:
#             delay: true
#             enabled: true
#             minimum: 100
#             reload: 50
#             sync: 30
#         priority: 110
#         timers:
#             hold_time: 250
#             msec:
#                 hello_interval: 200
#         track:
#         -   decrement: 20
#             track_no: 1
#         -   shutdown: true
#             track_no: 2
#     -   follow: MASTER_GROUP
#         group_name: IPV6_GROUP
#         group_no: 20
#         ipv6:
#             addresses:
#             - 2001:db8:10::1/64
#             - 2001:db8:20::1/64
#             autoconfig: true
#         mac_address: 0000.0c07.ac14
#         priority: 120
#     version: 2
# -   delay:
#         minimum: 100
#         reload: 200
#     name: Vlan100
#     standby_options:
#     -   authentication:
#             password_text: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
#         group_name: BACKUP_GROUP
#         group_no: 5
#         ip:
#         -   virtual_ip: 192.168.1.1
#         preempt:
#             enabled: true
#         priority: 150
#         timers:
#             hello_interval: 5
#             hold_time: 15
#         track:
#         -   decrement: 30
#             track_no: 10
#     version: 2
# -   name: GigabitEthernet3
#     standby_options:
#     -   group_no: 1
#         ip:
#         -   virtual_ip: 172.16.1.1
#         priority: 100
#     use_bia:
#         set: true
# -   name: GigabitEthernet2
#     standby_options:
#     -   authentication:
#             key_chain: AUTH_CHAIN
#         group_no: 2
#         ip:
#         -   secondary: true
#             virtual_ip: 172.16.2.1
#         priority: 100
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
    - standby 22 ip 10.0.0.1 secondary
    - standby 0 priority 5
    - standby mac-refresh 21
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - standby 22 ip 10.0.0.1 secondary
    - standby 0 priority 5
    - standby mac-refresh 21
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Hsrp_interfacesArgs.argument_spec,
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

    result = Hsrp_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
