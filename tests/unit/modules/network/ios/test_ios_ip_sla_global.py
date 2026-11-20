# (c) 2026 Red Hat Inc.
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

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_ip_sla_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


RAW_REQUEST = (
    "GET http://192.0.2.10/test HTTP/1.0\\r\\nUser-Agent: Cisco IP SLA\\r\\nend\\r\\n\\r\\n"
)

RUNNING = dedent(
    """\
    ip sla logging traps
    ip sla 1
     icmp-echo 192.0.2.1 source-interface Loopback0
      vrf MGMT
      frequency 5
    ip sla 2
     http raw http://192.0.2.10
      vrf MGMT
      http-raw-request
       %s
       exit
      threshold 500
      timeout 5000
    ip sla schedule 1 life forever start-time now
    ip sla schedule 2 life forever start-time now
    """
    % RAW_REQUEST,
)


class TestIosIpSlaModule(TestIosModule):
    module = ios_ip_sla_global

    def setUp(self):
        super(TestIosIpSlaModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ip_sla_global.ip_sla_global."
            "Ip_sla_globalFacts.get_ip_sla_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosIpSlaModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True, failed=False):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def test_ios_ip_sla_global_merged(self):
        result = self._run(
            "",
            {
                "config": {
                    "logging_traps": True,
                    "enable_reaction_alerts": True,
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {
                                "destination": "192.0.2.1",
                                "source_interface": "Loopback0",
                            },
                            "vrf": "MGMT",
                            "frequency": 5,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                        {
                            "operation_id": 2,
                            "http": {
                                "method": "raw",
                                "url": "http://192.0.2.10",
                                "raw_request": RAW_REQUEST,
                            },
                            "threshold": 500,
                            "timeout": 5000,
                        },
                        {
                            "operation_id": 3,
                            "tcp_connect": {
                                "destination": "192.0.2.3",
                                "port": 443,
                                "source_port": 4000,
                            },
                            "tag": "web check",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "ip sla logging traps",
                "ip sla enable reaction-alerts",
                "ip sla 1",
                "icmp-echo 192.0.2.1 source-interface Loopback0",
                "vrf MGMT",
                "frequency 5",
                "ip sla schedule 1 life forever start-time now",
                "ip sla 2",
                "http raw http://192.0.2.10",
                "http-raw-request",
                RAW_REQUEST,
                "exit",
                "threshold 500",
                "timeout 5000",
                "ip sla 3",
                "tcp-connect 192.0.2.3 443 source-port 4000",
                "tag web check",
            ],
        )

    def test_ios_ip_sla_global_merged_idempotent(self):
        # the short interface name in the task is the long one on the device
        result = self._run(
            RUNNING,
            {
                "config": {
                    "logging_traps": True,
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {
                                "destination": "192.0.2.1",
                                "source_interface": "loopback0",
                            },
                            "vrf": "MGMT",
                            "frequency": 5,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                        {
                            "operation_id": 2,
                            "http": {
                                "method": "raw",
                                "url": "http://192.0.2.10",
                                "raw_request": RAW_REQUEST,
                            },
                            "vrf": "MGMT",
                            "threshold": 500,
                            "timeout": 5000,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_merged_interface_alias_idempotent(self):
        result = self._run(
            "ip sla 7\n icmp-echo 192.0.2.7 source-interface GigabitEthernet1\n",
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 7,
                            "icmp_echo": {"destination": "192.0.2.7", "source_interface": "Gi1"},
                        },
                    ],
                },
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_merged_keeps_what_is_not_in_the_task(self):
        # only the frequency is given, vrf, type, schedule and the global option stay
        result = self._run(
            RUNNING,
            {"config": {"operations": [{"operation_id": 1, "frequency": 10}]}, "state": "merged"},
        )
        # operation 1 is running: stopped for the change, started again afterwards
        self.assertEqual(
            result["commands"],
            [
                "no ip sla schedule 1",
                "ip sla 1",
                "frequency 10",
                "ip sla schedule 1 life forever start-time now",
            ],
        )

    def test_ios_ip_sla_global_merged_changes_destination_recreates(self):
        # IOS cannot change the destination: the operation is rebuilt, with what the device had
        result = self._run(
            RUNNING,
            {
                "config": {
                    "operations": [{"operation_id": 1, "icmp_echo": {"destination": "192.0.2.99"}}],
                },
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip sla 1",
                "ip sla 1",
                "icmp-echo 192.0.2.99 source-interface Loopback0",
                "vrf MGMT",
                "frequency 5",
                "ip sla schedule 1 life forever start-time now",
            ],
        )

    def test_ios_ip_sla_global_merged_changes_schedule(self):
        result = self._run(
            RUNNING,
            {
                "config": {"operations": [{"operation_id": 1, "schedule": {"life": "3600"}}]},
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["no ip sla schedule 1", "ip sla schedule 1 life 3600 start-time now"],
        )

    def test_ios_ip_sla_global_merged_changes_raw_request(self):
        result = self._run(
            RUNNING,
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 2,
                            "http": {
                                "method": "raw",
                                "url": "http://192.0.2.10",
                                "raw_request": "new",
                            },
                        },
                    ],
                },
                "state": "merged",
            },
        )
        # the payload is replaced in place, operation 2 is stopped meanwhile
        self.assertEqual(
            result["commands"],
            [
                "no ip sla schedule 2",
                "ip sla 2",
                "http-raw-request",
                "new",
                "exit",
                "ip sla schedule 2 life forever start-time now",
            ],
        )

    def test_ios_ip_sla_global_replaced(self):
        # vrf, frequency, schedule and the type line of operation 1 are cut down to the task
        result = self._run(
            RUNNING,
            {
                "config": {
                    "logging_traps": True,
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {
                                "destination": "192.0.2.1",
                                "source_interface": "Loopback0",
                            },
                            "timeout": 2000,
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            ["no ip sla schedule 1", "ip sla 1", "no vrf", "no frequency", "timeout 2000"],
        )

    def test_ios_ip_sla_global_replaced_idempotent(self):
        result = self._run(
            "ip sla 1\n icmp-echo 192.0.2.1\n  frequency 5\nip sla schedule 1 life forever start-time now\n",
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {"destination": "192.0.2.1"},
                            "frequency": 5,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_replaced_changes_type(self):
        result = self._run(
            RUNNING,
            {
                "config": {
                    "logging_traps": True,
                    "operations": [
                        {
                            "operation_id": 1,
                            "tcp_connect": {"destination": "192.0.2.1", "port": 80},
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            ["no ip sla 1", "ip sla 1", "tcp-connect 192.0.2.1 80"],
        )

    def test_ios_ip_sla_global_replaced_dropped_raw_request_recreates(self):
        # "no http-raw-request" does not exist on IOS
        result = self._run(
            RUNNING,
            {
                "config": {
                    "logging_traps": True,
                    "operations": [
                        {
                            "operation_id": 2,
                            "http": {"method": "raw", "url": "http://192.0.2.10"},
                            "vrf": "MGMT",
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            ["no ip sla 2", "ip sla 2", "http raw http://192.0.2.10", "vrf MGMT"],
        )

    def test_ios_ip_sla_global_default_life_is_idempotent(self):
        # IOS does not print "life 3600"
        result = self._run(
            "ip sla 1\n icmp-echo 192.0.2.1\nip sla schedule 1 start-time now\n",
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {"destination": "192.0.2.1"},
                            "schedule": {"life": "3600", "start_time": "now"},
                        },
                    ],
                },
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_schedule_with_threshold_above_timeout_fails(self):
        # the default threshold is 5000 ms, IOS refuses to schedule it with a smaller timeout
        result = self._run(
            "",
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {"destination": "192.0.2.1"},
                            "timeout": 2000,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "merged",
            },
            failed=True,
        )
        self.assertIn("threshold of 5000 ms is greater than the timeout of 2000 ms", result["msg"])

    def test_ios_ip_sla_global_schedule_with_timeout_above_frequency_fails(self):
        result = self._run(
            "",
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {"destination": "192.0.2.1"},
                            "frequency": 5,
                            "timeout": 6000,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "merged",
            },
            failed=True,
        )
        self.assertIn("timeout of 6000 ms is greater than the frequency of 5 s", result["msg"])

    def test_ios_ip_sla_global_replaced_leaves_other_operations(self):
        result = self._run(
            RUNNING,
            {
                "config": {
                    "logging_traps": True,
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {
                                "destination": "192.0.2.1",
                                "source_interface": "Loopback0",
                            },
                            "vrf": "MGMT",
                            "frequency": 5,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_overridden(self):
        result = self._run(
            RUNNING,
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 1,
                            "icmp_echo": {
                                "destination": "192.0.2.1",
                                "source_interface": "Loopback0",
                            },
                            "vrf": "MGMT",
                            "frequency": 5,
                            "schedule": {"life": "forever", "start_time": "now"},
                        },
                    ],
                },
                "state": "overridden",
            },
        )
        # logging traps is not in the task, operation 2 is not in the task
        self.assertEqual(result["commands"], ["no ip sla logging traps", "no ip sla 2"])

    def test_ios_ip_sla_global_deleted_operation(self):
        result = self._run(
            RUNNING,
            {
                "config": {"operations": [{"operation_id": 2}, {"operation_id": 9}]},
                "state": "deleted",
            },
        )
        self.assertEqual(result["commands"], ["no ip sla 2"])

    def test_ios_ip_sla_global_deleted_all(self):
        result = self._run(RUNNING, {"state": "deleted"})
        self.assertEqual(
            result["commands"],
            ["no ip sla logging traps", "no ip sla 1", "no ip sla 2"],
        )

    def test_ios_ip_sla_global_deleted_all_empty_device(self):
        result = self._run("", {"state": "deleted"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_ip_sla_global_rendered(self):
        set_module_args(
            {
                "config": {
                    "operations": [
                        {
                            "operation_id": 5,
                            "tcp_connect": {"destination": "192.0.2.5", "port": 443},
                            "frequency": 30,
                            "schedule": {"life": "forever", "start_time": "now", "recurring": True},
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "ip sla 5",
                "tcp-connect 192.0.2.5 443",
                "frequency 30",
                "ip sla schedule 5 life forever start-time now recurring",
            ],
        )

    def test_ios_ip_sla_global_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "logging_traps": True,
                "operations": [
                    {
                        "operation_id": 1,
                        "icmp_echo": {"destination": "192.0.2.1", "source_interface": "Loopback0"},
                        "vrf": "MGMT",
                        "frequency": 5,
                        "schedule": {"life": "forever", "start_time": "now"},
                    },
                    {
                        "operation_id": 2,
                        "http": {
                            "method": "raw",
                            "url": "http://192.0.2.10",
                            "raw_request": RAW_REQUEST,
                        },
                        "vrf": "MGMT",
                        "threshold": 500,
                        "timeout": 5000,
                        "schedule": {"life": "forever", "start_time": "now"},
                    },
                ],
            },
        )

    def test_ios_ip_sla_global_gathered_ignores_unsupported_operations(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip sla 4
             udp-jitter 192.0.2.4 5000 codec g711alaw
              frequency 20
            ip sla 5
             http get http://192.0.2.5 version 1.1
            ip sla 6
             icmp-echo 192.0.2.6
              tos 8
              request-data-size 64
              owner ops
            ip sla schedule 4 life forever start-time now
            ip sla group schedule 1 4,5 schedule-period 60 life forever
            """,
        )
        set_module_args({"state": "gathered"})
        with patch.object(ios_ip_sla_global.AnsibleModule, "warn") as warn:
            result = self.execute_module(changed=False)
        self.assertEqual(
            result["gathered"],
            {
                "operations": [
                    {
                        "operation_id": 6,
                        "icmp_echo": {"destination": "192.0.2.6"},
                        "tos": 8,
                        "request_data_size": 64,
                        "owner": "ops",
                    },
                ],
            },
        )
        warn.assert_called_once()
        self.assertIn("4, 5", warn.call_args[0][0])

    def test_ios_ip_sla_global_unsupported_operation_is_not_overridden(self):
        result = self._run(
            "ip sla 4\n udp-jitter 192.0.2.4 5000\n",
            {
                "config": {
                    "operations": [{"operation_id": 1, "icmp_echo": {"destination": "192.0.2.1"}}],
                },
                "state": "overridden",
            },
        )
        self.assertEqual(result["commands"], ["ip sla 1", "icmp-echo 192.0.2.1"])
