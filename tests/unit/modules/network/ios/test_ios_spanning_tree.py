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
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_spanning_tree
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosSpanningTreeModule(TestIosModule):
    module = ios_spanning_tree

    def setUp(self):
        super(TestIosSpanningTreeModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.spanning_tree.spanning_tree."
            "Spanning_treeFacts.get_spanning_tree_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosSpanningTreeModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
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
            "backbonefast": True,
            "bridge_assurance": False,
            "forward_time": [
                {
                    "value": 20,
                    "vlan_list": "1,7-20",
                },
            ],
            "hello_time": [
                {
                    "value": 4,
                    "vlan_list": "1,3,9",
                },
                {
                    "value": 5,
                    "vlan_list": "4,6-8",
                },
                {
                    "value": 6,
                    "vlan_list": "5",
                },
            ],
            "logging": True,
            "loopguard_default": True,
            "max_age": [
                {
                    "value": 38,
                    "vlan_list": "1-2,4-5",
                },
            ],
            "mode": "mst",
            "mst": {
                "configuration": {
                    "instances": [
                        {
                            "instance": 1,
                            "vlan_list": "40-50",
                        },
                        {
                            "instance": 2,
                            "vlan_list": "10-20",
                        },
                    ],
                    "name": "NAME",
                    "revision": 34,
                },
                "forward_time": 25,
                "hello_time": 4,
                "max_age": 33,
                "max_hops": 33,
                "priority": [
                    {
                        "instance": "0",
                        "value": 12288,
                    },
                    {
                        "instance": "1",
                        "value": 4096,
                    },
                    {
                        "instance": "5,7-9",
                        "value": 57344,
                    },
                ],
                "simulate_pvst_global": False,
            },
            "pathcost_method": "long",
            "portfast": {
                "edge_bpdufilter_default": True,
                "edge_bpduguard_default": True,
                "edge_default": True,
            },
            "priority": [
                {
                    "value": 24576,
                    "vlan_list": "1,3-5,7,9-11",
                },
            ],
            "transmit_hold_count": 5,
            "uplinkfast": {
                "enabled": True,
                "max_update_rate": 32,
            },
        }
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_spanning_tree_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    spanning-tree mode mst
                    no spanning-tree bridge assurance
                    spanning-tree transmit hold-count 5
                    spanning-tree loopguard default
                    spanning-tree logging
                    spanning-tree portfast edge default
                    spanning-tree portfast edge bpduguard default
                    spanning-tree portfast edge bpdufilter default
                    no spanning-tree etherchannel guard misconfig
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
                ),
                state="parsed",
            ),
        )

        parsed = {
            "backbonefast": True,
            "bridge_assurance": False,
            "etherchannel_guard_misconfig": False,
            "forward_time": [
                {
                    "value": 20,
                    "vlan_list": "1,7-20",
                },
            ],
            "hello_time": [
                {
                    "value": 4,
                    "vlan_list": "1,3,9",
                },
                {
                    "value": 5,
                    "vlan_list": "4,6-8",
                },
                {
                    "value": 6,
                    "vlan_list": "5",
                },
            ],
            "logging": True,
            "loopguard_default": True,
            "max_age": [
                {
                    "value": 38,
                    "vlan_list": "1-2,4-5",
                },
            ],
            "mode": "mst",
            "mst": {
                "configuration": {
                    "instances": [
                        {
                            "instance": 1,
                            "vlan_list": "40-50",
                        },
                        {
                            "instance": 2,
                            "vlan_list": "10-20",
                        },
                    ],
                    "name": "NAME",
                    "revision": 34,
                },
                "forward_time": 25,
                "hello_time": 4,
                "max_age": 33,
                "max_hops": 33,
                "priority": [
                    {
                        "instance": "0",
                        "value": 12288,
                    },
                    {
                        "instance": "1",
                        "value": 4096,
                    },
                    {
                        "instance": "5,7-9",
                        "value": 57344,
                    },
                ],
                "simulate_pvst_global": False,
            },
            "pathcost_method": "long",
            "portfast": {
                "edge_bpdufilter_default": True,
                "edge_bpduguard_default": True,
                "edge_default": True,
            },
            "priority": [
                {
                    "value": 24576,
                    "vlan_list": "1,3-5,7,9-11",
                },
            ],
            "transmit_hold_count": 5,
            "uplinkfast": {
                "enabled": True,
                "max_update_rate": 32,
            },
        }

        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_ios_spanning_tree_rendered(self):
        set_module_args(
            dict(
                config={
                    "mode": "mst",
                    "backbonefast": True,
                    "bridge_assurance": False,
                    "etherchannel_guard_misconfig": False,
                    "mst": {
                        "configuration": {
                            "instances": [
                                {
                                    "instance": 1,
                                    "vlan_list": "40-50",
                                },
                                {
                                    "instance": 2,
                                    "vlan_list": "20-30",
                                },
                            ],
                            "name": "NAME",
                            "revision": 34,
                        },
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                        "max_hops": 33,
                        "priority": [
                            {
                                "instance": "0",
                                "value": 12288,
                            },
                            {
                                "instance": "1",
                                "value": 4096,
                            },
                            {
                                "instance": "5-7,9",
                                "value": 57344,
                            },
                        ],
                        "simulate_pvst_global": False,
                    },
                    "portfast": {
                        "edge_bpdufilter_default": True,
                        "edge_default": True,
                    },
                    "hello_time": [
                        {
                            "value": 6,
                            "vlan_list": "1-3,5-6",
                        },
                    ],
                },
                state="rendered",
            ),
        )
        commands = [
            "spanning-tree mode mst",
            "spanning-tree backbonefast",
            "no spanning-tree bridge assurance",
            "no spanning-tree etherchannel guard misconfig",
            "no spanning-tree mst simulate pvst global",
            "spanning-tree portfast edge default",
            "spanning-tree portfast edge bpdufilter default",
            "spanning-tree mst 0 priority 12288",
            "spanning-tree mst 1 priority 4096",
            "spanning-tree mst 5-7,9 priority 57344",
            "spanning-tree mst forward-time 25",
            "spanning-tree mst hello-time 4",
            "spanning-tree mst max-age 33",
            "spanning-tree mst max-hops 33",
            "spanning-tree vlan 1-3,5-6 hello-time 6",
            "spanning-tree mst configuration",
            "name NAME",
            "revision 34",
            "instance 1 vlan 40-50",
            "instance 2 vlan 20-30",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(commands))

    def test_ios_spanning_tree_merged_idempotent1(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode rapid-pvst
            """,
        )
        set_module_args(
            dict(
                config={
                    "mst": {
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                    },
                },
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)

    def test_ios_spanning_tree_merged_idempotent2(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode rapid-pvst
            """,
        )
        set_module_args(
            dict(
                config={
                    "mode": "mst",
                    "mst": {
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                    },
                },
                state="merged",
            ),
        )
        commands = [
            "spanning-tree mode mst",
            "spanning-tree mst hello-time 4",
            "spanning-tree mst forward-time 25",
            "spanning-tree mst max-age 33",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_merged_idempotent3(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode mst
            """,
        )
        set_module_args(
            dict(
                config={
                    "mode": "rapid-pvst",
                    "mst": {
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                    },
                },
                state="merged",
            ),
        )
        commands = [
            "spanning-tree mode rapid-pvst",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_merged_idempotent4(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode mst
            no spanning-tree bridge assurance
            spanning-tree transmit hold-count 5
            spanning-tree loopguard default
            spanning-tree logging
            spanning-tree portfast edge default
            spanning-tree portfast edge bpdufilter default
            spanning-tree extend system-id
            spanning-tree uplinkfast max-update-rate 32
            spanning-tree uplinkfast
            spanning-tree pathcost method long
            spanning-tree mst hello-time 4
            spanning-tree mst forward-time 25
            spanning-tree mst max-age 33
            spanning-tree mst max-hops 33
            spanning-tree mst 0 priority 12288
            spanning-tree mst 1 priority 4096
            spanning-tree mst 5,7-9 priority 57344
            spanning-tree vlan 1,3,9 hello-time 4
            spanning-tree vlan 4,6-8 hello-time 5
            spanning-tree mst configuration
             name NAME
             revision 34
             instance 1 vlan 40-50
             instance 2 vlan 10-20
            """,
        )
        set_module_args(
            dict(
                config={
                    "backbonefast": True,
                    "bridge_assurance": True,
                    "mst": {
                        "configuration": {
                            "instances": [
                                {
                                    "instance": 1,
                                    "vlan_list": "40-50",
                                },
                                {
                                    "instance": 2,
                                    "vlan_list": "20-30",
                                },
                            ],
                            "name": "NAME",
                            "revision": 34,
                        },
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                        "max_hops": 33,
                        "priority": [
                            {
                                "instance": "0",
                                "value": 12288,
                            },
                            {
                                "instance": "1",
                                "value": 4096,
                            },
                            {
                                "instance": "5-7,9",
                                "value": 57344,
                            },
                        ],
                        "simulate_pvst_global": False,
                    },
                    "portfast": {
                        "edge_bpdufilter_default": True,
                        "edge_default": True,
                    },
                    "hello_time": [
                        {
                            "value": 6,
                            "vlan_list": "1-3,5-6",
                        },
                    ],
                },
                state="merged",
            ),
        )
        commands = [
            "spanning-tree backbonefast",
            "spanning-tree bridge assurance",
            "no spanning-tree mst simulate pvst global",
            "spanning-tree mst 6 priority 57344",
            "spanning-tree vlan 1-3,5-6 hello-time 6",
            "spanning-tree mst configuration",
            "instance 2 vlan 21-30",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_merged_idempotent5(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode pvst
            """,
        )
        set_module_args(
            dict(
                config={
                    "bridge_assurance": False,
                    "etherchannel_guard_misconfig": False,
                },
                state="merged",
            ),
        )
        commands = [
            "no spanning-tree bridge assurance",
            "no spanning-tree etherchannel guard misconfig",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode mst
            spanning-tree extend system-id
            no spanning-tree bridge assurance
            spanning-tree transmit hold-count 10
            spanning-tree loopguard default
            spanning-tree portfast edge default
            spanning-tree portfast edge bpduguard default
            spanning-tree portfast edge bpdufilter default
            no spanning-tree etherchannel guard misconfig
            spanning-tree uplinkfast
            spanning-tree backbonefast
            spanning-tree mst hello-time 4
            spanning-tree mst forward-time 25
            spanning-tree mst max-age 33
            spanning-tree mst max-hops 33
            no spanning-tree mst simulate pvst global
            spanning-tree mst 0 priority 12288
            spanning-tree mst 1 priority 4096
            spanning-tree mst 5,7-9 priority 57344
            spanning-tree vlan 1,3-5,7,9-11 priority 24576
            spanning-tree vlan 1,3,9 hello-time 4
            spanning-tree vlan 4,6-8 hello-time 5
            spanning-tree vlan 5 hello-time 6
            spanning-tree vlan 1,7-20 forward-time 20
            spanning-tree vlan 1-2,4-5 max-age 38
            spanning-tree pathcost method long
            spanning-tree uplinkfast max-update-rate 32
            spanning-tree mst configuration
             name NAME
             revision 34
             instance 1 vlan 40-50
             instance 2 vlan 10-20
            """,
        )
        set_module_args(
            dict(
                config={
                    "mode": "rapid-pvst",
                    "logging": True,
                    "priority": [
                        {
                            "value": 24576,
                            "vlan_list": "1,3-5",
                        },
                    ],
                    "mst": {
                        "priority": [
                            {
                                "instance": "7-9",
                                "value": 57344,
                            },
                        ],
                    },
                },
                state="replaced",
            ),
        )
        commands = [
            "spanning-tree mode rapid-pvst",
            "spanning-tree logging",
            "spanning-tree bridge assurance",
            "no spanning-tree transmit hold-count 10",
            "no spanning-tree loopguard default",
            "no spanning-tree portfast edge default",
            "no spanning-tree portfast edge bpduguard default",
            "no spanning-tree portfast edge bpdufilter default",
            "spanning-tree etherchannel guard misconfig",
            "spanning-tree mst simulate pvst global",
            "no spanning-tree uplinkfast",
            "no spanning-tree backbonefast",
            "no spanning-tree vlan 7,9-11 priority 24576",
            "no spanning-tree vlan 1,3,9 hello-time 4",
            "no spanning-tree vlan 4,6-8 hello-time 5",
            "no spanning-tree vlan 5 hello-time 6",
            "no spanning-tree vlan 1,7-20 forward-time 20",
            "no spanning-tree vlan 1-2,4-5 max-age 38",
            "no spanning-tree mst configuration",
            "no spanning-tree pathcost method long",
            "no spanning-tree uplinkfast max-update-rate 32",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_deleted_idempotent1(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mst configuration
             name NAME
             revision 34
             instance 1 vlan 40-50
             instance 2 vlan 10-20
            """,
        )
        set_module_args(
            dict(
                config={
                    "mst": {
                        "configuration": {
                            "name": "NAME",
                            "revision": 34,
                            "instances": [
                                {
                                    "instance": 1,
                                    "vlan_list": "30-45",
                                },
                            ],
                        },
                    },
                },
                state="deleted",
            ),
        )
        commands = [
            "spanning-tree mst configuration",
            "no name NAME",
            "no revision 34",
            "no instance 1 vlan 40-45",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_deleted_idempotent2(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mst configuration
             name NAME
             revision 34
             instance 1 vlan 40-50
             instance 2 vlan 10-20
            """,
        )
        set_module_args(
            dict(
                config={
                    "mst": {
                        "configuration": {
                            "name": "NAME",
                            "revision": 34,
                            "instances": [
                                {
                                    "instance": 1,
                                    "vlan_list": "40-50",
                                },
                                {
                                    "instance": 2,
                                    "vlan_list": "10-20",
                                },
                            ],
                        },
                    },
                },
                state="deleted",
            ),
        )
        commands = [
            "no spanning-tree mst configuration",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_deleted_idempotent3(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode rapid-pvst
            no spanning-tree bridge assurance
            no spanning-tree etherchannel guard misconfig
            no spanning-tree mst simulate pvst global
            """,
        )
        set_module_args(
            dict(
                config={
                    "bridge_assurance": False,
                    "etherchannel_guard_misconfig": False,
                    "mst": {
                        "simulate_pvst_global": False,
                    },
                },
                state="deleted",
            ),
        )
        commands = [
            "spanning-tree mst simulate pvst global",
            "spanning-tree bridge assurance",
            "spanning-tree etherchannel guard misconfig",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_deleted_idempotent4(self):
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
            spanning-tree vlan 1,7-12,16-20 forward-time 20
            spanning-tree vlan 1-2,4-5 max-age 38
            """,
        )
        set_module_args(
            dict(
                config={
                    "bridge_assurance": False,
                    "transmit_hold_count": 5,
                    "uplinkfast": {
                        "enabled": True,
                        "max_update_rate": 32,
                    },
                    "logging": False,
                    "portfast": {
                        "edge_bpdufilter_default": True,
                        "edge_bpduguard_default": True,
                        "edge_default": True,
                    },
                    "backbonefast": True,
                    "etherchannel_guard_misconfig": True,
                    "pathcost_method": "long",
                    "forward_time": [
                        {"value": 20, "vlan_list": "9-15,18-30"},
                    ],
                    "priority": [
                        {"value": 24576, "vlan_list": "7,8"},
                    ],
                    "hello_time": [
                        {"value": 4, "vlan_list": "1,3,9"},
                        {"value": 5, "vlan_list": "4,6-8"},
                        {"value": 6, "vlan_list": "5"},
                    ],
                    "max_age": [
                        {"value": 38, "vlan_list": "1-2,4-5"},
                    ],
                    "mst": {
                        "forward_time": 25,
                        "hello_time": 4,
                        "max_age": 33,
                        "max_hops": 33,
                        "simulate_pvst_global": False,
                        "configuration": {
                            "instances": [
                                {
                                    "instance": 1,
                                    "vlan_list": "40-50",
                                },
                            ],
                        },
                    },
                },
                state="deleted",
            ),
        )
        commands = [
            "spanning-tree bridge assurance",
            "no spanning-tree transmit hold-count 5",
            "no spanning-tree uplinkfast max-update-rate 32",
            "no spanning-tree uplinkfast",
            "no spanning-tree portfast edge bpdufilter default",
            "no spanning-tree portfast edge default",
            "no spanning-tree portfast edge bpduguard default",
            "no spanning-tree backbonefast",
            "no spanning-tree pathcost method long",
            "no spanning-tree vlan 9-12,18-20 forward-time 20",
            "no spanning-tree vlan 7 priority 24576",
            "no spanning-tree vlan 5 hello-time 6",
            "no spanning-tree vlan 1-2,4-5 max-age 38",
            "no spanning-tree vlan 4,6-8 hello-time 5",
            "no spanning-tree vlan 1,3,9 hello-time 4",
            "spanning-tree mst simulate pvst global",
            "no spanning-tree mst hello-time 4",
            "no spanning-tree mst forward-time 25",
            "no spanning-tree mst max-age 33",
            "no spanning-tree mst max-hops 33",
            "spanning-tree mst configuration",
            "no instance 1 vlan 40-50",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_spanning_tree_deleted_idempotent5(self):
        self.execute_show_command.return_value = dedent(
            """\
            spanning-tree mode rapid-pvst
            spanning-tree extend system-id
            spanning-tree transmit hold-count 5
            spanning-tree loopguard default
            """,
        )
        set_module_args(
            dict(
                config={},
                state="deleted",
            ),
        )
        commands = [
            "no spanning-tree transmit hold-count 5",
            "no spanning-tree loopguard default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
