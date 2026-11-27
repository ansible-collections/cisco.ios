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

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_dot1x_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


# what "show running-config all | include ^dot1x|^authentication" prints on a device without 802.1X,
# "authentication mac-move deny" is the display of "neither permit nor deny-uncontrolled"
DEFAULT_DEVICE = dedent(
    """\
    dot1x guest-vlan supplicant
    authentication mac-move deny
    authentication critical recovery delay 100
    """,
)

# a device that uses 802.1X
CONFIGURED_DEVICE = dedent(
    """\
    dot1x system-auth-control
    dot1x critical eapol
    dot1x guest-vlan supplicant
    authentication mac-move permit
    authentication critical recovery delay 1000
    """,
)


class TestIosDot1xGlobalModule(TestIosModule):
    module = ios_dot1x_global

    def setUp(self):
        super(TestIosDot1xGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.dot1x_global.dot1x_global."
            "Dot1x_globalFacts.get_dot1x_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosDot1xGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed)

    def test_ios_dot1x_global_merged(self):
        result = self._run(
            DEFAULT_DEVICE,
            {
                "config": {
                    "system_auth_control": True,
                    "critical_eapol": True,
                    "auth_fail_eapol": True,
                    "authentication": {
                        "mac_move": {"permit": True, "deny_uncontrolled": True},
                        "critical_recovery_delay": 1000,
                    },
                },
                "state": "merged",
            },
        )
        # 802.1X is switched on last, deny-uncontrolled is sent in full: IOS reads "deny" as that keyword
        self.assertEqual(
            result["commands"],
            [
                "dot1x auth-fail eapol",
                "dot1x critical eapol",
                "authentication mac-move permit",
                "authentication mac-move deny-uncontrolled",
                "authentication critical recovery delay 1000",
                "dot1x system-auth-control",
            ],
        )

    def test_ios_dot1x_global_merged_idempotent(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {
                "config": {
                    "system_auth_control": True,
                    "critical_eapol": True,
                    "authentication": {
                        "mac_move": {"permit": True},
                        "critical_recovery_delay": 1000,
                    },
                },
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_global_merged_keeps_what_is_not_in_the_task(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {"config": {"authentication": {"critical_recovery_delay": 500}}, "state": "merged"},
        )
        self.assertEqual(result["commands"], ["authentication critical recovery delay 500"])

    def test_ios_dot1x_global_merged_the_options_that_are_off_are_idempotent(self):
        # IOS prints nothing for the options that are off, only "authentication mac-move deny" and the delay
        result = self._run(
            DEFAULT_DEVICE,
            {
                "config": {
                    "system_auth_control": False,
                    "critical_eapol": False,
                    "auth_fail_eapol": False,
                    "authentication": {
                        "mac_move": {"permit": False, "deny_uncontrolled": False},
                        "critical_recovery_delay": 100,
                    },
                },
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_global_merged_false_turns_an_option_off(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {
                "config": {
                    "critical_eapol": False,
                    "system_auth_control": False,
                    "authentication": {"mac_move": {"permit": False}},
                },
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no dot1x critical eapol",
                "no authentication mac-move permit",
                "no dot1x system-auth-control",
            ],
        )

    def test_ios_dot1x_global_the_two_mac_move_options_are_independent(self):
        # permit is on, deny-uncontrolled is added without touching it, and removed on its own
        device = CONFIGURED_DEVICE + "authentication mac-move deny-uncontrolled\n"
        result = self._run(
            CONFIGURED_DEVICE,
            {
                "config": {"authentication": {"mac_move": {"deny_uncontrolled": True}}},
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["authentication mac-move deny-uncontrolled"])
        result = self._run(
            device,
            {
                "config": {"authentication": {"mac_move": {"deny_uncontrolled": False}}},
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["no authentication mac-move deny-uncontrolled"])

    def test_ios_dot1x_global_replaced_resets_what_is_not_in_the_task(self):
        result = self._run(
            CONFIGURED_DEVICE + "authentication mac-move deny-uncontrolled\n",
            {"config": {"critical_eapol": True}, "state": "replaced"},
        )
        self.assertEqual(
            result["commands"],
            [
                "no authentication mac-move permit",
                "no authentication mac-move deny-uncontrolled",
                "authentication critical recovery delay 100",
                "no dot1x system-auth-control",
            ],
        )

    def test_ios_dot1x_global_replaced_idempotent(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {
                "config": {
                    "system_auth_control": True,
                    "critical_eapol": True,
                    "authentication": {
                        "mac_move": {"permit": True},
                        "critical_recovery_delay": 1000,
                    },
                },
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_global_replaced_with_nothing_to_reset_is_idempotent(self):
        result = self._run(
            DEFAULT_DEVICE,
            {"config": {"critical_eapol": False}, "state": "replaced"},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_global_overridden_is_the_same_as_replaced(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {
                "config": {"system_auth_control": True, "critical_eapol": True},
                "state": "overridden",
            },
        )
        self.assertEqual(
            result["commands"],
            ["no authentication mac-move permit", "authentication critical recovery delay 100"],
        )

    def test_ios_dot1x_global_deleted(self):
        result = self._run(CONFIGURED_DEVICE, {"state": "deleted"})
        self.assertEqual(
            result["commands"],
            [
                "no dot1x critical eapol",
                "no authentication mac-move permit",
                "authentication critical recovery delay 100",
                "no dot1x system-auth-control",
            ],
        )

    def test_ios_dot1x_global_deleted_ignores_the_values_of_the_task(self):
        result = self._run(
            CONFIGURED_DEVICE,
            {"config": {"critical_eapol": True}, "state": "deleted"},
        )
        self.assertIn("no dot1x system-auth-control", result["commands"])
        self.assertIn("no dot1x critical eapol", result["commands"])

    def test_ios_dot1x_global_deleted_idempotent(self):
        result = self._run(DEFAULT_DEVICE, {"state": "deleted"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_dot1x_global_rendered(self):
        set_module_args(
            {
                "config": {
                    "system_auth_control": True,
                    "authentication": {"mac_move": {"permit": True}},
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            ["authentication mac-move permit", "dot1x system-auth-control"],
        )

    def test_ios_dot1x_global_parsed(self):
        set_module_args({"running_config": CONFIGURED_DEVICE, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "system_auth_control": True,
                "critical_eapol": True,
                "authentication": {"mac_move": {"permit": True}, "critical_recovery_delay": 1000},
            },
        )

    def test_ios_dot1x_global_parsed_the_baseline_mac_move_line_is_not_an_option(self):
        set_module_args(
            {
                "running_config": "authentication mac-move deny\nauthentication mac-move deny-uncontrolled\n",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {"authentication": {"mac_move": {"deny_uncontrolled": True}}},
        )

    def test_ios_dot1x_global_parsed_ignores_the_look_alike_commands(self):
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    no dot1x critical eapol
                    dot1x critical eapol block
                    authentication mac-move deny
                    authentication command bounce-port ignore
                    dot1x supplicant force-multicast
                    dot1x guest-vlan supplicant
                    dot1x credentials LAB
                    authentication dis-scale-opt
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], {})

    def test_ios_dot1x_global_gathered(self):
        self.execute_show_command.return_value = DEFAULT_DEVICE
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        # the delay that IOS prints is part of it
        self.assertEqual(result["gathered"], {"authentication": {"critical_recovery_delay": 100}})

    def test_ios_dot1x_global_the_interface_options_are_not_read(self):
        # the lines of the ports are indented and belong to ios_dot1x_interfaces, the facts only ask for the global ones
        result = self._run(
            DEFAULT_DEVICE + " authentication port-control auto\n dot1x pae authenticator\n",
            {"config": {"critical_eapol": True}, "state": "merged"},
        )
        self.assertEqual(result["commands"], ["dot1x critical eapol"])
