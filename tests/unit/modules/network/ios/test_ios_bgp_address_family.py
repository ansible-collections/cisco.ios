#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_bgp_address_family
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosBgpAddressFamilyModule(TestIosModule):
    module = ios_bgp_address_family

    def setUp(self):
        super(TestIosBgpAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_address_family.bgp_address_family."
            "Bgp_address_familyFacts.get_bgp_address_family_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBgpAddressFamilyModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_bgp_address_family_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_addresses=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            bgp=dict(
                                dampening=dict(
                                    penalty_half_time=10,
                                    reuse_route_val=10,
                                    suppress_route_val=10,
                                    max_suppress=10,
                                ),
                            ),
                            neighbors=[
                                dict(
                                    neighbor_address="198.51.100.1",
                                    remote_as="65.11",
                                    route_maps=[
                                        dict(name="test-route-out", out="true"),
                                    ],
                                    prefix_lists=[
                                        dict(name="AS65100-PREFIX-OUT", out="true"),
                                    ],
                                ),
                            ],
                        ),
                        dict(
                            afi="nsap",
                            bgp=dict(aggregate_timer=20, dmzlink_bw=True, scan_time=10),
                            default_metric=10,
                            networks=[
                                dict(address="192.0.1.1", route_map="test_route"),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "bgp dampening 10 10 10 10",
            "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
            "address-family nsap",
            "bgp aggregate-timer 20",
            "bgp dmzlink-bw",
            "bgp scan-time 10",
            "neighbor 198.51.100.1 remote-as 65.11",
            "neighbor 198.51.100.1 route-map test-route-out out",
            "network 192.0.1.1 route-map test_route",
            "default-metric 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_merged_2(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="unicast",
                            vrf="blue",
                            neighbor=[
                                dict(
                                    address="192.0.3.1",
                                    remote_as=65001,
                                    soft_reconfiguration=True,
                                    prefix_list=dict(name="PREFIX-OUT", out=True),
                                ),
                            ],
                            network=[dict(address="192.0.3.1", mask="255.255.255.0")],
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 unicast vrf blue",
            "neighbor 192.0.3.1 remote-as 65001",
            "neighbor 192.0.3.1 prefix-list PREFIX-OUT out",
            "neighbor 192.0.3.1 soft-reconfiguration inbound",
            "network 192.0.3.1 mask 255.255.255.0",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
              maximum-secondary-paths eibgp 2
              maximum-paths 12
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 10.64760
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config={
                    "address_family": [
                        {
                            "afi": "ipv4",
                            "bgp": {"redistribute_internal": True},
                            "maximum_paths": {"paths": 12},
                            "maximum_secondary_paths": {"eibgp": 2},
                            "neighbors": [
                                {
                                    "neighbor_address": "TEST-PEER-GROUP",
                                    "nexthop_self": {"all": True},
                                    "send_community": {"set": True},
                                },
                                {"activate": True, "neighbor_address": "2001:db8::1"},
                            ],
                            "redistribute": [{"connected": {"set": True}}],
                        },
                        {
                            "afi": "ipv4",
                            "aggregate_addresses": [
                                {
                                    "address": "192.0.3.1",
                                    "as_confed_set": True,
                                    "netmask": "255.255.255.255",
                                },
                            ],
                            "default_metric": 12,
                            "distance": {"external": 10, "internal": 10, "local": 100},
                            "networks": [
                                {
                                    "address": "198.51.111.11",
                                    "mask": "255.255.255.255",
                                    "route_map": "test",
                                },
                            ],
                            "safi": "multicast",
                            "table_map": {"filter": True, "name": "test_tableMap"},
                        },
                        {
                            "afi": "ipv4",
                            "bgp": {
                                "dampening": {
                                    "max_suppress": 5,
                                    "penalty_half_time": 1,
                                    "reuse_route_val": 10,
                                    "suppress_route_val": 100,
                                },
                                "dmzlink_bw": True,
                                "soft_reconfig_backup": True,
                            },
                            "safi": "mdt",
                        },
                        {
                            "afi": "ipv4",
                            "aggregate_addresses": [
                                {
                                    "address": "192.0.2.1",
                                    "as_confed_set": True,
                                    "netmask": "255.255.255.255",
                                },
                            ],
                            "bgp": {
                                "aggregate_timer": 10,
                                "dampening": {
                                    "max_suppress": 1,
                                    "penalty_half_time": 1,
                                    "reuse_route_val": 1,
                                    "suppress_route_val": 1,
                                },
                                "slow_peer_options": {"detection": {"threshold": 150}},
                            },
                            "neighbors": [
                                {
                                    "activate": True,
                                    "aigp": {
                                        "send": {
                                            "cost_community": {
                                                "id": 100,
                                                "poi": {
                                                    "igp_cost": True,
                                                    "transitive": True,
                                                },
                                            },
                                        },
                                    },
                                    "local_as": {"number": "10.64760", "set": True},
                                    "neighbor_address": "198.51.100.1",
                                    "nexthop_self": {"all": True},
                                    "prefix_lists": [
                                        {"name": "AS65100-PREFIX-OUT", "out": True},
                                    ],
                                    "remote_as": 10,
                                    "route_maps": [{"name": "test-out", "out": True}],
                                    "route_server_client": True,
                                    "slow_peer_options": {
                                        "detection": {"threshold": 150},
                                    },
                                },
                            ],
                            "networks": [
                                {
                                    "address": "198.51.110.10",
                                    "backdoor": True,
                                    "mask": "255.255.255.255",
                                },
                            ],
                            "safi": "multicast",
                            "vrf": "blue",
                        },
                    ],
                    "as_number": "65000",
                },
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_ios_bgp_address_family_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                slow_peer=[dict(detection=dict(threshold=200))],
                            ),
                            redistribute=[dict(connected=dict(metric=10))],
                            neighbor=[
                                dict(
                                    address="198.51.110.1",
                                    activate=True,
                                    remote_as=200,
                                    route_maps=[
                                        dict(name="test-replaced-route", out=True),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "no bgp dampening 1 1 1 1",
            "bgp slow-peer detection threshold 200",
            "redistribute connected metric 10",
            "neighbor 198.51.110.1 activate",
            "neighbor 198.51.110.1 remote-as 200",
            "neighbor 198.51.110.1 route-map test-replaced-route out",
            "no neighbor 198.51.100.1",
            "no network 198.51.110.10 mask 255.255.255.255 backdoor",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                                slow_peer=[dict(detection=dict(threshold=150))],
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            ),
                                        ),
                                    ),
                                    nexthop_self=dict(all=True),
                                    prefix_lists=[
                                        dict(name="AS65100-PREFIX-OUT", out="true"),
                                    ],
                                    slow_peer=[dict(detection=dict(threshold=150))],
                                    remote_as=10,
                                    local_as=dict(number=20),
                                    route_maps=[dict(name="test-out", out=True)],
                                    route_server_client=True,
                                ),
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                ),
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="mdt",
                            bgp=dict(
                                dmzlink_bw=True,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=10,
                                    suppress_route_val=100,
                                    max_suppress=5,
                                ),
                                soft_reconfig_backup=True,
                            ),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                ),
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_address_family_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            bgp=dict(redistribute_internal=True),
                            redistribute=[
                                dict(connected=dict(set=True)),
                                dict(
                                    ospf=dict(
                                        process_id=200,
                                        metric=100,
                                        match=dict(
                                            internal=True,
                                            externals=dict(
                                                type_1=True,
                                                type_2=True,
                                            ),
                                        ),
                                    ),
                                ),
                            ],
                            neighbor=[
                                dict(
                                    tag="TEST-PEER-GROUP",
                                    nexthop_self=dict(all=True),
                                    send_community=dict(set=True),
                                ),
                                dict(ipv6_address="2001:db8::1", activate=True),
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                                slow_peer=[dict(detection=dict(threshold=150))],
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            ),
                                        ),
                                    ),
                                    nexthop_self=dict(all=True),
                                    prefix_lists=[
                                        dict(name="AS65100-PREFIX-OUT", out="true"),
                                    ],
                                    slow_peer=[dict(detection=dict(threshold=150))],
                                    remote_as=10,
                                    local_as=dict(number=20),
                                    route_maps=[dict(name="test-out", out=True)],
                                    route_server_client=True,
                                ),
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                ),
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="mdt",
                            bgp=dict(
                                dmzlink_bw=True,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=10,
                                    suppress_route_val=100,
                                    max_suppress=5,
                                ),
                                soft_reconfig_backup=True,
                            ),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                ),
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="overridden",
            ),
        )

        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_address_family_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(dict(state="deleted"))
        commands = [
            "router bgp 65000",
            "no address-family ipv4",
            "no address-family ipv4 multicast vrf blue",
            "no address-family ipv4 mdt",
            "no address-family ipv4 multicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_delete_without_config(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(afi="ipv4", safi="mdt"),
                    ],
                ),
                state="deleted",
            ),
        )
        commands = [
            "router bgp 65000",
            "no address-family ipv4 mdt",
            "no address-family ipv4 multicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            maximum_paths=dict(paths=12),
                            maximum_secondary_paths=dict(eibgp=2),
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            bgp=dict(
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            ),
                                        ),
                                    ),
                                    slow_peer=[dict(detection=dict(threshold=150))],
                                    remote_as=10,
                                    route_maps=[dict(name="test-route", out=True)],
                                    route_server_client=True,
                                ),
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                ),
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                ),
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                ),
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                            snmp=dict(
                                context=dict(
                                    user=dict(
                                        name="abc",
                                        access=dict(ipv6="ipcal"),
                                        credential=True,
                                        encrypted=True,
                                    ),
                                    name="testsnmp",
                                ),
                            ),
                        ),
                    ],
                ),
                state="rendered",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "bgp dampening 1 1 1 1",
            "maximum-secondary-paths eibgp 2",
            "maximum-paths 12",
            "neighbor 198.51.100.1 remote-as 10",
            "neighbor 198.51.100.1 activate",
            "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
            "neighbor 198.51.100.1 route-map test-route out",
            "neighbor 198.51.100.1 route-server-client",
            "neighbor 198.51.100.1 slow-peer detection threshold 150",
            "network 198.51.110.10 mask 255.255.255.255 backdoor",
            "aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
            "address-family ipv4 multicast",
            "network 198.51.111.11 mask 255.255.255.255 route-map test",
            "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
            "default-metric 12",
            "distance bgp 10 10 100",
            "table-map test_tableMap filter",
            "snmp context testsnmp user abc credential encrypted access ipv6 ipcal",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_bgp_address_family_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65000
                     bgp log-neighbor-changes
                     bgp nopeerup-delay cold-boot 20
                     neighbor TEST-PEER-GROUP peer-group
                     neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
                     neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
                     !
                     address-family ipv4
                      bgp redistribute-internal
                      redistribute connected
                      redistribute ospf 200 metric 100 match internal external 1 external 2
                      neighbor TEST-PEER-GROUP send-community
                      neighbor TEST-PEER-GROUP next-hop-self all
                      neighbor 2001:db8::1 activate
                      maximum-secondary-paths eibgp 2
                      maximum-paths 12
                     !
                     address-family ipv4 multicast
                      table-map test_tableMap filter
                      network 198.51.111.11 mask 255.255.255.255 route-map test
                      aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
                      default-metric 12
                      distance bgp 10 10 100
                     exit-address-family
                     !
                     address-family ipv4 mdt
                      bgp dampening 1 10 100 5
                      bgp dmzlink-bw
                      bgp soft-reconfig-backup
                     exit-address-family
                     !
                     address-family ipv4 multicast vrf blue
                      bgp aggregate-timer 10
                      bgp slow-peer detection threshold 150
                      bgp dampening 1 1 1 1
                      network 198.51.110.10 mask 255.255.255.255 backdoor
                      aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
                      neighbor 198.51.100.1 remote-as 10
                      neighbor 198.51.100.1 local-as 20
                      neighbor 198.51.100.1 activate
                      neighbor 198.51.100.1 next-hop-self all
                      neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
                      neighbor 198.51.100.1 route-server-client
                      neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
                      neighbor 198.51.100.1 slow-peer detection threshold 150
                      neighbor 198.51.100.1 route-map test-out out
                     exit-address-family
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "as_number": "65000",
            "address_family": [
                {
                    "afi": "ipv4",
                    "bgp": {"redistribute_internal": True},
                    "redistribute": [
                        {"connected": {"set": True}},
                        {
                            "ospf": {
                                "process_id": 200,
                                "metric": 100,
                                "match": {
                                    "internal": True,
                                    "externals": {
                                        "type_1": True,
                                        "type_2": True,
                                    },
                                },
                            },
                        },
                    ],
                    "maximum_paths": {"paths": 12},
                    "maximum_secondary_paths": {"eibgp": 2},
                    "neighbors": [
                        {
                            "send_community": {"set": True},
                            "nexthop_self": {"all": True},
                            "neighbor_address": "TEST-PEER-GROUP",
                        },
                        {"neighbor_address": "2001:db8::1", "activate": True},
                    ],
                },
                {
                    "afi": "ipv4",
                    "safi": "multicast",
                    "table_map": {"name": "test_tableMap", "filter": True},
                    "networks": [
                        {
                            "address": "198.51.111.11",
                            "mask": "255.255.255.255",
                            "route_map": "test",
                        },
                    ],
                    "aggregate_addresses": [
                        {
                            "address": "192.0.3.1",
                            "netmask": "255.255.255.255",
                            "as_confed_set": True,
                        },
                    ],
                    "default_metric": 12,
                    "distance": {"external": 10, "internal": 10, "local": 100},
                },
                {
                    "afi": "ipv4",
                    "safi": "mdt",
                    "bgp": {
                        "dampening": {
                            "penalty_half_time": 1,
                            "reuse_route_val": 10,
                            "suppress_route_val": 100,
                            "max_suppress": 5,
                        },
                        "dmzlink_bw": True,
                        "soft_reconfig_backup": True,
                    },
                },
                {
                    "afi": "ipv4",
                    "safi": "multicast",
                    "vrf": "blue",
                    "bgp": {
                        "aggregate_timer": 10,
                        "slow_peer_options": {"detection": {"threshold": 150}},
                        "dampening": {
                            "penalty_half_time": 1,
                            "reuse_route_val": 1,
                            "suppress_route_val": 1,
                            "max_suppress": 1,
                        },
                    },
                    "networks": [
                        {
                            "address": "198.51.110.10",
                            "mask": "255.255.255.255",
                            "backdoor": True,
                        },
                    ],
                    "aggregate_addresses": [
                        {
                            "address": "192.0.2.1",
                            "netmask": "255.255.255.255",
                            "as_confed_set": True,
                        },
                    ],
                    "neighbors": [
                        {
                            "remote_as": "10",
                            "local_as": {"set": True, "number": "20"},
                            "activate": True,
                            "neighbor_address": "198.51.100.1",
                            "nexthop_self": {"all": True},
                            "aigp": {
                                "send": {
                                    "cost_community": {
                                        "id": 100,
                                        "poi": {"igp_cost": True, "transitive": True},
                                    },
                                },
                            },
                            "route_server_client": True,
                            "prefix_lists": [
                                {"name": "AS65100-PREFIX-OUT", "out": True},
                            ],
                            "slow_peer_options": {"detection": {"threshold": 150}},
                            "route_maps": [{"name": "test-out", "out": True}],
                        },
                    ],
                },
            ],
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_bgp_address_family_merged_multiple_neighbor(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            neighbor=[
                                dict(
                                    address="192.31.39.212",
                                    soft_reconfiguration=True,
                                    activate=True,
                                ),
                                dict(
                                    address="192.31.47.206",
                                    soft_reconfiguration=True,
                                    activate=True,
                                ),
                            ],
                            network=[
                                dict(address="192.0.3.1", mask="255.255.255.0"),
                                dict(address="192.0.2.1", mask="255.255.255.0"),
                                dict(address="192.0.4.1", mask="255.255.255.0"),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4",
            "neighbor 192.31.39.212 activate",
            "neighbor 192.31.39.212 soft-reconfiguration inbound",
            "neighbor 192.31.47.206 activate",
            "neighbor 192.31.47.206 soft-reconfiguration inbound",
            "network 192.0.3.1 mask 255.255.255.0",
            "network 192.0.2.1 mask 255.255.255.0",
            "network 192.0.4.1 mask 255.255.255.0",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_overridden_multiple_neighbor(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp log-neighbor-changes
             bgp nopeerup-delay cold-boot 20
             neighbor TEST-PEER-GROUP peer-group
             neighbor 2001:db8::1 peer-group TEST-PEER-GROUP
             neighbor 2001:db8::1 description TEST-PEER-GROUP-DESCRIPTION
             !
             address-family ipv4
              bgp redistribute-internal
              redistribute connected
              redistribute ospf 200 metric 100 match internal external 1 external 2
              neighbor TEST-PEER-GROUP send-community
              neighbor TEST-PEER-GROUP next-hop-self all
              neighbor 2001:db8::1 activate
             !
             address-family ipv4 multicast
              table-map test_tableMap filter
              network 198.51.111.11 mask 255.255.255.255 route-map test
              aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
              default-metric 12
              distance bgp 10 10 100
             exit-address-family
             !
             address-family ipv4 mdt
              bgp dampening 1 10 100 5
              bgp dmzlink-bw
              bgp soft-reconfig-backup
             exit-address-family
             !
             address-family ipv4 multicast vrf blue
              bgp aggregate-timer 10
              bgp slow-peer detection threshold 150
              bgp dampening 1 1 1 1
              network 198.51.110.10 mask 255.255.255.255 backdoor
              aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
              neighbor 198.51.100.1 remote-as 10
              neighbor 198.51.100.1 local-as 20
              neighbor 198.51.100.1 activate
              neighbor 198.51.100.1 next-hop-self all
              neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
              neighbor 198.51.100.1 route-server-client
              neighbor 198.51.100.1 prefix-list AS65100-PREFIX-OUT out
              neighbor 198.51.100.1 slow-peer detection threshold 150
              neighbor 198.51.100.1 route-map test-out out
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            neighbor=[
                                dict(
                                    address="192.31.39.212",
                                    soft_reconfiguration=True,
                                    activate=True,
                                ),
                                dict(
                                    address="192.31.47.206",
                                    soft_reconfiguration=True,
                                    activate=True,
                                ),
                            ],
                            network=[
                                dict(address="192.0.3.1", mask="255.255.255.0"),
                                dict(address="192.0.2.1", mask="255.255.255.0"),
                                dict(address="192.0.4.1", mask="255.255.255.0"),
                            ],
                        ),
                    ],
                ),
                state="overridden",
            ),
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast",
            "no default-metric 12",
            "no distance bgp 10 10 100",
            "no redistribute ospf 200",
            "no table-map test_tableMap filter",
            "no network 198.51.111.11 mask 255.255.255.255 route-map test",
            "no aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
            "address-family ipv4 mdt",
            "no bgp dmzlink-bw",
            "no bgp soft-reconfig-backup",
            "no bgp dampening 1 10 100 5",
            "address-family ipv4 multicast vrf blue",
            "no bgp aggregate-timer 10",
            "no bgp dampening 1 1 1 1",
            "no bgp slow-peer detection threshold 150",
            "no neighbor 198.51.100.1",
            "no network 198.51.110.10 mask 255.255.255.255 backdoor",
            "no aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
            "address-family ipv4",
            "no bgp redistribute-internal",
            "no redistribute connected",
            "neighbor 192.31.39.212 activate",
            "neighbor 192.31.39.212 soft-reconfiguration inbound",
            "neighbor 192.31.47.206 activate",
            "neighbor 192.31.47.206 soft-reconfiguration inbound",
            "no neighbor TEST-PEER-GROUP",
            "no neighbor 2001:db8::1",
            "network 192.0.3.1 mask 255.255.255.0",
            "network 192.0.2.1 mask 255.255.255.0",
            "network 192.0.4.1 mask 255.255.255.0",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
