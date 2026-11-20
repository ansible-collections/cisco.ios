#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_track_objects
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_track_objects
short_description: Resource module to configure tracked objects.
description:
  - This module configures and manages the attributes of tracked objects on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
options:
  config:
    description: A list of tracked objects.
    type: list
    elements: dict
    suboptions:
      object_id:
        description: Tracked object number (1-1000).
        type: int
        required: true
      interface:
        description:
          - Track the state of an interface.
          - Mutually exclusive with I(ip_sla), I(ip_route) and I(boolean_list).
        type: dict
        suboptions:
          name:
            description: Interface name, for example C(GigabitEthernet1) or C(Gi1).
            type: str
            required: true
          parameter:
            description: What to track, C(line_protocol) or C(ip_routing).
            type: str
            required: true
            choices: ["line_protocol", "ip_routing"]
      ip_sla:
        description:
          - Track an IP SLA operation.
          - Mutually exclusive with I(interface), I(ip_route) and I(boolean_list).
        type: dict
        suboptions:
          operation_id:
            description: IP SLA operation number.
            type: int
            required: true
          parameter:
            description: What to track, C(reachability) or C(state).
            type: str
            required: true
            choices: ["reachability", "state"]
      ip_route:
        description:
          - Track the reachability of a route.
          - Mutually exclusive with I(interface), I(ip_sla) and I(boolean_list).
        type: dict
        suboptions:
          prefix:
            description: Route to track in C(address/prefix-length) form, for example C(192.0.2.0/24).
            type: str
            required: true
          vrf:
            description: VRF the route is looked up in (C(ip vrf)).
            type: str
      boolean_list:
        description:
          - Track a boolean combination of other tracked objects (C(list boolean)).
          - Mutually exclusive with I(interface), I(ip_sla) and I(ip_route).
        type: dict
        suboptions:
          operator:
            description: How the objects are combined.
            type: str
            required: true
            choices: ["and", "or"]
          objects:
            description: The tracked objects in the list.
            type: list
            elements: dict
            suboptions:
              object_id:
                description: Number of the tracked object.
                type: int
                required: true
              negate:
                description: Use the opposite state of the object (C(object N not)).
                type: bool
      delay:
        description: Delay before a state change is reported (C(delay down N up N)).
        type: dict
        suboptions:
          down:
            description: Seconds to wait before reporting down.
            type: int
          up:
            description: Seconds to wait before reporting up.
            type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^track).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided configuration is added to the existing one. Nothing is removed.
      - With state I(replaced), every object named in the task is made to match exactly. Objects not named are left alone.
      - With state I(overridden), the device is made to match the task exactly, objects not named are removed.
      - With state I(deleted), the objects named in the task are removed. Without I(config) all supported objects are removed.
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
# router#show running-config | section ^track
# router#

- name: Merge tracked objects
  cisco.ios.ios_track_objects:
    config:
      - object_id: 1
        ip_sla:
          operation_id: 1
          parameter: state
        delay:
          down: 120
          up: 180
      - object_id: 2
        ip_route:
          prefix: 192.0.2.0/28
          vrf: MGMT
        delay:
          down: 10
          up: 5
      - object_id: 10
        boolean_list:
          operator: and
          objects:
            - object_id: 1
            - object_id: 2
              negate: true
        delay:
          down: 10
    state: merged

# Task Output
# -----------
#
# commands:
#   - track 1 ip sla 1 state
#   - delay down 120 up 180
#   - track 2 ip route 192.0.2.0 255.255.255.240 reachability
#   - ip vrf MGMT
#   - delay down 10 up 5
#   - track 10 list boolean and
#   - object 1
#   - object 2 not
#   - delay down 10

# After state:
# ------------
#
# router#show running-config | section ^track
# track 1 ip sla 1 state
#  delay down 120 up 180
# track 2 ip route 192.0.2.0 255.255.255.240 reachability
#  ip vrf MGMT
#  delay down 10 up 5
# track 10 list boolean and
#  object 1
#  object 2 not
#  delay down 10

# Using replaced

# Before state:
# -------------
#
# track 1 ip sla 1 state
#  delay down 120 up 180

- name: Replace tracked object 1
  cisco.ios.ios_track_objects:
    config:
      - object_id: 1
        ip_sla:
          operation_id: 1
          parameter: state
        delay:
          up: 30
    state: replaced

# Task Output
# -----------
#
# commands:
#   - track 1
#   - no delay
#   - delay up 30

# Using overridden

# Before state:
# -------------
#
# track 1 ip sla 1 state
# track 2 ip sla 2 state

- name: Override tracked objects
  cisco.ios.ios_track_objects:
    config:
      - object_id: 1
        ip_sla:
          operation_id: 1
          parameter: state
    state: overridden

# Task Output
# -----------
#
# commands:
#   - no track 2

# Using deleted

- name: Delete tracked object 1
  cisco.ios.ios_track_objects:
    config:
      - object_id: 1
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no track 1

- name: Delete all tracked objects
  cisco.ios.ios_track_objects:
    state: deleted

# Using gathered

- name: Gather tracked objects
  cisco.ios.ios_track_objects:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   - object_id: 1
#     ip_sla:
#       operation_id: 1
#       parameter: state
#     delay:
#       down: 120
#       up: 180

# Using rendered

- name: Render tracked object commands
  cisco.ios.ios_track_objects:
    config:
      - object_id: 3
        interface:
          name: GigabitEthernet1
          parameter: line_protocol
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - track 3 interface GigabitEthernet1 line-protocol

# Using parsed

- name: Parse tracked objects
  cisco.ios.ios_track_objects:
    running_config: |
      track 1 ip sla 1 state
       delay down 120 up 180
    state: parsed

# Task Output
# -----------
#
# parsed:
#   - object_id: 1
#     ip_sla:
#       operation_id: 1
#       parameter: state
#     delay:
#       down: 120
#       up: 180
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
    - track 1 ip sla 1 state
    - delay down 120 up 180
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - track 1 ip sla 1 state
    - delay down 120 up 180
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.track_objects.track_objects import (
    Track_objectsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.track_objects.track_objects import (
    Track_objects,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Track_objectsArgs.argument_spec,
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

    result = Track_objects(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
