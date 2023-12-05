#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_line
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosLineModule(TestIosModule):
    module = ios_line

    def setUp(self):
        super(TestIosLineModule, self).setUp()
        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.line.line."
            "LineFacts.get_line_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLineModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_line_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    line con 0
                     session-timeout 5
                     exec-timeout 60 0
                     authorization exec CON
                     login authentication CON
                     escape-character 3
                     stopbits 1
                    line vty 0 4
                     session-timeout 5
                     exec-timeout 60 0
                     logging synchronous
                     transport preferred none
                     transport input telnet ssh
                     transport output ssh
                     escape-character 3
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = {
            "lines": [
                {
                    "name": "con 0",
                    "authorization": {
                        "arap": "default",
                        "exec": "CON",
                        "reverse_access": "default",
                    },
                    "escape_character": {
                        "value": "3",
                    },
                    "exec": {
                        "timeout": 60,
                    },
                    "login": "CON",
                    "motd": True,
                    "session": {
                        "timeout": 5,
                    },
                    "stopbits": "1",
                },
                {
                    "name": "vty 0 4",
                    "escape_character": {
                        "value": "3",
                    },
                    "exec": {
                        "timeout": 60,
                    },
                    "logging": {
                        "enable": True,
                    },
                    "login": "default",
                    "motd": True,
                    "session": {
                        "timeout": 5,
                    },
                    "transport": [
                        {
                            "name": "preferred",
                            "none": True,
                        },
                        {
                            "name": "input",
                            "telnet": True,
                            "ssh": True,
                        },
                        {
                            "name": "output",
                            "ssh": True,
                        },
                    ],
                },
            ],
        }

        result = self.execute_module(changed=False)
        self.assertEqual(parsed, result["parsed"])

    def test_ios_line_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             authorization exec CON
             login authentication CON
             escape-character 3
             stopbits 1
            line vty 0 4
             session-timeout 5
             exec-timeout 60 0
             logging synchronous
             transport preferred none
             transport input telnet ssh
             transport output ssh
             escape-character 3
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = {
            "lines": [
                {
                    "name": "con 0",
                    "authorization": {
                        "arap": "default",
                        "exec": "CON",
                        "reverse_access": "default",
                    },
                    "escape_character": {
                        "value": "3",
                    },
                    "exec": {
                        "timeout": 60,
                    },
                    "login": "CON",
                    "motd": True,
                    "session": {
                        "timeout": 5,
                    },
                    "stopbits": "1",
                },
                {
                    "name": "vty 0 4",
                    "escape_character": {
                        "value": "3",
                    },
                    "exec": {
                        "timeout": 60,
                    },
                    "logging": {
                        "enable": True,
                    },
                    "login": "default",
                    "motd": True,
                    "session": {
                        "timeout": 5,
                    },
                    "transport": [
                        {
                            "name": "preferred",
                            "none": True,
                        },
                        {
                            "name": "input",
                            "telnet": True,
                            "ssh": True,
                        },
                        {
                            "name": "output",
                            "ssh": True,
                        },
                    ],
                },
            ],
        }

        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(gathered, result["gathered"])

    def test_ios_line_rendered(self):
        set_module_args(
            {
                "config": {
                    "lines": [
                        {
                            "name": "con 0",
                            "authorization": {
                                "arap": "default",
                                "exec": "CON",
                                "reverse_access": "default",
                            },
                            "escape_character": {
                                "value": "3",
                            },
                            "exec": {
                                "timeout": 60,
                            },
                            "login": "CON",
                            "motd": True,
                            "session": {
                                "timeout": 5,
                            },
                            "stopbits": "1",
                        },
                        {
                            "name": "vty 0 4",
                            "escape_character": {
                                "value": "3",
                            },
                            "exec": {
                                "timeout": 60,
                            },
                            "logging": {
                                "enable": True,
                            },
                            "login": "default",
                            "motd": True,
                            "session": {
                                "timeout": 5,
                            },
                            "transport": [
                                {
                                    "name": "preferred",
                                    "none": True,
                                },
                                {
                                    "name": "input",
                                    "telnet": True,
                                    "ssh": True,
                                },
                                {
                                    "name": "output",
                                    "ssh": True,
                                },
                            ],
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = [
            "line con 0",
            "session-timeout 5",
            "exec-timeout 60 0",
            "authorization exec CON",
            "login authentication CON",
            "escape-character 3",
            "stopbits 1",
            "line vty 0 4",
            "session-timeout 5",
            "exec-timeout 60 0",
            "logging synchronous",
            "transport preferred none",
            "transport input telnet ssh",
            "transport output ssh",
            "escape-character 3",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None

        self.assertEqual(sorted(result["rendered"]), sorted(rendered))

    def test_ios_line_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             authorization exec CON
             login authentication CON
             escape-character 3
             stopbits 1
            line vty 0 4
             session-timeout 5
             exec-timeout 60 0
             logging synchronous
             transport preferred none
             transport input telnet ssh
             transport output ssh
             escape-character 3
            """,
        )

        playbook = {
            "config": {
                "lines": [
                    {
                        "name": "con 0",
                        "authorization": {
                            "exec": "CON",
                        },
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "login": "CON",
                        "session": {
                            "timeout": 5,
                        },
                        "stopbits": "1",
                    },
                    {
                        "name": "vty 0 4",
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "logging": {
                            "enable": True,
                        },
                        "login": "default",
                        "session": {
                            "timeout": 5,
                        },
                        "transport": [
                            {
                                "name": "preferred",
                                "none": True,
                            },
                            {
                                "name": "input",
                                "telnet": True,
                                "ssh": True,
                            },
                            {
                                "name": "output",
                                "ssh": True,
                            },
                        ],
                    },
                ],
            },
        }

        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_line_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             stopbits 1
            line vty 0 4
             session-timeout 5
             exec-timeout 60 0
             transport input ssh
            """,
        )

        playbook = {
            "config": {
                "lines": [
                    {
                        "name": "con 0",
                        "authorization": {
                            "exec": "CON",
                        },
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "login": "CON",
                        "session": {
                            "timeout": 5,
                        },
                        "stopbits": "1",
                    },
                    {
                        "name": "vty 0 4",
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "logging": {
                            "enable": True,
                        },
                        "login": "default",
                        "session": {
                            "timeout": 5,
                        },
                        "transport": [
                            {
                                "name": "preferred",
                                "none": True,
                            },
                            {
                                "name": "input",
                                "telnet": True,
                                "ssh": True,
                            },
                            {
                                "name": "output",
                                "ssh": True,
                            },
                        ],
                    },
                ],
            },
        }

        merged = [
            "line con 0",
            "authorization exec CON",
            "login authentication CON",
            "escape-character 3",
            "line vty 0 4",
            "logging synchronous",
            "transport preferred none",
            "transport input telnet ssh",
            "transport output ssh",
            "escape-character 3",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_line_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             authorization commands 15 CON
             password 7 02050D480809
             length 0
             stopbits 1
            line vty 0 4
             access-class filter in
             password 7 02050D480809
             transport input telnet
            line vty 5 15
             password 7 02050D480809
             length 0
             transport input telnet
            """,
        )
        playbook = {
            "config": {
                "lines": [
                    {
                        "name": "con 0",
                        "authorization": {
                            "exec": "CON",
                        },
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "login": "CON",
                        "session": {
                            "timeout": 5,
                        },
                        "stopbits": "1",
                    },
                    {
                        "name": "vty 0 4",
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "logging": {
                            "enable": True,
                        },
                        "login": "default",
                        "session": {
                            "timeout": 5,
                        },
                        "transport": [
                            {
                                "name": "preferred",
                                "none": True,
                            },
                            {
                                "name": "input",
                                "telnet": True,
                                "ssh": True,
                            },
                            {
                                "name": "output",
                                "ssh": True,
                            },
                        ],
                    },
                ],
            },
        }
        overridden = [
            "line con 0",
            "authorization exec CON",
            "login authentication CON",
            "escape-character 3",
            "no authorization commands 15 CON",
            "no length 0",
            "no password 7 02050D480809",
            "line vty 0 4",
            "exec-timeout 60 0",
            "logging synchronous",
            "transport preferred none",
            "transport input telnet ssh",
            "transport output ssh",
            "escape-character 3",
            "session-timeout 5",
            "no access-class filter in",
            "no password 7 02050D480809",
            "no line vty 5 15",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_line_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             authorization exec CON
             login authentication CON
             escape-character 3
             stopbits 1
            line vty 0 4
             session-timeout 5
             exec prompt expand
             exec-timeout 60 0
             logging synchronous
             transport preferred none
             transport input telnet ssh
             transport output ssh
             escape-character 3
            """,
        )
        playbook = {
            "config": {
                "lines": [
                    {
                        "name": "con 0",
                        "authorization": {
                            "exec": "CON",
                        },
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "timeout": 60,
                        },
                        "login": "CON",
                        "session": {
                            "timeout": 5,
                        },
                        "stopbits": "1",
                    },
                    {
                        "name": "vty 0 4",
                        "escape_character": {
                            "value": "3",
                        },
                        "exec": {
                            "prompt": {
                                "expand": True,
                            },
                            "timeout": 60,
                        },
                        "logging": {
                            "enable": True,
                        },
                        "login": "default",
                        "session": {
                            "timeout": 5,
                        },
                        "transport": [
                            {
                                "name": "preferred",
                                "none": True,
                            },
                            {
                                "name": "input",
                                "telnet": True,
                                "ssh": True,
                            },
                            {
                                "name": "output",
                                "ssh": True,
                            },
                        ],
                    },
                ],
            },
        }
        overridden = []
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=False)

        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_line_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            line con 0
             session-timeout 5
             exec-timeout 60 0
             authorization exec CON
             login authentication CON
             escape-character 3
             stopbits 1
            line vty 0 4
             session-timeout 5
             exec-timeout 60 0
             logging synchronous
             transport preferred none
             transport input telnet ssh
             transport output ssh
             escape-character 3
            line vty 5 15
             session-timeout 5
             exec-timeout 60 0
             logging synchronous
             transport preferred none
             transport input telnet ssh
             transport output ssh
             escape-character 3
            """,
        )

        playbook = {"config": {}}
        deleted = [
            "line con 0",
            "no session-timeout 5",
            "exec-timeout 10 0",
            "authorization exec default",
            "login authentication default",
            "escape-character DEFAULT",
            "no stopbits 1",
            "line vty 0 4",
            "no session-timeout 5",
            "exec-timeout 10 0",
            "no logging synchronous",
            "no transport preferred",
            "no transport input",
            "no transport output",
            "escape-character DEFAULT",
            "no line vty 5 15",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        self.maxDiff = None
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(deleted))
