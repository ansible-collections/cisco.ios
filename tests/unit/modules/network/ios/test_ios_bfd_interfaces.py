#
# (c) 2025, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_bfd_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosBfdInterfacesModule(TestIosModule):
    module = ios_bfd_interfaces

    def setUp(self):
        super(TestIosBfdInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bfd_interfaces.bfd_interfaces."
            "Bfd_interfacesFacts.get_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBfdInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_bfd_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             description Ansible UT interface 1
             no shutdown
             bfd local-address 10.0.0.1
             bfd interval 57 min_rx 66 multiplier 45
            interface GigabitEthernet2
             description Ansible UT interface 2
             ip address dhcp
             bfd template OLD_TEMPLATE
            interface GigabitEthernet3
             description Ansible UT interface 3
             no ip address
             shutdown
             bfd jitter
             bfd local-address 10.0.1.2
             bfd interval 50 min_rx 50 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "local_address": "10.0.1.2",
                        "name": "GigabitEthernet1",
                        "template": "ANSIBLE",
                    },
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "name": "GigabitEthernet2",
                    },
                    {"template": "ANSIBLE_3Tempalte", "name": "GigabitEthernet6"},
                ],
                "state": "merged",
            },
        )
        commands = [
            "interface GigabitEthernet1",
            "bfd enable",
            "bfd echo",
            "bfd jitter",
            "bfd local-address 10.0.1.2",
            "bfd interval 100 min_rx 100 multiplier 3",
            "bfd template ANSIBLE",
            "interface GigabitEthernet2",
            "bfd enable",
            "bfd echo",
            "bfd jitter",
            "bfd interval 100 min_rx 100 multiplier 3",
            "interface GigabitEthernet6",
            "bfd template ANSIBLE_3Tempalte",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             description Ansible UT interface 1
             no shutdown
             bfd local-address 10.0.0.1
             bfd interval 57 min_rx 66 multiplier 45
            interface GigabitEthernet2
             description Ansible UT interface 2
             ip address dhcp
             bfd template OLD_TEMPLATE
            interface GigabitEthernet3
             description Ansible UT interface 3
             no ip address
             shutdown
             bfd jitter
             bfd local-address 10.0.1.2
             bfd interval 50 min_rx 50 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "local_address": "10.0.1.2",
                        "name": "GigabitEthernet1",
                        "template": "ANSIBLE",
                    },
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "name": "GigabitEthernet2",
                    },
                    {"template": "ANSIBLE_3Tempalte", "name": "GigabitEthernet6"},
                ],
                "state": "replaced",
            },
        )
        commands = [
            "interface GigabitEthernet1",
            "bfd enable",
            "bfd echo",
            "bfd jitter",
            "bfd local-address 10.0.1.2",
            "bfd interval 100 min_rx 100 multiplier 3",
            "bfd template ANSIBLE",
            "interface GigabitEthernet2",
            "bfd enable",
            "bfd echo",
            "bfd jitter",
            "bfd interval 100 min_rx 100 multiplier 3",
            "no bfd template OLD_TEMPLATE",
            "interface GigabitEthernet6",
            "bfd template ANSIBLE_3Tempalte",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             description Ansible UT interface 1
             no shutdown
             no bfd enable
             no bfd echo
             bfd local-address 10.0.0.1
             bfd interval 57 min_rx 66 multiplier 45
            interface GigabitEthernet2
             description Ansible UT interface 2
             ip address dhcp
             bfd template OLD_TEMPLATE
            interface GigabitEthernet3
             description Ansible UT interface 3
             no ip address
             shutdown
             bfd local-address 10.0.1.2
             bfd interval 50 min_rx 50 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "local_address": "10.0.1.2",
                        "name": "GigabitEthernet1",
                        "template": "ANSIBLE",
                    },
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": False,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "name": "GigabitEthernet2",
                    },
                    {"template": "ANSIBLE_3Tempalte", "name": "GigabitEthernet6"},
                ],
                "state": "overridden",
            },
        )
        commands = [
            "interface GigabitEthernet3",
            "no bfd local-address 10.0.1.2",
            "no bfd interval 50 min_rx 50 multiplier 3",
            "interface GigabitEthernet1",
            "bfd enable",
            "bfd echo",
            "bfd jitter",
            "bfd local-address 10.0.1.2",
            "bfd interval 100 min_rx 100 multiplier 3",
            "bfd template ANSIBLE",
            "interface GigabitEthernet2",
            "bfd enable",
            "bfd echo",
            "bfd interval 100 min_rx 100 multiplier 3",
            "no bfd template OLD_TEMPLATE",
            "no bfd jitter",
            "interface GigabitEthernet6",
            "bfd template ANSIBLE_3Tempalte",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             description Ansible UT interface 1
             no shutdown
             bfd local-address 10.0.0.1
             bfd interval 57 min_rx 66 multiplier 45
            interface GigabitEthernet2
             description Ansible UT interface 2
             ip address dhcp
             bfd template OLD_TEMPLATE
            interface GigabitEthernet3
             description Ansible UT interface 3
             no ip address
             shutdown
             bfd jitter
             bfd local-address 10.0.1.2
             bfd interval 50 min_rx 50 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "local_address": "10.0.1.2",
                        "name": "GigabitEthernet1",
                        "template": "ANSIBLE",
                    },
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
                        "name": "GigabitEthernet2",
                    },
                    {"template": "ANSIBLE_3Tempalte", "name": "GigabitEthernet6"},
                ],
                "state": "deleted",
            },
        )
        commands = [
            "interface GigabitEthernet1",
            "no bfd local-address 10.0.0.1",
            "no bfd interval 57 min_rx 66 multiplier 45",
            "interface GigabitEthernet2",
            "no bfd template OLD_TEMPLATE",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_action_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet1
             description Ansible UT interface 1
             no shutdown
             bfd local-address 10.0.0.1
             bfd interval 57 min_rx 66 multiplier 45
            interface GigabitEthernet2
             description Ansible UT interface 2
             no bfd enable
             no bfd echo
             no bfd jitter
             ip address dhcp
             bfd template OLD_TEMPLATE
            interface GigabitEthernet3
             description Ansible UT interface 3
             no ip address
             shutdown
             bfd local-address 10.0.1.2
             bfd interval 50 min_rx 50 multiplier 3
            """,
        )
        for states in ["merged", "replaced", "overridden"]:
            set_module_args(
                {
                    "config": [
                        {
                            "name": "GigabitEthernet1",
                            "local_address": "10.0.0.1",
                            "interval": {"input": 57, "min_rx": 66, "multiplier": 45},
                        },
                        {
                            "name": "GigabitEthernet2",
                            "bfd": False,
                            "echo": False,
                            "jitter": False,
                            "template": "OLD_TEMPLATE",
                        },
                        {
                            "name": "GigabitEthernet3",
                            "local_address": "10.0.1.2",
                            "interval": {"input": 50, "min_rx": 50, "multiplier": 3},
                        },
                    ],
                    "state": states,
                },
            )
            commands = []

            result = self.execute_module(changed=False)
            self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet2
                     description Ansible UT interface 1
                     no shutdown
                     no bfd enable
                     no bfd echo
                     bfd local-address 10.0.1.2
                     bfd interval 100 min_rx 100 multiplier 3
                    interface GigabitEthernet3
                     description Ansible UT interface 2
                     ip address dhcp
                     bfd interval 100 min_rx 100 multiplier 3
                    interface GigabitEthernet4
                     bfd template ANSIBLE_Template
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "GigabitEthernet2",
                "bfd": False,
                "echo": False,
                "local_address": "10.0.1.2",
                "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
            },
            {
                "name": "GigabitEthernet3",
                "interval": {"input": 100, "min_rx": 100, "multiplier": 3},
            },
            {"name": "GigabitEthernet4", "template": "ANSIBLE_Template"},
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_bfd_interfaces_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "GigabitEthernet1",
                        "local_address": "10.0.0.1",
                        "interval": {"input": 57, "min_rx": 66, "multiplier": 45},
                    },
                    {"name": "GigabitEthernet2", "template": "OLD_TEMPLATE"},
                    {
                        "name": "GigabitEthernet3",
                        "jitter": True,
                        "local_address": "10.0.1.2",
                        "interval": {"input": 50, "min_rx": 50, "multiplier": 3},
                    },
                ],
                state="rendered",
            ),
        )

        commands = [
            "interface GigabitEthernet1",
            "bfd local-address 10.0.0.1",
            "bfd interval 57 min_rx 66 multiplier 45",
            "interface GigabitEthernet2",
            "bfd template OLD_TEMPLATE",
            "interface GigabitEthernet3",
            "bfd jitter",
            "bfd local-address 10.0.1.2",
            "bfd interval 50 min_rx 50 multiplier 3",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
