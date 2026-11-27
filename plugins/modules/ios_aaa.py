#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_aaa
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_aaa
short_description: Resource module to configure AAA.
description:
  - This module configures and manages the attributes of AAA on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of AAA configuration.
    type: dict
    suboptions:
      new_model:
        description:
          - Enable AAA (C(aaa new-model)). It is only changed when it is in the task.
        type: bool
      session_id:
        description: Session ID of the AAA sessions (C(aaa session-id)). It is only changed when it is in the task.
        type: str
        choices: ["common", "unique"]
      authentication:
        description: Authentication method lists (C(aaa authentication)).
        type: dict
        suboptions:
          login:
            description: Method lists of C(aaa authentication login).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          enable:
            description: Method lists of C(aaa authentication enable).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          dot1x:
            description: Method lists of C(aaa authentication dot1x).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
      authorization:
        description: Authorization method lists (C(aaa authorization)).
        type: dict
        suboptions:
          exec:
            description: Method lists of C(aaa authorization exec).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          network:
            description: Method lists of C(aaa authorization network).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          commands:
            description: Method lists of C(aaa authorization commands).
            type: list
            elements: dict
            suboptions:
              level:
                description: Privilege level the commands are authorized or accounted for (C(0) to C(15)).
                type: int
                required: true
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          config_commands:
            description: Authorize the configuration commands (C(aaa authorization config-commands)).
            type: bool
          console:
            description: Authorize the console (C(aaa authorization console)).
            type: bool
      accounting:
        description: Accounting method lists (C(aaa accounting)).
        type: dict
        suboptions:
          exec:
            description: Method lists of C(aaa accounting exec).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          system:
            description: Method lists of C(aaa accounting system).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          dot1x:
            description: Method lists of C(aaa accounting dot1x).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          network:
            description: Method lists of C(aaa accounting network).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          identity:
            description: Method lists of C(aaa accounting identity).
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
          commands:
            description: Method lists of C(aaa accounting commands).
            type: list
            elements: dict
            suboptions:
              level:
                description: Privilege level the commands are authorized or accounted for (C(0) to C(15)).
                type: int
                required: true
              name:
                description: Name of the method list, C(default) or a name.
                type: str
                required: true
              record:
                description: What is recorded, C(none) takes no methods. It is required unless the list is removed.
                type: str
                choices: ["start-stop", "stop-only", "none"]
              methods:
                description:
                  - The methods in the order they are tried, for example C(group ISE), C(local), C(enable) or C(if-authenticated).
                type: list
                elements: str
      group_servers:
        description: Server groups (C(aaa group server)).
        type: list
        elements: dict
        suboptions:
          type:
            description: Protocol of the group.
            type: str
            choices: ["radius", "tacacs+"]
            required: true
          name:
            description: Name of the group.
            type: str
            required: true
          servers:
            description: Names of the servers (C(server name)) in the order they are tried.
            type: list
            elements: str
          source_interface:
            description: Source interface of the group (C(ip radius source-interface) or C(ip tacacs source-interface)).
            type: str
          vrf:
            description: VRF of the group (C(ip vrf forwarding)).
            type: str
          deadtime:
            description: Minutes a server that does not answer is skipped (C(deadtime)).
            type: int
      dynamic_author:
        description: RADIUS dynamic authorization (C(aaa server radius dynamic-author)).
        type: dict
        suboptions:
          clients:
            description: The clients that may send change of authorization requests.
            type: list
            elements: dict
            suboptions:
              address:
                description: IP address or name of the client.
                type: str
                required: true
              vrf:
                description: VRF of the client.
                type: str
              server_key:
                description:
                  - The key shared with the client.
                  - The device keeps it encrypted, so a plain text key cannot be compared with it.
                    A key of type C(0) is sent when the client is new or has no key yet, a key of type C(6) or C(7)
                    (what I(gathered) returns) is compared.
                type: dict
                suboptions:
                  type:
                    description: Encryption type of the key, C(0) is plain text.
                    type: int
                    choices: [0, 6, 7]
                    default: 0
                  key:
                    description: The key.
                    type: str
                    required: true
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config all | section ^aaa|^no aaa new-model).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the lists, groups and clients of the task are added or replaced. Nothing else is touched.
      - With state I(replaced), the same, and the options of a group server are made to match the task exactly.
      - With state I(overridden), the lists of the sections that are in the task (for example C(authentication.login))
        and the group servers and clients are made to match the task exactly, the others are removed.
        Sections that are not in the task are left alone, so are I(new_model) and I(session_id).
      - With state I(deleted), the lists, groups and clients named in the task are removed. Without I(config)
        all of them are removed except the C(default) lists, which decide how the logins work and are only removed
        when the task names them. I(new_model) and I(session_id) are not changed.
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
# router#show running-config | section ^aaa
# aaa new-model
# aaa session-id common

