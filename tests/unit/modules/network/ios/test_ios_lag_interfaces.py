#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_lag_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLagInterfacesModule(TestIosModule):
    module = ios_lag_interfaces

    def setUp(self):
        super(TestIosLagInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lag_interfaces.lag_interfaces."
            "Lag_interfacesFacts.get_lag_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLagInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_lag_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/1", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "passive"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="merged",
            ),
        )
        commands = ["interface GigabitEthernet0/3", "channel-group 22 mode passive"]
        result = self.execute_module(changed=True)
        # print(result["commands"])
        self.assertEqual(result["commands"], commands)

    def test_ios_lag_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/1", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "active"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_lag_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/3", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/1", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "on"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/1",
            "channel-group 22 mode active",
            "interface GigabitEthernet0/3",
            "channel-group 22 mode on",
            "interface GigabitEthernet0/2",
            "no channel-group 22 mode active",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lag_interfaces_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/1", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "active"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_lag_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "active"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="overridden",
            ),
        )

        commands = [
            "interface GigabitEthernet0/1",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/3",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/3",
            "channel-group 22 mode active",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(result["commands"], commands)

    def test_ios_lag_interfaces_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/1", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "active"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_lag_interfaces_deleted_interface(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface GigabitEthernet0/1",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/3",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/2",
            "no channel-group 22 mode active",
            "interface GigabitEthernet0/4",
            "no channel-group 22 mode active link 20",
            "interface GigabitEthernet0/5",
            "no channel-group 22 link 22",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(result["commands"], commands)

    def test_ios_lag_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel11
            interface Port-channel22
            interface GigabitEthernet0/1
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/2
             shutdown
             channel-group 22 mode active
            interface GigabitEthernet0/3
             shutdown
             channel-group 11 mode active
            interface GigabitEthernet0/4
             shutdown
             channel-group 22 mode active link 20
            interface GigabitEthernet0/5
             shutdown
             channel-group 22 link 22
            """,
        )
        set_module_args(dict(config=[dict(name="Port-channel11")], state="deleted"))
        commands = [
            "interface GigabitEthernet0/1",
            "no channel-group 11 mode active",
            "interface GigabitEthernet0/3",
            "no channel-group 11 mode active",
        ]
        res = self.execute_module(changed=True)
        self.assertEqual(res["commands"], commands)

    def test_ios_lag_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface Port-channel11
                    interface Port-channel22
                    interface GigabitEthernet0/1
                     shutdown
                     channel-group 11 mode active
                    interface GigabitEthernet0/2
                     shutdown
                     channel-group 22 mode active
                    interface GigabitEthernet0/3
                     shutdown
                     channel-group 11 mode active
                    interface GigabitEthernet0/4
                     shutdown
                     channel-group 22 mode active link 20
                    interface GigabitEthernet0/5
                     shutdown
                     channel-group 22 link 22
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "Port-channel11",
                "members": [
                    {"member": "GigabitEthernet0/1", "mode": "active"},
                    {"member": "GigabitEthernet0/3", "mode": "active"},
                ],
            },
            {
                "name": "Port-channel22",
                "members": [
                    {"member": "GigabitEthernet0/2", "mode": "active"},
                    {"member": "GigabitEthernet0/4", "link": 20, "mode": "active"},
                    {"member": "GigabitEthernet0/5", "link": 22},
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_lag_interfaces_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "members": [{"member": "GigabitEthernet0/1", "mode": "active"}],
                        "name": "Port-channel11",
                    },
                    {
                        "members": [
                            {"member": "GigabitEthernet0/2", "mode": "active"},
                            {"member": "GigabitEthernet0/3", "mode": "active"},
                            {
                                "link": 20,
                                "member": "GigabitEthernet0/4",
                                "mode": "active",
                            },
                            {"link": 22, "member": "GigabitEthernet0/5"},
                        ],
                        "name": "Port-channel22",
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "channel-group 11 mode active",
            "interface GigabitEthernet0/2",
            "channel-group 22 mode active",
            "interface GigabitEthernet0/3",
            "channel-group 22 mode active",
            "interface GigabitEthernet0/4",
            "channel-group 22 mode active link 20",
            "interface GigabitEthernet0/5",
            "channel-group 22 link 22",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
