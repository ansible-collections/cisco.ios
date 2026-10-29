#
# (c) 2025, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_flow_monitor
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosFlowMonitorModule(TestIosModule):
    module = ios_flow_monitor

    def setUp(self):
        super(TestIosFlowMonitorModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.flow_monitor.flow_monitor."
            "Flow_monitorFacts.get_flow_monitor_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosFlowMonitorModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    # ── merged ───────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_merged(self):
        """Merge a full Akvorado-style stack onto an empty device."""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "FLOW_RECORD_IPV4",
                            "match": {
                                "ipv4_tos": True,
                                "ipv4_protocol": True,
                                "ipv4_source_address": True,
                                "ipv4_destination_address": True,
                                "transport_source_port": True,
                                "transport_destination_port": True,
                                "flow_direction": True,
                                "interface_output": True,
                            },
                            "collect": {
                                "routing_source_as_4octet": True,
                                "routing_destination_as_4octet": True,
                                "routing_next_hop_ipv4": True,
                                "transport_tcp_flags": True,
                                "counter_bytes_long": True,
                                "counter_packets_long": True,
                                "timestamp_sys_uptime_first": True,
                                "timestamp_sys_uptime_last": True,
                                "interface_input": True,
                            },
                        },
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                            "options": {"sampler_table_timeout": 10},
                        },
                    ],
                    "samplers": [
                        {
                            "name": "FLOW_SAMPLER",
                            "mode": "random",
                            "window_size": 1000,
                        },
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "exporters": ["FLOW_EXPORTER_1"],
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        commands = result["commands"]

        # Check records block
        self.assertIn("flow record FLOW_RECORD_IPV4", commands)
        self.assertIn(" match ipv4 tos", commands)
        self.assertIn(" match ipv4 protocol", commands)
        self.assertIn(" match ipv4 source address", commands)
        self.assertIn(" match ipv4 destination address", commands)
        self.assertIn(" match transport source-port", commands)
        self.assertIn(" match transport destination-port", commands)
        self.assertIn(" match flow direction", commands)
        self.assertIn(" match interface output", commands)
        self.assertIn(" collect routing source as 4-octet", commands)
        self.assertIn(" collect counter bytes long", commands)
        self.assertIn(" collect timestamp sys-uptime first", commands)

        # Check exporter block
        self.assertIn("flow exporter FLOW_EXPORTER_1", commands)
        self.assertIn(" destination 192.0.2.1 vrf MGMT", commands)
        self.assertIn(" source Loopback0", commands)
        self.assertIn(" transport udp 2055", commands)
        self.assertIn(" option sampler-table timeout 10", commands)

        # Check sampler
        self.assertIn("sampler FLOW_SAMPLER", commands)
        self.assertIn(" mode random 1 out-of 1000", commands)

        # Check monitor
        self.assertIn("flow monitor FLOW_MONITOR_OUT", commands)
        self.assertIn(" exporter FLOW_EXPORTER_1", commands)
        self.assertIn(" cache timeout inactive 10", commands)
        self.assertIn(" cache timeout active 60", commands)
        self.assertIn(" record FLOW_RECORD_IPV4", commands)

    def test_ios_flow_monitor_merged_idempotent(self):
        """Merging the same config that's already on the device must produce no commands."""
        self.execute_show_command.return_value = dedent(
            """\
            flow record FLOW_RECORD_IPV4
             match ipv4 tos
             match ipv4 protocol
             match ipv4 source address
             match ipv4 destination address
             match transport source-port
             match transport destination-port
             match flow direction
             match interface output
             collect routing source as 4-octet
             collect routing destination as 4-octet
             collect routing next-hop address ipv4
             collect transport tcp flags
             collect counter bytes long
             collect counter packets long
             collect timestamp sys-uptime first
             collect timestamp sys-uptime last
             collect interface input
            flow exporter FLOW_EXPORTER_1
             destination 192.0.2.1 vrf MGMT
             source Loopback0
             transport udp 2055
             option sampler-table timeout 10
            sampler FLOW_SAMPLER
             mode random 1 out-of 1000
            flow monitor FLOW_MONITOR_OUT
             exporter FLOW_EXPORTER_1
             cache timeout inactive 10
             cache timeout active 60
             record FLOW_RECORD_IPV4
            """,
        )
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "FLOW_RECORD_IPV4",
                            "match": {
                                "ipv4_tos": True,
                                "ipv4_protocol": True,
                                "ipv4_source_address": True,
                                "ipv4_destination_address": True,
                                "transport_source_port": True,
                                "transport_destination_port": True,
                                "flow_direction": True,
                                "interface_output": True,
                            },
                            "collect": {
                                "routing_source_as_4octet": True,
                                "routing_destination_as_4octet": True,
                                "routing_next_hop_ipv4": True,
                                "transport_tcp_flags": True,
                                "counter_bytes_long": True,
                                "counter_packets_long": True,
                                "timestamp_sys_uptime_first": True,
                                "timestamp_sys_uptime_last": True,
                                "interface_input": True,
                            },
                        },
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                            "options": {"sampler_table_timeout": 10},
                        },
                    ],
                    "samplers": [
                        {
                            "name": "FLOW_SAMPLER",
                            "mode": "random",
                            "window_size": 1000,
                        },
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "exporters": ["FLOW_EXPORTER_1"],
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # ── deleted ──────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_deleted(self):
        """Delete all flow monitor config — deletion order must be monitors→exporters→samplers→records."""
        self.execute_show_command.return_value = dedent(
            """\
            flow record FLOW_RECORD_IPV4
             match ipv4 source address
             collect counter bytes long
            flow exporter FLOW_EXPORTER_1
             destination 192.0.2.1 vrf MGMT
             transport udp 2055
            sampler FLOW_SAMPLER
             mode random 1 out-of 1000
            flow monitor FLOW_MONITOR_OUT
             exporter FLOW_EXPORTER_1
             record FLOW_RECORD_IPV4
            """,
        )
        set_module_args({"state": "deleted"})
        result = self.execute_module(changed=True)
        commands = result["commands"]

        # Verify all four no-commands are present
        self.assertIn("no flow monitor FLOW_MONITOR_OUT", commands)
        self.assertIn("no flow exporter FLOW_EXPORTER_1", commands)
        self.assertIn("no sampler FLOW_SAMPLER", commands)
        self.assertIn("no flow record FLOW_RECORD_IPV4", commands)

        # Verify dependency order: monitor before exporter before sampler before record
        mon_idx = commands.index("no flow monitor FLOW_MONITOR_OUT")
        exp_idx = commands.index("no flow exporter FLOW_EXPORTER_1")
        smp_idx = commands.index("no sampler FLOW_SAMPLER")
        rec_idx = commands.index("no flow record FLOW_RECORD_IPV4")
        self.assertLess(mon_idx, exp_idx)
        self.assertLess(exp_idx, smp_idx)
        self.assertLess(smp_idx, rec_idx)

    # ── dual exporter ─────────────────────────────────────────────────────────

    def test_ios_flow_monitor_dual_exporter(self):
        """Monitor referencing two exporters (DNB-style pattern)."""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            {
                "config": {
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 9996},
                            "options": {
                                "sampler_table_timeout": 2000,
                                "template_data_timeout": 10000,
                            },
                        },
                        {
                            "name": "FLOW_EXPORTER_2",
                            "destination": "192.0.2.2",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 9996},
                            "options": {
                                "sampler_table_timeout": 2000,
                                "template_data_timeout": 10000,
                            },
                        },
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_IN",
                            "exporters": ["FLOW_EXPORTER_1", "FLOW_EXPORTER_2"],
                            "record": "FLOW_RECORD_IPV4",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        commands = result["commands"]

        self.assertIn("flow monitor FLOW_MONITOR_IN", commands)
        self.assertIn(" exporter FLOW_EXPORTER_1", commands)
        self.assertIn(" exporter FLOW_EXPORTER_2", commands)
        self.assertIn(" option template data timeout 10000", commands)

    # ── monitor without exporter ─────────────────────────────────────────────

    def test_ios_flow_monitor_monitor_no_exporter(self):
        """Monitor defined without any exporter (INT-router pattern)."""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "FLOW_RECORD_IPV4",
                            "match": {"ipv4_source_address": True},
                            "collect": {"counter_bytes_long": True},
                        },
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        commands = result["commands"]

        self.assertIn("flow monitor FLOW_MONITOR_OUT", commands)
        self.assertNotIn(" exporter", [c for c in commands if c.startswith(" exporter")])
        self.assertIn(" record FLOW_RECORD_IPV4", commands)

    # ── parsed ───────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_parsed(self):
        """Feed raw config string, assert structured output."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    flow record FLOW_RECORD_IPV4
                     match ipv4 tos
                     match ipv4 protocol
                     match ipv4 source address
                     match ipv4 destination address
                     match transport source-port
                     match transport destination-port
                     match flow direction
                     match interface output
                     collect routing source as 4-octet
                     collect counter bytes long
                     collect counter packets long
                    flow exporter FLOW_EXPORTER_1
                     destination 192.0.2.1 vrf MGMT
                     source Loopback0
                     transport udp 2055
                     option sampler-table timeout 10
                    sampler FLOW_SAMPLER
                     mode random 1 out-of 1000
                    flow monitor FLOW_MONITOR_OUT
                     exporter FLOW_EXPORTER_1
                     cache timeout inactive 10
                     cache timeout active 60
                     record FLOW_RECORD_IPV4
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed = result["parsed"]

        self.assertEqual(len(parsed["records"]), 1)
        self.assertEqual(parsed["records"][0]["name"], "FLOW_RECORD_IPV4")
        self.assertTrue(parsed["records"][0]["match"]["ipv4_tos"])
        self.assertTrue(parsed["records"][0]["collect"]["counter_bytes_long"])

        self.assertEqual(len(parsed["exporters"]), 1)
        exp = parsed["exporters"][0]
        self.assertEqual(exp["name"], "FLOW_EXPORTER_1")
        self.assertEqual(exp["destination"], "192.0.2.1")
        self.assertEqual(exp["vrf"], "MGMT")
        self.assertEqual(exp["transport"]["protocol"], "udp")
        self.assertEqual(exp["transport"]["port"], 2055)
        self.assertEqual(exp["options"]["sampler_table_timeout"], 10)

        self.assertEqual(len(parsed["samplers"]), 1)
        smp = parsed["samplers"][0]
        self.assertEqual(smp["name"], "FLOW_SAMPLER")
        self.assertEqual(smp["mode"], "random")
        self.assertEqual(smp["window_size"], 1000)

        self.assertEqual(len(parsed["monitors"]), 1)
        mon = parsed["monitors"][0]
        self.assertEqual(mon["name"], "FLOW_MONITOR_OUT")
        self.assertEqual(mon["exporters"], ["FLOW_EXPORTER_1"])
        self.assertEqual(mon["cache"]["timeout_inactive"], 10)
        self.assertEqual(mon["cache"]["timeout_active"], 60)
        self.assertEqual(mon["record"], "FLOW_RECORD_IPV4")

    # ── rendered ─────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_rendered(self):
        """No device connection, render commands from config."""
        set_module_args(
            dict(
                config={
                    "samplers": [
                        {
                            "name": "FLOW_SAMPLER",
                            "mode": "random",
                            "window_size": 1000,
                        },
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                        },
                    ],
                },
                state="rendered",
            ),
        )
        result = self.execute_module(changed=False)
        rendered = result["rendered"]

        self.assertIn("sampler FLOW_SAMPLER", rendered)
        self.assertIn(" mode random 1 out-of 1000", rendered)
        self.assertIn("flow exporter FLOW_EXPORTER_1", rendered)
        self.assertIn(" destination 192.0.2.1 vrf MGMT", rendered)
        self.assertIn(" source Loopback0", rendered)
        self.assertIn(" transport udp 2055", rendered)

    # ── dual exporter parsed ────────────────────────────────────────────────

    def test_ios_flow_monitor_parsed_dual_exporter(self):
        """Dual-exporter monitor is parsed into a list with two entries."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    flow monitor FLOW_MONITOR_IN
                     exporter FLOW_EXPORTER_1
                     exporter FLOW_EXPORTER_2
                     cache timeout inactive 10
                     cache timeout active 60
                     record FLOW_RECORD_IPV4
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        mon = result["parsed"]["monitors"][0]
        self.assertEqual(mon["exporters"], ["FLOW_EXPORTER_1", "FLOW_EXPORTER_2"])

    # ── values IOS-XE omits from the running config because they are defaults ──

    _DEFAULTS_HAVE = dedent(
        """\
        flow record REC
         match ipv4 protocol
         collect counter bytes long
        flow exporter EXP
         destination 192.0.2.1
         transport udp 9995
         option interface-table
         option exporter-stats
         option vrf-table
         option sampler-table
         option application-table
        flow monitor MON
         exporter EXP
         cache timeout active 90
         record REC
        """,
    )

    def _defaults_config(self):
        return {
            "records": [
                {
                    "name": "REC",
                    "match": {"ipv4_protocol": True},
                    "collect": {"counter_bytes_long": True},
                },
            ],
            "exporters": [
                {
                    "name": "EXP",
                    "destination": "192.0.2.1",
                    "export_protocol": "netflow-v9",
                    "template_data_timeout": 600,
                    "ttl": 255,
                    "dscp": 0,
                    "transport": {"protocol": "udp", "port": 9995},
                    "options": {
                        "interface_table_timeout": 600,
                        "exporter_stats_timeout": 600,
                        "vrf_table_timeout": 600,
                        "sampler_table_timeout": 600,
                        "application_table_timeout": 600,
                    },
                },
            ],
            "monitors": [
                {
                    "name": "MON",
                    "exporters": ["EXP"],
                    "cache": {"timeout_inactive": 15, "timeout_active": 90},
                    "record": "REC",
                },
            ],
        }

    def test_ios_flow_monitor_merged_idempotent_default_values(self):
        """Values equal to the IOS default are not shown in the running config and must not cause a diff."""
        self.execute_show_command.return_value = self._DEFAULTS_HAVE
        set_module_args({"config": self._defaults_config(), "state": "merged"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_flow_monitor_replaced_idempotent_default_values(self):
        self.execute_show_command.return_value = self._DEFAULTS_HAVE
        set_module_args({"config": self._defaults_config(), "state": "replaced"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_flow_monitor_changed_from_default_is_applied(self):
        """A value that differs from the default (and from the device) is still configured."""
        self.execute_show_command.return_value = self._DEFAULTS_HAVE
        config = self._defaults_config()
        config["monitors"][0]["cache"] = {"timeout_inactive": 20, "timeout_active": 90}
        config["exporters"][0]["ttl"] = 64
        set_module_args({"config": config, "state": "replaced"})
        result = self.execute_module(changed=True)
        self.assertIn(" cache timeout inactive 20", result["commands"])
        self.assertIn(" ttl 64", result["commands"])

    def test_ios_flow_monitor_explicit_default_replaces_non_default(self):
        """Setting the default value explicitly changes a non-default value on the device."""
        have = self._DEFAULTS_HAVE.replace(
            " cache timeout active 90",
            " cache timeout inactive 10\n cache timeout active 90",
        )
        self.execute_show_command.return_value = have
        set_module_args({"config": self._defaults_config(), "state": "replaced"})
        result = self.execute_module(changed=True)
        self.assertIn(" cache timeout inactive 15", result["commands"])

    def test_ios_flow_monitor_gathered_bare_option_lines(self):
        """A bare 'option X' line means the default 600 second timeout, not an unset option."""
        self.execute_show_command.return_value = self._DEFAULTS_HAVE
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        options = result["gathered"]["exporters"][0]["options"]
        self.assertEqual(
            options,
            {
                "interface_table_timeout": 600,
                "exporter_stats_timeout": 600,
                "vrf_table_timeout": 600,
                "sampler_table_timeout": 600,
                "application_table_timeout": 600,
            },
        )

    # ── platform differences: Catalyst 9300 / Catalyst 9600 / routers ─────────

    # A flow record as stored by a Catalyst 9600, which accepts the plain counters and sys-uptime.
    _C9600_CONFIG = dedent(
        """\
        flow record REC_IN
         match interface input
         match ipv4 tos
         match ipv4 protocol
         match ipv4 source address
         match ipv4 destination address
         match transport source-port
         match transport destination-port
         match flow direction
         collect routing source as 4-octet
         collect routing destination as 4-octet
         collect routing next-hop address ipv4
         collect transport tcp flags
         collect counter bytes
         collect counter packets
         collect timestamp sys-uptime first
         collect timestamp sys-uptime last
         collect interface output
        flow exporter EXP
         destination 192.0.2.10 vrf MGMT
         source Loopback0
         transport udp 2055
         option sampler-table timeout 10
        flow monitor MON_IN
         exporter EXP
         cache timeout inactive 10
         cache timeout active 60
         record REC_IN
        sampler SMP
         mode random 1 out-of 1000
        """,
    )

    def test_ios_flow_monitor_catalyst_9600_config_round_trip(self):
        """Every line of a Catalyst 9600 flow configuration is parsed and rendered again unchanged."""
        set_module_args({"state": "parsed", "running_config": self._C9600_CONFIG})
        parsed = self.execute_module(changed=False)["parsed"]
        collect = parsed["records"][0]["collect"]
        self.assertTrue(collect["counter_bytes"])
        self.assertTrue(collect["counter_packets"])
        self.assertTrue(collect["timestamp_sys_uptime_first"])

        set_module_args({"state": "rendered", "config": parsed})
        rendered = self.execute_module(changed=False)["rendered"]
        original = [line.strip() for line in self._C9600_CONFIG.splitlines()]
        self.assertEqual(sorted(line.strip() for line in rendered), sorted(original))

    def test_ios_flow_monitor_catalyst_9600_gathered_and_idempotent(self):
        """The plain counters must not make gathered fail or merged report a change."""
        self.execute_show_command.return_value = self._C9600_CONFIG
        set_module_args({"state": "gathered"})
        gathered = self.execute_module(changed=False)["gathered"]
        self.assertTrue(gathered["records"][0]["collect"]["counter_bytes"])

        set_module_args({"config": gathered, "state": "merged"})
        self.assertEqual(self.execute_module(changed=False)["commands"], [])
        set_module_args({"config": gathered, "state": "replaced"})
        self.assertEqual(self.execute_module(changed=False)["commands"], [])

    def test_ios_flow_monitor_plain_counters_and_routing_as_are_rendered(self):
        """counter_bytes, counter_packets and the unqualified routing AS options send the plain commands."""
        self.execute_show_command.return_value = ""
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "REC",
                            "collect": {
                                "counter_bytes": True,
                                "counter_packets": True,
                                "routing_source_as": True,
                                "routing_destination_as": True,
                            },
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        for line in (
            " collect counter bytes",
            " collect counter packets",
            " collect routing source as",
            " collect routing destination as",
        ):
            self.assertIn(line, result["commands"])

    def test_ios_flow_monitor_replaced_removes_plain_counter(self):
        self.execute_show_command.return_value = dedent(
            """\
            flow record REC
             match ipv4 protocol
             collect counter bytes
             collect counter packets
            """,
        )
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "REC",
                            "match": {"ipv4_protocol": True},
                            "collect": {"counter_packets": True},
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["flow record REC", " no collect counter bytes"])

    def test_ios_flow_monitor_catalyst_9300_layer2_long_counter(self):
        """A Catalyst 9300 stores 'collect counter bytes layer2 long', it must not be dropped by the parser."""
        have = dedent(
            """\
            flow record REC
             match ipv4 protocol
             collect counter bytes layer2 long
             collect counter packets long
             collect timestamp absolute first
            """,
        )
        self.execute_show_command.return_value = have
        set_module_args({"state": "gathered"})
        collect = self.execute_module(changed=False)["gathered"]["records"][0]["collect"]
        self.assertTrue(collect["counter_bytes_layer2_long"])
        self.assertNotIn("counter_bytes_layer2", collect)

        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "REC",
                            "match": {"ipv4_protocol": True},
                            "collect": {
                                "counter_bytes_layer2_long": True,
                                "counter_packets_long": True,
                                "timestamp_absolute_first": True,
                            },
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        self.assertEqual(self.execute_module(changed=False)["commands"], [])

    def test_ios_flow_monitor_every_collect_and_match_option_round_trips(self):
        """Guard: each option the module can render is read back from the device as the same option.

        A parser that produces an option missing from the argspec makes every state fail on a device
        that has the line, and a CLI line the parser does not know is silently dropped by gathered.
        """
        from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.flow_monitor.flow_monitor import (
            Flow_monitorArgs,
        )
        from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.flow_monitor.flow_monitor import (
            Flow_monitor,
        )
        from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.flow_monitor import (
            flow_monitor as facts,
        )

        record_spec = Flow_monitorArgs.argument_spec["config"]["options"]["records"]["options"]
        parser_tables = {"match": facts._MATCH_MAP, "collect": facts._COLLECT_MAP}
        failures = []
        for section, table in (
            ("match", Flow_monitor._MATCH_CLI),
            ("collect", Flow_monitor._COLLECT_CLI),
        ):
            argspec_options = set(record_spec[section]["options"])
            if argspec_options != {key for key, _cli in table}:
                failures.append("{0}: argspec and CLI table list different options".format(section))
            if argspec_options != set(parser_tables[section].values()):
                failures.append("{0}: argspec and parser list different options".format(section))
            if {cli for _key, cli in table} != set(parser_tables[section]):
                failures.append(
                    "{0}: CLI table and parser know different command lines".format(section),
                )
            for key, cli in table:
                config = "flow record REC\n {0}\n".format(cli)
                set_module_args({"state": "parsed", "running_config": config})
                parsed = self.execute_module(changed=False)["parsed"]
                got = parsed["records"][0].get(section, {})
                if got != {key: True}:
                    failures.append("{0}: '{1}' parsed as {2}".format(section, cli, got))
                    continue
                set_module_args({"state": "rendered", "config": parsed})
                rendered = [line.strip() for line in self.execute_module(changed=False)["rendered"]]
                if cli not in rendered:
                    failures.append("{0}: '{1}' rendered as {2}".format(section, cli, rendered))
        self.assertEqual(failures, [])
