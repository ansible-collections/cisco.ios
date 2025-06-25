#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_evpn_ethernet
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_evpn_ethernet
short_description: Resource module to configure L2VPN EVPN Ethernet Segment.
description: This module manages the L2VPN EVPN Ethernet Segment attributes of Cisco IOS network devices.
version_added: 9.2.0
author:
  - Sagar Paul (@KB-perByte)
  - Jorgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOSXE Version 17.16.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (callback_result_format=yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary of L2VPN EVPN Ethernet Segment options
    type: list
    elements: dict
    suboptions:
      segment:
        description:
          - L2VPN EVPN Ethernet Segment, l2vpn evpn ethernet-segment 1
        type: str
        required: true
      default:
        description: Set a command to its defaults
        type: bool
      df_election:
        description: Designated forwarder election parameters
        type: dict
        suboptions:
          preempt_time:
            description: Preempt time before advertising routes
            type: int
          wait_time:
            description: Designated forwarder election wait time
            type: int
      identifier:
        description: Ethernet Segment Identifiers
        type: dict
        suboptions:
          identifier_type:
            description:
              - Type 0 (arbitrary 9-octet ESI value)
              - Type 3 (MAC-based ESI value)
            type: str
            choices:
              - '0'
              - '3'
          esi_value:
            description: system mac or 9-octet ESI value in hex
            type: str
      redundancy:
        description: Multi-homing redundancy parameters
        type: dict
        suboptions:
          all_active:
            description: Per-flow load-balancing between PEs on same Ethernet Segment
            type: bool
          single_active:
            description: Per-vlan load-balancing between PEs on same Ethernet Segment
            type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^l2vpn).
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
        | section ^l2vpn) executed on device. For state I(parsed) active
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
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
      - identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.01
        redundancy:
          single_active: true
        segment: '1'
      - df_election:
          preempt_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.02
        redundancy:
          single_active: true
        segment: '2'
      - identifier:
          identifier_type: '3'
          esi_value: 00.00.00.00.00.00.00.00.03
        redundancy:
          single_active: true
        segment: '3'
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.04
        redundancy:
          all_active: true
        segment: '4'
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.05
        redundancy:
          all_active: true
        segment: '5'
    state: merged

# Task Output
# -----------
#
# before:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
# commands:
# - l2vpn evpn ethernet-segment 5
# - identifier type 0 00.00.00.00.00.00.00.00.05
# - redundancy all-active
# - df-election wait-time 1
# after:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.05
#    redundancy:
#        all_active: true
#    segment: '5'

# After state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !
# l2vpn evpn ethernet-segment 5
#  identifier type 0 00.00.00.00.00.00.00.00.05
#  redundancy all-active
#  df-election wait-time 1
# !

# Using replaced

# Before state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.04
        redundancy:
          single_active: true
        segment: '4'
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.05
        redundancy:
          all_active: true
        segment: '5'
    state: replaced

# Task Output
# -----------
#
# before:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
# commands:
# - l2vpn evpn ethernet-segment 4
# - redundancy single-active
# - l2vpn evpn ethernet-segment 5
# - identifier type 0 00.00.00.00.00.00.00.00.05
# - redundancy all-active
# - df-election wait-time 1
# after:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        single_active: true
#    segment: '4'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.05
#    redundancy:
#        all_active: true
#    segment: '5'

# After state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy single-active
#  df-election wait-time 1
# !
# l2vpn evpn ethernet-segment 5
#  identifier type 0 00.00.00.00.00.00.00.00.05
#  redundancy all-active
#  df-election wait-time 1
# !

# Using overridden

# Before state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.04
        redundancy:
          single_active: true
        segment: '4'
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.05
        redundancy:
          all_active: true
        segment: '5'
    state: overridden

# After state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy single-active
#  df-election wait-time 1
# !
# l2vpn evpn ethernet-segment 5
#  identifier type 0 00.00.00.00.00.00.00.00.05
#  redundancy all-active
#  df-election wait-time 1
# !

# Using deleted

# Before state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
      - identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.01
        redundancy:
          single_active: true
        segment: '1'
      - df_election:
          preempt_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.02
        redundancy:
          single_active: true
        segment: '2'
    state: deleted

