#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_lacp_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLacpInterfaceModule(TestIosModule):
    module = ios_lacp_interfaces

    def setUp(self):
        super(TestIosLacpInterfaceModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()
        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lacp_interfaces.lacp_interfaces."
            "Lacp_InterfacesFacts.get_lacp_interface_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLacpInterfaceModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    # lacp_interface
    def test_ios_lacp_interface_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             lacp fast-switchover
             lacp max-bundle 2
            interface Port-channel40
             lacp max-bundle 5
            interface GigabitEthernet0/0
            interface GigabitEthernet0/1
             lacp port-priority 30
            interface GigabitEthernet0/2
             lacp port-priority 20
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Port-channel10",
                        "fast_switchover": True,
                        "max_bundle": 12,
                    },
                    {"name": "Port-channel40", "max_bundle": 5},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 20},
                    {"name": "GigabitEthernet0/2", "port_priority": 30},
                ],
                state="merged",
            ),
        )
        commands = [
            "interface Port-channel10",
            "lacp max-bundle 12",
            "interface GigabitEthernet0/1",
            "lacp port-priority 20",
            "interface GigabitEthernet0/2",
            "lacp port-priority 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_interface_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             lacp fast-switchover
             lacp max-bundle 2
            interface Port-channel40
             lacp max-bundle 5
            interface GigabitEthernet0/0
            interface GigabitEthernet0/1
             lacp port-priority 30
            interface GigabitEthernet0/2
             lacp port-priority 20
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Port-channel10",
                        "fast_switchover": True,
                        "max_bundle": 2,
                    },
                    {"name": "Port-channel40", "max_bundle": 5},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 30},
                    {"name": "GigabitEthernet0/2", "port_priority": 20},
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_ios_lacp_interface_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             lacp fast-switchover
             lacp max-bundle 2
            interface Port-channel40
             lacp max-bundle 5
            interface GigabitEthernet0/0
            interface GigabitEthernet0/1
             lacp port-priority 30
            interface GigabitEthernet0/2
             lacp port-priority 20
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Port-channel10",
                        "fast_switchover": True,
                        "max_bundle": 12,
                    },
                    {"name": "Port-channel40", "max_bundle": 5},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 20},
                    {"name": "GigabitEthernet0/2", "port_priority": 30},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface Port-channel10",
            "lacp max-bundle 12",
            "interface GigabitEthernet0/1",
            "lacp port-priority 20",
            "interface GigabitEthernet0/2",
            "lacp port-priority 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_interface_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             lacp fast-switchover
             lacp max-bundle 2
            interface Port-channel40
             lacp max-bundle 5
            interface GigabitEthernet0/0
            interface GigabitEthernet0/1
             lacp port-priority 30
            interface GigabitEthernet0/2
             lacp port-priority 20
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Port-channel10",
                        "fast_switchover": True,
                        "max_bundle": 12,
                    },
                    {"name": "Port-channel40", "max_bundle": 5},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 20},
                    {"name": "GigabitEthernet0/2", "port_priority": 30},
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface Port-channel10",
            "lacp max-bundle 12",
            "interface GigabitEthernet0/1",
            "lacp port-priority 20",
            "interface GigabitEthernet0/2",
            "lacp port-priority 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_interface_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             lacp fast-switchover
             lacp max-bundle 2
            interface Port-channel40
             lacp max-bundle 5
            interface GigabitEthernet0/0
            interface GigabitEthernet0/1
             lacp port-priority 30
            interface GigabitEthernet0/2
             lacp port-priority 20
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Port-channel10",
                        "fast_switchover": True,
                        "max_bundle": 12,
                    },
                    {"name": "Port-channel40", "max_bundle": 5},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 20},
                    {"name": "GigabitEthernet0/2", "port_priority": 30},
                ],
                state="deleted",
            ),
        )
        commands = [
            "interface Port-channel10",
            "no lacp max-bundle",
            "no lacp fast-switchover",
            "interface Port-channel40",
            "no lacp max-bundle",
            "interface GigabitEthernet0/1",
            "no lacp port-priority",
            "interface GigabitEthernet0/2",
            "no lacp port-priority",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_interface_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface Port-channel10
                     lacp fast-switchover
                     lacp max-bundle 2
                    interface Port-channel40
                     lacp max-bundle 5
                    interface GigabitEthernet0/0
                    interface GigabitEthernet0/1
                     lacp port-priority 30
                    interface GigabitEthernet0/2
                     lacp port-priority 20
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {"name": "Port-channel10", "fast_switchover": True, "max_bundle": 2},
            {"name": "Port-channel40", "max_bundle": 5},
            {"name": "GigabitEthernet0/0"},
            {"name": "GigabitEthernet0/1", "port_priority": 30},
            {"name": "GigabitEthernet0/2", "port_priority": 20},
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_lacp_interface_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "fast_switchover": True,
                        "max_bundle": 2,
                        "name": "Port-channel10",
                    },
                    {"max_bundle": 5, "name": "Port-channel40"},
                    {"name": "GigabitEthernet0/0"},
                    {"name": "GigabitEthernet0/1", "port_priority": 30},
                    {"name": "GigabitEthernet0/2", "port_priority": 20},
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface Port-channel10",
            "lacp max-bundle 2",
            "lacp fast-switchover",
            "interface Port-channel40",
            "lacp max-bundle 5",
            "interface GigabitEthernet0/1",
            "lacp port-priority 30",
            "interface GigabitEthernet0/2",
            "lacp port-priority 20",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
