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

    def test_ios_bgp_global_asdot_local_as_parsed(self):
        """local_as.number must be returned as string "501.65083" (not float) for ASDOT notation."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65000
                     bgp asnotation dot
                     neighbor 192.0.2.1 remote-as 100
                     neighbor 192.0.2.1 local-as 501.65083
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        neighbor = next(
            n for n in result["parsed"]["neighbors"] if n["neighbor_address"] == "192.0.2.1"
        )
        self.assertEqual(neighbor["local_as"]["number"], "501.65083")
        self.assertIsInstance(neighbor["local_as"]["number"], str)

    def test_ios_bgp_global_asdot_local_as_merged_idempotent(self):
        """merged state with ASDOT local_as must be idempotent when device already has it."""
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp asnotation dot
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 local-as 501.65083
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bgp": {"asnotation": True},
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.1",
                            "remote_as": "100",
                            "local_as": {"set": True, "number": "501.65083"},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_asdot_local_as_int_backward_compat(self):
        """Integer local_as.number (e.g. 234) must still be accepted after type changed to str."""
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.1 remote-as 100
             neighbor 192.0.2.1 local-as 234
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
                            "local_as": {"set": True, "number": 234},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_asdot_combined_parsed(self):
        """ASDOT remote_as and ASDOT local_as.number must both be strings when parsed together."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65000
                     bgp asnotation dot
                     neighbor 192.0.2.1 remote-as 501.65083
                     neighbor 192.0.2.1 local-as 300.65
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        neighbor = next(
            n for n in result["parsed"]["neighbors"] if n["neighbor_address"] == "192.0.2.1"
        )
        self.assertEqual(neighbor["remote_as"], "501.65083")
        self.assertIsInstance(neighbor["remote_as"], str)
        self.assertEqual(neighbor["local_as"]["number"], "300.65")
        self.assertIsInstance(neighbor["local_as"]["number"], str)

    def test_ios_bgp_global_asdot_combined_merged_idempotent(self):
        """Merged with ASDOT remote_as and ASDOT local_as.number together must be idempotent."""
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bgp asnotation dot
             neighbor 192.0.2.1 remote-as 501.65083
             neighbor 192.0.2.1 local-as 300.65
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bgp": {"asnotation": True},
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.1",
                            "remote_as": "501.65083",
                            "local_as": {"set": True, "number": "300.65"},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    # ------------------------------------------------------------------ BMP

    BMP_RUNNING_CONFIG = dedent(
        """\
        router bgp 65000
         bmp server 1
          address 192.0.2.10 port-number 5000
          description collector one
          initial-delay 15
          failure-retry-delay 20
          flapping-delay 120
          stats-reporting-period 60
          update-source Loopback100
          set ip dscp 5
          activate
         exit-bmp-server-mode
         bmp server 2
          address 192.0.2.11 port-number 5001
         exit-bmp-server-mode
         bmp buffer-size 1024
         bmp initial-refresh delay 30
         neighbor 192.0.2.1 remote-as 65001
         neighbor 192.0.2.1 bmp-activate all
         neighbor 192.0.2.2 remote-as 65002
         neighbor 192.0.2.2 bmp-activate server 1 server 2
        """,
    )

    BMP_SERVER_ONE = {
        "number": 1,
        "address": {"host": "192.0.2.10", "port": 5000},
        "description": "collector one",
        "initial_delay": 15,
        "failure_retry_delay": 20,
        "flapping_delay": 120,
        "stats_reporting_period": 60,
        "update_source": "Loopback100",
        "set_ip_dscp": 5,
        "activate": True,
    }

    def _bmp_config(self, **overrides):
        config = {
            "as_number": "65000",
            "bgp": {"default": {"ipv4_unicast": True, "route_target": {"filter": True}}},
            "bmp": {
                "buffer_size": 1024,
                "initial_refresh": {"delay": 30},
                "servers": [
                    dict(self.BMP_SERVER_ONE),
                    {"number": 2, "address": {"host": "192.0.2.11", "port": 5001}},
                ],
            },
            "neighbors": [
                {
                    "neighbor_address": "192.0.2.1",
                    "remote_as": "65001",
                    "bmp_activate": {"all": True},
                },
                {
                    "neighbor_address": "192.0.2.2",
                    "remote_as": "65002",
                    "bmp_activate": {"servers": [1, 2]},
                },
            ],
        }
        config.update(overrides)
        return config

    def test_ios_bgp_global_bmp_parsed(self):
        set_module_args({"running_config": self.BMP_RUNNING_CONFIG, "state": "parsed"})
        parsed = self.execute_module(changed=False)["parsed"]
        self.assertEqual(parsed["bmp"]["buffer_size"], 1024)
        self.assertEqual(parsed["bmp"]["initial_refresh"], {"delay": 30})
        self.assertEqual(
            parsed["bmp"]["servers"],
            [
                self.BMP_SERVER_ONE,
                {"number": 2, "address": {"host": "192.0.2.11", "port": 5001}},
            ],
        )
        neighbors = {n["neighbor_address"]: n for n in parsed["neighbors"]}
        self.assertEqual(neighbors["192.0.2.1"]["bmp_activate"], {"all": True})
        self.assertEqual(neighbors["192.0.2.2"]["bmp_activate"], {"servers": [1, 2]})

    def test_ios_bgp_global_bmp_merged_idempotent(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args({"config": self._bmp_config(), "state": "merged"})
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_bmp_replaced_idempotent(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args({"config": self._bmp_config(), "state": "replaced"})
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_bmp_rendered(self):
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {"servers": [dict(self.BMP_SERVER_ONE)]},
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.9",
                            "remote_as": "65009",
                            "bmp_activate": {"servers": [2, 1]},
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = self.execute_module(changed=False)["rendered"]
        self.assertEqual(
            rendered[rendered.index("bmp server 1") : rendered.index("exit-bmp-server-mode") + 1],
            [
                "bmp server 1",
                "address 192.0.2.10 port-number 5000",
                "description collector one",
                "failure-retry-delay 20",
                "flapping-delay 120",
                "initial-delay 15",
                "set ip dscp 5",
                "stats-reporting-period 60",
                "update-source Loopback100",
                "activate",
                "exit-bmp-server-mode",
            ],
        )
        self.assertIn("neighbor 192.0.2.9 bmp-activate server 1 server 2", rendered)

    def test_ios_bgp_global_bmp_merged_option_change(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {
                        "servers": [{"number": 1, "description": "collector uno", "set_ip_dscp": 3}]
                    },
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "bmp server 1",
                "description collector uno",
                "set ip dscp 3",
                "exit-bmp-server-mode",
            ],
        )

    def test_ios_bgp_global_bmp_merged_address_change_on_active_server(self):
        """IOS-XE ignores an address change while activated, so it is deactivated around it."""
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {
                        "servers": [{"number": 1, "address": {"host": "192.0.2.50", "port": 5500}}]
                    },
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "bmp server 1",
                "no activate",
                "no address 192.0.2.10 port-number 5000",
                "address 192.0.2.50 port-number 5500",
                "activate",
                "exit-bmp-server-mode",
            ],
        )

    def test_ios_bgp_global_bmp_merged_new_server(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {
                        "servers": [
                            {
                                "number": 3,
                                "address": {"host": "192.0.2.12", "port": 5002},
                                "activate": True,
                            },
                        ],
                    },
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "bmp server 3",
                "address 192.0.2.12 port-number 5002",
                "activate",
                "exit-bmp-server-mode",
            ],
        )

    def test_ios_bgp_global_bmp_new_server_without_options(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args(
            {
                "config": {"as_number": "65000", "bmp": {"servers": [{"number": 4}]}},
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["router bgp 65000", "bmp server 4", "exit-bmp-server-mode"],
        )

    def test_ios_bgp_global_bmp_replaced_removes_options_and_servers(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        config = self._bmp_config()
        config["bmp"] = {
            "initial_refresh": {"skip": True},
            "servers": [
                {
                    "number": 1,
                    "address": {"host": "192.0.2.10", "port": 5000},
                    "description": "collector one",
                    "activate": True,
                },
            ],
        }
        set_module_args({"config": config, "state": "replaced"})
        result = self.execute_module(changed=True)
        commands = result["commands"]
        for expected in (
            "no bmp buffer-size 1024",
            "no bmp initial-refresh delay 30",
            "bmp initial-refresh skip",
            "no bmp server 2",
            "no initial-delay 15",
            "no failure-retry-delay 20",
            "no flapping-delay 120",
            "no stats-reporting-period 60",
            "no update-source Loopback100",
            "no set ip dscp 5",
        ):
            self.assertIn(expected, commands)
        self.assertNotIn("no activate", commands)
        self.assertNotIn("no description collector one", commands)

    def test_ios_bgp_global_bmp_server_deactivated(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {"servers": [{"number": 1, "activate": False}]},
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["router bgp 65000", "bmp server 1", "no activate", "exit-bmp-server-mode"],
        )

    def test_ios_bgp_global_bmp_deleted(self):
        self.execute_show_command.return_value = self.BMP_RUNNING_CONFIG
        set_module_args({"config": {"as_number": "65000"}, "state": "deleted"})
        commands = self.execute_module(changed=True)["commands"]
        for expected in (
            "no bmp server 1",
            "no bmp server 2",
            "no bmp buffer-size 1024",
            "no bmp initial-refresh delay 30",
        ):
            self.assertIn(expected, commands)

    def test_ios_bgp_global_bmp_neighbor_idempotent_all_and_servers(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.1 remote-as 65001
             neighbor 192.0.2.1 bmp-activate all
             neighbor 192.0.2.2 remote-as 65002
             neighbor 192.0.2.2 bmp-activate server 1 server 2
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.1",
                            "remote_as": "65001",
                            "bmp_activate": {"all": True},
                        },
                        {
                            "neighbor_address": "192.0.2.2",
                            "remote_as": "65002",
                            "bmp_activate": {"servers": [2, 1]},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_bmp_neighbor_activate_clears_before_change(self):
        """IOS-XE ignores bmp-activate on an activated neighbor, so the old one is removed first."""
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.2 remote-as 65002
             neighbor 192.0.2.2 bmp-activate server 1 server 2
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bgp": {"default": {"ipv4_unicast": True, "route_target": {"filter": True}}},
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.2",
                            "remote_as": "65002",
                            "bmp_activate": {"servers": [3]},
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "no neighbor 192.0.2.2 bmp-activate",
                "neighbor 192.0.2.2 bmp-activate server 3",
            ],
        )

    def test_ios_bgp_global_bmp_neighbor_activate_merged_unites_servers(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.2 remote-as 65002
             neighbor 192.0.2.2 bmp-activate server 1 server 2
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.2",
                            "remote_as": "65002",
                            "bmp_activate": {"servers": [3]},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "no neighbor 192.0.2.2 bmp-activate",
                "neighbor 192.0.2.2 bmp-activate server 1 server 2 server 3",
            ],
        )

    def test_ios_bgp_global_bmp_neighbor_activate_merged_all_wins(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.2 remote-as 65002
             neighbor 192.0.2.2 bmp-activate server 1
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.2",
                            "remote_as": "65002",
                            "bmp_activate": {"all": True},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "router bgp 65000",
                "no neighbor 192.0.2.2 bmp-activate",
                "neighbor 192.0.2.2 bmp-activate all",
            ],
        )

    def test_ios_bgp_global_bmp_neighbor_activate_removed_on_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.2 remote-as 65002
             neighbor 192.0.2.2 bmp-activate all
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bgp": {"default": {"ipv4_unicast": True, "route_target": {"filter": True}}},
                    "neighbors": [{"neighbor_address": "192.0.2.2", "remote_as": "65002"}],
                },
                "state": "replaced",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"], ["router bgp 65000", "no neighbor 192.0.2.2 bmp-activate"]
        )

    def test_ios_bgp_global_bmp_legacy_server_options(self):
        """The deprecated server/server_options still work and are the same as servers."""
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bmp server 4
              address 192.0.2.14 port-number 5004
              activate
             exit-bmp-server-mode
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bmp": {
                        "server": 4,
                        "server_options": {
                            "activate": True,
                            "address": {"host": "192.0.2.14", "port": 5004},
                        },
                    },
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_bmp_legacy_neighbor_server(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             neighbor 192.0.2.2 remote-as 65002
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.2",
                            "remote_as": "65002",
                            "bmp_activate": {"server": 2},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["router bgp 65000", "neighbor 192.0.2.2 bmp-activate server 2"],
        )

    def test_ios_bgp_global_bmp_server_options_without_server_fails(self):
        self.execute_show_command.return_value = "router bgp 65000\n"
        set_module_args(
            {
                "config": {"as_number": "65000", "bmp": {"server_options": {"activate": True}}},
                "state": "merged",
            },
        )
        result = self.execute_module(failed=True)
        self.assertIn("server_options requires", result["msg"])

    def test_ios_bgp_global_bmp_initial_refresh_switch(self):
        self.execute_show_command.return_value = dedent(
            """\
            router bgp 65000
             bmp initial-refresh delay 30
            """,
        )
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "bgp": {"default": {"ipv4_unicast": True, "route_target": {"filter": True}}},
                    "bmp": {"initial_refresh": {"skip": True}},
                },
                "state": "replaced",
            },
        )
        commands = self.execute_module(changed=True)["commands"]
        self.assertIn("bmp initial-refresh skip", commands)
        self.assertIn("no bmp initial-refresh delay 30", commands)

    def test_ios_bgp_global_bmp_neighbor_activate_follows_remote_as(self):
        """IOS-XE drops bmp-activate for a neighbor that does not exist yet."""
        self.execute_show_command.return_value = "router bgp 65000\n"
        set_module_args(
            {
                "config": {
                    "as_number": "65000",
                    "neighbors": [
                        {
                            "neighbor_address": "192.0.2.1",
                            "remote_as": "65001",
                            "bmp_activate": {"all": True},
                        },
                    ],
                },
                "state": "merged",
            },
        )
        commands = self.execute_module(changed=True)["commands"]
        self.assertLess(
            commands.index("neighbor 192.0.2.1 remote-as 65001"),
            commands.index("neighbor 192.0.2.1 bmp-activate all"),
        )
