#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_lldp_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLldpGlobalModule(TestIosModule):
    module = ios_lldp_global

    def setUp(self):
        super(TestIosLldpGlobalModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lldp_global.lldp_global."
            "Lldp_globalFacts.get_lldp_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLldpGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_lldp_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            lldp timer 10
            lldp holdtime 10
            lldp reinit 3
            lldp run
            """,
        )
        set_module_args(
            dict(
                config={"timer": 20, "holdtime": 10, "reinit": 3, "enabled": True},
                state="merged",
            ),
        )
        commands = ["lldp timer 20"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            lldp timer 10
            lldp holdtime 10
            lldp reinit 3
            lldp run
            """,
        )
        set_module_args(
            dict(
                config={"timer": 10, "holdtime": 10, "reinit": 3, "enabled": True},
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_ios_lldp_global_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            lldp timer 10
            lldp holdtime 10
            lldp reinit 3
            lldp run
            """,
        )
        set_module_args(
            dict(
                config={"timer": 15, "reinit": 9},
                state="replaced",
            ),
        )
        commands = ["no lldp holdtime", "no lldp run", "lldp timer 15", "lldp reinit 9"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            lldp timer 10
            lldp holdtime 10
            lldp reinit 3
            lldp run
            """,
        )
        set_module_args(
            dict(
                config={"timer": 15, "reinit": 9},
                state="overridden",
            ),
        )
        commands = ["no lldp holdtime", "no lldp run", "lldp timer 15", "lldp reinit 9"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            lldp timer 10
            lldp holdtime 10
            lldp reinit 3
            lldp run
            """,
        )
        set_module_args(
            dict(
                config={"timer": 15, "reinit": 9},
                state="deleted",
            ),
        )
        commands = [
            "no lldp holdtime",
            "no lldp run",
            "no lldp timer",
            "no lldp reinit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_lldp_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    lldp timer 10
                    lldp holdtime 10
                    lldp reinit 3
                    lldp run
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {"timer": 10, "holdtime": 10, "reinit": 3, "enabled": True}
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_lldp_global_rendered(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config={"timer": 10, "holdtime": 10, "reinit": 3, "enabled": True},
                state="rendered",
            ),
        )
        commands = ["lldp holdtime 10", "lldp run", "lldp timer 10", "lldp reinit 3"]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
