#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_bgp_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosBgpGlobalModule(TestIosModule):
    module = ios_bgp_global

    def setUp(self):
        super(TestIosBgpGlobalModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_global.bgp_global."
            "Bgp_globalFacts.get_bgp_global_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBgpGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_bgp_global.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_bgp_global_merged(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        dampening=dict(
                            penalty_half_time=1,
                            reuse_route_val=1,
                            suppress_route_val=1,
                            max_suppress=1,
                        ),
                        graceful_shutdown=dict(
                            neighbors=dict(time=50),
                            community=100,
                            local_preference=100,
                        ),
                    ),
                    neighbor=[
                        dict(
                            address="198.51.100.1",
                            description="merge neighbor",
                            aigp=dict(
                                send=dict(
                                    cost_community=dict(
                                        id=100,
                                        poi=dict(
                                            igp_cost=True, transitive=True
                                        ),
                                    )
                                )
                            ),
                        )
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "router bgp 65000",
            "bgp graceful-shutdown all neighbors 50 local-preference 100 community 100",
            "bgp dampening 1 1 1 1",
            "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
            "neighbor 198.51.100.1 description merge neighbor",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_global_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath=[dict(compare_routerid=True)],
                        nopeerup_delay=[dict(post_boot=10)],
                    ),
                    redistribute=[dict(connected=dict(metric=10))],
                    neighbor=[
                        dict(
                            address="198.51.100.1",
                            remote_as=100,
                            route_map=dict(name="test-route", out=True),
                        )
                    ],
                    timers=dict(keepalive=100, holdtime=200, min_holdtime=150),
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    # def test_ios_bgp_global_replaced(self):
    #     set_module_args(
    #         dict(
    #             config=dict(
    #                 processes=[
    #                     dict(
    #                         process_id="1",
    #                         max_metric=dict(
    #                             router_lsa=True, on_startup=dict(time=100)
    #                         ),
    #                         address_family=[
    #                             dict(
    #                                 afi="ipv4",
    #                                 unicast=True,
    #                                 vrf="blue",
    #                                 adjacency=dict(
    #                                     min_adjacency=100, max_adjacency=100
    #                                 ),
    #                             )
    #                         ],
    #                     )
    #                 ]
    #             ),
    #             state="replaced",
    #         )
    #     )
    #     commands = [
    #         "router ospfv3 1",
    #         "max-metric router-lsa on-startup 100",
    #         "no area 10 nssa default-information-originate metric 10",
    #         "address-family ipv4 unicast vrf blue",
    #         "adjacency stagger 100 100",
    #         "exit-address-family",
    #     ]
    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    #
    def test_ios_bgp_global_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        advertise_best_external=True,
                        bestpath=[dict(compare_routerid=True)],
                        nopeerup_delay=[dict(post_boot=10)],
                    ),
                    redistribute=[dict(connected=dict(metric=10))],
                    neighbor=[
                        dict(
                            address="198.51.100.1",
                            remote_as=100,
                            route_map=dict(name="test-route", out=True),
                        )
                    ],
                    timers=dict(keepalive=100, holdtime=200, min_holdtime=150),
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_global_deleted(self):
        set_module_args(dict(config=dict(as_number=65000), state="deleted"))
        commands = [
            "router bgp 65000",
            "no bgp nopeerup-delay post-boot 10",
            "no bgp bestpath compare-routerid",
            "no bgp advertise-best-external",
            "no timers bgp 100 200 150",
            "no redistribute connected metric 10",
            "no neighbor 198.51.100.1 remote-as 100",
            "no neighbor 198.51.100.1 route-map test-route out",
        ]
        # self.execute_module(changed=True, commands=commands)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_bgp_global_purged(self):
    #     set_module_args(
    #         dict(
    #             config=dict(as_number=65000), state="deleted"
    #         )
    #     )
    #     commands = ["no router bgp 65000"]
    #     self.execute_module(changed=True, commands=commands)

    def test_ios_bgp_global_parsed(self):
        set_module_args(
            dict(
                running_config="router bgp 65000\n bgp nopeerup-delay post-boot 10",
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "as_number": "65000",
            "bgp": {"nopeerup_delay": [{"post_boot": 10}]},
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_bgp_global_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    bgp=dict(
                        dampening=dict(
                            penalty_half_time=1,
                            reuse_route_val=1,
                            suppress_route_val=1,
                            max_suppress=1,
                        ),
                        graceful_shutdown=dict(
                            neighbors=dict(time=50),
                            community=100,
                            local_preference=100,
                        ),
                    ),
                    neighbor=[
                        dict(
                            address="198.51.100.1",
                            description="merge neighbor",
                            aigp=dict(
                                send=dict(
                                    cost_community=dict(
                                        id=100,
                                        poi=dict(
                                            igp_cost=True, transitive=True
                                        ),
                                    )
                                )
                            ),
                        )
                    ],
                ),
                state="rendered",
            )
        )
        commands = [
            "router bgp 65000",
            "bgp dampening 1 1 1 1",
            "bgp graceful-shutdown all neighbors 50 local-preference 100 community 100",
            "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
            "neighbor 198.51.100.1 description merge neighbor",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)
