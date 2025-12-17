#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_templates
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bfd_templates
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Bidirectional Forwarding Detection (BFD) templates configurations
description:
   - Manages Bidirectional Forwarding Detection (BFD) templates configurations
version_added: 1.0.0
author:
  - Komal Desai (@komaldesai13)
notes:
  - Tested against Cisco IOS XE Software, Version 17.13.01a on CML
  - This module works with connection C(network_cli)
options:
  config:
    description: A dictionary of bfd template options
    type: list
    elements: dict
    suboptions:
      name:
        description: name of the BFD template to be used
        required: true
        type: str
      hop:
        description: type of template to be used
        required: true
        choices:
          - single-hop
          - multi-hop
        type: str
      interval:
        description: defines transmit interval between BFD packets
        required: false
        type: dict
        suboptions:
          min_tx:
            description: The minimum interval in milliseconds that the local system desires for transmitting BFD control packets
            required: true
            type: int
          min_rx:
            description: The minimum interval in milliseconds that the local system is capable of supporting between received BFD control packets
            required: true
            type: int
          multiplier:
            description: Specifies the number of consecutive BFD control packets that must be missed from a BFD peer before BFD declares that the peer is unavailable and the Layer 3 BFD peer is informed of the failure.
            required: true
            type: int
      dampening:
        description: enables session dampening
        required: false
        type: dict
        suboptions:
          half_life_period:
            description: half-life period for the exponential decay algorithm, in minutes.
            required: true
            type: int
          reuse_threshold:
            description: The threshold at which a dampened session is allowed to be reused (taken out of dampening), in milliseconds.
            required: true
            type: int
          suppress_threshold:
            description: The threshold at which a session is suppressed (put into dampening), in milliseconds.
            required: true
            type: int
          max_suppress_time:
            description: The maximum amount of time a session can be suppressed, in minutes.
            required: true
            type: int
      echo:
        description: enables the BFD echo function for all interfaces which uses thsis specific template.
        required: false
        type : bool
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
        | include bfd-template ) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
    type: str
"""

EXAMPLES = """

"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.argspec.bfd_templates.bfd_templates import (
    Bfd_templatesArgs,
)
from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.config.bfd_templates.bfd_templates import (
    Bfd_templates,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_templatesArgs.argument_spec,
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

    result = Bfd_templates(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
