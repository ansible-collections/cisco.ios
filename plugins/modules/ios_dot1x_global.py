#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_dot1x_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_dot1x_global
short_description: Resource module to configure 802.1X global options.
description:
  - This module configures and manages the attributes of the global 802.1X (dot1x) options on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of the global 802.1X options.
    type: dict
    suboptions:
      system_auth_control:
        description:
          - Enable 802.1X on the device (C(dot1x system-auth-control)).
          - No port authenticates until it is on. It is off by default.
        type: bool
      critical_eapol:
        description:
          - Send an EAPOL-Success when a host is authorized by the critical authentication (C(dot1x critical eapol)).
          - It is off by default.
        type: bool
      auth_fail_eapol:
        description:
          - Send an EAPOL-Success when a host is moved to the auth-fail VLAN (C(dot1x auth-fail eapol)).
          - It is off by default.
        type: bool
      authentication:
        description: The global C(authentication) options.
        type: dict
        suboptions:
          mac_move:
            description: Whether a MAC address may move from a port to another one. The two options are independent, both are off by default.
            type: dict
            suboptions:
              permit:
                description: Allow a MAC address to move between ports (C(authentication mac-move permit)).
                type: bool
              deny_uncontrolled:
                description: Deny the move of a MAC address to a port that is not controlled by 802.1X (C(authentication mac-move deny-uncontrolled)).
                type: bool
          critical_recovery_delay:
            description:
              - Milliseconds between the reinitialization of the hosts of a port that comes back from the critical state
                (C(authentication critical recovery delay)).
              - It is 100 by default.
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config all | include ^dot1x|^authentication).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the options of the task are added to the existing ones.
      - With state I(replaced) and I(overridden), the options that are not in the task go back to their default,
        for example C(dot1x system-auth-control) is removed.
      - With state I(deleted), all the options go back to their default.
      - With state I(gathered), the configuration is read from the device and returned in I(gathered).
        The values that IOS prints with C(show running-config all), the defaults, are included.
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
# router#show running-config all | include ^dot1x|^authentication
# authentication mac-move deny
# authentication critical recovery delay 100

- name: Merge the global 802.1X options
  cisco.ios.ios_dot1x_global:
    config:
      critical_eapol: true
      authentication:
        mac_move:
          permit: true
        critical_recovery_delay: 1000
      system_auth_control: true
    state: merged

# Task Output
# -----------
#
# commands:
#   - dot1x critical eapol
#   - authentication mac-move permit
#   - authentication critical recovery delay 1000
#   - dot1x system-auth-control

# After state:
# ------------
#
# router#show running-config all | include ^dot1x|^authentication
# dot1x system-auth-control
# dot1x critical eapol
# authentication mac-move permit
# authentication critical recovery delay 1000

# Using replaced

# Before state:
# -------------
#
# dot1x system-auth-control
# dot1x critical eapol
# authentication mac-move permit
# authentication critical recovery delay 1000

- name: Replace the global 802.1X options
  cisco.ios.ios_dot1x_global:
    config:
      critical_eapol: true
    state: replaced

# Task Output
# -----------
#
# commands:
#   - no authentication mac-move permit
#   - authentication critical recovery delay 100
#   - no dot1x system-auth-control

# Using deleted

# Before state:
# -------------
#
# dot1x system-auth-control
# dot1x critical eapol
# authentication mac-move permit
# authentication critical recovery delay 100

- name: Reset the global 802.1X options
  cisco.ios.ios_dot1x_global:
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no dot1x critical eapol
#   - no authentication mac-move permit
#   - no dot1x system-auth-control

# Using gathered

- name: Gather the global 802.1X options
  cisco.ios.ios_dot1x_global:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   system_auth_control: true
#   critical_eapol: true
#   authentication:
#     mac_move:
#       permit: true
#     critical_recovery_delay: 1000

# Using rendered

- name: Render the commands
  cisco.ios.ios_dot1x_global:
    config:
      system_auth_control: true
      critical_eapol: true
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - dot1x critical eapol
#   - dot1x system-auth-control

# Using parsed

- name: Parse the global 802.1X options
  cisco.ios.ios_dot1x_global:
    running_config: |
      dot1x system-auth-control
      dot1x critical eapol
      authentication mac-move permit
    state: parsed

# Task Output
# -----------
#
# parsed:
#   system_auth_control: true
#   critical_eapol: true
#   authentication:
#     mac_move:
#       permit: true
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
    - dot1x critical eapol
    - authentication mac-move permit
    - dot1x system-auth-control
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - dot1x critical eapol
    - dot1x system-auth-control
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.dot1x_global.dot1x_global import (
    Dot1x_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.dot1x_global.dot1x_global import (
    Dot1x_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Dot1x_globalArgs.argument_spec,
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

    result = Dot1x_global(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
