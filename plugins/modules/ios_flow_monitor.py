#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_flow_monitor
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_flow_monitor
short_description: Resource module to configure Flexible NetFlow on Cisco IOS XE.
description:
  - This module manages the Flexible NetFlow global configuration on Cisco IOS XE devices.
  - It manages flow records, flow exporters, samplers, and flow monitors as named entities.
version_added: "11.7.0"
author:
  - Jorgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - The module examples use callback plugin (stdout_callback = yaml) to generate task
    output in yaml format.
  - Some options (C(cache type permanent), C(transport tcp)) are only supported on router platforms.
  - The platforms accept different C(collect) options. The module does not check the platform, the device
    rejects an option it does not support when the commands are applied. Commands sent before the rejected
    one stay applied.
  - Tested on a Catalyst 9300 (IOS XE 17.12.4 and 17.18.4) and a Catalyst 9600 (C9606R, IOS XE 17.12.5), both with
    Network Advantage and DNA Advantage licenses. The license does not change which options are accepted.
  - Catalyst 9600 accepts C(counter_bytes) and C(counter_packets) (C(collect counter bytes), C(collect counter packets))
    and C(timestamp_sys_uptime_first) and C(timestamp_sys_uptime_last). Existing flow records on these devices use them.
  - Catalyst 9300 rejects C(counter_bytes) and C(counter_packets) with C(% Incomplete command), and rejects
    C(timestamp_sys_uptime_first) and C(timestamp_sys_uptime_last) as invalid input. Use C(counter_bytes_long),
    C(counter_bytes_layer2_long), C(counter_packets_long), C(timestamp_absolute_first) and C(timestamp_absolute_last) there.
  - Catalyst 9300 also rejects C(counter_bytes_layer2) (it needs C(long), use C(counter_bytes_layer2_long)),
    C(routing_source_as) and C(routing_destination_as) without qualifier, and the C(routing_source_as_peer) and
    C(routing_destination_as_peer) variants, all with C(% Incomplete command). C(routing_source_as_4octet) and
    C(routing_destination_as_4octet) are accepted.
  - Accepted on the Catalyst 9300 and used in existing Catalyst 9600 flow records, so these are the safe choice on both,
    C(routing_source_as_4octet), C(routing_destination_as_4octet), C(routing_next_hop_ipv4), C(transport_tcp_flags),
    C(interface_input) and C(interface_output).
  - IOS XE does not show values that are the default in the running configuration, for example
    C(cache timeout inactive 15), C(cache timeout active 1800) and the exporter
    C(export-protocol netflow-v9), C(template data timeout 600), C(ttl 255) and C(dscp 0).
    The module treats these as equal to an unset value, so specifying them does not cause a change on every run.
  - IOS XE ignores changes to a flow record, without reporting an error, while a flow monitor that uses it
    exists. To change a record, delete the flow monitors using it first, or use a new record name.
