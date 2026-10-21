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
        self.execute_show_command.return_value = dedent("""\
            """)
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
                                "counter_bytes": True,
                                "counter_packets": True,
                                "timestamp_sys_uptime_first": True,
                                "timestamp_sys_uptime_last": True,
                                "interface_input": True,
                            },
                        }
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                            "options": {"sampler_table_timeout": 10},
                        }
                    ],
                    "samplers": [
                        {
                            "name": "FLOW_SAMPLER",
                            "mode": "random",
                            "window_size": 1000,
                        }
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "exporters": ["FLOW_EXPORTER_1"],
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        }
                    ],
                },
                "state": "merged",
            }
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
        self.assertIn(" collect counter bytes", commands)
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
        self.execute_show_command.return_value = dedent("""\
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
             collect counter bytes
             collect counter packets
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
            """)
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
                                "counter_bytes": True,
                                "counter_packets": True,
                                "timestamp_sys_uptime_first": True,
                                "timestamp_sys_uptime_last": True,
                                "interface_input": True,
                            },
                        }
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                            "options": {"sampler_table_timeout": 10},
                        }
                    ],
                    "samplers": [
                        {
                            "name": "FLOW_SAMPLER",
                            "mode": "random",
                            "window_size": 1000,
                        }
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "exporters": ["FLOW_EXPORTER_1"],
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        }
                    ],
                },
                "state": "merged",
            }
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # ── deleted ──────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_deleted(self):
        """Delete all flow monitor config — deletion order must be monitors→exporters→samplers→records."""
        self.execute_show_command.return_value = dedent("""\
            flow record FLOW_RECORD_IPV4
             match ipv4 source address
             collect counter bytes
            flow exporter FLOW_EXPORTER_1
             destination 192.0.2.1 vrf MGMT
             transport udp 2055
            sampler FLOW_SAMPLER
             mode random 1 out-of 1000
            flow monitor FLOW_MONITOR_OUT
             exporter FLOW_EXPORTER_1
             record FLOW_RECORD_IPV4
            """)
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
        self.execute_show_command.return_value = dedent("""\
            """)
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
                        }
                    ],
                },
                "state": "merged",
            }
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
        self.execute_show_command.return_value = dedent("""\
            """)
        set_module_args(
            {
                "config": {
                    "records": [
                        {
                            "name": "FLOW_RECORD_IPV4",
                            "match": {"ipv4_source_address": True},
                            "collect": {"counter_bytes": True},
                        }
                    ],
                    "monitors": [
                        {
                            "name": "FLOW_MONITOR_OUT",
                            "cache": {"timeout_inactive": 10, "timeout_active": 60},
                            "record": "FLOW_RECORD_IPV4",
                        }
                    ],
                },
                "state": "merged",
            }
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
                running_config=dedent("""\
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
                     collect counter bytes
                     collect counter packets
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
                    """),
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed = result["parsed"]

        self.assertEqual(len(parsed["records"]), 1)
        self.assertEqual(parsed["records"][0]["name"], "FLOW_RECORD_IPV4")
        self.assertTrue(parsed["records"][0]["match"]["ipv4_tos"])
        self.assertTrue(parsed["records"][0]["collect"]["counter_bytes"])

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
                        }
                    ],
                    "exporters": [
                        {
                            "name": "FLOW_EXPORTER_1",
                            "destination": "192.0.2.1",
                            "vrf": "MGMT",
                            "source": "Loopback0",
                            "transport": {"protocol": "udp", "port": 2055},
                        }
                    ],
                },
                state="rendered",
            )
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
                running_config=dedent("""\
                    flow monitor FLOW_MONITOR_IN
                     exporter FLOW_EXPORTER_1
                     exporter FLOW_EXPORTER_2
                     cache timeout inactive 10
                     cache timeout active 60
                     record FLOW_RECORD_IPV4
                    """),
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        mon = result["parsed"]["monitors"][0]
        self.assertEqual(mon["exporters"], ["FLOW_EXPORTER_1", "FLOW_EXPORTER_2"])
