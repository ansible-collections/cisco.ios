#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_radius_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_radius_global
short_description: Resource module to configure RADIUS.
description:
  - This module configures and manages the attributes of RADIUS servers and the global RADIUS settings on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - IOS accepts the C(radius server) and C(radius-server) commands only with C(aaa new-model) and rejects them as invalid input without it.
options:
  config:
    description: A dictionary of RADIUS configuration.
    type: dict
    suboptions:
      timeout:
        description: Seconds to wait for a reply of a server (C(radius-server timeout)). IOS uses 5 when it is not set.
        type: int
      retransmit:
        description: Number of times a request is sent again (C(radius-server retransmit)). IOS uses 3 when it is not set.
        type: int
      deadtime:
        description: Minutes a server that does not answer is skipped (C(radius-server deadtime)). IOS uses 0 when it is not set.
        type: int
      dead_criteria:
        description: When a server is considered dead (C(radius-server dead-criteria)). IOS uses a time of 10 and 10 tries when it is not set.
        type: dict
        suboptions:
          time:
            description: Seconds without a reply.
            type: int
          tries:
            description: Number of requests without a reply.
            type: int
      load_balance:
        description: Load balancing between the servers (C(radius-server load-balance)).
        type: dict
        suboptions:
          method:
            description: Method of the load balancing.
            type: str
            choices: ["least_outstanding"]
      source_interface:
        description: Source interface of the RADIUS packets (C(ip radius source-interface)).
        type: dict
        suboptions:
          name:
            description: Interface name.
            type: str
            required: true
          vrf:
            description: VRF of the interface.
            type: str
      attributes:
        description:
          - RADIUS attributes (C(radius-server attribute)).
          - The attributes that IOS sends by default, for example 77 with I(include_in_access_req) and
            I(include_in_acct_req), cannot be switched off with this module.
        type: list
        elements: dict
        suboptions:
          number:
            description: Attribute number.
            type: int
            required: true
          on_for_login_auth:
            description: Send the attribute for login authentication (C(on-for-login-auth)).
            type: bool
          access_request_include:
            description: Include the attribute in the access requests (C(access-request include)).
            type: bool
          include_in_access_req:
            description: Include the attribute in the access requests (C(include-in-access-req)).
            type: bool
          include_in_acct_req:
            description: Include the attribute in the accounting requests (C(include-in-acct-req)).
            type: bool
      servers:
        description: RADIUS servers (C(radius server)).
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the server.
            type: str
            required: true
          address:
            description:
              - Address of the server. It is required to create a server and cannot be removed.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 address or host name of the server (C(address ipv4)). Mutually exclusive with I(ipv6).
                type: str
              ipv6:
                description: IPv6 address or host name of the server (C(address ipv6)). Mutually exclusive with I(ipv4).
                type: str
              auth_port:
                description: Authentication port. IOS uses 1812 when it is not set.
                type: int
              acct_port:
                description: Accounting port. IOS uses 1813 when it is not set.
                type: int
          key:
            description:
              - Shared secret of the server (C(key)).
              - IOS stores the key encrypted and prints it as C(key 6 ...) or C(key 7 ...), which cannot be compared with a clear text key.
                A key of I(type=0) is therefore only sent when the server has no key, to change an existing key give it
                in the encrypted form of the running configuration (I(type=6) or I(type=7)).
            type: dict
            suboptions:
              type:
                description: How the key is written, C(0) for clear text, C(6) for an AES encrypted key and C(7) for a type 7 hash.
                type: int
                choices: [0, 6, 7]
                default: 0
              value:
                description: The key.
                type: str
                required: true
          timeout:
            description: Seconds to wait for a reply of this server (C(timeout)).
            type: int
          retransmit:
            description: Number of times a request to this server is sent again (C(retransmit)).
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^radius|^ip radius source-interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided configuration is added to the existing one.
      - With state I(replaced), the global options not in the task are set back to their defaults and every server named in
        the task is made to match exactly. Servers not named are left alone.
      - With state I(overridden), the device is made to match the task exactly, servers not named in the task are removed.
      - With state I(deleted), the servers named in the task are removed and the global options named in the task are set
        back to their defaults. Without any of them in the task everything is removed.
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
# router#show running-config | section ^radius|^ip radius source-interface
# router#

