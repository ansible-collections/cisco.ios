#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_l3_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_l3_interfaces
short_description: Resource module to configure L3 interfaces.
description:
  - This module provides declarative management of Layer-3 interface on Cisco IOS devices.
version_added: 1.0.0
author:
  - Sagar Paul (@KB-perByte)
  - Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - Using deleted state without config will delete all l3 attributes from all the interfaces.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A dictionary of Layer-3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.
        type: str
        required: true
      ipv4:
        description:
          - IPv4 address to be set for the Layer-3 interface mentioned in I(name) option.
            The address format is <ipv4 address>/<mask>, the mask is number in range
            0-32 eg. 192.168.0.1/24.
        type: list
        elements: dict
        suboptions:
          address:
            description:
              - Configures the IPv4 address for Interface.
            type: str
          secondary:
            description:
              - Configures the IP address as a secondary address.
            type: bool
          dhcp_client:
            description:
              - Configures and specifies client-id to use over DHCP ip. Note, This option
                shall work only when dhcp is configured as IP.
              - GigabitEthernet interface number
              - This option is DEPRECATED and is replaced with dhcp which
                accepts dict as input this attribute will be removed after 2023-08-01.
            type: str
          dhcp_hostname:
            description:
              - Configures and specifies value for hostname option over DHCP ip. Note,
                This option shall work only when dhcp is configured as IP.
              - This option is DEPRECATED and is replaced with dhcp which
                accepts dict as input this attribute will be removed after 2023-08-01.
            type: str
          dhcp:
            description: IP Address negotiated via DHCP.
            type: dict
            suboptions:
              enable:
                description: Enable dhcp.
                type: bool
              client_id:
                description: Specify client-id to use.
                type: str
              hostname:
                description: Specify value for hostname option.
                type: str
          pool:
            description: IP Address auto-configured from a local DHCP pool.
            type: str
      ipv6:
        description:
          - IPv6 address to be set for the Layer-3 interface mentioned in I(name) option.
          - The address format is <ipv6 address>/<mask>, the mask is number in range
            0-128 eg. fd5d:12c9:2201:1::1/64
        type: list
        elements: dict
        suboptions:
          address:
            description:
              - Configures the IPv6 address for Interface.
            type: str
          autoconfig:
            description: Obtain address using auto-configuration.
            type: dict
            suboptions:
              enable:
                description: enable auto-configuration.
                type: bool
              default:
                description: Insert default route.
                type: bool
          dhcp:
            description: Obtain a ipv6 address using DHCP.
            type: dict
            suboptions:
              enable:
                description: Enable dhcp.
                type: bool
              rapid_commit:
                description: Enable Rapid-Commit.
                type: bool
          anycast:
            description: Configure as an anycast
            type: bool
          cga:
            description: Use CGA interface identifier
            type: bool
          eui:
            description: Use eui-64 interface identifier
            type: bool
          link_local:
            description: Use link-local address
            type: bool
          segment_routing:
            description: Segment Routing submode
            type: dict
            suboptions:
              enable:
                description: Enable segmented routing.
                type: bool
              default:
                description: Set a command to its defaults.
                type: bool
              ipv6_sr:
                description: Set ipv6_sr.
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^interface).
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
        option should be the same format as the output of command
        I(show running-config | section ^interface) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# Router#show running-config | section ^interface
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

- name: Merge provided configuration with device configuration
  cisco.ios.ios_l3_interfaces:
    config:
      - name: GigabitEthernet0/1
        ipv4:
          - address: 192.168.0.1/24
            secondary: true
      - name: GigabitEthernet2
        ipv4:
          - address: 192.168.0.2/24
      - name: GigabitEthernet3
        ipv6:
          - address: fd5d:12c9:2201:1::1/64
      - name: GigabitEthernet3.100
        ipv4:
          - address: 192.168.0.3/24
    state: merged

# Task Output
# -----------
#
# before:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet4
# - name: Loopback999
# commands:
# - interface GigabitEthernet2
# - ip address 192.168.0.2 255.255.255.0
# - interface GigabitEthernet3
# - ipv6 address fd5d:12c9:2201:1::1/64
# - interface GigabitEthernet3.100
# - ip address 192.168.0.3 255.255.255.0
# after:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.2/24
#   name: GigabitEthernet2
# - ipv6:
#   - address: FD5D:12C9:2201:1::1/64
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
#   ipv4:
#   - address: 192.168.0.3/24
# - name: GigabitEthernet4
# - name: Loopback999

# After state:
# ------------
#
# Router#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.2 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet3.100
#  ip address 192.168.0.3 255.255.255.0
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using replaced

# Before state:
# -------------
#
# Router#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.2 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_l3_interfaces:
    config:
      - name: GigabitEthernet2
        ipv4:
          - address: 192.168.2.0/24
      - name: GigabitEthernet3
        ipv4:
          - dhcp:
              client_id: GigabitEthernet2
              hostname: test.com
    state: replaced

# Task Output
# -----------
#
# before:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.2/24
#   name: GigabitEthernet2
# - ipv6:
#   - address: FD5D:12C9:2201:1::1/64
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999
# commands:
# - interface GigabitEthernet2
# - ip address 192.168.0.3 255.255.255.0
# - no ip address 192.168.0.2 255.255.255.0
# - interface GigabitEthernet3
# - ip address dhcp client-id GigabitEthernet2 hostname test.com
# - no ipv6 address fd5d:12c9:2201:1::1/64
# after:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.3/24
#   name: GigabitEthernet2
# - ipv4:
#   - dhcp:
#       client_id: GigabitEthernet2
#       enable: true
#       hostname: test.com
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999