options:
  config:
    description: Flexible NetFlow global configuration.
    type: dict
    suboptions:
      records:
        description: Flow record definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the flow record.
            type: str
            required: true
          match:
            description: Flow record match fields.
            type: dict
            suboptions:
              ipv4_tos:
                description: Match IPv4 ToS/DSCP field.
                type: bool
              ipv4_protocol:
                description: Match IPv4 protocol field.
                type: bool
              ipv4_source_address:
                description: Match IPv4 source address.
                type: bool
              ipv4_destination_address:
                description: Match IPv4 destination address.
                type: bool
              ipv4_ttl:
                description: Match IPv4 TTL.
                type: bool
              ipv4_version:
                description: Match IPv4 version.
                type: bool
              transport_source_port:
                description: Match transport layer source port.
                type: bool
              transport_destination_port:
                description: Match transport layer destination port.
                type: bool
              transport_icmp_ipv4_code:
                description: Match ICMP IPv4 code.
                type: bool
              transport_icmp_ipv4_type:
                description: Match ICMP IPv4 type.
                type: bool
              transport_icmp_ipv6_code:
                description: Match ICMP IPv6 code.
                type: bool
              transport_icmp_ipv6_type:
                description: Match ICMP IPv6 type.
                type: bool
              flow_direction:
                description: Match flow direction (ingress/egress).
                type: bool
              interface_input:
                description: Match input interface.
                type: bool
              interface_output:
                description: Match output interface.
                type: bool
              routing_vrf_input:
                description: Match input routing VRF.
                type: bool
              ipv6_source_address:
                description: Match IPv6 source address.
                type: bool
              ipv6_destination_address:
                description: Match IPv6 destination address.
                type: bool
              ipv6_hop_limit:
                description: Match IPv6 hop-limit.
                type: bool
              ipv6_protocol:
                description: Match IPv6 protocol.
                type: bool
              ipv6_traffic_class:
                description: Match IPv6 traffic class.
                type: bool
              ipv6_version:
                description: Match IPv6 version.
                type: bool
              datalink_dot1q_priority:
                description: Match 802.1Q priority.
                type: bool
              datalink_dot1q_vlan_input:
                description: Match ingress 802.1Q VLAN.
                type: bool
              datalink_dot1q_vlan_output:
                description: Match egress 802.1Q VLAN.
                type: bool
              datalink_ethertype:
                description: Match EtherType.
                type: bool
              datalink_mac_destination_input:
                description: Match ingress destination MAC address.
                type: bool
              datalink_mac_destination_output:
                description: Match egress destination MAC address.
                type: bool
              datalink_mac_source_input:
                description: Match ingress source MAC address.
                type: bool
              datalink_mac_source_output:
                description: Match egress source MAC address.
                type: bool
              datalink_vlan_input:
                description: Match ingress VLAN.
                type: bool
              datalink_vlan_output:
                description: Match egress VLAN.
                type: bool
              application_name:
                description: Match application name (NBAR).
                type: bool
          collect:
            description: Flow record collect fields.
            type: dict
            suboptions:
              routing_source_as:
                description:
                  - Collect source AS number (C(collect routing source as)).
                  - Rejected by Catalyst 9300 as an incomplete command, use I(routing_source_as_4octet) there.
                type: bool
              routing_source_as_4octet:
                description: Collect 4-octet source AS number. Accepted on Catalyst 9300 and 9600.
                type: bool
              routing_source_as_peer:
                description:
                  - Collect peer source AS number.
                  - Rejected by Catalyst 9300 as an incomplete command.
                type: bool
              routing_destination_as:
                description:
                  - Collect destination AS number (C(collect routing destination as)).
                  - Rejected by Catalyst 9300 as an incomplete command, use I(routing_destination_as_4octet) there.
                type: bool
              routing_destination_as_4octet:
                description: Collect 4-octet destination AS number. Accepted on Catalyst 9300 and 9600.
                type: bool
              routing_destination_as_peer:
                description:
                  - Collect peer destination AS number.
                  - Rejected by Catalyst 9300 as an incomplete command.
                type: bool
              routing_next_hop_ipv4:
                description: Collect IPv4 next-hop address.
                type: bool
              routing_next_hop_ipv6:
                description: Collect IPv6 next-hop address.
                type: bool
              transport_tcp_flags:
                description: Collect TCP flags.
                type: bool
              transport_destination_port:
                description: Collect transport destination port.
                type: bool
              transport_source_port:
                description: Collect transport source port.
                type: bool
              counter_bytes:
                description:
                  - Collect byte counter (C(collect counter bytes)).
                  - Accepted by Catalyst 9600 and routers. Rejected by Catalyst 9300 as an incomplete command, use
                    I(counter_bytes_long) or I(counter_bytes_layer2_long) there.
                type: bool
              counter_bytes_long:
                description: Collect 64-bit byte counter. Accepted on Catalyst 9300 and 9600.
                type: bool
              counter_bytes_layer2:
                description:
                  - Collect Layer 2 byte counter (C(collect counter bytes layer2)).
                  - Rejected by Catalyst 9300 as an incomplete command, use I(counter_bytes_layer2_long) there.
                type: bool
              counter_bytes_layer2_long:
                description:
                  - Collect 64-bit Layer 2 byte counter (C(collect counter bytes layer2 long)).
                  - This is the byte counter recommended for Catalyst 9300.
                type: bool
              counter_packets:
                description:
                  - Collect packet counter (C(collect counter packets)).
                  - Accepted by Catalyst 9600 and routers. Rejected by Catalyst 9300 as an incomplete command, use
                    I(counter_packets_long) there.
                type: bool
              counter_packets_long:
                description: Collect 64-bit packet counter. Accepted on Catalyst 9300 and 9600.
                type: bool
              timestamp_sys_uptime_first:
                description:
                  - Collect system uptime at flow start.
                  - Accepted by Catalyst 9600 and routers. Rejected by Catalyst 9300, use I(timestamp_absolute_first) there.
                type: bool
              timestamp_sys_uptime_last:
                description:
                  - Collect system uptime at last packet.
                  - Accepted by Catalyst 9600 and routers. Rejected by Catalyst 9300, use I(timestamp_absolute_last) there.
                type: bool
              timestamp_absolute_first:
                description: Collect absolute timestamp at flow start. Accepted on Catalyst 9300.
                type: bool
              timestamp_absolute_last:
                description: Collect absolute timestamp at last packet. Accepted on Catalyst 9300.
                type: bool
              interface_input:
                description: Collect input interface.
                type: bool
              interface_output:
                description: Collect output interface.
                type: bool
              ipv4_source_address:
                description: Collect IPv4 source address.
                type: bool
              ipv4_source_mask:
                description: Collect IPv4 source mask.
                type: bool
              ipv4_source_prefix:
                description: Collect IPv4 source prefix.
                type: bool
              ipv4_destination_address:
                description: Collect IPv4 destination address.
                type: bool
              ipv4_destination_mask:
                description: Collect IPv4 destination mask.
                type: bool
              ipv4_destination_prefix:
                description: Collect IPv4 destination prefix.
                type: bool
              ipv4_protocol:
                description: Collect IPv4 protocol.
                type: bool
              ipv4_version:
                description: Collect IPv4 version.
                type: bool
              ipv6_source_address:
                description: Collect IPv6 source address.
                type: bool
              ipv6_source_mask:
                description: Collect IPv6 source mask.
                type: bool
              ipv6_source_prefix:
                description: Collect IPv6 source prefix.
                type: bool
              ipv6_destination_address:
                description: Collect IPv6 destination address.
                type: bool
              ipv6_destination_mask:
                description: Collect IPv6 destination mask.
                type: bool
              ipv6_destination_prefix:
                description: Collect IPv6 destination prefix.
                type: bool
              ipv6_protocol:
                description: Collect IPv6 protocol.
                type: bool
              ipv6_version:
                description: Collect IPv6 version.
                type: bool
              datalink_dot1q_vlan_input:
                description: Collect ingress 802.1Q VLAN.
                type: bool
              datalink_dot1q_vlan_output:
                description: Collect egress 802.1Q VLAN.
                type: bool
              datalink_mac_destination_input:
                description: Collect ingress destination MAC.
                type: bool
              datalink_mac_destination_output:
                description: Collect egress destination MAC.
                type: bool
              datalink_mac_source_input:
                description: Collect ingress source MAC.
                type: bool
              datalink_mac_source_output:
                description: Collect egress source MAC.
                type: bool
              flow_sampler:
                description: Collect flow sampler ID.
                type: bool
      exporters:
        description: Flow exporter definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the flow exporter.
            type: str
            required: true
          description:
            description: Human-readable description of the exporter.
            type: str
          destination:
            description: Destination IP address for the exporter.
            type: str
          vrf:
            description: VRF for the destination.
            type: str
          source:
            description: Source interface for exported packets.
            type: str
          export_protocol:
            description: Export protocol (ipfix or netflow-v9).
            type: str
            choices: [ipfix, netflow-v9]
          transport:
            description: Transport protocol and port.
            type: dict
            suboptions:
              protocol:
                description: Transport protocol (tcp is router-only).
                type: str
                choices: [udp, tcp]
                default: udp
              port:
                description: Destination port number.
                type: int
          template_data_timeout:
            description: Interval to re-send template records (seconds).
            type: int
          ttl:
            description: Time-to-live for exported packets.
            type: int
          dscp:
            description: DSCP value for exported packets.
            type: int
          options:
            description: Exporter option records to send.
            type: dict
            suboptions:
              sampler_table_timeout:
                description: Timeout for sampler-table option export (seconds).
                type: int
              template_data_timeout:
                description: Timeout for template data option export (seconds).
                type: int
              interface_table_timeout:
                description: Timeout for interface-table option export (seconds).
                type: int
              exporter_stats_timeout:
                description: Timeout for exporter-stats option export (seconds).
                type: int
              application_table_timeout:
                description: Timeout for application-table option export (seconds, NBAR).
                type: int
              vrf_table_timeout:
                description: Timeout for vrf-table option export (seconds).
                type: int
      samplers:
        description: Sampler definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the sampler.
            type: str
            required: true
          description:
            description: Human-readable description of the sampler.
            type: str
          mode:
            description: Sampling mode.
            type: str
            choices: [random, deterministic]
          window_size:
            description: Sampling rate expressed as N in "1 out-of N".
            type: int
      monitors:
        description: Flow monitor definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the flow monitor.
            type: str
            required: true
          description:
            description: Human-readable description of the monitor.
            type: str
          record:
            description: Name of the flow record to use.
            type: str
          exporters:
            description: List of exporter names to use (supports multiple exporters).
            type: list
            elements: str
          cache:
            description: Cache settings.
            type: dict
            suboptions:
              type:
                description: Cache type (permanent is router-only).
                type: str
                choices: [normal, permanent]
              entries:
                description: Maximum number of cache entries.
                type: int
              timeout_inactive:
                description: Inactive flow cache timeout (seconds).
                type: int
              timeout_active:
                description: Active flow cache timeout (seconds).
                type: int
              timeout_update:
                description: Update/sync cache timeout for permanent caches (seconds).
                type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output of the command
        B(show running-config | section ^(flow|sampler)) on the device.
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
      - State I(merged) merges the provided config into the existing device config.
      - State I(replaced) replaces the entire flow monitor configuration.
      - State I(overridden) is equivalent to I(replaced) for this module.
      - State I(deleted) removes the specified (or all) flow monitor entities.
        Deletion order is monitors → exporters → samplers → records to respect dependencies.
      - State I(rendered), I(gathered) and I(parsed) do not perform any change on the device.
    type: str
