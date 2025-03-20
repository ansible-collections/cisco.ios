#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_evpn_ethernet
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosEvpnEthernetModule(TestIosModule):
    module = ios_evpn_ethernet

    def setUp(self):
        super(TestIosEvpnEthernetModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_ethernet.evpn_ethernet."
            "Evpn_ethernetFacts.get_evpn_ethernet_segment_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosEvpnEthernetModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_evpn_ethernet_idempotent_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn ethernet-segment 1
             identifier type 0 00.00.00.00.00.00.00.00.01
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 2
             identifier type 0 00.00.00.00.00.00.00.00.02
             redundancy single-active
             df-election preempt-time 1
            !
            l2vpn evpn ethernet-segment 3
             identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 4
             identifier type 0 00.00.00.00.00.00.00.00.04
             redundancy all-active
             df-election wait-time 1
            !
            """,
        )
        for state in ["merged", "overridden", "replaced", "rendered", "gathered"]:
            set_module_args(
                dict(
                    config=[
                        {
                            "segment": "1",
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.01",
                            },
                            "redundancy": {"single_active": True},
                        },
                        {
                            "segment": "2",
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.02",
                            },
                            "redundancy": {"single_active": True},
                            "df_election": {"preempt_time": 1},
                        },
                        {
                            "segment": "3",
                            "identifier": {
                                "identifier_type": "3",
                                "esi_value": "00.00.00.00.00.00.00.00.03",
                            },
                            "redundancy": {"single_active": True},
                        },
                        {
                            "segment": "4",
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.04",
                            },
                            "redundancy": {"all_active": True},
                            "df_election": {"wait_time": 1},
                        },
                    ],
                    state=state,
                ),
            )
            result = self.execute_module(changed=False)
            commands = {
                "rendered": [
                    "l2vpn evpn ethernet-segment 1",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.01",
                    "l2vpn evpn ethernet-segment 2",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.02",
                    "df-election preempt-time 1",
                    "l2vpn evpn ethernet-segment 3",
                    "redundancy single-active",
                    "identifier type 3 system-mac 00.00.00.00.00.00.00.00.03",
                    "l2vpn evpn ethernet-segment 4",
                    "redundancy all-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.04",
                    "df-election wait-time 1",
                ],
                "gathered": [
                    {
                        "segment": "1",
                        "identifier": {
                            "identifier_type": "0",
                            "esi_value": "00.00.00.00.00.00.00.00.01",
                        },
                        "redundancy": {"single_active": True},
                    },
                    {
                        "segment": "2",
                        "identifier": {
                            "identifier_type": "0",
                            "esi_value": "00.00.00.00.00.00.00.00.02",
                        },
                        "redundancy": {"single_active": True},
                        "df_election": {"preempt_time": 1},
                    },
                    {
                        "segment": "3",
                        "identifier": {
                            "identifier_type": "3",
                            "esi_value": "00.00.00.00.00.00.00.00.03",
                        },
                        "redundancy": {"single_active": True},
                    },
                    {
                        "segment": "4",
                        "identifier": {
                            "identifier_type": "0",
                            "esi_value": "00.00.00.00.00.00.00.00.04",
                        },
                        "redundancy": {"all_active": True},
                        "df_election": {"wait_time": 1},
                    },
                ],
            }

            if state in ["rendered", "gathered"]:
                self.assertEqual(result[state], commands.get(state))
            else:
                self.assertEqual(result["commands"], [])

    def test_ios_evpn_ethernet_action_states(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn ethernet-segment 1
             identifier type 0 00.00.00.00.00.00.00.00.01
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 2
             identifier type 0 00.00.00.00.00.00.00.00.02
             redundancy single-active
             df-election preempt-time 1
            !
            l2vpn evpn ethernet-segment 3
             identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 4
             identifier type 0 00.00.00.00.00.00.00.00.04
             redundancy all-active
             df-election wait-time 1
            !
            """,
        )
        for state in [
            "merged",
            "replaced",
            "overridden",
        ]:
            set_module_args(
                dict(
                    config=[
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.01",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "1",
                        },
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.05",
                            },
                            "redundancy": {"all_active": True},
                            "segment": "5",
                        },
                        {
                            "df_election": {"preempt_time": 10},
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.06",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "6",
                        },
                    ],
                    state=state,
                ),
            )
            result = self.execute_module(changed=True)
            commands = {
                "merged": [
                    "l2vpn evpn ethernet-segment 6",
                    "df-election preempt-time 10",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.06",
                    "l2vpn evpn ethernet-segment 5",
                    "redundancy all-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.05",
                ],
                "overridden": [
                    "no l2vpn evpn ethernet-segment 2",
                    "no l2vpn evpn ethernet-segment 3",
                    "no l2vpn evpn ethernet-segment 4",
                    "l2vpn evpn ethernet-segment 5",
                    "redundancy all-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.05",
                    "l2vpn evpn ethernet-segment 6",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.06",
                    "df-election preempt-time 10",
                ],
                "replaced": [
                    "l2vpn evpn ethernet-segment 5",
                    "redundancy all-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.05",
                    "l2vpn evpn ethernet-segment 6",
                    "df-election preempt-time 10",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.06",
                ],
            }
            self.assertEqual(sorted(result["commands"]), sorted(commands.get(state)))

    def test_ios_evpn_ethernet_deleted_and_purged_states(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn ethernet-segment 1
             identifier type 0 00.00.00.00.00.00.00.00.01
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 2
             identifier type 0 00.00.00.00.00.00.00.00.02
             redundancy single-active
             df-election preempt-time 1
            !
            l2vpn evpn ethernet-segment 3
             identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 4
             identifier type 0 00.00.00.00.00.00.00.00.04
             redundancy all-active
             df-election wait-time 1
            !
            """,
        )
        for state in [
            "deleted",
            "purged",
        ]:
            set_module_args(
                dict(
                    config=[
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.01",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "1",
                        },
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.05",
                            },
                            "redundancy": {"all_active": True},
                            "segment": "5",
                        },
                        {
                            "df_election": {"preempt_time": 10},
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.06",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "6",
                        },
                    ],
                    state=state,
                ),
            )
            result = self.execute_module(changed=True)
            commands = {
                "deleted": [
                    "l2vpn evpn ethernet-segment 1",
                    "no redundancy single-active",
                    "no identifier type 0 00.00.00.00.00.00.00.00.01",
                ],
                "purged": [
                    "no l2vpn evpn ethernet-segment 1",
                    "no l2vpn evpn ethernet-segment 2",
                    "no l2vpn evpn ethernet-segment 3",
                    "no l2vpn evpn ethernet-segment 4",
                ],
            }
            self.assertEqual(result["commands"], commands.get(state))

    def test_ios_evpn_ethernet_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    l2vpn evpn ethernet-segment 1
                     identifier type 0 00.00.00.00.00.00.00.00.01
                     redundancy single-active
                    !
                    l2vpn evpn ethernet-segment 2
                     identifier type 0 00.00.00.00.00.00.00.00.02
                     redundancy single-active
                     df-election preempt-time 1
                    !
                    l2vpn evpn ethernet-segment 3
                     identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
                     redundancy single-active
                    !
                    l2vpn evpn ethernet-segment 4
                     identifier type 0 00.00.00.00.00.00.00.00.04
                     redundancy all-active
                     df-election wait-time 1
                    !
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "segment": "1",
                "identifier": {
                    "identifier_type": "0",
                    "esi_value": "00.00.00.00.00.00.00.00.01",
                },
                "redundancy": {"single_active": True},
            },
            {
                "segment": "2",
                "identifier": {
                    "identifier_type": "0",
                    "esi_value": "00.00.00.00.00.00.00.00.02",
                },
                "redundancy": {"single_active": True},
                "df_election": {"preempt_time": 1},
            },
            {
                "segment": "3",
                "identifier": {
                    "identifier_type": "3",
                    "esi_value": "00.00.00.00.00.00.00.00.03",
                },
                "redundancy": {"single_active": True},
            },
            {
                "segment": "4",
                "identifier": {
                    "identifier_type": "0",
                    "esi_value": "00.00.00.00.00.00.00.00.04",
                },
                "redundancy": {"all_active": True},
                "df_election": {"wait_time": 1},
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_evpn_ethernet_overridden_only(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn ethernet-segment 1
             identifier type 0 00.00.00.00.00.00.00.00.01
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 2
             identifier type 0 00.00.00.00.00.00.00.00.02
             redundancy single-active
             df-election preempt-time 1
            !
            l2vpn evpn ethernet-segment 3
             identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
             redundancy single-active
            !
            l2vpn evpn ethernet-segment 4
             identifier type 0 00.00.00.00.00.00.00.00.04
             redundancy all-active
             df-election wait-time 1
            !
            """,
        )
        for state in [
            "overridden",
        ]:
            set_module_args(
                dict(
                    config=[
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.01",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "1",
                        },
                        {
                            "segment": "2",
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.02",
                            },
                            "redundancy": {"single_active": True},
                            "df_election": {"preempt_time": 5},
                        },
                        {
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.05",
                            },
                            "redundancy": {"all_active": True},
                            "segment": "5",
                        },
                        {
                            "df_election": {"preempt_time": 10},
                            "identifier": {
                                "identifier_type": "0",
                                "esi_value": "00.00.00.00.00.00.00.00.06",
                            },
                            "redundancy": {"single_active": True},
                            "segment": "6",
                        },
                    ],
                    state=state,
                ),
            )
            result = self.execute_module(changed=True)
            commands = {
                "overridden": [
                    "no l2vpn evpn ethernet-segment 3",
                    "no l2vpn evpn ethernet-segment 4",
                    "l2vpn evpn ethernet-segment 2",
                    "df-election preempt-time 5",
                    "l2vpn evpn ethernet-segment 5",
                    "redundancy all-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.05",
                    "l2vpn evpn ethernet-segment 6",
                    "redundancy single-active",
                    "identifier type 0 00.00.00.00.00.00.00.00.06",
                    "df-election preempt-time 10",
                ],
            }
            self.assertEqual(sorted(result["commands"]), sorted(commands.get(state)))
