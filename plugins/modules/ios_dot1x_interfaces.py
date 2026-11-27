#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_dot1x_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_dot1x_interfaces
short_description: Resource module to configure 802.1X and MAB on interfaces.
description:
  - This module configures and manages the attributes of 802.1X and MAB port-based authentication on Cisco IOS interfaces.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A list of 802.1X and MAB configurations of interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description: Full name of the interface, for example C(GigabitEthernet1/0/1). C(Gi1/0/1) is accepted too.
        type: str
        required: true
      mab:
        description: Enable MAC authentication bypass (C(mab)).
        type: bool
      dot1x:
        description: 802.1X settings of the interface.
        type: dict
        suboptions:
          pae:
            description:
              - Port access entity type (C(dot1x pae)).
              - C(authenticator) together with I(authentication.port_control) C(auto) is the 802.1X/MAB core of an access port.
            type: str
            choices: ["authenticator", "supplicant", "both"]
          timeout:
            description: 802.1X timers.
            type: dict
            suboptions:
              tx_period:
                description: Seconds between the EAP identity requests (C(dot1x timeout tx-period)). The default is 30.
                type: int
          max_reauth_req:
            description: Number of EAP identity requests before the port is considered unresponsive (C(dot1x max-reauth-req)). The default is 2.
            type: int
      authentication:
        description: Authentication manager settings of the interface.
        type: dict
        suboptions:
          port_control:
            description: Port control of the interface (C(authentication port-control)). The default is C(force_authorized).
            type: str
            choices: ["auto", "force_authorized", "force_unauthorized"]
          periodic:
            description: Reauthenticate the sessions periodically (C(authentication periodic)).
            type: bool
          timer:
            description: Authentication timers.
            type: dict
            suboptions:
              reauthenticate:
                description: Interval of the reauthentication (C(authentication timer reauthenticate)).
                type: dict
                suboptions:
                  server:
                    description: Use the interval that the authentication server sends.
                    type: bool
                  seconds:
                    description: Interval in seconds. The default is 3600.
                    type: int
          violation:
            description: Action on a security violation (C(authentication violation)). The default is C(shutdown).
            type: str
            choices: ["protect", "replace", "restrict", "shutdown"]
          control_direction:
            description: Direction of the traffic that is blocked before the port is authorized (C(authentication control-direction)). The default is C(both).
            type: str
            choices: ["both", "in"]
          host_mode:
            description: Number of hosts and domains that are authenticated on the port (C(authentication host-mode)). The default is C(single_host).
            type: str
            choices: ["multi_auth", "multi_domain", "multi_host", "single_host"]
          order:
            description: Order of the authentication methods (C(authentication order)).
            type: list
            elements: str
            choices: ["dot1x", "mab", "webauth"]
          priority:
            description: Priority of the authentication methods (C(authentication priority)).
            type: list
            elements: str
            choices: ["dot1x", "mab", "webauth"]
          event:
            description: Actions on authentication events.
            type: dict
            suboptions:
              fail:
                description: Action when the authentication fails (C(authentication event fail)).
                type: dict
                suboptions:
                  retry:
                    description: Number of retries before the action is taken. The default is 2, IOS does not print it.
                    type: int
                  action:
                    description: C(authorize) puts the port in I(vlan), C(next_method) tries the next method.
                    type: str
                    choices: ["authorize", "next_method"]
                  vlan:
                    description: VLAN of the port with action C(authorize).
                    type: int
              no_response:
                description: Authorize the port in a VLAN when the host does not answer (C(authentication event no-response action authorize vlan)).
                type: dict
                suboptions:
                  vlan:
                    description: VLAN of the port.
                    type: int
              server_dead:
                description: Action when the authentication server is not reachable (C(authentication event server dead)).
                type: dict
                suboptions:
                  action:
                    description: Action to take.
                    type: str
                    choices: ["authorize", "reinitialize"]
                  vlan:
                    description: VLAN of the port.
                    type: int
                  voice:
                    description:
                      - Authorize the voice domain too (with action C(authorize)), it is a line of its own next to the one of I(vlan).
                      - The device prints it next to I(vlan) by itself. When it is not in the task it is left alone, C(false) removes it.
                    type: bool
              server_alive:
                description: Action when the authentication server is reachable again (C(authentication event server alive)).
                type: dict
                suboptions:
                  action:
                    description: Action to take.
                    type: str
                    choices: ["reinitialize"]
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
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided options are added to the existing ones. Nothing is removed.
      - With state I(replaced), the interfaces named in the task are made to match exactly, options
        not in the task are removed. Interfaces not named are left alone.
      - With state I(overridden), the device is made to match the task exactly, the 802.1X and MAB
        options of interfaces not named in the task are removed.
      - With state I(deleted), the 802.1X and MAB options of the interfaces named in the task are removed.
        Without I(config) the options of all interfaces are removed.
      - With state I(gathered), the configuration is read from the device and returned in I(gathered).
        Interfaces without 802.1X or MAB options are not returned.
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
# router#show running-config | section ^interface GigabitEthernet1/0/1
# interface GigabitEthernet1/0/1
#  switchport access vlan 10
#  switchport mode access

