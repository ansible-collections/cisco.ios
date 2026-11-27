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

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_aaa
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


# what "show running-config all | section ^aaa|^no aaa new-model" prints, with the lines of the device that are not managed
RUNNING = dedent(
    """\
    aaa new-model
    aaa authentication attempts login 3
    aaa authentication login default group ISE-TAC local
    aaa authentication login CONSOLE-LOGIN local
    aaa authentication enable default group ISE-TAC enable
    aaa authentication dot1x default group ISE-RAD
    aaa authorization exec default group ISE-TAC local if-authenticated
    aaa authorization commands 15 default group ISE-TAC local if-authenticated
    aaa authorization network default group ISE-RAD
    aaa authorization config-commands
    aaa authorization console
    aaa accounting update newinfo periodic 2880
    aaa accounting exec default start-stop group ISE-TAC
    aaa accounting commands 15 default start-stop group ISE-TAC
    aaa accounting system default start-stop group ISE-TAC
    aaa accounting dot1x default start-stop group ISE-RAD
    aaa group server tacacs+ ISE-TAC
     server name ISE-TAC-PRI
     server name ISE-TAC-SEC
     ip tacacs source-interface Loopback0
     ip vrf forwarding MGMT
    aaa group server ldap LDAP-GROUP
     server name LDAP-SERVER
    aaa group server radius ISE-RAD
     server name ISE-RAD-PRI
     deadtime 10
    aaa attribute list ATTRS
     attribute type ssid example
    aaa server radius dynamic-author
     client 192.0.2.10 server-key 6 EncryptedKey1
     client 192.0.2.11
    aaa session-id common
    """,
)

PARSED = {
    "new_model": True,
    "session_id": "common",
    "authentication": {
        "login": [
            {"name": "default", "methods": ["group ISE-TAC", "local"]},
            {"name": "CONSOLE-LOGIN", "methods": ["local"]},
        ],
        "enable": [{"name": "default", "methods": ["group ISE-TAC", "enable"]}],
        "dot1x": [{"name": "default", "methods": ["group ISE-RAD"]}],
    },
    "authorization": {
        "exec": [{"name": "default", "methods": ["group ISE-TAC", "local", "if-authenticated"]}],
        "network": [{"name": "default", "methods": ["group ISE-RAD"]}],
        "commands": [
            {
                "level": 15,
                "name": "default",
                "methods": ["group ISE-TAC", "local", "if-authenticated"],
            },
        ],
        "config_commands": True,
        "console": True,
    },
    "accounting": {
        "exec": [{"name": "default", "record": "start-stop", "methods": ["group ISE-TAC"]}],
        "system": [{"name": "default", "record": "start-stop", "methods": ["group ISE-TAC"]}],
        "dot1x": [{"name": "default", "record": "start-stop", "methods": ["group ISE-RAD"]}],
        "commands": [
            {"level": 15, "name": "default", "record": "start-stop", "methods": ["group ISE-TAC"]},
        ],
    },
    "group_servers": [
        {
            "type": "tacacs+",
            "name": "ISE-TAC",
            "servers": ["ISE-TAC-PRI", "ISE-TAC-SEC"],
            "source_interface": "Loopback0",
            "vrf": "MGMT",
        },
        {"type": "radius", "name": "ISE-RAD", "servers": ["ISE-RAD-PRI"], "deadtime": 10},
    ],
    "dynamic_author": {
        "clients": [
            {"address": "192.0.2.10", "server_key": {"type": 6, "key": "EncryptedKey1"}},
            {"address": "192.0.2.11"},
        ],
    },
}


