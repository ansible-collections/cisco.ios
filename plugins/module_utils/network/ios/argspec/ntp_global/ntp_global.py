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
The arg spec for the ios_ntp_global module
"""


class Ntp_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_ntp_global module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "access_group": {
                    "type": "dict",
                    "options": {
                        "peer": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "access_list": {"type": "str"},
                                "kod": {"type": "bool"},
                                "ipv4": {"type": "bool"},
                                "ipv6": {"type": "bool"},
                            },
                        },
                        "query_only": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "access_list": {"type": "str"},
                                "kod": {"type": "bool"},
                                "ipv4": {"type": "bool"},
                                "ipv6": {"type": "bool"},
                            },
                        },
                        "serve": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "access_list": {"type": "str"},
                                "kod": {"type": "bool"},
                                "ipv4": {"type": "bool"},
                                "ipv6": {"type": "bool"},
                            },
                        },
                        "serve_only": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "access_list": {"type": "str"},
                                "kod": {"type": "bool"},
                                "ipv4": {"type": "bool"},
                                "ipv6": {"type": "bool"},
                            },
                        },
                    },
                },
                "allow": {
                    "type": "dict",
                    "options": {
                        "control": {
                            "type": "dict",
                            "options": {"rate_limit": {"type": "int"}},
                        },
                        "private": {"type": "bool"},
                    },
                },
                "authenticate": {"type": "bool"},
                "authentication_keys": {
                    "type": "list",
                    "elements": "dict",
                    "no_log": False,
                    "options": {
                        "id": {"type": "int"},
                        "algorithm": {"type": "str"},
                        "key": {"type": "str", "no_log": True},
                        "encryption": {"type": "int"},
                    },
                },
                "broadcast_delay": {"type": "int"},
                "clock_period": {"type": "int"},
                "logging": {"type": "bool"},
                "master": {
                    "type": "dict",
                    "options": {
                        "enabled": {"type": "bool"},
                        "stratum_number": {"type": "int"},
                    },
                },
                "max_associations": {"type": "int"},
                "max_distance": {"type": "int"},
                "min_distance": {"type": "int"},
                "orphan": {"type": "int"},
                "panic_update": {"type": "bool"},
                "passive": {"type": "bool"},
                "peers": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "peer": {"type": "str"},
                        "use_ipv4": {"type": "bool"},
                        "use_ipv6": {"type": "bool"},
                        "vrf": {"type": "str"},
                        "burst": {"type": "bool"},
                        "iburst": {"type": "bool"},
                        "key": {"type": "int", "no_log": True},
                        "maxpoll": {"type": "int"},
                        "minpoll": {"type": "int"},
                        "normal_sync": {"type": "bool"},
                        "prefer": {"type": "bool"},
                        "source": {"type": "str"},
                        "version": {"type": "int"},
                    },
                },
                "servers": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "server": {"type": "str"},
                        "use_ipv4": {"type": "bool"},
                        "use_ipv6": {"type": "bool"},
                        "vrf": {"type": "str"},
                        "burst": {"type": "bool"},
                        "iburst": {"type": "bool"},
                        "key": {"type": "int", "no_log": True},
                        "maxpoll": {"type": "int"},
                        "minpoll": {"type": "int"},
                        "normal_sync": {"type": "bool"},
                        "prefer": {"type": "bool"},
                        "source": {"type": "str"},
                        "version": {"type": "int"},
                    },
                },
                "source": {"type": "str"},
                "trusted_keys": {
                    "type": "list",
                    "elements": "dict",
                    "no_log": False,
                    "options": {
                        "range_start": {"type": "int"},
                        "range_end": {"type": "int"},
                    },
                },
                "update_calendar": {"type": "bool"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
