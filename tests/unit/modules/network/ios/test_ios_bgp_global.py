#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_bgp_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import AnsibleFailJson, set_module_args

from .ios_module import TestIosModule


class TestIosBgpGlobalModule(TestIosModule):
    module = ios_bgp_global

    def setUp(self):
        super(TestIosBgpGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_global.bgp_global."
            "Bgp_globalFacts.get_bgp_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBgpGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_bgp_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 route-map test-route out
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )

        set_module_args(
            {
                "config": {
                    "aggregate_addresses": [
                        {
                            "address": "192.0.2.3",
                            "attribute_map": "ma",
                            "netmask": "255.255.0.0",
                            "summary_only": True,
                        },
                        {
                            "address": "192.0.2.4",
                            "as_set": True,
                            "netmask": "255.255.255.0",
                        },
                        {
                            "address": "192.0.2.5",
                            "as_set": True,
                            "netmask": "255.255.255.0",
                        },
                    ],
                    "as_number": "65000",
                    "auto_summary": True,
                    "bgp": {
                        "additional_paths": {"send": True},
                        "aggregate_timer": 0,
                        "always_compare_med": True,
                        "asnotation": True,
                        "bestpath_options": {
                            "aigp": True,
                            "compare_routerid": True,
                            "med": {"confed": True, "missing_as_worst": True},
                        },
                        "confederation": {"identifier": "22"},
                        "consistency_checker": {
                            "error_message": {"interval": 10, "set": True},
                        },
                        "dampening": {
                            "max_suppress": 44,
                            "penalty_half_time": 22,
                            "reuse_route_val": 22,
                            "suppress_route_val": 33,
                        },
                        "deterministic_med": True,
                        "graceful_restart": {"restart_time": 2, "stalepath_time": 22},
                        "graceful_shutdown": {
                            "community": "22",
                            "local_preference": 23,
                            "neighbors": {"time": 31},
                        },
                        "inject_maps": [
                            {
                                "copy_attributes": True,
                                "exist_map_name": "mp2",
                                "name": "map1",
                            },
                            {
                                "copy_attributes": True,
                                "exist_map_name": "mp3",
                                "name": "map2",
                            },
                        ],
                        "listen": {
                            "limit": 200,
                            "range": {
                                "host_with_subnet": "192.0.2.9/24",
                                "peer_group": "mygrp",
                            },
                        },
                        "log_neighbor_changes": True,
                        "maxas_limit": 2,
                        "maxcommunity_limit": 3,
                        "maxextcommunity_limit": 3,
                        "nexthop": {"route_map": "map1", "trigger": {"delay": 2}},
                        "nopeerup_delay_options": {
                            "cold_boot": 2,
                            "nsf_switchover": 10,
                            "post_boot": 22,
                            "user_initiated": 22,
                        },
                        "recursion": True,
                        "redistribute_internal": True,
                        "refresh": {"max_eor_time": 700, "stalepath_time": 800},
                        "router_id": {"vrf": True},
                        "scan_time": 22,
                        "slow_peer": {
                            "detection": {"threshold": 345},
                            "split_update_group": {"dynamic": True, "permanent": True},
                        },
                        "sso": True,
                        "suppress_inactive": True,
                        "update_delay": 2,
                        "update_group": True,
                    },
                    "bmp": {"buffer_size": 22},
                    "distance": {
                        "bgp": {
                            "routes_external": 2,
                            "routes_internal": 3,
                            "routes_local": 4,
                        },
                        "mbgp": {
                            "routes_external": 2,
                            "routes_internal": 3,
                            "routes_local": 5,
                        },
                    },
                    "distributes": [
                        {"out": True, "prefix": "workcheck"},
                        {"gateway": "checkme", "in": True},
                    ],
                    "maximum_paths": {"ibgp": 22},
                    "maximum_secondary_paths": {"ibgp": 22, "paths": 12},
                    "template": {"peer_policy": "Test1"},
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.3",
                            "remote_as": "300",
                            "timers": {
                                "holdtime": 20,
                                "interval": 10,
                            },
                        },
                        {
                            "aigp": {
                                "send": {
                                    "cost_community": {
                                        "id": 100,
                                        "poi": {"igp_cost": True, "transitive": True},
                                    },
                                },
                            },
                            "neighbor_address": "192.0.2.4",
                            "remote_as": "100.1",
                        },
                    ],
                    "redistribute": [
                        {"application": {"metric": 22, "name": "ap1"}},
                        {
                            "application": {
                                "metric": 33,
                                "name": "ap112",
                                "route_map": "mp1",
                            },
                        },
                        {"connected": {"metric": 22}},
                        {"static": {"metric": 33, "route_map": "mp1"}},
                        {"mobile": {"metric": 211}},
                    ],
                },
                "state": "merged",
            },
        )
        commands = [
            "router bgp 65000",
            "auto-summary",
            "bmp buffer-size 22",
            "distance bgp 2 3 4",
            "distance mbgp 2 3 5",
            "maximum-paths ibgp 22",
            "maximum-secondary-paths 12",
            "maximum-secondary-paths ibgp 22",
            "bgp additional-paths send",
            "bgp aggregate-timer 0",
            "bgp always-compare-med",
            "bgp asnotation dot",
            "bgp bestpath aigp ignore",
            "bgp bestpath med confed missing-as-worst",
            "bgp confederation identifier 22",
            "bgp consistency-checker error-message interval 10",
            "bgp dampening 22 22 33 44",
            "bgp deterministic-med",
            "bgp graceful-restart restart-time 2",
            "bgp graceful-restart stalepath-time 22",
            "bgp graceful-shutdown all neighbors 31 local-preference 23 community 22",
            "bgp listen limit 200",
            "bgp listen range 192.0.2.9/24 peer-group mygrp",
            "bgp log-neighbor-changes",
            "bgp maxas-limit 2",
            "bgp maxcommunity-limit 3",
            "bgp maxextcommunity-limit 3",
            "bgp nexthop route-map map1",
            "bgp nexthop trigger delay 2",
            "bgp nopeerup-delay cold-boot 2",
            "bgp nopeerup-delay post-boot 22",
            "bgp nopeerup-delay nsf-switchover 10",
            "bgp nopeerup-delay user-initiated 22",
            "bgp recursion host",
            "bgp redistribute-internal",
            "bgp refresh max-eor-time 700",
            "bgp refresh stalepath-time 800",
            "bgp router-id vrf auto-assign",
            "bgp scan-time 22",
            "bgp slow-peer detection threshold 345",
            "bgp slow-peer split-update-group dynamic permanent",
            "bgp sso route-refresh-enable",
            "bgp suppress-inactive",
            "bgp update-delay 2",
            "bgp update-group split as-override",
            "bgp inject-map map1 exist-map mp2 copy-attributes",
            "bgp inject-map map2 exist-map mp3 copy-attributes",
            "distribute-list prefix workcheck out",
            "distribute-list gateway checkme in",
            "aggregate-address 192.0.2.3 255.255.0.0 summary-only attribute-map ma",
            "aggregate-address 192.0.2.4 255.255.255.0 as-set",
            "aggregate-address 192.0.2.5 255.255.255.0 as-set",
            "neighbor 192.0.2.4 remote-as 100.1",
            "neighbor 192.0.2.4 aigp send cost-community 100 poi igp-cost transitive",
            "neighbor 192.0.2.3 remote-as 300",
            "neighbor 192.0.2.3 timers 10 20",
            "redistribute connected metric 22",
            "template peer-policy Test1",
            "redistribute mobile metric 211",
            "redistribute application ap1 metric 22",
            "redistribute static metric 33 route-map mp1",
            "redistribute application ap112 metric 33 route-map mp1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath_options=dict(compare_routerid=True),
                        nopeerup_delay_options=dict(post_boot=10),
                    ),
                    redistribute=[dict(connected=dict(set=True, metric=10))],
                    neighbors=[
                        dict(
                            neighbor_address="192.0.2.1",
                            remote_as=100,
                        ),
                    ],
                    timers=dict(keepalive=100, holdtime=200, min_holdtime=150),
                ),
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_ebgp_multihop(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 ebgp-multihop 255
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.1",
                            "remote_as": "100",
                            "ebgp_multihop": {
                                "enable": True,
                                "hop_count": 255,
                            },
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_merged_fail_msg(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="6500",
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath_options=dict(compare_routerid=True),
                        nopeerup_delay_options=dict(post_boot=10),
                    ),
                    redistribute=[dict(connected=dict(set=True, metric=10))],
                    neighbors=[
                        dict(
                            neighbor_address="192.0.2.1",
                            remote_as=100,
                        ),
                    ],
                    timers=dict(keepalive=100, holdtime=200, min_holdtime=150),
                ),
                state="merged",
            ),
        )
        with self.assertRaises(AnsibleFailJson) as error:
            self.execute_module(changed=False, commands=[])
        self.assertIn(
            "BGP is already configured with ASN 65000. Please remove it with state: purged before configuring new ASN",
            str(error.exception),
        )

    def test_ios_bgp_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.2 remote-as 100
             neighbor 192.0.2.2 route-map test-route out
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    aggregate_addresses=[
                        dict(
                            address="192.168.0.1",
                            attribute_map="map",
                            netmask="255.255.0.0",
                        ),
                        dict(
                            address="192.168.0.2",
                            attribute_map="map2",
                            netmask="255.255.0.0",
                        ),
                    ],
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath_options=dict(compare_routerid=True),
                        log_neighbor_changes=True,
                        nopeerup_delay_options=dict(cold_boot=20, post_boot=10),
                    ),
                    redistribute=[dict(connected=dict(set=True, metric=10))],
                    neighbors=[
                        dict(
                            neighbor_address="192.0.2.1",
                            remote_as=200,
                            description="replace neighbor",
                        ),
                    ],
                ),
                state="overridden",
            ),
        )
        commands = [
            "router bgp 65000",
            "no timers bgp 100 200 150",
            "bgp log-neighbor-changes",
            "bgp nopeerup-delay cold-boot 20",
            "aggregate-address 192.168.0.1 255.255.0.0 attribute-map map",
            "aggregate-address 192.168.0.2 255.255.0.0 attribute-map map2",
            "neighbor 192.0.2.1 remote-as 200",
            "neighbor 192.0.2.1 description replace neighbor",
            "no neighbor 192.0.2.2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.2 remote-as 100
             neighbor 192.0.2.2 route-map test-route out
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    aggregate_addresses=[
                        dict(
                            address="192.168.0.1",
                            attribute_map="map",
                            netmask="255.255.0.0",
                        ),
                        dict(
                            address="192.168.0.2",
                            attribute_map="map2",
                            netmask="255.255.0.0",
                        ),
                    ],
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath_options=dict(compare_routerid=True),
                        default=dict(
                            ipv4_unicast=False,
                            route_target=dict(filter=True),
                        ),
                        log_neighbor_changes=True,
                        nopeerup_delay_options=dict(cold_boot=20, post_boot=10),
                    ),
                    redistribute=[dict(connected=dict(set=True, metric=10))],
                    neighbors=[
                        dict(
                            neighbor_address="192.0.2.1",
                            remote_as=200,
                            description="replace neighbor",
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        commands = [
            "router bgp 65000",
            "no bgp default ipv4-unicast",
            "no timers bgp 100 200 150",
            "bgp log-neighbor-changes",
            "bgp nopeerup-delay cold-boot 20",
            "aggregate-address 192.168.0.1 255.255.0.0 attribute-map map",
            "aggregate-address 192.168.0.2 255.255.0.0 attribute-map map2",
            "neighbor 192.0.2.1 remote-as 200",
            "neighbor 192.0.2.1 description replace neighbor",
            "no neighbor 192.0.2.2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath_options=dict(compare_routerid=True),
                        nopeerup_delay_options=dict(post_boot=10),
                    ),
                    redistribute=[dict(connected=dict(set=True, metric=10))],
                    neighbors=[
                        dict(
                            neighbor_address="192.0.2.1",
                            remote_as=100,
                        ),
                    ],
                    timers=dict(keepalive=100, holdtime=200, min_holdtime=150),
                ),
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             no bgp default ipv4-unicast
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 route-map test-route out
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(dict(config=dict(as_number=65000), state="deleted"))
        commands = [
            "router bgp 65000",
            "bgp default ipv4-unicast",
            "no timers bgp 100 200 150",
            "no bgp advertise-best-external",
            "no bgp bestpath compare-routerid",
            "no bgp nopeerup-delay post-boot 10",
            "no neighbor 192.0.2.1",
            "no redistribute connected",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_deleted_empty(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(config=dict(as_number=65000), state="deleted"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_bgp_global_purged(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp nopeerup-delay post-boot 10
             bgp bestpath compare-routerid
             bgp advertise-best-external
             timers bgp 100 200 150
             redistribute connected metric 10
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 route-map test-route out
             address-family ipv4
              neighbor 192.0.2.28 activate
              neighbor 172.31.35.140 activate
            """,
        )
        set_module_args(dict(config=dict(as_number=65000), state="purged"))
        commands = ["no router bgp 65000"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_bgp_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65000
                     bgp nopeerup-delay post-boot 10
                     bgp bestpath compare-routerid
                     bgp advertise-best-external
                     timers bgp 100 200 150
                     redistribute connected metric 10
                     neighbor 192.0.2.1 remote-as 100
                     neighbor 192.0.2.1 password 7 DEQPITOP101395
                     neighbor 192.0.2.1 route-map test-route out
                     address-family ipv4
                      neighbor 192.0.2.28 activate
                      neighbor 172.31.35.140 activate
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "as_number": "65000",
            "bgp": {
                "nopeerup_delay_options": {"post_boot": 10},
                "bestpath_options": {"compare_routerid": True},
                "default": {"ipv4_unicast": True, "route_target": {"filter": True}},
                "advertise_best_external": True,
            },
            "timers": {"keepalive": 100, "holdtime": 200, "min_holdtime": 150},
            "redistribute": [{"connected": {"set": True, "metric": 10}}],
            "neighbors": [
                {
                    "remote_as": "100",
                    "neighbor_address": "192.0.2.1",
                    "route_maps": [
                        {"name": "test-route", "out": True},
                    ],
                    "password_options": {
                        "encryption": 7,
                        "pass_key": "DEQPITOP101395",
                    },
                },
            ],
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_bgp_global_action_states_specific_default(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 6500
             bgp log-neighbor-changes
             no bgp default ipv4-unicast
             no bgp default route-target filter
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 description Test description
             neighbor 192.0.2.2 remote-as 200
             neighbor 192.0.2.2 description Test description 2
             neighbor 192.0.2.2 shutdown
             !
             address-family ipv4
             exit-address-family
            """,
        )
        for stt in ["merged", "replaced", "overridden"]:
            set_module_args(
                {
                    "config": {
                        "as_number": "6500",
                        "bgp": {
                            "default": {
                                "ipv4_unicast": False,
                                "route_target": {
                                    "filter": False,
                                },
                            },
                            "log_neighbor_changes": True,
                        },
                        "neighbors": [
                            {
                                "neighbor_address": "192.0.2.1",
                                "remote_as": "100",
                                "description": "Test description",
                                "shutdown": {  # Don't have in config, adding
                                    "set": True,
                                },
                            },
                            {
                                "neighbor_address": "192.0.2.2",
                                "remote_as": "200",
                                "description": "Test description 2",
                                "shutdown": {  # Have in config negating with false
                                    "set": False,
                                },
                            },
                        ],
                    },
                    "state": stt,
                },
            )
            commands = [
                "router bgp 6500",
                "neighbor 192.0.2.1 shutdown",
                "no neighbor 192.0.2.2 shutdown",
            ]
            result = self.execute_module(changed=True)
            self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_action_states_no_default(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 6500
             bgp log-neighbor-changes
             no bgp default ipv4-unicast
             no bgp default route-target filter
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 description Test description
             neighbor 192.0.2.1 shutdown
             neighbor 192.0.2.2 remote-as 200
             neighbor 192.0.2.2 description Test description 2
             neighbor 192.0.2.2 shutdown
             neighbor 192.0.2.3 remote-as 300
             neighbor 192.0.2.3 description Test description 3
             neighbor 192.0.2.4 remote-as 400
             neighbor 192.0.2.4 description Test description 4
             !
             address-family ipv4
             exit-address-family
            """,
        )
        for stt in ["replaced", "overridden"]:
            set_module_args(
                {
                    "config": {
                        "as_number": "6500",
                        "bgp": {
                            "default": {
                                "ipv4_unicast": False,
                                "route_target": {
                                    "filter": False,
                                },
                            },
                            "log_neighbor_changes": True,
                        },
                        "neighbors": [
                            {
                                "neighbor_address": "192.0.2.1",
                                "remote_as": "100",
                                "description": "Test description",
                                "shutdown": {  # Have in config not adding again (idempotent)
                                    "set": True,
                                },
                            },
                            {
                                "neighbor_address": "192.0.2.2",
                                "remote_as": "200",
                                "description": "Test description 2",  # Have in config but don't want (to be removed)
                            },
                            {
                                "neighbor_address": "192.0.2.3",
                                "remote_as": "300",
                                "description": "Test description 3",  # Don't have in config don't want
                            },
                            {
                                "neighbor_address": "192.0.2.4",
                                "remote_as": "400",
                                "description": "Test description 4",
                                "shutdown": {  # Don't have in config, explicitly don't want
                                    "set": False,
                                },
                            },
                        ],
                    },
                    "state": stt,
                },
            )
            commands = ["router bgp 6500", "no neighbor 192.0.2.2 shutdown"]
            result = self.execute_module(changed=True)
            self.assertEqual(sorted(result["commands"]), sorted(commands))