- name: Configure 802.1X and MAB on an access port
  cisco.ios.ios_dot1x_interfaces:
    config:
      - name: GigabitEthernet1/0/1
        mab: true
        dot1x:
          pae: authenticator
          timeout:
            tx_period: 7
        authentication:
          port_control: auto
          periodic: true
          timer:
            reauthenticate:
              server: true
          violation: restrict
          control_direction: in
          event:
            fail:
              retry: 3
              action: authorize
              vlan: 999
            server_dead:
              action: authorize
              vlan: 20
            server_alive:
              action: reinitialize
    state: merged

# Task Output
# -----------
#
# commands:
#   - interface GigabitEthernet1/0/1
#   - authentication port-control auto
#   - authentication periodic
#   - authentication timer reauthenticate server
#   - authentication violation restrict
#   - authentication control-direction in
#   - authentication event fail retry 3 action authorize vlan 999
#   - authentication event server dead action authorize vlan 20
#   - authentication event server alive action reinitialize
#   - mab
#   - dot1x pae authenticator
#   - dot1x timeout tx-period 7

# After state:
# ------------
#
# router#show running-config | section ^interface GigabitEthernet1/0/1
# interface GigabitEthernet1/0/1
#  switchport access vlan 10
#  switchport mode access
#  authentication control-direction in
#  authentication event fail retry 3 action authorize vlan 999
#  authentication event server dead action authorize vlan 20
#  authentication event server dead action authorize voice
#  authentication event server alive action reinitialize
#  authentication port-control auto
#  authentication periodic
#  authentication timer reauthenticate server
#  authentication violation restrict
#  mab
#  dot1x pae authenticator
#  dot1x timeout tx-period 7

# Using replaced

# Before state:
# -------------
#
# interface GigabitEthernet1/0/1
#  authentication port-control auto
#  authentication periodic
#  authentication violation restrict
#  mab
#  dot1x pae authenticator

- name: Replace the options of an interface
  cisco.ios.ios_dot1x_interfaces:
    config:
      - name: GigabitEthernet1/0/1
        mab: true
        dot1x:
          pae: authenticator
        authentication:
          port_control: auto
          host_mode: multi_auth
    state: replaced

# Task Output
# -----------
#
# commands:
#   - interface GigabitEthernet1/0/1
#   - no authentication periodic
#   - no authentication violation restrict
#   - authentication host-mode multi-auth

# Using overridden

- name: Override the options of all interfaces
  cisco.ios.ios_dot1x_interfaces:
    config:
      - name: GigabitEthernet1/0/1
        mab: true
        dot1x:
          pae: authenticator
        authentication:
          port_control: auto
    state: overridden

# Using deleted

- name: Remove the options of one interface
  cisco.ios.ios_dot1x_interfaces:
    config:
      - name: GigabitEthernet1/0/1
    state: deleted

- name: Remove the options of all interfaces
  cisco.ios.ios_dot1x_interfaces:
    state: deleted

# Using gathered

- name: Gather the 802.1X and MAB options
  cisco.ios.ios_dot1x_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   - name: GigabitEthernet1/0/1
#     mab: true
#     dot1x:
#       pae: authenticator
#     authentication:
#       port_control: auto
#       periodic: true

# Using rendered

- name: Render the commands
  cisco.ios.ios_dot1x_interfaces:
    config:
      - name: GigabitEthernet1/0/2
        mab: true
        authentication:
          order:
            - mab
            - dot1x
          priority:
            - mab
            - dot1x
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - interface GigabitEthernet1/0/2
#   - authentication order mab dot1x
#   - authentication priority mab dot1x
#   - mab

# Using parsed

- name: Parse the options
  cisco.ios.ios_dot1x_interfaces:
    running_config: |
      interface GigabitEthernet1/0/1
       authentication port-control auto
       mab
       dot1x pae authenticator
    state: parsed

# Task Output
# -----------
#
# parsed:
#   - name: GigabitEthernet1/0/1
#     mab: true
#     dot1x:
#       pae: authenticator
#     authentication:
#       port_control: auto
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
    - interface GigabitEthernet1/0/1
    - authentication port-control auto
    - mab
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet1/0/1
    - authentication port-control auto
    - mab
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.dot1x_interfaces.dot1x_interfaces import (
    Dot1x_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.dot1x_interfaces.dot1x_interfaces import (
    Dot1x_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Dot1x_interfacesArgs.argument_spec,
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

    result = Dot1x_interfaces(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
