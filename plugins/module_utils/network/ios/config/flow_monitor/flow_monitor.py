# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_flow_monitor config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.flow_monitor import (
    Flow_monitorTemplate,
)


# Values that IOS-XE omits from the running config because they are the default
CACHE_TIMEOUT_DEFAULTS = {"timeout_inactive": 15, "timeout_active": 1800}
EXPORTER_DEFAULTS = {
    "export_protocol": "netflow-v9",
    "template_data_timeout": 600,
    "ttl": 255,
    "dscp": 0,
}


class Flow_monitor(ResourceModule):
    """
    The ios_flow_monitor config class
    """

    _MATCH_CLI = [
        ("ipv4_tos", "match ipv4 tos"),
        ("ipv4_protocol", "match ipv4 protocol"),
        ("ipv4_source_address", "match ipv4 source address"),
        ("ipv4_destination_address", "match ipv4 destination address"),
        ("ipv4_ttl", "match ipv4 ttl"),
        ("ipv4_version", "match ipv4 version"),
        ("transport_source_port", "match transport source-port"),
        ("transport_destination_port", "match transport destination-port"),
        ("transport_icmp_ipv4_code", "match transport icmp ipv4 code"),
        ("transport_icmp_ipv4_type", "match transport icmp ipv4 type"),
        ("transport_icmp_ipv6_code", "match transport icmp ipv6 code"),
        ("transport_icmp_ipv6_type", "match transport icmp ipv6 type"),
        ("flow_direction", "match flow direction"),
        ("interface_input", "match interface input"),
        ("interface_output", "match interface output"),
        ("routing_vrf_input", "match routing vrf input"),
        ("ipv6_source_address", "match ipv6 source address"),
        ("ipv6_destination_address", "match ipv6 destination address"),
        ("ipv6_hop_limit", "match ipv6 hop-limit"),
        ("ipv6_protocol", "match ipv6 protocol"),
        ("ipv6_traffic_class", "match ipv6 traffic-class"),
        ("ipv6_version", "match ipv6 version"),
        ("datalink_dot1q_priority", "match datalink dot1q priority"),
        ("datalink_dot1q_vlan_input", "match datalink dot1q vlan input"),
        ("datalink_dot1q_vlan_output", "match datalink dot1q vlan output"),
        ("datalink_ethertype", "match datalink ethertype"),
        ("datalink_mac_destination_input", "match datalink mac destination address input"),
        ("datalink_mac_destination_output", "match datalink mac destination address output"),
        ("datalink_mac_source_input", "match datalink mac source address input"),
        ("datalink_mac_source_output", "match datalink mac source address output"),
        ("datalink_vlan_input", "match datalink vlan input"),
        ("datalink_vlan_output", "match datalink vlan output"),
        ("application_name", "match application name"),
    ]

    _COLLECT_CLI = [
        ("routing_source_as_4octet", "collect routing source as 4-octet"),
        ("routing_source_as_peer", "collect routing source as peer"),
        ("routing_destination_as_4octet", "collect routing destination as 4-octet"),
        ("routing_destination_as_peer", "collect routing destination as peer"),
        ("routing_next_hop_ipv4", "collect routing next-hop address ipv4"),
        ("routing_next_hop_ipv6", "collect routing next-hop address ipv6"),
        ("transport_tcp_flags", "collect transport tcp flags"),
        ("transport_destination_port", "collect transport destination-port"),
        ("transport_source_port", "collect transport source-port"),
        ("counter_bytes_long", "collect counter bytes long"),
        ("counter_bytes_layer2", "collect counter bytes layer2"),
        ("counter_packets_long", "collect counter packets long"),
        ("timestamp_sys_uptime_first", "collect timestamp sys-uptime first"),
        ("timestamp_sys_uptime_last", "collect timestamp sys-uptime last"),
        ("timestamp_absolute_first", "collect timestamp absolute first"),
        ("timestamp_absolute_last", "collect timestamp absolute last"),
        ("interface_input", "collect interface input"),
        ("interface_output", "collect interface output"),
        ("ipv4_source_address", "collect ipv4 source address"),
        ("ipv4_source_mask", "collect ipv4 source mask"),
        ("ipv4_source_prefix", "collect ipv4 source prefix"),
        ("ipv4_destination_address", "collect ipv4 destination address"),
        ("ipv4_destination_mask", "collect ipv4 destination mask"),
        ("ipv4_destination_prefix", "collect ipv4 destination prefix"),
        ("ipv4_protocol", "collect ipv4 protocol"),
        ("ipv4_version", "collect ipv4 version"),
        ("ipv6_source_address", "collect ipv6 source address"),
        ("ipv6_source_mask", "collect ipv6 source mask"),
        ("ipv6_source_prefix", "collect ipv6 source prefix"),
        ("ipv6_destination_address", "collect ipv6 destination address"),
        ("ipv6_destination_mask", "collect ipv6 destination mask"),
        ("ipv6_destination_prefix", "collect ipv6 destination prefix"),
        ("ipv6_protocol", "collect ipv6 protocol"),
        ("ipv6_version", "collect ipv6 version"),
        ("datalink_dot1q_vlan_input", "collect datalink dot1q vlan input"),
        ("datalink_dot1q_vlan_output", "collect datalink dot1q vlan output"),
        ("datalink_mac_destination_input", "collect datalink mac destination address input"),
        ("datalink_mac_destination_output", "collect datalink mac destination address output"),
        ("datalink_mac_source_input", "collect datalink mac source address input"),
        ("datalink_mac_source_output", "collect datalink mac source address output"),
        ("flow_sampler", "collect flow sampler"),
    ]

    def __init__(self, module):
        super(Flow_monitor, self).__init__(
            empty_fact_val={"records": [], "exporters": [], "samplers": [], "monitors": []},
            facts_module=Facts(module),
            module=module,
            resource="flow_monitor",
            tmplt=Flow_monitorTemplate(),
        )
        self.parsers = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands based on want, have and state."""
        wantd = self._entities_to_dict(self.want or {})
        haved = self._entities_to_dict(self.have or {})

        if self.state == "deleted":
            # Remove everything that is in have (or only what's named in want if want given)
            if wantd and any(wantd[k] for k in wantd):
                # Selective delete: only remove named entities
                del_monitors = {
                    k: v for k, v in haved["monitors"].items() if k in wantd["monitors"]
                }
                del_exporters = {
                    k: v for k, v in haved["exporters"].items() if k in wantd["exporters"]
                }
                del_samplers = {
                    k: v for k, v in haved["samplers"].items() if k in wantd["samplers"]
                }
                del_records = {k: v for k, v in haved["records"].items() if k in wantd["records"]}
            else:
                # Delete all
                del_monitors = haved["monitors"]
                del_exporters = haved["exporters"]
                del_samplers = haved["samplers"]
                del_records = haved["records"]

            # Deletion order: monitors → exporters → samplers → records
            for name in del_monitors:
                self.commands.append("no flow monitor {0}".format(name))
            for name in del_exporters:
                self.commands.append("no flow exporter {0}".format(name))
            for name in del_samplers:
                self.commands.append("no sampler {0}".format(name))
            for name in del_records:
                self.commands.append("no flow record {0}".format(name))
            return

        if self.state in ["overridden", "replaced"]:
            # Remove entities in have that are not in want
            # Deletion order: monitors → exporters → samplers → records
            for name in haved["monitors"]:
                if name not in wantd["monitors"]:
                    self.commands.append("no flow monitor {0}".format(name))
            for name in haved["exporters"]:
                if name not in wantd["exporters"]:
                    self.commands.append("no flow exporter {0}".format(name))
            for name in haved["samplers"]:
                if name not in wantd["samplers"]:
                    self.commands.append("no sampler {0}".format(name))
            for name in haved["records"]:
                if name not in wantd["records"]:
                    self.commands.append("no flow record {0}".format(name))

        # Add/update in dependency order: records → samplers → exporters → monitors
        for name, want_rec in wantd["records"].items():
            have_rec = haved["records"].get(name, {})
            if want_rec != have_rec:
                if have_rec and self.state in ["replaced", "overridden"]:
                    self.commands.extend(self._record_diff_commands(name, want_rec, have_rec))
                else:
                    self.commands.extend(self._record_commands(name, want_rec))

        for name, want_smp in wantd["samplers"].items():
            have_smp = haved["samplers"].get(name, {})
            if want_smp != have_smp:
                self.commands.extend(self._sampler_commands(name, want_smp))

        for name, want_exp in wantd["exporters"].items():
            have_exp = haved["exporters"].get(name, {})
            if self._without_defaults(want_exp, EXPORTER_DEFAULTS) != self._without_defaults(
                have_exp,
                EXPORTER_DEFAULTS,
            ):
                self.commands.extend(self._exporter_commands(name, want_exp))

        for name, want_mon in wantd["monitors"].items():
            have_mon = haved["monitors"].get(name, {})
            if self._normalize_monitor(want_mon) != self._normalize_monitor(have_mon):
                if have_mon and self.state in ["replaced", "overridden"]:
                    self.commands.extend(self._monitor_diff_commands(name, want_mon, have_mon))
                else:
                    self.commands.extend(self._monitor_commands(name, want_mon))

    # ── default value handling ──────────────────────────────────────────────

    @staticmethod
    def _without_defaults(data, defaults):
        """Return a copy of data without the keys whose value is the IOS default."""
        return {k: v for k, v in data.items() if k not in defaults or v != defaults[k]}

    def _normalize_monitor(self, mon):
        """Return the monitor without default cache timeouts, as IOS does not show them."""
        mon = dict(mon)
        cache = self._without_defaults(mon.get("cache", {}), CACHE_TIMEOUT_DEFAULTS)
        if cache:
            mon["cache"] = cache
        else:
            mon.pop("cache", None)
        return mon

    # ── command builders ────────────────────────────────────────────────────

    def _record_commands(self, name, rec):
        cmds = ["flow record {0}".format(name)]
        match = rec.get("match", {})
        collect = rec.get("collect", {})
        for key, cli in self._MATCH_CLI:
            if match.get(key):
                cmds.append(" {0}".format(cli))
        for key, cli in self._COLLECT_CLI:
            if collect.get(key):
                cmds.append(" {0}".format(cli))
        return cmds

    def _record_diff_commands(self, name, want_rec, have_rec):
        """Emit minimal in-place update for replaced/overridden — add new fields, remove dropped ones."""
        cmds = ["flow record {0}".format(name)]
        want_match = want_rec.get("match", {})
        have_match = have_rec.get("match", {})
        want_collect = want_rec.get("collect", {})
        have_collect = have_rec.get("collect", {})
        for key, cli in self._MATCH_CLI:
            if have_match.get(key) and not want_match.get(key):
                cmds.append(" no {0}".format(cli))
            elif want_match.get(key) and not have_match.get(key):
                cmds.append(" {0}".format(cli))
        for key, cli in self._COLLECT_CLI:
            if have_collect.get(key) and not want_collect.get(key):
                cmds.append(" no {0}".format(cli))
            elif want_collect.get(key) and not have_collect.get(key):
                cmds.append(" {0}".format(cli))
        return cmds

    def _monitor_diff_commands(self, name, want_mon, have_mon):
        """Emit minimal in-place update for replaced/overridden — diff exporter list and scalar fields."""
        cmds = ["flow monitor {0}".format(name)]
        want_exporters = want_mon.get("exporters", [])
        have_exporters = have_mon.get("exporters", [])
        have_exp_set = set(have_exporters)
        want_exp_set = set(want_exporters)
        for exp in sorted(have_exp_set - want_exp_set):
            cmds.append(" no exporter {0}".format(exp))
        for exp in [e for e in want_exporters if e not in have_exp_set]:
            cmds.append(" exporter {0}".format(exp))
        want_desc = want_mon.get("description")
        have_desc = have_mon.get("description")
        if want_desc != have_desc:
            if want_desc:
                cmds.append(" description {0}".format(want_desc))
            else:
                cmds.append(" no description")
        want_cache = want_mon.get("cache", {})
        have_cache = have_mon.get("cache", {})
        if want_cache != have_cache:
            for field, cmd in [
                ("type", "cache type"),
                ("entries", "cache entries"),
                ("timeout_inactive", "cache timeout inactive"),
                ("timeout_active", "cache timeout active"),
                ("timeout_update", "cache timeout update"),
            ]:
                wv = want_cache.get(field)
                hv = have_cache.get(field)
                if hv is None:
                    # IOS does not show default values in the running config
                    hv = CACHE_TIMEOUT_DEFAULTS.get(field)
                if wv != hv and wv is not None:
                    cmds.append(" {0} {1}".format(cmd, wv))
        if want_mon.get("record") != have_mon.get("record") and want_mon.get("record"):
            cmds.append(" record {0}".format(want_mon["record"]))
        return cmds

    def _exporter_commands(self, name, exp):
        cmds = ["flow exporter {0}".format(name)]
        if exp.get("description"):
            cmds.append(" description {0}".format(exp["description"]))
        if exp.get("destination"):
            line = " destination {0}".format(exp["destination"])
            if exp.get("vrf"):
                line += " vrf {0}".format(exp["vrf"])
            cmds.append(line)
        if exp.get("source"):
            cmds.append(" source {0}".format(exp["source"]))
        if exp.get("export_protocol"):
            cmds.append(" export-protocol {0}".format(exp["export_protocol"]))
        transport = exp.get("transport", {})
        if transport.get("port"):
            proto = transport.get("protocol", "udp")
            cmds.append(" transport {0} {1}".format(proto, transport["port"]))
        if exp.get("template_data_timeout") is not None:
            cmds.append(" template data timeout {0}".format(exp["template_data_timeout"]))
        if exp.get("ttl") is not None:
            cmds.append(" ttl {0}".format(exp["ttl"]))
        if exp.get("dscp") is not None:
            cmds.append(" dscp {0}".format(exp["dscp"]))
        options = exp.get("options", {})
        if options.get("sampler_table_timeout") is not None:
            cmds.append(
                " option sampler-table timeout {0}".format(options["sampler_table_timeout"]),
            )
        if options.get("template_data_timeout") is not None:
            cmds.append(
                " option template data timeout {0}".format(options["template_data_timeout"]),
            )
        if options.get("interface_table_timeout") is not None:
            cmds.append(
                " option interface-table timeout {0}".format(options["interface_table_timeout"]),
            )
        if options.get("exporter_stats_timeout") is not None:
            cmds.append(
                " option exporter-stats timeout {0}".format(options["exporter_stats_timeout"]),
            )
        if options.get("application_table_timeout") is not None:
            cmds.append(
                " option application-table timeout {0}".format(
                    options["application_table_timeout"],
                ),
            )
        if options.get("vrf_table_timeout") is not None:
            cmds.append(" option vrf-table timeout {0}".format(options["vrf_table_timeout"]))
        return cmds

    def _sampler_commands(self, name, smp):
        cmds = ["sampler {0}".format(name)]
        if smp.get("description"):
            cmds.append(" description {0}".format(smp["description"]))
        if smp.get("mode") and smp.get("window_size") is not None:
            cmds.append(" mode {0} 1 out-of {1}".format(smp["mode"], smp["window_size"]))
        return cmds

    def _monitor_commands(self, name, mon):
        cmds = ["flow monitor {0}".format(name)]
        if mon.get("description"):
            cmds.append(" description {0}".format(mon["description"]))
        for exp_name in mon.get("exporters", []):
            cmds.append(" exporter {0}".format(exp_name))
        cache = mon.get("cache", {})
        if cache.get("type"):
            cmds.append(" cache type {0}".format(cache["type"]))
        if cache.get("entries") is not None:
            cmds.append(" cache entries {0}".format(cache["entries"]))
        if cache.get("timeout_inactive") is not None:
            cmds.append(" cache timeout inactive {0}".format(cache["timeout_inactive"]))
        if cache.get("timeout_active") is not None:
            cmds.append(" cache timeout active {0}".format(cache["timeout_active"]))
        if cache.get("timeout_update") is not None:
            cmds.append(" cache timeout update {0}".format(cache["timeout_update"]))
        if mon.get("record"):
            cmds.append(" record {0}".format(mon["record"]))
        return cmds

    # ── helpers ─────────────────────────────────────────────────────────────

    def _entities_to_dict(self, config):
        """Convert config dict-of-lists into dicts keyed by name for comparison."""
        return {
            "records": {r["name"]: r for r in config.get("records", [])},
            "exporters": {e["name"]: e for e in config.get("exporters", [])},
            "samplers": {s["name"]: s for s in config.get("samplers", [])},
            "monitors": {m["name"]: m for m in config.get("monitors", [])},
        }
