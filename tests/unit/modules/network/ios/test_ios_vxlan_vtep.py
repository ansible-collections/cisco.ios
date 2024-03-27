#
# (c) 2023, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vxlan_vtep
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosVxlanVtepModule(TestIosModule):
    module = ios_vxlan_vtep

    def setUp(self):
        super(TestIosVxlanVtepModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vxlan_vtep.vxlan_vtep."
            "Vxlan_vtepFacts.get_vxlan_vtep_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosVxlanVtepModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_vxlan_vtep_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback1
             host-reachability protocol bgp
             member vni 10101 mcast-group 225.0.0.101
             member vni 10102 ingress-replication
             member vni 50901 vrf green
             member vni 10201 mcast-group 225.0.0.101
             member vni 10202 ingress-replication
             member vni 50902 vrf blue
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {"type": "ingress"},
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv4": "225.0.0.101",
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                ],
                                "l3vni": [
                                    {
                                        "vni": "50901",
                                        "vrf": "blue",
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "interface nve1",
            "source-interface Loopback2",
            "no member vni 10101 mcast-group 225.0.0.101",
            "member vni 10101 ingress-replication",
            "no member vni 10201 mcast-group 225.0.0.101",
            "member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
            "no member vni 50901 vrf green",
            "no member vni 50902 vrf blue",
            "member vni 50901 vrf blue",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_vxlan_vtep_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback2
             host-reachability protocol bgp
             member vni 10101 ingress-replication
             member vni 10102 ingress-replication
             member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
             member vni 10202 ingress-replication
             member vni 50901 vrf blue
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {"type": "ingress"},
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv4": "225.0.0.101",
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                ],
                                "l3vni": [
                                    {
                                        "vni": "50901",
                                        "vrf": "blue",
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vxlan_vtep_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback2
             host-reachability protocol bgp
             member vni 10101 ingress-replication
             member vni 10102 ingress-replication
             member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
             member vni 10202 ingress-replication
             member vni 50901 vrf blue
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "host_reachability_bgp": True,
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::102",
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface nve1",
            "no member vni 10101 ingress-replication",
            "member vni 10101 mcast-group FF0E:225::101",
            "no member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
            "member vni 10201 mcast-group FF0E:225::102",
            "no member vni 10102 ingress-replication",
            "no member vni 10202 ingress-replication",
            "no member vni 50901 vrf blue",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_vxlan_vtep_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback2
             host-reachability protocol bgp
             member vni 10101 mcast-group FF0E:225::101
             member vni 10201 mcast-group FF0E:225::102
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "host_reachability_bgp": True,
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::102",
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vxlan_vtep_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
        interface nve1
         no ip address
         source-interface Loopback2
         host-reachability protocol bgp
         member vni 10102 ingress-replication
         member vni 10202 ingress-replication
         member vni 10101 ingress-replication
         member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
         member vni 50901 vrf blue
        """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "host_reachability_bgp": True,
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::102",
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface nve1",
            "no member vni 10101 ingress-replication",
            "member vni 10101 mcast-group FF0E:225::101",
            "no member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
            "member vni 10201 mcast-group FF0E:225::102",
            "no member vni 10102 ingress-replication",
            "no member vni 10202 ingress-replication",
            "no member vni 50901 vrf blue",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_vxlan_vtep_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
        interface nve1
         no ip address
         source-interface Loopback2
         host-reachability protocol bgp
         member vni 10101 mcast-group FF0E:225::101
         member vni 10201 mcast-group FF0E:225::102
        """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "source_interface": "Loopback2",
                        "host_reachability_bgp": True,
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {
                                        "vni": "10101",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::101",
                                            },
                                        },
                                    },
                                    {
                                        "vni": "10201",
                                        "replication": {
                                            "type": "static",
                                            "mcast_group": {
                                                "ipv6": "FF0E:225::102",
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    },
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vxlan_vtep_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback2
             host-reachability protocol bgp
             member vni 10101 mcast-group FF0E:225::101
             member vni 10201 mcast-group FF0E:225::102
            """,
        )
        set_module_args(dict(config=[dict(interface="nve1")], state="deleted"))
        commands = [
            "interface nve1",
            "no source-interface Loopback2",
            "no host-reachability protocol bgp",
            "no member vni 10101 mcast-group FF0E:225::101",
            "no member vni 10201 mcast-group FF0E:225::102",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_vxlan_vtep_deleted_member_vni(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface nve1
             no ip address
             source-interface Loopback2
             host-reachability protocol bgp
             member vni 10101 mcast-group FF0E:225::101
             member vni 10201 mcast-group FF0E:225::102
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "interface": "nve1",
                        "member": {
                            "vni": {
                                "l2vni": [
                                    {"vni": "10101"},
                                    {"vni": "10201"},
                                ],
                            },
                        },
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "interface nve1",
            "no member vni 10101 mcast-group FF0E:225::101",
            "no member vni 10201 mcast-group FF0E:225::102",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
