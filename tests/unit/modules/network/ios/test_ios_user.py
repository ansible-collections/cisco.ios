# (c) 2016 Red Hat Inc.
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
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_user
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule, load_fixture


class TestIosUserModule(TestIosModule):
    module = ios_user

    def setUp(self):
        super(TestIosUserModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_user.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_user.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestIosUserModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        self.get_config.return_value = load_fixture("ios_user_config.cfg")
        self.load_config.return_value = dict(diff=None, session="session")

    def test_ios_user_create(self):
        set_module_args(dict(name="test", nopassword=True))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username test nopassword"])

    def test_ios_user_delete(self):
        set_module_args(dict(name="ansible", state="absent"))
        result = self.execute_module(changed=True)
        cmds = [
            {
                "command": "no username ansible",
                "answer": "y",
                "newline": False,
                "prompt": "This operation will remove all username related configurations with same name",
            },
        ]

        result_cmd = []
        for i in result["commands"]:
            result_cmd.append(i)

        self.assertEqual(result_cmd, cmds)

    def test_ios_user_password(self):
        set_module_args(dict(name="ansible", configured_password="test"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username ansible secret test"])

    def test_ios_user_privilege(self):
        set_module_args(dict(name="ansible", privilege=15))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username ansible privilege 15"])

    def test_ios_user_privilege_invalid(self):
        set_module_args(dict(name="ansible", privilege=25))
        self.execute_module(failed=True)

    def test_ios_user_purge(self):
        set_module_args(dict(purge=True))
        result = self.execute_module(changed=True)
        cmd = [
            "ip ssh pubkey-chain",
            "no username purger",
            "exit",
            "ip ssh pubkey-chain",
            "no username ansible",
            "exit",
            {
                "command": "no username ansible",
                "answer": "y",
                "newline": False,
                "prompt": "This operation will remove all username related configurations with same name",
            },
        ]

        result_cmd = []
        for i in result["commands"]:
            result_cmd.append(i)

        self.assertCountEqual(result_cmd, cmd)

    def test_ios_user_view(self):
        set_module_args(dict(name="ansible", view="test"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username ansible view test"])

    def test_ios_user_update_password_changed(self):
        set_module_args(
            dict(name="test", configured_password="test", update_password="on_create"),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username test secret test"])

    def test_ios_user_update_password_on_create_ok(self):
        set_module_args(
            dict(
                name="ansible",
                configured_password="test",
                update_password="on_create",
            ),
        )
        self.execute_module()

    def test_ios_user_update_password_always(self):
        set_module_args(
            dict(name="ansible", configured_password="test", update_password="always"),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username ansible secret test"])

    def test_ios_user_set_sshkey(self):
        set_module_args(dict(name="ansible", sshkey="dGVzdA=="))
        commands = [
            "ip ssh pubkey-chain",
            "username ansible",
            "key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result["commands"], commands)

    def test_ios_user_set_sshkey_multiple(self):
        set_module_args(dict(name="ansible", sshkey=["dGVzdA==", "eHWacB2=="]))
        commands = [
            "ip ssh pubkey-chain",
            "username ansible",
            "key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6",
            "key-hash ssh-rsa A019918340A1E9183388D9A675603036",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result["commands"], commands)

    def test_ios_user_set_sshkey_purge_keys_false(self):
        set_module_args(dict(name="ansible", sshkey="dGVzdA==", purge_keys=False))
        commands = [
            "ip ssh pubkey-chain",
            "username ansible",
            "key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result["commands"], commands)

    def test_ios_user_set_sshkey_purge_keys_true(self):
        set_module_args(dict(name="purger", sshkey="dGVzdA==", purge_keys=True))
        commands = [
            "ip ssh pubkey-chain",
            "username purger",
            "no key-hash ssh-rsa A019918340A1E9183388D9A675603036",
            "no key-hash ssh-rsa D1B15A08146DD96ED43FD5F48CA11FC8",
            "exit",
            "exit",
            "ip ssh pubkey-chain",
            "username purger",
            "key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_user_add_sshkey_purge_keys_true(self):
        set_module_args(dict(name="purger", sshkey=["dGVzdA==", "eHWacB2=="], purge_keys=True))
        commands = [
            "ip ssh pubkey-chain",
            "username purger",
            "no key-hash ssh-rsa D1B15A08146DD96ED43FD5F48CA11FC8",
            "exit",
            "exit",
            "ip ssh pubkey-chain",
            "username purger",
            "key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6",
            "key-hash ssh-rsa A019918340A1E9183388D9A675603036",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result["commands"], commands)

    def test_ios_user_add_sshkey_purge_keys_true_idempotent(self):
        set_module_args(dict(name="purger", sshkey=["eHWacB2==", "dHJhaWxpbmc="], purge_keys=True))
        commands = []
        result = self.execute_module(changed=False, commands=commands)
        self.assertEqual(result["commands"], commands)

    def test_ios_user_set_three_sshkeys_fail(self):
        set_module_args(dict(name="purger", sshkey=["dGVzdA==", "eHWacB2==", "dGVzdA=="]))
        self.execute_module(failed=True)

    def test_add_hashed_password(self):
        hashed_password_val = "replacementforhashwhichissupposedtogohereonlyfortestingpurposes"
        set_module_args(
            dict(
                name="ansible",
                hashed_password={
                    "type": 9,
                    "value": hashed_password_val,
                },
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [f"username ansible secret 9 {hashed_password_val}"],
        )

    def test_add_hpassword_with_type(self):
        set_module_args(
            dict(
                name="ansible",
                hashed_password={
                    "type": 0,
                    "value": "test",
                },
                password_type="password",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["username ansible password 0 test"])

    def test_add_hashed_password_idempotent(self):
        # Same type and value as in fixture -> no commands
        set_module_args(
            dict(
                name="ansible",
                hashed_password={
                    "type": 5,
                    "value": "$1$3yWSXiIi$VdzV59ChiurrNdGxlDeAW/",
                },
            ),
        )
        self.execute_module(changed=False)

    def test_ios_user_aggregate_update_password_on_create(self):
        # Per-item on_create overrides module-level always.
        # ansible (exists in fixture): on_create -> no password command.
        # newuser (new): on_create still applies, but not-have path triggers creation.
        set_module_args(
            dict(
                aggregate=[
                    {
                        "name": "ansible",
                        "configured_password": "pass_ansible",
                        "update_password": "on_create",
                    },
                    {
                        "name": "newuser",
                        "configured_password": "pass_newuser",
                        "update_password": "on_create",
                    },
                ],
                update_password="always",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertNotIn("username ansible secret pass_ansible", result["commands"])
        self.assertIn("username newuser secret pass_newuser", result["commands"])

    def test_ios_user_aggregate_update_password_always(self):
        # Per-item always: both existing (ansible) and new (newuser) get password commands.
        set_module_args(
            dict(
                aggregate=[
                    {
                        "name": "ansible",
                        "configured_password": "pass_ansible",
                        "update_password": "always",
                    },
                    {
                        "name": "newuser",
                        "configured_password": "pass_newuser",
                        "update_password": "always",
                    },
                ],
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("username ansible secret pass_ansible", result["commands"])
        self.assertIn("username newuser secret pass_newuser", result["commands"])

    def test_aggregate_per_item_password_type(self):
        # password_type per aggregate item applies independently to each user's command.
        set_module_args(
            dict(
                aggregate=[
                    {
                        "name": "newuser1",
                        "configured_password": "pass1",
                        "password_type": "password",
                    },
                    {"name": "newuser2", "configured_password": "pass2"},
                ],
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("username newuser1 password pass1", result["commands"])
        self.assertIn("username newuser2 secret pass2", result["commands"])

    def test_aggregate_hashed_password_type_and_value_mismatch(self):
        # ansible (exists in fixture with type=5): same hash → no command.
        # newuser1: different type (9) → update required.
        # newuser2: same type (5) but different value → update required.
        set_module_args(
            dict(
                aggregate=[
                    {
                        "name": "ansible",
                        "hashed_password": {
                            "type": 5,
                            "value": "$1$3yWSXiIi$VdzV59ChiurrNdGxlDeAW/",
                        },
                    },
                    {
                        "name": "newuser1",
                        "hashed_password": {"type": 9, "value": "newscryptvalue"},
                    },
                    {
                        "name": "newuser2",
                        "hashed_password": {"type": 5, "value": "differenthash"},
                    },
                ],
            ),
        )
        result = self.execute_module(changed=True)
        self.assertNotIn(
            "username ansible secret 5 $1$3yWSXiIi$VdzV59ChiurrNdGxlDeAW/",
            result["commands"],
        )
        self.assertIn("username newuser1 secret 9 newscryptvalue", result["commands"])
        self.assertIn("username newuser2 secret 5 differenthash", result["commands"])

    def test_aggregate_hashed_password_on_create_does_not_suppress_hash_comparison(self):
        # update_password=on_create does NOT suppress hashed_password updates (unlike
        # configured_password). Hash+type comparison always runs.
        # ansible (exists): same hash + on_create → no change.
        # newuser: different hash + on_create → still generates command.
        set_module_args(
            dict(
                aggregate=[
                    {
                        "name": "ansible",
                        "hashed_password": {
                            "type": 5,
                            "value": "$1$3yWSXiIi$VdzV59ChiurrNdGxlDeAW/",
                        },
                        "update_password": "on_create",
                    },
                    {
                        "name": "newuser",
                        "hashed_password": {"type": 9, "value": "scryptvalue"},
                        "update_password": "on_create",
                    },
                ],
            ),
        )
        result = self.execute_module(changed=True)
        self.assertNotIn(
            "username ansible secret 5 $1$3yWSXiIi$VdzV59ChiurrNdGxlDeAW/",
            result["commands"],
        )
        self.assertIn("username newuser secret 9 scryptvalue", result["commands"])
