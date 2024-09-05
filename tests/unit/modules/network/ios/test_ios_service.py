#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_service
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosServiceModule(TestIosModule):
    module = ios_service

    def setUp(self):
        super(TestIosServiceModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.service.service."
            "ServiceFacts.get_service_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosServiceModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_service_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            service slave-log
            service tcp-keepalives-in
            service tcp-keepalives-out
            service timestamps debug datetime msec
            service timestamps log datetime msec
            service private-config-encryption
            service prompt config
            service counters max age 0
            service dhcp
            service call-home
            service password-recovery
            """,
        )

        playbook = {
            "config": {
                "call_home": True,
                "tcp_keepalives_in": True,
                "tcp_keepalives_out": True,
                "timestamps": [
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                    {
                        "msg": "debug",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                ],
            },
        }
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_service_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            service slave-log
            service tcp-keepalives-in
            service tcp-keepalives-out
            service timestamps debug datetime msec
            service timestamps log datetime msec
            service private-config-encryption
            service prompt config
            service counters max age 0
            service dhcp
            service call-home
            service password-recovery
            """,
        )

        playbook = {
            "config": {
                "tcp_keepalives_in": True,
                "tcp_keepalives_out": True,
                "timestamps": [
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "localtime": True,
                            "msec": True,
                            "show_timezone": True,
                            "year": True,
                        },
                    },
                    {
                        "msg": "debug",
                        "timestamp": "uptime",
                    },
                ],
                "pad": False,
                "password_encryption": True,
            },
        }
        merged = [
            "service password-encryption",
            "service timestamps debug uptime msec",
            "service timestamps log datetime msec localtime show-timezone year",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_snm_server_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            service slave-log
            service tcp-keepalives-in
            service tcp-keepalives-out
            service timestamps debug datetime msec
            service timestamps log datetime msec localtime show-timezone year
            service password-encryption
            service private-config-encryption
            service prompt config
            service counters max age 0
            service dhcp
            service call-home
            service password-recovery
            """,
        )
        playbook = {"config": {}}
        deleted = [
            "no service tcp-keepalives-in",
            "no service tcp-keepalives-out",
            "no service timestamps debug",
            "no service timestamps log",
            "no service password-encryption",
            "no service call-home",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        self.maxDiff = None
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_service_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            service call-home
            service config
            service counters max age 0
            service dhcp
            service pad
            service password-recovery
            service private-config-encryption
            service prompt config
            service slave-log
            service timestamps log datetime msec
            """,
        )
        playbook = {
            "config": {
                "timestamps": [
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "localtime": True,
                            "msec": True,
                            "show_timezone": True,
                            "year": True,
                        },
                    },
                    {
                        "msg": "debug",
                        "timestamp": "datetime",
                    },
                ],
                "tcp_keepalives_in": True,
                "tcp_keepalives_out": True,
                "password_encryption": True,
                "counters": 5,
            },
        }
        overridden = [
            "no service call-home",
            "no service config",
            "service counters max age 5",
            "no service pad",
            "service password-encryption",
            "service tcp-keepalives-in",
            "service tcp-keepalives-out",
            "service timestamps log datetime msec localtime show-timezone year",
            "service timestamps debug datetime",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_service_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            service call-home
            service config
            service counters max age 0
            service dhcp
            service pad
            service password-recovery
            service private-config-encryption
            service prompt config
            service slave-log
            service timestamps log datetime msec
            """,
        )
        playbook = {
            "config": {
                "timestamps": [
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "localtime": True,
                            "msec": True,
                            "show_timezone": True,
                            "year": True,
                        },
                    },
                    {
                        "msg": "debug",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "localtime": True,
                            "msec": True,
                        },
                    },
                ],
                "tcp_keepalives_in": True,
                "tcp_keepalives_out": True,
                "password_encryption": True,
                "counters": 5,
            },
        }
        replaced = [
            "no service call-home",
            "no service config",
            "service counters max age 5",
            "no service pad",
            "service password-encryption",
            "service tcp-keepalives-in",
            "service tcp-keepalives-out",
            "service timestamps log datetime msec localtime show-timezone year",
            "service timestamps debug datetime msec localtime",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(replaced))

    def test_ios_service_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            service slave-log
            service timestamps debug datetime msec
            service timestamps log datetime msec
            service private-config-encryption
            service prompt config
            service counters max age 0
            service dhcp
            service call-home
            service password-recovery
            """,
        )
        playbook = {
            "config": {
                "call_home": True,
                "timestamps": [
                    {
                        "msg": "debug",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                ],
            },
        }
        replaced = []
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.maxDiff = None

        self.assertEqual(sorted(result["commands"]), sorted(replaced))

    def test_ios_service_replaced_idempotent_old(self):
        self.execute_show_command.return_value = dedent(
            """\
            service slave-log
            service timestamps debug datetime msec
            service timestamps log datetime msec
            service prompt config
            service counters max age 0
            service dhcp
            service call-home
            service password-recovery
            """,
        )
        playbook = {
            "config": {
                "call_home": True,
                "timestamps": [
                    {
                        "msg": "debug",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                    {
                        "msg": "log",
                        "timestamp": "datetime",
                        "datetime_options": {
                            "msec": True,
                        },
                    },
                ],
            },
        }
        replaced = []
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.maxDiff = None

        self.assertEqual(sorted(result["commands"]), sorted(replaced))

    def test_ios_service_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    service slave-log
                    service timestamps debug datetime msec
                    service timestamps log datetime msec
                    service private-config-encryption
                    service prompt config
                    service counters max age 0
                    service dhcp
                    service call-home
                    service password-recovery
                    """,
                ),
                state="parsed",
            ),
        )

        parsed = {
            "timestamps": [
                {
                    "msg": "debug",
                    "timestamp": "datetime",
                    "datetime_options": {
                        "msec": True,
                    },
                },
                {
                    "msg": "log",
                    "timestamp": "datetime",
                    "datetime_options": {
                        "msec": True,
                    },
                },
            ],
            "prompt": True,
            "private_config_encryption": True,
            "counters": 0,
            "dhcp": True,
            "call_home": True,
            "password_recovery": True,
            "slave_log": True,
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None

        self.assertEqual(result["parsed"], parsed)

    def test_ios_service_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            service timestamps log datetime msec localtime show-timezone year
            service timestamps debug uptime
            service call-home
            service udp-small-servers
            service tcp-small-servers no-limit
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = {
            "timestamps": [
                {
                    "msg": "log",
                    "timestamp": "datetime",
                    "datetime_options": {
                        "msec": True,
                        "localtime": True,
                        "show_timezone": True,
                        "year": True,
                    },
                },
                {"msg": "debug", "timestamp": "uptime"},
            ],
            "call_home": True,
            "udp_small_servers": {"enable": True},
            "tcp_small_servers": {"enable": True, "no_limit": True},
            "counters": 0,
            "dhcp": True,
            "password_recovery": True,
            "prompt": True,
            "slave_log": True,
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_service_rendered(self):
        set_module_args(
            {
                "config": {
                    "call_home": True,
                    "counters": 5,
                    "config": False,
                    "pad": False,
                    "tcp_keepalives_in": True,
                    "tcp_keepalives_out": True,
                    "timestamps": [
                        {
                            "msg": "debug",
                            "timestamp": "uptime",
                            "datetime_options": {
                                "localtime": True,
                            },
                        },
                        {
                            "msg": "log",
                            "timestamp": "datetime",
                            "datetime_options": {
                                "localtime": True,
                                "msec": True,
                                "show_timezone": True,
                                "year": True,
                            },
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = [
            "service call-home",
            "service counters max age 5",
            "service dhcp",
            "service password-recovery",
            "service prompt config",
            "service slave-log",
            "service tcp-keepalives-in",
            "service tcp-keepalives-out",
            "service timestamps debug uptime localtime",
            "service timestamps log datetime msec localtime show-timezone year",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), sorted(rendered))
