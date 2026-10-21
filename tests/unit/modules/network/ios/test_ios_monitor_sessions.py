#
# (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_monitor_sessions
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosMonitorSessionsModule(TestIosModule):
    module = ios_monitor_sessions

    def setUp(self):
        super(TestIosMonitorSessionsModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.monitor_sessions.monitor_sessions."
            "Monitor_sessionsFacts.get_monitor_sessions_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosMonitorSessionsModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_monitor_sessions_merged(self):
        """Merge new session onto empty device."""
        self.execute_show_command.return_value = ""
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Gi1/0/1"]},
                            {"interfaces": ["Gi1/0/2"], "direction": "rx"},
                        ],
                        "destination": {
                            "interface": "Gi1/0/48",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "monitor session 1 source interface Gi1/0/1",
            "monitor session 1 source interface Gi1/0/2 rx",
            "monitor session 1 destination interface Gi1/0/48 encapsulation replicate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_monitor_sessions_merged_idempotent(self):
        """Merged with no changes required."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 source interface Gi1/0/2 rx
            monitor session 1 destination interface Gi1/0/48 encapsulation replicate
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Gi1/0/1"]},
                            {"interfaces": ["Gi1/0/2"], "direction": "rx"},
                        ],
                        "destination": {
                            "interface": "Gi1/0/48",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_monitor_sessions_merged_multiple_sources(self):
        """Merge with multiple source entries - all same direction are combined in one command."""
        self.execute_show_command.return_value = ""
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Twe1/0/2", "Twe1/0/12", "Twe1/0/45"]},
                            {"interfaces": ["Po2"]},
                        ],
                        "destination": {
                            "interface": "Po3",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        cmds = result["commands"]
        # All same-direction sources are combined into one command
        self.assertIn("monitor session 1 destination interface Po3 encapsulation replicate", cmds)
        self.assertTrue(
            any(
                "Twe1/0/2" in c and "Twe1/0/12" in c and "Twe1/0/45" in c and "Po2" in c
                for c in cmds
            ),
        )

    def test_ios_monitor_sessions_merged_multiple_sources_idempotent(self):
        """Same interfaces in different order are idempotent."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
            monitor session 1 source interface Po2
            monitor session 1 destination interface Po3 encapsulation replicate
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Twe1/0/45", "Twe1/0/2", "Twe1/0/12"]},
                            {"interfaces": ["Po2"]},
                        ],
                        "destination": {
                            "interface": "Po3",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_monitor_sessions_replaced(self):
        """Replace source list of a session."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 source interface Gi1/0/2
            monitor session 1 destination interface Gi1/0/48 encapsulation replicate
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Gi1/0/2"]},
                            {"interfaces": ["Gi1/0/3"]},
                        ],
                        "destination": {
                            "interface": "Gi1/0/48",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no monitor session 1 source interface Gi1/0/1", result["commands"])
        self.assertIn("monitor session 1 source interface Gi1/0/3", result["commands"])
        self.assertNotIn("no monitor session 1 source interface Gi1/0/2", result["commands"])

    def test_ios_monitor_sessions_replaced_idempotent(self):
        """Replace with no changes required."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {"interface": "Gi1/0/48"},
                    },
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_monitor_sessions_overridden(self):
        """Overridden removes sessions not in want."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            monitor session 2 source interface Gi1/0/2
            monitor session 2 destination interface Gi1/0/47
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {"interface": "Gi1/0/48"},
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no monitor session 2", result["commands"])

    def test_ios_monitor_sessions_overridden_idempotent(self):
        """Overridden with no changes required."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {"interface": "Gi1/0/48"},
                    },
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_monitor_sessions_deleted_specific(self):
        """Delete a specific session."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            monitor session 2 source interface Gi1/0/2
            monitor session 2 destination interface Gi1/0/47
            """,
        )
        set_module_args(dict(config=[{"session": 1}], state="deleted"))
        commands = ["no monitor session 1"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_monitor_sessions_deleted_all(self):
        """Delete all sessions when no config specified."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            monitor session 2 source interface Gi1/0/2
            monitor session 2 destination interface Gi1/0/47
            """,
        )
        set_module_args(dict(state="deleted"))
        result = self.execute_module(changed=True)
        self.assertIn("no monitor session 1", result["commands"])
        self.assertIn("no monitor session 2", result["commands"])

    def test_ios_monitor_sessions_deleted_no_config(self):
        """Delete on empty device is idempotent."""
        self.execute_show_command.return_value = ""
        set_module_args(dict(state="deleted"))
        self.execute_module(changed=False, commands=[])

    def test_ios_monitor_sessions_rendered(self):
        """Rendered generates commands without device connection."""
        self.execute_show_command.return_value = ""
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [
                            {"interfaces": ["Po2"]},
                        ],
                        "destination": {
                            "interface": "Po3",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "monitor session 1 source interface Po2",
            "monitor session 1 destination interface Po3 encapsulation replicate",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_monitor_sessions_parsed(self):
        """Parsed returns structured data from running config string."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
                    monitor session 1 source interface Po2
                    monitor session 1 destination interface Po3 encapsulation replicate
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["session"], 1)
        self.assertEqual(len(parsed[0]["sources"]), 2)
        self.assertEqual(parsed[0]["destination"]["interface"], "Po3")
        self.assertTrue(parsed[0]["destination"]["encapsulation_replicate"])

    def test_ios_monitor_sessions_gathered(self):
        """Gathered returns structured data from device."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1 - 2 rx
            monitor session 1 source interface Gi1/0/5
            monitor session 1 destination interface Gi1/0/48 encapsulation replicate
            """,
        )
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        gathered = result["gathered"]
        self.assertEqual(len(gathered), 1)
        session = gathered[0]
        self.assertEqual(session["session"], 1)
        source_with_dir = next(s for s in session["sources"] if s.get("direction") == "rx")
        self.assertIn("Gi1/0/1", source_with_dir["interfaces"])
        self.assertIn("Gi1/0/2", source_with_dir["interfaces"])

    def test_ios_monitor_sessions_merged_destination_update(self):
        """Merged updates destination when it changes."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {
                            "interface": "Gi1/0/48",
                            "encapsulation_replicate": True,
                        },
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn(
            "monitor session 1 destination interface Gi1/0/48 encapsulation replicate",
            result["commands"],
        )

    def test_ios_monitor_sessions_overridden_extra_sources(self):
        """Overridden strips extra sources from sessions that stay in want."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 source interface Gi1/0/2
            monitor session 1 destination interface Gi1/0/48
            monitor session 2 source interface Gi1/0/3
            monitor session 2 destination interface Gi1/0/47
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {"interface": "Gi1/0/48"},
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no monitor session 1 source interface Gi1/0/2", result["commands"])
        self.assertIn("no monitor session 2", result["commands"])
        self.assertNotIn("no monitor session 1 source interface Gi1/0/1", result["commands"])

    def test_ios_monitor_sessions_merged_sources_only_preserves_dest(self):
        """Merged with sources only (no destination) does not negate existing destination."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/2"]}],
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("monitor session 1 source interface Gi1/0/2", result["commands"])
        self.assertNotIn("no monitor session 1 destination interface Gi1/0/48", result["commands"])

    def test_ios_monitor_sessions_merged_dest_interface_change(self):
        """Merged negates old destination and adds new one when interface changes."""
        self.execute_show_command.return_value = dedent(
            """\
            monitor session 1 source interface Gi1/0/1
            monitor session 1 destination interface Gi1/0/48
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "session": 1,
                        "sources": [{"interfaces": ["Gi1/0/1"]}],
                        "destination": {"interface": "Gi1/0/47"},
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no monitor session 1 destination interface Gi1/0/48", result["commands"])
        self.assertIn("monitor session 1 destination interface Gi1/0/47", result["commands"])
