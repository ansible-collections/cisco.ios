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
                        "description": "This interface should be disabled",
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "mix_rx": 100, "multiplier": 3},
                        "local_address": "10.0.1.2",
                        "name": "GigabitEthernet1",
                        "template": "ANSIBLE",
                    },
                    {
                        "bfd": True,
                        "echo": True,
                        "jitter": True,
                        "interval": {"input": 100, "mix_rx": 100, "multiplier": 3},
                        "name": "GigabitEthernet2",
                    },
                    {"template": "ANSIBLE_3Tempalte", "name": "GigabitEthernet6"},
                ],
                "state": "merged",
            },
        )
        commands = []
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
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
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = []
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
                        "description": "Ansible UT interface 1",
                        "enabled": False,
                    },
                    {
                        "name": "GigabitEthernet0/1",
                        "description": "Ansible UT interface 2",
                        "speed": "1000",
                        "mtu": 1500,
                        "enabled": True,
                    },
                    {
                        "name": "gigabitEthernet3",
                        "description": "Ansible UT interface 3",
                        "enabled": True,
                        "duplex": "auto",
                    },
                ],
                state="rendered",
            ),
        )

        commands = [
            "interface GigabitEthernet1",
            "description Ansible UT interface 1",
            "shutdown",
            "interface GigabitEthernet0/1",
            "description Ansible UT interface 2",
            "speed 1000",
            "mtu 1500",
            "no shutdown",
            "interface GigabitEthernet3",
            "description Ansible UT interface 3",
            "duplex auto",
            "no shutdown",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