class TestIosAaaModule(TestIosModule):
    module = ios_aaa

    def setUp(self):
        super(TestIosAaaModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.aaa.aaa."
            "AaaFacts.get_aaa_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosAaaModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, config, state="merged", changed=True, failed=False):
        self.execute_show_command.return_value = running
        args = {"state": state}
        if config is not None:
            args["config"] = config
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    # ------------------------------------------------------------------ facts
    def test_ios_aaa_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], PARSED)

    def test_ios_aaa_gathered(self):
        self.execute_show_command.return_value = RUNNING
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], PARSED)

    def test_ios_aaa_aaa_is_off_when_the_device_prints_no_aaa_new_model(self):
        self.execute_show_command.return_value = "no aaa new-model\n"
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})

    def test_ios_aaa_the_device_prints_a_space_after_some_lists(self):
        set_module_args(
            {
                "running_config": "aaa authorization exec default local \naaa authorization network default group ISE-RAD \n",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"]["authorization"]["exec"],
            [{"name": "default", "methods": ["local"]}],
        )
        self.assertEqual(
            result["parsed"]["authorization"]["network"],
            [{"name": "default", "methods": ["group ISE-RAD"]}],
        )

    def test_ios_aaa_the_methods_keep_their_order(self):
        set_module_args(
            {
                "running_config": "aaa authentication login default local group ISE-TAC none\n",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"]["authentication"]["login"][0]["methods"],
            ["local", "group ISE-TAC", "none"],
        )

    # ------------------------------------------------------------------ merged
    def test_ios_aaa_merged_idempotent(self):
        result = self._run(RUNNING, PARSED, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_merged_new_configuration(self):
        # the groups and the clients come first, a method list refers to a group
        result = self._run(
            "",
            {
                "new_model": True,
                "authentication": {
                    "login": [{"name": "ISE-LOGIN", "methods": ["group ISE-TAC", "local"]}],
                },
                "authorization": {
                    "commands": [
                        {
                            "level": 15,
                            "name": "ISE-CMD",
                            "methods": ["group ISE-TAC", "if-authenticated"],
                        },
                    ],
                    "config_commands": True,
                },
                "accounting": {
                    "exec": [
                        {"name": "ISE-ACC", "record": "start-stop", "methods": ["group ISE-TAC"]},
                    ],
                },
                "group_servers": [
                    {
                        "type": "radius",
                        "name": "ISE-RAD",
                        "servers": ["ISE-RAD-PRI", "ISE-RAD-SEC"],
                        "source_interface": "Loopback0",
                        "vrf": "MGMT",
                        "deadtime": 5,
                    },
                ],
                "dynamic_author": {
                    "clients": [
                        {
                            "address": "192.0.2.10",
                            "vrf": "MGMT",
                            "server_key": {"key": "Secret123"},
                        },
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "aaa new-model",
                "aaa authorization config-commands",
                "aaa group server radius ISE-RAD",
                "server name ISE-RAD-PRI",
                "server name ISE-RAD-SEC",
                "ip radius source-interface Loopback0",
                "ip vrf forwarding MGMT",
                "deadtime 5",
                "aaa server radius dynamic-author",
                "client 192.0.2.10 vrf MGMT server-key Secret123",
                "aaa authentication login ISE-LOGIN group ISE-TAC local",
                "aaa authorization commands 15 ISE-CMD group ISE-TAC if-authenticated",
                "aaa accounting exec ISE-ACC start-stop group ISE-TAC",
            ],
        )

    def test_ios_aaa_merged_only_touches_what_is_in_the_task(self):
        result = self._run(
            RUNNING,
            {"authentication": {"login": [{"name": "NEW-LIST", "methods": ["local"]}]}},
        )
        self.assertEqual(result["commands"], ["aaa authentication login NEW-LIST local"])

    def test_ios_aaa_merged_a_changed_order_of_the_methods_is_sent_again(self):
        result = self._run(
            RUNNING,
            {
                "authentication": {
                    "login": [{"name": "default", "methods": ["local", "group ISE-TAC"]}],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            ["aaa authentication login default local group ISE-TAC"],
        )

    def test_ios_aaa_merged_accounting_record_none_has_no_methods(self):
        result = self._run(
            RUNNING,
            {"accounting": {"network": [{"name": "default", "record": "none"}]}},
        )
        self.assertEqual(result["commands"], ["aaa accounting network default none"])

    def test_ios_aaa_merged_changed_record_type(self):
        result = self._run(
            RUNNING,
            {
                "accounting": {
                    "system": [
                        {"name": "default", "record": "stop-only", "methods": ["group ISE-TAC"]},
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            ["aaa accounting system default stop-only group ISE-TAC"],
        )

    def test_ios_aaa_a_list_without_methods_fails(self):
        result = self._run(RUNNING, {"authentication": {"login": [{"name": "X"}]}}, failed=True)
        self.assertIn("methods are required", result["msg"])

    def test_ios_aaa_an_accounting_list_without_record_fails(self):
        result = self._run(
            RUNNING,
            {"accounting": {"exec": [{"name": "X", "methods": ["local"]}]}},
            failed=True,
        )
        self.assertIn("record is required", result["msg"])

    def test_ios_aaa_new_model_session_id_and_flags_are_only_changed_when_in_the_task(self):
        for state in ("merged", "replaced", "overridden"):
            result = self._run(
                RUNNING,
                {
                    "authentication": {
                        "login": [{"name": "default", "methods": ["group ISE-TAC", "local"]}],
                    },
                },
                state=state,
                changed=state == "overridden",
            )
            for command in result["commands"]:
                self.assertNotIn("new-model", command, state)
                self.assertNotIn("session-id", command, state)
                self.assertNotIn("config-commands", command, state)
                self.assertNotIn("console", command, state)

    def test_ios_aaa_new_model_false_and_session_id_and_flags(self):
        result = self._run(
            RUNNING,
            {
                "new_model": False,
                "session_id": "unique",
                "authorization": {"config_commands": False, "console": False},
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no aaa new-model",
                "aaa session-id unique",
                "no aaa authorization config-commands",
                "no aaa authorization console",
            ],
        )

    # ------------------------------------------------------------------ group servers
    def test_ios_aaa_merged_group_appends_the_new_servers_and_keeps_the_rest(self):
        result = self._run(
            RUNNING,
            {"group_servers": [{"type": "tacacs+", "name": "ISE-TAC", "servers": ["ISE-TAC-TER"]}]},
        )
        self.assertEqual(
            result["commands"],
            ["aaa group server tacacs+ ISE-TAC", "server name ISE-TAC-TER"],
        )

    def test_ios_aaa_merged_group_source_interface_may_be_abbreviated(self):
        result = self._run(
            RUNNING,
            {"group_servers": [{"type": "tacacs+", "name": "ISE-TAC", "source_interface": "Lo0"}]},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_merged_group_changes_source_interface_and_deadtime(self):
        result = self._run(
            RUNNING,
            {
                "group_servers": [
                    {
                        "type": "radius",
                        "name": "ISE-RAD",
                        "source_interface": "Vlan10",
                        "deadtime": 20,
                    },
                ],
            },
        )
        self.assertEqual(
            result["commands"],
            ["aaa group server radius ISE-RAD", "ip radius source-interface Vlan10", "deadtime 20"],
        )

    def test_ios_aaa_replaced_group_is_made_to_match(self):
        result = self._run(
            RUNNING,
            {"group_servers": [{"type": "tacacs+", "name": "ISE-TAC", "servers": ["ISE-TAC-PRI"]}]},
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "aaa group server tacacs+ ISE-TAC",
                "no server name ISE-TAC-SEC",
                "no ip tacacs source-interface",
                "no ip vrf forwarding",
            ],
        )

    def test_ios_aaa_replaced_group_with_another_order_of_the_servers(self):
        # the order is the order the servers are tried, change from where it differs
        result = self._run(
            RUNNING,
            {
                "group_servers": [
                    {
                        "type": "tacacs+",
                        "name": "ISE-TAC",
                        "servers": ["ISE-TAC-SEC", "ISE-TAC-PRI"],
                        "source_interface": "Loopback0",
                        "vrf": "MGMT",
                    },
                ],
            },
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "aaa group server tacacs+ ISE-TAC",
                "no server name ISE-TAC-PRI",
                "no server name ISE-TAC-SEC",
                "server name ISE-TAC-SEC",
                "server name ISE-TAC-PRI",
            ],
        )

    def test_ios_aaa_replaced_leaves_the_other_groups_and_lists(self):
        result = self._run(
            RUNNING,
            {
                "group_servers": [
                    {
                        "type": "radius",
                        "name": "ISE-RAD",
                        "servers": ["ISE-RAD-PRI"],
                        "deadtime": 10,
                    },
                ],
            },
            state="replaced",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    # ------------------------------------------------------------------ dynamic author
    def test_ios_aaa_client_key_in_plain_text_is_sent_for_a_new_client_or_one_without_key(self):
        result = self._run(
            RUNNING,
            {
                "dynamic_author": {
                    "clients": [
                        {"address": "192.0.2.11", "server_key": {"key": "Plain1"}},
                        {"address": "192.0.2.12", "server_key": {"key": "Plain2"}},
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "aaa server radius dynamic-author",
                "client 192.0.2.11 server-key Plain1",
                "client 192.0.2.12 server-key Plain2",
            ],
        )

    def test_ios_aaa_client_key_in_plain_text_is_not_compared_with_the_encrypted_one(self):
        result = self._run(
            RUNNING,
            {
                "dynamic_author": {
                    "clients": [{"address": "192.0.2.10", "server_key": {"key": "Plain1"}}],
                },
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_client_encrypted_key_is_compared(self):
        same = {"address": "192.0.2.10", "server_key": {"type": 6, "key": "EncryptedKey1"}}
        other = {"address": "192.0.2.10", "server_key": {"type": 6, "key": "EncryptedKey2"}}
        self._run(RUNNING, {"dynamic_author": {"clients": [same]}}, changed=False)
        result = self._run(RUNNING, {"dynamic_author": {"clients": [other]}})
        self.assertEqual(
            result["commands"],
            ["aaa server radius dynamic-author", "client 192.0.2.10 server-key 6 EncryptedKey2"],
        )

    def test_ios_aaa_client_without_key_in_the_task_keeps_the_key_of_the_device(self):
        result = self._run(
            RUNNING,
            {"dynamic_author": {"clients": [{"address": "192.0.2.10"}]}},
            state="replaced",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_client_with_another_vrf_is_removed_and_added(self):
        result = self._run(
            RUNNING,
            {"dynamic_author": {"clients": [{"address": "192.0.2.11", "vrf": "MGMT"}]}},
        )
        self.assertEqual(
            result["commands"],
            [
                "aaa server radius dynamic-author",
                "no client 192.0.2.11",
                "client 192.0.2.11 vrf MGMT",
            ],
        )

    # ------------------------------------------------------------------ overridden
    def test_ios_aaa_overridden_removes_the_lists_of_the_sections_in_the_task_only(self):
        result = self._run(
            RUNNING,
            {
                "authentication": {
                    "login": [{"name": "default", "methods": ["group ISE-TAC", "local"]}],
                },
            },
            state="overridden",
        )
        # CONSOLE-LOGIN is another login list, the enable and dot1x lists, the other sections, the groups
        # and the clients are not in the task
        self.assertEqual(result["commands"], ["no aaa authentication login CONSOLE-LOGIN"])

    def test_ios_aaa_overridden_removes_the_other_groups_and_clients_when_the_task_has_groups_and_clients(
        self,
    ):
        result = self._run(
            RUNNING,
            {
                "group_servers": [
                    {
                        "type": "radius",
                        "name": "ISE-RAD",
                        "servers": ["ISE-RAD-PRI"],
                        "deadtime": 10,
                    },
                ],
                "dynamic_author": {"clients": [{"address": "192.0.2.10"}]},
            },
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            [
                "no aaa group server tacacs+ ISE-TAC",
                "aaa server radius dynamic-author",
                "no client 192.0.2.11",
            ],
        )

    # ------------------------------------------------------------------ deleted
    def test_ios_aaa_deleted_what_the_task_names(self):
        result = self._run(
            RUNNING,
            {
                "authentication": {"login": [{"name": "CONSOLE-LOGIN"}, {"name": "UNKNOWN"}]},
                "authorization": {"commands": [{"level": 15, "name": "default"}], "console": True},
                "group_servers": [{"type": "radius", "name": "ISE-RAD"}],
                "dynamic_author": {"clients": [{"address": "192.0.2.11"}]},
            },
            state="deleted",
        )
        self.assertEqual(
            result["commands"],
            [
                "no aaa authentication login CONSOLE-LOGIN",
                "no aaa authorization commands 15 default",
                "no aaa group server radius ISE-RAD",
                "aaa server radius dynamic-author",
                "no client 192.0.2.11",
                "no aaa authorization console",
            ],
        )

    def test_ios_aaa_deleted_the_last_clients_remove_the_block(self):
        # IOS keeps an empty "aaa server radius dynamic-author" when the last client is removed
        result = self._run(
            RUNNING,
            {"dynamic_author": {"clients": [{"address": "192.0.2.10"}, {"address": "192.0.2.11"}]}},
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no aaa server radius dynamic-author"])

    def test_ios_aaa_deleted_without_config_keeps_the_default_lists_aaa_and_the_session_id(self):
        # the default lists decide how the logins work, the other lists, groups and clients go
        result = self._run(RUNNING, None, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "no aaa authentication login CONSOLE-LOGIN",
                "no aaa group server tacacs+ ISE-TAC",
                "no aaa group server radius ISE-RAD",
                "no aaa server radius dynamic-author",
            ],
        )

    def test_ios_aaa_deleted_removes_a_default_list_when_the_task_names_it(self):
        result = self._run(
            RUNNING,
            {
                "authentication": {"login": [{"name": "default"}]},
                "authorization": {"commands": [{"level": 15, "name": "default"}]},
                "accounting": {"exec": [{"name": "default"}]},
            },
            state="deleted",
        )
        self.assertEqual(
            result["commands"],
            [
                "no aaa authentication login default",
                "no aaa authorization commands 15 default",
                "no aaa accounting exec default",
            ],
        )

    def test_ios_aaa_deleted_only_default_lists_on_the_device_is_nothing_to_do(self):
        result = self._run(
            "aaa new-model\naaa authentication login default local\naaa authorization exec default local\naaa session-id common\n",
            None,
            state="deleted",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_overridden_and_replaced_are_not_changed_by_the_default_lists_rule(self):
        # overridden removes the default login list when it is not in the task, as any other list
        config = {"authentication": {"login": [{"name": "CONSOLE-LOGIN", "methods": ["local"]}]}}
        result = self._run(RUNNING, config, state="overridden")
        self.assertEqual(result["commands"], ["no aaa authentication login default"])
        # replaced only replaces what the task names
        result = self._run(RUNNING, config, state="replaced", changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_aaa_deleted_nothing_on_an_empty_device(self):
        result = self._run("", None, state="deleted", changed=False)
        self.assertEqual(result["commands"], [])

    # ------------------------------------------------------------------ rendered
    def test_ios_aaa_rendered(self):
        set_module_args(
            {
                "config": {
                    "accounting": {
                        "system": [
                            {
                                "name": "default",
                                "record": "start-stop",
                                "methods": ["group ISE-TAC"],
                            },
                        ],
                    },
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            ["aaa accounting system default start-stop group ISE-TAC"],
        )

    # ------------------------------------------------------------------ what is not managed
    def test_ios_aaa_the_children_of_other_aaa_blocks_are_not_attached_to_a_group(self):
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    aaa group server radius ISE-RAD
                     server name ISE-RAD-PRI
                    aaa group server ldap LDAP-GROUP
                     server name LDAP-SERVER
                    aaa attribute list ATTRS
                     deadtime 99
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"]["group_servers"],
            [{"type": "radius", "name": "ISE-RAD", "servers": ["ISE-RAD-PRI"]}],
        )
