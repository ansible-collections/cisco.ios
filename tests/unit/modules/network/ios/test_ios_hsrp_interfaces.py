#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_hsrp_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule



class TestIosHSRPInterfaceModule(TestIosModule):
    module = ios_hsrp_interfaces

    def setUp(self):
        super(TestIosHSRPInterfaceModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.hsrp_interfaces.hsrp_interfaces."
            "Hsrp_interfacesFacts.get_hsrp_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosHSRPInterfaceModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_hsrp_interfaces_merged_common_ip(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_hsrp_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_hsrp_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(dict(state="deleted"))
        commands = [
            "interface GigabitEthernet4",
            "no standby 22 ip 10.0.0.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet3",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="12.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                track=[dict(track_no=20, shutdown=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "no standby 22 ip 10.0.0.1 secondary",
            "standby 22 track 20 shutdown",
            "interface GigabitEthernet3",
            "standby 22 ip 12.0.0.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet4
                     standby 22 ip 10.0.0.1 secondary
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "GigabitEthernet4",
                "standby_groups": [
                    {
                        "group_no": 22,
                        "ip": [
                            {
                                "virtual_ip": "10.0.0.1",
                                "secondary": True,
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_hsrp_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet3",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="12.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                track=[dict(track_no=20, shutdown=True)],
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "standby 22 ip 10.0.0.1 secondary",
            "standby 22 track 20 shutdown",
            "interface GigabitEthernet3",
            "standby 22 ip 12.0.0.1 secondary",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_hsrp_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            interface GigabitEthernet3
             standby 0 priority 5
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet3",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="12.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                track=[dict(track_no=20, shutdown=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "standby 22 track 20 shutdown",
            "interface GigabitEthernet3",
            "standby 22 ip 12.0.0.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
            interface GigabitEthernet3
             standby 0 priority 5
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet3",
                        standby_groups=[
                            dict(
                                priority=5,
                                group_no=0,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_primary_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1
             standby 10 ip 10.0.0.3 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "no standby 10 ip 10.0.0.3 secondary",
            "standby 22 ip 10.0.0.1 secondary",
            "no standby 22 ip 10.0.0.1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 7 ip 10.0.0.3 secondary
            interface GigabitEthernet3
             standby 10 ip 10.0.0.2 secondary
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
        )
        result = self.execute_module(changed=False)
        gathered = [
            {
                "name": "GigabitEthernet4",
                "standby_groups": [
                    {
                        "ip": [{"virtual_ip": "10.0.0.3", "secondary": True}],
                        "group_no": 7,
                    },
                ],
            },
            {
                "name": "GigabitEthernet3",
                "standby_groups": [
                    {
                        "ip": [{"virtual_ip": "10.0.0.2", "secondary": True}],
                        "group_no": 10,
                    },
                ],
            },
        ]
        self.assertEqual(result["gathered"], gathered)
