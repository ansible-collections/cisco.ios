#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_ntp_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_ntp_global
short_description: ntp_global resource module
description:
- This module provides declarative management of ntp on Cisco IOS devices.
version_added: 2.5.0
author:
- Sagar Paul (@KB-perByte)
notes:
- Tested against Cisco IOSv Version 15.6.
- This module works with connection C(network_cli).
options:
  config:
    description: A dictionary of ntp options
    type: dict
    suboptions:
      access_group:
        description: Control NTP access
        type: dict
        suboptions:
          peer: 
            description: Provide full access
            type: list
            elements: dict
            suboptions:
              access_list: &access_group_acl
                description:  name or number of access list
                type: str
              kod: &kod
                description: Send a Kiss-o-Death packet for failing peers
                type: bool
              ipv4: &ipv4
                description:  ipv4 access lists (Default not idempotent)
                type: bool
              ipv6: &ipv6
                description:  ipv6 access lists (Default not idempotent)
                type: bool
          query_only: 
            description:  Allow only control queries
            type: list
            elements: dict
            suboptions: 
              access_list: *access_group_acl
              kod: *kod
              ipv4: *ipv4
              ipv6: *ipv6
          serve: 
            description:  Provide server and query access
            type: list
            elements: dict
            suboptions:
              access_list: *access_group_acl
              kod: *kod
              ipv4: *ipv4
              ipv6: *ipv6
          serve_only: 
            description:  Provide only server access
            type: list
            elements: dict
            suboptions:
              access_list: *access_group_acl
              kod: *kod
              ipv4: *ipv4
              ipv6: *ipv6
      allow:
        description: Allow processing of packets
        type: dict
        suboptions:
          control:
            description: Allow processing control mode packets
            type: dict
            suboptions:
              rate_limit:
                description: Rate-limit delay.
                type: int
          private:
            description: Allow processing private mode packets
            type: bool
      authenticate:
        description: Authenticate time sources
        type: bool
      authentication_keys:
        description: Authentication key for trusted time sources
        type: list
        elements: dict
        suboptions:
          id:
            description: Key number
            type: int
          algorithm:
            description: Authentication type
            type: str
          key:
            description: Password
            type: str
          encryption:
            description: Authentication key encryption type
            type: int
      broadcast_delay:
        description: Estimated round-trip delay
        type: int
      clock_period:
        description: Length of hardware clock tick, clock period in 2^-32 seconds
        type: int
      logging:
        description: Enable NTP message logging
        type: bool
      master:
        description: Act as NTP master clock
        type: dict
        suboptions:
          enabled:
            description: Enable master clock
            type: bool
          stratum_number:
            description: Stratum number
            type: int
      max_associations:
        description: Set maximum number of associations
        type: int
      max_distance:
        description: Maximum Distance for synchronization
        type: int
      min_distance:
        description: Minimum distance to consider for clockhop
        type: int
      orphan:
        description: Threshold Stratum for orphan mode
        type: int
      panic_update:
        description: Reject time updates > panic threshold (default 1000Sec)
        type: bool
      passive:
        description: NTP passive mode
        type: bool
      peers:
        description: Configure NTP peer
        type: list
        elements: dict
        suboptions:
          peer:
            description: ipv4/ipv6 address or hostname of the peer
            type: str
          use_ipv4: &use_ipv4
            description: Use IP for DNS resolution
            type: bool
          use_ipv6: &use_ipv6
            description: Use IPv6 for DNS resolution
            type: bool
          vrf: &vrf
            description: VPN Routing/Forwarding Information
            type: str
          burst: &burst
            description: Send a burst when peer is reachable (Default)
            type: bool
          iburst: &iburst
            description: Send a burst when peer is unreachable (Default)
            type: bool
          key: &key
            description: Configure peer authentication key
            type: int
          maxpoll: &maxpoll
            description: Maximum poll interval Poll value in Log2
            type: int
          minpoll: &minpoll
            description: Minimum poll interval Poll value in Log2
            type: int
          normal_sync: &normal_sync
            description: Disable rapid sync at startup
            type: bool
          prefer: &prefer
            description: Prefer this peer when possible
            type: bool
          source: &source
            description: Interface for source address
            type: str
          version: &version
            description: Configure NTP version
            type: int
      servers:
        description: Configure NTP server
        type: list
        elements: dict
        suboptions:
          server:
            description: ipv4/ipv6 address or hostname of the server
            type: str
          use_ipv4: *use_ipv4
          use_ipv6: *use_ipv6
          vrf: *vrf
          burst: *burst
          iburst: *iburst
          key: *key
          maxpoll: *maxpoll
          minpoll: *minpoll
          normal_sync: *normal_sync
          prefer: *prefer
          source: *source
          version: *version
      source:
        description: Configure interface for source address
        type: str
      trusted_keys:
        description: Key numbers for trusted time sources
        type: list
        elements: dict
        suboptions:
          range_start:
            description: Start / key number
            type: int
          range_end:
            description: End key number
            type: int
      update_calendar:
        description: Periodically update calendar with NTP time
        type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^ntp).
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
      - The states I(replaced) and I(overridden) have identical
        behaviour for this module.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command
        I(show running-config | section ^ntp) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
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
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
  type: list
  sample:
    - "ntp peer 20.18.11.3 key 6 minpoll 15 prefer version 2"
    - "ntp access-group ipv4 peer DHCP-Server kod"
    - "ntp trusted-key 9 - 96"
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when state is I(rendered)
  type: list
  sample:
    - "ntp server ip testserver.com prefer"
    - "ntp authentication-key 2 md5 testpass 22"
    - "ntp allow mode control 4"
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when state is I(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when state is I(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ntp_global.ntp_global import (
    Ntp_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.ntp_global.ntp_global import (
    Ntp_global,
)

# import debugpy

# debugpy.listen(3000)
# debugpy.wait_for_client()


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ntp_globalArgs.argument_spec,
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

    result = Ntp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
