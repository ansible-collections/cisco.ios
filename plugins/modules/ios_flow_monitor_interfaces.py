#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_flow_monitor_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_flow_monitor_interfaces
short_description: Resource module to configure per-interface flow monitor assignments on Cisco IOS XE.
description:
  - This module manages the per-interface C(ip flow monitor) configuration on Cisco IOS XE devices.
  - It assigns flow monitors (with a sampler and direction) to interfaces.
  - Flow monitor and sampler names referenced here must already exist on the device;
    use M(cisco.ios.ios_flow_monitor) to create them.
version_added: "11.7.0"
author:
  - Jorgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - Short interface names (e.g. Gi0/1) may impact idempotency; prefer full names.
  - The module examples use callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
options:
  config:
    description: A list of interfaces with flow monitor assignments.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface, e.g. GigabitEthernet0/1, Port-channel21.800.
          - Short interface names like Gi0/1 may impact idempotency.
        type: str
        required: true
      flow_monitors:
        description: List of flow monitor assignments on this interface.
        type: list
        elements: dict
        suboptions:
          monitor:
            description: Name of the flow monitor to apply.
            type: str
            required: true
          sampler:
            description: Name of the sampler to use with this monitor.
            type: str
            required: true
          direction:
            description: Traffic direction to monitor.
            type: str
            required: true
            choices: [input, output]
          protocol:
            description:
              - IP protocol family for the flow monitor assignment.
              - Use C(ipv6) to assign the monitor to IPv6 traffic (C(ipv6 flow monitor ...)).
              - Defaults to C(ip) for standard IPv4 monitoring.
            type: str
            choices: [ip, ipv6]
            default: ip
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS XE device by
        executing the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec.
    type: str
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - parsed
    default: merged
    description:
      - The state the configuration should be left in.
      - State I(merged) merges the provided flow monitor assignments into existing interface config.
      - State I(replaced) replaces the flow monitor assignments for specified interfaces only.
      - State I(overridden) replaces flow monitor assignments across all interfaces.
      - State I(deleted) removes the specified (or all) flow monitor assignments.
      - State I(rendered), I(gathered) and I(parsed) do not perform any change on the device.
    type: str
"""

EXAMPLES = """
# Using state: merged

# Before state:
# router# show running-config | section ^interface
# interface GigabitEthernet1
#  ip address 192.0.2.10 255.255.255.0

- name: Assign flow monitors to interfaces
  cisco.ios.ios_flow_monitor_interfaces:
    config:
      - name: GigabitEthernet1
        flow_monitors:
          - monitor: FLOW_MONITOR_IN
            sampler: FLOW_SAMPLER
            direction: input
          - monitor: FLOW_MONITOR_OUT
            sampler: FLOW_SAMPLER
            direction: output
    state: merged

# Commands fired:
# interface GigabitEthernet1
#  ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
#  ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output

# Using state: deleted

- name: Remove flow monitors from specific interfaces
  cisco.ios.ios_flow_monitor_interfaces:
    config:
      - name: GigabitEthernet1
    state: deleted

# Using state: deleted — remove all

- name: Remove all interface flow monitor assignments
  cisco.ios.ios_flow_monitor_interfaces:
    state: deleted

# Using state: replaced

# Before state:
# interface GigabitEthernet1
#  ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input
#  ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output

- name: Replace flow monitors on GigabitEthernet1
  cisco.ios.ios_flow_monitor_interfaces:
    config:
      - name: GigabitEthernet1
        flow_monitors:
          - monitor: FLOW_MONITOR_IN
            sampler: FLOW_SAMPLER
            direction: input
          - monitor: FLOW_MONITOR_OUT
            sampler: FLOW_SAMPLER
            direction: output
    state: replaced

# Commands fired:
# interface GigabitEthernet1
#  no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input
#  no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output
#  ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
#  ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output

# Using state: parsed

- name: Parse interface config into structured data
  cisco.ios.ios_flow_monitor_interfaces:
    running_config: |
      interface GigabitEthernet1
       ip address 192.0.2.10 255.255.255.0
       ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
       ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
    state: parsed

# Using state: merged — with IPv6 monitor

- name: Assign IPv6 flow monitor to interface
  cisco.ios.ios_flow_monitor_interfaces:
    config:
      - name: GigabitEthernet1
        flow_monitors:
          - monitor: FLOW_MONITOR_V6
            sampler: FLOW_SAMPLER
            direction: input
            protocol: ipv6
    state: merged

# Commands fired:
# interface GigabitEthernet1
#  ipv6 flow monitor FLOW_MONITOR_V6 sampler FLOW_SAMPLER input

# Using state: gathered

- name: Gather flow monitor interface assignments
  cisco.ios.ios_flow_monitor_interfaces:
    state: gathered
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
after:
  description: The resulting configuration module invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample:
    - interface GigabitEthernet1
    - ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
    - ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
rendered:
  description: The set of CLI commands generated from the value of I(state=rendered) option.
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface GigabitEthernet1
    - ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option, parsed into structured data.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    emit_warnings,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.flow_monitor_interfaces.flow_monitor_interfaces import (
    Flow_monitor_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.flow_monitor_interfaces.flow_monitor_interfaces import (
    Flow_monitor_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Flow_monitor_interfacesArgs.argument_spec,
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

    result = Flow_monitor_interfaces(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
