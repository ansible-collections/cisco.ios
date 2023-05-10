#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_service
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
---
module: ios_service
short_description: Resource module to configure service.
description:
  - This module configures and manages service attributes on IOS platforms
version_added: 4.6.0
author:
  - Ambroise Rosset (@earendilfr)
notes:
  - Tested against Cisco IOSXE Version 16.9
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionnary of service configuration
    suboptions:
      call_home:
        description: Cisco call-home service
        type: bool
      compress_config:
        description: Compress the nvram configuration file
        type: bool
      config:
        description: TFTP load config files
        type: bool
      counters:
        description:
          - Control aging of interface counters by setting the maximum counter aging threshold
        type: int
        default: 0
      dhcp:
        description: Enable DHCP server and relay agent
        type: bool
        default: true
      disable_ip_fast_frag:
        description: Disable IP particle-based fast fragmentation
        type: bool
      exec_callback:
        description: Enable exec callback
        type: bool
      exec_wait:
        description: Delay EXEC startup on noisy lines
        type: bool
      hide_telnet_addresses:
        description: Hide destination addresses in telnet command
        type: bool
      internal:
        description: Enable/Disable Internal commands
        type: bool
      linenumber:
        description: enable line number banner for each exec
        type: bool
      log:
        description: log backtrace
        type: bool
      log_hidden:
        description: Enable syslog msgs for hidden/internal commands
        type: bool
      nagle:
        description: Enable Nagle's congestion control algorithm
        type: bool
      old_slip_prompts:
        description: Allow old scripts to operate with slip/ppp
        type: bool
      pad:
        description: Enable PAD commands
        type: bool
      pad_cmns:
        description: Enable PAD over CMNS connections
        type: bool
      pad_from_xot:
        description: Accept XOT to PAD connections
        type: bool
      pad_to_xot:
        description: Allow outgoing PAD over XOT connections
        type: bool
      password_encryption:
        description: Encrypt system passwords
        type: bool
      password_recovery:
        description: Password recovery
        type: bool
        default: true
      prompt:
        description: Enable mode specific prompt
        type: bool
        default: true
      private_config_encryption:
        description: Enable private config file encryption
        type: bool
      pt_vty_logging:
        description: Log significant VTY-Async events
        type: bool
      scripting:
        description: scripting
        type: bool
      sequence_numbers:
        description: Stamp logger messages with a sequence number
        type: bool
      slave_coredump:
        description: slave-coredump
        type: bool
      slave_log:
        description: Enable log capability of slave IPs
        type: bool
        default: true
      tcp_keepalives_in:
        description: Generate keepalives on idle incoming network connections
        type: bool
      tcp_keepalives_out:
        description: Generate keepalives on idle outgoing network connections
        type: bool
      tcp_small_servers:
        description:
          - TCP and UDP small servers are servers (daemons, in Unix parlance) that run in the
            router which are useful for diagnostics.
        suboptions:
          enable:
            description: Enable small TCP servers (e.g., ECHO)
            type: bool
          max_servers:
            description:
              - Set number of allowable TCP small servers
              - 1 to 2147483647 or no-limit
            type: str
        type: dict
      telnet_zeroidle:
        description: Set TCP window 0 when connection is idle
        type: bool
      timestamps:
        description: Timestamp debug/log messages
        elements: dict
        suboptions:
          msg:
            description: Timestamp log or debug messages
            choices:
              - debug
              - log
            type: str
          enable:
            description: Enable timestamp for the choosen message
            type: bool
          timestamp:
            description: Timestamp with date and time or with system uptime
            choices:
              - datetime
              - uptime
            type: str
          datetime_options:
            description: Options for date and time timestamp
            suboptions:
              localtime:
                description: Use local time zone for timestamps
                type: bool
              msec:
                description: Include milliseconds in timestamp
                type: bool
              show_timezone:
                description: Add time zone information to timestamp
                type: bool
              year:
                description: Include year in timestam
                type: bool
            type: dict
        type: list
      udp_small_servers:
        description:
          - TCP and UDP small servers are servers (daemons, in Unix parlance) that run in the
            router which are useful for diagnostics.
        suboptions:
          enable:
            description: Enable small UDP servers (e.g., ECHO)
            type: bool
          max_servers:
            description:
              - Set number of allowable TCP small servers
              - 1 to 2147483647 or no-limit
            type: str
        type: dict
      unsupported_transceiver:
        description: enable support for third-party transceivers
        type: bool
    type: dict
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^service|^no service).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
      - merged
      - replaced
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
    description:
      - The state the configuration should be left in.
      - Refer to examples for more details.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------

# router-ios#show running-config all | section ^service
# service slave-log
# service timestamps debug datetime msec
# service timestamps log datetime msec
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service call-home
# service password-recovery

- name: Merge provided configuration with device configuration
  cisco.ios.ios_service:
    config:
      tcp_keepalives_in: true
      tcp_keepalives_out: true
      timestamps:
        - msg: debug
          enable: true
          timestamp: datetime
        - msg: log
          enable: true
          timestamp: datetime
      pad: false
      password_encryption: true
    state: merged

# Task Output
# -----------
#
# before:
#   call_home: true
#   counters: 0
#   dhcp: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   timestamps:
#   - datetime_options:
#       msec: true
#     msg: debug
#     timestamp: datetime
#   - datetime_options:
#       msec: true
#     msg: log
#     timestamp: datetime
# commands:
# - service password-encryption
# - service tcp-keepalives-in
# - service tcp-keepalives-out
# after:
#   call_home: true
#   counters: 0
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   tcp_keepalives_in: true
#   tcp_keepalives_out: true
#   timestamps:
#   - datetime_options:
#       msec: true
#     msg: debug
#     timestamp: datetime
#   - datetime_options:
#       msec: true
#     msg: log
#     timestamp: datetime

