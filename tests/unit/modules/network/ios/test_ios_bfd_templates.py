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
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 500,
                            "min_rx": 500,
                            "multiplier": 3,
                        },
                        "echo": True,
                    },
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {
                            "min_tx": 1000,
                            "min_rx": 1000,
                            "multiplier": 5,
                        },
                        "dampening": {
                            "half_life_period": 2,
                            "reuse_threshold": 1000,
                            "suppress_threshold": 3000,
                            "max_suppress_time": 8,
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "bfd-template single-hop template1",
            "interval min-tx 500 min-rx 500 multiplier 3",
            "echo",
            "bfd-template multi-hop template2",
            "interval min-tx 1000 min-rx 1000 multiplier 5",
            "dampening 2 1000 3000 8",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
             dampening 2 1000 3000 8
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 500,
                            "min_rx": 500,
                            "multiplier": 3,
                        },
                        "echo": True,
                    },
                    {
                        "name": "template2",
                        "hop": "multi_hop",
                        "interval": {
                            "min_tx": 1000,
                            "min_rx": 1000,
                            "multiplier": 5,
                        },
                        "dampening": {
                            "half_life_period": 2,
                            "reuse_threshold": 1000,
                            "suppress_threshold": 3000,
                            "max_suppress_time": 8,
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_merged_with_authentication(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "secure_template",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 300,
                            "min_rx": 300,
                            "multiplier": 4,
                        },
                        "authentication": {
                            "authentication_type": "sha-1",
                            "chain_name": "bfd_keychain",
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "bfd-template single-hop secure_template",
            "interval min-tx 300 min-rx 300 multiplier 4",
            "authentication sha-1 keychain bfd_keychain",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 1000,
                            "min_rx": 1000,
                            "multiplier": 5,
                        },
                        "echo": False,
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "bfd-template single-hop template1",
            "interval min-tx 1000 min-rx 1000 multiplier 5",
            "no echo",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 1000 min-rx 1000 multiplier 5
             no echo
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 1000,
                            "min_rx": 1000,
                            "multiplier": 5,
                        },
                        "echo": False,
                    },
                ],
                state="replaced",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "new_template",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 200,
                            "min_rx": 200,
                            "multiplier": 6,
                        },
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "no bfd-template single-hop template1",
            "no bfd-template multi-hop template2",
            "bfd-template single-hop new_template",
            "interval min-tx 200 min-rx 200 multiplier 6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop new_template
             interval min-tx 200 min-rx 200 multiplier 6
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "new_template",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 200,
                            "min_rx": 200,
                            "multiplier": 6,
                        },
                    },
                ],
                state="overridden",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_deleted_single(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "no bfd-template single-hop template1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
            """,
        )
        set_module_args(
            dict(
                config=[],
                state="deleted",
            ),
        )
        commands = [
            "no bfd-template single-hop template1",
            "no bfd-template multi-hop template2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_deleted_blank(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[],
                state="deleted",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_rendered(self):
        set_module_args(
            dict(
                config=[
                    {
                        "name": "rendered_template",
                        "hop": "single_hop",
                        "interval": {
                            "min_tx": 400,
                            "min_rx": 400,
                            "multiplier": 4,
                        },
                        "authentication": {
                            "authentication_type": "md5",
                            "chain_name": "my_keychain",
                        },
                        "echo": True,
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "bfd-template single-hop rendered_template",
            "interval min-tx 400 min-rx 400 multiplier 4",
            "authentication md5 keychain my_keychain",
            "echo",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_bfd_templates_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    bfd-template single-hop template1
                     interval min-tx 500 min-rx 500 multiplier 3
                     echo
                    !
                    bfd-template multi-hop template2
                     interval min-tx 1000 min-rx 1000 multiplier 5
                     dampening 2 1000 3000 8
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "name": "template1",
                "hop": "single_hop",
                "interval": {
                    "min_tx": 500,
                    "min_rx": 500,
                    "multiplier": 3,
                },
                "echo": True,
            },
            {
                "name": "template2",
                "hop": "multi_hop",
                "interval": {
                    "min_tx": 1000,
                    "min_rx": 1000,
                    "multiplier": 5,
                },
                "dampening": {
                    "half_life_period": 2,
                    "reuse_threshold": 1000,
                    "suppress_threshold": 3000,
                    "max_suppress_time": 8,
                },
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_ios_bfd_templates_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
             dampening 2 1000 3000 8
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
        )
        gathered = [
            {
                "name": "template1",
                "hop": "single_hop",
                "interval": {
                    "min_tx": 500,
                    "min_rx": 500,
                    "multiplier": 3,
                },
                "echo": True,
            },
            {
                "name": "template2",
                "hop": "multi_hop",
                "interval": {
                    "min_tx": 1000,
                    "min_rx": 1000,
                    "multiplier": 5,
                },
                "dampening": {
                    "half_life_period": 2,
                    "reuse_threshold": 1000,
                    "suppress_threshold": 3000,
                    "max_suppress_time": 8,
                },
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_bfd_templates_purged_single(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "template1",
                        "hop": "single_hop",
                    },
                ],
                state="purged",
            ),
        )
        commands = [
            "no bfd-template single-hop template1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_purged_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            bfd-template single-hop template1
             interval min-tx 500 min-rx 500 multiplier 3
             echo
            !
            bfd-template multi-hop template2
             interval min-tx 1000 min-rx 1000 multiplier 5
            """,
        )
        set_module_args(
            dict(
                config=[],
                state="purged",
            ),
        )
        commands = [
            "no bfd-template single-hop template1",
            "no bfd-template multi-hop template2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bfd_templates_purged_blank(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[],
                state="purged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
