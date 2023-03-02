# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.cisco.ios.plugins.plugin_utils.pop_ace import pop_ace


class TestPopAce(unittest.TestCase):
    def setUp(self):
        pass

    def test_pop_ace_plugin(self):
        filter_options = {"match_all": True}
        match_criteria = {
            "afi": "ipv4",
            "source": "192.0.2.0",
            "destination": "192.0.3.0",
        }
        data = [
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "192.0.3.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "dscp": "ef",
                                "grant": "deny",
                                "protocol": "icmp",
                                "protocol_options": {"icmp": {"traceroute": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "192.0.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"eq": 10},
                            },
                            {
                                "destination": {
                                    "host": "198.51.110.0",
                                    "port_protocol": {"eq": "telnet"},
                                },
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 20,
                                "source": {"host": "198.51.100.0"},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "110",
                    },
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "198.51.101.0",
                                    "port_protocol": {"eq": "telnet"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "198.51.100.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "tos": {"service_value": 12},
                            },
                            {
                                "destination": {
                                    "address": "192.0.4.0",
                                    "port_protocol": {"eq": "www"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "dscp": "ef",
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 20,
                                "source": {
                                    "address": "192.0.3.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"lt": 20},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "123",
                    },
                    {
                        "aces": [
                            {
                                "grant": "deny",
                                "sequence": 10,
                                "source": {"host": "192.168.1.200"},
                            },
                            {
                                "grant": "deny",
                                "sequence": 20,
                                "source": {
                                    "address": "192.168.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                        "acl_type": "standard",
                        "name": "std_acl",
                    },
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "192.0.3.0",
                                    "port_protocol": {"eq": "www"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "deny",
                                "option": {"traceroute": True},
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"fin": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "192.0.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"eq": 10},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "test",
                    },
                ],
                "afi": "ipv4",
            },
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
                                "source": {"any": True, "port_protocol": {"eq": "www"}},
                            },
                        ],
                        "name": "R1_TRAFFIC",
                    },
                ],
                "afi": "ipv6",
            },
        ]
        args = [data, filter_options, match_criteria]
        clean_acls = {
            "acls": [
                {
                    "acls": [
                        {
                            "name": "110",
                            "aces": [
                                {
                                    "destination": {
                                        "host": "198.51.110.0",
                                        "port_protocol": {"eq": "telnet"},
                                    },
                                    "grant": "deny",
                                    "protocol": "tcp",
                                    "protocol_options": {"tcp": {"ack": True}},
                                    "sequence": 20,
                                    "source": {"host": "198.51.100.0"},
                                },
                            ],
                        },
                        {
                            "name": "123",
                            "aces": [
                                {
                                    "destination": {
                                        "address": "198.51.101.0",
                                        "port_protocol": {"eq": "telnet"},
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "grant": "deny",
                                    "protocol": "tcp",
                                    "protocol_options": {"tcp": {"ack": True}},
                                    "sequence": 10,
                                    "source": {
                                        "address": "198.51.100.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "tos": {"service_value": 12},
                                },
                                {
                                    "destination": {
                                        "address": "192.0.4.0",
                                        "port_protocol": {"eq": "www"},
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "dscp": "ef",
                                    "grant": "deny",
                                    "protocol": "tcp",
                                    "protocol_options": {"tcp": {"ack": True}},
                                    "sequence": 20,
                                    "source": {
                                        "address": "192.0.3.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "ttl": {"lt": 20},
                                },
                            ],
                        },
                        {
                            "name": "std_acl",
                            "aces": [
                                {
                                    "grant": "deny",
                                    "sequence": 10,
                                    "source": {"host": "192.168.1.200"},
                                },
                                {
                                    "grant": "deny",
                                    "sequence": 20,
                                    "source": {
                                        "address": "192.168.2.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                },
                            ],
                        },
                    ],
                    "afi": "ipv4",
                },
                {
                    "acls": [
                        {
                            "name": "R1_TRAFFIC",
                            "aces": [
                                {
                                    "destination": {"any": True, "port_protocol": {"eq": "telnet"}},
                                    "dscp": "af11",
                                    "grant": "deny",
                                    "protocol": "tcp",
                                    "protocol_options": {"tcp": {"ack": True}},
                                    "sequence": 10,
                                    "source": {"any": True, "port_protocol": {"eq": "www"}},
                                },
                            ],
                        },
                    ],
                    "afi": "ipv6",
                },
            ],
        }
        removed_aces = {
            "acls": [
                {
                    "acls": [
                        {
                            "name": "110",
                            "aces": [
                                {
                                    "destination": {
                                        "address": "192.0.3.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "dscp": "ef",
                                    "grant": "deny",
                                    "protocol": "icmp",
                                    "protocol_options": {"icmp": {"traceroute": True}},
                                    "sequence": 10,
                                    "source": {
                                        "address": "192.0.2.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "ttl": {"eq": 10},
                                },
                            ],
                        },
                        {
                            "name": "test",
                            "aces": [
                                {
                                    "destination": {
                                        "address": "192.0.3.0",
                                        "port_protocol": {"eq": "www"},
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "grant": "deny",
                                    "option": {"traceroute": True},
                                    "protocol": "tcp",
                                    "protocol_options": {"tcp": {"fin": True}},
                                    "sequence": 10,
                                    "source": {
                                        "address": "192.0.2.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "ttl": {"eq": 10},
                                },
                            ],
                        },
                    ],
                    "afi": "ipv4",
                },
                {"acls": [], "afi": "ipv6"},
            ],
        }
        result = pop_ace(*args)
        print(result)
        self.assertEqual(result.get("removed_aces"), removed_aces)
        self.assertEqual(result.get("clean_acls"), clean_acls)

    def test_pop_ace_plugin_remove_first(self):
        filter_options = {"match_all": True, "remove": "first"}
        match_criteria = {
            "afi": "ipv4",
            # "source": "192.0.2.0",
            "destination": "any",
            "grant": "permit",
        }
        data = [
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "grant": "permit",
                                "protocol": "tcp",
                                "sequence": 15,
                                "source": {"any": True, "host": "172.16.2.9"},
                            },
                            {
                                "grant": "permit",
                                "protocol": "tcp",
                                "sequence": 18,
                                "source": {"any": True, "host": "172.16.2.11"},
                            },
                            {
                                "destination": {"any": True},
                                "grant": "permit",
                                "protocol": "udp",
                                "sequence": 20,
                                "source": {"host": "172.16.1.21"},
                            },
                            {
                                "destination": {"any": True},
                                "grant": "permit",
                                "protocol": "udp",
                                "sequence": 30,
                                "source": {"host": "172.16.1.22"},
                            },
                            {
                                "grant": "deny",
                                "protocol": "icmp",
                                "protocol_options": {"icmp": {"echo": True}},
                                "sequence": 40,
                                "source": {
                                    "address": "10.1.1.0",
                                    "any": True,
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                            {
                                "grant": "permit",
                                "protocol": "ip",
                                "sequence": 50,
                                "source": {
                                    "address": "10.1.1.0",
                                    "any": True,
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                            {
                                "grant": "permit",
                                "protocol": "tcp",
                                "sequence": 60,
                                "source": {
                                    "any": True,
                                    "host": "10.1.1.1",
                                    "port_protocol": {"eq": "telnet"},
                                },
                            },
                            {
                                "destination": {
                                    "address": "172.16.1.0",
                                    "port_protocol": {"eq": "telnet"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "permit",
                                "protocol": "tcp",
                                "sequence": 70,
                                "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
                                "time_range": "EVERYOTHERDAY",
                            },
                        ],
                        "acl_type": "extended",
                        "name": "101",
                    },
                    {
                        "aces": [
                            {"grant": "permit", "sequence": 30, "source": {"host": "172.16.1.11"}},
                            {"grant": "permit", "sequence": 20, "source": {"host": "172.16.1.10"}},
                            {"grant": "permit", "sequence": 10, "source": {"host": "172.16.1.2"}},
                        ],
                        "acl_type": "standard",
                        "name": "2",
                    },
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "172.16.1.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "permit",
                                "protocol": "icmp",
                                "sequence": 10,
                                "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "outboundfilters",
                    },
                    {
                        "aces": [
                            {
                                "destination": {"host": "10.3.3.3"},
                                "grant": "permit",
                                "protocol": "ip",
                                "sequence": 10,
                                "source": {"host": "10.2.2.2"},
                            },
                            {
                                "destination": {"host": "10.5.5.5", "port_protocol": {"eq": "www"}},
                                "grant": "permit",
                                "protocol": "tcp",
                                "sequence": 20,
                                "source": {"host": "10.1.1.1"},
                            },
                            {
                                "destination": {"any": True},
                                "grant": "permit",
                                "protocol": "icmp",
                                "sequence": 30,
                                "source": {"any": True},
                            },
                            {
                                "grant": "permit",
                                "protocol": "udp",
                                "sequence": 40,
                                "source": {
                                    "address": "10.10.10.0",
                                    "host": "10.6.6.6",
                                    "port_protocol": {"eq": "domain"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                        "acl_type": "extended",
                        "name": "test",
                    },
                ],
                "afi": "ipv4",
            },
        ]
        args = [data, filter_options, match_criteria]
        clean_acls = {
            "acls": [
                {
                    "acls": [
                        {
                            "name": "101",
                            "aces": [
                                {
                                    "grant": "permit",
                                    "protocol": "tcp",
                                    "sequence": 15,
                                    "source": {"any": True, "host": "172.16.2.9"},
                                },
                                {
                                    "grant": "permit",
                                    "protocol": "tcp",
                                    "sequence": 18,
                                    "source": {"any": True, "host": "172.16.2.11"},
                                },
                                {
                                    "destination": {"any": True},
                                    "grant": "permit",
                                    "protocol": "udp",
                                    "sequence": 30,
                                    "source": {"host": "172.16.1.22"},
                                },
                                {
                                    "grant": "deny",
                                    "protocol": "icmp",
                                    "protocol_options": {"icmp": {"echo": True}},
                                    "sequence": 40,
                                    "source": {
                                        "address": "10.1.1.0",
                                        "any": True,
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                },
                                {
                                    "grant": "permit",
                                    "protocol": "ip",
                                    "sequence": 50,
                                    "source": {
                                        "address": "10.1.1.0",
                                        "any": True,
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                },
                                {
                                    "grant": "permit",
                                    "protocol": "tcp",
                                    "sequence": 60,
                                    "source": {
                                        "any": True,
                                        "host": "10.1.1.1",
                                        "port_protocol": {"eq": "telnet"},
                                    },
                                },
                                {
                                    "destination": {
                                        "address": "172.16.1.0",
                                        "port_protocol": {"eq": "telnet"},
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "grant": "permit",
                                    "protocol": "tcp",
                                    "sequence": 70,
                                    "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
                                    "time_range": "EVERYOTHERDAY",
                                },
                            ],
                        },
                        {
                            "name": "2",
                            "aces": [
                                {
                                    "grant": "permit",
                                    "sequence": 30,
                                    "source": {"host": "172.16.1.11"},
                                },
                                {
                                    "grant": "permit",
                                    "sequence": 20,
                                    "source": {"host": "172.16.1.10"},
                                },
                                {
                                    "grant": "permit",
                                    "sequence": 10,
                                    "source": {"host": "172.16.1.2"},
                                },
                            ],
                        },
                        {
                            "name": "outboundfilters",
                            "aces": [
                                {
                                    "destination": {
                                        "address": "172.16.1.0",
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                    "grant": "permit",
                                    "protocol": "icmp",
                                    "sequence": 10,
                                    "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
                                },
                            ],
                        },
                        {
                            "name": "test",
                            "aces": [
                                {
                                    "destination": {"host": "10.3.3.3"},
                                    "grant": "permit",
                                    "protocol": "ip",
                                    "sequence": 10,
                                    "source": {"host": "10.2.2.2"},
                                },
                                {
                                    "destination": {
                                        "host": "10.5.5.5",
                                        "port_protocol": {"eq": "www"},
                                    },
                                    "grant": "permit",
                                    "protocol": "tcp",
                                    "sequence": 20,
                                    "source": {"host": "10.1.1.1"},
                                },
                                {
                                    "grant": "permit",
                                    "protocol": "udp",
                                    "sequence": 40,
                                    "source": {
                                        "address": "10.10.10.0",
                                        "host": "10.6.6.6",
                                        "port_protocol": {"eq": "domain"},
                                        "wildcard_bits": "0.0.0.255",
                                    },
                                },
                            ],
                        },
                    ],
                    "afi": "ipv4",
                },
                {"acls": [], "afi": "ipv6"},
            ],
        }
        removed_aces = {
            "acls": [
                {
                    "acls": [
                        {
                            "name": "101",
                            "aces": [
                                {
                                    "destination": {"any": True},
                                    "grant": "permit",
                                    "protocol": "udp",
                                    "sequence": 20,
                                    "source": {"host": "172.16.1.21"},
                                },
                            ],
                        },
                        {
                            "name": "test",
                            "aces": [
                                {
                                    "destination": {"any": True},
                                    "grant": "permit",
                                    "protocol": "icmp",
                                    "sequence": 30,
                                    "source": {"any": True},
                                },
                            ],
                        },
                    ],
                    "afi": "ipv4",
                },
                {"acls": [], "afi": "ipv6"},
            ],
        }
        result = pop_ace(*args)
        self.assertEqual(result.get("removed_aces"), removed_aces)
        self.assertEqual(result.get("clean_acls"), clean_acls)

    def test_pop_ace_plugin_fail_no_match(self):
        filter_options = {"match_all": True, "failed_when": "missing"}
        match_criteria = {
            "afi": "ipv4",
            "source": "0.0.2.0",
            "destination": "0.0.3.0",
        }
        data = [
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "192.0.3.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "dscp": "ef",
                                "grant": "deny",
                                "protocol": "icmp",
                                "protocol_options": {"icmp": {"traceroute": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "192.0.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"eq": 10},
                            },
                            {
                                "destination": {
                                    "host": "198.51.110.0",
                                    "port_protocol": {"eq": "telnet"},
                                },
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 20,
                                "source": {"host": "198.51.100.0"},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "110",
                    },
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "198.51.101.0",
                                    "port_protocol": {"eq": "telnet"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "198.51.100.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "tos": {"service_value": 12},
                            },
                            {
                                "destination": {
                                    "address": "192.0.4.0",
                                    "port_protocol": {"eq": "www"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "dscp": "ef",
                                "grant": "deny",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"ack": True}},
                                "sequence": 20,
                                "source": {
                                    "address": "192.0.3.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"lt": 20},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "123",
                    },
                    {
                        "aces": [
                            {
                                "grant": "deny",
                                "sequence": 10,
                                "source": {"host": "192.168.1.200"},
                            },
                            {
                                "grant": "deny",
                                "sequence": 20,
                                "source": {
                                    "address": "192.168.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                            },
                        ],
                        "acl_type": "standard",
                        "name": "std_acl",
                    },
                    {
                        "aces": [
                            {
                                "destination": {
                                    "address": "192.0.3.0",
                                    "port_protocol": {"eq": "www"},
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "grant": "deny",
                                "option": {"traceroute": True},
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"fin": True}},
                                "sequence": 10,
                                "source": {
                                    "address": "192.0.2.0",
                                    "wildcard_bits": "0.0.0.255",
                                },
                                "ttl": {"eq": 10},
                            },
                        ],
                        "acl_type": "extended",
                        "name": "test",
                    },
                ],
                "afi": "ipv4",
            },
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
                                "source": {"any": True, "port_protocol": {"eq": "www"}},
                            },
                        ],
                        "name": "R1_TRAFFIC",
                    },
                ],
                "afi": "ipv6",
            },
        ]
        args = [data, filter_options, match_criteria]
        with self.assertRaises(AnsibleFilterError) as error:
            pop_ace(*args)
        self.assertIn(
            "Error when using plugin 'pop_ace': no entries removed on the provided match_criteria",
            str(error.exception),
        )
