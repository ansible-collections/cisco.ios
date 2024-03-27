#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_ospfv3
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule, load_fixture


class TestIosOspfV3Module(TestIosModule):
    module = ios_ospfv3

    def setUp(self):
        super(TestIosOspfV3Module, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv3.ospfv3."
            "Ospfv3Facts.get_ospfv3_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfV3Module, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_ospfv3.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_ospfv3_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            auto_cost=dict(reference_bandwidth="4"),
                            areas=[dict(area_id=10, default_cost=10)],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=100,
                                        max_adjacency=100,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "router ospfv3 1",
            "auto-cost reference-bandwidth 4",
            "area 10 default-cost 10",
            "address-family ipv4 unicast vrf blue",
            "adjacency stagger 100 100",
            "exit-address-family",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv3_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(router_lsa=True, on_startup=dict(time=110)),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(metric=10),
                                    ),
                                ),
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(min_adjacency=50, max_adjacency=50),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25,
                                                    nssa_only=True,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(router_lsa=True, on_startup=dict(time=100)),
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=100,
                                        max_adjacency=100,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        commands = [
            "router ospfv3 1",
            "max-metric router-lsa on-startup 100",
            "no area 10 nssa default-information-originate metric 10",
            "address-family ipv4 unicast vrf blue",
            "adjacency stagger 100 100",
            "exit-address-family",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    #
    def test_ios_ospfv3_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(router_lsa=True, on_startup=dict(time=110)),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(metric=10),
                                    ),
                                ),
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(min_adjacency=50, max_adjacency=50),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25,
                                                    nssa_only=True,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_overridden(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            max_metric=dict(router_lsa=True, on_startup=dict(time=200)),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(metric=10),
                                    ),
                                ),
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    adjacency=dict(min_adjacency=50, max_adjacency=50),
                                    areas=[
                                        dict(
                                            area_id=200,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=200,
                                                    nssa_only=True,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                state="overridden",
            ),
        )

        commands = [
            "no router ospfv3 1",
            "router ospfv3 200",
            "max-metric router-lsa on-startup 200",
            "area 10 nssa default-information-originate metric 10",
            "address-family ipv4 unicast",
            "adjacency stagger 50 50",
            "area 200 nssa default-information-originate metric 200 nssa-only",
            "exit-address-family",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv3_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(router_lsa=True, on_startup=dict(time=110)),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(metric=10),
                                    ),
                                ),
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(min_adjacency=50, max_adjacency=50),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25,
                                                    nssa_only=True,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_deleted(self):
        set_module_args(
            dict(config=dict(processes=[dict(process_id="1")]), state="deleted"),
        )
        commands = ["no router ospfv3 1"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv3_parsed(self):
        set_module_args(dict(running_config="router ospfv3 1\n area 5", state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = {"processes": [{"areas": [{"area_id": "5"}], "process_id": 1}]}
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_ospfv3_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    {
                        "processes": [
                            {
                                "address_family": [
                                    {
                                        "adjacency": {
                                            "disable": True,
                                            "max_adjacency": 25,
                                            "min_adjacency": 25,
                                            "none": True,
                                        },
                                        "afi": "ipv4",
                                        "areas": [
                                            {
                                                "area_id": "25",
                                                "authentication": {
                                                    "null": True,
                                                },
                                                "default_cost": 10,
                                                # "filter_list": [
                                                #     {
                                                #         "name": "flist1",
                                                #         "direction": "in",
                                                #     }
                                                # ],
                                                "normal": True,
                                                "nssa": {
                                                    "default_information_originate": {
                                                        "metric": 25,
                                                        "metric_type": 1,
                                                        "nssa_only": True,
                                                    },
                                                    "no_redistribution": True,
                                                    "no_summary": True,
                                                    "set": True,
                                                    "translate": "always",
                                                },
                                                # "ranges": [
                                                #     {
                                                #         "address": "172.16.1.0",
                                                #         "netmask": "0.0.0.255",
                                                #         "advertise": True,
                                                #         "cost": 150,
                                                #         "not_advertise": True,
                                                #     }
                                                # ],
                                                "sham_link": {
                                                    "source": "demoSource",
                                                    "destination": "demoDest",
                                                    "authentication": {
                                                        "key_chain": "mykey",
                                                        "null": True,
                                                    },
                                                    "cost": 10,
                                                    "ttl_security": 20,
                                                },
                                                "stub": {
                                                    "set": True,
                                                    "no_summary": True,
                                                },
                                            },
                                        ],
                                        "authentication": {
                                            "deployment": True,
                                            "normal": True,
                                        },
                                        "auto_cost": {
                                            "set": True,
                                            "reference_bandwidth": 10,
                                        },
                                        "bfd": {
                                            "all_interfaces": True,
                                            "disable": True,
                                        },
                                        # "capability": True,
                                        "compatible": {
                                            "rfc1583": True,
                                            "rfc1587": True,
                                            "rfc5243": True,
                                        },
                                        "default_information": {
                                            "originate": True,
                                            "always": True,
                                            "metric": 10,
                                            "metric_type": 100,
                                            "route_map": "rmap1",
                                        },
                                        "default_metric": 10,
                                        "discard_route": {
                                            "sham_link": True,
                                            "external": True,
                                            "internal": True,
                                        },
                                        "distance": 10,
                                        "distribute_list": {
                                            # "acls": [
                                            #     {
                                            #         "name": "testAcl",
                                            #         "direction": "in",
                                            #         "interface": "GigabitEthernet0/1",
                                            #         "protocol": "tcp",
                                            #     }
                                            # ],
                                            "prefix": {
                                                "name": "Prefixlist1",
                                                "gateway_name": "gateway1",
                                                "direction": "in",
                                                "interface": "GigabitEthernet0/1",
                                                "protocol": "tcp",
                                            },
                                            "route_map": {"name": "ramp1"},
                                        },
                                        "event_log": {
                                            "enable": True,
                                            "one_shot": True,
                                            "pause": True,
                                            "size": 200,
                                        },
                                        "graceful_restart": {
                                            "enable": True,
                                            "disable": True,
                                            "strict_lsa_checking": True,
                                        },
                                        "interface_id": {
                                            "ios_if_index": True,
                                            "snmp_if_index": True,
                                        },
                                        # "limit": {
                                        #     "dc": {
                                        #         "number": {"type": 20},
                                        #         "disable": {"type": True},
                                        #     },
                                        #     "non_dc": {
                                        #         "number": {"type": 20},
                                        #         "disable": {"type": True},
                                        #     },
                                        # },
                                        "local_rib_criteria": {
                                            "enable": True,
                                            "forwarding_address": True,
                                            "inter_area_summary": True,
                                            "nssa_translation": True,
                                        },
                                        "log_adjacency_changes": {
                                            "set": True,
                                            "detail": True,
                                        },
                                        "manet": {
                                            "cache": {
                                                "acknowledgement": 10,
                                                "update": 20,
                                            },
                                            "hello": {
                                                "multicast": True,
                                                "unicast": True,
                                            },
                                            "peering": {
                                                "set": True,
                                                "disable": True,
                                                "per_interface": True,
                                                "redundancy": 10,
                                            },
                                            "willingness": 10,
                                        },
                                        "max_lsa": {
                                            "number": 10,
                                            "threshold_value": 20,
                                            "ignore_count": 30,
                                            "ignore_time": 5,
                                            "reset_time": 5,
                                            "warning_only": True,
                                        },
                                        "max_metric": {
                                            "disable": True,
                                            "external_lsa": 20,
                                            "inter_area_lsas": 30,
                                            "on_startup": {
                                                "time": 15,
                                                "wait_for_bgp": True,
                                            },
                                            "stub_prefix_lsa": True,
                                        },
                                        "maximum_paths": 35,
                                        "passive_interface": "gigEth0/1",
                                        "prefix_suppression": {
                                            "enable": True,
                                        },
                                        "queue_depth": {
                                            "hello": {
                                                "max_packets": 10,
                                                "unlimited": True,
                                            },
                                            "update": {
                                                "max_packets": 20,
                                                "unlimited": True,
                                            },
                                        },
                                        "router_id": "router2",
                                        "shutdown": {
                                            "enable": True,
                                        },
                                        "summary_prefix": {
                                            "address": "172.16.1.0",
                                            "mask": "0.0.0.255",
                                            "not_advertise": True,
                                            "nssa_only": True,
                                            "tag": 15,
                                        },
                                        "timers": {
                                            "lsa": 10,
                                            "manet": {
                                                "cache": {
                                                    "acknowledgement": 20,
                                                    "redundancy": 30,
                                                },
                                                "hello": True,
                                                "peering": {
                                                    "set": True,
                                                    "per_interface": True,
                                                    "redundancy": 40,
                                                },
                                                "willingness": 30,
                                            },
                                            "pacing": {
                                                "flood": 10,
                                                "lsa_group": 20,
                                                "retransmission": 30,
                                            },
                                            "throttle": {
                                                "lsa": {
                                                    "first_delay": 10,
                                                    "min_delay": 20,
                                                    "max_delay": 30,
                                                },
                                                "spf": {
                                                    "receive_delay": 20,
                                                    "between_delay": 25,
                                                    "max_delay": 35,
                                                },
                                            },
                                        },
                                        "unicast": True,
                                        "vrf": "ospf_vrf",
                                    },
                                ],
                                "adjacency": {
                                    "min_adjacency": 10,
                                    "max_adjacency": 20,
                                    "none": True,
                                },
                                "areas": [
                                    {
                                        "area_id": "10",
                                        "authentication": {
                                            "key_chain": "topsecretpass",
                                            "ipsec": {
                                                "spi": 10,
                                                "md5": 10,
                                                "sha1": 20,
                                                "hex_string": "736563726574506173736f777264",
                                            },
                                        },
                                        "default_cost": 50,
                                        "nssa": {
                                            "default_information_originate": {
                                                "metric": 10,
                                                "metric_type": 2,
                                                "nssa_only": True,
                                            },
                                            "no_redistribution": True,
                                            "no_summary": True,
                                            "set": True,
                                            "translate": "always",
                                        },
                                        "stub": {
                                            "set": True,
                                            "no_summary": True,
                                        },
                                    },
                                ],
                                "authentication": True,
                                "auto_cost": {
                                    "set": True,
                                    "reference_bandwidth": 10,
                                },
                                "bfd": True,
                                "compatible": {
                                    "rfc1583": True,
                                    "rfc1587": True,
                                    "rfc5243": True,
                                },
                                "event_log": {
                                    "enable": True,
                                    "one_shot": True,
                                    "pause": True,
                                    "size": True,
                                },
                                "graceful_restart": {
                                    "disable": True,
                                    "strict_lsa_checking": True,
                                },
                                "help": True,
                                "interface_id": True,
                                # "limit": {
                                #     "dc": {
                                #         "number": 10,
                                #         "disable": True,
                                #     },
                                #     "non_dc": {
                                #         "number": 10,
                                #         "disable": True,
                                #     },
                                # },
                                "local_rib_criteria": {
                                    "enable": True,
                                    "forwarding_address": True,
                                    "inter_area_summary": True,
                                    "nssa_translation": True,
                                },
                                "log_adjacency_changes": {"set": True, "detail": True},
                                "manet": {
                                    "cache": {
                                        "acknowledgement": 10,
                                        "redundancy": 20,
                                    },
                                    "hello": True,
                                    "peering": {
                                        "set": True,
                                        "per_interface": True,
                                        "redundancy": 20,
                                    },
                                    # "willingness": "test",
                                },
                                "max_lsa": {
                                    "number": 10,
                                    "threshold_value": 10,
                                    "ignore_count": 10,
                                    "ignore_time": 10,
                                    "reset_time": 10,
                                    "warning_only": True,
                                },
                                "max_metric": {
                                    "external_lsa": 10,
                                    "include_stub": True,
                                    "on_startup": {"time": 110, "wait_for_bgp": True},
                                    "router_lsa": True,
                                    "summary_lsa": 10,
                                },
                                "passive_interface": "GigabitEthernet0/1",
                                "prefix_suppression": True,
                                "process_id": 1,
                                "queue_depth": {
                                    "hello": {
                                        "max_packets": 20,
                                        "unlimited": True,
                                    },
                                },
                                "router_id": "router1",
                                "shutdown": True,
                                "timers": {
                                    "lsa": 10,
                                    "manet": {
                                        "cache": {
                                            "acknowledgement": 10,
                                            "redundancy": 20,
                                        },
                                        "hello": True,
                                        "peering": {
                                            "set": True,
                                            "per_interface": True,
                                            "redundancy": 10,
                                        },
                                        "willingness": 20,
                                    },
                                    "pacing": {
                                        "flood": 20,
                                        "lsa_group": 20,
                                        "retransmission": 20,
                                    },
                                    "throttle": {
                                        "lsa": {
                                            "first_delay": 30,
                                            "min_delay": 10,
                                            "max_delay": 50,
                                        },
                                        "spf": {
                                            "receive_delay": 10,
                                            "between_delay": 5,
                                            "max_delay": 20,
                                        },
                                    },
                                },
                            },
                        ],
                    },
                ),
                state="rendered",
            ),
        )
        commands = [
            "router ospfv3 1",
            "adjacency stagger none 10",
            "auto-cost reference-bandwidth 10",
            "bfd all-interfaces",
            "compatible rfc1583",
            "event-log one-shot pause size True",
            "help",
            "interface-id snmp-if-index",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "manet cache acknowledgement 10",
            "manet hello",
            "manet peering selective per-interface redundancy 20",
            "max-lsa 10 10 ignore-count 10 ignore-time 10 reset-time 10 warning-only",
            "max-metric router-lsa external-lsa 10 include-stub on-startup 110 summary-lsa 10",
            "passive-interface GigabitEthernet0/1",
            "prefix-suppression",
            "router-id router1",
            "shutdown",
            "area 10 authentication",
            "area 10 default-cost 50",
            "area 10 nssa default-information-originate metric 10 metric-type 2 nssa-only no-redistribution no-summary",
            "area 10 nssa translate type7 always",
            "area 10 stub no-summary",
            "address-family ipv4 unicast vrf ospf_vrf",
            "adjacency stagger none 25",
            "auto-cost reference-bandwidth 10",
            "bfd all-interfaces",
            "compatible rfc1583",
            "default-information originate always metric 10 metric-type 100 route-map rmap1",
            "default-metric 10",
            "distribute-list prefix Prefixlist1 gateway gateway1 in GigabitEthernet0/1 tcp",
            "distribute-list route-map ramp1 in",
            "event-log one-shot pause size 200",
            "graceful_restart True disable",
            "interface-id snmp-if-index",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "max-lsa 10 20 ignore-count 30 ignore-time 5 reset-time 5 warning-only",
            "max-lsa 10 20 ignore-count 30 ignore-time 5 reset-time 5 warning-only",
            "max-metric external-lsa 20 on-startup 15",
            "maximum-paths 35",
            "passive-interface gigEth0/1",
            "prefix-suppression",
            "router-id router2",
            "shutdown",
            "summary-prefix 172.16.1.0 0.0.0.255 not-advertise",
            "area 25 authentication",
            "area 25 default-cost 10",
            "area 25 nssa default-information-originate metric 25 metric-type 1 nssa-only no-redistribution no-summary",
            "area 25 nssa translate type7 always",
            "area 25 sham-link demoSource demoDest cost 10 ttl-security hops 20",
            "area 25 stub no-summary",
            "exit-address-family",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
