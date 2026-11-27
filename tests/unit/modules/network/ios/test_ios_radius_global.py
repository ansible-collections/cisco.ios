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

from ansible_collections.cisco.ios.plugins.modules import ios_radius_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


SERVERS = dedent(
    """\
    radius server RADIUS-PRI
     address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
     key 7 EXAMPLEHASH7
     timeout 3
     retransmit 2
    radius server RADIUS-SEC
     address ipv6 2001:db8::10 auth-port 1645 acct-port 1646
     key 6 EXAMPLEHASH6
    """,
)

GLOBALS = dedent(
    """\
    radius-server timeout 4
    radius-server retransmit 2
    radius-server deadtime 5
    radius-server dead-criteria time 5 tries 3
    radius-server load-balance method least-outstanding
    radius-server attribute 6 on-for-login-auth
    radius-server attribute 8 include-in-access-req
    radius-server attribute 25 access-request include
    ip radius source-interface Vlan10 vrf MGMT
    """,
)

RUNNING = SERVERS + GLOBALS

PRI = {
    "name": "RADIUS-PRI",
    "address": {"ipv4": "192.0.2.10", "auth_port": 1812, "acct_port": 1813},
    "key": {"type": 7, "value": "EXAMPLEHASH7"},
    "timeout": 3,
    "retransmit": 2,
}
SEC = {
    "name": "RADIUS-SEC",
    "address": {"ipv6": "2001:db8::10", "auth_port": 1645, "acct_port": 1646},
    "key": {"type": 6, "value": "EXAMPLEHASH6"},
}
GLOBAL_CONFIG = {
    "timeout": 4,
    "retransmit": 2,
    "deadtime": 5,
    "dead_criteria": {"time": 5, "tries": 3},
    "load_balance": {"method": "least_outstanding"},
    "source_interface": {"name": "Vlan10", "vrf": "MGMT"},
    "attributes": [
        {"number": 6, "on_for_login_auth": True},
        {"number": 8, "include_in_access_req": True},
        {"number": 25, "access_request_include": True},
    ],
}


