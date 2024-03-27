#
# (c) 2022, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_ping
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosPingModule(TestIosModule):
    module = ios_ping

    def setUp(self):
        super(TestIosPingModule, self).setUp()
        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.ping.ping.Ping.run_command",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosPingModule, self).tearDown()
        self.mock_execute_show_command.stop()

    def test_ios_ping_count(self):
        self.execute_show_command.return_value = dedent(
            """\
            Type escape sequence to abort.
            ending 2, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
            !
            Success rate is 100 percent (2/2), round-trip min/avg/max = 25/25/25 ms
            """,
        )
        set_module_args(dict(count=2, dest="8.8.8.8"))
        result = self.execute_module()
        mock_res = {
            "commands": "ping ip 8.8.8.8 repeat 2",
            "packet_loss": "0%",
            "packets_rx": 2,
            "packets_tx": 2,
            "rtt": {"min": 25, "avg": 25, "max": 25},
            "changed": False,
        }
        self.assertEqual(result, mock_res)

    def test_ios_ping_v6(self):
        self.execute_show_command.return_value = dedent(
            """\
            Type escape sequence to abort.
            ending 2, 100-byte ICMP Echos to 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff, timeout is 2 seconds:
            !
            Success rate is 100 percent (2/2), round-trip min/avg/max = 25/25/25 ms
            """,
        )
        set_module_args(
            dict(count=2, dest="2001:db8:ffff:ffff:ffff:ffff:ffff:ffff", afi="ipv6"),
        )
        result = self.execute_module()
        mock_res = {
            "commands": "ping ipv6 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff repeat 2",
            "packet_loss": "0%",
            "packets_rx": 2,
            "packets_tx": 2,
            "rtt": {"min": 25, "avg": 25, "max": 25},
            "changed": False,
        }
        self.assertEqual(result, mock_res)

    def test_ios_ping_options_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            Type escape sequence to abort.
            ending 2, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
            !
            Success rate is 100 percent (2/2), round-trip min/avg/max = 25/25/25 ms
            """,
        )
        set_module_args(
            {
                "afi": "ip",
                "count": 4,
                "dest": "8.8.8.8",
                "size": 800,
                "df_bit": True,
                "source": "Loopback88",
                "state": "present",
                "vrf": "DummyVrf",
            },
        )
        result = self.execute_module()
        mock_res = {
            "commands": "ping vrf DummyVrf ip 8.8.8.8 repeat 4 df-bit size 800 source Loopback88",
            "packet_loss": "0%",
            "packets_rx": 2,
            "packets_tx": 2,
            "rtt": {"min": 25, "avg": 25, "max": 25},
            "changed": False,
        }
        self.assertEqual(result, mock_res)

    def test_ios_ping_state_absent_pass(self):
        self.execute_show_command.return_value = dedent(
            """\
            Type escape sequence to abort.
            ending 2, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
            !
            Success rate is 90 percent (2/2), round-trip min/avg/max = 25/25/25 ms
            """,
        )
        set_module_args(dict(count=2, dest="8.8.8.8", state="absent"))
        result = self.execute_module(failed=True)
        mock_res = {
            "msg": "Ping succeeded unexpectedly",
            "commands": "ping ip 8.8.8.8 repeat 2",
            "packet_loss": "10%",
            "packets_rx": 2,
            "packets_tx": 2,
            "rtt": {"min": 25, "avg": 25, "max": 25},
            "failed": True,
        }
        self.assertEqual(result, mock_res)

    def test_ios_ping_state_absent_present_fail(self):
        self.execute_show_command.return_value = dedent(
            """\
            Type escape sequence to abort.
            ending 2, 100-byte ICMP Echos to 8.8.8.8, timeout is 12 seconds:
            !
            Success rate is 0 percent (0/2), round-trip min/avg/max = 25/25/25 ms
            """,
        )
        set_module_args(dict(count=2, dest="8.8.8.8", state="present"))
        result = self.execute_module(failed=True)
        mock_res = {
            "msg": "Ping failed unexpectedly",
            "commands": "ping ip 8.8.8.8 repeat 2",
            "packet_loss": "100%",
            "packets_rx": 0,
            "packets_tx": 2,
            "rtt": {"min": 25, "avg": 25, "max": 25},
            "failed": True,
        }
        self.assertEqual(result, mock_res)