- name: Merge the RADIUS configuration
  cisco.ios.ios_radius_global:
    config:
      timeout: 4
      retransmit: 2
      deadtime: 5
      dead_criteria:
        time: 5
        tries: 3
      load_balance:
        method: least_outstanding
      source_interface:
        name: Vlan10
      attributes:
        - number: 6
          on_for_login_auth: true
        - number: 25
          access_request_include: true
        - number: 8
          include_in_access_req: true
      servers:
        - name: RADIUS-PRI
          address:
            ipv4: 192.0.2.10
            auth_port: 1812
            acct_port: 1813
          key:
            type: 0
            value: example-secret
          timeout: 3
    state: merged

# Task Output
# -----------
#
# commands:
#   - radius-server timeout 4
#   - radius-server retransmit 2
#   - radius-server deadtime 5
#   - radius-server dead-criteria time 5 tries 3
#   - radius-server load-balance method least-outstanding
#   - ip radius source-interface vlan10
#   - radius-server attribute 6 on-for-login-auth
#   - radius-server attribute 25 access-request include
#   - radius-server attribute 8 include-in-access-req
#   - radius server RADIUS-PRI
#   - address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
#   - key 0 example-secret
#   - timeout 3

# After state:
# ------------
#
# router#show running-config | section ^radius|^ip radius source-interface
# radius server RADIUS-PRI
#  address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
#  key 7 <encrypted key>
#  timeout 3
# radius-server attribute 6 on-for-login-auth
# radius-server attribute 8 include-in-access-req
# radius-server attribute 25 access-request include
# radius-server dead-criteria time 5 tries 3
# radius-server deadtime 5
# radius-server load-balance method least-outstanding
# radius-server retransmit 2
# radius-server timeout 4
# ip radius source-interface Vlan10

# Using replaced

# Before state:
# -------------
#
# radius server RADIUS-PRI
#  address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
#  key 7 <encrypted key>
#  timeout 3
#  retransmit 2

- name: Replace the server
  cisco.ios.ios_radius_global:
    config:
      servers:
        - name: RADIUS-PRI
          address:
            ipv4: 192.0.2.11
          timeout: 3
    state: replaced

# Task Output
# -----------
#
# commands:
#   - radius server RADIUS-PRI
#   - address ipv4 192.0.2.11 auth-port 1812 acct-port 1813
#   - no key
#   - no retransmit

# Using overridden

# Before state:
# -------------
#
# radius server RADIUS-PRI
#  address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
# radius server RADIUS-SEC
#  address ipv4 192.0.2.11 auth-port 1812 acct-port 1813

- name: Keep only the primary server
  cisco.ios.ios_radius_global:
    config:
      servers:
        - name: RADIUS-PRI
          address:
            ipv4: 192.0.2.10
    state: overridden

# Task Output
# -----------
#
# commands:
#   - no radius server RADIUS-SEC

# Using deleted

- name: Remove one server
  cisco.ios.ios_radius_global:
    config:
      servers:
        - name: RADIUS-SEC
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no radius server RADIUS-SEC

- name: Remove all servers and set the global options back to their defaults
  cisco.ios.ios_radius_global:
    state: deleted

# Using gathered

- name: Gather the RADIUS configuration
  cisco.ios.ios_radius_global:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   timeout: 4
#   attributes:
#     - number: 6
#       on_for_login_auth: true
#   servers:
#     - name: RADIUS-PRI
#       address:
#         ipv4: 192.0.2.10
#         auth_port: 1812
#         acct_port: 1813
#       key:
#         type: 7
#         value: <encrypted key>

# Using rendered

- name: Render the RADIUS commands
  cisco.ios.ios_radius_global:
    config:
      source_interface:
        name: Vlan10
        vrf: MGMT
      servers:
        - name: RADIUS-SEC
          address:
            ipv6: 2001:db8::10
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - ip radius source-interface vlan10 vrf MGMT
#   - radius server RADIUS-SEC
#   - address ipv6 2001:db8::10 auth-port 1812 acct-port 1813

# Using parsed

- name: Parse the RADIUS configuration
  cisco.ios.ios_radius_global:
    running_config: |
      radius server RADIUS-PRI
       address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
       timeout 3
      radius-server retransmit 2
    state: parsed

# Task Output
# -----------
#
# parsed:
#   retransmit: 2
#   servers:
#     - name: RADIUS-PRI
#       address:
#         ipv4: 192.0.2.10
#         auth_port: 1812
#         acct_port: 1813
#       timeout: 3
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
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
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - radius-server timeout 4
    - radius server RADIUS-PRI
    - address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - radius-server timeout 4
    - radius server RADIUS-PRI
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    emit_warnings,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.radius_global.radius_global import (
    Radius_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.radius_global.radius_global import (
    Radius_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Radius_globalArgs.argument_spec,
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

    result = Radius_global(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