class TestIosRadiusGlobalModule(TestIosModule):
    module = ios_radius_global

    def setUp(self):
        super(TestIosRadiusGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.radius_global.radius_global."
            "Radius_globalFacts.get_radius_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosRadiusGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, config, state="merged", changed=True, failed=False):
        self.execute_show_command.return_value = running
        args = {"state": state}
        if config is not None:
            args["config"] = config
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    # ------------------------------------------------------------------ merged
    def test_ios_radius_global_merged(self):
        result = self._run(
            "",
            dict(
                GLOBAL_CONFIG,
                source_interface={"name": "Vl10", "vrf": "MGMT"},
                servers=[PRI, SEC],
            ),
        )
        self.assertEqual(
            result["commands"],
            [
                "radius-server timeout 4",
                "radius-server retransmit 2",
                "radius-server deadtime 5",
                "radius-server dead-criteria time 5 tries 3",
                "radius-server load-balance method least-outstanding",
                "ip radius source-interface Vlan10 vrf MGMT",
                "radius-server attribute 6 on-for-login-auth",
                "radius-server attribute 8 include-in-access-req",
                "radius-server attribute 25 access-request include",
                "radius server RADIUS-PRI",
                "address ipv4 192.0.2.10 auth-port 1812 acct-port 1813",
                "key 7 EXAMPLEHASH7",
                "timeout 3",
                "retransmit 2",
                "radius server RADIUS-SEC",
                "address ipv6 2001:db8::10 auth-port 1645 acct-port 1646",
                "key 6 EXAMPLEHASH6",
            ],
        )

    def test_ios_radius_global_merged_idempotent_with_a_short_interface_name(self):
        result = self._run(
            RUNNING,
            dict(
                GLOBAL_CONFIG,
                source_interface={"name": "Vl10", "vrf": "MGMT"},
                servers=[PRI, SEC],
            ),
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_defaults_are_not_printed_so_setting_them_is_idempotent(self):
        result = self._run(
            "",
            {
                "timeout": 5,
                "retransmit": 3,
                "deadtime": 0,
                "dead_criteria": {"time": 10, "tries": 10},
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_a_default_value_is_reached_with_the_bare_no_form(self):
        # "radius-server deadtime 0" is invalid input on IOS
        result = self._run(
            RUNNING,
            {
                "timeout": 5,
                "retransmit": 3,
                "deadtime": 0,
                "dead_criteria": {"time": 10, "tries": 10},
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no radius-server timeout",
                "no radius-server retransmit",
                "no radius-server deadtime",
                "no radius-server dead-criteria",
            ],
        )

    def test_ios_radius_global_ipv6_address_is_compared_as_an_address(self):
        # IOS prints 2001:DB8::10
        running = SERVERS.replace("2001:db8::10", "2001:DB8::10")
        result = self._run(
            running,
            {
                "servers": [
                    dict(
                        SEC,
                        address={
                            "ipv6": "2001:db8:0:0:0:0:0:10",
                            "auth_port": 1645,
                            "acct_port": 1646,
                        },
                    ),
                ],
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_host_name_is_compared_without_the_case(self):
        result = self._run(
            "radius server RADIUS-HOST\n address ipv4 Radius.Example.COM auth-port 1812 acct-port 1813\n",
            {"servers": [{"name": "RADIUS-HOST", "address": {"ipv4": "radius.example.com"}}]},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_merged_keeps_what_is_not_in_the_task(self):
        result = self._run(RUNNING, {"timeout": 6})
        self.assertEqual(result["commands"], ["radius-server timeout 6"])

    def test_ios_radius_global_merged_dead_criteria_keeps_the_other_value(self):
        result = self._run(RUNNING, {"dead_criteria": {"time": 7}})
        self.assertEqual(result["commands"], ["radius-server dead-criteria time 7 tries 3"])

    def test_ios_radius_global_merged_turns_an_attribute_option_off(self):
        result = self._run(RUNNING, {"attributes": [{"number": 6, "on_for_login_auth": False}]})
        self.assertEqual(result["commands"], ["no radius-server attribute 6 on-for-login-auth"])

    def test_ios_radius_global_merged_false_on_an_option_that_is_off_is_idempotent(self):
        result = self._run(
            RUNNING,
            {"attributes": [{"number": 6, "include_in_acct_req": False}]},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_attribute_sent_by_default_cannot_be_switched_off(self):
        result = self._run(
            "",
            {"attributes": [{"number": 77, "include_in_access_req": False}]},
            failed=True,
        )
        self.assertIn("attribute 77 is sent by default", result["msg"])

    # ------------------------------------------------------------------ servers
    def test_ios_radius_global_merged_server_changes_only_what_is_in_the_task(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "timeout": 9}]},
        )
        self.assertEqual(result["commands"], ["radius server RADIUS-PRI", "timeout 9"])

    def test_ios_radius_global_merged_address_port_only_keeps_the_address(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "address": {"auth_port": 1645}}]},
        )
        self.assertEqual(
            result["commands"],
            ["radius server RADIUS-PRI", "address ipv4 192.0.2.10 auth-port 1645 acct-port 1813"],
        )

    def test_ios_radius_global_merged_address_family_changes(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "address": {"ipv6": "2001:db8::11"}}]},
        )
        self.assertEqual(
            result["commands"],
            ["radius server RADIUS-PRI", "address ipv6 2001:db8::11 auth-port 1812 acct-port 1813"],
        )

    def test_ios_radius_global_default_ports_are_not_a_change(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "address": {"ipv4": "192.0.2.10"}}]},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_key_in_clear_text_is_only_sent_when_there_is_no_key(self):
        # IOS prints "key 7 <hash>", a clear text key cannot be compared with it
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "key": {"type": 0, "value": "example-secret"}}]},
            changed=False,
        )
        self.assertEqual(result["commands"], [])
        result = self._run(
            SERVERS.replace(" key 7 EXAMPLEHASH7\n", ""),
            {"servers": [{"name": "RADIUS-PRI", "key": {"type": 0, "value": "example-secret"}}]},
        )
        self.assertEqual(result["commands"], ["radius server RADIUS-PRI", "key 0 example-secret"])

    def test_ios_radius_global_key_in_the_encrypted_form_is_compared(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-PRI", "key": {"type": 7, "value": "OTHERHASH7"}}]},
        )
        self.assertEqual(result["commands"], ["radius server RADIUS-PRI", "key 7 OTHERHASH7"])

    def test_ios_radius_global_new_server_needs_an_address(self):
        result = self._run("", {"servers": [{"name": "RADIUS-NEW", "timeout": 3}]}, failed=True)
        self.assertIn("RADIUS-NEW is required", result["msg"].replace("radius server ", ""))
        result = self._run(
            "",
            {"servers": [{"name": "RADIUS-NEW", "address": {"auth_port": 1812}}]},
            failed=True,
        )
        self.assertIn("(ipv4 or ipv6)", result["msg"])

    def test_ios_radius_global_address_is_ipv4_or_ipv6(self):
        result = self._run(
            "",
            {
                "servers": [
                    {"name": "RADIUS-NEW", "address": {"ipv4": "192.0.2.1", "ipv6": "2001:db8::1"}},
                ],
            },
            failed=True,
        )
        self.assertIn("mutually exclusive", result["msg"])

    # ------------------------------------------------------------------ replaced / overridden
    def test_ios_radius_global_replaced_server_removes_what_is_not_in_the_task(self):
        result = self._run(
            RUNNING,
            dict(
                GLOBAL_CONFIG,
                servers=[{"name": "RADIUS-PRI", "address": {"ipv4": "192.0.2.11"}, "timeout": 3}],
            ),
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "radius server RADIUS-PRI",
                "address ipv4 192.0.2.11 auth-port 1812 acct-port 1813",
                "no key",
                "no retransmit",
            ],
        )

    def test_ios_radius_global_replaced_sets_the_global_options_that_are_not_in_the_task_back(self):
        result = self._run(RUNNING, {"servers": [PRI]}, state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "no radius-server timeout",
                "no radius-server retransmit",
                "no radius-server deadtime",
                "no radius-server dead-criteria",
                "no radius-server load-balance method least-outstanding",
                "no ip radius source-interface Vlan10 vrf MGMT",
                "no radius-server attribute 6 on-for-login-auth",
                "no radius-server attribute 8 include-in-access-req",
                "no radius-server attribute 25 access-request include",
            ],
        )

    def test_ios_radius_global_replaced_idempotent_and_leaves_the_other_servers(self):
        result = self._run(
            RUNNING,
            dict(GLOBAL_CONFIG, servers=[PRI]),
            state="replaced",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_radius_global_replaced_dead_criteria_partial_goes_back_to_the_default(self):
        result = self._run(
            RUNNING,
            dict(GLOBAL_CONFIG, dead_criteria={"time": 7}, servers=[PRI]),
            state="replaced",
        )
        self.assertEqual(result["commands"], ["radius-server dead-criteria time 7 tries 10"])

    def test_ios_radius_global_overridden_removes_the_servers_that_are_not_in_the_task(self):
        result = self._run(RUNNING, dict(GLOBAL_CONFIG, servers=[PRI]), state="overridden")
        self.assertEqual(result["commands"], ["no radius server RADIUS-SEC"])

    # ------------------------------------------------------------------ deleted
    def test_ios_radius_global_deleted_server(self):
        result = self._run(
            RUNNING,
            {"servers": [{"name": "RADIUS-SEC"}, {"name": "RADIUS-NONE"}]},
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no radius server RADIUS-SEC"])

    def test_ios_radius_global_deleted_global_option_keeps_the_servers(self):
        result = self._run(
            RUNNING,
            {"timeout": 4, "source_interface": {"name": "Vlan10"}},
            state="deleted",
        )
        self.assertEqual(
            result["commands"],
            ["no radius-server timeout", "no ip radius source-interface Vlan10 vrf MGMT"],
        )

    def test_ios_radius_global_deleted_everything(self):
        result = self._run(RUNNING, None, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "no radius server RADIUS-PRI",
                "no radius server RADIUS-SEC",
                "no radius-server timeout",
                "no radius-server retransmit",
                "no radius-server deadtime",
                "no radius-server dead-criteria",
                "no radius-server load-balance method least-outstanding",
                "no ip radius source-interface Vlan10 vrf MGMT",
                "no radius-server attribute 6 on-for-login-auth",
                "no radius-server attribute 8 include-in-access-req",
                "no radius-server attribute 25 access-request include",
            ],
        )

    def test_ios_radius_global_deleted_empty_device(self):
        result = self._run("", None, state="deleted", changed=False)
        self.assertEqual(result["commands"], [])

    # ------------------------------------------------------------------ rendered / parsed / gathered
    def test_ios_radius_global_rendered(self):
        set_module_args(
            {
                "config": {
                    "source_interface": {"name": "Loopback1"},
                    "servers": [
                        {"name": "RADIUS-NEW", "address": {"ipv4": "192.0.2.50"}, "retransmit": 4},
                    ],
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "ip radius source-interface loopback1",
                "radius server RADIUS-NEW",
                "address ipv4 192.0.2.50 auth-port 1812 acct-port 1813",
                "retransmit 4",
            ],
        )

    def test_ios_radius_global_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            dict(GLOBAL_CONFIG, servers=[PRI, SEC]),
        )

    def test_ios_radius_global_parsed_ignores_what_the_module_does_not_manage(self):
        # the lines of other radius-server options and of the legacy host form must not end up in a server
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    radius server RADIUS-PRI
                     address ipv4 192.0.2.10 auth-port 1812 acct-port 1813
                     automate-tester username probe probe-on
                    radius-server attribute wireless accounting username-delimiter colon
                    radius-server host 192.0.2.99 auth-port 1812 acct-port 1813
                    ip radius source-interface Vlan10
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "source_interface": {"name": "Vlan10"},
                "servers": [
                    {
                        "name": "RADIUS-PRI",
                        "address": {"ipv4": "192.0.2.10", "auth_port": 1812, "acct_port": 1813},
                    },
                ],
            },
        )

    def test_ios_radius_global_gathered(self):
        self.execute_show_command.return_value = RUNNING
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"]["servers"][0]["name"], "RADIUS-PRI")
        self.assertEqual(
            result["gathered"]["attributes"][2],
            {"number": 25, "access_request_include": True},
        )
