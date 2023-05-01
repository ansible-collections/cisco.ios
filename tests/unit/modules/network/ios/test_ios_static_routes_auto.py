#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_static_routes
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args
from ansible_collections.cisco.ios.tests.unit.unit_utils.module_dynamic_test_generator import (
    TestGeneratorFromModuleExamples,
)

from .ios_module import TestIosModule


class TestIosStaticRoutesModuleAuto(TestIosModule):
    module = ios_static_routes

    def setUp(self):
        super(TestIosStaticRoutesModuleAuto, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.static_routes.static_routes."
            "Static_routesFacts.get_static_routes_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.dyanmic_test_obj = TestGeneratorFromModuleExamples(ios_static_routes)
        self.test_asset = self.dyanmic_test_obj.extract_test_asset_from_example()

    def tearDown(self):
        super(TestIosStaticRoutesModuleAuto, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_static_routes_auto(self):
        for key, test_vars in self.test_asset.items():
            self.execute_show_command.return_value = test_vars.get("device_config")
            set_module_args(
                dict(
                    config=test_vars.get("config"),
                    state=test_vars.get("state"),
                ),
            )
            result = self.execute_module(changed=test_vars.get("changed"))
            commands = test_vars.get("commands")
            self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_static_routes_overridden(self):
        test_vars = self.test_core.get("overridden")
        self.execute_show_command.return_value = test_vars.get("before")
        set_module_args(
            dict(
                config=test_vars.get("config"),
                state=test_vars.get("operation_state"),
            ),
        )
        result = self.execute_module(changed=True)
        commands = test_vars.get("commands")
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_static_routes_replaced(self):
        test_vars = self.test_core.get("replaced")
        self.execute_show_command.return_value = test_vars.get("before")
        set_module_args(
            dict(
                config=test_vars.get("config"),
                state=test_vars.get("operation_state"),
            ),
        )
        result = self.execute_module(changed=True)
        commands = test_vars.get("commands")
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_static_routes_rendered(self):
        test_vars = self.test_core.get("rendered")
        self.execute_show_command.return_value = test_vars.get("before")
        set_module_args(
            dict(
                config=test_vars.get("config"),
                state=test_vars.get("operation_state"),
            ),
        )
        result = self.execute_module(changed=False)
        commands = test_vars.get("commands")
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    # def test_ios_static_routes_gathered(self):
    #     test_vars = self.test_core.get("gathered")
    #     self.execute_show_command.return_value = test_vars.get("before")
    #     set_module_args(
    #         dict(
    #             config=test_vars.get("config"),
    #             state=test_vars.get("operation_state"),
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     commands = test_vars.get("structured_data").get("gathered")
    #     self.assertEqual(result["gathered"], commands)
