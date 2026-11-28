#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_ip_sla_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_ip_sla_global
short_description: Resource module to configure IP SLA operations.
description:
  - This module configures and manages the attributes of IP SLA operations on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A dictionary of IP SLA configuration.
    type: dict
    suboptions:
      logging_traps:
        description: Enable SNMP traps for IP SLA events (C(ip sla logging traps)).
        type: bool
      enable_reaction_alerts:
        description: Enable IP SLA reaction alerts (C(ip sla enable reaction-alerts)).
        type: bool
      operations:
        description: List of IP SLA operations.
        type: list
        elements: dict
        suboptions:
          operation_id:
            description: IP SLA operation number (1-2147483647).
            type: int
            required: true
          icmp_echo:
            description:
              - ICMP echo operation (C(icmp-echo)).
              - Mutually exclusive with I(tcp_connect) and I(http).
            type: dict
            suboptions:
              destination:
                description: Destination IP address or hostname.
                type: str
                required: true
              source_ip:
                description: Source IP address. Mutually exclusive with I(source_interface).
                type: str
              source_interface:
                description: Source interface. Mutually exclusive with I(source_ip).
                type: str
          tcp_connect:
            description:
              - TCP connect operation (C(tcp-connect)).
              - Mutually exclusive with I(icmp_echo) and I(http).
            type: dict
            suboptions:
              destination:
                description: Destination IP address or hostname.
                type: str
                required: true
              port:
                description: Destination TCP port.
                type: int
                required: true
              source_ip:
                description: Source IP address.
                type: str
              source_port:
                description: Source TCP port.
                type: int
          http:
            description:
              - HTTP operation (C(http get) or C(http raw)).
              - Mutually exclusive with I(icmp_echo) and I(tcp_connect).
            type: dict
            suboptions:
              method:
                description: HTTP operation type.
                type: str
                required: true
                choices: ["get", "raw"]
              url:
                description: URL to probe.
                type: str
                required: true
              raw_request:
                description:
                  - The request sent with C(http raw), the single line inside the C(http-raw-request) block.
                  - Line breaks are written as the literal characters C(\\r\\n), exactly as IOS stores them.
                type: str
          vrf:
            description: VRF the probe is sent in.
            type: str
          frequency:
            description: Seconds between probes.
            type: int
          threshold:
            description: Upper threshold in milliseconds for the operation to be considered over threshold.
            type: int
          timeout:
            description: Probe timeout in milliseconds.
            type: int
          tag:
            description: User-defined tag.
            type: str
          owner:
            description: Owner of the operation.
            type: str
          request_data_size:
            description: Payload size in bytes of the request.
            type: int
          tos:
            description: Type of service byte.
            type: int
          schedule:
            description: Schedule of the operation (C(ip sla schedule)).
            type: dict
            suboptions:
              life:
                description: Lifetime in seconds, or C(forever). IOS uses 3600 when it is not given.
                type: str
              start_time:
                description:
                  - When the operation starts, for example C(now), C(pending), C(after 00:05:00) or C(14:30).
                type: str
              ageout:
                description: Seconds an inactive operation stays in memory.
                type: int
              recurring:
                description: Schedule the operation every day.
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^ip sla).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided configuration is added to the existing one.
      - With state I(replaced), every operation named in the task is made to match exactly.
        Operations not named are left alone. Global options not set in the task are removed.
      - With state I(overridden), the device is made to match the task exactly, operations not named
        in the task are removed.
      - With state I(deleted), the operations named in the task are removed. If no operations are given
        in the task, all supported operations and the global options are removed.
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
# router#show running-config | section ^ip sla
# router#

- name: Merge IP SLA configuration
  cisco.ios.ios_ip_sla_global:
    config:
      logging_traps: true
      operations:
        - operation_id: 1
          icmp_echo:
            destination: 192.0.2.1
            source_interface: Loopback0
          vrf: MGMT
          frequency: 5
          schedule:
            life: forever
            start_time: now
        - operation_id: 2
          http:
            method: raw
            url: http://192.0.2.10
            raw_request: "GET http://192.0.2.10/test HTTP/1.0\\\\r\\\\nUser-Agent: Cisco IP SLA\\\\r\\\\nend\\\\r\\\\n\\\\r\\\\n"
          threshold: 500
          timeout: 5000
    state: merged

