#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bfd_interfaces
short_description: Resource module to configure bfd in interfaces.
description: This module manages the bfd configuration in interface of Cisco IOS network devices.
version_added: 11.3.0
author:
  - Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSXE Version 17.3 on CML.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples uses callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A list of interface options, to configure bfd.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of interface, e.g. GigabitEthernet0/2, loopback999.
          - Short interface names like Gi0/2, Lo999 may impact idempotency.
        type: str
        required: true
      echo:
        description:
          - Use echo adjunct as bfd detection mechanism.
        type: bool
      bfd:
        description:
          - Enable or disable bfd for the interface.
          - Default value for appliance might impact idempotency.
        type: bool
      template:
        description:
          - BFD template (might impact other BFD configuration),
          - Ansible won't guarantee state operations.
        type: str
      local_address:
        description:
          - BFD local address.
        type: str
      jitter:
        description:
          - Enable BFD interval transmit jittering.
        type: bool
      interval:
        description:
          - Transmit interval between BFD packets
        type: dict
        suboptions:
          input:
            description:
              - Interval between transmitted BFD control packets 50 - 9999 Milliseconds
            type: int
          min_rx:
            description:
              - Minimum receive interval capability 50 - 9999 Milliseconds
            type: int
          multiplier:
            description:
              - Detection multiplier 3 - 50
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
        | section interface) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
    type: str
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
    - interface GigabitEthernet0/2
    - bfd echo
    - bfd interval 100 min_rx 100 multiplier 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet0/2
    - bfd echo
    - bfd jitter
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_interfaces.bfd_interfaces import (
    Bfd_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bfd_interfaces.bfd_interfaces import (
    Bfd_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_interfacesArgs.argument_spec,
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

    result = Bfd_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
