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

    def test_ios_hsrp_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby mac-refresh 21
             standby version 7
             standby delay minimum 30 reload 40
             standby use-bia scope interface
             standby follow test
             standby redirect advertisement authentication md5 key-string apple timeout 10
             standby 22 follow test123
             standby 22 priority 7
             standby 22 preempt delay minimum 60 reload 70 sync 90
             standby 22 track 4 decrement 45 shutdown
             standby 22 mac-address A:B:C:D
             standby 22 name sentry
             standby 22 timers 20 30
             standby 22 authentication md5 key-string 0 apple timeout 10
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        mac_refresh=21,
                        version=7,
                        delay=dict(
                            minimum=30,
                            reload=40,
                        ),
                        use_bia=dict(
                            scope=dict(
                                interface=True,
                            ),
                        ),
                        follow="test",
                        redirect=dict(
                            advertisement=dict(
                                authentication=dict(
                                    key_string=True,
                                    password_text="apple",
                                    time_out=10,
                                ),
                            ),
                        ),
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                                follow="test123",
                                priority=7,
                                preempt=dict(
                                    delay=True,
                                    minimum=60,
                                    reload=70,
                                    sync=90,
                                ),
                                track=[dict(track_no=4, decrement=45, shutdown=True)],
                                mac_address="A:B:C:D",
                                group_name="sentry",
                                authentication=dict(
                                    advertisement=dict(
                                        key_string=True,
                                        password_text="apple",
                                        encryption=0,
                                        time_out=10,
                                    ),
                                ),
                                timers=dict(hello_interval=20, hold_time=30),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], commands)

    def test_ios_hsrp_interfaces_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby mac-refresh 21
             standby version 7
             standby delay minimum 30 reload 40
             standby use-bia scope interface
             standby follow test
             standby redirect advertisement authentication md5 key-string apple timeout 10
             standby 22 follow test123
             standby 22 priority 7
             standby 22 preempt delay minimum 60 reload 70 sync 90
             standby 22 track 4 decrement 45 shutdown
             standby 22 mac-address A:B:C:D
             standby 22 name sentry
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet4",
                        mac_refresh=21,
                        version=7,
                        delay=dict(
                            minimum=30,
                            reload=40,
                        ),
                        use_bia=dict(
                            scope=dict(
                                interface=True,
                            ),
                        ),
                        follow="test",
                        redirect=dict(
                            advertisement=dict(
                                authentication=dict(
                                    key_string=True,
                                    password_text="apple",
                                    time_out=10,
                                ),
                            ),
                        ),
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                                follow="test123",
                                priority=7,
                                preempt=dict(
                                    enabled=True,
                                    delay=True,
                                    minimum=60,
                                    reload=70,
                                    sync=90,
                                ),
                                track=[dict(track_no=4, decrement=45, shutdown=True)],
                                mac_address="A:B:C:D",
                                group_name="sentry",
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
             standby mac-refresh 21
             standby version 7
             standby delay minimum 30 reload 40
             standby follow test
             standby redirect advertisement authentication md5 key-string apple timeout 10
             standby 22 priority 7
             standby 22 preempt delay minimum 60 reload 70 sync 90
             standby 22 follow test123
             standby 22 track 4 decrement 45 shutdown
             standby 22 mac-address A:B:C:D
             standby 22 name sentry
             standby 22 timers 20 30
             standby 22 authentication md5 key-string 0 apple timeout 10
             standby 22 ip 10.0.0.1 secondary
            """,
        )
        set_module_args(dict(state="deleted"))
        commands = [
            "interface GigabitEthernet4",
            "no standby mac-refresh 21",
            "no standby version 7",
            "no standby delay minimum 30 reload 40",
            "no standby follow test",
            "no standby redirect advertisement authentication md5 key-string apple timeout 10",
            "no standby 22 priority 7",
            "no standby 22 preempt",
            "no standby 22 follow test123",
            "no standby 22 track 4 decrement 45 shutdown",
            "no standby 22 mac-address A:B:C:D",
            "no standby 22 name sentry",
            "no standby 22 timers 20 30",
            "no standby 22 authentication md5 key-string 0 apple timeout 10",
            "no standby 22 ip 10.0.0.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby 22 ip 10.0.0.1 secondary
             standby 22 timers 20 30
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
                                timers=dict(hello_interval=40, hold_time=50),
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
            "standby 22 timers 40 50",
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
                     standby mac-refresh 21
                     standby version 7
                     standby delay minimum 30 reload 40
                     standby follow test
                     standby redirect advertisement authentication md5 key-string apple timeout 10
                     standby 22 follow test123
                     standby 22 priority 7
                     standby 22 preempt delay minimum 60 reload 70 sync 90
                     standby 22 track 4 decrement 45 shutdown
                     standby 22 mac-address A:B:C:D
                     standby 22 name sentry
                     standby 22 timers 20 30
                     standby 22 authentication md5 key-string 0 apple timeout 10
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
                "mac_refresh": 21,
                "version": 7,
                "delay": {
                    "minimum": 30,
                    "reload": 40,
                },
                "follow": "test",
                "redirect": {
                    "advertisement": {
                        "authentication": {
                            "key_string": True,
                            "password_text": "apple",
                            "time_out": 10,
                        },
                    },
                },
                "standby_groups": [
                    {
                        "group_no": 22,
                        "follow": "test123",
                        "priority": 7,
                        "preempt": {
                            "enabled": True,
                            "delay": True,
                            "minimum": 60,
                            "reload": 70,
                            "sync": 90,
                        },
                        "track": [
                            {
                                "track_no": 4,
                                "decrement": 45,
                                "shutdown": True,
                            },
                        ],
                        "mac_address": "A:B:C:D",
                        "group_name": "sentry",
                        "timers": {
                            "hello_interval": 20,
                            "hold_time": 30,
                        },
                        "authentication": {
                            "advertisement": {
                                "key_string": True,
                                "encryption": 0,
                                "password_text": "apple",
                                "time_out": 10,
                            },
                        },
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
                        mac_refresh=21,
                        version=7,
                        delay=dict(
                            minimum=30,
                            reload=40,
                        ),
                        follow="test",
                        redirect=dict(
                            advertisement=dict(
                                authentication=dict(
                                    key_string=True,
                                    password_text="apple",
                                    time_out=10,
                                ),
                            ),
                        ),
                        standby_groups=[
                            dict(
                                ip=[dict(virtual_ip="10.0.0.1", secondary=True)],
                                group_no=22,
                                follow="test123",
                                priority=7,
                                preempt=dict(
                                    delay=True,
                                    minimum=60,
                                    reload=70,
                                    sync=90,
                                ),
                                track=[dict(track_no=4, decrement=45, shutdown=True)],
                                mac_address="A:B:C:D",
                                group_name="sentry",
                                authentication=dict(
                                    advertisement=dict(
                                        key_string=True,
                                        password_text="apple",
                                        encryption=0,
                                        time_out=10,
                                    ),
                                ),
                                timers=dict(hello_interval=20, hold_time=30),
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet3",
            "standby mac-refresh 21",
            "standby version 7",
            "standby delay minimum 30 reload 40",
            "standby follow test",
            "standby redirect advertisement authentication md5 key-string apple timeout 10",
            "standby 22 follow test123",
            "standby 22 priority 7",
            "standby 22 preempt delay minimum 60 reload 70 sync 90",
            "standby 22 track 4 decrement 45 shutdown",
            "standby 22 mac-address A:B:C:D",
            "standby 22 name sentry",
            "standby 22 timers 20 30",
            "standby 22 authentication md5 key-string 0 apple timeout 10",
            "standby 22 ip 10.0.0.1 secondary",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_hsrp_interfaces_merged_common_ip(self):
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
             standby mac-refresh 21
             standby version 7
             standby delay minimum 30 reload 40
             standby follow test
             standby redirect advertisement authentication md5 key-string apple timeout 10
             standby 22 follow test123
             standby 22 priority 7
             standby 22 preempt delay minimum 60 reload 70 sync 90
             standby 22 track 4 decrement 45 shutdown
             standby 22 mac-address A:B:C:D
             standby 22 name sentry
             standby 22 timers 20 30
             standby 22 authentication md5 key-string 0 apple timeout 10
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
                                ip=[dict(virtual_ip="10.0.0.3", secondary=True)],
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
            "no standby mac-refresh 21",
            "no standby version 7",
            "no standby delay minimum 30 reload 40",
            "no standby follow test",
            "no standby redirect advertisement authentication md5 key-string apple timeout 10",
            "standby 22 ip 10.0.0.3 secondary",
            "no standby 22 track 4 decrement 45 shutdown",
            "no standby 22 ip 10.0.0.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet4
             standby mac-refresh 21
             standby version 7
             standby delay minimum 30 reload 40
             standby follow test
             standby redirect advertisement authentication md5 key-string apple timeout 10
             standby 22 follow test123
             standby 22 priority 7
             standby 22 preempt delay minimum 60 reload 70 sync 90
             standby 22 track 4 decrement 45 shutdown
             standby 22 mac-address A:B:C:D
             standby 22 name sentry
             standby 22 timers 20 30
             standby 22 authentication md5 key-string 0 apple timeout 10
             standby 22 ip 10.0.0.1 secondary
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
                "mac_refresh": 21,
                "version": 7,
                "delay": {
                    "minimum": 30,
                    "reload": 40,
                },
                "follow": "test",
                "redirect": {
                    "advertisement": {
                        "authentication": {
                            "key_string": True,
                            "password_text": "apple",
                            "time_out": 10,
                        },
                    },
                },
                "standby_groups": [
                    {
                        "group_no": 22,
                        "follow": "test123",
                        "priority": 7,
                        "preempt": {
                            "enabled": True,
                            "delay": True,
                            "minimum": 60,
                            "reload": 70,
                            "sync": 90,
                        },
                        "track": [
                            {
                                "track_no": 4,
                                "decrement": 45,
                                "shutdown": True,
                            },
                        ],
                        "mac_address": "A:B:C:D",
                        "group_name": "sentry",
                        "timers": {
                            "hello_interval": 20,
                            "hold_time": 30,
                        },
                        "authentication": {
                            "advertisement": {
                                "key_string": True,
                                "encryption": 0,
                                "password_text": "apple",
                                "time_out": 10,
                            },
                        },
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
        self.assertEqual(result["gathered"], gathered)
