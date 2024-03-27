#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_ospfv2
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosOspfV2Module(TestIosModule):
    module = ios_ospfv2

    def setUp(self):
        super(TestIosOspfV2Module, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv2.ospfv2."
            "Ospfv2Facts.get_ospfv2_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfV2Module, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_ospfv2_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
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
                                dict(
                                    address="198.51.100.0",
                                    wildcard_bits="0.0.0.255",
                                    area=5,
                                ),
                                dict(
                                    address="192.0.2.0",
                                    wildcard_bits="0.0.0.255",
                                    area=5,
                                ),
                            ],
                            domain_id=dict(ip_address=dict(address="192.0.3.1")),
                            max_metric=dict(on_startup=dict(time=100), router_lsa=True),
                            passive_interfaces=dict(
                                interface=dict(
                                    set_interface=False,
                                    name=["GigabitEthernet0/2"],
                                ),
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

    def test_ios_ospfv2_merged_specific_param(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
        set_module_args(
            dict(
                config={
                    "processes": [
                        {
                            "process_id": 1,
                            "router_id": "0.0.0.1",
                            "vrf": "vrf",
                            "areas": [{"area_id": 0}],
                            "capability": {"vrf_lite": True},
                        },
                    ],
                },
                state="merged",
            ),
        )
        commands = ["router ospf 1 vrf vrf", "capability vrf-lite", "router-id 0.0.0.1"]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv2_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
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
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
        set_module_args(
            dict(
                config={
                    "processes": [
                        {
                            "process_id": "200",
                            "auto_cost": {
                                "reference_bandwidth": "4",
                            },
                            "domain_id": {
                                "ip_address": {
                                    "address": "192.0.1.1",
                                },
                            },
                            "max_metric": {
                                "on_startup": {
                                    "time": 200,
                                },
                                "router_lsa": True,
                            },
                            "areas": [
                                {
                                    "area_id": "10",
                                    "capability": True,
                                },
                            ],
                            "vrf": "blue",
                        },
                    ],
                },
                state="replaced",
            ),
        )
        commands = [
            "router ospf 200 vrf blue",
            "auto-cost reference-bandwidth 4",
            "no distribute-list 123 in",
            "no distribute-list 10 out",
            "domain-id 192.0.1.1",
            "max-metric router-lsa on-startup 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv2_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
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
                                    "authentication": {
                                        "enable": True,
                                        "message_digest": True,
                                    },
                                },
                                {
                                    "area_id": "10",
                                    "authentication": {
                                        "enable": True,
                                        "message_digest": True,
                                    },
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
                                "opaque": False,
                                "transit": False,
                                "vrf_lite": False,
                            },
                            "compatible": {
                                "rfc1583": True,
                                "rfc1587": False,
                                "rfc5243": False,
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
                                },
                                "non_dc": {
                                    "disable": True,
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
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "name": [
                                        "GigabitEthernet0/1",
                                        "GigabitEthernet0/2",
                                    ],
                                    "set_interface": False,
                                },
                            },
                            "prefix_suppression": True,
                            "priority": 10,
                            "process_id": 1,
                            "queue_depth": {
                                "hello": {
                                    "max_packets": 10,
                                },
                                "update": {
                                    "max_packets": 30,
                                },
                            },
                            "router_id": "router1",
                            "shutdown": True,
                            "summary_address": {
                                "address": "172.16.1.0",
                                "mask": "0.0.0.255",
                                "nssa_only": True,
                                "tag": 12,
                            },
                            "timers": {
                                "lsa": 12,
                                "pacing": {
                                    "flood": 25,
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
            "adjacency stagger none 10",
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
            "distance 2 192.168.1.0 0.0.0.255 acl1",
            "distance ospf inter-area 2 intra-area 3 external 1",
            "domain-id 192.168.1.0 secondary",
            "domain-tag 54",
            "event-log one-shot pause size 10",
            "help",
            "ignore lsa mospf",
            "interface-id snmp-if-index",
            "ispf",
            "limit retransmissions dc disable non-dc disable",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "max-lsa 10 10 warning-only",
            "max-metric router-lsa external-lsa 10 include-stub on-startup 110 summary-lsa 20",
            "maximum-paths 15",
            "mpls ldp autoconfig area area1",
            "mpls traffic-eng area area12",
            "neighbor 172.16.1.0 cost 2 database-filter all out poll-interval 20 priority 10",
            "nsf cisco helper disable",
            "nsf ietf helper disable",
            "nsf ietf helper strict-lsa-checking",
            "prefix-suppression",
            "priority 10",
            "queue-depth hello 10",
            "queue-depth update 30",
            "router-id router1",
            "shutdown",
            "summary-address 172.16.1.0 0.0.0.255 nssa-only tag 12",
            "timers pacing flood 25",
            "traffic-share min across-interfaces",
            "ttl-security all-interfaces hops 12",
            "area 5 authentication message-digest",
            "area 10 authentication message-digest",
            "area 10 capability default-exclusion",
            "area 10 default-cost 10",
            "area 10 nssa default-information-originate metric 10 metric-type 1 nssa-only no-ext-capability no-redistribution no-summary",
            "area 10 nssa translate type7 suppress-fa",
            "area 10 sham-link checkSource checkDestination cost 10 ttl-security hops 20",
            "area 10 stub no-ext-capability no-summary",
            "area 10 filter-list prefix test_prefix_in in",
            "area 10 filter-list prefix test_prefix_out out",
            "area 10 range 172.16.1.0 0.0.0.255 not-advertise cost 20",
            "network 198.51.100.0 0.0.0.255 area 5",
            "passive-interface default",
            "no passive-interface GigabitEthernet0/1",
            "no passive-interface GigabitEthernet0/2",
        ]
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(commands, result["commands"])

    def test_ios_ospfv2_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
        set_module_args(
            dict(
                config=dict(processes=[dict(process_id="200", vrf="blue")]),
                state="deleted",
            ),
        )
        commands = ["no router ospf 200 vrf blue"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv2_parsed(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
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
                        {
                            "area_id": "5",
                            "authentication": {"enable": True},
                            "capability": True,
                        },
                    ],
                    "process_id": 1,
                },
            ],
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_ospfv2_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
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
                                    "authentication": {
                                        "enable": True,
                                        "message_digest": True,
                                    },
                                },
                                {
                                    "area_id": "10",
                                    "authentication": {
                                        "enable": True,
                                        "message_digest": True,
                                    },
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
                                "opaque": False,
                                "transit": False,
                                "vrf_lite": False,
                            },
                            "compatible": {
                                "rfc1583": True,
                                "rfc1587": False,
                                "rfc5243": False,
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
                                "warning_only": False,
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
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "name": [
                                        "GigabitEthernet0/1",
                                        "GigabitEthernet0/2",
                                    ],
                                    "set_interface": False,
                                },
                            },
                            "prefix_suppression": True,
                            "priority": 10,
                            "process_id": 1,
                            "queue_depth": {
                                "hello": {
                                    "unlimited": True,
                                },
                                "update": {
                                    "unlimited": True,
                                },
                            },
                            "router_id": "router1",
                            "shutdown": True,
                            "summary_address": {
                                "address": "172.16.1.0",
                                "mask": "0.0.0.255",
                                "nssa_only": True,
                                "tag": 12,
                            },
                            "timers": {
                                "lsa": 12,
                                "pacing": {
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
            "adjacency stagger none 10",
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
            "distance 2 192.168.1.0 0.0.0.255 acl1",
            "distance ospf inter-area 2 intra-area 3 external 1",
            "domain-id 192.168.1.0 secondary",
            "domain-tag 54",
            "event-log one-shot pause size 10",
            "exit-address-family",
            "help",
            "ignore lsa mospf",
            "interface-id snmp-if-index",
            "ispf",
            "limit retransmissions dc 20 non-dc 10",
            "local-rib-criteria forwarding-address inter-area-summary nssa-translation",
            "log-adjacency-changes detail",
            "max-lsa 10 10 ignore-count 10 ignore-time 10 reset-time 10",
            "max-metric router-lsa external-lsa 10 include-stub on-startup 110 summary-lsa 20",
            "maximum-paths 15",
            "mpls ldp sync",
            "mpls traffic-eng area area12",
            "neighbor 172.16.1.0 cost 2 database-filter all out poll-interval 20 priority 10",
            "network 198.51.100.0 0.0.0.255 area 5",
            "no passive-interface GigabitEthernet0/1",
            "no passive-interface GigabitEthernet0/2",
            "nsf cisco helper disable",
            "nsf ietf helper disable",
            "nsf ietf helper strict-lsa-checking",
            "passive-interface default",
            "prefix-suppression",
            "priority 10",
            "queue-depth hello unlimited",
            "queue-depth update unlimited",
            "router ospf 1 vrf vrf1",
            "router-id router1",
            "shutdown",
            "summary-address 172.16.1.0 0.0.0.255 nssa-only tag 12",
            "timers pacing retransmission 30",
            "topology base",
            "traffic-share min across-interfaces",
            "ttl-security all-interfaces hops 12",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), commands)

    def test_ios_ospfv2_overridden_2(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             area 10 filter-list prefix test_prefix_in in
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            router ospf 210 vrf green
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )

        set_module_args(
            dict(
                config={
                    "processes": [
                        {
                            "process_id": 200,
                            "vrf": "blue",
                            "auto_cost": {"set": True, "reference_bandwidth": 4},
                            "distribute_list": {
                                "acls": [
                                    {"name": "110", "direction": "out"},
                                    {"name": "123", "direction": "in"},
                                ],
                            },
                            "queue_depth": {
                                "hello": {
                                    "unlimited": True,
                                },
                                "update": {
                                    "unlimited": True,
                                },
                            },
                            "domain_id": {"null": True},
                            "timers": {
                                "pacing": {
                                    "lsa_group": 25,
                                },
                            },
                            "max_metric": {
                                "router_lsa": True,
                                "on_startup": {"time": 100},
                            },
                            "areas": [{"area_id": "10", "capability": True}],
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "set_interface": False,
                                    "name": [
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                },
                            },
                        },
                        {
                            "process_id": 210,
                            "vrf": "green",
                            "auto_cost": {"set": True, "reference_bandwidth": 5},
                            "distribute_list": {
                                "acls": [
                                    {"name": "5120", "direction": "out"},
                                    {"name": "123", "direction": "out"},
                                ],
                            },
                            "domain_id": {"ip_address": {"address": "192.0.3.1"}},
                            "nsf": {
                                "ietf": {
                                    "strict_lsa_checking": True,
                                },
                            },
                            "mpls": {
                                "ldp": {
                                    "sync": True,
                                },
                            },
                            "timers": {
                                "pacing": {
                                    "flood": 25,
                                },
                            },
                            "max_metric": {
                                "router_lsa": True,
                                "on_startup": {"wait_for_bgp": True},
                            },
                            "areas": [{"area_id": "11", "capability": True}],
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "set_interface": False,
                                    "name": ["GigabitEthernet0/2"],
                                },
                            },
                        },
                    ],
                },
                state="overridden",
            ),
        )

        result = self.execute_module(changed=True)
        print(result["commands"])
        commands = [
            "router ospf 200 vrf blue",
            "domain-id null",
            "queue-depth hello unlimited",
            "queue-depth update unlimited",
            "timers pacing lsa-group 25",
            "no area 10 filter-list prefix test_prefix_in in",
            "distribute-list 110 out",
            "no distribute-list 10 out",
            "router ospf 210 vrf green",
            "auto-cost reference-bandwidth 5",
            "max-metric router-lsa on-startup wait-for-bgp",
            "mpls ldp sync",
            "nsf ietf helper strict-lsa-checking",
            "timers pacing flood 25",
            "area 11 capability default-exclusion",
            "no area 10 capability default-exclusion",
            "distribute-list 5120 out",
            "no distribute-list 123 in",
            "distribute-list 123 out",
            "no distribute-list 10 out",
            "passive-interface GigabitEthernet0/1",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_ospfv2_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            router ospf 200 vrf blue
             auto-cost reference-bandwidth 4
             distribute-list 10 out
             distribute-list 123 in
             domain-id 192.0.3.1
             max-metric router-lsa on-startup 100
             area 10 capability default-exclusion
             passive-interface default
             no passive-interface GigabitEthernet0/1
             no passive-interface GigabitEthernet0/2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        {
                            "process_id": 200,
                            "vrf": "blue",
                            "auto_cost": {"set": True, "reference_bandwidth": 4},
                            "distribute_list": {
                                "acls": [
                                    {"name": "10", "direction": "out"},
                                    {"name": "123", "direction": "in"},
                                ],
                            },
                            "domain_id": {"ip_address": {"address": "192.0.3.1"}},
                            "max_metric": {
                                "router_lsa": True,
                                "on_startup": {"time": 100},
                            },
                            "areas": [{"area_id": "10", "capability": True}],
                            "passive_interfaces": {
                                "default": True,
                                "interface": {
                                    "set_interface": False,
                                    "name": [
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                },
                            },
                        },
                    ],
                ),
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])
