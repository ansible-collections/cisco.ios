#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_monitor_sessions
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_monitor_sessions
short_description: Resource module to configure SPAN/RSPAN monitor sessions.
description:
  - This module provides declarative management of SPAN (Switched Port Analyzer)
    monitor sessions on Cisco IOS-XE devices.
  - Each monitor session defines one or more source interfaces whose traffic is
    mirrored to a destination interface.
version_added: "9.0.0"
author:
  - Ansible Network Eng Team
notes:
  - Tested against Cisco IOS-XE on Cat9k switches.
  - This module works with connection C(network_cli).
  - Interface names in C(config) must match the abbreviated form used in the
    running configuration (e.g. C(Gi1/0/1), C(Po2), C(Twe1/0/2)).
options:
  config:
    description: List of monitor session configurations.
    type: list
    elements: dict
    suboptions:
      session:
        description: Monitor session number.
        type: int
        required: true
      sources:
        description: List of source interface specifications.
        type: list
        elements: dict
        suboptions:
          interfaces:
            description:
              - List of source interface names for this source entry.
              - Each element is a single interface name (e.g. C(Gi1/0/1), C(Po2))
                or a range string exactly as it appears in the running configuration
                (e.g. C(Gi1/0/1 - 3)).
              - All interfaces in the list share the same C(direction).
            type: list
            elements: str
            required: true
          direction:
            description:
              - Traffic direction to monitor on the source interface.
              - C(both) is the default when no direction is specified.
            type: str
            choices:
              - rx
              - tx
              - both
            default: both
      destination:
        description: Destination interface configuration.
        type: dict
        suboptions:
          interface:
            description: Destination interface name.
            type: str
            required: true
          encapsulation_replicate:
            description: Replicate the encapsulation of the monitored traffic.
            type: bool
            default: false
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output of
        B(show running-config | section ^monitor session) executed on the device.
      - The state I(parsed) reads the configuration from this option and
        transforms it into Ansible structured data as per the resource module's
        argspec.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - I(merged) adds or updates monitor sessions without removing existing ones.
      - I(replaced) replaces source and destination configuration for the
        specified sessions, leaving unspecified sessions intact.
      - I(overridden) replaces the entire monitor session configuration; sessions
        not present in C(config) are removed.
      - I(deleted) removes the specified sessions, or all sessions when
        C(config) is omitted.
      - I(rendered) generates CLI commands from C(config) without connecting to
        the device.
      - I(gathered) retrieves and returns the running configuration as structured
        data without modifying the device.
      - I(parsed) parses the configuration provided in C(running_config) and
        returns structured data.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using state: merged

# Before state:
# -------------
# (no monitor session configuration)

- name: Configure SPAN session 1 with multiple sources and replicate encapsulation
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 1
        sources:
          - interfaces:
              - Twe1/0/2
              - Twe1/0/12
              - Twe1/0/45
          - interfaces:
              - Po2
        destination:
          interface: Po3
          encapsulation_replicate: true
    state: merged

# Commands fired:
# ---------------
# monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
# monitor session 1 source interface Po2
# monitor session 1 destination interface Po3 encapsulation replicate

# After state:
# ------------
# monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
# monitor session 1 source interface Po2
# monitor session 1 destination interface Po3 encapsulation replicate

# Using state: merged with direction

# Before state:
# -------------
# (no monitor session configuration)

- name: Configure SPAN session with rx-only sources
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 2
        sources:
          - interfaces:
              - "Gi1/0/1 - 3"
            direction: rx
          - interfaces:
              - Gi1/0/5
        destination:
          interface: Gi1/0/48
    state: merged

# Commands fired:
# ---------------
# monitor session 2 source interface Gi1/0/1 - 3 rx
# monitor session 2 source interface Gi1/0/5
# monitor session 2 destination interface Gi1/0/48

# Using state: replaced

# Before state:
# -------------
# monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
# monitor session 1 source interface Po2
# monitor session 1 destination interface Po3 encapsulation replicate

- name: Replace session 1 with updated source list
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 1
        sources:
          - interfaces:
              - Po2
          - interfaces:
              - Po4
        destination:
          interface: Po3
          encapsulation_replicate: true
    state: replaced

# Commands fired:
# ---------------
# no monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
# monitor session 1 source interface Po4

# After state:
# ------------
# monitor session 1 source interface Po2
# monitor session 1 source interface Po4
# monitor session 1 destination interface Po3 encapsulation replicate

# Using state: overridden

# Before state:
# -------------
# monitor session 1 source interface Po2
# monitor session 1 destination interface Po3 encapsulation replicate
# monitor session 2 source interface Gi1/0/1
# monitor session 2 destination interface Gi1/0/48

- name: Override all sessions - remove session 2 and update session 1
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 1
        sources:
          - interfaces:
              - Po2
        destination:
          interface: Po3
          encapsulation_replicate: true
    state: overridden

# Commands fired:
# ---------------
# no monitor session 2

# Using state: deleted - specific session

- name: Delete monitor session 1
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 1
    state: deleted

# Commands fired:
# ---------------
# no monitor session 1

# Using state: deleted - all sessions

- name: Delete all monitor sessions
  cisco.ios.ios_monitor_sessions:
    state: deleted

# Commands fired:
# ---------------
# no monitor session 1
# no monitor session 2

# Using state: gathered

- name: Gather monitor session facts
  cisco.ios.ios_monitor_sessions:
    state: gathered

# Returns:
# gathered:
#   - session: 1
#     sources:
#       - interfaces:
#           - Twe1/0/2
#           - Twe1/0/12
#           - Twe1/0/45
#         direction: both
#       - interfaces:
#           - Po2
#         direction: both
#     destination:
#       interface: Po3
#       encapsulation_replicate: true

# Using state: rendered

- name: Render monitor session commands without connecting to the device
  cisco.ios.ios_monitor_sessions:
    config:
      - session: 1
        sources:
          - interfaces:
              - Po2
        destination:
          interface: Po3
          encapsulation_replicate: true
    state: rendered

# Returns:
# rendered:
#   - monitor session 1 source interface Po2
#   - monitor session 1 destination interface Po3 encapsulation replicate

# Using state: parsed

- name: Parse monitor session configuration
  cisco.ios.ios_monitor_sessions:
    running_config: |
      monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
      monitor session 1 source interface Po2
      monitor session 1 destination interface Po3 encapsulation replicate
    state: parsed

# Returns:
# parsed:
#   - session: 1
#     sources:
#       - interfaces:
#           - Twe1/0/2
#           - Twe1/0/12
#           - Twe1/0/45
#         direction: both
#       - interfaces:
#           - Po2
#         direction: both
#     destination:
#       interface: Po3
#       encapsulation_replicate: true
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration module invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
    of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - monitor session 1 source interface Po2
    - monitor session 1 destination interface Po3 encapsulation replicate
rendered:
  description: The set of CLI commands generated from the value of I(config) option.
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - monitor session 1 source interface Po2
    - monitor session 1 destination interface Po3 encapsulation replicate
gathered:
  description: Facts about the network resource gathered from the remote device
    as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option,
    parsed into structured data as per module argspec.
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.monitor_sessions.monitor_sessions import (
    Monitor_sessionsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.monitor_sessions.monitor_sessions import (
    Monitor_sessions,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Monitor_sessionsArgs.argument_spec,
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

    result = Monitor_sessions(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