# After state:
# ------------
#
# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.3 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  ip address dhcp client-id GigabitEthernet2 hostname test.com
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using overridden

# Before state:
# -------------
#
# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.3 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  ip address dhcp client-id GigabitEthernet2 hostname test.com
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_l3_interfaces:
    config:
      - ipv4:
          - dhcp:
              enable: true
        name: GigabitEthernet1
      - name: GigabitEthernet2
        ipv4:
          - address: 192.168.0.1/24
      - name: GigabitEthernet3
    state: overridden

# Task Output
# -----------
# before:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.3/24
#   name: GigabitEthernet2
# - ipv4:
#   - dhcp:
#       client_id: GigabitEthernet2
#       enable: true
#       hostname: test.com
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999
# commands:
# - interface GigabitEthernet2
# - ip address 192.168.0.1 255.255.255.0
# - no ip address 192.168.0.3 255.255.255.0
# - interface GigabitEthernet3
# - no ip address dhcp client-id GigabitEthernet2 hostname test.com
# after:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.1/24
#   name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999

# After state:
# ------------
#
# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using deleted

# Before state:
# -------------
#
# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: "Delete attributes of given interfaces (NOTE: This won't delete the interfaces)"
  cisco.ios.ios_l3_interfaces:
    config:
      - name: GigabitEthernet2
      - name: GigabitEthernet3.100
    state: deleted

# Task Output
# -----------
#
# before:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.1/24
#   name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999
# commands:
# - interface GigabitEthernet2
# - no ip address 192.168.0.1 255.255.255.0
# after:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - name: GigabitEthernet2
# - name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999

# After state:
# -------------
#
# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using deleted without config passed, only interface's configuration will be negated

# Before state:
# -------------

# router-ios#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.2 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: "Delete L3 config of all interfaces"
  cisco.ios.ios_l3_interfaces:
    state: deleted

# Task Output
# -----------
#
# before:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.2/24
#   name: GigabitEthernet2
# - ipv6:
#   - address: FD5D:12C9:2201:1::1/64
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999
# commands:
# - interface GigabitEthernet1
# - no ip address dhcp
# - interface GigabitEthernet2
# - no ip address 192.168.0.2 255.255.255.0
# - interface GigabitEthernet3
# - no ipv6 address fd5d:12c9:2201:1::1/64
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
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  negotiation auto
# interface GigabitEthernet2
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  no ip address
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

# Using gathered

# Before state:
# -------------
#
# Router#show running-config | section ^interface
# interface Loopback999
#  no ip address
#  shutdown
# interface GigabitEthernet1
#  description Management interface do not change
#  ip address dhcp
#  negotiation auto
# interface GigabitEthernet2
#  ip address 192.168.0.3 255.255.255.0
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3
#  description Configured and Overridden by Ansible Network
#  ip address dhcp client-id GigabitEthernet2 hostname test.com
#  shutdown
#  speed 1000
#  no negotiation auto
# interface GigabitEthernet3.100
# interface GigabitEthernet4
#  no ip address
#  shutdown
#  negotiation auto

- name: Gather facts for l3 interfaces
  cisco.ios.ios_l3_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
# - ipv4:
#   - dhcp:
#       enable: true
#   name: GigabitEthernet1
# - ipv4:
#   - address: 192.168.0.3/24
#   name: GigabitEthernet2
# - ipv4:
#   - dhcp:
#       client_id: GigabitEthernet2
#       enable: true
#       hostname: test.com
#   name: GigabitEthernet3
# - name: GigabitEthernet3.100
# - name: GigabitEthernet4
# - name: Loopback999

# Using rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_l3_interfaces:
    config:
      - name: GigabitEthernet1
        ipv4:
          - dhcp:
              client_id: GigabitEthernet0/0
              hostname: test.com
      - name: GigabitEthernet2
        ipv4:
          - address: 198.51.100.1/24
            secondary: true
          - address: 198.51.100.2/24
        ipv6:
          - address: 2001:db8:0:3::/64
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface GigabitEthernet1
# - ip address dhcp client-id GigabitEthernet0/0 hostname test.com
# - interface GigabitEthernet2
# - ip address 198.51.100.1 255.255.255.0 secondary
# - ip address 198.51.100.2 255.255.255.0
# - ipv6 address 2001:db8:0:3::/64

# Using parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
#  ip address dhcp client-id GigabitEthernet 0/0 hostname test.com
# interface GigabitEthernet0/2
#  ip address 198.51.100.1 255.255.255.0
#  ip address 198.51.100.2 255.255.255.0 secondary
#  ipv6 address 2001:db8:0:3::/64

- name: Parse the provided configuration
  cisco.ios.ios_l3_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
# - ipv4:
#   - dhcp:
#       client_id: GigabitEthernet0/0
#       hostname: test.com
#   name: GigabitEthernet0/1
# - ipv4:
#   - address: 198.51.100.1/24
#     secondary: true
#   - address: 198.51.100.2/24
#   ipv6:
#   - address: 2001:db8:0:3::/64
#   name: GigabitEthernet0/2

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
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
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
  type: list
  sample:
    - "ip address 192.168.0.3 255.255.255.0"
    - "ipv6 address dhcp rapid-commit"
    - "ipv6 address fd5d:12c9:2201:1::1/64 anycast"
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when state is I(rendered)
  type: list
  sample:
    - "ipv6 address FD5D:12C9:2201:1::1/64"
    - "ip address 192.168.0.3 255.255.255.0"
    - "ip address autoconfig"
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when state is I(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when state is I(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l3_interfaces.l3_interfaces import (
    L3_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L3_interfacesArgs.argument_spec,
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

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
