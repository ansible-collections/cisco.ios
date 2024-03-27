#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_ospf_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosOspfInterfacesModule(TestIosModule):
    module = ios_ospf_interfaces

    def setUp(self):
        super(TestIosOspfInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospf_interfaces.ospf_interfaces."
            "Ospf_interfacesFacts.get_ospf_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_ospf_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=30),
                                network=dict(broadcast=True),
                                priority=60,
                                resync_timeout=90,
                                ttl_security=dict(hops=120),
                                authentication=dict(key_chain="test_key"),
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                dead_interval=dict(time=100),
                                network=dict(manet=True),
                                priority=50,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "ip ospf authentication key-chain test_key",
            "ip ospf bfd",
            "ip ospf network broadcast",
            "ip ospf priority 60",
            "ip ospf resync-timeout 90",
            "ip ospf ttl-security hops 120",
            "ipv6 ospf bfd",
            "ipv6 ospf dead-interval 100",
            "ipv6 ospf network manet",
            "ipv6 ospf priority 50",
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_ospf_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(hops=50),
                            ),
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            ),
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
            "no ipv6 ospf 55 area 105",
            "no ipv6 ospf adjacency stagger disable",
            "no ipv6 ospf priority 20",
            "no ipv6 ospf transmit-delay 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(set=True, hops=50),
                            ),
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            ),
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                manet=dict(cost=dict(percent=10)),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                transmit_delay=50,
                            ),
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "no ip ospf 10 area 20",
            "no ip ospf adjacency stagger disable",
            "no ip ospf cost 30",
            "no ip ospf priority 40",
            "no ip ospf ttl-security hops 50",
            "interface GigabitEthernet0/3",
            "ipv6 ospf 10 area 20",
            "no ipv6 ospf adjacency stagger disable",
            "ipv6 ospf manet peering cost percent 10",
            "ipv6 ospf priority 40",
            "ipv6 ospf transmit-delay 50" "",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(set=True, hops=50),
                            ),
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            ),
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_deleted_interface(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(dict(config=[dict(name="GigabitEthernet0/2")], state="deleted"))
        commands = [
            "interface GigabitEthernet0/2",
            "no ip ospf priority 40",
            "no ip ospf adjacency stagger disable",
            "no ip ospf ttl-security hops 50",
            "no ip ospf 10 area 20",
            "no ip ospf cost 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface GigabitEthernet0/3",
            "no ipv6 ospf 55 area 105",
            "no ipv6 ospf adjacency stagger disable",
            "no ipv6 ospf priority 20",
            "no ipv6 ospf transmit-delay 30",
            "interface GigabitEthernet0/2",
            "no ip ospf 10 area 20",
            "no ip ospf adjacency stagger disable",
            "no ip ospf cost 30",
            "no ip ospf priority 40",
            "no ip ospf ttl-security hops 50",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=30),
                                network=dict(broadcast=True),
                                dead_interval=dict(time=20, minimal=100),
                                demand_circuit=dict(enable=True, ignore=True),
                                multi_area=dict(id=15, cost=20),
                                priority=60,
                                resync_timeout=90,
                                authentication=dict(
                                    key_chain="thekeychain",
                                    message_digest=True,
                                    null=True,
                                ),
                                ttl_security=dict(hops=120),
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                dead_interval=dict(time=100),
                                demand_circuit=dict(enable=True, ignore=True),
                                network=dict(manet=True),
                                neighbor=dict(
                                    address="10.0.2.15",
                                    cost=14,
                                    database_filter=True,
                                    # poll_interval=13,
                                    # priority=56,
                                ),
                                priority=50,
                                authentication=dict(
                                    key_chain="thekeychain",
                                    message_digest=True,
                                    null=True,
                                ),
                                cost=dict(
                                    interface_cost=10,
                                    dynamic_cost=dict(
                                        default=10,
                                        hysteresis=dict(
                                            percent=15,
                                            threshold=25,
                                        ),
                                        weight=dict(
                                            l2_factor=12,
                                            latency=14,
                                            oc=True,
                                            resources=13,
                                            throughput=56,
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet0/2",
            "ip ospf bfd",
            "ip ospf cost 30",
            "ip ospf dead-interval 20 minimal hello-multiplier 100",
            "ip ospf demand-circuit ignore",
            "ip ospf multi-area 15 cost 20",
            "ip ospf network broadcast",
            "ip ospf priority 60",
            "ip ospf resync-timeout 90",
            "ip ospf ttl-security hops 120",
            "ipv6 ospf bfd",
            "ipv6 ospf cost 10",
            "ipv6 ospf dead-interval 100",
            "ipv6 ospf demand-circuit ignore",
            "ipv6 ospf neighbor 10.0.2.15 cost 14 database-filter all out",
            "ipv6 ospf network manet",
            "ipv6 ospf priority 50",
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    def test_ios_ospf_interfaces_parsed(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/2
             ip ospf priority 40
             ip ospf adjacency stagger disable
             ip ospf ttl-security hops 50
             ip ospf 10 area 20
             ip ospf cost 30
            interface GigabitEthernet0/3
             ipv6 ospf 55 area 105
             ipv6 ospf priority 20
             ipv6 ospf transmit-delay 30
             ipv6 ospf adjacency stagger disable
            """,
        )
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet0/0
                     ip ospf dead-interval 10
                    interface GigabitEthernet0/1
                     ip ospf network broadcast
                     ip ospf resync-timeout 10
                     ip ospf dead-interval 5
                     ip ospf priority 25
                     ip ospf demand-circuit ignore
                     ip ospf bfd
                     ip ospf adjacency stagger disable
                     ip ospf ttl-security hops 50
                     ip ospf shutdown
                     ip ospf 10 area 30
                     ip ospf cost 5
                     ipv6 ospf 35 area 45
                     ipv6 ospf priority 55
                     ipv6 ospf transmit-delay 45
                     ipv6 ospf database-filter all out
                     ipv6 ospf adjacency stagger disable
                     ipv6 ospf manet peering link-metrics 10
                    interface GigabitEthernet0/2
                     ip ospf dead-interval minimal hello-multiplier 10
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "GigabitEthernet0/0",
                "address_family": [{"afi": "ipv4", "dead_interval": {"time": 10}}],
            },
            {
                "name": "GigabitEthernet0/1",
                "address_family": [
                    {
                        "afi": "ipv4",
                        "network": {"broadcast": True},
                        "resync_timeout": 10,
                        "dead_interval": {"time": 5},
                        "priority": 25,
                        "demand_circuit": {"enable": True, "ignore": True},
                        "bfd": True,
                        "adjacency": True,
                        "ttl_security": {"set": True, "hops": 50},
                        "shutdown": True,
                        "process": {"id": 10, "area_id": "30"},
                        "cost": {"interface_cost": 5},
                    },
                    {
                        "afi": "ipv6",
                        "process": {"id": 35, "area_id": "45"},
                        "priority": 55,
                        "transmit_delay": 45,
                        "database_filter": True,
                        "adjacency": True,
                        "manet": {"link_metrics": {"cost_threshold": 10}},
                    },
                ],
            },
            {
                "name": "GigabitEthernet0/2",
                "address_family": [{"afi": "ipv4", "dead_interval": {"minimal": 10}}],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])
