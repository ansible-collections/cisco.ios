#
# (c) 2023 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_evpn_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosEvpnGlobalModule(TestIosModule):
    module = ios_evpn_global

    def setUp(self):
        super(TestIosEvpnGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_global.evpn_global."
            "Evpn_globalFacts.get_evpn_global_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosEvpnGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_evpn_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             replication-type static
             router-id Loopback1
             default-gateway advertise
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    replication_type="ingress",
                    route_target=dict(auto=dict(vni=True)),
                    default_gateway=dict(advertise=False),
                    ip=dict(local_learning=dict(disable=True)),
                    flooding_suppression=dict(address_resolution=dict(disable=False)),
                ),
                state="merged",
            ),
        )
        commands = [
            "l2vpn evpn",
            "no default-gateway advertise",
            "replication-type ingress",
            "route-target auto vni",
            "ip local-learning disable",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
             l2vpn evpn
              replication-type ingress
              router-id Loopback1
              ip local-learning disable
              route-target auto vni
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    replication_type="ingress",
                    route_target=dict(auto=dict(vni=True)),
                    default_gateway=dict(advertise=False),
                    ip=dict(local_learning=dict(disable=True)),
                    flooding_suppression=dict(address_resolution=dict(disable=False)),
                ),
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             replication-type static
             flooding-suppression address-resolution disable
             router-id Loopback2
             default-gateway advertise
            """,
        )
        set_module_args(dict(config=dict(), state="deleted"))
        commands = [
            "no l2vpn evpn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_global_deleted_blank(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(config=dict(), state="deleted"))
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_global_replaced_overridden(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             replication-type ingress
             router-id Loopback1
             ip local-learning disable
             route-target auto vni
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    replication_type="static",
                    router_id="Loopback2",
                    default_gateway=dict(advertise=True),
                    flooding_suppression=dict(address_resolution=dict(disable=True)),
                ),
                state="replaced",
            ),
        )
        commands = [
            "l2vpn evpn",
            "default-gateway advertise",
            "flooding-suppression address-resolution disable",
            "no ip local-learning disable",
            "replication-type static",
            "no route-target auto vni",
            "router-id Loopback2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_global_replaced_overridden_idempotent(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
             l2vpn evpn
              replication-type static
              flooding-suppression address-resolution disable
              router-id Loopback2
              default-gateway advertise
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    replication_type="static",
                    router_id="Loopback2",
                    default_gateway=dict(advertise=True),
                    flooding_suppression=dict(address_resolution=dict(disable=True)),
                ),
                state="overridden",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
