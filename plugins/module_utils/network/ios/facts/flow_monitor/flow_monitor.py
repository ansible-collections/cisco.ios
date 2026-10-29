# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios flow_monitor fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.flow_monitor.flow_monitor import (
    Flow_monitorArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.flow_monitor import (
    Flow_monitorTemplate,
)


# IOS-XE omits the timeout from an exporter "option" line when it is the default
DEFAULT_OPTION_TIMEOUT = 600

# CLI line -> option name, for the flow record "match" and "collect" fields.
# Every option here must also exist in the argspec, a missing one makes every state fail on a device that has the line.
_MATCH_MAP = {
    "match ipv4 tos": "ipv4_tos",
    "match ipv4 protocol": "ipv4_protocol",
    "match ipv4 source address": "ipv4_source_address",
    "match ipv4 destination address": "ipv4_destination_address",
    "match ipv4 ttl": "ipv4_ttl",
    "match ipv4 version": "ipv4_version",
    "match transport source-port": "transport_source_port",
    "match transport destination-port": "transport_destination_port",
    "match transport icmp ipv4 code": "transport_icmp_ipv4_code",
    "match transport icmp ipv4 type": "transport_icmp_ipv4_type",
    "match transport icmp ipv6 code": "transport_icmp_ipv6_code",
    "match transport icmp ipv6 type": "transport_icmp_ipv6_type",
    "match flow direction": "flow_direction",
    "match interface input": "interface_input",
    "match interface output": "interface_output",
    "match routing vrf input": "routing_vrf_input",
    "match ipv6 source address": "ipv6_source_address",
    "match ipv6 destination address": "ipv6_destination_address",
    "match ipv6 hop-limit": "ipv6_hop_limit",
    "match ipv6 protocol": "ipv6_protocol",
    "match ipv6 traffic-class": "ipv6_traffic_class",
    "match ipv6 version": "ipv6_version",
    "match datalink dot1q priority": "datalink_dot1q_priority",
    "match datalink dot1q vlan input": "datalink_dot1q_vlan_input",
    "match datalink dot1q vlan output": "datalink_dot1q_vlan_output",
    "match datalink ethertype": "datalink_ethertype",
    "match datalink mac destination address input": "datalink_mac_destination_input",
    "match datalink mac destination address output": "datalink_mac_destination_output",
    "match datalink mac source address input": "datalink_mac_source_input",
    "match datalink mac source address output": "datalink_mac_source_output",
    "match datalink vlan input": "datalink_vlan_input",
    "match datalink vlan output": "datalink_vlan_output",
    "match application name": "application_name",
}

_COLLECT_MAP = {
    "collect routing source as 4-octet": "routing_source_as_4octet",
    "collect routing source as peer": "routing_source_as_peer",
    "collect routing source as": "routing_source_as",
    "collect routing destination as 4-octet": "routing_destination_as_4octet",
    "collect routing destination as peer": "routing_destination_as_peer",
    "collect routing destination as": "routing_destination_as",
    "collect routing next-hop address ipv4": "routing_next_hop_ipv4",
    "collect routing next-hop address ipv6": "routing_next_hop_ipv6",
    "collect transport tcp flags": "transport_tcp_flags",
    "collect transport destination-port": "transport_destination_port",
    "collect transport source-port": "transport_source_port",
    "collect counter bytes long": "counter_bytes_long",
    "collect counter bytes layer2": "counter_bytes_layer2",
    "collect counter bytes layer2 long": "counter_bytes_layer2_long",
    "collect counter bytes": "counter_bytes",
    "collect counter packets long": "counter_packets_long",
    "collect counter packets": "counter_packets",
    "collect timestamp sys-uptime first": "timestamp_sys_uptime_first",
    "collect timestamp sys-uptime last": "timestamp_sys_uptime_last",
    "collect timestamp absolute first": "timestamp_absolute_first",
    "collect timestamp absolute last": "timestamp_absolute_last",
    "collect interface input": "interface_input",
    "collect interface output": "interface_output",
    "collect ipv4 source address": "ipv4_source_address",
    "collect ipv4 source mask": "ipv4_source_mask",
    "collect ipv4 source prefix": "ipv4_source_prefix",
    "collect ipv4 destination address": "ipv4_destination_address",
    "collect ipv4 destination mask": "ipv4_destination_mask",
    "collect ipv4 destination prefix": "ipv4_destination_prefix",
    "collect ipv4 protocol": "ipv4_protocol",
    "collect ipv4 version": "ipv4_version",
    "collect ipv6 source address": "ipv6_source_address",
    "collect ipv6 source mask": "ipv6_source_mask",
    "collect ipv6 source prefix": "ipv6_source_prefix",
    "collect ipv6 destination address": "ipv6_destination_address",
    "collect ipv6 destination mask": "ipv6_destination_mask",
    "collect ipv6 destination prefix": "ipv6_destination_prefix",
    "collect ipv6 protocol": "ipv6_protocol",
    "collect ipv6 version": "ipv6_version",
    "collect datalink dot1q vlan input": "datalink_dot1q_vlan_input",
    "collect datalink dot1q vlan output": "datalink_dot1q_vlan_output",
    "collect datalink mac destination address input": "datalink_mac_destination_input",
    "collect datalink mac destination address output": "datalink_mac_destination_output",
    "collect datalink mac source address input": "datalink_mac_source_input",
    "collect datalink mac source address output": "datalink_mac_source_output",
    "collect flow sampler": "flow_sampler",
}