"""

EXAMPLES = """
# Using state: merged

# Before state:
# router# show running-config | section ^(flow|sampler)
# (empty)

- name: Configure Flexible NetFlow (Catalyst 9600 and routers, see the notes for Catalyst 9300)
  cisco.ios.ios_flow_monitor:
    config:
      records:
        - name: FLOW_RECORD_IPV4
          match:
            ipv4_tos: true
            ipv4_protocol: true
            ipv4_source_address: true
            ipv4_destination_address: true
            transport_source_port: true
            transport_destination_port: true
            flow_direction: true
            interface_output: true
          collect:
            routing_source_as_4octet: true
            routing_destination_as_4octet: true
            routing_next_hop_ipv4: true
            transport_tcp_flags: true
            counter_bytes: true
            counter_packets: true
            timestamp_sys_uptime_first: true
            timestamp_sys_uptime_last: true
            interface_input: true
      exporters:
        - name: FLOW_EXPORTER_1
          destination: 192.0.2.1
          vrf: MGMT
          source: Loopback0
          transport:
            protocol: udp
            port: 2055
          options:
            sampler_table_timeout: 10
      samplers:
        - name: FLOW_SAMPLER
          mode: random
          window_size: 1000
      monitors:
        - name: FLOW_MONITOR_OUT
          exporters:
            - FLOW_EXPORTER_1
          cache:
            timeout_inactive: 10
            timeout_active: 60
          record: FLOW_RECORD_IPV4
    state: merged

