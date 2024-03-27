#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_lacp
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLacpModule(TestIosModule):
    module = ios_lacp

    def setUp(self):
        super(TestIosLacpModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lacp.lacp."
            "LacpFacts.get_lacp_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLacpModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_lacp_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            123, 5e00.0000.8000
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 32768}},
                state="merged",
            ),
        )
        commands = ["lacp system-priority 32768"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            123, 5e00.0000.8000
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 123}},
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_ios_lacp_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            123, 5e00.0000.8000
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 12300}},
                state="replaced",
            ),
        )
        commands = ["lacp system-priority 12300"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            123, 5e00.0000.8000
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 12300}},
                state="overridden",
            ),
        )
        commands = ["lacp system-priority 12300"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            123, 5e00.0000.8000
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 1}},
                state="deleted",
            ),
        )
        commands = ["no lacp system-priority"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lacp_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    123, 5e00.0000.8000
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {"system": {"priority": 123}}
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_lacp_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config={"system": {"priority": 123}},
                state="rendered",
            ),
        )
        commands = ["lacp system-priority 123"]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
