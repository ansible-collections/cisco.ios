#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.cisco.ios.plugins.modules import ios_ospfv2
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule, load_fixture


class TestIosOspfV2Module(TestIosModule):
    module = ios_ospfv2

    def setUp(self):
        super(TestIosOspfV2Module, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv2.ospfv2."
            "Ospfv2Facts.get_ospfv2_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfV2Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_ospfv2.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_ospfv2_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            auto_cost=dict(reference_bandwidth="4"),
                            distribute_list=dict(
                                acls=[
                                    dict(direction="out", name="10"),
                                    dict(direction="in", name="123"),
                                ],
                                prefix=dict(
                                    direction="in",
                                    name="123",
                                    gateway_name="gateway",
                                    interface="GigabitEthernet0/1",
                                    protocol="icmp",
                                ),
                            ),
                            network=[
                                dict(address="198.51.100.0", wildcard_bits="0.0.0.255", area=5),
                                dict(address="192.0.2.0", wildcard_bits="0.0.0.255", area=5),
                            ],
                            domain_id=dict(ip_address=dict(address="192.0.3.1")),
                            max_metric=dict(on_startup=dict(time=100), router_lsa=True),
                            passive_interfaces=dict(
                                interface=dict(set_interface=False, name=["GigabitEthernet0/2"]),
                            ),
                            vrf="blue",
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "router ospf 100 vrf blue",
            "auto-cost reference-bandwidth 4",
            "distribute-list 123 in",
            "distribute-list 10 out",
            "distribute-list prefix 123 gateway gateway in GigabitEthernet0/1 icmp",
            "network 198.51.100.0 0.0.0.255 area 5",
            "network 192.0.2.0 0.0.0.255 area 5",
            "domain-id 192.0.3.1",
            "no passive-interface GigabitEthernet0/2",
            "max-metric router-lsa on-startup 100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv2_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            auto_cost=dict(reference_bandwidth="4"),
                            distribute_list=dict(
                                acls=[
                                    dict(direction="out", name="10"),
                                    dict(direction="in", name="123"),
                                ],
                            ),
                            domain_id=dict(ip_address=dict(address="192.0.3.1")),
                            max_metric=dict(on_startup=dict(time=100), router_lsa=True),
                            areas=[dict(area_id="10", capability=True)],
                            passive_interfaces=dict(
                                default=True,
                                interface=dict(
                                    set_interface=False,
                                    name=["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                ),
                            ),
                            vrf="blue",
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv2_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            auto_cost=dict(reference_bandwidth="4"),
                            domain_id=dict(ip_address=dict(address="192.0.1.1")),
                            max_metric=dict(on_startup=dict(time=200), router_lsa=True),
                            areas=[dict(area_id="10", capability=True)],
                            vrf="blue",
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        commands = [
            "router ospf 200 vrf blue",
            "no distribute-list 123 in",
            "no distribute-list 10 out",
            "domain-id 192.0.1.1",
            "max-metric router-lsa on-startup 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv2_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            auto_cost=dict(reference_bandwidth="4"),
                            distribute_list=dict(
                                acls=[
                                    dict(direction="out", name="10"),
                                    dict(direction="in", name="123"),
                                ],
                            ),
                            domain_id=dict(ip_address=dict(address="192.0.3.1")),
                            max_metric=dict(on_startup=dict(time=100), router_lsa=True),
                            areas=[dict(area_id="10", capability=True)],
                            passive_interfaces=dict(
                                default=True,
                                interface=dict(
                                    set_interface=False,
                                    name=["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                ),
                            ),
                            vrf="blue",
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv2_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            auto_cost=dict(reference_bandwidth="4"),
                            distribute_list=dict(
                                acls=[
                                    dict(direction="out", name="10"),
                                    dict(direction="in", name="123"),
                                ],
                            ),
                            domain_id=dict(ip_address=dict(address="192.0.3.1")),
                            max_metric=dict(on_startup=dict(time=100), router_lsa=True),
                            areas=[dict(area_id="10", capability=True)],
                            passive_interfaces=dict(
                                default=True,
                                interface=dict(
                                    set_interface=False,
                                    name=["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                ),
                            ),
                            vrf="blue",
                        ),
                    ],
                ),
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv2_overridden(self):
        set_module_args(
            dict(
                config={
                    "processes": [
                        {
                            "address_family": {
                                "default": True,
                                "snmp_context": "snmp_test",
                                "topology": {
                                    "base": True,
                                    "name": "test_topology",
                                    "tid": True,
                                },
                            },
                            "adjacency": {
                                "max_adjacency": 10,
                                "min_adjacency": 2,
                                "none": True,
                            },
                            "areas": [
                                {
                                    "area_id": "5",
                                    "authentication": {"enable": True, "message_digest": True},
                                },
                                {
                                    "area_id": "10",
                                    "authentication": {"enable": True, "message_digest": True},
                                    "capability": True,
                                    "default_cost": 10,
                                    "filter_list": [
                                        {"direction": "in", "name": "test_prefix_in"},
                                        {"direction": "out", "name": "test_prefix_out"},
                                    ],
                                    "nssa": {
                                        "default_information_originate": {
                                            "metric": 10,
                                            "metric_type": 1,
                                            "nssa_only": True,
                                        },
                                        "no_ext_capability": True,
                                        "no_redistribution": True,
                                        "no_summary": True,
                                        "set": True,
                                        "translate": "suppress-fa",
                                    },
                                    "ranges": [
                                        {
                                            "address": "172.16.1.0",
                                            "advertise": True,
                                            "cost": 20,
                                            "netmask": "0.0.0.255",
                                            "not_advertise": True,
                                        },
                                    ],
                                    "sham_link": {
                                        "cost": 10,
                                        "destination": "checkDestination",
                                        "source": "checkSource",
                                        "ttl_security": 20,
                                    },
                                    "stub": {
                                        "no_ext_capability": True,
                                        "no_summary": True,
                                        "set": True,
                                    },
                                },
                            ],
                            "auto_cost": {
                                "reference_bandwidth": 50,
                                "set": True,
                            },
                            "bfd": True,
                            "capability": {
                                "lls": True,
                                "opaque": True,
                                "transit": True,
                                "vrf_lite": True,
                            },
                            "compatible": {
                                "rfc1583": True,
                                "rfc1587": True,
                                "rfc5243": True,
                            },
                            "default_information": {
                                "always": True,
                                "metric": 25,
                                "metric_type": 26,
                                "originate": True,
                                "route_map": "rmap1",
                            },
                            "default_metric": "50",
                            "discard_route": {
                                "external": 5,
                                "internal": 2,
                                "set": True,
                            },
                            "distance": {
                                "admin_distance": {
                                    "acl": "acl1",
                                    "address": "192.168.1.0",
                                    "distance": 2,
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ospf": {
                                    "external": 1,
                                    "inter_area": 2,
                                    "intra_area": 3,
                                },
                            },
                            "domain_id": {
                                "ip_address": {
                                    "address": "192.168.1.0",
                                    "secondary": True,
                                },
                                "null": True,
                            },
                            "domain_tag": 54,
                            "event_log": {
                                "enable": True,
                                "one_shot": True,
                                "pause": True,
                                "size": 10,
                            },
                            "help": True,
                            "ignore": True,
                            "interface_id": True,
                            "ispf": True,
                            "limit": {
                                "dc": {
                                    "disable": True,
                                    "number": 20,
                                },
                                "non_dc": {
                                    "disable": True,
                                    "number": 10,
                                },
                            },
                            "local_rib_criteria": {
                                "enable": True,
                                "forwarding_address": True,
                                "inter_area_summary": True,
                                "nssa_translation": True,
                            },
                            "log_adjacency_changes": {"detail": True},
                            "max_lsa": {
                                "ignore_count": 10,
                                "ignore_time": 10,
                                "number": 10,
                                "reset_time": 10,
                                "threshold_value": 10,
                                "warning_only": True,
                            },
                            "max_metric": {
                                "external_lsa": 10,
                                "include_stub": True,
                                "on_startup": {"time": 110, "wait_for_bgp": True},
                                "router_lsa": True,
                                "summary_lsa": 20,
                            },
                            "maximum_paths": 15,
                            "mpls": {
                                "ldp": {
                                    "autoconfig": {
                                        "area": "area1",
                                        "set": True,
                                    },
                                    "sync": True,
                                },
                                "traffic_eng": {
                                    "area": "area12",
                                    "autoroute_exclude": 2,
                                    "interface": {
                                        "area": 13,
                                        "interface_type": "0/1",
                                    },
                                    "mesh_group": {
                                        "area": "area14",
                                        "id": 12,
                                        "interface": "GigabitEthernet0/1",
                                    },
                                    "multicast_intact": True,
                                    "router_id_interface": "0/1",
                                },
                            },
                            "neighbor": {
                                "address": "172.16.1.0",
                                "cost": 2,
                                "database_filter": True,
                                "poll_interval": 20,
                                "priority": 10,
                            },
                            "network": [
                                {
                                    "address": "198.51.100.0",
                                    "area": "5",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            ],
                            "nsf": {
                                "cisco": {
                                    "disable": True,
                                    "helper": True,
                                },
                                "ietf": {
                                    "disable": True,
                                    "helper": True,
                                    "strict_lsa_checking": True,
                                },
                            },
                            # "passive_interface": "GigabitEthernet0/1",
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "name": ["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                    "set_interface": False,
                                },
                            },
                            "prefix_suppression": True,
                            "priority": 10,
                            "process_id": 1,
                            "queue_depth": {
                                "hello": {
                                    "max_packets": 10,
                                    "unlimited": True,
                                },
                                "update": {
                                    "max_packets": 30,
                                    "unlimited": True,
                                },
                            },
                            "router_id": "router1",
                            "shutdown": True,
                            "summary_address": {
                                "address": "172.16.1.0",
                                "mask": "0.0.0.255",
                                "not_advertise": True,
                                "nssa_only": True,
                                "tag": 12,
                            },
                            "timers": {
                                "lsa": 12,
                                "pacing": {
                                    "flood": 25,
                                    "lsa_group": 15,
                                    "retransmission": 30,
                                },
                                "throttle": {
                                    "lsa": {
                                        "first_delay": 10,
                                        "max_delay": 20,
                                        "min_delay": 30,
                                    },
                                    "spf": {
                                        "between_delay": 10,
                                        "max_delay": 20,
                                        "receive_delay": 5,
                                    },
                                },
                            },
                            "traffic_share": True,
                            "ttl_security": {"hops": 12, "set": True},
                            "vrf": "vrf1",
                        },
                    ],
                },
                state="overridden",
            ),
        )

        commands = [
            "no router ospf 200 vrf blue",
            "router ospf 1 vrf vrf1",
            "adjacency stagger  none 2",
            "address-family ipv4 multicast",
            "topology base",
            "exit-address-family",
            "auto-cost reference-bandwidth 50",
            "bfd all-interfaces",
            "capability lls",
            "compatible rfc1583",
            "default-information originate always metric 25 metric-type 26 route-map rmap1",
            "default-metric 50",
            "discard-route external 5 internal 2",
            "domain-id 192.168.1.0 True",
            "domain-tag 54",
            "event-log one-shot pause size 10",
            "help",
            "ignore lsa mospf",
            "interface-id snmp-if-index",
            "ispf",
            "limit retransmissions dc 20 dc disable non-dc 10 non-dc disable",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "max-lsa 10 10 ignore-count 10 ignore-time 10 reset-time 10 warning-only",
            "max-metric router-lsa external-lsa 10 include-stub on-startup 110 summary-lsa 20",
            "maximum-paths 15",
            "neighbor 172.16.1.0 cost 2 database-filter all out poll-interval 20 priority 10",
            "network 198.51.100.0 0.0.0.255 area 5",
            "prefix-suppression",
            "priority 10",
            "router-id router1",
            "shutdown",
            "summary-address 172.16.1.0 0.0.0.255 not-advertise",
            "traffic-share min across-interfaces",
            "ttl-security all-interfaces hops 12",
            "area 5 authentication message-digest",
            "area 10 authentication message-digest",
            "area 10 capability default-exclusion",
            "area 10 default-cost 10",
            "area 10 nssa translate type7 suppress-fa",
            "area 10 nssa default-information-originate metric 10 metric-type 1 nssa-only no-ext-capability no-redistribution no-summary",
            "area 10 range 172.16.1.0 0.0.0.255 advertise cost 20",
            "area 10 sham-link checkSource checkDestination cost 10 ttl-security hops 20",
            "area 10 stub no-ext-capability no-summary",
            "area 10 filter-list prefix test_prefix_in in",
            "area 10 filter-list prefix test_prefix_out out",
            "passive-interface default",
            "no passive-interface GigabitEthernet0/1",
            "no passive-interface GigabitEthernet0/2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(commands, result["commands"])

    def test_ios_ospfv2_deleted(self):
        set_module_args(
            dict(config=dict(processes=[dict(process_id="200", vrf="blue")]), state="deleted"),
        )
        commands = ["no router ospf 200 vrf blue"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv2_parsed(self):
        set_module_args(
            dict(
                running_config="router ospf 1\n area 5 authentication\n area 5 capability default-exclusion",
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "processes": [
                {
                    "areas": [
                        {"area_id": "5", "authentication": {"enable": True}, "capability": True},
                    ],
                    "process_id": 1,
                },
            ],
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_ospfv2_rendered(self):
        set_module_args(
            dict(
                config={
                    "processes": [
                        {
                            "address_family": {
                                "default": True,
                                "snmp_context": "snmp_test",
                                "topology": {
                                    "base": True,
                                    "name": "test_topology",
                                    "tid": True,
                                },
                            },
                            "adjacency": {
                                "max_adjacency": 10,
                                "min_adjacency": 2,
                                "none": True,
                            },
                            "areas": [
                                {
                                    "area_id": "5",
                                    "authentication": {"enable": True, "message_digest": True},
                                },
                                {
                                    "area_id": "10",
                                    "authentication": {"enable": True, "message_digest": True},
                                    "capability": True,
                                    "default_cost": 10,
                                    "filter_list": [
                                        {"direction": "in", "name": "test_prefix_in"},
                                        {"direction": "out", "name": "test_prefix_out"},
                                    ],
                                    "nssa": {
                                        "default_information_originate": {
                                            "metric": 10,
                                            "metric_type": 1,
                                            "nssa_only": True,
                                        },
                                        "no_ext_capability": True,
                                        "no_redistribution": True,
                                        "no_summary": True,
                                        "set": True,
                                        "translate": "suppress-fa",
                                    },
                                    "ranges": [
                                        {
                                            "address": "172.16.1.0",
                                            "advertise": True,
                                            "cost": 20,
                                            "netmask": "0.0.0.255",
                                            "not_advertise": True,
                                        },
                                    ],
                                    "sham_link": {
                                        "cost": 10,
                                        "destination": "checkDestination",
                                        "source": "checkSource",
                                        "ttl_security": 20,
                                    },
                                    "stub": {
                                        "no_ext_capability": True,
                                        "no_summary": True,
                                        "set": True,
                                    },
                                },
                            ],
                            "auto_cost": {
                                "reference_bandwidth": 50,
                                "set": True,
                            },
                            "bfd": True,
                            "capability": {
                                "lls": True,
                                "opaque": True,
                                "transit": True,
                                "vrf_lite": True,
                            },
                            "compatible": {
                                "rfc1583": True,
                                "rfc1587": True,
                                "rfc5243": True,
                            },
                            "default_information": {
                                "always": True,
                                "metric": 25,
                                "metric_type": 26,
                                "originate": True,
                                "route_map": "rmap1",
                            },
                            "default_metric": "50",
                            "discard_route": {
                                "external": 5,
                                "internal": 2,
                                "set": True,
                            },
                            "distance": {
                                "admin_distance": {
                                    "acl": "acl1",
                                    "address": "192.168.1.0",
                                    "distance": 2,
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ospf": {
                                    "external": 1,
                                    "inter_area": 2,
                                    "intra_area": 3,
                                },
                            },
                            "domain_id": {
                                "ip_address": {
                                    "address": "192.168.1.0",
                                    "secondary": True,
                                },
                                "null": True,
                            },
                            "domain_tag": 54,
                            "event_log": {
                                "enable": True,
                                "one_shot": True,
                                "pause": True,
                                "size": 10,
                            },
                            "help": True,
                            "ignore": True,
                            "interface_id": True,
                            "ispf": True,
                            "limit": {
                                "dc": {
                                    "disable": True,
                                    "number": 20,
                                },
                                "non_dc": {
                                    "disable": True,
                                    "number": 10,
                                },
                            },
                            "local_rib_criteria": {
                                "enable": True,
                                "forwarding_address": True,
                                "inter_area_summary": True,
                                "nssa_translation": True,
                            },
                            "log_adjacency_changes": {"detail": True},
                            "max_lsa": {
                                "ignore_count": 10,
                                "ignore_time": 10,
                                "number": 10,
                                "reset_time": 10,
                                "threshold_value": 10,
                                "warning_only": True,
                            },
                            "max_metric": {
                                "external_lsa": 10,
                                "include_stub": True,
                                "on_startup": {"time": 110, "wait_for_bgp": True},
                                "router_lsa": True,
                                "summary_lsa": 20,
                            },
                            "maximum_paths": 15,
                            "mpls": {
                                "ldp": {
                                    "autoconfig": {
                                        "area": "area1",
                                        "set": True,
                                    },
                                    "sync": True,
                                },
                                "traffic_eng": {
                                    "area": "area12",
                                    "autoroute_exclude": 2,
                                    "interface": {
                                        "area": 13,
                                        "interface_type": "0/1",
                                    },
                                    "mesh_group": {
                                        "area": "area14",
                                        "id": 12,
                                        "interface": "GigabitEthernet0/1",
                                    },
                                    "multicast_intact": True,
                                    "router_id_interface": "0/1",
                                },
                            },
                            "neighbor": {
                                "address": "172.16.1.0",
                                "cost": 2,
                                "database_filter": True,
                                "poll_interval": 20,
                                "priority": 10,
                            },
                            "network": [
                                {
                                    "address": "198.51.100.0",
                                    "area": "5",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            ],
                            "nsf": {
                                "cisco": {
                                    "disable": True,
                                    "helper": True,
                                },
                                "ietf": {
                                    "disable": True,
                                    "helper": True,
                                    "strict_lsa_checking": True,
                                },
                            },
                            # "passive_interface": "GigabitEthernet0/1",
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "name": ["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                    "set_interface": False,
                                },
                            },
                            "prefix_suppression": True,
                            "priority": 10,
                            "process_id": 1,
                            "queue_depth": {
                                "hello": {
                                    "max_packets": 10,
                                    "unlimited": True,
                                },
                                "update": {
                                    "max_packets": 30,
                                    "unlimited": True,
                                },
                            },
                            "router_id": "router1",
                            "shutdown": True,
                            "summary_address": {
                                "address": "172.16.1.0",
                                "mask": "0.0.0.255",
                                "not_advertise": True,
                                "nssa_only": True,
                                "tag": 12,
                            },
                            "timers": {
                                "lsa": 12,
                                "pacing": {
                                    "flood": 25,
                                    "lsa_group": 15,
                                    "retransmission": 30,
                                },
                                "throttle": {
                                    "lsa": {
                                        "first_delay": 10,
                                        "max_delay": 20,
                                        "min_delay": 30,
                                    },
                                    "spf": {
                                        "between_delay": 10,
                                        "max_delay": 20,
                                        "receive_delay": 5,
                                    },
                                },
                            },
                            "traffic_share": True,
                            "ttl_security": {"hops": 12, "set": True},
                            "vrf": "vrf1",
                        },
                    ],
                },
                state="rendered",
            ),
        )
        commands = [
            "address-family ipv4 multicast",
            "adjacency stagger  none 2",
            "area 10 authentication message-digest",
            "area 10 capability default-exclusion",
            "area 10 default-cost 10",
            "area 10 filter-list prefix test_prefix_in in",
            "area 10 filter-list prefix test_prefix_out out",
            "area 10 nssa default-information-originate metric 10 metric-type 1 nssa-only no-ext-capability no-redistribution no-summary",
            "area 10 nssa translate type7 suppress-fa",
            "area 10 range 172.16.1.0 0.0.0.255 advertise cost 20",
            "area 10 sham-link checkSource checkDestination cost 10 ttl-security hops 20",
            "area 10 stub no-ext-capability no-summary",
            "area 5 authentication message-digest",
            "auto-cost reference-bandwidth 50",
            "bfd all-interfaces",
            "capability lls",
            "compatible rfc1583",
            "default-information originate always metric 25 metric-type 26 route-map rmap1",
            "default-metric 50",
            "discard-route external 5 internal 2",
            "domain-id 192.168.1.0 True",
            "domain-tag 54",
            "event-log one-shot pause size 10",
            "exit-address-family",
            "help",
            "ignore lsa mospf",
            "interface-id snmp-if-index",
            "ispf",
            "limit retransmissions dc 20 dc disable non-dc 10 non-dc disable",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "max-lsa 10 10 ignore-count 10 ignore-time 10 reset-time 10 warning-only",
            "max-metric router-lsa external-lsa 10 include-stub on-startup 110 summary-lsa 20",
            "maximum-paths 15",
            "neighbor 172.16.1.0 cost 2 database-filter all out poll-interval 20 priority 10",
            "network 198.51.100.0 0.0.0.255 area 5",
            "no passive-interface GigabitEthernet0/1",
            "no passive-interface GigabitEthernet0/2",
            "passive-interface default",
            "prefix-suppression",
            "priority 10",
            "router ospf 1 vrf vrf1",
            "router-id router1",
            "shutdown",
            "summary-address 172.16.1.0 0.0.0.255 not-advertise",
            "topology base",
            "traffic-share min across-interfaces",
            "ttl-security all-interfaces hops 12",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)
