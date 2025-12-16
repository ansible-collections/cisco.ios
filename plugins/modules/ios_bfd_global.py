#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_bfd_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_bfd_global
extends_documentation_fragment:
  - cisco.ios.ios
short_description: Bidirectional Forwarding Detection (BFD) global-level configuration
description:
   - Manages Bidirectional Forwarding Detection (BFD) global-level configuration.
version_added: 1.0.0
author:
  - Komal Desai (@komaldesai13)
notes:
  - Tested against Cisco IOS XE Software, Version 17.13.01a on CML
  - This module works with connection C(network_cli)
options:
  slow_timer:
    description:
      - Configures slow timers used by BFD , Value in ms to use for slow timers  <1000-30000>
    required: false
    type: int
  l2cos:
    description:
      - Configures L2 COS value to be used for BFD packets over VLAN interfaces <0-7>
    required: false
    type: int
  bfd_template:
    description: creates a reusable template that defines a set of Bidirectional Forwarding Detection (BFD) session parameters
    required: false
    type: dict
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
      config:
        description: bfd template configuration
        required: false
        type: dict
        suboptions:
          interval:
            description: defines transmit interval between BFD packets
            required: false
            type: dict
            suboptions:
              min-tx:
                description: The minimum interval in milliseconds that the local system desires for transmitting BFD control packets
                required: true
                type: int
              min-rx:
                description: The minimum interval in milliseconds that the local system is capable of supporting between received BFD control packets
                required: true
                type: int
              multiplier:
                description: The minimum interval in milliseconds that the local system is capable of supporting between received BFD control packets
                required: true
                type: int
          dampening:
            description: enables session dampening
            required: false
            type: dict
            suboptions:
              half-life-period:
                description: half-life period for the exponential decay algorithm, in minutes.
                required: true
                type: int
              reuse-threshold:
                description: The threshold at which a dampened session is allowed to be reused (taken out of dampening), in milliseconds.
                required: true
                type: int
              suppress-threshold:
                description: The threshold at which a session is suppressed (put into dampening), in milliseconds.
                required: true
                type: int
              max-suppress-time:
                description: The maximum amount of time a session can be suppressed, in minutes.
                required: true
                type: int
          echo:
            description: enables the BFD echo function for all interfaces which uses thsis specific template.
            required: false
            type : bool
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

from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.argspec.bfd_global.bfd_global import (
    Bfd_globalArgs,
)
from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.config.bfd_global.bfd_global import (
    Bfd_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bfd_globalArgs.argument_spec,
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

    result = Bfd_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
