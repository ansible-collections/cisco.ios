#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_interfaces
short_description: Resource module to configure interfaces.
description: This module manages the interface attributes of Cisco IOS network devices.
version_added: 1.0.0
author:
  - Sumit Jaiswal (@justjais)
  - Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of interface, e.g. GigabitEthernet0/2, loopback999.
        type: str
        required: true
      description:
        description:
          - Interface description.
        type: str
      enabled:
        description:
          - Administrative state of the interface.
          - Set the value to C(true) to administratively enable the interface or C(false)
            to disable it.
        type: bool
      speed:
        description:
          - Interface link speed. Applicable for Ethernet interfaces only.
        type: str
      mtu:
        description:
          - MTU for a specific interface. Applicable for Ethernet interfaces only.
          - Refer to vendor documentation for valid values.
        type: int
      mode:
        description:
          - Manage Layer2 or Layer3 state of the interface.
          - For a Layer 2 appliance mode Layer2 adds switchport command ( default impacts idempotency).
          - For a Layer 2 appliance mode Layer3 adds no switchport command.
          - For a Layer 3 appliance mode Layer3/2 has no impact rather command fails on apply.
        choices:
          - layer2
          - layer3
        type: str
      duplex:
        description:
          - Interface link status. Applicable for Ethernet interfaces only, either in
            half duplex, full duplex or in automatic state which negotiates the duplex
            automatically.
        type: str
        choices:
          - full
          - half
          - auto
      template:
        description:
          - IOS template name.
        type: str
      mac_address:
        description:
          - H.H.H  MAC address.
        type: str
      service_policy:
        description:
          - Service policy configuration
        type: dict
        suboptions:
          input:
            description:
              - Assign policy-map to the input of an interface
            type: str
          output:
            description:
              - Assign policy-map to the output of an interface
            type: str
          type_options:
            description:
              - Configure CPL Service Policy
            type: dict
            suboptions:
              access_control:
                description: access-control specific policy-map
                type: dict
                suboptions:
                  input:
                    description:
                      - Assign policy-map to the input of an interface
                    type: str
                  output:
                    description:
                      - Assign policy-map to the output of an interface
                    type: str
              epbr:
                description: Configure ePBR Service Policy
                type: dict
                suboptions:
                  input:
                    description:
                      - Assign policy-map to the input of an interface
                    type: str
                  output:
                    description:
                      - Assign policy-map to the output of an interface
                    type: str
              nwpi:
                description: Configure Network Wide Path Insight Service Policy
                type: dict
                suboptions:
                  input:
                    description:
                      - Assign policy-map to the input of an interface
                    type: str
                  output:
                    description:
                      - Assign policy-map to the output of an interface
                    type: str
              packet_service:
                description: Configure Packet-Service Service Policy
                type: dict
                suboptions:
                  input:
                    description:
                      - Assign policy-map to the input of an interface
                    type: str
                  output:
                    description:
                      - Assign policy-map to the output of an interface
                    type: str
              service_chain:
                description: Configure Service-chain Service Policy
                type: dict
                suboptions:
                  input:
                    description:
                      - Assign policy-map to the input of an interface
                    type: str
                  output:
                    description:
                      - Assign policy-map to the output of an interface
                    type: str
      logging:
        description:
          - Logging interface events
        type: dict
        suboptions:
          bundle_status:
            description:
              - BUNDLE/UNBUNDLE messages
            type: bool
          link_status:
            description:
              - UPDOWN and CHANGE messages
            type: bool
          nfas_status:
            description:
              - NFAS D-channel status messages
            type: bool
          spanning_tree:
            description:
              - Spanning-tree Interface events
            type: bool
          status:
            description:
              - Spanning-tree state change messages
            type: bool
          subif_link_status:
            description:
              - Sub-interface UPDOWN and CHANGE messages
            type: bool
          trunk_status:
            description:
              - TRUNK status messages
            type: bool
      snmp:
        description:
          - snmp trap configurations
        type: dict
        suboptions:
          trap:
            description:
              - Allow a specific SNMP trap
            type: dict
            suboptions:
              ip:
                description: internet protocol (snmp trap ip verify drop-rate)
                type: bool
              link_status:
                description: Allow SNMP LINKUP and LINKDOWN traps (snmp trap link-status permit duplicates)
                type: bool
              mac_notification_added:
                description: MAC Address notification for the interface (snmp trap mac-notification change added)
                type: bool
              mac_notification_removed:
                description: MAC Address notification for the interface (snmp trap mac-notification change removed)
                type: bool
          ifindex:
            description:
              - Persist ifindex for the interface
            type: dict
            suboptions:
              clear:
                description: Clear Enable/Disable ifIndex persistence
                type: bool
              persist:
                description: Enable/Disable ifIndex persistence
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^interface).
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
      - rendered
      - gathered
      - purged
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
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# Router#sh running-config | section interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  description Configured and Merged by Ansible Network
#  ip address dhcp
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Merge provided configuration with device configuration
  cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet2
        description: Configured and Merged by Ansible Network
        enabled: true
      - name: GigabitEthernet3
        description: Configured and Merged by Ansible Network
        mtu: 3800
        enabled: false
        speed: 100
        duplex: full
    state: merged

