#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_lldp_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLldpInterfacesModule(TestIosModule):
    module = ios_lldp_interfaces

    def setUp(self):
        super(TestIosLldpInterfacesModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lldp_interfaces.lldp_interfaces."
            "Lldp_InterfacesFacts.get_lldp_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLldpInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_lldp_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            GigabitEthernet0/0:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME

            GigabitEthernet0/1:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME

            GigabitEthernet0/2:
                Tx: disabled
                Rx: disabled
                Tx state: IDLE
                Rx state: INIT

            GigabitEthernet0/3:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet0/1", "receive": True, "transmit": True},
                    {"name": "GigabitEthernet0/2", "receive": True},
                    {"name": "GigabitEthernet0/3", "transmit": True},
                ],
                state="merged",
            ),
        )
        commands = ["interface GigabitEthernet0/2", "lldp receive"]
        result = self.execute_module(changed=True)
        # print(result["commands"])
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            GigabitEthernet0/0:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME

            GigabitEthernet0/1:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME

            GigabitEthernet0/2:
               Tx: disabled
               Rx: disabled
               Tx state: IDLE
               Rx state: INIT

            GigabitEthernet0/3:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet0/2", "receive": True, "transmit": True},
                    {"name": "GigabitEthernet0/3", "receive": False},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "lldp receive",
            "lldp transmit",
            "interface GigabitEthernet0/3",
            "no lldp transmit",
            "no lldp receive",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lag_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            GigabitEthernet0/0:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME

            GigabitEthernet0/1:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME

            GigabitEthernet0/2:
               Tx: disabled
               Rx: disabled
               Tx state: IDLE
               Rx state: INIT

            GigabitEthernet0/3:
               Tx: enabled
               Rx: enabled
               Tx state: IDLE
               Rx state: WAIT FOR FRAME
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet0/2", "receive": True, "transmit": True},
                ],
                state="overridden",
            ),
        )

        commands = [
            "interface GigabitEthernet0/0",
            "no lldp receive",
            "no lldp transmit",
            "interface GigabitEthernet0/1",
            "no lldp receive",
            "no lldp transmit",
            "interface GigabitEthernet0/2",
            "lldp receive",
            "lldp transmit",
            "interface GigabitEthernet0/3",
            "no lldp receive",
            "no lldp transmit",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            GigabitEthernet0/0:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME

            GigabitEthernet0/1:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME

            GigabitEthernet0/2:
                Tx: disabled
                Rx: disabled
                Tx state: IDLE
                Rx state: INIT

            GigabitEthernet0/3:
                Tx: enabled
                Rx: enabled
                Tx state: IDLE
                Rx state: WAIT FOR FRAME
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(name="GigabitEthernet0/2"),
                    dict(name="GigabitEthernet0/1"),
                ],
                state="deleted",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no lldp receive",
            "no lldp transmit",
        ]
        res = self.execute_module(changed=True)
        self.assertEqual(res["commands"], commands)

    def test_ios_lldp_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    GigabitEthernet0/0:
                        Tx: enabled
                        Rx: disabled
                        Tx state: IDLE
                        Rx state: WAIT FOR FRAME

                    GigabitEthernet0/1:
                        Tx: enabled
                        Rx: enabled
                        Tx state: IDLE
                        Rx state: WAIT FOR FRAME

                    GigabitEthernet0/2:
                        Tx: disabled
                        Rx: enabled
                        Tx state: IDLE
                        Rx state: INIT
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {"name": "GigabitEthernet0/0", "transmit": True, "receive": False},
            {"name": "GigabitEthernet0/1", "transmit": True, "receive": True},
            {"name": "GigabitEthernet0/2", "transmit": False, "receive": True},
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_lldp_interfaces_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet0/0", "transmit": True, "receive": False},
                    {"name": "GigabitEthernet0/1", "transmit": True, "receive": True},
                    {"name": "GigabitEthernet0/2", "transmit": False, "receive": True},
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet0/0",
            "no lldp receive",
            "lldp transmit",
            "interface GigabitEthernet0/1",
            "lldp receive",
            "lldp transmit",
            "interface GigabitEthernet0/2",
            "lldp receive",
            "no lldp transmit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
