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

    def _run_ip(self, running, config, state="merged", changed=True):
        self.execute_show_command.return_value = running
        args = {"state": state}
        if config is not None:
            args["config"] = config
        set_module_args(args)
        return self.execute_module(changed=changed)

    def test_ios_service_ip_merged(self):
        result = self._run_ip(
            "service dhcp\n",
            {
                "ip": {
                    "finger": True,
                    "source_route": True,
                    "rcmd": {"rsh_enable": True},
                    "tftp": {"source_interface": "GigabitEthernet0/0"},
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "ip finger",
                "ip source-route",
                "ip rcmd rsh-enable",
                "ip tftp source-interface GigabitEthernet0/0",
            ],
        )

    def test_ios_service_ip_merged_idempotent_and_the_source_interface_may_be_abbreviated(self):
        result = self._run_ip(
            "service dhcp\nip finger\nip scp server enable\nip tftp source-interface GigabitEthernet0/0\n"
            "ip ftp source-interface Loopback1\n",
            {
                "ip": {
                    "finger": True,
                    "scp_server": True,
                    "tftp": {"source_interface": "Gi0/0"},
                    "ftp": {"source_interface": "Loopback1"},
                },
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_ip_merged_keeps_what_is_not_in_the_task(self):
        result = self._run_ip(
            "service dhcp\nip finger\nip tftp source-interface GigabitEthernet0/0\n",
            {"ip": {"bootp_server": True}},
        )
        self.assertEqual(result["commands"], ["ip bootp server"])

    def test_ios_service_ip_merged_changes_a_source_interface(self):
        result = self._run_ip(
            "service dhcp\nip tftp source-interface GigabitEthernet0/0\n",
            {"ip": {"tftp": {"source_interface": "Vlan402"}}},
        )
        self.assertEqual(result["commands"], ["ip tftp source-interface Vlan402"])

    def test_ios_service_ip_false_turns_a_service_off(self):
        result = self._run_ip(
            "service dhcp\nip finger\nip scp server enable\nip rcmd rsh-enable\n",
            {"ip": {"finger": False, "scp_server": False, "rcmd": {"rsh_enable": False}}},
        )
        self.assertEqual(
            result["commands"],
            ["no ip finger", "no ip scp server enable", "no ip rcmd rsh-enable"],
        )

    def test_ios_service_ip_false_on_a_service_that_is_off_is_idempotent(self):
        # IOS prints "no ip finger" with "show running-config all", it is not a service that is on
        result = self._run_ip(
            "service dhcp\nno ip finger\nno ip bootp server\nno ip source-route\n",
            {"ip": {"finger": False, "bootp_server": False, "source_route": False}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_ip_replaced_removes_what_is_not_in_the_section(self):
        result = self._run_ip(
            "service dhcp\nip finger\nip scp server enable\nip tftp source-interface GigabitEthernet0/0\n",
            {"ip": {"scp_server": True}},
            state="replaced",
        )
        self.assertEqual(result["commands"], ["no ip finger", "no ip tftp source-interface"])

    def test_ios_service_ip_overridden_removes_what_is_not_in_the_section(self):
        result = self._run_ip(
            "service dhcp\nip bootp server\nip ftp source-interface Loopback1\n",
            {"ip": {"bootp_server": True}},
            state="overridden",
        )
        self.assertEqual(result["commands"], ["no ip ftp source-interface"])

    def test_ios_service_states_leave_the_ip_section_alone_when_it_is_not_in_the_task(self):
        # existing playbooks must not start to switch services off
        running = (
            "service dhcp\nservice call-home\nip finger\nip scp server enable\n"
            "ip tftp source-interface GigabitEthernet0/0\n"
        )
        for state, config in (
            ("replaced", {"dhcp": True}),
            ("overridden", {"dhcp": True}),
            ("merged", {"dhcp": True}),
            ("deleted", None),
        ):
            self.execute_show_command.return_value = running
            args = {"state": state}
            if config is not None:
                args["config"] = config
            set_module_args(args)
            result = self.execute_module(changed=state in ("replaced", "overridden", "deleted"))
            ip_commands = [c for c in result["commands"] if " ip " in " " + c]
            self.assertEqual(ip_commands, [], state)

    def test_ios_service_ip_deleted_removes_only_what_the_task_names(self):
        result = self._run_ip(
            "service dhcp\nip finger\nip scp server enable\nip tftp source-interface GigabitEthernet0/0\n",
            {"ip": {"finger": True, "tftp": {"source_interface": "Gi0/0"}}},
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no ip finger", "no ip tftp source-interface"])

    def test_ios_service_ip_rendered(self):
        set_module_args(
            {
                "config": {
                    "ip": {
                        "bootp_server": True,
                        "scp_server": True,
                        "rcmd": {"rsh_enable": True, "rcp_enable": True},
                        "ftp": {"source_interface": "Loopback1"},
                    },
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        # the defaults of the service options are rendered as well, as for any other task
        self.assertEqual(
            [c for c in result["rendered"] if c.startswith("ip ")],
            [
                "ip bootp server",
                "ip scp server enable",
                "ip rcmd rsh-enable",
                "ip rcmd rcp-enable",
                "ip ftp source-interface Loopback1",
            ],
        )

    def test_ios_service_ip_parsed_and_gathered(self):
        running = dedent(
            """\
            service dhcp
            no ip bootp server
            no ip finger
            no ip source-route
            ip scp server enable
            ip rcmd rsh-enable
            ip tftp source-interface GigabitEthernet0/0
            ip ftp source-interface Loopback1
            """,
        )
        expected_ip = {
            "scp_server": True,
            "rcmd": {"rsh_enable": True},
            "tftp": {"source_interface": "GigabitEthernet0/0"},
            "ftp": {"source_interface": "Loopback1"},
        }
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"]["ip"], expected_ip)

        self.execute_show_command.return_value = running
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"]["ip"], expected_ip)

    # ---- ip.http ----
    HTTP_RUNNING = (
        "service dhcp\n"
        "ip http server\n"
        "ip http authentication enable\n"
        "ip http secure-server\n"
        "ip http secure-port 443\n"
        "ip http port 80\n"
        "ip http max-connections 300\n"
        "ip http timeout-policy idle 180 life 180 requests 25\n"
        "ip http client source-interface GigabitEthernet0/0\n"
    )

    def test_ios_service_http_merged_sets_the_options(self):
        result = self._run_ip(
            "service dhcp\n",
            {
                "ip": {
                    "http": {
                        "authentication": "local",
                        "access_class": "HTTP-CLIENTS",
                        "port": 8080,
                        "secure_port": 8443,
                        "max_connections": 100,
                        "secure_trustpoint": "LAB-TP",
                        "client": {"source_interface": "Gi0/0", "secure_trustpoint": "LAB-CA"},
                    },
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "ip http access-class ipv4 HTTP-CLIENTS",
                "ip http secure-trustpoint LAB-TP",
                "ip http client source-interface Gi0/0",
                "ip http client secure-trustpoint LAB-CA",
                "ip http authentication local",
                "ip http port 8080",
                "ip http secure-port 8443",
                "ip http max-connections 100",
            ],
        )

    def test_ios_service_http_merged_idempotent_with_the_defaults_printed_by_the_device(self):
        # "show running-config all" prints the defaults, a task may state them or leave them out
        result = self._run_ip(
            self.HTTP_RUNNING,
            {
                "ip": {
                    "http": {
                        "server": True,
                        "secure_server": True,
                        "authentication": "enable",
                        "port": 80,
                        "secure_port": 443,
                        "max_connections": 300,
                        "client": {"source_interface": "Gi0/0"},
                    },
                },
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_http_merged_a_default_that_is_not_printed_is_idempotent(self):
        result = self._run_ip(
            "service dhcp\n",
            {"ip": {"http": {"port": 80, "secure_port": 443, "authentication": "enable"}}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_http_merged_turns_the_server_off(self):
        result = self._run_ip(
            self.HTTP_RUNNING,
            {"ip": {"http": {"server": False}}},
        )
        self.assertEqual(result["commands"], ["no ip http server"])

    def test_ios_service_http_merged_false_on_a_server_that_is_off_is_idempotent(self):
        result = self._run_ip(
            "service dhcp\nno ip http server\nno ip http secure-server\n",
            {"ip": {"http": {"server": False, "secure_server": False}}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_http_merged_keeps_what_is_not_in_the_task(self):
        result = self._run_ip(
            self.HTTP_RUNNING + "ip http access-class ipv4 HTTP-CLIENTS\n",
            {"ip": {"http": {"port": 8080}}},
        )
        self.assertEqual(result["commands"], ["ip http port 8080"])

    def test_ios_service_http_merged_changes_the_source_interface(self):
        result = self._run_ip(
            self.HTTP_RUNNING,
            {"ip": {"http": {"client": {"source_interface": "Vlan402"}}}},
        )
        self.assertEqual(result["commands"], ["ip http client source-interface Vlan402"])

    def test_ios_service_http_authentication_aaa_with_its_options_is_read_as_aaa(self):
        result = self._run_ip(
            "service dhcp\nip http authentication aaa login-authentication WEB-LOGIN\n",
            {"ip": {"http": {"authentication": "aaa"}}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_http_replaced_removes_what_is_not_in_the_section(self):
        # the defaults printed by the device are not removed on every run
        result = self._run_ip(
            self.HTTP_RUNNING,
            {"ip": {"http": {"server": True, "secure_server": True}}},
            state="replaced",
        )
        self.assertEqual(result["commands"], ["no ip http client source-interface"])

    def test_ios_service_http_replaced_resets_values_that_are_not_the_default(self):
        result = self._run_ip(
            "service dhcp\nip http server\nip http authentication local\nip http port 8080\n"
            "ip http max-connections 100\nip http secure-port 443\n",
            {"ip": {"http": {"server": True}}},
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            ["no ip http authentication", "no ip http port", "no ip http max-connections"],
        )

    def test_ios_service_http_removal_of_trustpoints_and_access_class_carries_the_value(self):
        # IOS answers "Incomplete command" to the bare forms
        result = self._run_ip(
            "service dhcp\nip http server\nip http access-class ipv4 HTTP-CLIENTS\n"
            "ip http secure-trustpoint LAB-TP\nip http client secure-trustpoint LAB-CA\n",
            {"ip": {"http": {"server": True}}},
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip http access-class ipv4 HTTP-CLIENTS",
                "no ip http secure-trustpoint LAB-TP",
                "no ip http client secure-trustpoint LAB-CA",
            ],
        )

    def test_ios_service_http_replaced_changes_a_trustpoint(self):
        result = self._run_ip(
            "service dhcp\nip http secure-trustpoint OLD-TP\n",
            {"ip": {"http": {"secure_trustpoint": "NEW-TP"}}},
            state="replaced",
        )
        self.assertEqual(result["commands"], ["ip http secure-trustpoint NEW-TP"])

    def test_ios_service_http_deleted_removes_only_what_the_task_names(self):
        result = self._run_ip(
            self.HTTP_RUNNING + "ip http access-class ipv4 HTTP-CLIENTS\n",
            {"ip": {"http": {"server": True, "access_class": "HTTP-CLIENTS", "port": 80}}},
            state="deleted",
        )
        # port 80 is the default, there is nothing to remove
        self.assertEqual(
            result["commands"],
            ["no ip http server", "no ip http access-class ipv4 HTTP-CLIENTS"],
        )

    def test_ios_service_http_deleted_resets_a_port_that_is_not_the_default(self):
        result = self._run_ip(
            "service dhcp\nip http port 8080\nip http secure-port 8443\n",
            {"ip": {"http": {"port": 8080}}},
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no ip http port"])

    def test_ios_service_http_states_leave_the_section_alone_when_it_is_not_in_the_task(self):
        running = self.HTTP_RUNNING + "ip http access-class ipv4 HTTP-CLIENTS\nservice call-home\n"
        for state, config in (
            ("replaced", {"dhcp": True}),
            ("overridden", {"dhcp": True}),
            ("merged", {"dhcp": True}),
            ("deleted", None),
        ):
            self.execute_show_command.return_value = running
            args = {"state": state}
            if config is not None:
                args["config"] = config
            set_module_args(args)
            result = self.execute_module(changed=state in ("replaced", "overridden", "deleted"))
            http_commands = [c for c in result["commands"] if "ip http" in c]
            self.assertEqual(http_commands, [], state)

    def test_ios_service_http_rendered(self):
        set_module_args(
            {
                "config": {
                    "ip": {
                        "http": {
                            "server": True,
                            "secure_server": True,
                            "authentication": "tacacs",
                            "port": 8080,
                            "client": {"source_interface": "Loopback1"},
                        },
                    },
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            [c for c in result["rendered"] if c.startswith("ip http")],
            [
                "ip http server",
                "ip http secure-server",
                "ip http client source-interface Loopback1",
                "ip http authentication tacacs",
                "ip http port 8080",
            ],
        )

    def test_ios_service_http_parsed_and_gathered(self):
        running = self.HTTP_RUNNING + (
            "ip http access-class ipv4 HTTP-CLIENTS\n"
            "ip http access-class ipv6 HTTP-V6\n"
            "ip http secure-trustpoint LAB-TP\n"
            "ip http client secure-trustpoint LAB-CA\n"
            "ip http active-session-modules all\n"
        )
        expected = {
            "server": True,
            "secure_server": True,
            "authentication": "enable",
            "access_class": "HTTP-CLIENTS",
            "port": 80,
            "secure_port": 443,
            "max_connections": 300,
            "secure_trustpoint": "LAB-TP",
            "client": {"source_interface": "GigabitEthernet0/0", "secure_trustpoint": "LAB-CA"},
        }
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"]["ip"]["http"], expected)

        self.execute_show_command.return_value = running
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"]["ip"]["http"], expected)

    # ---- tftp-server: the files served by the TFTP server ----
    def _run_tftp_server(self, running, config, state="merged", changed=True):
        self.execute_show_command.return_value = running
        args = {"state": state}
        if config is not None:
            args["config"] = config
        set_module_args(args)
        return self.execute_module(changed=changed)

    def test_ios_service_tftp_server_merged(self):
        result = self._run_tftp_server(
            "service dhcp\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:image.bin"},
                        {"file": "flash:config.txt", "alias": "backup.txt"},
                        {
                            "file": "flash:log.txt",
                            "alias": "log.txt",
                            "access_list": 11,
                        },
                        {"file": "flash:old.txt", "access_list": 12},
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "tftp-server flash:image.bin",
                "tftp-server flash:config.txt alias backup.txt",
                "tftp-server flash:log.txt alias log.txt 11",
                "tftp-server flash:old.txt 12",
            ],
        )

    def test_ios_service_tftp_server_merged_idempotent_and_keeps_the_other_files(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\ntftp-server flash:config.txt alias backup.txt 10\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:config.txt", "alias": "backup.txt", "access_list": 10},
                    ],
                },
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_tftp_server_merged_keeps_the_access_list_the_task_leaves_out(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt alias backup.txt 10\n",
            {"tftp_server": {"files": [{"file": "flash:config.txt", "alias": "backup.txt"}]}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_tftp_server_merged_changes_the_access_list(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt alias backup.txt 10\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:config.txt", "alias": "backup.txt", "access_list": 20},
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no tftp-server flash:config.txt alias backup.txt 10",
                "tftp-server flash:config.txt alias backup.txt 20",
            ],
        )

    def test_ios_service_tftp_server_the_same_file_with_another_alias_is_another_line(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt alias one.txt\n",
            {"tftp_server": {"files": [{"file": "flash:config.txt", "alias": "two.txt"}]}},
        )
        self.assertEqual(result["commands"], ["tftp-server flash:config.txt alias two.txt"])

    def test_ios_service_tftp_server_enable_false_removes_every_line(self):
        running = "service dhcp\ntftp-server flash:image.bin\ntftp-server flash:config.txt alias backup.txt 10\n"
        for state in ("merged", "replaced", "overridden", "deleted"):
            result = self._run_tftp_server(running, {"tftp_server": {"enable": False}}, state=state)
            tftp = [c for c in result["commands"] if "tftp-server" in c]
            self.assertEqual(
                tftp,
                [
                    "no tftp-server flash:image.bin",
                    "no tftp-server flash:config.txt alias backup.txt 10",
                ],
                state,
            )

    def test_ios_service_tftp_server_enable_false_on_a_server_that_serves_nothing_is_idempotent(
        self,
    ):
        result = self._run_tftp_server(
            "service dhcp\n",
            {"tftp_server": {"enable": False}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_tftp_server_enable_false_with_files_fails(self):
        self.execute_show_command.return_value = "service dhcp\n"
        set_module_args(
            {
                "config": {
                    "tftp_server": {"enable": False, "files": [{"file": "flash:image.bin"}]},
                },
                "state": "merged",
            },
        )
        result = self.execute_module(failed=True)
        self.assertIn("enable false", result["msg"])

    def test_ios_service_tftp_server_enable_true_alone_does_nothing(self):
        for state in ("merged", "replaced", "overridden", "deleted"):
            result = self._run_tftp_server(
                "service dhcp\ntftp-server flash:image.bin\n",
                {"tftp_server": {"enable": True}},
                state=state,
                changed=False,
            )
            self.assertEqual([c for c in result["commands"] if "tftp-server" in c], [], state)

    def test_ios_service_tftp_server_replaced_leaves_only_the_listed_files(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\ntftp-server flash:config.txt alias backup.txt\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:config.txt", "alias": "backup.txt"},
                        {"file": "flash:new.txt"},
                    ],
                },
            },
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            ["no tftp-server flash:image.bin", "tftp-server flash:new.txt"],
        )

    def test_ios_service_tftp_server_overridden_leaves_only_the_listed_files(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\ntftp-server flash:config.txt\n",
            {"tftp_server": {"files": [{"file": "flash:config.txt"}]}},
            state="overridden",
        )
        self.assertEqual(result["commands"], ["no tftp-server flash:image.bin"])

    def test_ios_service_tftp_server_replaced_idempotent(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\n",
            {"tftp_server": {"files": [{"file": "flash:image.bin"}]}},
            state="replaced",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_tftp_server_deleted_removes_only_the_files_the_task_names(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\ntftp-server flash:config.txt alias one.txt\n"
            "tftp-server flash:config.txt alias two.txt\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:image.bin"},
                        {"file": "flash:config.txt", "alias": "two.txt"},
                    ],
                },
            },
            state="deleted",
        )
        # IOS removes the wrong line of a file that has several, so the lines of the file are rebuilt
        self.assertEqual(
            [c for c in result["commands"] if "tftp-server" in c],
            [
                "no tftp-server flash:image.bin",
                "no tftp-server flash:config.txt alias one.txt",
                "no tftp-server flash:config.txt alias two.txt",
                "tftp-server flash:config.txt alias one.txt",
            ],
        )

    def test_ios_service_tftp_server_deleted_a_file_without_alias_removes_every_alias_of_it(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt alias one.txt\ntftp-server flash:config.txt alias two.txt\n",
            {"tftp_server": {"files": [{"file": "flash:config.txt"}]}},
            state="deleted",
        )
        self.assertEqual(
            [c for c in result["commands"] if "tftp-server" in c],
            [
                "no tftp-server flash:config.txt alias one.txt",
                "no tftp-server flash:config.txt alias two.txt",
            ],
        )

    def test_ios_service_tftp_server_deleted_a_file_that_is_not_served_is_idempotent(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:image.bin\n",
            {"tftp_server": {"files": [{"file": "flash:other.bin"}]}},
            state="deleted",
            changed=False,
        )
        self.assertEqual([c for c in result["commands"] if "tftp-server" in c], [])

    def test_ios_service_tftp_server_states_leave_it_alone_when_it_is_not_in_the_task(self):
        # existing playbooks must not start to remove the files that are served
        running = "service dhcp\nservice call-home\ntftp-server flash:image.bin\ntftp-server flash:config.txt alias a.txt 10\n"
        for state, config in (
            ("replaced", {"dhcp": True}),
            ("overridden", {"dhcp": True}),
            ("merged", {"dhcp": True}),
            ("deleted", None),
        ):
            self.execute_show_command.return_value = running
            args = {"state": state}
            if config is not None:
                args["config"] = config
            set_module_args(args)
            result = self.execute_module(changed=state in ("replaced", "overridden", "deleted"))
            self.assertEqual([c for c in result["commands"] if "tftp-server" in c], [], state)

    def test_ios_service_tftp_server_rendered(self):
        set_module_args(
            {
                "config": {
                    "tftp_server": {
                        "files": [
                            {"file": "flash:image.bin"},
                            {
                                "file": "flash:config.txt",
                                "alias": "backup.txt",
                                "access_list": 10,
                            },
                        ],
                    },
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            [c for c in result["rendered"] if "tftp-server" in c],
            [
                "tftp-server flash:image.bin",
                "tftp-server flash:config.txt alias backup.txt 10",
            ],
        )

    def test_ios_service_tftp_server_parsed_and_gathered_including_the_old_form(self):
        running = dedent(
            """\
            service dhcp
            tftp-server flash:image.bin
            tftp-server flash:config.txt alias backup.txt 10
            tftp-server flash:log.txt 10
            tftp-server flash old.bin
            tftp-server flash old2.bin alias legacy.bin
            ip tftp source-interface GigabitEthernet0/0
            """,
        )
        expected = {
            "files": [
                {"file": "flash:image.bin"},
                {"file": "flash:config.txt", "alias": "backup.txt", "access_list": 10},
                {"file": "flash:log.txt", "access_list": 10},
                {"file": "flash:old.bin"},
                {"file": "flash:old2.bin", "alias": "legacy.bin"},
            ],
        }
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"]["tftp_server"], expected)
        # the line of the ip section next to them is not taken for a file
        self.assertEqual(
            result["parsed"]["ip"],
            {"tftp": {"source_interface": "GigabitEthernet0/0"}},
        )

        self.execute_show_command.return_value = running
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"]["tftp_server"], expected)

    def test_ios_service_tftp_server_the_old_form_on_the_device_is_the_same_file(self):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash old.bin\n",
            {"tftp_server": {"files": [{"file": "flash:old.bin"}]}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_tftp_server_a_plain_line_stays_when_the_alias_line_of_the_same_file_goes(
        self,
    ):
        # on the switch "no tftp-server F alias A" took the plain line, so both are removed and the plain one added again
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt\ntftp-server flash:config.txt alias backup.txt 10\n",
            {"tftp_server": {"files": [{"file": "flash:config.txt"}]}},
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "no tftp-server flash:config.txt",
                "no tftp-server flash:config.txt alias backup.txt 10",
                "tftp-server flash:config.txt",
            ],
        )

    def test_ios_service_tftp_server_changing_the_access_list_keeps_the_other_line_of_the_file(
        self,
    ):
        result = self._run_tftp_server(
            "service dhcp\ntftp-server flash:config.txt\ntftp-server flash:config.txt alias backup.txt 10\n",
            {
                "tftp_server": {
                    "files": [
                        {"file": "flash:config.txt", "alias": "backup.txt", "access_list": 20},
                    ],
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no tftp-server flash:config.txt",
                "no tftp-server flash:config.txt alias backup.txt 10",
                "tftp-server flash:config.txt",
                "tftp-server flash:config.txt alias backup.txt 20",
            ],
        )

    def test_ios_service_tftp_server_a_named_access_list_is_refused_by_the_argspec(self):
        # IOS: "% Invalid input" for "tftp-server F alias A NAME", it takes a number
        self.execute_show_command.return_value = "service dhcp\n"
        set_module_args(
            {
                "config": {
                    "tftp_server": {
                        "files": [{"file": "flash:image.bin", "access_list": "TFTP-CLIENTS"}],
                    },
                },
                "state": "merged",
            },
        )
        result = self.execute_module(failed=True)
        self.assertIn("access_list", result["msg"])

    # ---------------------------------------------------------------- ip ssh
    SSH_RUNNING = dedent(
        """\
        service dhcp
        ip ssh bulk-mode 131072
        ip ssh time-out 120
        ip ssh authentication-retries 3
        ip ssh window-size 8192
        ip ssh break-string ~break
        ip ssh logging events
        ip ssh version 2
        ip ssh dh min size 2048
        ip ssh server authenticate user publickey
        ip ssh server certificate profile
        ip ssh server algorithm mac hmac-sha2-256-etm@openssh.com hmac-sha2-512-etm@openssh.com
        ip ssh server algorithm encryption aes256-gcm aes128-gcm aes256-ctr
        ip ssh server algorithm kex ecdh-sha2-nistp521 ecdh-sha2-nistp384 ecdh-sha2-nistp256
        ip ssh server algorithm hostkey rsa-sha2-512 rsa-sha2-256
        ip ssh server algorithm authentication publickey keyboard password
        ip ssh server algorithm publickey ecdsa-sha2-nistp256 ecdsa-sha2-nistp384 ssh-ed25519
        ip ssh client algorithm mac hmac-sha2-256
        """,
    )

    def test_ios_service_ssh_merged(self):
        result = self._run_ip(
            "service dhcp\n",
            {
                "ip": {
                    "ssh": {
                        "version": 2,
                        "time_out": 60,
                        "authentication_retries": 4,
                        "dh_min_size": 3072,
                        "bulk_mode": 65536,
                        "logging_events": True,
                        "source_interface": "Vlan402",
                        "rsa_keypair_name": "KEYS",
                        "server": {
                            "algorithm": {
                                "mac": ["hmac-sha2-512-etm@openssh.com", "hmac-sha2-512"],
                                "kex": ["ecdh-sha2-nistp521"],
                                "hostkey": ["rsa-sha2-512"],
                                "encryption": ["aes256-gcm", "aes256-ctr"],
                                "publickey": ["ecdsa-sha2-nistp521"],
                                "authentication": ["publickey"],
                            },
                        },
                    },
                },
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "ip ssh version 2",
                "ip ssh time-out 60",
                "ip ssh authentication-retries 4",
                "ip ssh dh min size 3072",
                "ip ssh bulk-mode 65536",
                "ip ssh logging events",
                "ip ssh source-interface Vlan402",
                "ip ssh rsa keypair-name KEYS",
                "ip ssh server algorithm mac hmac-sha2-512-etm@openssh.com hmac-sha2-512",
                "ip ssh server algorithm kex ecdh-sha2-nistp521",
                "ip ssh server algorithm hostkey rsa-sha2-512",
                "ip ssh server algorithm encryption aes256-gcm aes256-ctr",
                "ip ssh server algorithm publickey ecdsa-sha2-nistp521",
                "ip ssh server algorithm authentication publickey",
            ],
        )

    def test_ios_service_ssh_merged_idempotent(self):
        result = self._run_ip(
            self.SSH_RUNNING,
            {
                "ip": {
                    "ssh": {
                        "version": 2,
                        "time_out": 120,
                        "authentication_retries": 3,
                        "dh_min_size": 2048,
                        "bulk_mode": 131072,
                        "logging_events": True,
                        "server": {
                            "algorithm": {
                                "mac": [
                                    "hmac-sha2-256-etm@openssh.com",
                                    "hmac-sha2-512-etm@openssh.com",
                                ],
                                "hostkey": ["rsa-sha2-512", "rsa-sha2-256"],
                                "authentication": ["publickey", "keyboard", "password"],
                            },
                        },
                    },
                },
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_ssh_the_order_of_an_algorithm_list_matters(self):
        result = self._run_ip(
            self.SSH_RUNNING,
            {
                "ip": {
                    "ssh": {"server": {"algorithm": {"hostkey": ["rsa-sha2-256", "rsa-sha2-512"]}}},
                },
            },
        )
        self.assertEqual(
            result["commands"],
            ["ip ssh server algorithm hostkey rsa-sha2-256 rsa-sha2-512"],
        )

    def test_ios_service_ssh_a_list_replaces_the_one_of_the_device(self):
        result = self._run_ip(
            self.SSH_RUNNING,
            {"ip": {"ssh": {"server": {"algorithm": {"mac": ["hmac-sha2-512-etm@openssh.com"]}}}}},
        )
        # no union of the two lists
        self.assertEqual(
            result["commands"],
            ["ip ssh server algorithm mac hmac-sha2-512-etm@openssh.com"],
        )

    def test_ios_service_ssh_options_that_are_not_in_the_task_are_left_alone(self):
        for state in ("merged", "replaced", "overridden"):
            result = self._run_ip(
                self.SSH_RUNNING,
                {"ip": {"ssh": {"time_out": 60}}},
                state=state,
            )
            self.assertEqual(result["commands"], ["ip ssh time-out 60"], state)

    def test_ios_service_ssh_states_leave_ssh_alone_when_it_is_not_in_the_task(self):
        for state, config in (
            ("replaced", {"ip": {"finger": True}}),
            ("overridden", {"ip": {"finger": True}}),
            ("deleted", None),
        ):
            self.execute_show_command.return_value = self.SSH_RUNNING + "ip finger\n"
            args = {"state": state}
            if config is not None:
                args["config"] = config
            set_module_args(args)
            result = self.execute_module(changed=False)
            ssh_commands = [c for c in result["commands"] if "ip ssh" in c]
            self.assertEqual(ssh_commands, [], state)

    def test_ios_service_ssh_logging_events_false(self):
        result = self._run_ip(
            self.SSH_RUNNING,
            {"ip": {"ssh": {"logging_events": False}}},
        )
        self.assertEqual(result["commands"], ["no ip ssh logging events"])
        # IOS prints "no ip ssh logging events" with "all" when it is off
        result = self._run_ip(
            "service dhcp\nno ip ssh logging events\n",
            {"ip": {"ssh": {"logging_events": False}}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_ssh_source_interface_may_be_abbreviated(self):
        result = self._run_ip(
            "service dhcp\nip ssh source-interface GigabitEthernet0/0\n",
            {"ip": {"ssh": {"source_interface": "Gi0/0"}}},
            changed=False,
        )
        self.assertEqual(result["commands"], [])
        result = self._run_ip(
            "service dhcp\nip ssh source-interface GigabitEthernet0/0\n",
            {"ip": {"ssh": {"source_interface": "Vlan402"}}},
        )
        self.assertEqual(result["commands"], ["ip ssh source-interface Vlan402"])

    def test_ios_service_ssh_deleted_resets_only_the_options_without_a_default(self):
        result = self._run_ip(
            self.SSH_RUNNING + "ip ssh source-interface Vlan402\nip ssh rsa keypair-name KEYS\n",
            {
                "ip": {
                    "ssh": {
                        "version": 2,
                        "time_out": 60,
                        "source_interface": "Vlan402",
                        "rsa_keypair_name": "KEYS",
                    },
                },
            },
            state="deleted",
        )
        # the options with a default value are printed whatever the configuration is: nothing to remove
        self.assertEqual(
            result["commands"],
            ["no ip ssh source-interface", "no ip ssh rsa keypair-name KEYS"],
        )

    def test_ios_service_ssh_deleted_of_an_option_that_is_not_set_is_idempotent(self):
        result = self._run_ip(
            self.SSH_RUNNING,
            {"ip": {"ssh": {"source_interface": "Vlan402", "rsa_keypair_name": "KEYS"}}},
            state="deleted",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_service_ssh_rendered(self):
        set_module_args(
            {
                "config": {
                    "ip": {
                        "ssh": {
                            "version": 2,
                            "logging_events": True,
                            "server": {
                                "algorithm": {"kex": ["ecdh-sha2-nistp521", "ecdh-sha2-nistp384"]},
                            },
                        },
                    },
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            [c for c in result["rendered"] if c.startswith("ip ssh")],
            [
                "ip ssh version 2",
                "ip ssh logging events",
                "ip ssh server algorithm kex ecdh-sha2-nistp521 ecdh-sha2-nistp384",
            ],
        )

    def test_ios_service_ssh_parsed_and_gathered(self):
        expected = {
            "version": 2,
            "time_out": 120,
            "authentication_retries": 3,
            "dh_min_size": 2048,
            "bulk_mode": 131072,
            "logging_events": True,
            "server": {
                "algorithm": {
                    "mac": ["hmac-sha2-256-etm@openssh.com", "hmac-sha2-512-etm@openssh.com"],
                    "encryption": ["aes256-gcm", "aes128-gcm", "aes256-ctr"],
                    "kex": ["ecdh-sha2-nistp521", "ecdh-sha2-nistp384", "ecdh-sha2-nistp256"],
                    "hostkey": ["rsa-sha2-512", "rsa-sha2-256"],
                    "authentication": ["publickey", "keyboard", "password"],
                    "publickey": ["ecdsa-sha2-nistp256", "ecdsa-sha2-nistp384", "ssh-ed25519"],
                },
            },
        }
        set_module_args({"running_config": self.SSH_RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"]["ip"]["ssh"], expected)

        self.execute_show_command.return_value = self.SSH_RUNNING
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"]["ip"]["ssh"], expected)
