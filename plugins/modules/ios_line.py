#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_line
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
---
module: ios_line
short_description: Resource module to configure line
description:
  - This module provides declarative management of the lines I(console), I(vty)
version_added: 5.0.0
author:
  - Ambroise Rosset (@earendilfr)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
options:
  config:
    description: The provided configurations.
    type: dict
    suboptions:
      lines:
        description: Configuration for each lines
        type: list
        elements: dict
        suboptions:
          access_classes_in:
            description: ID of the access-list used to filter inbound connections
            type: str
          access_classes_out:
            description: ID of the access-list used to filter outbound connections
            type: str
          accounting:
            description: Accounting parameters
            type: dict
            suboptions:
              arap:
                description:
                  - For Appletalk Remote Access Protocol
                  - Use an accounting list with this name
                  - I(default) is the default name
                type: str
                default: default
              commands:
                description:
                  - For exec (shell) commands
                type: list
                elements: dict
                suboptions:
                  level:
                    description:
                      - Enable level
                    type: int
                  command:
                    description:
                      - Use an accounting list with this name
                      - I(default) is the default name
                    type: str
                    default: default
              connection:
                description:
                  - For connection accounting
                  - Use an accounting list with this name
                  - I(default) is the default name
                type: str
                default: default
              exec:
                description:
                  - For starting an exec (shell)
                  - Use an accounting list with this name
                  - I(default) is the default name
                type: str
                default: default
              resource:
                description:
                  - For resource accounting
                  - Use an accounting list with this name
                  - I(default) is the default name
                type: str
                default: default
          authorization:
            description: Authorization parameters
            type: dict
            suboptions:
              arap:
                description:
                  - For Appletalk Remote Access Protocol
                  - Use an authorization list with this name
                  - I(default) is the default name
                type: str
                default: default
              commands:
                description:
                  - For exec (shell) commands
                type: list
                elements: dict
                suboptions:
                  level:
                    description:
                      - Enable level
                    type: int
                  command:
                    description:
                      - Use an authorization list with this name
                      - I(default) is the default name
                    type: str
                    default: default
              exec:
                description:
                  - For starting an exec (shell)
                  - Use an authorization list with this name
                  - I(default) is the default name
                type: str
                default: default
              reverse_access:
                description:
                  - For reverse telnet connections
                  - Use an authorization list with this name
                  - I(default) is the default name
                type: str
                default: default
          escape_character:
            description: Change the current line's escape character
            type: dict
            suboptions:
              soft:
                description: Set the soft escape character for this line
                type: bool
              value:
                description:
                  - Escape character configured
                  - I(BREAK) - Cause escape on BREAK
                  - I(DEFAULT) - Use default escape character
                  - I(NONE) - Disable escape entirely
                  - I(CHAR) or I(<0-255>) - Escape character or its ASCII decimal equivalent
                type: str
          exec:
            description: Configure EXEC
            type: dict
            suboptions:
              banner:
                description: Enable the display of the EXEC banner
                type: bool
              character_bits:
                description: Size of characters to the command exec
                type: int
                choices:
                  - 7
                  - 8
              prompt:
                description: EXEC prompt
                type: dict
                suboptions:
                  expand:
                    description: Prints expanded command for show commands
                    type: bool
                  timestamp:
                    description: Print timestamps for show commands
                    type: bool
              timeout:
                description:
                  - Timeout in minutes (Value between C(<0-35791>))
                type: int
          length:
            description:
              - Set number of lines on a screen (Value between C(<0-512>))
              - C(0) for no pausing
            type: int
          location:
            description:
              - Enter terminal location description
            type: str
          logging:
            description: Modify message logging facilities for synchronous
            type: dict
            suboptions:
              enable:
                description: Enable logging synchronous
                type: bool
              level:
                description: Severity level to output asynchronously
                type: str
                choices: [ '0', '1', '2', '3', '4', '5', '6', '7', 'all']
              limit:
                description:
                  - Messages queue size (Value between C(<0-2147483647>))
                type: int
          login:
            description:
              - Enable password checking for authentication
              - Use an authentication list with this name
              - I(default) is the default name
            type: str
            default: default
          logout_warning:
            description:
              - Set Warning countdown for absolute timeout of line
              - (Value between C(<0-4294967295>))
            type: int
          motd:
            description: Enable the display of the MOTD banner
            type: bool
            default: true
          name:
            description:
              - Define the type of line to configure
              - Should be the same form than C(line ....) indicated in the cisco running configuration
              - By example, I(con 0) or I(vty 0 4)
            type: str
            required: true
          notify:
            description: Inform users of output from concurrent sessions
            type: bool
          padding:
            description: Set padding for a specified output character
            type: str
          parity:
            description: Set terminal parity
            type: str
            choices:
              - even
              - mark
              - none
              - odd
              - space
          password:
            description: Password to connect to the line
            type: dict
            suboptions:
              hash:
                description:
                  - I(0) - Specifies an UNENCRYPTED password will follow
                  - I(7) - Specifies a HIDDEN password will follow
                type: int
                choices: [0, 7]
              value:
                description: The actual hashed password to be configured
                type: str
          privilege:
            description:
              - Change privilege level for line
              - The I(privilege) valu should be between C(0) and C(15)
            type: int
            choices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 13, 14, 15]
          session:
            description: Configure for session
            type: dict
            suboptions:
              disconnect_warning:
                description: Set warning countdown for session-timeout (Between C(<0-4294967295>))
                type: int
              limit:
                description: Set maximum number of sessions (Between C(<0-4294967295>))
                type: int
              timeout:
                description:
                  - Set interval for closing connection when there is no input traffic
                  - (Between C(<0-35791>))
                type: int
          speed:
            description: Set the transmit and receive speeds (Between C(<0-4294967295>))
            type: int
          stopbits:
            description:
              - Set async line stop bits
              - I(1) - One stop bit
              - I(1.5) - One and one-half stop bits
              - I(2) - Two stop bits
            type: str
            choices: ['1', '1.5', '2']
          transport:
            description: Define transport protocols for line
            type: list
            elements: dict
            suboptions:
              all:
                description:
                  - All protocols are allowed
                  - Not used if I(name) is configured at I(preferred)
                type: bool
              name:
                description:
                  - Type of transport to configure
                  - I(input) - Configure incomming connections
                  - I(output) - Configure outgoing connections
                  - I(preferred) - Configure preferred protocol to use
                type: str
                choices:
                  - input
                  - output
                  - preferred
              none:
                description: No protocols are allowed
                type: bool
              pad:
                description: Allow X.3 PAD
                type: bool
              rlogin:
                description: Allow Unix rlogin protocol
                type: bool
              ssh:
                description: Allow TCP/IP SSH protocol
                type: bool
              telnet:
                description: Allow TCP/IP Telnet protocol
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show lacp sys-id).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
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
        | sec ^line) executed on device. For state I(parsed) active connection to
        remote host is not required.
    type: str
    choices:
      - merged
      - overridden
      - deleted
      - rendered
      - parsed
      - gathered
    default: merged
"""

EXAMPLES = """

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
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.line.line import (
    LineArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.line.line import Line


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=LineArgs.argument_spec,
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

    result = Line(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
