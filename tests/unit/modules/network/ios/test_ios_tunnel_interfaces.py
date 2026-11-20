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

from ansible_collections.cisco.ios.plugins.modules import ios_tunnel_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


RUNNING = dedent(
    """\
    interface Tunnel1501
     tunnel source Loopback499
     tunnel destination 198.51.100.101
     tunnel key 1501
     tunnel vrf MGMT
    interface Tunnel1502
     tunnel source GigabitEthernet1/0/12
     tunnel mode gre ipv6
     tunnel destination 2001:DB8::1
     tunnel ttl 64
     tunnel checksum
     tunnel path-mtu-discovery
    """,
)


class TestIosTunnelInterfacesModule(TestIosModule):
    module = ios_tunnel_interfaces

    def setUp(self):
        super(TestIosTunnelInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.tunnel_interfaces.tunnel_interfaces."
            "Tunnel_interfacesFacts.get_tunnel_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosTunnelInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True, failed=False):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def test_ios_tunnel_interfaces_merged(self):
        result = self._run(
            "",
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "source": "Loopback499",
                        "destination": "198.51.100.101",
                        "key": 1501,
                        "vrf": "MGMT",
                    },
                    {
                        "name": "Tunnel1502",
                        "mode": "gre_ipv6",
                        "source": "GigabitEthernet1/0/12",
                        "destination": "2001:db8::1",
                        "ttl": 64,
                        "checksum": True,
                        "path_mtu_discovery": True,
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Tunnel1501",
                "tunnel source Loopback499",
                "tunnel destination 198.51.100.101",
                "tunnel key 1501",
                "tunnel vrf MGMT",
                "interface Tunnel1502",
                "tunnel mode gre ipv6",
                "tunnel source GigabitEthernet1/0/12",
                "tunnel destination 2001:db8::1",
                "tunnel ttl 64",
                "tunnel checksum",
                "tunnel path-mtu-discovery",
            ],
        )

    def test_ios_tunnel_interfaces_merged_idempotent_with_short_names_and_upper_case_ipv6(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "Tu1501",
                        "source": "Lo499",
                        "destination": "198.51.100.101",
                        "key": 1501,
                        "vrf": "MGMT",
                    },
                    {
                        "name": "Tunnel1502",
                        "mode": "gre_ipv6",
                        "source": "Gi1/0/12",
                        "destination": "2001:db8:0:0:0:0:0:1",
                        "ttl": 64,
                        "checksum": True,
                        "path_mtu_discovery": True,
                    },
                ],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_tunnel_interfaces_defaults_are_not_printed_so_setting_them_is_idempotent(self):
        result = self._run(
            RUNNING,
            {"config": [{"name": "Tunnel1501", "mode": "gre_ip", "ttl": 255}], "state": "merged"},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_tunnel_interfaces_merged_keeps_what_is_not_in_the_task(self):
        result = self._run(
            RUNNING,
            {"config": [{"name": "Tunnel1501", "key": 99}], "state": "merged"},
        )
        self.assertEqual(result["commands"], ["interface Tunnel1501", "tunnel key 99"])

    def test_ios_tunnel_interfaces_merged_can_turn_off_a_flag(self):
        result = self._run(
            RUNNING,
            {"config": [{"name": "Tunnel1502", "checksum": False}], "state": "merged"},
        )
        self.assertEqual(result["commands"], ["interface Tunnel1502", "no tunnel checksum"])

    def test_ios_tunnel_interfaces_merged_multipoint_removes_destination_first(self):
        # IOS: "p2mp tunnels cannot have a tunnel destination", the destination goes before the mode
        result = self._run(
            RUNNING,
            {"config": [{"name": "Tunnel1501", "mode": "gre_multipoint"}], "state": "merged"},
        )
        self.assertEqual(
            result["commands"],
            ["interface Tunnel1501", "no tunnel destination", "tunnel mode gre multipoint"],
        )

    def test_ios_tunnel_interfaces_leaving_multipoint_sets_the_mode_before_the_destination(self):
        result = self._run(
            "interface Tunnel1501\n tunnel source Loopback499\n tunnel mode gre multipoint\n",
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "source": "Loopback499",
                        "destination": "198.51.100.101",
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            ["interface Tunnel1501", "no tunnel mode", "tunnel destination 198.51.100.101"],
        )

    def test_ios_tunnel_interfaces_multipoint_with_destination_fails(self):
        result = self._run(
            "",
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "mode": "gre_multipoint",
                        "destination": "198.51.100.101",
                    },
                ],
                "state": "merged",
            },
            failed=True,
        )
        self.assertIn("gre_multipoint", result["msg"])

    def test_ios_tunnel_interfaces_only_tunnel_interfaces(self):
        result = self._run(
            "",
            {"config": [{"name": "GigabitEthernet1", "key": 1}], "state": "merged"},
            failed=True,
        )
        self.assertIn("not a tunnel interface", result["msg"])

    def test_ios_tunnel_interfaces_replaced_removes_what_is_not_in_the_task(self):
        # "no tunnel vrf" needs the name of the VRF on IOS ("Incomplete command" otherwise)
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "source": "Loopback499",
                        "destination": "198.51.100.102",
                        "ttl": 64,
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Tunnel1501",
                "tunnel destination 198.51.100.102",
                "no tunnel key",
                "no tunnel vrf MGMT",
                "tunnel ttl 64",
            ],
        )

    def test_ios_tunnel_interfaces_replaced_without_ttl_goes_back_to_the_default(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "Tunnel1502",
                        "mode": "gre_ipv6",
                        "source": "GigabitEthernet1/0/12",
                        "destination": "2001:db8::1",
                        "checksum": True,
                        "path_mtu_discovery": True,
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(result["commands"], ["interface Tunnel1502", "no tunnel ttl"])

    def test_ios_tunnel_interfaces_replaced_leaves_other_interfaces(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "source": "Loopback499",
                        "destination": "198.51.100.101",
                        "key": 1501,
                        "vrf": "MGMT",
                    },
                ],
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_tunnel_interfaces_overridden(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "name": "Tunnel1501",
                        "source": "Loopback499",
                        "destination": "198.51.100.101",
                        "key": 1501,
                        "vrf": "MGMT",
                    },
                ],
                "state": "overridden",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Tunnel1502",
                "no tunnel mode",
                "no tunnel source",
                "no tunnel destination",
                "no tunnel ttl",
                "no tunnel checksum",
                "no tunnel path-mtu-discovery",
            ],
        )

    def test_ios_tunnel_interfaces_deleted_one(self):
        result = self._run(
            RUNNING,
            {"config": [{"name": "Tunnel1501"}, {"name": "Tunnel9"}], "state": "deleted"},
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Tunnel1501",
                "no tunnel source",
                "no tunnel destination",
                "no tunnel key",
                "no tunnel vrf MGMT",
            ],
        )

    def test_ios_tunnel_interfaces_deleted_all(self):
        result = self._run(RUNNING, {"state": "deleted"})
        self.assertEqual(result["commands"].count("interface Tunnel1501"), 1)
        self.assertEqual(result["commands"].count("interface Tunnel1502"), 1)
        self.assertIn("no tunnel mode", result["commands"])

    def test_ios_tunnel_interfaces_deleted_all_empty_device(self):
        result = self._run("", {"state": "deleted"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_tunnel_interfaces_rendered(self):
        set_module_args(
            {
                "config": [
                    {
                        "name": "Tunnel1502",
                        "mode": "gre_multipoint",
                        "source": "Loopback499",
                        "key": 7,
                    },
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "interface Tunnel1502",
                "tunnel mode gre multipoint",
                "tunnel source Loopback499",
                "tunnel key 7",
            ],
        )

    def test_ios_tunnel_interfaces_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "name": "Tunnel1501",
                    "source": "Loopback499",
                    "destination": "198.51.100.101",
                    "key": 1501,
                    "vrf": "MGMT",
                },
                {
                    "name": "Tunnel1502",
                    "source": "GigabitEthernet1/0/12",
                    "mode": "gre_ipv6",
                    "destination": "2001:DB8::1",
                    "ttl": 64,
                    "checksum": True,
                    "path_mtu_discovery": True,
                },
            ],
        )

    def test_ios_tunnel_interfaces_parsed_long_path_mtu_discovery_and_sample_lines_of_other_modules(
        self,
    ):
        # the other lines of a tunnel interface belong to other modules and are not touched
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    interface Tunnel1501
                     description Tunnel to the remote site
                     vrf forwarding CUSTOMER
                     ip address 192.0.2.82 255.255.255.252
                     no ip redirects
                     ip mtu 1400
                     tunnel source Loopback499
                     tunnel destination 198.51.100.101
                     tunnel path-mtu-discovery age-timer 20
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "name": "Tunnel1501",
                    "source": "Loopback499",
                    "destination": "198.51.100.101",
                    "path_mtu_discovery": True,
                },
            ],
        )

    def test_ios_tunnel_interfaces_gathered_ignores_unsupported_modes(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Tunnel1
             tunnel source Loopback499
             tunnel mode ipsec ipv4
             tunnel key 9
            interface Tunnel2
             tunnel source Loopback499
            """,
        )
        set_module_args({"state": "gathered"})
        with patch.object(ios_tunnel_interfaces.AnsibleModule, "warn") as warn:
            result = self.execute_module(changed=False)
        # the key of Tunnel1 must not end up on Tunnel2 nor anywhere else
        self.assertEqual(result["gathered"], [{"name": "Tunnel2", "source": "Loopback499"}])
        warn.assert_called_once()
        self.assertIn("Tunnel1", warn.call_args[0][0])

    def test_ios_tunnel_interfaces_unsupported_mode_is_not_overridden(self):
        result = self._run(
            "interface Tunnel1\n tunnel mode ipsec ipv4\n tunnel source Loopback499\n",
            {"config": [{"name": "Tunnel2", "source": "Loopback499"}], "state": "overridden"},
        )
        self.assertEqual(result["commands"], ["interface Tunnel2", "tunnel source Loopback499"])
