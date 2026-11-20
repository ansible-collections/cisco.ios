#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_tunnel_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_tunnel_interfaces
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Resource module to configure tunnel interface parameters.
description:
  - This module configures and manages the tunnel specific parameters (C(tunnel source), C(tunnel destination),
    C(tunnel key), C(tunnel vrf) and so on) of tunnel interfaces on Cisco IOS devices.
  - The other settings of a tunnel interface are managed by the modules that already own them, C(ios_interfaces)
    for the description, C(ios_vrf_interfaces) for C(vrf forwarding) and C(ios_l3_interfaces) for the IP address, MTU,
    TCP MSS and redirects.
  - Supported parameters are I(source), I(destination), I(mode) (C(gre ip), C(gre ipv6) and C(gre multipoint)), I(key), I(tunnel_vrf),
    I(ttl), I(checksum) and I(path_mtu_discovery). Others, for example C(tunnel keepalive) and C(tunnel protection), are not covered yet.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
  - IOS does not print the defaults C(tunnel mode gre ip) and C(tunnel ttl 255). The module treats a tunnel without them as
    I(mode=gre_ip) and I(ttl=255), so setting the defaults explicitly is idempotent.
  - IOS refuses C(tunnel mode gre multipoint) while a C(tunnel destination) is configured, and the error is not seen by the
    connection plugin. The module removes the destination before switching to I(gre_multipoint), sets the mode before the
    destination when leaving it, and fails when a task sets I(destination) together with I(mode=gre_multipoint).
  - The tunnel interface itself is not removed by this module. State I(deleted) removes the tunnel parameters only,
    use C(ios_interfaces) with state I(purged) to remove the interface.
options:
  config:
    description: A list of tunnel interface configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description: Full name of the tunnel interface, for example C(Tunnel1501). C(Tu1501) is accepted too.
        type: str
        required: true
      source:
        description: Source of the tunnel, an interface name or an IP address (C(tunnel source)).
        type: str
      destination:
        description: Destination of the tunnel, an IPv4 or IPv6 address (C(tunnel destination)).
        type: str
      mode:
        description:
          - Encapsulation of the tunnel (C(tunnel mode)).
          - C(gre_ip) is the default of IOS and is not printed in the running configuration.
        type: str
        choices: ["gre_ip", "gre_ipv6", "gre_multipoint"]
      key:
        description: GRE key of the tunnel (C(tunnel key)).
        type: int
      tunnel_vrf:
        description:
          - VRF used to reach the tunnel destination, also called the front-door VRF (C(tunnel vrf)).
          - This is not the VRF of the tunnel interface itself (C(vrf forwarding)), that one is managed by C(ios_vrf_interfaces).
        type: str
      ttl:
        description: TTL of the tunnel packets (C(tunnel ttl)). 255 is the default of IOS and is not printed.
        type: int
      checksum:
        description: Enable GRE checksums (C(tunnel checksum)).
        type: bool
      path_mtu_discovery:
        description: Enable path MTU discovery on the tunnel (C(tunnel path-mtu-discovery)).
        type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^interface Tunnel).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided parameters are added to the existing ones. Nothing is removed.
      - With state I(replaced), the tunnel interfaces named in the task are made to match exactly, parameters
        not in the task are removed. Tunnel interfaces not named are left alone.
      - With state I(overridden), the device is made to match the task exactly, the parameters of tunnel
        interfaces not named in the task are removed.
      - With state I(deleted), the tunnel parameters of the interfaces named in the task are removed. Without
        I(config) the parameters of all tunnel interfaces are removed.
      - With state I(gathered), the configuration is read from the device and returned in I(gathered).
      - With state I(rendered), the task configuration is returned as device commands in I(rendered)
        without connecting to the device.
      - With state I(parsed), I(running_config) is returned as structured data in I(parsed).
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
# Using merged

# Before state:
# -------------
#
# router#show running-config | section ^interface Tunnel
# router#

- name: Configure the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1501
        source: Loopback499
        destination: 198.51.100.101
        key: 1501
        tunnel_vrf: MGMT
    state: merged

# Task Output
# -----------
#
# commands:
#   - interface Tunnel1501
#   - tunnel source loopback499
#   - tunnel destination 198.51.100.101
#   - tunnel key 1501
#   - tunnel vrf MGMT