# Task Output
# -----------
#
# before:
# - enabled: true
#   name: GigabitEthernet1
# - description: Configured and Merged by Ansible Network
#   enabled: true
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Merged by Ansible Network
#   enabled: false
#   mtu: 3800
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: true
#   name: Loopback888
# - enabled: true
#   name: Loopback999
# commands:
# - interface GigabitEthernet3
# - description Configured and Merged by Ansible Network
# - speed 100
# - mtu 3800
# - duplex full
# - shutdown
# after:
# - enabled: true
#   name: GigabitEthernet1
# - description: Configured and Merged by Ansible Network
#   enabled: true
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Merged by Ansible Network
#   enabled: true
#   mtu: 2800
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: true
#   name: Loopback888
# - enabled: true
#   name: Loopback999

# After state:
# ------------
#
# Router#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  description Configured and Merged by Ansible Network
#  ip address dhcp
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Merged by Ansible Network
#  mtu 3800
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using merged - with mode attribute

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Configured by Ansible
# interface GigabitEthernet2
#  description This is test
# interface GigabitEthernet3
#  description This is test
#  no switchport

- name: Merge provided configuration with device configuration
  cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet2
        description: Configured and Merged by Ansible Network
        enabled: true
        mode: layer2
      - name: GigabitEthernet3
        description: Configured and Merged by Ansible Network
        mode: layer3
    state: merged

# Task Output
# -----------
#
# before:
# - enabled: true
#   name: GigabitEthernet1
# - description: Configured and Merged by Ansible Network
#   name: GigabitEthernet2
# - description: Configured and Merged by Ansible Network
#   name: GigabitEthernet3
# commands:
# - interface GigabitEthernet2
# - description Configured and Merged by Ansible Network
# - switchport
# - interface GigabitEthernet3
# - description Configured and Merged by Ansible Network
# after:
# - enabled: true
#   name: GigabitEthernet1
# - description: Configured and Merged by Ansible Network
#   enabled: true
#   name: GigabitEthernet2
# - description: Configured and Merged by Ansible Network
#   name: GigabitEthernet3
#   mode: layer3

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet1
#  description Configured by Ansible
# interface GigabitEthernet2
#  description Configured and Merged by Ansible Network
# interface GigabitEthernet3
#  description Configured and Merged by Ansible Network
#  no switchport

# Using replaced

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  no ip address
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet3
        description: Configured and Replaced by Ansible Network
        enabled: false
        speed: 1000
    state: replaced

# Task Output
# -----------
#
# before:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: true
#   name: GigabitEthernet2
#   speed: '1000'
# - enabled: true
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: true
#   name: Loopback888
# - enabled: true
#   name: Loopback999
# - enabled: true
#   name: Vlan50
# commands:
# - interface GigabitEthernet3
# - description Configured and Replaced by Ansible Network
# - shutdown
# after:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: true
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Replaced by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: true
#   name: Loopback888
# - enabled: true
#   name: Loopback999
# - enabled: true
#   name: Vlan50

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Replaced by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname

# Using overridden

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
# interface Loopback999
#  no ip address
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Replaced by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
      - description: Management interface do not change
        enabled: true
        name: GigabitEthernet1
      - name: GigabitEthernet2
        description: Configured and Overridden by Ansible Network
        speed: 10000
      - name: GigabitEthernet3
        description: Configured and Overridden by Ansible Network
        enabled: false
    state: overridden

# Task Output
# -----------
#
# before:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: true
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Replaced by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: true
#   name: Loopback888
# - enabled: true
#   name: Loopback999
# - enabled: true
#   name: Vlan50
# commands:
# - interface loopback888
# - shutdown
# - interface loopback999
# - shutdown
# - interface Vlan50
# - shutdown
# - interface GigabitEthernet2
# - description Configured and Overridden by Ansible Network
# - speed 10000
# - interface GigabitEthernet3
# - description Configured and Overridden by Ansible Network
# - no speed 1000
# after:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - description: Configured and Overridden by Ansible Network
#   enabled: true
#   name: GigabitEthernet2
#   speed: '10000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback888
# - enabled: false
#   name: Loopback999
# - enabled: false
#   name: Vlan50

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
#  shutdown
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  description Configured and Overridden by Ansible Network
#  ip address dhcp
#  speed 10000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname
#  shutdown

# Using Deleted

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
#  shutdown
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  description Configured and Overridden by Ansible Network
#  ip address dhcp
#  speed 10000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname
#  shutdown

- name: "Delete interface attributes (Note: This won't delete the interface itself)"
  cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet2
    state: deleted

# Task Output
# -----------
#
# before:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - description: Configured and Overridden by Ansible Network
#   enabled: true
#   name: GigabitEthernet2
#   speed: '10000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback888
# - enabled: false
#   name: Loopback999
# - enabled: false
#   name: Vlan50
# commands:
# - interface GigabitEthernet2
# - no description Configured and Overridden by Ansible Network
# - no speed 10000
# - shutdown
# after:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: false
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback888
# - enabled: false
#   name: Loopback999
# - enabled: false
#   name: Vlan50

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
#  shutdown
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname
#  shutdown

# Using Purged

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback888
#  no ip address
#  shutdown
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto
# interface Vlan50
#  ip address dhcp hostname testHostname
#  shutdown

- name: "Purge given interfaces (Note: This will delete the interface itself)"
  cisco.ios.ios_interfaces:
    config:
      - name: Loopback888
      - name: Vlan50
    state: purged

# Task Output
# -----------
#
# before:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: false
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback888
# - enabled: false
#   name: Loopback999
# - enabled: false
#   name: Vlan50
# commands:
# - no interface loopback888
# - no interface Vlan50
# after:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: false
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback999

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Gather facts of interfaces
  cisco.ios.ios_interfaces:
    config:
    state: gathered

# Task Output
# -----------
#
# gathered:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: false
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback999

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet1
        description: Configured by Ansible-Network
        mtu: 110
        enabled: true
        duplex: half
      - name: GigabitEthernet2
        description: Configured by Ansible-Network
        mtu: 2800
        enabled: false
        speed: 100
        duplex: full
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface GigabitEthernet1
# - description Configured by Ansible-Network
# - mtu 110
# - duplex half
# - no shutdown
# - interface GigabitEthernet2
# - description Configured by Ansible-Network
# - speed 100
# - mtu 2800
# - duplex full
# - shutdown

# Using parsed

# File: parsed.cfg
# ----------------
#
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address dhcp
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Parse the provided configuration
  cisco.ios.ios_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
# - description: Management interface do not change
#   enabled: true
#   name: GigabitEthernet1
# - enabled: false
#   name: GigabitEthernet2
#   speed: '1000'
# - description: Configured and Overridden by Ansible Network
#   enabled: false
#   name: GigabitEthernet3
#   speed: '1000'
# - enabled: false
#   name: GigabitEthernet4
# - enabled: false
#   name: Loopback999
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
    - interface GigabitEthernet2
    - speed 1200
    - mtu 1800
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet1
    - description Interface description
    - shutdown
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.interfaces.interfaces import (
    Interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=InterfacesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "purged", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