# After state:
# ------------

# router-ios#show running-config all | section ^service
# service slave-log
# service tcp-keepalives-in
# service tcp-keepalives-out
# service timestamps debug datetime msec
# service timestamps log datetime msec
# service password-encryption
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service call-home
# service password-recovery

# Using replaced

# Before state:
# -------------

# router-ios#show running-config all | section ^service
# service slave-log
# service tcp-keepalives-in
# service tcp-keepalives-out
# service timestamps debug datetime msec
# service timestamps log datetime msec
# service password-encryption
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service call-home
# service password-recovery

- name: Replaces device configuration of services with provided configuration
  cisco.ios.ios_service:
    config:
      timestamps:
        - msg: log
          enable: true
          timestamp: datetime
          datetime_options:
            localtime: true
            msec: true
            show_timezone: true
            year: true
        - msg: debug
          enable: true
          timestamp: datetime
      pad: false
      password_encryption: true
    state: "replaced"

# Task Output
# -----------
#
# before:
#   call_home: true
#   counters: 0
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   tcp_keepalives_in: true
#   tcp_keepalives_out: true
#   timestamps:
#   - datetime_options:
#       msec: true
#     msg: debug
#     timestamp: datetime
#   - datetime_options:
#       msec: true
#     msg: log
#     timestamp: datetime
# commands:
# - no service call-home
# - no service tcp-keepalives-in
# - no service tcp-keepalives-out
# - no service timestamps log
# - service timestamps log datetime msec localtime show-timezone year
# - no service timestamps debug
# - service timestamps debug datetime
# after:
#   counters: 0
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   timestamps:
#   - msg: debug
#     timestamp: datetime
#   - datetime_options:
#       localtime: true
#       msec: true
#       show_timezone: true
#       year: true
#     msg: log
#     timestamp: datetime

# After state:
# ------------

# router-ios#show running-config all | section ^service
# service slave-log
# service timestamps debug datetime
# service timestamps log datetime msec localtime show-timezone year
# service password-encryption
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service password-recovery

# Using Deleted

# Before state:
# -------------

# router-ios#show running-config all | section ^service
# service slave-log
# service timestamps debug datetime
# service timestamps log datetime msec localtime show-timezone year
# service password-encryption
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service password-recovery

- name: "Delete service configuration and restore default configuration for some importants service (those with a default value in module)"
  cisco.ios.ios_service:
    state: deleted

# Task Output
# -----------
#
# before:
#   counters: 0
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   timestamps:
#   - msg: debug
#     timestamp: datetime
#   - datetime_options:
#       localtime: true
#       msec: true
#       show_timezone: true
#       year: true
#     msg: log
#     timestamp: datetime
# commands:
# - no service password-encryption
# - no service timestamps debug
# - no service timestamps log
# after:
#   counters: 0
#   dhcp: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true

#·After·state:
#·------------
#
# router-ios#show running-config all | section ^service
# service slave-log
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service password-recovery

# Using gathered

# Before state:
# -------------
#
# router-ios#show running-config all | section ^service
# service slave-log
# service timestamps debug datetime
# service timestamps log datetime msec localtime show-timezone year
# service password-encryption
# service private-config-encryption
# service prompt config
# service counters max age 0
# service dhcp
# service password-recovery

- name: Gather facts of interfaces
  cisco.ios.ios_service:
    config:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   counters: 0
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   private_config_encryption: true
#   prompt: true
#   slave_log: true
#   timestamps:
#   - msg: debug
#     timestamp: datetime
#   - datetime_options:
#       localtime: true
#       msec: true
#       show_timezone: true
#       year: true
#     msg: log
#     timestamp: datetime

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_service:
    config:
      timestamps:
        - msg: log
          enable: true
          timestamp: datetime
          datetime_options:
            localtime: true
            msec: true
            show_timezone: true
            year: true
        - msg: debug
          enable: true
          timestamp: datetime
      pad: false
      password_encryption: true
    state: rendered

# ·Task·Output
# -----------
#
# rendered:
# - service dhcp
# - service password-encryption
# - service password-recovery
# - service prompt config
# - service slave-log
# - service timestamps log datetime msec localtime show-timezone year
# - service timestamps debug datetime

# Using parsed

# File: parsed.cfg
# ----------------
#
# no service pad
# service password-encryption
# service tcp-keepalives-in
# service tcp-keepalives-out
# service timestamps debug datetime msec localtime show-timezone year
# service timestamps log datetime msec localtime show-timezone year
# service counters max age 5

- name: Parse the provided configuration
  cisco.ios.ios_service:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
#   counters: 5
#   dhcp: true
#   password_encryption: true
#   password_recovery: true
#   prompt: true
#   slave_log: true
#   tcp_keepalives_in: true
#   tcp_keepalives_out: true
#   timestamps:
#   - datetime_options:
#       localtime: true
#       msec: true
#       show_timezone: true
#       year: true
#     msg: debug
#     timestamp: datetime
#   - datetime_options:
#       localtime: true
#       msec: true
#       show_timezone: true
#       year: true
#     msg: log
#     timestamp: datetime
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
    - no service config
    - service tcp-keepalives-in
    - service tcp-keepalives-out
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - service dhcp
    - service password-encryption
    - service password-recovery
    - service prompt config
    - service slave-log
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.service.service import (
    ServiceArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.service.service import (
    Service,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=ServiceArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Service(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
