#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_l2_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosL2InterfacesModule(TestIosModule):
    module = ios_l2_interfaces

    def setUp(self):
        super(TestIosL2InterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2_interfaces.l2_interfaces."
            "L2_interfacesFacts.get_l2_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_l2_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/1",
                        voice=dict(vlan=40),
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["9-15", "20"],
                        ),
                    ),
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="TwoGigabitEthernet1/0/1",
                        trunk=dict(pruning_vlans=["9-19", "20"]),
                        private_vlan={
                            "association": True,
                            "host": True,
                            "primary_range": 2000,
                            "secondary_range": 2500,
                        },
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "switchport access vlan 20",
            "switchport voice vlan 40",
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan add 60",
            "switchport trunk pruning vlan add 9,11-15",
            "interface TwoGigabitEthernet1/0/1",
            "switchport private-vlan association host 2000 2500",
            "switchport trunk pruning vlan 9-20",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/3",
                        trunk=dict(
                            allowed_vlans=[
                                "11",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "461",
                                "674",
                                "675",
                                "696",
                                "931",
                                "935",
                                "951",
                                "952",
                                "973",
                                "974",
                                "979",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            pruning_vlans=["10", "11", "12", "13", "14", "15"],
                            encapsulation="dot1q",
                        ),
                    ),
                ],
                state="merged",
            ),
        )
        self.maxDiff = None
        self.execute_module(changed=False, commands=[])

    def test_ios_l2_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["20-25", "40"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10"],
                        ),
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "no switchport mode",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan remove 10-19",
            "switchport trunk allowed vlan add 21-25",
            "switchport trunk pruning vlan remove 20",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="TwoGigabitEthernet1/0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/3",
                        trunk=dict(
                            allowed_vlans=[
                                "11",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "461",
                                "674",
                                "675",
                                "696",
                                "931",
                                "935",
                                "951",
                                "952",
                                "973",
                                "974",
                                "979",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            pruning_vlans=["10", "11", "12", "13", "14", "15"],
                            encapsulation="dot1q",
                        ),
                    ),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        commands = []
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
             switchport private-vlan association mapping 2000 remove abc
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        voice=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/2",
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport access vlan",
            "no switchport mode",
            "interface TwoGigabitEthernet1/0/1",
            "no switchport access vlan",
            "no switchport mode",
            "no switchport private-vlan association mapping 2000 remove abc",
            "interface GigabitEthernet0/3",
            "no switchport mode",
            "no switchport trunk encapsulation",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
            "interface GigabitEthernet0/2",
            "switchport access vlan 10",
            "switchport voice vlan 20",
            "switchport mode access",
            "no switchport trunk encapsulation",
            "no switchport trunk native vlan",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="TwoGigabitEthernet1/0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/3",
                        trunk=dict(
                            allowed_vlans=[
                                "11",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "461",
                                "674",
                                "675",
                                "696",
                                "931",
                                "935",
                                "951",
                                "952",
                                "973",
                                "974",
                                "979",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            pruning_vlans=["10", "11", "12", "13", "14", "15"],
                            encapsulation="dot1q",
                        ),
                    ),
                ],
                state="overridden",
            ),
        )
        self.maxDiff = None
        self.execute_module(changed=False, commands=[])

    def test_ios_l2_interfaces_deleted_interface(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(dict(config=[dict(name="GigabitEthernet0/1")], state="deleted"))
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport mode",
            "no switchport access vlan",
        ]
        self.maxDiff = None
        self.execute_module(changed=True, commands=commands)

    def test_ios_l2_interfaces_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport access vlan",
            "no switchport mode",
            "interface GigabitEthernet0/2",
            "no switchport mode",
            "no switchport trunk encapsulation",
            "no switchport trunk native vlan",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
            "interface TwoGigabitEthernet1/0/1",
            "no switchport access vlan",
            "no switchport mode",
            "interface GigabitEthernet0/3",
            "no switchport mode",
            "no switchport trunk encapsulation",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet0/1
                     switchport mode access
                     switchport access vlan 10
                    interface GigabitEthernet0/2
                     switchport trunk allowed vlan 10-20,40
                     switchport trunk encapsulation dot1q
                     switchport trunk native vlan 10
                     switchport trunk pruning vlan 10,20
                     switchport mode trunk
                    interface TwoGigabitEthernet1/0/1
                     switchport mode access
                     switchport access vlan 20
                    interface GigabitEthernet0/3
                     switchport trunk allowed vlan 1,2
                     switchport trunk encapsulation dot1q
                     switchport trunk pruning vlan 10-15
                     switchport mode private-vlan trunk secondary
                    interface GigabitEthernet1/0/1
                     switchport mode access
                     switchport nonegotiate
                     switchport protected
                     switchport block multicast
                     switchport block unicast
                     switchport vepa enabled
                     switchport app-interface
                     switchport voice vlan 22
                     snmp trap mac-notification change added
                     snmp trap mac-notification change removed
                     snmp trap link-status permit duplicates
                     spanning-tree portfast
                     spanning-tree bpdufilter enable
                     spanning-tree bpduguard disable
                     spanning-tree link-type point-to-point
                     spanning-tree vlan 9-11 cost 22
                     spanning-tree guard root
                     spanning-tree mst simulate pvst disable
                     spanning-tree mst 0-1 cost 22
                     spanning-tree cost 22
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {"name": "GigabitEthernet0/1", "mode": "access", "access": {"vlan": 10}},
            {
                "name": "GigabitEthernet0/2",
                "trunk": {
                    "allowed_vlans": ["10-20", "40"],
                    "encapsulation": "dot1q",
                    "native_vlan": 10,
                    "pruning_vlans": ["10", "20"],
                },
                "mode": "trunk",
            },
            {"name": "TwoGigabitEthernet1/0/1", "mode": "access", "access": {"vlan": 20}},
            {
                "name": "GigabitEthernet0/3",
                "trunk": {
                    "allowed_vlans": ["1", "2"],
                    "encapsulation": "dot1q",
                    "pruning_vlans": ["10-15"],
                },
                "mode": "private_vlan_trunk",
            },
            {
                "name": "GigabitEthernet1/0/1",
                "mode": "access",
                "nonegotiate": True,
                "protected": True,
                "block_options": {"multicast": True, "unicast": True},
                "vepa": True,
                "app_interface": True,
                "voice": {"vlan": 22},
                "spanning_tree": {
                    "link_type": {"point_to_point": True},
                    "vlan": {"vlan_range": "9-11", "cost": "22"},
                    "guard": {"none": False, "root": True},
                    "mst": {"instance_range": "0-1", "cost": "22"},
                    "cost": 22,
                },
            },
        ]
        self.maxDiff = None
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_l2_interfaces_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/1",
                        voice=dict(vlan=40),
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["12-15", "20"],
                        ),
                    ),
                    dict(
                        name="GigabitEthernet1/0/1",
                        mode="access",
                        nonegotiate=True,
                        protected=True,
                        block_options={"multicast": True, "unicast": True},
                        vepa=True,
                        app_interface=True,
                        voice={"vlan": 22},
                        spanning_tree={
                            "link_type": {"point_to_point": True},
                            "vlan": {"vlan_range": "9-11", "cost": "22"},
                            "guard": {"none": False, "root": True},
                            "mst": {"instance_range": "0-1", "cost": "22"},
                            "cost": 22,
                        },
                        private_vlan={
                            "association": True,
                            "host": True,
                            "primary_range": 2000,
                            "secondary_range": 2500,
                        },
                    ),
                    dict(
                        name="GigabitEthernet1/0/2",
                        private_vlan={
                            "association": True,
                            "mapping": True,
                            "primary_range": 2000,
                            "secondary_vlan_id": "xyz",
                        },
                    ),
                    dict(
                        name="GigabitEthernet1/0/3",
                        private_vlan={
                            "host_association": True,
                            "primary_range": 2000,
                            "secondary_range": 2500,
                        },
                    ),
                    dict(
                        name="GigabitEthernet1/0/4",
                        private_vlan={
                            "mapping": True,
                            "primary_range": 2000,
                            "add": True,
                            "secondary_vlan_id": "xyz",
                        },
                    ),
                    dict(
                        name="GigabitEthernet1/0/5",
                        private_vlan={
                            "mapping": True,
                            "primary_range": 2000,
                            "remove": True,
                            "secondary_vlan_id": "xyz",
                        },
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "switchport access vlan 20",
            "switchport voice vlan 40",
            "switchport mode access",
            "interface GigabitEthernet0/2",
            "switchport mode trunk",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan 10-20,40",
            "switchport trunk pruning vlan 12-15,20",
            "interface GigabitEthernet1/0/1",
            "switchport voice vlan 22",
            "switchport mode access",
            "switchport private-vlan association host 2000 2500",
            "switchport app-interface",
            "switchport nonegotiate",
            "switchport vepa enabled",
            "switchport protected",
            "switchport block multicast",
            "switchport block unicast",
            "spanning-tree cost 22",
            "spanning-tree guard root",
            "spanning-tree link-type point-to-point",
            "interface GigabitEthernet1/0/2",
            "switchport private-vlan association mapping 2000 xyz",
            "interface GigabitEthernet1/0/3",
            "switchport private-vlan host-association 2000 2500",
            "interface GigabitEthernet1/0/4",
            "switchport private-vlan mapping 2000 add xyz",
            "interface GigabitEthernet1/0/5",
            "switchport private-vlan mapping 2000 remove xyz",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(result["rendered"], commands)

    def test_ios_l2_interfaces_merged_mode_change(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="trunk",
                        name="TwoGigabitEthernet1/0/1",
                    ),
                ],
                state="merged",
            ),
        )
        commands = ["interface TwoGigabitEthernet1/0/1", "switchport mode trunk"]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_fiveGibBit(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             switchport mode access
             switchport access vlan 10
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            interface TwoGigabitEthernet1/0/1
             switchport mode access
             switchport access vlan 20
            interface GigabitEthernet0/3
             switchport trunk allowed vlan 11,59,67,75,77,81,100,400-408,411-413,415,418
             switchport trunk allowed vlan add 461,674,675,696,931,935,951,952,973,974,979
             switchport trunk allowed vlan add 982,986,988,993
             switchport trunk encapsulation dot1q
             switchport trunk pruning vlan 10-15
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="trunk",
                        name="FiveGigabitEthernet1/0/1",
                    ),
                    dict(
                        access=dict(vlan_name="vlan12"),
                        mode="trunk",
                        name="FiveGigabitEthernet1/0/2",
                    ),
                    dict(
                        voice=dict(vlan_tag="dot1p"),
                        mode="trunk",
                        name="FiveGigabitEthernet1/0/3",
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface FiveGigabitEthernet1/0/3",
            "switchport voice vlan dot1p",
            "switchport mode trunk",
            "interface FiveGigabitEthernet1/0/1",
            "switchport access vlan 20",
            "switchport mode trunk",
            "interface FiveGigabitEthernet1/0/2",
            "switchport access vlan name vlan12",
            "switchport mode trunk",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l2_interfaces_trunk_multiline_merge(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60-70"] + [str(vlan) for vlan in range(101, 500, 2)],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10", "20", "30-40"],
                        ),
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan add 60-70,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,"
            + "149,151,153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205",
            "switchport trunk allowed vlan add 207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,247,249,251,253,255,257,"
            + "259,261,263,265,267,269,271,273,275,277,279,281,283,285,287,289,291,293,295,297,299,301,303,305,307,309,311,313,315",
            "switchport trunk allowed vlan add 317,319,321,323,325,327,329,331,333,335,337,339,341,343,345,347,349,351,353,355,357,359,361,363,365,367,"
            + "369,371,373,375,377,379,381,383,385,387,389,391,393,395,397,399,401,403,405,407,409,411,413,415,417,419,421,423,425",
            "switchport trunk allowed vlan add 427,429,431,433,435,437,439,441,443,445,447,449,451,453,455,457,459,461,463,465,467,469,471,473,475,477,"
            + "479,481,483,485,487,489,491,493,495,497,499",
            "switchport trunk pruning vlan add 30-40",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_trunk_multiline_replace(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60-70"] + [str(vlan) for vlan in range(101, 500, 2)],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10", "20", "30-40"],
                        ),
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan remove 10-20,40",
            "switchport trunk allowed vlan add 60-70,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,"
            + "149,151,153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205",
            "switchport trunk allowed vlan add 207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,247,249,251,253,255,257,"
            + "259,261,263,265,267,269,271,273,275,277,279,281,283,285,287,289,291,293,295,297,299,301,303,305,307,309,311,313,315",
            "switchport trunk allowed vlan add 317,319,321,323,325,327,329,331,333,335,337,339,341,343,345,347,349,351,353,355,357,359,361,363,365,367,"
            + "369,371,373,375,377,379,381,383,385,387,389,391,393,395,397,399,401,403,405,407,409,411,413,415,417,419,421,423,425",
            "switchport trunk allowed vlan add 427,429,431,433,435,437,439,441,443,445,447,449,451,453,455,457,459,461,463,465,467,469,471,473,475,477,"
            + "479,481,483,485,487,489,491,493,495,497,499",
            "switchport trunk pruning vlan add 30-40",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_trunk_multiline_replace_init(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60-70"] + [str(vlan) for vlan in range(101, 500, 2)],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10", "20", "30-40"],
                        ),
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan 60-70,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,149,151,153,"
            + "155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205",
            "switchport trunk allowed vlan add 207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,247,249,251,253,255,257,259,"
            + "261,263,265,267,269,271,273,275,277,279,281,283,285,287,289,291,293,295,297,299,301,303,305,307,309,311,313,315",
            "switchport trunk allowed vlan add 317,319,321,323,325,327,329,331,333,335,337,339,341,343,345,347,349,351,353,355,357,359,361,363,365,367,369,"
            + "371,373,375,377,379,381,383,385,387,389,391,393,395,397,399,401,403,405,407,409,411,413,415,417,419,421,423,425",
            "switchport trunk allowed vlan add 427,429,431,433,435,437,439,441,443,445,447,449,451,453,455,457,459,461,463,465,467,469,471,473,475,477,479,"
            + "481,483,485,487,489,491,493,495,497,499",
            "switchport trunk pruning vlan add 30-40",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_trunk_multiline_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             switchport trunk allowed vlan 10-20,40
             switchport trunk encapsulation dot1q
             switchport trunk native vlan 10
             switchport trunk pruning vlan 10,20
             switchport mode trunk
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60-70"] + [str(vlan) for vlan in range(101, 500, 2)],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10", "20", "30-40"],
                        ),
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan remove 10-20,40",
            "switchport trunk allowed vlan add 60-70,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,149,151,"
            + "153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205",
            "switchport trunk allowed vlan add 207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,247,249,251,253,255,257,259,"
            + "261,263,265,267,269,271,273,275,277,279,281,283,285,287,289,291,293,295,297,299,301,303,305,307,309,311,313,315",
            "switchport trunk allowed vlan add 317,319,321,323,325,327,329,331,333,335,337,339,341,343,345,347,349,351,353,355,357,359,361,363,365,367,369,"
            + "371,373,375,377,379,381,383,385,387,389,391,393,395,397,399,401,403,405,407,409,411,413,415,417,419,421,423,425",
            "switchport trunk allowed vlan add 427,429,431,433,435,437,439,441,443,445,447,449,451,453,455,457,459,461,463,465,467,469,471,473,475,477,479,"
            + "481,483,485,487,489,491,493,495,497,499",
            "switchport trunk pruning vlan add 30-40",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(result["commands"], commands)