- name: Add the method lists, a server group and a dynamic authorization client
  cisco.ios.ios_aaa:
    config:
      authentication:
        login:
          - name: ISE-LOGIN
            methods:
              - group ISE-TAC
              - local
        dot1x:
          - name: default
            methods:
              - group ISE-RAD
      authorization:
        exec:
          - name: ISE-EXEC
            methods:
              - group ISE-TAC
              - local
              - if-authenticated
        commands:
          - level: 15
            name: ISE-CMD
            methods:
              - group ISE-TAC
              - local
              - if-authenticated
      accounting:
        exec:
          - name: ISE-ACC
            record: start-stop
            methods:
              - group ISE-TAC
      group_servers:
        - type: radius
          name: ISE-RAD
          servers:
            - ISE-RAD-PRI
            - ISE-RAD-SEC
          source_interface: Loopback0
      dynamic_author:
        clients:
          - address: 192.0.2.10
            server_key:
              key: Secret123
    state: merged

# Task Output
# -----------
#
# commands:
#   - aaa authentication login ISE-LOGIN group ISE-TAC local
#   - aaa authentication dot1x default group ISE-RAD
#   - aaa authorization exec ISE-EXEC group ISE-TAC local if-authenticated
#   - aaa authorization commands 15 ISE-CMD group ISE-TAC local if-authenticated
#   - aaa accounting exec ISE-ACC start-stop group ISE-TAC
#   - aaa group server radius ISE-RAD
#   - server name ISE-RAD-PRI
#   - server name ISE-RAD-SEC
#   - ip radius source-interface loopback0
#   - aaa server radius dynamic-author
#   - client 192.0.2.10 server-key Secret123

# After state:
# ------------
#
# router#show running-config | section ^aaa
# aaa new-model
# aaa authentication login ISE-LOGIN group ISE-TAC local
# aaa authentication dot1x default group ISE-RAD
# aaa authorization exec ISE-EXEC group ISE-TAC local if-authenticated
# aaa authorization commands 15 ISE-CMD group ISE-TAC local if-authenticated
# aaa accounting exec ISE-ACC start-stop group ISE-TAC
# aaa group server radius ISE-RAD
#  server name ISE-RAD-PRI
#  server name ISE-RAD-SEC
#  ip radius source-interface Loopback0
# aaa server radius dynamic-author
#  client 192.0.2.10 server-key 6 <encrypted>
# aaa session-id common

# Using replaced

# Before state:
# -------------
#
# aaa group server radius ISE-RAD
#  server name ISE-RAD-PRI
#  server name ISE-RAD-SEC
#  ip radius source-interface Loopback0

- name: Replace the group server, the second server and the source interface go
  cisco.ios.ios_aaa:
    config:
      group_servers:
        - type: radius
          name: ISE-RAD
          servers:
            - ISE-RAD-PRI
    state: replaced

# Task Output
# -----------
#
# commands:
#   - aaa group server radius ISE-RAD
#   - no server name ISE-RAD-SEC
#   - no ip radius source-interface

# Using overridden

# Before state:
# -------------
#
# aaa authentication login ISE-LOGIN group ISE-TAC local
# aaa authentication login LOCAL-ONLY local

- name: Keep only the login list of the task
  cisco.ios.ios_aaa:
    config:
      authentication:
        login:
          - name: ISE-LOGIN
            methods:
              - group ISE-TAC
              - local
    state: overridden

# Task Output
# -----------
#
# commands:
#   - no aaa authentication login LOCAL-ONLY

# Using deleted

- name: Remove a method list and a group server
  cisco.ios.ios_aaa:
    config:
      authentication:
        login:
          - name: LOCAL-ONLY
      group_servers:
        - type: radius
          name: ISE-RAD
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no aaa authentication login LOCAL-ONLY
#   - no aaa group server radius ISE-RAD

# Using gathered

- name: Gather the AAA configuration
  cisco.ios.ios_aaa:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   new_model: true
#   session_id: common
#   authentication:
#     login:
#       - name: ISE-LOGIN
#         methods:
#           - group ISE-TAC
#           - local
#   group_servers:
#     - type: radius
#       name: ISE-RAD
#       servers:
#         - ISE-RAD-PRI

# Using rendered

- name: Render the AAA commands
  cisco.ios.ios_aaa:
    config:
      accounting:
        system:
          - name: default
            record: start-stop
            methods:
              - group ISE-TAC
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - aaa accounting system default start-stop group ISE-TAC

# Using parsed

- name: Parse the AAA configuration
  cisco.ios.ios_aaa:
    running_config: |
      aaa new-model
      aaa authentication login default group ISE-TAC local
      aaa session-id common
    state: parsed

# Task Output
# -----------
#
# parsed:
#   new_model: true
#   session_id: common
#   authentication:
#     login:
#       - name: default
#         methods:
#           - group ISE-TAC
#           - local
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
    - aaa authentication login ISE-LOGIN group ISE-TAC local
    - aaa group server radius ISE-RAD
    - server name ISE-RAD-PRI
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - aaa authentication login ISE-LOGIN group ISE-TAC local
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.aaa.aaa import (
    AaaArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.aaa.aaa import (
    Aaa,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=AaaArgs.argument_spec,
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

    result = Aaa(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
