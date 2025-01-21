# (c) 2024 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vrf_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosVrfInterfacesModule(TestIosModule):
    module = ios_vrf_interfaces

    def setUp(self):
        super(TestIosVrfInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_interfaces.vrf_interfaces."
            "Vrf_interfacesFacts.get_vrf_interfaces_data",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestIosVrfInterfacesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_ios_vrf_interfaces_merged_idempotent(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
             ip address dhcp
             no shutdown
             !

            interface GigabitEthernet2
             no ip address
             shutdown
             !

            interface GigabitEthernet3
             no ip address
             shutdown
             !

            interface GigabitEthernet4
             no ip address
             shutdown
             !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3", "vrf_name": "testvrf2"},
                    {"name": "GigabitEthernet3", "vrf_name": "testvrf2"},
                    {"name": "GigabitEthernet4", "vrf_name": "testvrf1"},
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "vrf forwarding testvrf1",
            "interface GigabitEthernet3",
            "vrf forwarding testvrf2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_interfaces_merged(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
             ip address dhcp
             no shutdown
             !

            interface GigabitEthernet2
             no ip address
             shutdown
             !

            interface GigabitEthernet3
             no ip address
             shutdown
             !

            interface GigabitEthernet4
             no ip address
             shutdown
             !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3"},
                    {"name": "GigabitEthernet4", "vrf_name": "testvrf1"},
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "vrf forwarding testvrf1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_interfaces_replaced(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
             ip address dhcp
             no shutdown
             !

            interface GigabitEthernet2
             no ip address
             shutdown
             !

            interface GigabitEthernet3
             no ip address
             shutdown
             !

            interface GigabitEthernet4
             vrf forwarding vrf_2
             no shutdown
             !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3"},
                    {"name": "GigabitEthernet4", "vrf_name": "testvrf1_replaced"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "vrf forwarding testvrf1_replaced",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_interfaces_deleted(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
             ip address dhcp
             no shutdown
             !

            interface GigabitEthernet2
             no ip address
             shutdown
             !

            interface GigabitEthernet3
             vrf forwarding vrf_3
             no shutdown
             !

            interface GigabitEthernet4
             vrf forwarding vrf_2
             no shutdown
             !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3"},
                    {"name": "GigabitEthernet4"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet4",
            "no vrf forwarding vrf_2",
            "interface GigabitEthernet3",
            "no vrf forwarding vrf_3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet1
                    ip address dhcp
                    no shutdown
                    !

                    interface GigabitEthernet2
                    vrf forwarding vrf_1
                    shutdown
                    !

                    interface GigabitEthernet3
                    no shutdown
                    !

                    interface GigabitEthernet4
                    vrf forwarding vrf_2
                    no shutdown
                    !
                    """,
                ),
                state="parsed",
            ),
        )
        parsed_list = [
            {"name": "GigabitEthernet1"},
            {"name": "GigabitEthernet2", "vrf_name": "vrf_1"},
            {"name": "GigabitEthernet3"},
            {"name": "GigabitEthernet4", "vrf_name": "vrf_2"},
        ]
        result = self.execute_module(changed=False)

        self.assertEqual(result["parsed"], parsed_list)

    def test_ios_vrf_interfaces_overridden(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
             ip address dhcp
             no shutdown
             !

            interface GigabitEthernet2
             vrf forwarding vrf_1
             shutdown
             !

            interface GigabitEthernet3
             vrf forwarding vrf_2
             shutdown
             !

            interface GigabitEthernet4
             no shutdown
             !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3"},
                    {"name": "GigabitEthernet4", "vrf_name": "vrf_5"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet2",
            "no vrf forwarding vrf_1",
            "interface GigabitEthernet3",
            "no vrf forwarding vrf_2",
            "interface GigabitEthernet4",
            "vrf forwarding vrf_5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_interfaces_replaced_idempotent(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
            ip address dhcp
            no shutdown
            !

            interface GigabitEthernet2
            no ip address
            shutdown
            !

            interface GigabitEthernet3
            vrf forwarding testvrf2
            no ip address
            shutdown
            !

            interface GigabitEthernet4
            vrf forwarding testvrf1
            no ip address
            shutdown
            !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3", "vrf_name": "testvrf2"},
                    {"name": "GigabitEthernet4", "vrf_name": "testvrf1"},
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_interfaces_overridden_idempotent(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
            ip address dhcp
            no shutdown
            !

            interface GigabitEthernet2
            no ip address
            shutdown
            !

            interface GigabitEthernet3
            vrf forwarding testvrf2
            no ip address
            shutdown
            !

            interface GigabitEthernet4
            vrf forwarding testvrf1
            no ip address
            shutdown
            !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2"},
                    {"name": "GigabitEthernet3", "vrf_name": "testvrf2"},
                    {"name": "GigabitEthernet4", "vrf_name": "testvrf1"},
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_interfaces_gathered(self):
        self.maxDiff = None
        run_cfg = dedent(
            """\
            interface GigabitEthernet1
            ip address dhcp
            no shutdown
            !

            interface GigabitEthernet2
            vrf forwarding vrf_1
            shutdown
            !

            interface GigabitEthernet3
            vrf forwarding vrf_2
            no ip address
            shutdown
            !

            interface GigabitEthernet4
            no shutdown
            !
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(dict(state="gathered"))
        gathered_list = [
            {"name": "GigabitEthernet1"},
            {"name": "GigabitEthernet2", "vrf_name": "vrf_1"},
            {"name": "GigabitEthernet3", "vrf_name": "vrf_2"},
            {"name": "GigabitEthernet4"},
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered_list)

    def test_ios_vrf_interfaces_rendered(self):
        self.maxDiff = None
        set_module_args(
            dict(
                config=[
                    {"name": "GigabitEthernet1"},
                    {"name": "GigabitEthernet2", "vrf_name": "vrf_1"},
                    {"name": "GigabitEthernet3", "vrf_name": "vrf_2"},
                    {"name": "GigabitEthernet4"},
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet2",
            "vrf forwarding vrf_1",
            "interface GigabitEthernet3",
            "vrf forwarding vrf_2",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
