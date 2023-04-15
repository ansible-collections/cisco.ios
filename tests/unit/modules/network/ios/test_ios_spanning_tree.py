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

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_spanning_tree
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosSpanningTreeModule(TestIosModule):
    module = ios_spanning_tree

    def setUp(self):
        super(TestIosSpanningTreeModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.spanning_tree.spanning_tree."
            "Spanning_treeFacts.get_spanning_tree_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()


    def tearDown(self):
        super(TestIosSpanningTreeModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()


    def test_ios_spanning_tree_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode mst
            no spanning-tree bridge assurance
            spanning-tree transmit hold-count 5
            spanning-tree loopguard default
            spanning-tree logging
            spanning-tree portfast edge default
            spanning-tree portfast edge bpduguard default
            spanning-tree portfast edge bpdufilter default
            spanning-tree queue maxsize 16786
            spanning-tree etherchannel guard misconfig
            spanning-tree extend system-id
            spanning-tree uplinkfast max-update-rate 32
            spanning-tree uplinkfast
            spanning-tree backbonefast
            spanning-tree pathcost method long
            no spanning-tree mst simulate pvst global
            spanning-tree mst configuration
             name NAME
             revision 34
             instance 1 vlan 40-50
             instance 2 vlan 10-20
            spanning-tree mst hello-time 4
            spanning-tree mst forward-time 25
            spanning-tree mst max-age 33
            spanning-tree mst max-hops 33
            spanning-tree mst 0 priority 12288
            spanning-tree mst 1 priority 4096
            spanning-tree mst 5,7-9 priority 57344
            spanning-tree vlan 1,3-5,7,9-11 priority 24576
            spanning-tree vlan 1,3,9 hello-time 4
            spanning-tree vlan 4,6-8 hello-time 5
            spanning-tree vlan 5 hello-time 6
            spanning-tree vlan 1,7-20 forward-time 20
            spanning-tree vlan 1-2,4-5 max-age 38
            """,
        )
        gathered = {
            "spanning_tree": {
                "backbonefast": True,
                "bridge_assurance": False,
                "etherchannel_guard_misconfig": True,
                "extend_system_id": True,
                "forward_time": [
                    {
                        "value": 20,
                        "vlan_list": [ 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                    }
                ],
                "hello_time": [
                    {
                        "value": 4,
                        "vlan_list": [ 1, 3, 9 ]
                    },
                    {
                        "value": 5,
                        "vlan_list": [ 4, 6, 7, 8 ]
                    },
                    {
                        "value": 6,
                        "vlan_list": [ 5 ]
                    }
                ],
                "logging": True,
                "loopguard_default": True,
                "max_age": [
                    {
                        "value": 38,
                        "vlan_list": [ 1, 2, 4, 5 ]
                    }
                ],
                "mode": "mst",
                "mst": {
                    "configuration": {
                        "instances": [
                            {
                                "instance": 1,
                                "vlan_list": [ 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 ]
                            },
                            {
                                "instance": 2,
                                "vlan_list": [ 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]
                            }
                        ],
                        "name": "NAME",
                        "revision": 34
                    },
                    "forward_time": 25,
                    "hello_time": 4,
                    "max_age": 33,
                    "max_hops": 33,
                    "priority": [
                        {
                            "instance": [ 0 ],
                            "value": 12288
                        },
                        {
                            "instance": [ 1 ],
                            "value": 4096
                        },
                        {
                            "instance": [ 5, 7, 8, 9 ],
                            "value": 57344
                        }
                    ],
                    "simulate_pvst_global": False
                },
                "pathcost_method": "long",
                "portfast": {
                    "bpdufilter_default": True,
                    "bpduguard_default": True,
                    "edge_default": True
                },
                "priority": [
                    {
                        "value": 24576,
                        "vlan_list": [ 1, 3, 4, 5, 7, 9, 10, 11 ]
                    }
                ],
                "transmit_hold_count": 5,
                "uplinkfast": {
                    "enabled": True,
                    "max_update_rate": 32
                }
            }
        }
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_spanning_tree_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode mst
            no spanning-tree bridge assurance
            spanning-tree transmit hold-count 5
            spanning-tree loopguard default
            spanning-tree logging
            spanning-tree portfast edge default
            spanning-tree portfast edge bpdufilter default
            spanning-tree queue maxsize 16786
            spanning-tree etherchannel guard misconfig
            spanning-tree extend system-id
            spanning-tree uplinkfast max-update-rate 32
            spanning-tree uplinkfast
            spanning-tree pathcost method long
            spanning-tree mst simulate pvst global
            spanning-tree mst hello-time 4
            spanning-tree mst forward-time 25
            spanning-tree mst max-age 33
            spanning-tree mst max-hops 33
            spanning-tree mst 0 priority 12288
            spanning-tree mst 1 priority 4096
            spanning-tree mst 5,7-9 priority 57344
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    spanning_tree=dict(
                        backbonefast=True,
                        bridge_assurance=True,
                        mst=dict(
                            simulate_pvst_global=False,
                            priority = [
                                dict(
                                    instance = [ 0 ],
                                    value = 12288
                                ),
                                dict(
                                    instance = [ 1 ],
                                    value = 4096
                                ),
                                dict(
                                    instance = [ 5, 9, 6, 7, ],
                                    value = 57344
                                ),
                            ],
                        ),
                        portfast=dict(
                            bpduguard_default=False,
                        ),
                    ),
                ),
                state="merged",
            ),
        )
        commands = [
            "spanning-tree backbonefast",
            "spanning-tree bridge assurance",
            "no spanning-tree mst simulate pvst global",
            "spanning-tree mst 6 priority 57344",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
