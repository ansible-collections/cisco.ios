#
# (c) 2025, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_flow_monitor_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosFlowMonitorInterfacesModule(TestIosModule):
    module = ios_flow_monitor_interfaces

    def setUp(self):
        super(TestIosFlowMonitorInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.flow_monitor_interfaces.flow_monitor_interfaces."
            "Flow_monitor_interfacesFacts.get_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosFlowMonitorInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    # ── merged ───────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_interfaces_merged(self):
        """Assign IN+OUT flow monitors to an interface with no existing flow config."""
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             ip address 192.0.2.10 255.255.255.0
             negotiation auto
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "GigabitEthernet1",
                        "flow_monitors": [
                            {
                                "monitor": "FLOW_MONITOR_IN",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "input",
                            },
                            {
                                "monitor": "FLOW_MONITOR_OUT",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "output",
                            },
                        ],
                    },
                ],
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertIn("interface GigabitEthernet1", result["commands"])
        self.assertIn(
            "ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input",
            result["commands"],
        )
        self.assertIn(
            "ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output",
            result["commands"],
        )

    def test_ios_flow_monitor_interfaces_merged_idempotent(self):
        """Merging identical config must produce no commands."""
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             ip address 192.0.2.10 255.255.255.0
             ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
             ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "GigabitEthernet1",
                        "flow_monitors": [
                            {
                                "monitor": "FLOW_MONITOR_IN",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "input",
                            },
                            {
                                "monitor": "FLOW_MONITOR_OUT",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "output",
                            },
                        ],
                    },
                ],
                "state": "merged",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # ── deleted ──────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_interfaces_deleted(self):
        """Deleting a named interface removes its flow monitor assignments."""
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             ip address 192.0.2.10 255.255.255.0
             ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
             ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
            interface GigabitEthernet2
             ip address 192.0.2.20 255.255.255.0
             ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
            """
        )
        set_module_args(
            {
                "config": [{"name": "GigabitEthernet1"}],
                "state": "deleted",
            },
        )
        result = self.execute_module(changed=True)
        self.assertIn("interface GigabitEthernet1", result["commands"])
        self.assertIn(
            "no ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input",
            result["commands"],
        )
        self.assertIn(
            "no ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output",
            result["commands"],
        )
        # GigabitEthernet2 should NOT be touched
        self.assertNotIn("interface GigabitEthernet2", result["commands"])

    def test_ios_flow_monitor_interfaces_deleted_all(self):
        """Deleting with no config removes flow monitors from all interfaces."""
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
            interface GigabitEthernet2
             ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
            """
        )
        set_module_args({"state": "deleted"})
        result = self.execute_module(changed=True)
        self.assertIn("interface GigabitEthernet1", result["commands"])
        self.assertIn("interface GigabitEthernet2", result["commands"])

    # ── replaced ─────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_interfaces_replaced(self):
        """Replaced removes old monitor and adds the new one on an interface."""
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             ip address 192.0.2.10 255.255.255.0
             ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input
             ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "GigabitEthernet1",
                        "flow_monitors": [
                            {
                                "monitor": "FLOW_MONITOR_IN",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "input",
                            },
                            {
                                "monitor": "FLOW_MONITOR_OUT",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "output",
                            },
                        ],
                    },
                ],
                "state": "replaced",
            },
        )
        result = self.execute_module(changed=True)
        self.assertIn("interface GigabitEthernet1", result["commands"])
        self.assertIn(
            "no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input",
            result["commands"],
        )
        self.assertIn(
            "no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output",
            result["commands"],
        )
        self.assertIn(
            "ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input",
            result["commands"],
        )
        self.assertIn(
            "ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output",
            result["commands"],
        )

    # ── parsed ───────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_interfaces_parsed(self):
        """Feed raw interface config, assert structured output."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet1
                     ip address 192.0.2.10 255.255.255.0
                     ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
                     ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
                    interface GigabitEthernet2
                     ip address 192.0.2.20 255.255.255.0
                    """
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed = result["parsed"]

        # Only GigabitEthernet1 should appear (it has flow monitors)
        names = [e["name"] for e in parsed]
        self.assertIn("GigabitEthernet1", names)
        self.assertNotIn("GigabitEthernet2", names)

        gi1 = next(e for e in parsed if e["name"] == "GigabitEthernet1")
        self.assertEqual(len(gi1["flow_monitors"]), 2)
        directions = {m["direction"] for m in gi1["flow_monitors"]}
        self.assertIn("input", directions)
        self.assertIn("output", directions)

    # ── rendered ─────────────────────────────────────────────────────────────

    def test_ios_flow_monitor_interfaces_rendered(self):
        """Render commands without device connection."""
        set_module_args(
            dict(
                config=[
                    {
                        "name": "GigabitEthernet1",
                        "flow_monitors": [
                            {
                                "monitor": "FLOW_MONITOR_IN",
                                "sampler": "FLOW_SAMPLER",
                                "direction": "input",
                            },
                        ],
                    },
                ],
                state="rendered",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertIn("interface GigabitEthernet1", result["rendered"])
        self.assertIn(
            "ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input",
            result["rendered"],
        )
