#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_evpn_evi
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosEvpnEviModule(TestIosModule):
    module = ios_evpn_evi

    def setUp(self):
        super(TestIosEvpnEviModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_evi.evpn_evi."
            "Evpn_eviFacts.get_evpn_evi_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosEvpnEviModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_evpn_evi_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            !
            l2vpn evpn instance 201 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type ingress
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "route_distinguisher": "1:1",
                        "default_gateway": {
                            "advertise": {"enable": False},
                        },
                        "ip": {
                            "local_learning": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "static",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                        "ip": {
                            "local_learning": {"disable": True},
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "l2vpn evpn instance 101 vlan-based",
            "ip local-learning enable",
            "replication-type ingress",
            "rd 1:1",
            "l2vpn evpn instance 202 vlan-based",
            "default-gateway advertise enable",
            "ip local-learning disable",
            "replication-type static",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             rd 1:1
             replication-type ingress
             ip local-learning enable
            !
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            !
            l2vpn evpn instance 201 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type static
             ip local-learning disable
             default-gateway advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "route_distinguisher": "1:1",
                        "default_gateway": {
                            "advertise": {"enable": False},
                        },
                        "ip": {
                            "local_learning": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "static",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                        "ip": {
                            "local_learning": {"disable": True},
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_deleted_evi(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type ingress
             default-gateway advertise enable
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type static
             default-gateway advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "no l2vpn evpn instance 101 vlan-based",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type ingress
             default-gateway advertise enable
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type static
             default-gateway advertise enable
            """,
        )
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "no l2vpn evpn instance 101 vlan-based",
            "no l2vpn evpn instance 102 vlan-based",
            "no l2vpn evpn instance 202 vlan-based",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_deleted_blank(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(config=list(), state="deleted"))
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_replaced(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             rd 1:1
             replication-type ingress
             ip local-learning enable
            !
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            !
            l2vpn evpn instance 201 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type static
             ip local-learning disable
             default-gateway advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "ingress",
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "l2vpn evpn instance 101 vlan-based",
            "default-gateway advertise enable",
            "no ip local-learning enable",
            "no rd 1:1",
            "l2vpn evpn instance 202 vlan-based",
            "no default-gateway advertise enable",
            "no ip local-learning disable",
            "replication-type ingress",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_replaced_idempotent(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type ingress
             default-gateway advertise enable
            !
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            !
            l2vpn evpn instance 201 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type ingress
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "ingress",
                    },
                ],
                state="replaced",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_overridden(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type ingress
             default-gateway advertise enable
            !
            l2vpn evpn instance 102 vlan-based
             encapsulation vxlan
             replication-type ingress
            !
            l2vpn evpn instance 201 vlan-based
             encapsulation vxlan
             replication-type static
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type ingress
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "static",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "no l2vpn evpn instance 102 vlan-based",
            "no l2vpn evpn instance 201 vlan-based",
            "l2vpn evpn instance 202 vlan-based",
            "default-gateway advertise enable",
            "replication-type static",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_evpn_evi_overridden_idempotent(self):
        """both the replaced and overridden states are supported to have same behaviour"""
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 101 vlan-based
             encapsulation vxlan
             replication-type ingress
             default-gateway advertise enable
            !
            l2vpn evpn instance 202 vlan-based
             encapsulation vxlan
             replication-type static
             default-gateway advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "evi": "101",
                        "replication_type": "ingress",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                    {
                        "evi": "202",
                        "replication_type": "static",
                        "default_gateway": {
                            "advertise": {"enable": True},
                        },
                    },
                ],
                state="overridden",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