class Flow_monitorFacts(object):
    """The ios flow_monitor facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Flow_monitorArgs.argument_spec

    def get_flow_monitor_data(self, connection):
        return connection.get("show running-config | section ^(flow|sampler)")

    def _parse_flow_config(self, data):
        """Custom block parser that handles the multi-exporter list correctly."""
        records = {}
        exporters = {}
        samplers = {}
        monitors = {}

        current_type = None
        current_name = None

        for raw_line in data.splitlines():
            line = raw_line.rstrip()

            # ── block openers (non-indented) ──────────────────────────────
            m = re.match(r"^flow record (\S+)$", line)
            if m:
                current_type = "records"
                current_name = m.group(1)
                records[current_name] = {"name": current_name, "match": {}, "collect": {}}
                continue

            m = re.match(r"^flow exporter (\S+)$", line)
            if m:
                current_type = "exporters"
                current_name = m.group(1)
                exporters[current_name] = {"name": current_name}
                continue

            m = re.match(r"^sampler (\S+)$", line)
            if m:
                current_type = "samplers"
                current_name = m.group(1)
                samplers[current_name] = {"name": current_name}
                continue

            m = re.match(r"^flow monitor (\S+)$", line)
            if m:
                current_type = "monitors"
                current_name = m.group(1)
                monitors[current_name] = {"name": current_name, "exporters": []}
                continue

            # ── sub-commands (indented) ────────────────────────────────────
            if not line.startswith(" ") or current_name is None:
                continue

            stripped = line.strip()

            if current_type == "records":
                rec = records[current_name]
                if stripped in _MATCH_MAP:
                    rec["match"][_MATCH_MAP[stripped]] = True
                elif stripped in _COLLECT_MAP:
                    rec["collect"][_COLLECT_MAP[stripped]] = True

            elif current_type == "exporters":
                exp = exporters[current_name]
                m = re.match(r"^destination (\S+)(?:\s+vrf (\S+))?$", stripped)
                if m:
                    exp["destination"] = m.group(1)
                    if m.group(2):
                        exp["vrf"] = m.group(2)
                    continue
                m = re.match(r"^source (\S+)$", stripped)
                if m:
                    exp["source"] = m.group(1)
                    continue
                m = re.match(r"^transport (udp|tcp) (\d+)$", stripped)
                if m:
                    exp["transport"] = {"protocol": m.group(1), "port": int(m.group(2))}
                    continue
                m = re.match(r"^export-protocol (\S+)$", stripped)
                if m:
                    exp["export_protocol"] = m.group(1)
                    continue
                m = re.match(r"^template data timeout (\d+)$", stripped)
                if m:
                    exp["template_data_timeout"] = int(m.group(1))
                    continue
                m = re.match(r"^ttl (\d+)$", stripped)
                if m:
                    exp["ttl"] = int(m.group(1))
                    continue
                m = re.match(r"^dscp (\d+)$", stripped)
                if m:
                    exp["dscp"] = int(m.group(1))
                    continue
                m = re.match(r"^option sampler-table(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["sampler_table_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^option template data(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["template_data_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^option interface-table(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["interface_table_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^option exporter-stats(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["exporter_stats_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^option application-table(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["application_table_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^option vrf-table(?: timeout (\d+))?$", stripped)
                if m:
                    exp.setdefault("options", {})["vrf_table_timeout"] = (
                        int(m.group(1)) if m.group(1) else DEFAULT_OPTION_TIMEOUT
                    )
                    continue
                m = re.match(r"^description (.+)$", stripped)
                if m:
                    exp["description"] = m.group(1)
                    continue

            elif current_type == "samplers":
                smp = samplers[current_name]
                m = re.match(r"^mode (random|deterministic) 1 out-of (\d+)$", stripped)
                if m:
                    smp["mode"] = m.group(1)
                    smp["window_size"] = int(m.group(2))

            elif current_type == "monitors":
                mon = monitors[current_name]
                m = re.match(r"^exporter (\S+)$", stripped)
                if m:
                    mon["exporters"].append(m.group(1))
                    continue
                m = re.match(r"^record (\S+)$", stripped)
                if m:
                    mon["record"] = m.group(1)
                    continue
                m = re.match(r"^cache timeout inactive (\d+)$", stripped)
                if m:
                    mon.setdefault("cache", {})["timeout_inactive"] = int(m.group(1))
                    continue
                m = re.match(r"^cache timeout active (\d+)$", stripped)
                if m:
                    mon.setdefault("cache", {})["timeout_active"] = int(m.group(1))
                    continue
                m = re.match(r"^cache timeout update (\d+)$", stripped)
                if m:
                    mon.setdefault("cache", {})["timeout_update"] = int(m.group(1))
                    continue
                m = re.match(r"^cache type (\S+)$", stripped)
                if m:
                    mon.setdefault("cache", {})["type"] = m.group(1)
                    continue
                m = re.match(r"^cache entries (\d+)$", stripped)
                if m:
                    mon.setdefault("cache", {})["entries"] = int(m.group(1))
                    continue
                m = re.match(r"^description (.+)$", stripped)
                if m:
                    mon["description"] = m.group(1)
                    continue

        return {
            "records": list(records.values()),
            "exporters": list(exporters.values()),
            "samplers": list(samplers.values()),
            "monitors": list(monitors.values()),
        }

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Flow_monitor network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_flow_monitor_data(connection)

        objs = self._parse_flow_config(data)

        # Remove empty sub-dicts from records
        for rec in objs.get("records", []):
            if not rec.get("match"):
                rec.pop("match", None)
            if not rec.get("collect"):
                rec.pop("collect", None)

        # Remove empty exporters list from monitors
        for mon in objs.get("monitors", []):
            if not mon.get("exporters"):
                mon.pop("exporters", None)

        ansible_facts["ansible_network_resources"].pop("flow_monitor", None)

        tmplt = Flow_monitorTemplate(module=self._module)
        params = utils.remove_empties(
            tmplt.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["flow_monitor"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