# Commands fired:
# flow record FLOW_RECORD_IPV4
#  match ipv4 tos
#  match ipv4 protocol
#  match ipv4 source address
#  match ipv4 destination address
#  match transport source-port
#  match transport destination-port
#  match flow direction
#  match interface output
#  collect routing source as 4-octet
#  collect routing destination as 4-octet
#  collect routing next-hop address ipv4
#  collect transport tcp flags
#  collect counter bytes
#  collect counter packets
#  collect timestamp sys-uptime first
#  collect timestamp sys-uptime last
#  collect interface input
# flow exporter FLOW_EXPORTER_1
#  destination 192.0.2.1 vrf MGMT
#  source Loopback0
#  transport udp 2055
#  option sampler-table timeout 10
# sampler FLOW_SAMPLER
#  mode random 1 out-of 1000
# flow monitor FLOW_MONITOR_OUT
#  exporter FLOW_EXPORTER_1
#  cache timeout inactive 10
#  cache timeout active 60
#  record FLOW_RECORD_IPV4

# Using state: merged — Catalyst 9300 flow record
#
# Catalyst 9300 rejects the counter_bytes, counter_packets and timestamp_sys_uptime options
# used in the first example, it needs the long counters and absolute timestamps.

- name: Configure a flow record on a Catalyst 9300
  cisco.ios.ios_flow_monitor:
    config:
      records:
        - name: FLOW_RECORD_IPV4
          match:
            ipv4_tos: true
            ipv4_protocol: true
            ipv4_source_address: true
            ipv4_destination_address: true
            transport_source_port: true
            transport_destination_port: true
            flow_direction: true
            interface_output: true
          collect:
            routing_source_as_4octet: true
            routing_destination_as_4octet: true
            routing_next_hop_ipv4: true
            transport_tcp_flags: true
            counter_bytes_layer2_long: true
            counter_packets_long: true
            timestamp_absolute_first: true
            timestamp_absolute_last: true
            interface_input: true
    state: merged

