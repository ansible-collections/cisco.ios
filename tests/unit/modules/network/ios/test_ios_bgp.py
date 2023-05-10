#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.cli.config.bgp.process import (
    Provider,
)
from ansible_collections.cisco.ios.plugins.modules import ios_bgp

from .ios_module import TestIosModule, load_fixture


class TestIosBgpModule(TestIosModule):
    module = ios_bgp

    def setUp(self):
        super().setUp()
        self._bgp_config = load_fixture("ios_bgp_config.cfg")

    def test_ios_bgp(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "router_id": "192.0.2.2",
                    "networks": None,
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == ["router bgp 64496", "bgp router-id 192.0.2.2", "exit"]

    def test_ios_bgp_idempotent(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "router_id": "192.0.2.1",
                    "networks": None,
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_remove(self):
        obj = Provider(
            params={
                "config": {"bgp_as": 64496, "networks": None, "address_family": None},
                "operation": "delete",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == ["no router bgp 64496"]

    def test_ios_bgp_neighbor(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "neighbors": [{"neighbor": "192.51.100.2", "remote_as": 64496}],
                    "networks": None,
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == ["router bgp 64496", "neighbor 192.51.100.2 remote-as 64496", "exit"]

    def test_ios_bgp_neighbor_idempotent(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "neighbors": [
                        {
                            "neighbor": "192.51.100.1",
                            "remote_as": 64496,
                            "timers": {"keepalive": 120, "holdtime": 360, "min_neighbor_holdtime": 360},
                        },
                    ],
                    "networks": None,
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_network(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "networks": [{"prefix": "192.0.1.0", "masklen": 23, "route_map": "RMAP_1"}],
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert sorted(commands) == sorted(["router bgp 64496", "network 192.0.1.0 mask 255.255.254.0 route-map RMAP_1", "exit"])

    def test_ios_bgp_network_idempotent(self):
        obj = Provider(
            params={
                "config": {
                    "bgp_as": 64496,
                    "networks": [
                        {"prefix": "192.0.2.0", "masklen": 23, "route_map": "RMAP_1"},
                        {"prefix": "198.51.100.0", "masklen": 25, "route_map": "RMAP_2"},
                    ],
                    "address_family": None,
                },
                "operation": "merge",
            },
        )
        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_address_family_redistribute(self):
        rd_1 = {"protocol": "ospf", "id": "233", "metric": 90, "route_map": None}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "unicast", "redistribute": [rd_1]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        cmd = [
            "router bgp 64496",
            "address-family ipv4",
            "redistribute ospf 233 metric 90",
            "exit-address-family",
            "exit",
        ]
        assert sorted(commands) == sorted(cmd)

    def test_ios_bgp_address_family_redistribute_idempotent(self):
        rd_1 = {"protocol": "eigrp", "metric": 10, "route_map": "RMAP_3", "id": None}
        rd_2 = {"protocol": "static", "metric": 100, "id": None, "route_map": None}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "unicast", "redistribute": [rd_1, rd_2]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_address_family_neighbors(self):
        af_nbr_1 = {"neighbor": "192.51.100.1", "maximum_prefix": 35, "activate": True}
        af_nbr_2 = {"neighbor": "192.51.100.3", "route_reflector_client": True, "activate": True}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "multicast", "neighbors": [af_nbr_1, af_nbr_2]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        cmd = [
            "router bgp 64496",
            "address-family ipv4 multicast",
            "neighbor 192.51.100.1 activate",
            "neighbor 192.51.100.1 maximum-prefix 35",
            "neighbor 192.51.100.3 activate",
            "neighbor 192.51.100.3 route-reflector-client",
            "exit-address-family",
            "exit",
        ]
        assert sorted(commands) == sorted(cmd)

    def test_ios_bgp_address_family_neighbors_idempotent(self):
        af_nbr_1 = {"neighbor": "203.0.113.1", "remove_private_as": True, "maximum_prefix": 100}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "unicast", "neighbors": [af_nbr_1]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_address_family_networks(self):
        net = {"prefix": "1.0.0.0", "masklen": 8, "route_map": "RMAP_1"}
        net2 = {"prefix": "192.168.1.0", "masklen": 24, "route_map": "RMAP_2"}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "multicast", "networks": [net, net2]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        cmd = [
            "router bgp 64496",
            "address-family ipv4 multicast",
            "network 1.0.0.0 mask 255.0.0.0 route-map RMAP_1",
            "network 192.168.1.0 mask 255.255.255.0 route-map RMAP_2",
            "exit-address-family",
            "exit",
        ]
        assert sorted(commands) == sorted(cmd)

    def test_ios_bgp_address_family_networks_idempotent(self):
        net = {"prefix": "203.0.113.0", "masklen": 27, "route_map": "RMAP_1"}
        net2 = {"prefix": "192.0.2.0", "masklen": 26, "route_map": "RMAP_2"}

        config = {
            "bgp_as": 64496,
            "address_family": [{"afi": "ipv4", "safi": "multicast", "networks": [net, net2]}],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "merge"})

        commands = obj.render(self._bgp_config)
        assert commands == []

    def test_ios_bgp_operation_override(self):
        net_1 = {"prefix": "1.0.0.0", "masklen": 8, "route_map": "RMAP_1"}
        net_2 = {"prefix": "192.168.1.0", "masklen": 24, "route_map": "RMAP_2"}
        nbr_1 = {"neighbor": "192.51.100.1", "remote_as": 64496, "update_source": "GigabitEthernet0/1"}
        nbr_2 = {
            "neighbor": "192.51.100.3",
            "remote_as": 64496,
            "timers": {"keepalive": 300, "holdtime": 360, "min_neighbor_holdtime": 360},
        }
        af_nbr_1 = {"neighbor": "192.51.100.1", "maximum_prefix": 35}
        af_nbr_2 = {"neighbor": "192.51.100.3", "route_reflector_client": True}

        af_1 = {"afi": "ipv4", "safi": "unicast", "neighbors": [af_nbr_1, af_nbr_2]}
        af_2 = {"afi": "ipv4", "safi": "multicast", "networks": [net_1, net_2]}
        config = {
            "bgp_as": 64496,
            "neighbors": [nbr_1, nbr_2],
            "address_family": [af_1, af_2],
            "networks": None,
        }

        obj = Provider(params={"config": config, "operation": "override"})
        commands = obj.render(self._bgp_config)

        cmd = [
            "no router bgp 64496",
            "router bgp 64496",
            "neighbor 192.51.100.1 remote-as 64496",
            "neighbor 192.51.100.1 update-source GigabitEthernet0/1",
            "neighbor 192.51.100.3 remote-as 64496",
            "neighbor 192.51.100.3 timers 300 360 360",
            "address-family ipv4",
            "neighbor 192.51.100.1 maximum-prefix 35",
            "neighbor 192.51.100.3 route-reflector-client",
            "exit-address-family",
            "address-family ipv4 multicast",
            "network 1.0.0.0 mask 255.0.0.0 route-map RMAP_1",
            "network 192.168.1.0 mask 255.255.255.0 route-map RMAP_2",
            "exit-address-family",
            "exit",
        ]

        assert sorted(commands) == sorted(cmd)

    def test_ios_bgp_operation_replace(self):
        rd = {"protocol": "ospf", "id": 223, "metric": 110, "route_map": None}
        net = {"prefix": "203.0.113.0", "masklen": 27, "route_map": "RMAP_1"}
        net2 = {"prefix": "192.0.2.0", "masklen": 26, "route_map": "RMAP_2"}

        af_1 = {"afi": "ipv4", "safi": "unicast", "redistribute": [rd]}
        af_2 = {"afi": "ipv4", "safi": "multicast", "networks": [net, net2]}

        config = {"bgp_as": 64496, "address_family": [af_1, af_2], "networks": None}
        obj = Provider(params={"config": config, "operation": "replace"})
        commands = obj.render(self._bgp_config)

        cmd = [
            "router bgp 64496",
            "address-family ipv4",
            "redistribute ospf 223 metric 110",
            "no redistribute eigrp",
            "no redistribute static",
            "exit-address-family",
            "exit",
        ]

        assert sorted(commands) == sorted(cmd)

    def test_ios_bgp_operation_replace_with_new_as(self):
        rd = {"protocol": "ospf", "id": 223, "metric": 110, "route_map": None}

        af_1 = {"afi": "ipv4", "safi": "unicast", "redistribute": [rd]}

        config = {"bgp_as": 64497, "address_family": [af_1], "networks": None}
        obj = Provider(params={"config": config, "operation": "replace"})
        commands = obj.render(self._bgp_config)

        cmd = [
            "no router bgp 64496",
            "router bgp 64497",
            "address-family ipv4",
            "redistribute ospf 223 metric 110",
            "exit-address-family",
            "exit",
        ]

        assert sorted(commands) == sorted(cmd)
