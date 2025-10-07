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
      follow:
        description: Name of HSRP group to follow
        type: str
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
                    type: bool
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
            description: Scope interface option
            type: dict
            suboptions:
              interface:
                description: >-
                  Use-bia applies to all groups on this interface or
                  sub-interface
                type: bool
      version:
        description: HSRP version
        type: int
      standby_groups:
        description: Group number and group options for standby (HSRP)
        type: list
        elements: dict
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
              advertisement:
                description: Redirect advertisement messages (standby redirect advertisement authentication md5)
                type: dict
                suboptions:
                  key_chain:
                    description: Set key chain
                    type: str
                  key_string:
                    description: Set key string
                    type: bool
                  encryption:
                    description: Set encryption 0 (unencrypted/default) or 7 (hidden)
                    type: int
                  time_out:
                    description: Set timeout
                    type: int
                  password_text:
                    description: Password text valid for plain text and and key-string
                    type: str
                  text:
                    description: Password text valid for plain text
                    type: dict
                    suboptions:
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
#  no ip address
#  shutdown
#  negotiation auto

- name: Merge provided configuration with device configuration
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
            priority: 5
    state: merged

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet4
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
#         priority: 5
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

- name: "Delete attributes of given interfaces (NOTE: This won't delete the interfaces)"
  cisco.ios.ios_hsrp_interfaces:
    config:
      - name: GigabitEthernet4
    state: deleted

# Task Output
# -----------
#
# before:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet4
#     standby_groups:
#       - group_no: 0
#         priority: 10
# - name: Loopback999
# - name: Loopback888
# commands:
# - interface GigabitEthernet4
# - no standby 0 priority 10
# after:
#   name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet4
# - name: Loopback999
# - name: Loopback888

# After state:
# -------------
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
#  shutdown
#  negotiation auto

# Using deleted without config passed, only interface's configuration will be negated

# Before state:
# -------------

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

- name: "Delete HSRP config of all interfaces"
  cisco.ios.ios_hsrp_interfaces:
    state: deleted

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
#         priority: 5
# - name: Loopback999
# - name: Loopback888
# commands:
# - interface GigabitEthernet3
# - no standby 22 ip 192.168.0.2 secondary
# - interface GigabitEthernet4
# - no standby 0 priority 5
# after:
# - name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999

# After state:
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
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet4
#  description Auto_Cable_Testing_Ansible
#  no ip address
#  shutdown
#  negotiation auto

# Using gathered

# Before state:
# -------------
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

- name: Gather facts for hsrp interfaces
  cisco.ios.ios_hsrp_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
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
#         priority: 5
# - name: Loopback999
# - name: Loopback888

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_hsrp_interfaces:
    config:
      - name: GigabitEthernet3
        standby_groups:
          - group_no: 22
            ip:
              - virtual_ip: 192.168.0.2
                secondary: true
      - name: GigabitEthernet4
        standby_groups:
          - group_no: 0
            priority: 5
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface GigabitEthernet3
# - "standby 22 ip 10.0.0.1 secondary
# - interface GigabitEthernet4
# - standby 0 priority 5

# Using parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet3
#  standby 22 ip 10.0.0.1 secondary
# interface GigabitEthernet4
#  standby 0 priority 5

# - name: Parse the provided configuration
#   cisco.ios.ios_hsrp_interfaces:
#     running_config: "{{ lookup('file', 'parsed.cfg') }}"
#     state: parsed

# Task Output
# -----------
#
# parsed:
# - name: GigabitEthernet3
#    standby_groups:
#     - group_no: 22
#       ip:
#         - virtual_ip: 192.168.0.2
#           secondary: True
# - name: GigabitEthernet4
#    standby_groups:
#     - group_no: 0
#       priority: 5
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
