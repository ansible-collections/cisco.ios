#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_static_routes
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosStaticRoutesModule(TestIosModule):
    module = ios_static_routes

    def setUp(self):
        super(TestIosStaticRoutesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.static_routes.static_routes."
            "Static_routesFacts.get_static_routes_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosStaticRoutesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_static_routes_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf ansible_vrf 0.0.0.0 0.0.0.0 198.51.101.1 name test_vrf_1 track 150 tag 100
            ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf_2 track 175 tag 50
            ip route vrf ansible_vrf 192.51.110.0 255.255.255.255 GigabitEthernet0/2 192.51.111.1 10 name partner
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 60
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet0/2 2001:DB8:0:3::2 tag 105 name test_v6
            ipv6 route vrf ansible_vrf 2001:DB8:0:4::/64 2001:DB8:0:4::2 tag 115 name test_v6_vrf
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.0 255.255.255.0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf",
                                                tag=50,
                                                track=150,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="198.51.100.0 255.255.255.0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="route_1",
                                                distance_metric=110,
                                                tag=40,
                                                multicast=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast",
            "ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.0/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        commands = []
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.1/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:4::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.1/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip route 198.51.100.1 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.3 name merged_route_3",
            "ip route 198.51.100.1 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet4 multicast permanent name onlyname",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "ipv6 route 2001:DB8:0:4::/64 Null0",
            "ipv6 route 2001:DB8:0:4::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "ipv6 route 2001:DB8:0:4::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "ip route vrf testVrf2 192.168.1.1 255.255.255.0 10.1.1.2 track 10",
            "ip route vrf testVrf2 192.168.1.1 255.255.255.0 10.1.1.3 22 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.0/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        commands = []
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.1/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:4::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.1/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip route 198.51.100.1 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.1 255.255.255.0 198.51.101.3 name merged_route_3",
            "ip route 198.51.100.1 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet4 multicast permanent name onlyname",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "ipv6 route 2001:DB8:0:4::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "ipv6 route 2001:DB8:0:4::/64 Null0",
            "ipv6 route 2001:DB8:0:4::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "ipv6 route 2001:DB8:0:4::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "ip route vrf testVrf2 192.168.1.1 255.255.255.0 10.1.1.2 track 10",
            "ip route vrf testVrf2 192.168.1.1 255.255.255.0 10.1.1.3 22 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.0/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=False)
        commands = []
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_config_del_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.0/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10",
            "no ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_config_empty_del_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10",
            "no ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10",
            "no ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150",
            "no ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_config(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_config_second_check(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {"interface": "Null0"},
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_dest_based(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "dest": "198.51.100.0/24",
                                    },
                                    {
                                        "dest": "198.51.100.2/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "no ipv6 route 2001:DB8:0:3::/64 Null0",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_dest_based_second_check(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route 198.51.100.1 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.1 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "dest": "198.51.100.0/24",
                                    },
                                    {
                                        "dest": "198.51.100.1/24",
                                    },
                                    {
                                        "dest": "198.51.100.2/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "no ip route 198.51.100.1 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "no ip route 198.51.100.1 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_vrf_based(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
            ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route 198.51.100.1 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
            ip route 198.51.100.1 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
            ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
            ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
            ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
            ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
            ipv6 route 2001:DB8:0:3::/64 Null0
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            ipv6 route vrf testVrfv6 2001:DB8:0:4::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
            ipv6 route vrf testVrfv6 2001:DB8:0:4::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="testVrf2",
                        address_families=[
                            dict(afi="ipv4", routes=[dict(dest="192.0.2.0/24")]),
                        ],
                    ),
                    dict(
                        vrf="testVrfv6",
                        address_families=[
                            dict(afi="ipv6", routes=[dict(dest="2001:DB8:0:4::/64")]),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "no ipv6 route vrf testVrfv6 2001:DB8:0:4::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "no ipv6 route vrf testVrfv6 2001:DB8:0:4::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_route_rendered(self):
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.12",
                                                "distance_metric": 34,
                                                "tag": 22,
                                                "name": "nm12",
                                                "track": 11,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.1",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "forward_router_address": "198.51.101.11",
                                                "distance_metric": 22,
                                                "tag": 22,
                                                "permanent": True,
                                                "name": "nm1",
                                                "multicast": True,
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "GigabitEthernet4",
                                                "permanent": True,
                                                "name": "onlyname",
                                                "multicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet3",
                                                "tag": 11,
                                                "permanent": True,
                                                "name": "qq",
                                                "unicast": True,
                                            },
                                            {
                                                "interface": "GigabitEthernet2",
                                                "tag": 2,
                                                "permanent": True,
                                                "name": "nm1",
                                            },
                                            {"interface": "Null0"},
                                            {
                                                "forward_router_address": "2001:DB8:0:3::3",
                                                "distance_metric": 22,
                                                "permanent": True,
                                                "name": "pp1",
                                                "multicast": True,
                                            },
                                            {
                                                "forward_router_address": "2001:DB8:0:3::2",
                                                "tag": 22,
                                                "name": "name1",
                                                "track": 22,
                                            },
                                        ],
                                        "dest": "2001:DB8:0:3::/64",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.1.1.2",
                                                "track": 10,
                                            },
                                            {
                                                "forward_router_address": "10.1.1.3",
                                                "distance_metric": 22,
                                                "track": 10,
                                            },
                                        ],
                                        "dest": "192.168.1.0/24",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "testVrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.3",
                                                "tag": 30,
                                                "name": "test_vrf2",
                                                "track": 120,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.1",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.2",
                                                "tag": 50,
                                                "name": "test_vrf",
                                                "track": 150,
                                            },
                                        ],
                                        "dest": "192.0.2.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast",
            "ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname",
            "ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq",
            "ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1",
            "ipv6 route 2001:DB8:0:3::/64 Null0",
            "ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1",
            "ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1",
            "ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10",
            "ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10",
            "ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120",
            "ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150",
            "ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_static_routes_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.2 track 10
                    ip route vrf testVrf2 192.168.1.0 255.255.255.0 10.1.1.3 22 track 10
                    ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
                    ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
                    ip route vrf testVrf2 192.0.2.0 255.255.255.0 192.0.2.3 tag 30 name test_vrf2 track 120
                    ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
                    ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
                    ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
                    ip route vrf testVrf 192.0.2.0 255.255.255.0 192.0.2.2 tag 50 name test_vrf track 150
                    ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
                    ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
                    ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
                    ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
                    ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
                    ipv6 route 2001:DB8:0:3::/64 Null0
                    ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
                    ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "interface": "GigabitEthernet2",
                                        "forward_router_address": "198.51.101.12",
                                        "distance_metric": 34,
                                        "tag": 22,
                                        "name": "nm12",
                                        "track": 11,
                                    },
                                    {
                                        "forward_router_address": "198.51.101.1",
                                        "distance_metric": 175,
                                        "tag": 70,
                                        "name": "replaced_route",
                                        "track": 150,
                                    },
                                    {
                                        "forward_router_address": "198.51.101.20",
                                        "distance_metric": 175,
                                        "tag": 70,
                                        "name": "replaced_route",
                                        "track": 150,
                                    },
                                    {
                                        "forward_router_address": "198.51.101.3",
                                        "name": "merged_route_3",
                                    },
                                    {
                                        "interface": "GigabitEthernet2",
                                        "forward_router_address": "198.51.101.11",
                                        "distance_metric": 22,
                                        "tag": 22,
                                        "permanent": True,
                                        "name": "nm1",
                                        "multicast": True,
                                    },
                                ],
                                "dest": "198.51.100.0/24",
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "interface": "GigabitEthernet4",
                                        "permanent": True,
                                        "name": "onlyname",
                                        "multicast": True,
                                    },
                                    {
                                        "interface": "GigabitEthernet3",
                                        "tag": 11,
                                        "permanent": True,
                                        "name": "qq",
                                        "unicast": True,
                                    },
                                    {
                                        "interface": "GigabitEthernet2",
                                        "tag": 2,
                                        "permanent": True,
                                        "name": "nm1",
                                    },
                                    {"interface": "Null0"},
                                    {
                                        "forward_router_address": "2001:DB8:0:3::3",
                                        "distance_metric": 22,
                                        "permanent": True,
                                        "name": "pp1",
                                        "multicast": True,
                                    },
                                    {
                                        "forward_router_address": "2001:DB8:0:3::2",
                                        "tag": 22,
                                        "name": "name1",
                                        "track": 22,
                                    },
                                ],
                                "dest": "2001:DB8:0:3::/64",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "testVrf2",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "10.1.1.2", "track": 10},
                                    {
                                        "forward_router_address": "10.1.1.3",
                                        "distance_metric": 22,
                                        "track": 10,
                                    },
                                ],
                                "dest": "192.168.1.0/24",
                            },
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "192.0.2.3",
                                        "tag": 30,
                                        "name": "test_vrf2",
                                        "track": 120,
                                    },
                                ],
                                "dest": "192.0.2.0/24",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "testVrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "192.0.2.3",
                                        "tag": 30,
                                        "name": "test_vrf2",
                                        "track": 120,
                                    },
                                    {
                                        "forward_router_address": "192.0.2.1",
                                        "tag": 50,
                                        "name": "test_vrf",
                                        "track": 150,
                                    },
                                    {
                                        "forward_router_address": "192.0.2.2",
                                        "tag": 50,
                                        "name": "test_vrf",
                                        "track": 150,
                                    },
                                ],
                                "dest": "192.0.2.0/24",
                            },
                        ],
                    },
                ],
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_ios_static_route_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 10.0.0.0 255.0.0.0 Null0 permanent
            ip route 192.168.1.0 255.255.255.0 GigabitEthernet0/1.22 10.0.0.1 tag 30
            ip route 192.168.1.0 255.255.255.0 10.0.0.2
            ip route 192.168.1.0 255.255.255.248 GigabitEthernet0/1.23 10.0.0.3 tag 30
            ipv6 route 2001:DB8:0:3::/128 2001:DB8:0:3::33
            ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "dest": "10.0.0.0/8",
                                "next_hops": [
                                    {
                                        "interface": "Null0",
                                        "permanent": True,
                                    },
                                ],
                            },
                            {
                                "dest": "192.168.1.0/24",
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.0.1",
                                        "interface": "GigabitEthernet0/1.22",
                                        "tag": 30,
                                    },
                                    {
                                        "forward_router_address": "10.0.0.2",
                                    },
                                ],
                            },
                            {
                                "dest": "192.168.1.0/29",
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.0.3",
                                        "interface": "GigabitEthernet0/1.23",
                                        "tag": 30,
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "routes": [
                            {
                                "dest": "2001:DB8:0:3::/128",
                                "next_hops": [
                                    {
                                        "forward_router_address": "2001:DB8:0:3::33",
                                    },
                                ],
                            },
                            {
                                "dest": "2001:DB8:0:3::/64",
                                "next_hops": [
                                    {
                                        "forward_router_address": "2001:DB8:0:3::3",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        print(result["gathered"])
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_static_route_gathered_2(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
            ip route 192.168.1.0 255.255.255.0 GigabitEthernet0/1.22 10.0.0.1 tag 30
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "198.51.101.1",
                                        "distance_metric": 175,
                                        "tag": 70,
                                        "name": "replaced_route",
                                        "multicast": True,
                                    },
                                ],
                                "dest": "198.51.100.0/24",
                            },
                            {
                                "next_hops": [
                                    {
                                        "interface": "GigabitEthernet0/1.22",
                                        "forward_router_address": "10.0.0.1",
                                        "tag": 30,
                                    },
                                ],
                                "dest": "192.168.1.0/24",
                            },
                        ],
                    },
                ],
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_static_route_overridden_2(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
            ip route 192.168.1.0 255.255.255.0 GigabitEthernet0/1.22 10.0.0.1 tag 30
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "198.51.101.20",
                                                "distance_metric": 175,
                                                "tag": 70,
                                                "name": "replaced_route",
                                                "track": 150,
                                            },
                                            {
                                                "forward_router_address": "198.51.101.3",
                                                "name": "merged_route_3",
                                            },
                                        ],
                                        "dest": "198.51.100.0/24",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast",
            "no ip route 192.168.1.0 255.255.255.0 GigabitEthernet0/1.22 10.0.0.1 tag 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
