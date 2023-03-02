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

    #
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

    def test_ios_ospfv2_overridden(self):
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
                state="overridden",
            ),
        )

        commands = [
            "router ospf 200 vrf blue",
            "no distribute-list 10 out",
            "no distribute-list 123 in",
            "domain-id 192.0.1.1",
            "max-metric router-lsa on-startup 200",
        ]
        self.execute_module(changed=True, commands=commands)

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
                config=dict(
                    {
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
                                        "authentication": {"enable": true, "message_digest": null},
                                        "capability": true,
                                        "default_cost": null,
                                        "filter_list": null,
                                        "nssa": null,
                                        "ranges": null,
                                        "sham_link": null,
                                        "stub": null,
                                    },
                                    {
                                        "area_id": "10",
                                        "authentication": {"enable": null, "message_digest": true},
                                        "capability": null,
                                        "default_cost": 10,
                                        "filter_list": [
                                            {"direction": "in", "name": "test_prefix_in"},
                                            {"direction": "out", "name": "test_prefix_out"},
                                        ],
                                        "nssa": {
                                            "default_information_originate": {
                                                "metric": 10,
                                                "metric_type": null,
                                                "nssa_only": null,
                                            },
                                            "no_ext_capability": null,
                                            "no_redistribution": null,
                                            "no_summary": null,
                                            "set": null,
                                            "translate": "suppress-fa",
                                        },
                                        "ranges": null,
                                        "sham_link": null,
                                        "stub": null,
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
                                "distribute_list": null,
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
                                "limit": null,
                                "local_rib_criteria": null,
                                "log_adjacency_changes": null,
                                "max_lsa": null,
                                "max_metric": {
                                    "external_lsa": null,
                                    "include_stub": null,
                                    "on_startup": {"time": 110, "wait_for_bgp": null},
                                    "router_lsa": true,
                                    "summary_lsa": null,
                                },
                                "maximum_paths": null,
                                "mpls": null,
                                "neighbor": null,
                                "network": [
                                    {
                                        "address": "198.51.100.0",
                                        "area": "5",
                                        "wildcard_bits": "0.0.0.255",
                                    }
                                ],
                                "nsf": null,
                                "passive_interface": null,
                                "passive_interfaces": {
                                    "default": true,
                                    "interface": {
                                        "name": ["GigabitEthernet0/1", "GigabitEthernet0/2"],
                                        "set_interface": false,
                                    },
                                },
                                "prefix_suppression": null,
                                "priority": null,
                                "process_id": 1,
                                "queue_depth": null,
                                "router_id": null,
                                "shutdown": null,
                                "summary_address": null,
                                "timers": null,
                                "traffic_share": null,
                                "ttl_security": null,
                                "vrf": null,
                            },
                            {
                                "address_family": null,
                                "adjacency": null,
                                "areas": [
                                    {
                                        "area_id": "10",
                                        "authentication": null,
                                        "capability": true,
                                        "default_cost": null,
                                        "filter_list": null,
                                        "nssa": null,
                                        "ranges": null,
                                        "sham_link": null,
                                        "stub": null,
                                    }
                                ],
                                "auto_cost": {"reference_bandwidth": 4, "set": null},
                                "bfd": null,
                                "capability": null,
                                "compatible": null,
                                "default_information": null,
                                "default_metric": null,
                                "discard_route": null,
                                "distance": null,
                                "distribute_list": {
                                    "acls": [
                                        {
                                            "direction": "out",
                                            "interface": null,
                                            "name": "10",
                                            "protocol": null,
                                        },
                                        {
                                            "direction": "in",
                                            "interface": null,
                                            "name": "123",
                                            "protocol": null,
                                        },
                                    ],
                                    "prefix": null,
                                    "route_map": null,
                                },
                                "domain_id": {
                                    "ip_address": {"address": "192.0.3.1", "secondary": null},
                                    "null": null,
                                },
                                "domain_tag": null,
                                "event_log": null,
                                "help": null,
                                "ignore": null,
                                "interface_id": null,
                                "ispf": null,
                                "limit": null,
                                "local_rib_criteria": null,
                                "log_adjacency_changes": null,
                                "max_lsa": null,
                                "max_metric": {
                                    "external_lsa": null,
                                    "include_stub": null,
                                    "on_startup": {"time": 100, "wait_for_bgp": null},
                                    "router_lsa": true,
                                    "summary_lsa": null,
                                },
                                "maximum_paths": null,
                                "mpls": null,
                                "neighbor": null,
                                "network": null,
                                "nsf": null,
                                "passive_interface": null,
                                "passive_interfaces": null,
                                "prefix_suppression": null,
                                "priority": null,
                                "process_id": 200,
                                "queue_depth": null,
                                "router_id": null,
                                "shutdown": null,
                                "summary_address": null,
                                "timers": null,
                                "traffic_share": null,
                                "ttl_security": null,
                                "vrf": "blue",
                            },
                        ]
                    }
                ),
                state="rendered",
            ),
        )
        commands = [
            "auto-cost reference-bandwidth 4",
            "distribute-list 10 out",
            "distribute-list 123 in",
            "domain-id 192.0.3.1",
            "max-metric router-lsa on-startup 100",
            "router ospf 100 vrf blue",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)
