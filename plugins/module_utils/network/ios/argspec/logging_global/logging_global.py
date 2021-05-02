# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the ios_logging_global module
"""


class Logging_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_logging_global module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "buffered": {
                    "type": "dict",
                    "options": {
                        "size": {"type": "int"},
                        "severity": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                            ],
                        },
                        "discriminator": {"type": "str"},
                        "filtered": {"type": "bool"},
                        "xml": {"type": "bool"},
                    },
                },
                "buginf": {"type": "bool"},
                "cns_events": {
                    "type": "str",
                    "choices": [
                        "alerts",
                        "critical",
                        "debugging",
                        "emergencies",
                        "errors",
                        "informational",
                        "notifications",
                        "warnings",
                    ],
                },
                "console": {
                    "type": "dict",
                    "options": {
                        "severity": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                                "guaranteed",
                            ],
                        },
                        "discriminator": {"type": "str"},
                        "filtered": {"type": "bool"},
                        "xml": {"type": "bool"},
                    },
                },
                "count": {"type": "bool"},
                "delimiter": {
                    "type": "dict",
                    "options": {"tcp": {"type": "bool"}},
                },
                "discriminator": {
                    "type": "list",
                    "elements": "str",
                },
                "dmvpn": {
                    "type": "dict",
                    "options": {"rate_limit": {"type": "int"}},
                },
                "esm": {"type": "dict", "options": {"config": {"type": "bool"}}},
                "exception": {"type": "int"},
                "facility": {
                    "type": "str",
                    "choices": [
                        "auth",
                        "cron",
                        "daemon",
                        "kern",
                        "local0",
                        "local1",
                        "local2",
                        "local3",
                        "local4",
                        "local5",
                        "local6",
                        "local7",
                        "lpr",
                        "mail",
                        "news",
                        "sys10",
                        "sys11",
                        "sys12",
                        "sys13",
                        "sys14",
                        "sys9",
                        "syslog",
                        "user",
                        "uucp",
                    ],
                },
                "filter": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "url": {"type": "str"},
                        "order": {"type": "int"},
                        "args": {"type": "str"},
                    },
                },
                "history": {
                    "type": "dict",
                    "options": {
                        "size": {"type": "int"},
                        "severity": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                            ],
                        },
                    },
                },
                "hosts": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "discriminator": {"type": "str"},
                        "filtered": {"type": "bool"},
                        "sequence_num_session": {"type": "bool"},
                        "session_id": {
                            "type": "dict",
                            "options": {
                                "tag": {
                                    "type": "str",
                                    "choices": ["hostname", "ipv4", "ipv6"],
                                },
                                "text": {"type": "str"},
                            },
                        },
                        "transport": {
                            "type": "dict",
                            "options": {
                                "tcp": {
                                    "type": "dict",
                                    "options": {
                                        "audit": {"type": "bool"},
                                        "discriminator": {"type": "str"},
                                        "filtered": {"type": "bool"},
                                        "stream": {"type": "int"},
                                        "port": {"type": "int"},
                                        "sequence_num_session": {"type": "bool"},
                                        "session_id": {
                                            "type": "dict",
                                            "options": {
                                                "tag": {
                                                    "type": "str",
                                                    "choices": [
                                                        "hostname",
                                                        "ipv4",
                                                        "ipv6",
                                                    ],
                                                },
                                                "text": {"type": "str"},
                                            },
                                        },
                                        "xml": {"type": "bool"},
                                    },
                                },
                                "udp": {
                                    "type": "dict",
                                    "options": {
                                        "discriminator": {"type": "str"},
                                        "filtered": {"type": "bool"},
                                        "stream": {"type": "int"},
                                        "port": {"type": "int"},
                                        "sequence_num_session": {"type": "bool"},
                                        "session_id": {
                                            "type": "dict",
                                            "options": {
                                                "tag": {
                                                    "type": "str",
                                                    "choices": [
                                                        "hostname",
                                                        "ipv4",
                                                        "ipv6",
                                                    ],
                                                },
                                                "text": {"type": "str"},
                                            },
                                        },
                                        "xml": {"type": "bool"},
                                    },
                                },
                            },
                        },
                        "vrf": {"type": "str"},
                        "xml": {"type": "bool"},
                        "stream": {"type": "int"},
                        "ipv6": {"type": "str"},
                        "hostname": {"type": "str"},
                    },
                },
                "message_counter": {
                    "type": "list",
                    "elements": "str",
                    "choices": ["log", "debug", "syslog"],
                },
                "monitor": {
                    "type": "dict",
                    "options": {
                        "severity": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                            ],
                        },
                        "discriminator": {"type": "str"},
                        "filtered": {"type": "bool"},
                        "xml": {"type": "bool"},
                    },
                },
                "logging_on": {
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "origin_id": {
                    "type": "dict",
                    "options": {
                        "tag": {
                            "type": "str",
                            "choices": ["hostname", "ip", "ipv6"],
                        },
                        "text": {"type": "str"},
                    },
                },
                "persistent": {
                    "type": "dict",
                    "options": {
                        "batch": {"type": "int"},
                        "filesize": {"type": "int"},
                        "immediate": {"type": "bool"},
                        "notify": {"type": "bool"},
                        "protected": {"type": "bool"},
                        "size": {"type": "int"},
                        "threshold": {"type": "int"},
                        "url": {"type": "str"},
                    },
                },
                "policy_firewall": {
                    "type": "dict",
                    "options": {"rate_limit": {"type": "int"}},
                },
                "queue_limit": {
                    "type": "dict",
                    "options": {
                        "size": {"type": "int"},
                        "esm": {"type": "int"},
                        "trap": {"type": "int"},
                    },
                },
                "rate_limit": {
                    "type": "dict",
                    "options": {
                        "size": {"type": "int", "required": True},
                        "all": {"type": "bool"},
                        "console": {"type": "bool"},
                        "except": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                            ],
                        },
                    },
                },
                "reload": {
                    "type": "dict",
                    "options": {
                        "severity": {
                            "type": "str",
                            "choices": [
                                "alerts",
                                "critical",
                                "debugging",
                                "emergencies",
                                "errors",
                                "informational",
                                "notifications",
                                "warnings",
                            ],
                        },
                        "message_limit": {"type": "int"},
                    },
                },
                "server_arp": {"type": "bool"},
                "snmp_trap": {
                    "type": "list",
                    "elements": "str",
                    "choices": [
                        "alerts",
                        "critical",
                        "debugging",
                        "emergencies",
                        "errors",
                        "informational",
                        "notifications",
                        "warnings",
                    ],
                },
                "source_interface": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "interface": {"type": "str"},
                        "vrf": {"type": "str"},
                    },
                },
                "trap": {
                    "type": "str",
                    "choices": [
                        "alerts",
                        "critical",
                        "debugging",
                        "emergencies",
                        "errors",
                        "informational",
                        "notifications",
                        "warnings",
                    ],
                },
                "userinfo": {"type": "bool"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "parsed",
                "rendered",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