# Task Output
# -----------
#
# before:
#  - identifier:
#      identifier_type: '0'
#      esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#      single_active: true
#    segment: '1'
#  - df_election:
#      preempt_time: 1
#    identifier:
#      identifier_type: '0'
#      esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#      single_active: true
#    segment: '2'
#  - identifier:
#      identifier_type: '3'
#      esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#      single_active: true
#    segment: '3'
#  - df_election:
#      wait_time: 1
#    identifier:
#      identifier_type: '0'
#      esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#      all_active: true
#    segment: '4'
# commands:
# - l2vpn evpn ethernet-segment 1
# - no identifier type 0 00.00.00.00.00.00.00.00.01
# - no redundancy single-active
# - l2vpn evpn ethernet-segment 2
# - no identifier type 0 00.00.00.00.00.00.00.00.02
# - no redundancy single-active
# - no df-election wait-time 1
# after:
#  - segment: '1'
#  - segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.05
#    redundancy:
#        all_active: true
#    segment: '5'

# After state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
# !
# l2vpn evpn ethernet-segment 2
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !
# l2vpn evpn ethernet-segment 5
#  identifier type 0 00.00.00.00.00.00.00.00.05
#  redundancy all-active
#  df-election wait-time 1
# !

# Using purged

# Before state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
      - segment: '1'
      - segment: '2'
    state: purged

# Task Output
# -----------
#
# before:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
# commands:
# - no l2vpn evpn ethernet-segment 1
# - no l2vpn evpn ethernet-segment 2
# after:
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.05
#    redundancy:
#        all_active: true
#    segment: '5'

# After state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !
# l2vpn evpn ethernet-segment 5
#  identifier type 0 00.00.00.00.00.00.00.00.05
#  redundancy all-active
#  df-election wait-time 1
# !

# Using gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^l2vpn evpn ethernet-segment
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Gather facts of evpn ethernet segment
  cisco.ios.ios_evpn_ethernet:
    config:
    state: gathered

# Task Output
# -----------
#
# gathered:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'

# Using rendered

- name: Render commands with provided configuration
  cisco.ios.ios_evpn_ethernet:
    config:
      - identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.01
        redundancy:
          single_active: true
        segment: '1'
      - df_election:
          preempt_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.02
        redundancy:
          single_active: true
        segment: '2'
      - identifier:
          identifier_type: '3'
          esi_value: 00.00.00.00.00.00.00.00.03
        redundancy:
          single_active: true
        segment: '3'
      - df_election:
          wait_time: 1
        identifier:
          identifier_type: '0'
          esi_value: 00.00.00.00.00.00.00.00.04
        redundancy:
          all_active: true
        segment: '4'
    state: rendered

# Task Output
# -----------
#
# rendered:
# - l2vpn evpn ethernet-segment 1
# - redundancy single-active
# - identifier type 0 00.00.00.00.00.00.00.00.01
# - l2vpn evpn ethernet-segment 2
# - df-election preempt-time 1
# - redundancy single-active
# - identifier type 0 00.00.00.00.00.00.00.00.02
# - l2vpn evpn ethernet-segment 3
# - redundancy single-active
# - identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
# - l2vpn evpn ethernet-segment 4
# - df-election wait-time 1
# - redundancy all-active
# - identifier type 0 00.00.00.00.00.00.00.00.04

# Using parsed

# File: parsed.cfg
# ----------------
#
# l2vpn evpn ethernet-segment 1
#  identifier type 0 00.00.00.00.00.00.00.00.01
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 2
#  identifier type 0 00.00.00.00.00.00.00.00.02
#  redundancy single-active
#  df-election preempt-time 1
# !
# l2vpn evpn ethernet-segment 3
#  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
#  redundancy single-active
# !
# l2vpn evpn ethernet-segment 4
#  identifier type 0 00.00.00.00.00.00.00.00.04
#  redundancy all-active
#  df-election wait-time 1
# !

- name: Parse the provided configuration
  cisco.ios.ios_evpn_ethernet:
    running_config: "{{ lookup('file', 'ios_ethernet_segment_parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
#  - identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.01
#    redundancy:
#        single_active: true
#    segment: '1'
#  - df_election:
#        preempt_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.02
#    redundancy:
#        single_active: true
#    segment: '2'
#  - identifier:
#        identifier_type: '3'
#        esi_value: 00.00.00.00.00.00.00.00.03
#    redundancy:
#        single_active: true
#    segment: '3'
#  - df_election:
#        wait_time: 1
#    identifier:
#        identifier_type: '0'
#        esi_value: 00.00.00.00.00.00.00.00.04
#    redundancy:
#        all_active: true
#    segment: '4'
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - l2vpn evpn ethernet-segment 1
    - identifier type 0 00.00.00.00.00.00.00.00.01
    - redundancy single-active
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - l2vpn evpn ethernet-segment 1
    - identifier type 3 system-mac 0000.0000.0000.0001
    - redundancy all-active
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernetArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernet,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Evpn_ethernetArgs.argument_spec,
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

    result = Evpn_ethernet(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