# Commands fired:
# flow record FLOW_RECORD_IPV4
#  match ipv4 tos
#  match ipv4 protocol
#  match ipv4 source address
#  match ipv4 destination address
#  match transport source-port
#  match transport destination-port
#  match flow direction
#  match interface output
#  collect routing source as 4-octet
#  collect routing destination as 4-octet
#  collect routing next-hop address ipv4
#  collect transport tcp flags
#  collect counter bytes layer2 long
#  collect counter packets long
#  collect timestamp absolute first
#  collect timestamp absolute last
#  collect interface input

# Using state: merged — dual exporter (two collectors)

- name: Configure flow monitor with dual exporters
  cisco.ios.ios_flow_monitor:
    config:
      exporters:
        - name: FLOW_EXPORTER_1
          destination: 192.0.2.1
          vrf: MGMT
          source: Loopback0
          transport:
            protocol: udp
            port: 9996
          options:
            sampler_table_timeout: 2000
            template_data_timeout: 10000
        - name: FLOW_EXPORTER_2
          destination: 192.0.2.2
          vrf: MGMT
          source: Loopback0
          transport:
            protocol: udp
            port: 9996
          options:
            sampler_table_timeout: 2000
            template_data_timeout: 10000
      monitors:
        - name: FLOW_MONITOR_IN
          exporters:
            - FLOW_EXPORTER_1
            - FLOW_EXPORTER_2
          record: FLOW_RECORD_IPV4
    state: merged

# Using state: deleted

- name: Remove all flow monitor configuration
  cisco.ios.ios_flow_monitor:
    state: deleted

# Using state: gathered

- name: Gather existing flow monitor configuration
  cisco.ios.ios_flow_monitor:
    state: gathered

# Using state: rendered

- name: Render commands without connecting to device
  cisco.ios.ios_flow_monitor:
    config:
      samplers:
        - name: FLOW_SAMPLER
          mode: random
          window_size: 1000
    state: rendered

# Using state: parsed

- name: Parse device config into structured data
  cisco.ios.ios_flow_monitor:
    running_config: |
      flow record FLOW_RECORD_IPV4
       match ipv4 source address
       match ipv4 destination address
       collect counter bytes
       collect counter packets
      sampler FLOW_SAMPLER
       mode random 1 out-of 1000
      flow monitor FLOW_MONITOR_OUT
       record FLOW_RECORD_IPV4
    state: parsed
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
after:
  description: The resulting configuration module invocation.
  returned: when changed
  type: dict
  sample: >
    The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample:
    - flow record FLOW_RECORD_IPV4
    - " match ipv4 source address"
    - " collect counter bytes"
rendered:
  description: The set of CLI commands generated from the value of I(state=rendered) option.
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - flow record FLOW_RECORD_IPV4
    - " match ipv4 source address"
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option, parsed into structured data.
  returned: when I(state) is C(parsed)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    emit_warnings,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.flow_monitor.flow_monitor import (
    Flow_monitorArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.flow_monitor.flow_monitor import (
    Flow_monitor,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Flow_monitorArgs.argument_spec,
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

    result = Flow_monitor(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
