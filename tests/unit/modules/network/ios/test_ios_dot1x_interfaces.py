# (c) 2026 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import time

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_dot1x_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


PORT_BLOCK = """\
interface GigabitEthernet1/0/{n}
 switchport access vlan 10
 switchport mode access
 authentication control-direction in
 authentication event fail retry 2 action authorize vlan 999
 authentication event server dead action authorize vlan 20
 authentication event no-response action authorize vlan 30
 authentication event server alive action reinitialize
 authentication port-control auto
 authentication periodic
 authentication timer reauthenticate server
 authentication violation restrict
 mab
 dot1x pae authenticator
 dot1x timeout tx-period 7
 spanning-tree portfast
 ip dhcp snooping limit rate 100
"""

RUNNING = PORT_BLOCK.format(n=1) + dedent(
    """\
        interface GigabitEthernet1/0/2
         switchport access vlan 10
        interface GigabitEthernet1/0/3
         authentication host-mode multi-auth
         authentication order mab dot1x
         authentication priority mab dot1x
         authentication event fail action next-method
         mab
        """,
)

PORT1 = {
    "name": "GigabitEthernet1/0/1",
    "mab": True,
    "dot1x": {"pae": "authenticator", "timeout": {"tx_period": 7}},
    "authentication": {
        "port_control": "auto",
        "periodic": True,
        "timer": {"reauthenticate": {"server": True}},
        "violation": "restrict",
        "control_direction": "in",
        "event": {
            "fail": {"retry": 2, "action": "authorize", "vlan": 999},
            "no_response": {"vlan": 30},
            "server_dead": {"action": "authorize", "vlan": 20},
            "server_alive": {"action": "reinitialize"},
        },
    },
}
PORT3 = {
    "name": "GigabitEthernet1/0/3",
    "mab": True,
    "authentication": {
        "host_mode": "multi_auth",
        "order": ["mab", "dot1x"],
        "priority": ["mab", "dot1x"],
        "event": {"fail": {"action": "next_method"}},
    },
}
PORT1_COMMANDS = [
    "authentication port-control auto",
    "authentication periodic",
    "authentication timer reauthenticate server",
    "authentication violation restrict",
    "authentication control-direction in",
    "authentication event fail action authorize vlan 999",
    "authentication event no-response action authorize vlan 30",
    "authentication event server dead action authorize vlan 20",
    "authentication event server alive action reinitialize",
    "mab",
    "dot1x pae authenticator",
    "dot1x timeout tx-period 7",
]
PORT3_REMOVED = [
    "no authentication host-mode multi-auth",
    "no authentication order mab dot1x",
    "no authentication priority mab dot1x",
    "no authentication event fail action next-method",
    "no mab",
]


