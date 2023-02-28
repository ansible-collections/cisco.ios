# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.cisco.ios.plugins.plugin_utils.pop_ace import pop_ace


class TestAcePopper(unittest.TestCase):
    def setUp(self):
        pass

    def test_pop_ace_plugin(self):
        filter_options = {"match_all": True}
        match_criteria = {
            "afi": "ipv4",
            "source_address": "192.0.2.0",
            "destination_address": "192.0.3.0",
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
