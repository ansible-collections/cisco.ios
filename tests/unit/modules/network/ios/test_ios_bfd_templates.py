#
# (c) 2025, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_bfd_templates
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosBfdTemplatesModule(TestIosModule):
    module = ios_bfd_templates

    def setUp(self):
        super(TestIosBfdTemplatesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bfd_templates.bfd_templates."
            "Bfd_templatesFacts.get_bfd_templates_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBfdTemplatesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_bfd_templates_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {"type": "sha_1", "keychain": "bfd_keychain"},
                        "echo": True,
                    },
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {"min_tx": 500, "min_rx": 500, "multiplier": 5},
                        "dampening": {
                            "half_life_period": 30,
                            "reuse_threshold": 2000,
                            "suppress_threshold": 5000,
                            "max_suppress_time": 54,
                        },
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "interval min-tx 200 min-rx 200 multiplier 3",
            "authentication sha-1 keychain bfd_keychain",
            "echo",
            "bfd-template multi-hop template2",
            "interval min-tx 500 min-rx 500 multiplier 5",
            "dampening 30 2000 5000 54",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain bfd_keychain
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {"type": "sha_1", "keychain": "bfd_keychain"},
                        "echo": True,
                    },
                ],
                "state": "merged",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_bfd_templates_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain bfd_keychain
             echo
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 4},
                        "authentication": {"type": "sha_1", "keychain": "new_keychain"},
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no echo",
            "interval min-tx 300 min-rx 300 multiplier 4",
            "no authentication sha-1 keychain bfd_keychain",
            "authentication sha-1 keychain new_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 300 min-rx 300 multiplier 4
             authentication sha-1 keychain new_keychain
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 4},
                        "authentication": {"type": "sha_1", "keychain": "new_keychain"},
                    },
                ],
                "state": "replaced",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_bfd_templates_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            bfd-template single-hop template3
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 5},
                        "authentication": {"type": "md5", "keychain": "secure_key"},
                    },
                ],
                "state": "overridden",
            },
        )
        commands = [
            "no bfd-template multi-hop template2",
            "no bfd-template single-hop template3",
            "bfd-template single-hop template1",
            "interval min-tx 300 min-rx 300 multiplier 5",
            "authentication md5 keychain secure_key",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 300 min-rx 300 multiplier 5
             authentication md5 keychain secure_key
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 5},
                        "authentication": {"type": "md5", "keychain": "secure_key"},
                    },
                ],
                "state": "overridden",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_bfd_templates_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain bfd_keychain
             echo
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "config": [
                    {"name": "template1", "hop": "single_hop"},
                ],
                "state": "deleted",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no echo",
            "no interval min-tx 200 min-rx 200 multiplier 3",
            "no authentication sha-1 keychain bfd_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "state": "deleted",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no interval min-tx 200 min-rx 200 multiplier 3",
            "bfd-template multi-hop template2",
            "no interval min-tx 500 min-rx 500 multiplier 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_purged(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "config": [
                    {"name": "template1", "hop": "single_hop"},
                ],
                "state": "purged",
            },
        )
        commands = ["no bfd-template single-hop template1"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_rendered(self):
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {
                            "type": "meticulous_sha_1",
                            "keychain": "secure_chain",
                        },
                        "echo": True,
                    },
                ],
                "state": "rendered",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "interval min-tx 200 min-rx 200 multiplier 3",
            "authentication meticulous-sha-1 keychain secure_chain",
            "echo",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    def test_ios_bfd_templates_parsed(self):
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    bfd-template single-hop template1
                     interval min-tx 200 min-rx 200 multiplier 3
                     authentication sha-1 keychain bfd_keychain
                     echo
                    bfd-template multi-hop template2
                     dampening 30 2000 5000 54
                    """,
                ),
                "state": "parsed",
            },
        )
        parsed = [
            {
                "authentication": {"keychain": "bfd_keychain", "type": "sha_1"},
                "echo": True,
                "hop": "single_hop",
                "interval": {"min_rx": 200, "min_tx": 200, "multiplier": 3},
                "name": "template1",
            },
            {
                "dampening": {
                    "half_life_period": 30,
                    "max_suppress_time": 54,
                    "reuse_threshold": 2000,
                    "suppress_threshold": 5000,
                },
                "hop": "multi_hop",
                "name": "template2",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_ios_bfd_templates_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain bfd_keychain
             echo
            bfd-template multi-hop template2
             dampening 30 2000 5000 54
            """,
        )
        set_module_args(
            {
                "state": "gathered",
            },
        )
        gathered = [
            {
                "authentication": {"keychain": "bfd_keychain", "type": "sha_1"},
                "echo": True,
                "hop": "single_hop",
                "interval": {"min_rx": 200, "min_tx": 200, "multiplier": 3},
                "name": "template1",
            },
            {
                "dampening": {
                    "half_life_period": 30,
                    "max_suppress_time": 54,
                    "reuse_threshold": 2000,
                    "suppress_threshold": 5000,
                },
                "hop": "multi_hop",
                "name": "template2",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_bfd_templates_authentication_types(self):
        """Test all authentication types"""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        for auth_type, cli_type in [
            ("sha_1", "sha-1"),
            ("md5", "md5"),
            ("meticulous_md5", "meticulous-md5"),
            ("meticulous_sha_1", "meticulous-sha-1"),
        ]:
            set_module_args(
                {
                    "config": [
                        {
                            "name": "test_template",
                            "hop": "single_hop",
                            "authentication": {"type": auth_type, "keychain": "test_key"},
                        },
                    ],
                    "state": "merged",
                },
            )
            commands = [
                "bfd-template single-hop test_template",
                f"authentication {cli_type} keychain test_key",
            ]
            result = self.execute_module(changed=True)
            self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_add_authentication(self):
        """Test adding authentication to existing template without auth"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {"type": "sha_1", "keychain": "new_keychain"},
                        "echo": True,
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "authentication sha-1 keychain new_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_remove_authentication(self):
        """Test removing authentication completely from template"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain bfd_keychain
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "echo": True,
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no authentication sha-1 keychain bfd_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_change_authentication_type(self):
        """Test changing authentication type from md5 to sha-1"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication md5 keychain old_keychain
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {"type": "sha_1", "keychain": "new_keychain"},
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no authentication md5 keychain old_keychain",
            "authentication sha-1 keychain new_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_change_authentication_keychain_only(self):
        """Test changing only keychain with same authentication type"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             authentication sha-1 keychain old_keychain
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "authentication": {"type": "sha_1", "keychain": "new_keychain"},
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "no authentication sha-1 keychain old_keychain",
            "authentication sha-1 keychain new_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_add_dampening(self):
        """Test adding dampening to existing template"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {"min_tx": 500, "min_rx": 500, "multiplier": 5},
                        "dampening": {
                            "half_life_period": 30,
                            "reuse_threshold": 2000,
                            "suppress_threshold": 5000,
                            "max_suppress_time": 120,
                        },
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template multi-hop template2",
            "dampening 30 2000 5000 120",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_remove_dampening(self):
        """Test removing dampening from template"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
             dampening 30 2000 5000 120
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {"min_tx": 500, "min_rx": 500, "multiplier": 5},
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template multi-hop template2",
            "no dampening 30 2000 5000 120",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_update_interval_only(self):
        """Test updating only interval values"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 5},
                        "echo": True,
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "interval min-tx 300 min-rx 300 multiplier 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_overridden_multiple_changes(self):
        """Test overridden with multiple existing templates - keep one, modify one, delete one"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
             echo
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            bfd-template single-hop template3
             authentication sha-1 keychain old_key
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 300, "min_rx": 300, "multiplier": 4},
                    },
                ],
                "state": "overridden",
            },
        )
        commands = [
            "no bfd-template multi-hop template2",
            "no bfd-template single-hop template3",
            "bfd-template single-hop template1",
            "no echo",
            "interval min-tx 300 min-rx 300 multiplier 4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_deleted_idempotent(self):
        """Test deleting already deleted template"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            """,
        )
        set_module_args(
            {
                "config": [
                    {"name": "template1", "hop": "single_hop"},
                ],
                "state": "deleted",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_bfd_templates_purged_multiple(self):
        """Test purging multiple templates"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
            bfd-template single-hop template3
             echo
            """,
        )
        set_module_args(
            {
                "config": [
                    {"name": "template1", "hop": "single_hop"},
                    {"name": "template3", "hop": "single_hop"},
                ],
                "state": "purged",
            },
        )
        commands = [
            "no bfd-template single-hop template1",
            "no bfd-template single-hop template3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_add_echo(self):
        """Test adding echo to template without echo"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {"min_tx": 200, "min_rx": 200, "multiplier": 3},
                        "echo": True,
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "echo",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_echo_only(self):
        """Test adding only echo to existing template"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 200 min-rx 200 multiplier 3
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "echo": True,
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template single-hop template1",
            "echo",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_replaced_dampening_to_authentication(self):
        """Test replacing dampening with authentication"""
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template multi-hop template2
             interval min-tx 500 min-rx 500 multiplier 5
             dampening 30 2000 5000 120
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {"min_tx": 500, "min_rx": 500, "multiplier": 5},
                        "authentication": {"type": "md5", "keychain": "new_key"},
                    },
                ],
                "state": "replaced",
            },
        )
        commands = [
            "bfd-template multi-hop template2",
            "no dampening 30 2000 5000 120",
            "authentication md5 keychain new_key",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_bfd_templates_merged_dampening_only(self):
        """Test adding only dampening without other parameters"""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            {
                "config": [
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "dampening": {
                            "half_life_period": 30,
                            "reuse_threshold": 2000,
                            "suppress_threshold": 5000,
                            "max_suppress_time": 120,
                        },
                    },
                ],
                "state": "merged",
            },
        )
        commands = [
            "bfd-template multi-hop template2",
            "dampening 30 2000 5000 120",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)