class TestIosDot1xInterfacesModule(TestIosModule):
    module = ios_dot1x_interfaces

    def setUp(self):
        super(TestIosDot1xInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.dot1x_interfaces.dot1x_interfaces."
            "Dot1x_interfacesFacts.get_dot1x_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosDot1xInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True, failed=False):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def test_ios_dot1x_interfaces_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        # GigabitEthernet1/0/2 has none of the options, the switchport and spanning-tree lines are not ours
        self.assertEqual(result["parsed"], [PORT1, PORT3])

    def test_ios_dot1x_interfaces_gathered(self):
        self.execute_show_command.return_value = RUNNING
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], [PORT1, PORT3])

    def test_ios_dot1x_interfaces_parsed_other_blocks_do_not_end_up_on_an_interface(self):
        # the children of a bfd-template or of an interface template look the same
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    interface GigabitEthernet1/0/1
                     mab
                    bfd-template single-hop BFD1
                     authentication sha-1 keychain KEYS
                    template ACCESS
                     authentication port-control auto
                     dot1x pae authenticator
                    interface GigabitEthernet1/0/2
                     description uplink
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], [{"name": "GigabitEthernet1/0/1", "mab": True}])

    def test_ios_dot1x_interfaces_parsed_variants(self):
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    interface GigabitEthernet1/0/1
                     mab eap
                     authentication port-control force-authorized
                     authentication timer reauthenticate 3600
                     authentication host-mode multi-domain
                     authentication event server dead action reinitialize vlan 20
                     dot1x max-reauth-req 3
                    interface GigabitEthernet1/0/2
                     authentication event server dead action authorize voice
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "name": "GigabitEthernet1/0/1",
                    "mab": True,
                    "dot1x": {"max_reauth_req": 3},
                    "authentication": {
                        "port_control": "force_authorized",
                        "timer": {"reauthenticate": {"seconds": 3600}},
                        "host_mode": "multi_domain",
                        "event": {"server_dead": {"action": "reinitialize", "vlan": 20}},
                    },
                },
                {
                    "name": "GigabitEthernet1/0/2",
                    "authentication": {
                        "event": {"server_dead": {"action": "authorize", "voice": True}},
                    },
                },
            ],
        )

    def test_ios_dot1x_interfaces_merged(self):
        result = self._run("", {"config": [PORT1], "state": "merged"})
        self.assertEqual(result["commands"], ["interface GigabitEthernet1/0/1"] + PORT1_COMMANDS)

    def test_ios_dot1x_interfaces_merged_idempotent_with_a_short_name(self):
        port = dict(PORT1, name="Gi1/0/1")
        result = self._run(RUNNING, {"config": [port, PORT3], "state": "merged"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_interfaces_merged_keeps_what_is_not_in_the_task(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {"name": "GigabitEthernet1/0/1", "authentication": {"violation": "shutdown"}},
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["interface GigabitEthernet1/0/1", "authentication violation shutdown"],
        )

    def test_ios_dot1x_interfaces_merged_replaces_a_command_line_as_a_whole(self):
        # "authorize voice" must not keep the vlan of the line on the device
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "authentication": {
                            "event": {"server_dead": {"action": "authorize", "voice": True}},
                            "timer": {"reauthenticate": {"seconds": 600}},
                        },
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "authentication timer reauthenticate 600",
                "authentication event server dead action authorize voice",
            ],
        )

    def test_ios_dot1x_interfaces_merged_order_is_replaced_and_keeps_its_order(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {"name": "GigabitEthernet1/0/3", "authentication": {"order": ["dot1x", "mab"]}},
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["interface GigabitEthernet1/0/3", "authentication order dot1x mab"],
        )

    def test_ios_dot1x_interfaces_merged_false_turns_a_flag_off(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "mab": False,
                        "authentication": {"periodic": False},
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["interface GigabitEthernet1/0/1", "no authentication periodic", "no mab"],
        )

    def test_ios_dot1x_interfaces_replaced_removes_what_is_not_in_the_task(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "mab": True,
                        "dot1x": {"pae": "authenticator"},
                        "authentication": {"port_control": "auto", "host_mode": "multi_auth"},
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "no authentication periodic",
                "no authentication timer reauthenticate server",
                "no authentication violation restrict",
                "no authentication control-direction in",
                "authentication host-mode multi-auth",
                "no authentication event fail action authorize vlan 999",
                "no authentication event no-response action authorize vlan 30",
                "no authentication event server dead action authorize vlan 20",
                "no authentication event server alive action reinitialize",
                "no dot1x timeout tx-period 7",
            ],
        )

    def test_ios_dot1x_interfaces_replaced_idempotent_and_leaves_other_interfaces(self):
        result = self._run(RUNNING, {"config": [PORT1], "state": "replaced"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_interfaces_overridden(self):
        result = self._run(RUNNING, {"config": [PORT1], "state": "overridden"})
        self.assertEqual(result["commands"], ["interface GigabitEthernet1/0/3"] + PORT3_REMOVED)

    def test_ios_dot1x_interfaces_deleted_one_interface(self):
        result = self._run(
            RUNNING,
            {"config": [{"name": "Gi1/0/3"}, {"name": "GigabitEthernet1/0/9"}], "state": "deleted"},
        )
        self.assertEqual(result["commands"], ["interface GigabitEthernet1/0/3"] + PORT3_REMOVED)

    def test_ios_dot1x_interfaces_deleted_all(self):
        result = self._run(RUNNING, {"state": "deleted"})
        self.assertEqual(result["commands"].count("interface GigabitEthernet1/0/1"), 1)
        self.assertEqual(result["commands"].count("interface GigabitEthernet1/0/3"), 1)
        self.assertNotIn("interface GigabitEthernet1/0/2", result["commands"])
        self.assertIn("no dot1x pae authenticator", result["commands"])

    def test_ios_dot1x_interfaces_deleted_all_empty_device(self):
        result = self._run(
            "interface GigabitEthernet1/0/2\n switchport access vlan 10\n",
            {"state": "deleted"},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_interfaces_rendered(self):
        set_module_args(
            {
                "config": [
                    {
                        "name": "Gi1/0/2",
                        "mab": True,
                        "authentication": {"order": ["mab", "dot1x"], "priority": ["mab", "dot1x"]},
                    },
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "interface GigabitEthernet1/0/2",
                "authentication order mab dot1x",
                "authentication priority mab dot1x",
                "mab",
            ],
        )

    def test_ios_dot1x_interfaces_validation(self):
        cases = (
            ({"event": {"fail": {"action": "authorize"}}}, "action authorize needs a vlan"),
            ({"event": {"fail": {"action": "next_method", "vlan": 5}}}, "does not take a vlan"),
            ({"event": {"server_dead": {"action": "reinitialize"}}}, "reinitialize needs a vlan"),
            (
                {"event": {"server_dead": {"action": "reinitialize", "vlan": 5, "voice": True}}},
                "takes no voice",
            ),
            (
                {"event": {"server_dead": {"action": "authorize"}}},
                "authorize needs a vlan or voice",
            ),
            ({"timer": {"reauthenticate": {"server": True, "seconds": 5}}}, "mutually exclusive"),
        )
        for authentication, expected in cases:
            result = self._run(
                "",
                {
                    "config": [{"name": "Gi1/0/1", "authentication": authentication}],
                    "state": "merged",
                },
                failed=True,
            )
            self.assertIn(expected, result["msg"])

    def test_ios_dot1x_interfaces_parsed_tolerates_trailing_whitespace(self):
        # the device prints "authentication event server alive action reinitialize " with a space at the end
        set_module_args(
            {
                "running_config": "interface GigabitEthernet1/0/1\n"
                " authentication event server alive action reinitialize \n"
                " authentication port-control auto  \n mab \n",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "name": "GigabitEthernet1/0/1",
                    "mab": True,
                    "authentication": {
                        "port_control": "auto",
                        "event": {"server_alive": {"action": "reinitialize"}},
                    },
                },
            ],
        )

    def test_ios_dot1x_interfaces_the_default_of_an_option_is_not_printed_so_it_is_not_a_change(
        self,
    ):
        # IOS does not print what is the default: violation shutdown, port-control force-authorized,
        # control-direction both, host-mode single-host, tx-period 30, max-reauth-req 2, fail retry 2
        result = self._run(
            "interface GigabitEthernet1/0/1\n mab\n authentication event fail action authorize vlan 999\n",
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "mab": True,
                        "dot1x": {"timeout": {"tx_period": 30}, "max_reauth_req": 2},
                        "authentication": {
                            "violation": "shutdown",
                            "port_control": "force_authorized",
                            "control_direction": "both",
                            "host_mode": "single_host",
                            "timer": {"reauthenticate": {"seconds": 3600}},
                            "event": {"fail": {"retry": 2, "action": "authorize", "vlan": 999}},
                        },
                    },
                ],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_interfaces_the_default_is_a_change_on_a_port_that_has_something_else(self):
        result = self._run(
            "interface GigabitEthernet1/0/1\n authentication violation restrict\n authentication port-control auto\n",
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "authentication": {
                            "violation": "shutdown",
                            "port_control": "force_authorized",
                        },
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "authentication port-control force-authorized",
                "authentication violation shutdown",
            ],
        )

    def test_ios_dot1x_interfaces_replaced_does_not_remove_what_is_at_the_default(self):
        # nothing is printed for the default, there is nothing to remove, and the other options go
        result = self._run(
            "interface GigabitEthernet1/0/1\n mab\n authentication violation restrict\n",
            {"config": [{"name": "GigabitEthernet1/0/1", "mab": True}], "state": "replaced"},
        )
        self.assertEqual(
            result["commands"],
            ["interface GigabitEthernet1/0/1", "no authentication violation restrict"],
        )

    def test_ios_dot1x_interfaces_fail_retry_that_is_not_the_default_is_set_back(self):
        running = "interface GigabitEthernet1/0/1\n authentication event fail retry 4 action authorize vlan 999\n"
        task = {
            "config": [
                {
                    "name": "GigabitEthernet1/0/1",
                    "authentication": {"event": {"fail": {"action": "authorize", "vlan": 999}}},
                },
            ],
            "state": "replaced",
        }
        result = self._run(running, task)
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "authentication event fail retry 2 action authorize vlan 999",
            ],
        )

    def test_ios_dot1x_interfaces_server_dead_vlan_and_voice_are_two_lines(self):
        # the voice domain is an addition, it does not replace the vlan
        running = "interface GigabitEthernet1/0/1\n authentication event server dead action authorize vlan 20\n"
        result = self._run(
            running,
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "authentication": {
                            "event": {"server_dead": {"action": "authorize", "voice": True}},
                        },
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "authentication event server dead action authorize voice",
            ],
        )
        both = "%s authentication event server dead action authorize voice\n" % running
        set_module_args({"running_config": both, "state": "parsed"})
        parsed = self.execute_module(changed=False)["parsed"]
        self.assertEqual(
            parsed[0]["authentication"]["event"]["server_dead"],
            {"action": "authorize", "vlan": 20, "voice": True},
        )
        # both lines are idempotent, and replaced takes one of them away with its full line
        task = {
            "config": [
                {
                    "name": "GigabitEthernet1/0/1",
                    "authentication": {
                        "event": {
                            "server_dead": {"action": "authorize", "vlan": 20, "voice": True},
                        },
                    },
                },
            ],
            "state": "replaced",
        }
        self.assertEqual(self._run(both, task, changed=False)["commands"], [])
        # the device prints the voice line by itself next to the vlan: not in the task, it is left alone
        task["config"][0]["authentication"]["event"]["server_dead"] = {
            "action": "authorize",
            "vlan": 20,
        }
        self.assertEqual(self._run(both, task, changed=False)["commands"], [])
        # voice: false takes it away with its full line
        task["config"][0]["authentication"]["event"]["server_dead"] = {
            "action": "authorize",
            "vlan": 20,
            "voice": False,
        }
        self.assertEqual(
            self._run(both, task)["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "no authentication event server dead action authorize voice",
            ],
        )

    def test_ios_dot1x_interfaces_server_dead_voice_line_that_the_device_added_is_not_a_change(
        self,
    ):
        # the port has the voice line next to the vlan although the task never had it
        running = (
            "interface GigabitEthernet1/0/1\n"
            " authentication event server dead action authorize vlan 20\n"
            " authentication event server dead action authorize voice \n"
        )
        for state in ("merged", "replaced"):
            result = self._run(
                running,
                {
                    "config": [
                        {
                            "name": "GigabitEthernet1/0/1",
                            "authentication": {
                                "event": {"server_dead": {"action": "authorize", "vlan": 20}},
                            },
                        },
                    ],
                    "state": state,
                },
                changed=False,
            )
            self.assertEqual(result["commands"], [], state)

    def test_ios_dot1x_interfaces_server_dead_is_removed_with_both_lines(self):
        running = (
            "interface GigabitEthernet1/0/1\n"
            " authentication event server dead action authorize vlan 20\n"
            " authentication event server dead action authorize voice \n"
            " mab\n"
        )
        result = self._run(
            running,
            {"config": [{"name": "GigabitEthernet1/0/1", "mab": True}], "state": "replaced"},
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "no authentication event server dead action authorize vlan 20",
                "no authentication event server dead action authorize voice",
            ],
        )

    def test_ios_dot1x_interfaces_a_thousand_ports_are_parsed_in_time(self):
        # an access switch has more than a thousand interfaces
        running = "".join(PORT_BLOCK.format(n=n) for n in range(1, 1301))
        started = time.time()
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        elapsed = time.time() - started
        self.assertEqual(len(result["parsed"]), 1300)
        self.assertEqual(result["parsed"][1299]["name"], "GigabitEthernet1/0/1300")
        self.assertLess(elapsed, 15, "parsing 1300 interfaces took %.1f s" % elapsed)

    def test_ios_dot1x_interfaces_deleted_for_many_ports_is_done_in_time(self):
        running = "".join(PORT_BLOCK.format(n=n) for n in range(1, 401))
        started = time.time()
        result = self._run(running, {"state": "deleted"})
        elapsed = time.time() - started
        self.assertEqual(result["commands"].count("no mab"), 400)
        self.assertEqual(sum(1 for c in result["commands"] if c.startswith("interface ")), 400)
        self.assertLess(
            elapsed,
            30,
            "removing the options of 400 interfaces took %.1f s" % elapsed,
        )

    def test_ios_dot1x_interfaces_server_dead_vlan_changes_and_the_voice_line_stays(self):
        running = (
            "interface GigabitEthernet1/0/1\n"
            " authentication event server dead action authorize vlan 20\n"
            " authentication event server dead action authorize voice \n"
        )
        result = self._run(
            running,
            {
                "config": [
                    {
                        "name": "GigabitEthernet1/0/1",
                        "authentication": {
                            "event": {"server_dead": {"action": "authorize", "vlan": 25}},
                        },
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface GigabitEthernet1/0/1",
                "no authentication event server dead action authorize vlan 20",
                "authentication event server dead action authorize vlan 25",
            ],
        )
