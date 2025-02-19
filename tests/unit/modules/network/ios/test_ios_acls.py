#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_acls
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosAclsModule(TestIosModule):
    module = ios_acls

    def setUp(self):
        super(TestIosAclsModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.acls.acls."
            "AclsFacts.get_acl_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.mock_execute_show_command_name_specific = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.acls.acls."
            "AclsFacts.get_acl_names",
        )
        self.execute_show_command_name = self.mock_execute_show_command_name_specific.start()

    def tearDown(self):
        super(TestIosAclsModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()
        self.mock_execute_show_command_name_specific.stop()

    def test_ios_acls_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            ip access-list extended test_pre
                10 permit ip any any precedence internet
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                aces=[
                                    dict(
                                        destination=dict(any=True),
                                        grant="permit",
                                        precedence="immediate",
                                        protocol="ip",
                                        sequence=20,
                                        source=dict(any=True),
                                    ),
                                ],
                                acl_type="extended",
                                name="test_pre",
                            ),
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
                                    ),
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
                                        log_input=dict(user_cookie="test_logInput"),
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
                                            port_protocol=dict(eq="80"),
                                        ),
                                        protocol="tcp",
                                        sequence=100,
                                        source=dict(host="192.0.2.1"),
                                    ),
                                    dict(
                                        grant="deny",
                                        protocol_options=dict(tcp=dict(ack="True")),
                                        sequence="200",
                                        source=dict(object_group="test_network_og"),
                                        destination=dict(
                                            object_group="test_network_og",
                                        ),
                                        dscp="ef",
                                        ttl=dict(eq=10),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
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
            "ip access-list extended test_pre",
            "20 permit ip any any precedence immediate",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_merged_remarks_positional(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "acls": [
                            {
                                "aces": [
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "sequence": 10,
                                        "source": {
                                            "address": "10.40.150.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                    },
                                    {
                                        "destination": {
                                            "address": "10.40.150.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "sequence": 20,
                                        "source": {"any": True},
                                    },
                                ],
                                "acl_type": "extended",
                                "name": "199",
                            },
                            {
                                "aces": [
                                    {
                                        "grant": "permit",
                                        "sequence": 10,
                                        "source": {
                                            "address": "10.182.250.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                    },
                                ],
                                "acl_type": "standard",
                                "name": "42",
                            },
                            {
                                "aces": [
                                    {
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "22"},
                                        },
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "sequence": 10,
                                        "source": {
                                            "address": "10.57.66.243",
                                            "wildcard_bits": "0.0.0.7",
                                        },
                                    },
                                    {
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "22"},
                                        },
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "sequence": 20,
                                        "source": {"host": "10.160.114.111"},
                                    },
                                    {
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "22"},
                                        },
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "sequence": 30,
                                        "source": {"host": "10.160.115.22"},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "deny",
                                        "log": {"set": True},
                                        "protocol": "ip",
                                        "sequence": 40,
                                        "source": {"any": True},
                                    },
                                ],
                                "acl_type": "extended",
                                "name": "NET-MGMT-VTY",
                            },
                            {
                                "aces": [
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "remarks": [
                                            "FIRST REMARK BEFORE LINE 10",
                                            "============",
                                            "ALLOW HOST FROM BUILDING 10",
                                        ],
                                        "sequence": 10,
                                        "source": {"host": "1.1.1.1"},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "remarks": [
                                            "FIRST REMARK BEFORE LINE 20",
                                            "============",
                                            "ALLOW HOST FROM BUILDING 20",
                                        ],
                                        "sequence": 20,
                                        "source": {"host": "2.2.2.2"},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "remarks": [
                                            "FIRST REMARK BEFORE LINE 30",
                                            "============",
                                            "ALLOW NEW HOST FROM BUILDING 10",
                                        ],
                                        "sequence": 30,
                                        "source": {"host": "3.3.3.3"},
                                    },
                                    {
                                        "remarks": [
                                            "FIRST REMARK AT END OF ACL",
                                            "SECOND REMARK AT END OF ACL",
                                        ],
                                    },
                                ],
                                "acl_type": "extended",
                                "name": "TEST",
                            },
                            {
                                "aces": [
                                    {
                                        "remarks": [
                                            "empty remark 1",
                                            "empty remark 2",
                                            "empty remark never ends",
                                        ],
                                    },
                                ],
                                "acl_type": "extended",
                                "name": "empty_ip_ex_acl",
                            },
                            {
                                "aces": [
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "remarks": [
                                            "I am a test ace",
                                            "I am right after the test ace",
                                            "I third the test ace",
                                        ],
                                        "sequence": 100,
                                        "source": {"host": "100.100.100.100"},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "remarks": [
                                            "I am the next test ace",
                                            "I am the next ace to the next ace",
                                        ],
                                        "sequence": 110,
                                        "source": {"host": "10.40.150.0"},
                                    },
                                    {"remarks": ["I am the peace ace", "Peace out"]},
                                ],
                                "acl_type": "extended",
                                "name": "mytest",
                            },
                            {
                                "aces": [
                                    {
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {
                                                "eq": "135",
                                            },
                                        },
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "sequence": 10,
                                        "source": {"any": True},
                                    },
                                    {
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {
                                                "eq": "135",
                                            },
                                        },
                                        "grant": "permit",
                                        "protocol": "udp",
                                        "sequence": 20,
                                        "source": {"any": True},
                                    },
                                ],
                                "name": "example",
                                "acl_type": "extended",
                            },
                        ],
                        "afi": "ipv4",
                    },
                    {
                        "acls": [
                            {
                                "aces": [
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "ipv6",
                                        "sequence": 10,
                                        "source": {
                                            "address": "2001:ABAD:BEEF:1221::/64",
                                        },
                                    },
                                    {
                                        "destination": {
                                            "host": "2001:ABAD:BEEF:1212::1",
                                            "port_protocol": {"eq": "www"},
                                        },
                                        "grant": "deny",
                                        "protocol": "tcp",
                                        "sequence": 20,
                                        "source": {"host": "2001:ABAD:BEEF:2345::1"},
                                    },
                                ],
                                "name": "R1_TRAFFIC",
                            },
                            {
                                "aces": [
                                    {"remarks": ["empty remark 1"], "sequence": 10},
                                    {"remarks": ["empty remark 2"], "sequence": 20},
                                    {
                                        "remarks": ["empty remark never ends"],
                                        "sequence": 30,
                                    },
                                ],
                                "name": "empty_ipv6_acl",
                            },
                            {
                                "aces": [
                                    {"remarks": ["I am a ipv6 ace"], "sequence": 10},
                                    {"remarks": ["I am test"], "sequence": 20},
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "sequence": 30,
                                        "source": {"any": True},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "udp",
                                        "sequence": 40,
                                        "source": {"any": True},
                                    },
                                    {
                                        "remarks": ["I am new set of ipv6 ace"],
                                        "sequence": 50,
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol": "icmp",
                                        "sequence": 60,
                                        "source": {"any": True},
                                    },
                                ],
                                "name": "ipv6_acl",
                            },
                        ],
                        "afi": "ipv6",
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended 199",
            "10 permit ip 10.40.150.0 0.0.0.255 any",
            "20 permit ip any 10.40.150.0 0.0.0.255",
            "ip access-list standard 42",
            "10 permit 10.182.250.0 0.0.0.255",
            "ip access-list extended empty_ip_ex_acl",
            "remark empty remark 1",
            "remark empty remark 2",
            "remark empty remark never ends",
            "ip access-list extended NET-MGMT-VTY",
            "10 permit tcp 10.57.66.243 0.0.0.7 any eq 22",
            "20 permit tcp host 10.160.114.111 any eq 22",
            "30 permit tcp host 10.160.115.22 any eq 22",
            "40 deny ip any any log",
            "ip access-list extended mytest",
            "100 remark I am a test ace",
            "100 remark I am right after the test ace",
            "100 remark I third the test ace",
            "100 permit ip host 100.100.100.100 any",
            "110 remark I am the next test ace",
            "110 remark I am the next ace to the next ace",
            "110 permit ip host 10.40.150.0 any",
            "remark I am the peace ace",
            "remark Peace out",
            "ip access-list extended example",
            "10 permit tcp any any eq msrpc",
            "20 permit udp any any eq 135",
            "ip access-list extended TEST",
            "10 remark FIRST REMARK BEFORE LINE 10",
            "10 remark ============",
            "10 remark ALLOW HOST FROM BUILDING 10",
            "10 permit ip host 1.1.1.1 any",
            "20 remark FIRST REMARK BEFORE LINE 20",
            "20 remark ============",
            "20 remark ALLOW HOST FROM BUILDING 20",
            "20 permit ip host 2.2.2.2 any",
            "30 remark FIRST REMARK BEFORE LINE 30",
            "30 remark ============",
            "30 remark ALLOW NEW HOST FROM BUILDING 10",
            "30 permit ip host 3.3.3.3 any",
            "remark FIRST REMARK AT END OF ACL",
            "remark SECOND REMARK AT END OF ACL",
            "ipv6 access-list R1_TRAFFIC",
            "permit ipv6 2001:ABAD:BEEF:1221::/64 any sequence 10",
            "deny tcp host 2001:ABAD:BEEF:2345::1 host 2001:ABAD:BEEF:1212::1 eq www sequence 20",
            "ipv6 access-list empty_ipv6_acl",
            "10 remark empty remark 1",
            "20 remark empty remark 2",
            "30 remark empty remark never ends",
            "ipv6 access-list ipv6_acl",
            "10 remark I am a ipv6 ace",
            "20 remark I am test",
            "permit tcp any any sequence 30",
            "permit udp any any sequence 40",
            "50 remark I am new set of ipv6 ace",
            "permit icmp any any sequence 60",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent("")

        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {"name": "110", "acl_type": "extended"},
                            {"name": "test_acl", "acl_type": "standard"},
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "acls": [
                            {
                                "name": "R1_TRAFFIC",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "deny",
                                        "protocol": "tcp",
                                        "source": {
                                            "any": True,
                                            "port_protocol": {"eq": "www"},
                                        },
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "telnet"},
                                        },
                                        "dscp": "af11",
                                        "protocol_options": {"tcp": {"ack": True}},
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_acls_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            ip access-list standard testRobustReplace
                10 remark Remarks for 10
                10 permit 192.168.1.0 0.0.0.255
                20 remark Remarks for 20
                20 permit 0.0.0.0 255.0.0.0
                30 remark Remarks for 30
                30 permit 172.16.0.0 0.15.255.255
                40 remark Remarks for 40
                40 permit 192.0.2.0 0.0.0.255
                50 remark Remarks for 50
                50 permit 198.51.100.0 0.0.0.255
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            Standard IP access list testRobustReplace
            """,
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
                                        protocol_options=dict(tcp=dict(ack="True")),
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
                                ],
                            ),
                            dict(
                                name="test_acl",
                                acl_type="standard",
                                aces=[dict(remarks=["Another remark here"])],
                            ),
                            dict(
                                name="testRobustReplace",
                                acl_type="standard",
                                aces=[
                                    dict(
                                        sequence=10,
                                        grant="permit",
                                        remarks=["Remarks for 10"],
                                        source=dict(
                                            address="192.168.1.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended replace_acl",
            "deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos min-monetary-cost",
            "ip access-list standard test_acl",
            "no remark",
            "remark Another remark here",
            "ip access-list standard testRobustReplace",
            "no 20 remark",
            "no 20 permit 0.0.0.0 255.0.0.0",
            "no 30 remark",
            "no 30 permit 172.16.0.0 0.15.255.255",
            "no 40 remark",
            "no 40 permit 192.0.2.0 0.0.0.255",
            "no 50 remark",
            "no 50 permit 198.51.100.0 0.0.0.255",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            ip access-list extended test_pre
                10 permit ip any any precedence internet
            ip access-list extended test-idem
                10 permit ip host 10.153.14.21 any
                20 permit ip host 10.153.14.22 any
            ip access-list standard test-acl-no-seq
                permit 10.0.0.0 0.255.255.255
                permit 172.31.16.0 0.0.7.255
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            Standard IP access list test-acl-no-seq
            Extended IP access list 110
            Extended IP access list test-idem
            Extended IP access list test_pre
            IPv6 access list R1_TRAFFIC
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {
                                "name": "110",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {
                                            "address": "198.51.100.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "22"},
                                        },
                                        "log": {"set": True, "user_cookie": "testLog"},
                                    },
                                    {
                                        "sequence": 20,
                                        "grant": "deny",
                                        "protocol": "icmp",
                                        "source": {
                                            "address": "192.0.2.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "address": "192.0.3.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "dscp": "ef",
                                        "ttl": {"eq": 10},
                                        "protocol_options": {"icmp": {"echo": True}},
                                    },
                                    {
                                        "sequence": 30,
                                        "grant": "deny",
                                        "protocol": "icmp",
                                        "source": {"object_group": "test_network_og"},
                                        "destination": {"any": True},
                                        "dscp": "ef",
                                        "ttl": {"eq": 10},
                                    },
                                ],
                            },
                            {"name": "test_acl", "acl_type": "standard"},
                            {
                                "aces": [
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol_options": {"ip": True},
                                        "sequence": 10,
                                        "source": {"host": "10.153.14.21"},
                                    },
                                    {
                                        "destination": {"any": True},
                                        "grant": "permit",
                                        "protocol_options": {"ip": True},
                                        "sequence": 20,
                                        "source": {"host": "10.153.14.22"},
                                    },
                                ],
                                "acl_type": "extended",
                                "name": "test-idem",
                            },
                            {
                                "name": "test_pre",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"any": True},
                                        "destination": {"any": True},
                                        "precedence": "internet",
                                    },
                                ],
                            },
                            {
                                "name": "test-acl-no-seq",
                                "acl_type": "standard",
                                "aces": [
                                    {
                                        "grant": "permit",
                                        "source": {
                                            "address": "10.0.0.0",
                                            "wildcard_bits": "0.255.255.255",
                                        },
                                    },
                                    {
                                        "grant": "permit",
                                        "source": {
                                            "address": "172.31.16.0",
                                            "wildcard_bits": "0.0.7.255",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "acls": [
                            {
                                "name": "R1_TRAFFIC",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "deny",
                                        "protocol": "tcp",
                                        "source": {
                                            "any": True,
                                            "port_protocol": {"eq": "www"},
                                        },
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "telnet"},
                                        },
                                        "dscp": "af11",
                                        "protocol_options": {"tcp": {"ack": True}},
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_acls_replaced_changetype(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="110",
                                acl_type="standard",
                                aces=[
                                    dict(
                                        grant="deny",
                                        source=dict(
                                            address="198.51.100.0",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                    ),
                                ],
                            ),
                            dict(
                                name="test_acl",
                                acl_type="standard",
                                aces=[dict(remarks=["Another remark here"])],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ip access-list extended 110",
            "ip access-list standard 110",
            "deny 198.51.100.0 0.0.0.255",
            "ip access-list standard test_acl",
            "no remark",
            "remark Another remark here",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
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
                                        protocol_options=dict(tcp=dict(syn="True")),
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
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
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
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ip access-list reflexive MIRROR
                permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50200 (2 matches) (time left 123)
                permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50201 (2 matches) (time left 345)
                permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50202 (2 matches) (time left 678)
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent(
            """\
            Standard IP access list test_acl
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {
                                "name": "110",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {
                                            "address": "198.51.100.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "22"},
                                        },
                                        "log": {"set": True, "user_cookie": "testLog"},
                                    },
                                    {
                                        "sequence": 20,
                                        "grant": "deny",
                                        "protocol": "icmp",
                                        "source": {
                                            "address": "192.0.2.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "address": "192.0.3.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "dscp": "ef",
                                        "ttl": {"eq": 10},
                                        "protocol_options": {"icmp": {"echo": True}},
                                    },
                                    {
                                        "sequence": 30,
                                        "grant": "deny",
                                        "protocol": "icmp",
                                        "source": {"object_group": "test_network_og"},
                                        "destination": {"any": True},
                                        "dscp": "ef",
                                        "ttl": {"eq": 10},
                                    },
                                ],
                            },
                            {"name": "test_acl", "acl_type": "standard"},
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "acls": [
                            {
                                "name": "R1_TRAFFIC",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "deny",
                                        "protocol": "tcp",
                                        "source": {
                                            "any": True,
                                            "port_protocol": {"eq": "www"},
                                        },
                                        "destination": {
                                            "any": True,
                                            "port_protocol": {"eq": "telnet"},
                                        },
                                        "dscp": "af11",
                                        "protocol_options": {"tcp": {"ack": True}},
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=False)
        command = []
        self.assertEqual(sorted(result["commands"]), sorted(command))

    def test_ios_acls_deleted_afi_based(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
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
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
            ipv6 access-list R1_TRAFFIC
                sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
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
                                        protocol_options=dict(icmp=dict(echo="True")),
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
                                        protocol_options=dict(tcp=dict(ack="True")),
                                        sequence="10",
                                        source=dict(
                                            any="True",
                                            port_protocol=dict(eq="www"),
                                        ),
                                        destination=dict(
                                            any="True",
                                            port_protocol=dict(eq="telnet"),
                                        ),
                                        dscp="af11",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = ["no ip access-list extended 110", "no ipv6 access-list R1_TRAFFIC"]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_rendered(self):
        self.execute_show_command_name.return_value = dedent("")
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
                                        protocol_options=dict(tcp=dict(syn="True")),
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
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "ip access-list extended 110",
            "10 remark check for remark",
            "10 remark remark for acl 110",
            "10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_acls_parsed(self):
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                running_config="""ipv6 access-list R1_TRAFFIC\n sequence 10 deny tcp any eq www any range 10 20 ack dscp af11
                20 permit icmp host 192.0.2.1 host 192.0.2.2 echo\n 30 permit icmp host 192.0.2.3 host 192.0.2.4 echo-reply""",
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "afi": "ipv6",
                "acls": [
                    {
                        "name": "R1_TRAFFIC",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "deny",
                                "protocol": "tcp",
                                "source": {"any": True, "port_protocol": {"eq": "www"}},
                                "destination": {
                                    "any": True,
                                    "port_protocol": {
                                        "range": {"start": 10, "end": 20},
                                    },
                                },
                                "dscp": "af11",
                                "protocol_options": {"tcp": {"ack": True}},
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "protocol": "icmp",
                                "source": {"host": "192.0.2.1"},
                                "destination": {"host": "192.0.2.2"},
                                "protocol_options": {"icmp": {"echo": True}},
                            },
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "protocol": "icmp",
                                "source": {"host": "192.0.2.3"},
                                "destination": {"host": "192.0.2.4"},
                                "protocol_options": {"icmp": {"echo_reply": True}},
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_acls_parsed_matches(self):
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            {
                "running_config": """ip access-list standard R1_TRAFFIC
                 10 permit 10.11.12.13
                 40 permit 128.0.0.0 63.255.255.255
                 60 permit 134.107.136.0 0.0.0.255""",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "afi": "ipv4",
                "acls": [
                    {
                        "name": "R1_TRAFFIC",
                        "acl_type": "standard",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "source": {"host": "10.11.12.13"},
                            },
                            {
                                "sequence": 40,
                                "grant": "permit",
                                "source": {
                                    "address": "128.0.0.0",
                                    "wildcard_bits": "63.255.255.255",
                                },
                            },
                            {
                                "sequence": 60,
                                "grant": "permit",
                                "source": {
                                    "address": "134.107.136.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_acls_overridden_remark(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list extended 110
                10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
                20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
                30 deny icmp object-group test_network_og any dscp ef ttl eq 10
                remark test ab.
                remark test again ab.
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {
                                "name": "110",
                                "acl_type": "extended",
                                "aces": [{"remarks": ["test ab.", "test again ab."]}],
                            },
                            {"name": "test_acl", "acl_type": "standard"},
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True, sort=True)
        cmds = [
            "ip access-list extended 110",
            "no 10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log testLog",
            "no 20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10",
            "no 30 deny icmp object-group test_network_og any dscp ef ttl eq 10",
        ]
        self.assertEqual(sorted(result["commands"]), cmds)

    def test_ios_acls_overridden_option(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """,
        )
        self.execute_show_command_name.return_value = dedent("")

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
                                        protocol_options=dict(tcp=dict(ack="True")),
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
                                        protocol_options=dict(protocol_number=433),
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
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended 113",
            "deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos min-monetary-cost",
            "permit 198.51.102.0 0.0.0.255 198.51.103.0 0.0.0.255 precedence 10 tos normal",
            "permit 433 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 eq telnet log check tos max-throughput",
            "permit 198.51.105.0 0.0.0.255 198.51.106.0 0.0.0.255 time-range 20 tos max-throughput",
            "ip access-list standard test_acl",
            "no remark",
            "remark Another remark here",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden_clear(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        self.execute_show_command_name.return_value = dedent("")

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
                                        enable_fragments=True,
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
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list extended 113",
            "deny 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 fragments tos max-reliability",
            "permit 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 log check tos 119",
            "remark extended ACL remark",
            "ip access-list standard 23",
            "remark check remark here",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_delete_acl(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard 2
                30 permit 172.16.1.11
                20 permit 172.16.1.10 log
                10 permit 172.16.1.2
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
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
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )

        result = self.execute_module(changed=True)
        commands = ["no ip access-list standard 2"]
        self.assertEqual(result["commands"], commands)

    def test_ios_failed_extra_param_standard_acl(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
            ip access-list standard test_acl
                remark remark check 1
                remark some random remark 2
            """,
        )
        self.execute_show_command_name.return_value = dedent("")

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
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertEqual(result, {"failed": True})

    def test_ios_failed_update_with_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test_acl
                30 permit 172.16.1.11
                20 permit 172.16.1.10 log
                10 permit 172.16.1.2
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
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
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )

        result = self.execute_module(failed=True)
        self.assertEqual(
            result,
            {
                "msg": "Cannot update existing sequence 10 of ACLs test_acl with state merged. Please use state replaced or overridden.",
                "failed": True,
            },
        )

    def test_ios_acls_parsed_multioption(self):
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    ip access-list standard 99
                        10 remark standalone remarks
                        20 permit 192.15.0.1
                        30 permit 192.15.0.2
                        40 permit 192.15.0.3
                    ip access-list standard 2
                        30 permit 172.16.1.11
                        20 permit 172.16.1.10
                        10 permit 172.16.1.2
                    ip access-list extended 101
                        15 permit tcp any host 172.16.2.9
                        18 permit tcp any host 172.16.2.11
                        20 permit udp host 172.16.1.21 any
                        30 permit udp host 172.16.1.22 any
                        40 deny icmp any 10.1.1.0 0.0.0.255 echo
                        50 permit ip any 10.1.1.0 0.0.0.255
                        60 permit tcp any host 10.1.1.1 eq telnet
                        70 permit tcp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255 eq telnet time-range EVERYOTHERDAY (active)
                    ip access-list extended outboundfilters
                        10 permit icmp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255
                    ip access-list extended test
                        10 permit ip host 10.2.2.2 host 10.3.3.3
                        20 permit tcp host 10.1.1.1 host 10.5.5.5 eq www
                        30 permit icmp any any
                        40 permit udp host 10.6.6.6 10.10.10.0 0.0.0.255 eq domain
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "afi": "ipv4",
                "acls": [
                    {
                        "name": "101",
                        "acl_type": "extended",
                        "aces": [
                            {
                                "sequence": 15,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {"any": True},
                                "destination": {"host": "172.16.2.9"},
                            },
                            {
                                "sequence": 18,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {"any": True},
                                "destination": {"host": "172.16.2.11"},
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "protocol": "udp",
                                "source": {"host": "172.16.1.21"},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "protocol": "udp",
                                "source": {"host": "172.16.1.22"},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 40,
                                "grant": "deny",
                                "protocol": "icmp",
                                "source": {"any": True},
                                "destination": {
                                    "address": "10.1.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "protocol_options": {"icmp": {"echo": True}},
                            },
                            {
                                "sequence": 50,
                                "grant": "permit",
                                "protocol": "ip",
                                "source": {"any": True},
                                "destination": {
                                    "address": "10.1.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                            {
                                "sequence": 60,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {"any": True},
                                "destination": {
                                    "host": "10.1.1.1",
                                    "port_protocol": {"eq": "telnet"},
                                },
                            },
                            {
                                "sequence": 70,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {
                                    "address": "10.1.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "destination": {
                                    "address": "172.16.1.0",
                                    "port_protocol": {"eq": "telnet"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "time_range": "EVERYOTHERDAY",
                            },
                        ],
                    },
                    {
                        "name": "2",
                        "acl_type": "standard",
                        "aces": [
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "source": {"host": "172.16.1.11"},
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "source": {"host": "172.16.1.10"},
                            },
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "source": {"host": "172.16.1.2"},
                            },
                        ],
                    },
                    {
                        "name": "99",
                        "acl_type": "standard",
                        "aces": [
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "source": {"host": "192.15.0.1"},
                            },
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "source": {"host": "192.15.0.2"},
                            },
                            {
                                "sequence": 40,
                                "grant": "permit",
                                "source": {"host": "192.15.0.3"},
                            },
                            {"sequence": 10, "remarks": ["standalone remarks"]},
                        ],
                    },
                    {
                        "name": "outboundfilters",
                        "acl_type": "extended",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "icmp",
                                "source": {
                                    "address": "10.1.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "destination": {
                                    "address": "172.16.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                    },
                    {
                        "name": "test",
                        "acl_type": "extended",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "ip",
                                "source": {"host": "10.2.2.2"},
                                "destination": {"host": "10.3.3.3"},
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {"host": "10.1.1.1"},
                                "destination": {
                                    "host": "10.5.5.5",
                                    "port_protocol": {"eq": "www"},
                                },
                            },
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "protocol": "icmp",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 40,
                                "grant": "permit",
                                "protocol": "udp",
                                "source": {"host": "10.6.6.6"},
                                "destination": {
                                    "address": "10.10.10.0",
                                    "port_protocol": {"eq": "domain"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_acls_rendered_muiltioption(self):
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {
                                "name": "101",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 15,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {"any": True},
                                        "destination": {"host": "172.16.2.9"},
                                    },
                                    {
                                        "sequence": 18,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {"any": True},
                                        "destination": {"host": "172.16.2.11"},
                                    },
                                    {
                                        "sequence": 20,
                                        "grant": "permit",
                                        "protocol": "udp",
                                        "source": {"host": "172.16.1.21"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 30,
                                        "grant": "permit",
                                        "protocol": "udp",
                                        "source": {"host": "172.16.1.22"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 40,
                                        "grant": "deny",
                                        "protocol": "icmp",
                                        "source": {"any": True},
                                        "destination": {
                                            "address": "10.1.1.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "protocol_options": {"icmp": {"echo": True}},
                                    },
                                    {
                                        "sequence": 50,
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"any": True},
                                        "destination": {
                                            "address": "10.1.1.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                    },
                                    {
                                        "sequence": 60,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {"any": True},
                                        "destination": {
                                            "host": "10.1.1.1",
                                            "port_protocol": {"eq": "telnet"},
                                        },
                                    },
                                    {
                                        "sequence": 70,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {
                                            "address": "10.1.1.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "address": "172.16.1.0",
                                            "port_protocol": {"eq": "telnet"},
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "time_range": "EVERYOTHERDAY",
                                    },
                                ],
                            },
                            {
                                "name": "99",
                                "acl_type": "standard",
                                "aces": [
                                    {
                                        "sequence": 20,
                                        "grant": "permit",
                                        "source": {"host": "192.15.0.1"},
                                    },
                                    {
                                        "sequence": 30,
                                        "grant": "permit",
                                        "source": {"host": "192.15.0.2"},
                                    },
                                    {
                                        "sequence": 40,
                                        "grant": "permit",
                                        "source": {"host": "192.15.0.3"},
                                    },
                                    {"sequence": 10, "remarks": ["standalone remarks"]},
                                ],
                            },
                            {
                                "name": "2",
                                "acl_type": "standard",
                                "aces": [
                                    {
                                        "sequence": 30,
                                        "grant": "permit",
                                        "source": {"host": "172.16.1.11"},
                                    },
                                    {
                                        "sequence": 20,
                                        "grant": "permit",
                                        "source": {"host": "172.16.1.10"},
                                    },
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "source": {"host": "172.16.1.2"},
                                    },
                                ],
                            },
                            {
                                "name": "outboundfilters",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "protocol": "icmp",
                                        "source": {
                                            "address": "10.1.1.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                        "destination": {
                                            "address": "172.16.1.0",
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                    },
                                ],
                            },
                            {
                                "name": "test",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"host": "10.2.2.2"},
                                        "destination": {"host": "10.3.3.3"},
                                    },
                                    {
                                        "sequence": 20,
                                        "grant": "permit",
                                        "protocol": "tcp",
                                        "source": {"host": "10.1.1.1"},
                                        "destination": {
                                            "host": "10.5.5.5",
                                            "port_protocol": {"eq": "www"},
                                        },
                                    },
                                    {
                                        "sequence": 30,
                                        "grant": "permit",
                                        "protocol": "icmp",
                                        "source": {"any": True},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 40,
                                        "grant": "permit",
                                        "protocol": "udp",
                                        "source": {"host": "10.6.6.6"},
                                        "destination": {
                                            "address": "10.10.10.0",
                                            "port_protocol": {"eq": "domain"},
                                            "wildcard_bits": "0.0.0.255",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "ip access-list extended 101",
            "15 permit tcp any host 172.16.2.9",
            "18 permit tcp any host 172.16.2.11",
            "20 permit udp host 172.16.1.21 any",
            "30 permit udp host 172.16.1.22 any",
            "40 deny icmp any 10.1.1.0 0.0.0.255 echo",
            "50 permit ip any 10.1.1.0 0.0.0.255",
            "60 permit tcp any host 10.1.1.1 eq telnet",
            "70 permit tcp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255 eq telnet time-range EVERYOTHERDAY",
            "ip access-list standard 99",
            "20 permit host 192.15.0.1",
            "30 permit host 192.15.0.2",
            "40 permit host 192.15.0.3",
            "10 remark standalone remarks",
            "ip access-list standard 2",
            "30 permit host 172.16.1.11",
            "20 permit host 172.16.1.10",
            "10 permit host 172.16.1.2",
            "ip access-list extended outboundfilters",
            "10 permit icmp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255",
            "ip access-list extended test",
            "10 permit ip host 10.2.2.2 host 10.3.3.3",
            "20 permit tcp host 10.1.1.1 host 10.5.5.5 eq www",
            "30 permit icmp any any",
            "40 permit udp host 10.6.6.6 10.10.10.0 0.0.0.255 eq domain",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_acls_overridden_sticky_remarks(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list standard test123
             10 remark TEST
             10 permit 8.8.8.8
             20 remark TEST
             20 permit 8.8.4.4
            """,
        )
        self.execute_show_command_name.return_value = dedent("")

        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="test123",
                                acl_type="standard",
                                aces=[
                                    dict(
                                        grant="permit",
                                        source=dict(
                                            address="8.8.128.0",
                                            wildcard_bits="0.0.0.63",
                                        ),
                                        remarks=["TEST", "TEST 2"],
                                        sequence=10,
                                    ),
                                    dict(
                                        grant="permit",
                                        source=dict(
                                            host="8.8.4.4",
                                        ),
                                        remarks=["TEST"],
                                        sequence=20,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "ip access-list standard test123",
            "no 10 remark",
            "no 10 permit host 8.8.8.8",
            "10 remark TEST",
            "10 remark TEST 2",
            "10 permit 8.8.128.0 0.0.0.63",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_acls_overridden_remarks_complex(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list extended TEST
             10 remark FIRST REMARK BEFORE SEQUENCE 10
             10 remark ============
             10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
             20 remark FIRST REMARK BEFORE SEQUENCE 20
             20 remark ============
             20 remark ALLOW HOST FROM SEQUENCE 20
             20 permit ip host 1.1.1.1 any
             30 remark FIRST REMARK BEFORE SEQUENCE 30
             30 remark ============
             30 remark ALLOW HOST FROM SEQUENCE 30
             30 permit ip host 2.2.2.2 any
             40 remark FIRST REMARK BEFORE SEQUENCE 40
             40 remark ============
             40 remark ALLOW NEW HOST FROM SEQUENCE 40
             40 permit ip host 3.3.3.3 any
             remark Remark not specific to sequence
             remark ============
             remark End Remarks
            ip access-list extended test_acl
             10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
            ip access-list extended 110
             10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
            ip access-list extended 123
             10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
             20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
            ipv6 access-list R1_TRAFFIC
             sequence 10 deny tcp any eq www any eq telnet ack dscp af11
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv4",
                        "acls": [
                            {
                                "name": "TEST",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "sequence": 10,
                                        "remarks": [
                                            "FIRST REMARK BEFORE SEQUENCE 10",
                                            "============",
                                            "REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE",
                                        ],
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"host": "1.1.1.1"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 20,
                                        "remarks": [
                                            "FIRST REMARK BEFORE SEQUENCE 20",
                                            "============",
                                            "ALLOW HOST FROM SEQUENCE 20",
                                        ],
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"host": "192.168.0.1"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 30,
                                        "remarks": [
                                            "FIRST REMARK BEFORE SEQUENCE 30",
                                            "============",
                                            "ALLOW HOST FROM SEQUENCE 30 updated",
                                        ],
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"host": "2.2.2.2"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "sequence": 40,
                                        "remarks": [
                                            "FIRST REMARK BEFORE SEQUENCE 40",
                                            "============",
                                            "ALLOW NEW HOST FROM SEQUENCE 40",
                                        ],
                                        "grant": "permit",
                                        "protocol": "ip",
                                        "source": {"host": "3.3.3.3"},
                                        "destination": {"any": True},
                                    },
                                    {
                                        "remarks": [
                                            "Remark not specific to sequence",
                                            "============",
                                            "End Remarks 1",
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no ipv6 access-list R1_TRAFFIC",
            "ip access-list extended TEST",
            "no 10",  # removes all remarks and ace entry for sequence 10
            "no 20 permit ip host 1.1.1.1 any",  # removing the ace automatically removes the remarks
            "no 30 remark",  # just remove remarks for sequence 30
            "no remark",  # remove all remarks at end of acl, that has no sequence
            "10 remark FIRST REMARK BEFORE SEQUENCE 10",
            "10 remark ============",
            "10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE",
            "10 permit ip host 1.1.1.1 any",
            "20 remark FIRST REMARK BEFORE SEQUENCE 20",
            "20 remark ============",
            "20 remark ALLOW HOST FROM SEQUENCE 20",
            "20 permit ip host 192.168.0.1 any",
            "30 remark FIRST REMARK BEFORE SEQUENCE 30",
            "30 remark ============",
            "30 remark ALLOW HOST FROM SEQUENCE 30 updated",
            "remark Remark not specific to sequence",
            "remark ============",
            "remark End Remarks 1",
            "no ip access-list extended 110",
            "no ip access-list extended 123",
            "no ip access-list extended test_acl",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_merged_general(self):
        self.execute_show_command.return_value = dedent(
            """\
            ipv6 access-list extended std_acl_name_test_1
                10 remark std_acl_name_test_1
                20 permit 220 any any
            """,
        )
        self.execute_show_command_name.return_value = dedent("")
        set_module_args(
            dict(
                config=[
                    {
                        "afi": "ipv6",
                        "acls": [
                            {
                                "name": "std_acl_name_test_1",
                                "acl_type": "extended",
                                "aces": [
                                    {
                                        "remarks": [
                                            "Test_ipv4_ipv6_acl",
                                        ],
                                    },
                                    {
                                        "destination": {
                                            "any": True,
                                        },
                                        "grant": "permit",
                                        "protocol": 220,
                                        "sequence": 40,
                                        "source": {
                                            "any": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )

        result = self.execute_module(changed=True)
        commands = [
            "ipv6 access-list std_acl_name_test_1",
            "permit 220 any any sequence 40",
            "remark Test_ipv4_ipv6_acl",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))
