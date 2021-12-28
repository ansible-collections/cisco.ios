#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_lag_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule


class TestIosLagInterfacesModule(TestIosModule):
    module = ios_lag_interfaces

    def setUp(self):
        super(TestIosLagInterfacesModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lag_interfaces.lag_interfaces."
            "Lag_interfacesFacts.get_lag_interfaces_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLagInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_lag_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             no ip address
            interface Port-channel20
             no ip address
            interface GigabitEthernet1
             ip address dhcp
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "members": [
                            {"member": "GigabitEthernet1", "mode": "active"},
                            {
                                "member": "GigabitEthernet4",
                                "mode": "active",
                                "link": 2,
                            },
                        ],
                        "name": "Port-channel10",
                    }
                ],
                "state": "merged",
            }
        )
        commands = [
            "interface GigabitEthernet1",
            "channel-group 10 mode active",
            "interface GigabitEthernet4",
            "channel-group 10 mode active",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_lag_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             no ip address
            interface Port-channel20
             no ip address
            interface GigabitEthernet1
             ip address dhcp
             channel-group 10 mode active
            interface GigabitEthernet2
             ip address dhcp
            interface GigabitEthernet4
             ip address dhcp
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "members": [
                            {"member": "GigabitEthernet2", "mode": "active"},
                            {"member": "GigabitEthernet4", "mode": "active"},
                        ],
                        "name": "Port-channel10",
                    }
                ],
                "state": "overridden",
            }
        )
        commands = [
            "interface GigabitEthernet1",
            "no channel-group",
            "interface GigabitEthernet2",
            "channel-group 10 mode active",
            "interface GigabitEthernet4",
            "channel-group 10 mode active",
            "no channel-group",
            "channel-group 10 mode active",
            "channel-group 10 mode active",
        ]
        result = self.execute_module(changed=True)
        print(result)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_lag_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
            interface Port-channel20
            interface Port-channel30
            interface GigabitEthernet0/1
             shutdown
             channel-group 10 mode auto
            interface GigabitEthernet0/2
             shutdown
             channel-group 10 mode auto
            interface GigabitEthernet0/3
             shutdown
             channel-group 30 mode on
            interface GigabitEthernet0/4
             shutdown
             channel-group 30 mode active
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "members": [
                            {"member": "GigabitEthernet0/3", "mode": "auto"}
                        ],
                        "name": "Port-channel30",
                    }
                ],
                "state": "replaced",
            }
        )
        commands = [
            "interface GigabitEthernet0/3",
            "channel-group 30 mode auto",
        ]
        result = self.execute_module(changed=True)
        print(result)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_lag_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Port-channel10
             no ip address
            interface Port-channel20
             no ip address
            interface GigabitEthernet1
             ip address dhcp
             channel-group 10 mode active
            interface GigabitEthernet4
             ip address dhcp
             channel-group 10 mode active
            """
        )
        set_module_args(
            {
                "config": [
                    {
                        "members": [
                            {"member": "GigabitEthernet1", "mode": "active"},
                            {"member": "GigabitEthernet4", "mode": "active"},
                        ],
                        "name": "Port-channel10",
                    }
                ],
                "state": "merged",
            }
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
