#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

import yaml

from ansible_collections.cisco.ios.plugins.modules import ios_static_routes
from ansible_collections.cisco.ios.plugins.modules.ios_static_routes import EXAMPLES as examples
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosStaticRoutesModule(TestIosModule):
    module = ios_static_routes

    def setUp(self):
        super(TestIosStaticRoutesModule, self).setUp()

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

        self.mock_EXAMPLE_check = examples
        self.test_core = self.test()

    def tearDown(self):
        super(TestIosStaticRoutesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test(self):
        """
        Main entry point for module execution

        :returns: the result form module invocation
        """

        def identify_yaml(string_data):
            try:
                yaml_data = yaml.safe_load(string_data)
                if yaml_data is None:
                    return False
                return True, yaml_data
            except yaml.YAMLError:
                return False, None

        print("off to module exec")
        _top_arg = {}
        state_split = self.mock_EXAMPLE_check.split("# Using")
        for _state in state_split:
            if len(_state) >= 10:
                _psudo_before, _task_args, operation_state = "", {}, ""
                _before, _playbook, _commands = None, None, None
                # just state
                print("*************************************")
                print(_state)
                print("*************************************")
                top_split = _state.split("- name")
                find_before = top_split[0].split("-------------")

                for _st in [
                    "merged",
                    "replaced",
                    "overridden",
                    "purged",
                    "gathered",
                    "rendered",
                    "parsed",
                    "deleted",
                    "present",
                    "absent",
                ]:
                    if _st in find_before[0].lower():
                        operation_state = _st  # operation state is stored

                if operation_state != "rendered":
                    find_before = find_before[1].replace("#", "")
                    find_before = find_before.split(
                        "\n ",
                    )

                    for line in find_before:
                        if line != "" and "show running-config" not in line:
                            _psudo_before += line + "\n"
                    _before = dedent(_psudo_before)  # before config is stored

                find_playbook = top_split[1].split("# Task Output")
                probable_playbook = "- name" + find_playbook[0]
                is_playbook, _playbook = identify_yaml(
                    probable_playbook,
                )  # playbook is scrapped out

                if operation_state not in ["parsed", "gathered"]:
                    if operation_state == "rendered":
                        extract_commands_to_assert = (find_playbook[1].split("# rendered:"))[1]
                    else:
                        extract_commands_to_assert = (find_playbook[1].split("# commands:"))[1]

                    extract_commands_to_assert = (extract_commands_to_assert.split("# after:"))[0]
                    is_commands, _commands = identify_yaml(
                        extract_commands_to_assert.replace("#", ""),
                    )  # commands to assert is scrapped

                    if is_playbook and is_commands:
                        _top_arg[operation_state] = {
                            "operation_state": operation_state,
                            "before": _before,
                            "playbook": _playbook,
                            "commands": _commands,
                        }
                else:
                    if operation_state == "gathered":
                        extract_commands_to_assert = (find_playbook[1].split("# gathered:"))[1]
                    if operation_state == "parsed":
                        extract_commands_to_assert = (find_playbook[1].split("# parsed:"))[1]
                    extract_commands_to_assert = "gathered:" + extract_commands_to_assert
                    is_commands, _commands = identify_yaml(
                        extract_commands_to_assert.replace("#", ""),
                    )
                    _top_arg[operation_state] = {
                        "operation_state": operation_state,
                        "before": _before,
                        "playbook": _playbook,
                        "structured_data": _commands,
                    }

                print("_--------------------------------------_")
                print(_top_arg)
                # _top_arg.append(_task_args)
                print("_--------------------------------------_")

        print("Debug here")
        return _top_arg

    def test_ios_static_routes_merged(self):
        test_vars = self.test_core.get("merged")
        self.execute_show_command.return_value = test_vars.get("before")
        set_module_args(
            dict(
                config=test_vars.get("playbook")[0]["cisco.ios.ios_static_routes"]["config"],
                state=test_vars.get("operation_state"),
            ),
        )
        result = self.execute_module(changed=True)
        commands = test_vars.get("commands")
        self.assertEqual(sorted(result["commands"]), sorted(commands))