# After state:
# ------------
#
# router#show running-config | section ^interface Tunnel
# interface Tunnel1501
#  tunnel source Loopback499
#  tunnel destination 198.51.100.101
#  tunnel key 1501
#  tunnel vrf MGMT

# A complete tunnel interface is built by the modules that own each part

- name: Create the tunnel interface, its description and VRF
  cisco.ios.ios_interfaces:
    config:
      - name: Tunnel1501
        description: "Tunnel to the remote site"
    state: merged

- name: Put the tunnel interface in a VRF
  cisco.ios.ios_vrf_interfaces:
    config:
      - name: Tunnel1501
        vrf_name: CUSTOMER
    state: merged

- name: Address and tune the tunnel interface
  cisco.ios.ios_l3_interfaces:
    config:
      - name: Tunnel1501
        ipv4:
          - address: 192.0.2.82/30
            mtu: 1400
        redirects: false
        tcp_adjust_mss: 1360
        ipv6_redirects: false
        ipv6_unreachables: false
    state: merged

- name: Configure the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1501
        source: Loopback499
        destination: 198.51.100.101
        key: 1501
        tunnel_vrf: MGMT
    state: merged

# router#show running-config interface Tunnel1501
# interface Tunnel1501
#  description Tunnel to the remote site
#  vrf forwarding CUSTOMER
#  ip address 192.0.2.82 255.255.255.252
#  no ip redirects
#  ip mtu 1400
#  ip tcp adjust-mss 1360
#  no ipv6 redirects
#  no ipv6 unreachables
#  tunnel source Loopback499
#  tunnel destination 198.51.100.101
#  tunnel key 1501
#  tunnel vrf MGMT

# Using replaced

# Before state:
# -------------
#
# interface Tunnel1501
#  tunnel source Loopback499
#  tunnel destination 198.51.100.101
#  tunnel key 1501
#  tunnel vrf MGMT

- name: Replace the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1501
        source: Loopback499
        destination: 198.51.100.102
        ttl: 64
    state: replaced

# Task Output
# -----------
#
# commands:
#   - interface Tunnel1501
#   - tunnel destination 198.51.100.102
#   - no tunnel key
#   - no tunnel vrf MGMT
#   - tunnel ttl 64

# Using overridden

# Before state:
# -------------
#
# interface Tunnel1501
#  tunnel source Loopback499
#  tunnel destination 198.51.100.101
# interface Tunnel1502
#  tunnel source Loopback499
#  tunnel destination 198.51.100.102

- name: Override the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1501
        source: Loopback499
        destination: 198.51.100.101
    state: overridden

# Task Output
# -----------
#
# commands:
#   - interface Tunnel1502
#   - no tunnel source
#   - no tunnel destination

# Using deleted

- name: Remove the tunnel parameters of one interface
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1501
    state: deleted

- name: Remove the tunnel parameters of all tunnel interfaces
  cisco.ios.ios_tunnel_interfaces:
    state: deleted

# Using gathered

- name: Gather the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   - name: Tunnel1501
#     source: Loopback499
#     destination: 198.51.100.101
#     key: 1501
#     tunnel_vrf: MGMT

# Using rendered

- name: Render the tunnel commands
  cisco.ios.ios_tunnel_interfaces:
    config:
      - name: Tunnel1502
        mode: gre_multipoint
        source: Loopback499
        key: 7
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - interface Tunnel1502
#   - tunnel mode gre multipoint
#   - tunnel source loopback499
#   - tunnel key 7

# Using parsed

- name: Parse the tunnel parameters
  cisco.ios.ios_tunnel_interfaces:
    running_config: |
      interface Tunnel1501
       tunnel source Loopback499
       tunnel destination 198.51.100.101
       tunnel key 1501
    state: parsed

# Task Output
# -----------
#
# parsed:
#   - name: Tunnel1501
#     source: Loopback499
#     destination: 198.51.100.101
#     key: 1501
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
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
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - interface Tunnel1501
    - tunnel source loopback499
    - tunnel destination 198.51.100.101
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface Tunnel1501
    - tunnel source loopback499
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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    emit_warnings,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.tunnel_interfaces.tunnel_interfaces import (
    Tunnel_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.tunnel_interfaces.tunnel_interfaces import (
    Tunnel_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Tunnel_interfacesArgs.argument_spec,
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

    result = Tunnel_interfaces(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
