#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_acls
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule


class TestIosAclsModule(TestIosModule):
    module = ios_acls

    def setUp(self):
        super(TestIosAclsModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.acls.acls."
            "AclsFacts.get_acl_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosAclsModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_acls_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="std_acl",
                                acl_type="standard",
                                aces=[
                                    dict(
                                        grant="deny",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                    )
                                ],
                            ),
                            dict(
                                name="in_to_out",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="permit",
                                        protocol="tcp",
                                        source=dict(host="10.1.1.2"),
                                        destination=dict(
                                            host="172.16.1.1",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        log_input=dict(
                                            user_cookie="test_logInput"
                                        ),
                                        protocol="ip",
                                        source=dict(any=True),
                                        destination=dict(any=True),
                                    ),
                                ],
                            ),
                            dict(
                                name="test_acl_merge",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        protocol="tcp",
                                        sequence=100,
                                        source=dict(host="192.0.2.1"),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        sequence="200",
                                        source=dict(
                                            object_group="test_network_og"
                                        ),
                                        destination=dict(
                                            object_group="test_network_og"
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
                state="merged",
            )
        )
        result = self.execute_module(changed=True)

        commands = [
            "ip access-list standard std_acl",
            "deny 192.0.2.0 0.0.0.255",
            "ip access-list extended test_acl_merge",
            "100 permit tcp host 192.0.2.1 192.0.2.0 0.0.0.255 eq www",
            "200 deny tcp object-group test_network_og object-group test_network_og ack dscp ef ttl eq 10",
            "ip access-list extended in_to_out",
            "permit tcp host 10.1.1.2 host 172.16.1.1 eq telnet",
            "deny ip any any log-input test_logInput",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(acl_type="standard", name="test_acl"),
                            dict(
                                name="110",
                                aces=[
                                    dict(
                                        grant="permit",
                                        log=dict(user_cookie="testLog"),
                                        protocol="tcp",
                                        sequence="10",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            any=True,
                                            port_protocol=dict(eq="22"),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="20",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="30",
                                        source=dict(
                                            object_group="test_network_og"
                                        ),
                                        destination=dict(any=True),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="R1_TRAFFIC",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        sequence="10",
                                        source=dict(
                                            any="true",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        destination=dict(
                                            any="true",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="af11",
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_acls_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="replace_acl",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.101.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        tos=dict(min_monetary_cost=True),
                                    )
                                ],
                            ),
                            dict(
                                name="test_acl",
                                acl_type="standard",
                                aces=[dict(remarks=["Another remark here"])],
                            ),
                        ],
                    )
                ],
                state="replaced",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended replace_acl",
            "deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos min-monetary-cost",
            "ip access-list standard test_acl",
            "remark Another remark here",
            "no remark remark check 1",
            "no remark some random remark 2",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(acl_type="standard", name="test_acl"),
                            dict(
                                name="110",
                                aces=[
                                    dict(
                                        grant="permit",
                                        log=dict(user_cookie="testLog"),
                                        protocol="tcp",
                                        sequence="10",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            any=True,
                                            port_protocol=dict(eq="22"),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="20",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="30",
                                        source=dict(
                                            object_group="test_network_og"
                                        ),
                                        destination=dict(any=True),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_acls_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="150",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(syn="true")
                                        ),
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        destination=dict(
                                            address="198.51.110.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="overridden",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ipv6 access-list R1_TRAFFIC",
            "no ip access-list standard test_acl",
            "no ip access-list extended 110",
            "ip access-list extended 150",
            "deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(acl_type="standard", name="test_acl"),
                            dict(
                                name="110",
                                aces=[
                                    dict(
                                        grant="permit",
                                        log=dict(user_cookie="testLog"),
                                        protocol="tcp",
                                        sequence="10",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            any=True,
                                            port_protocol=dict(eq="22"),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="20",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="30",
                                        source=dict(
                                            object_group="test_network_og"
                                        ),
                                        destination=dict(any=True),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="R1_TRAFFIC",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        sequence="10",
                                        source=dict(
                                            any="true",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        destination=dict(
                                            any="true",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="af11",
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_acls_deleted_afi_based(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(dict(config=[dict(afi="ipv4")], state="deleted"))
        result = self.execute_module(changed=True)
        commands = [
            "no ip access-list extended 110",
            "no ip access-list standard test_acl",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_deleted_acl_based(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            IPv6 access list R1_TRAFFIC
                deny tcp any eq www any eq telnet ack dscp af11 sequence 10
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="110",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="10",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    )
                                ],
                            )
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="R1_TRAFFIC",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        sequence="10",
                                        source=dict(
                                            any="true",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        destination=dict(
                                            any="true",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="af11",
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="deleted",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip access-list extended 110",
            "no ipv6 access-list R1_TRAFFIC",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="110",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="deny",
                                        sequence="10",
                                        remarks=[
                                            "check for remark",
                                            "remark for acl 110",
                                        ],
                                        protocol_options=dict(
                                            tcp=dict(syn="true")
                                        ),
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="rendered",
            )
        )
        commands = [
            "ip access-list extended 110",
            "10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10",
            "remark check for remark",
            "remark remark for acl 110",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_acls_parsed(self):
        set_module_args(
            dict(
                running_config="IPv6 access list R1_TRAFFIC\ndeny tcp any eq www any eq telnet ack dscp af11 sequence 10",
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "destination": {
                                    "any": True,
                                    "port_protocol": {"eq": "telnet"},
                                },
                                "dscp": "af11",
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 10,
                                "source": {
                                    "any": True,
                                    "port_protocol": {"eq": "www"},
                                },
                            }
                        ],
                        "name": "R1_TRAFFIC",
                    }
                ],
                "afi": "ipv6",
            }
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_acls_overridden_remark(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            Extended IP access list 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any echo dscp ef ttl eq 10
            access-list 110 remark test ab.
            access-list 110 remark test again ab.
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(acl_type="standard", name="test_acl"),
                            dict(
                                name="110",
                                aces=[
                                    dict(
                                        grant="permit",
                                        log=dict(user_cookie="testLog"),
                                        protocol="tcp",
                                        sequence="10",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            any=True,
                                            port_protocol=dict(eq="22"),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="20",
                                        source=dict(
                                            address="192.0.2.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="192.0.3.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            icmp=dict(echo="true")
                                        ),
                                        sequence="30",
                                        source=dict(
                                            object_group="test_network_og"
                                        ),
                                        destination=dict(any=True),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="R1_TRAFFIC",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        sequence="10",
                                        source=dict(
                                            any="true",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        destination=dict(
                                            any="true",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="af11",
                                    ),
                                    dict(
                                        remarks=[
                                            "ipv6 remarks one",
                                            "ipv6 remarks test 2",
                                        ]
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        result = self.execute_module(changed=True, sort=True)
        commands = [
            "ip access-list extended 110",
            "no remark test ab.",
            "no remark test again ab.",
            "ipv6 access-list R1_TRAFFIC",
            "deny tcp any eq www any eq telnet ack dscp af11 sequence 10",
            "remark ipv6 remarks one",
            "remark ipv6 remarks test 2",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden_option(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="113",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(
                                            tcp=dict(ack="true")
                                        ),
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.101.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        tos=dict(min_monetary_cost=True),
                                    ),
                                    dict(
                                        grant="permit",
                                        protocol_options=dict(
                                            protocol_number=433
                                        ),
                                        source=dict(
                                            address="198.51.101.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.102.0",
                                            wildcard_bits="0.0.0.255",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        log=dict(user_cookie="check"),
                                        tos=dict(max_throughput=True),
                                    ),
                                    dict(
                                        grant="permit",
                                        source=dict(
                                            address="198.51.102.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.103.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        precedence=10,
                                        tos=dict(normal=True),
                                    ),
                                    dict(
                                        grant="permit",
                                        source=dict(
                                            address="198.51.105.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.106.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        time_range=20,
                                        tos=dict(max_throughput=True),
                                    ),
                                ],
                            ),
                            dict(
                                name="test_acl",
                                acl_type="standard",
                                aces=[dict(remarks=["Another remark here"])],
                            ),
                        ],
                    )
                ],
                state="overridden",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended 113",
            "deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos min-monetary-cost",
            "permit 198.51.102.0 0.0.0.255 198.51.103.0 0.0.0.255 precedence 10 tos normal",
            "permit 433 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 eq telnet log check tos max-throughput",
            "permit 198.51.105.0 0.0.0.255 198.51.106.0 0.0.0.255 time-range 20 tos max-throughput",
            "ip access-list standard test_acl",
            "remark Another remark here",
            "no remark remark check 1",
            "no remark some random remark 2",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden_clear(self):
        self.execute_show_command.return_value = dedent(
            """\
            """
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="113",
                                acl_type="extended",
                                aces=[
                                    dict(
                                        grant="deny",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.101.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        tos=dict(max_reliability=True),
                                        fragments=10,
                                    ),
                                    dict(
                                        remarks=["extended ACL remark"],
                                        grant="permit",
                                        source=dict(
                                            address="198.51.101.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(
                                            address="198.51.102.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        log=dict(user_cookie="check"),
                                        tos=dict(service_value="119"),
                                    ),
                                ],
                            ),
                            dict(
                                name="23",
                                acl_type="standard",
                                aces=[dict(remarks=["check remark here"])],
                            ),
                        ],
                    )
                ],
                state="overridden",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended 113",
            "deny 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 fragments 10 tos max-reliability",
            "permit 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 log check tos 119",
            "remark extended ACL remark",
            "ip access-list standard 23",
            "remark check remark here",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_delete_acl(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list 2
                30 permit 172.16.1.11
                20 permit 172.16.1.10 log
                10 permit 172.16.1.2
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="2",
                                aces=[
                                    dict(
                                        grant="permit",
                                        source=dict(host="192.0.2.1"),
                                        sequence=10,
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="deleted",
            )
        )

        result = self.execute_module(changed=True)
        commands = ["no ip access-list standard 2"]
        self.assertEqual(result["commands"], commands)

    def test_ios_failed_extra_param_standard_acl(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="test_acl",
                                acl_type="standard",
                                aces=[
                                    dict(
                                        grant="deny",
                                        sequence=10,
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                        destination=dict(any="True"),
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="overridden",
            )
        )
        result = self.execute_module(failed=True)
        self.assertEqual(result, {"failed": True})

    def test_ios_failed_update_with_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            Standard IP access list test_acl
                30 permit 172.16.1.11
                20 permit 172.16.1.10 log
                10 permit 172.16.1.2
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="test_acl",
                                aces=[
                                    dict(
                                        grant="permit",
                                        source=dict(host="192.0.2.1"),
                                        sequence=10,
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="merged",
            )
        )

        result = self.execute_module(failed=True)
        self.assertEqual(result, {"failed": True})
