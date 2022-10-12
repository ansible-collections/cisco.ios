#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_static_routes
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosStaticRoutesModule(TestIosModule):
    module = ios_static_routes

    def setUp(self):
        super(TestIosStaticRoutesModule, self).setUp()

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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.static_routes.static_routes."
            "Static_RoutesFacts.get_static_routes_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosStaticRoutesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    # def load_fixtures(self, commands=None, transport="cli"):
    #     # def load_from_file(*args, **kwargs):
    #     #     return load_fixture("ios_static_routes_config.cfg")

    #     # self.execute_show_command.side_effect = load_from_file
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         ip route vrf ansible_vrf 0.0.0.0 0.0.0.0 198.51.101.1 name test_vrf_1 track 150 tag 100
    #         ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf_2 track 175 tag 50
    #         ip route vrf ansible_vrf 192.51.110.0 255.255.255.255 GigabitEthernet0/2 192.51.111.1 10 name partner
    #         ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 60
    #         ipv6 route 2001:DB8:0:3::/64 GigabitEthernet0/2 2001:DB8:0:3::2 tag 105 name test_v6
    #         """
    #     )

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
            "ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf track 150 tag 50",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 40",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route vrf ansible_vrf 0.0.0.0 0.0.0.0 198.51.101.1 name test_vrf_1 track 150 tag 100
            ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf_2 track 175 tag 50
            ip route vrf ansible_vrf 192.51.110.0 255.255.255.255 GigabitEthernet0/2 192.51.111.1 10 name partner
            ip route vrf ansible_vrf_2 192.51.111.0 255.255.255.255 GigabitEthernet0/1
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
                                        dest="0.0.0.0/0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="test_vrf_1",
                                                tag=100,
                                                track=150,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf_2",
                                                tag=50,
                                                track=175,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.51.110.0/32",
                                        next_hops=[
                                            dict(
                                                distance_metric=10,
                                                forward_router_address="192.51.111.1",
                                                interface="GigabitEthernet0/2",
                                                name="partner",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf_2",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.51.111.0/32",
                                        next_hops=[
                                            dict(
                                                interface="GigabitEthernet0/1",
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
                                        dest="198.51.100.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="route_1",
                                                distance_metric=110,
                                                tag=60,
                                                multicast=True,
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
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:3::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:3::2",
                                                interface="GigabitEthernet0/2",
                                                name="test_v6",
                                                tag=105,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:4::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:4::2",
                                                name="test_v6_vrf",
                                                tag=115,
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
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_static_routes_replaced(self):
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
                                                name="replaced_vrf",
                                                tag=10,
                                                track=170,
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
                                                name="replaced_route_1",
                                                distance_metric=110,
                                                tag=60,
                                                multicast=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name replaced_vrf track 170 tag 10",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name replaced_route_1 tag 60",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_replaced_idempotent(self):
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
                                        dest="0.0.0.0/0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="test_vrf_1",
                                                tag=100,
                                                track=150,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf_2",
                                                tag=50,
                                                track=175,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.51.110.0/32",
                                        next_hops=[
                                            dict(
                                                distance_metric=10,
                                                forward_router_address="192.51.111.1",
                                                interface="GigabitEthernet0/2",
                                                name="partner",
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
                                        dest="198.51.100.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="route_1",
                                                distance_metric=110,
                                                tag=60,
                                                multicast=True,
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
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:3::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:3::2",
                                                interface="GigabitEthernet0/2",
                                                name="test_v6",
                                                tag=105,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:4::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:4::2",
                                                name="test_v6_vrf",
                                                tag=115,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_static_routes_overridden(self):
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
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="198.51.100.0 255.255.255.0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="override_route_1",
                                                distance_metric=150,
                                                tag=50,
                                                multicast=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 60",
            "no ip route vrf ansible_vrf 0.0.0.0 0.0.0.0 198.51.101.1 name test_vrf_1 track 150 tag 100",
            "no ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf_2 track 175 tag 50",
            "no ip route vrf ansible_vrf 192.51.110.0 255.255.255.255 GigabitEthernet0/2 192.51.111.1 10 name partner",
            "no ipv6 route 2001:DB8:0:3::/64 GigabitEthernet0/2 2001:DB8:0:3::2 name test_v6 tag 105",
            "no ipv6 route vrf ansible_vrf 2001:DB8:0:4::/64 2001:DB8:0:4::2 name test_v6_vrf tag 115",
            "ip route 198.51.100.0 255.255.255.0 198.51.101.1 150 multicast name override_route_1 tag 50",
        ]

        self.assertEqual(result["commands"], commands)

    def test_ios_static_routes_overridden_idempotent(self):
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
                                        dest="0.0.0.0/0",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="test_vrf_1",
                                                tag=100,
                                                track=150,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf_2",
                                                tag=50,
                                                track=175,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.51.110.0/32",
                                        next_hops=[
                                            dict(
                                                distance_metric=10,
                                                forward_router_address="192.51.111.1",
                                                interface="GigabitEthernet0/2",
                                                name="partner",
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
                                        dest="198.51.100.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="route_1",
                                                distance_metric=110,
                                                tag=60,
                                                multicast=True,
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
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:3::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:3::2",
                                                interface="GigabitEthernet0/2",
                                                name="test_v6",
                                                tag=105,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        vrf="ansible_vrf",
                        address_families=[
                            dict(
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:DB8:0:4::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:DB8:0:4::2",
                                                name="test_v6_vrf",
                                                tag=115,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_delete_static_route_config(self):
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
                                        dest="192.0.2.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf",
                                                tag=50,
                                                track=175,
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
                                        dest="198.51.100.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="198.51.101.1",
                                                name="route_1",
                                                distance_metric=110,
                                                tag=60,
                                                multicast=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf track 175 tag 50",
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 60",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_dest_based(self):
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
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[dict(dest="198.51.100.0/24")],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 multicast name route_1 tag 60",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_static_route_vrf_based(self):
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
                                routes=[dict(dest="192.0.2.0/24")],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf_2 track 175 tag 50",
        ]
        self.assertEqual(result["commands"], commands)

    def test_static_route_rendered(self):
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
                                        dest="192.0.2.0/24",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.1",
                                                name="test_vrf",
                                                tag=50,
                                                track=175,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "ip route vrf ansible_vrf 192.0.2.0 255.255.255.0 192.0.2.1 name test_vrf track 175 tag 50",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)

    def test_static_route_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 10.0.0.0 255.0.0.0 Null0 permanent
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
                                    {"interface": "Null0", "permanent": True},
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
        # self.assertEqual(result["gathered"], gathered)
