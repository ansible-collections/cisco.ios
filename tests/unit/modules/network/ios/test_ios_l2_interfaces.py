#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_l2_interfaces
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosL2InterfacesModule(TestIosModule):
    module = ios_l2_interfaces

    def setUp(self):
        super(TestIosL2InterfacesModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2_interfaces.l2_interfaces."
            "L2_interfacesFacts.get_l2_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
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
                    dict(access=dict(vlan=10), mode="access", name="GigabitEthernet0/1"),
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
                    dict(access=dict(vlan=10), mode="access", name="GigabitEthernet0/1"),
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
                    dict(access=dict(vlan=20), mode="access", name="TwoGigabitEthernet1/0/1"),
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
                    dict(access=dict(vlan=10), mode="access", name="GigabitEthernet0/1"),
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
                    dict(access=dict(vlan=20), mode="access", name="TwoGigabitEthernet1/0/1"),
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
                config=[dict(access=dict(vlan=20), mode="trunk", name="TwoGigabitEthernet1/0/1")],
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
                    dict(access=dict(vlan=20), mode="trunk", name="FiveGigabitEthernet1/0/1"),
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