# Task Output
# -----------
#
# before: {}
#
# commands:
#   - ip sla logging traps
#   - ip sla 1
#   - icmp-echo 192.0.2.1 source-interface loopback0
#   - vrf MGMT
#   - frequency 5
#   - ip sla schedule 1 life forever start-time now
#   - ip sla 2
#   - http raw http://192.0.2.10
#   - http-raw-request
#   - GET http://192.0.2.10/test HTTP/1.0\\r\\nUser-Agent: Cisco IP SLA\\r\\nend\\r\\n\\r\\n
#   - exit
#   - threshold 500
#   - timeout 5000

# After state:
# ------------
#
# router#show running-config | section ^ip sla
# ip sla logging traps
# ip sla 1
#  icmp-echo 192.0.2.1 source-interface Loopback0
#   vrf MGMT
#   frequency 5
# ip sla 2
#  http raw http://192.0.2.10
#   http-raw-request
#    GET http://192.0.2.10/test HTTP/1.0\\r\\nUser-Agent: Cisco IP SLA\\r\\nend\\r\\n\\r\\n
#    exit
#   threshold 500
#   timeout 5000
# ip sla schedule 1 life forever start-time now

# Using replaced

# Before state:
# -------------
#
# ip sla 1
#  icmp-echo 192.0.2.1 source-interface Loopback0
#   vrf MGMT
#   frequency 5
# ip sla schedule 1 life forever start-time now

- name: Replace operation 1
  cisco.ios.ios_ip_sla_global:
    config:
      operations:
        - operation_id: 1
          icmp_echo:
            destination: 192.0.2.1
          frequency: 10
          schedule:
            life: forever
            start_time: now
    state: replaced

# Task Output
# -----------
#
# commands:
#   - ip sla 1
#   - icmp-echo 192.0.2.1
#   - no vrf
#   - frequency 10

# Using overridden

# Before state:
# -------------
#
# ip sla 1
#  icmp-echo 192.0.2.1 source-interface Loopback0
# ip sla 2
#  icmp-echo 192.0.2.2
# ip sla schedule 1 life forever start-time now

- name: Override the IP SLA configuration
  cisco.ios.ios_ip_sla_global:
    config:
      operations:
        - operation_id: 1
          icmp_echo:
            destination: 192.0.2.1
            source_interface: Loopback0
          schedule:
            life: forever
            start_time: now
    state: overridden

# Task Output
# -----------
#
# commands:
#   - no ip sla 2

# Using deleted

- name: Delete one operation
  cisco.ios.ios_ip_sla_global:
    config:
      operations:
        - operation_id: 2
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no ip sla 2

- name: Delete all IP SLA configuration
  cisco.ios.ios_ip_sla_global:
    state: deleted

# Using gathered

- name: Gather IP SLA configuration
  cisco.ios.ios_ip_sla_global:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   logging_traps: true
#   operations:
#     - operation_id: 1
#       icmp_echo:
#         destination: 192.0.2.1
#         source_interface: Loopback0
#       frequency: 5
#       vrf: MGMT
#       schedule:
#         life: forever
#         start_time: now

# Using rendered

- name: Render IP SLA commands
  cisco.ios.ios_ip_sla_global:
    config:
      operations:
        - operation_id: 5
          tcp_connect:
            destination: 192.0.2.5
            port: 443
          frequency: 30
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - ip sla 5
#   - tcp-connect 192.0.2.5 443
#   - frequency 30

# Using parsed

- name: Parse IP SLA configuration
  cisco.ios.ios_ip_sla_global:
    running_config: |
      ip sla 1
       icmp-echo 192.0.2.1 source-interface Loopback0
        frequency 5
      ip sla schedule 1 life forever start-time now
    state: parsed

# Task Output
# -----------
#
# parsed:
#   operations:
#     - operation_id: 1
#       icmp_echo:
#         destination: 192.0.2.1
#         source_interface: Loopback0
#       frequency: 5
#       schedule:
#         life: forever
#         start_time: now
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
    - ip sla 1
    - icmp-echo 192.0.2.1 source-interface loopback0
    - frequency 5
    - ip sla schedule 1 life forever start-time now
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - ip sla 1
    - icmp-echo 192.0.2.1 source-interface loopback0
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ip_sla_global.ip_sla_global import (
    Ip_sla_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.ip_sla_global.ip_sla_global import (
    Ip_sla_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ip_sla_globalArgs.argument_spec,
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

    result = Ip_sla_global(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
