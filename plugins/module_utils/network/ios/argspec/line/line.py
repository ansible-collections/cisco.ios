# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.content_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the documentation in the module file and re-run
# ansible.content_builder commenting out
# the path to external 'docstring' in build.yaml.
#
##############################################

"""
The arg spec for the ios_line module
"""


class LineArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_line module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "lines": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "access_classes_in": {"type": "str"},
                        "access_classes_out": {"type": "str"},
                        "accounting": {
                            "type": "dict",
                            "options": {
                                "arap": {"type": "str", "default": "default"},
                                "commands": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "level": {"type": "int"},
                                        "command": {
                                            "type": "str",
                                            "default": "default",
                                        },
                                    },
                                },
                                "connection": {
                                    "type": "str",
                                    "default": "default",
                                },
                                "exec": {"type": "str", "default": "default"},
                                "resource": {"type": "str", "default": "default"},
                            },
                        },
                        "authorization": {
                            "type": "dict",
                            "options": {
                                "arap": {"type": "str", "default": "default"},
                                "commands": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "level": {"type": "int"},
                                        "command": {
                                            "type": "str",
                                            "default": "default",
                                        },
                                    },
                                },
                                "exec": {"type": "str", "default": "default"},
                                "reverse_access": {
                                    "type": "str",
                                    "default": "default",
                                },
                            },
                        },
                        "escape_character": {
                            "type": "dict",
                            "options": {
                                "soft": {"type": "bool"},
                                "value": {"type": "str"},
                            },
                        },
                        "exec": {
                            "type": "dict",
                            "options": {
                                "banner": {"type": "bool"},
                                "character_bits": {
                                    "type": "int",
                                    "choices": [7, 8],
                                },
                                "prompt": {
                                    "type": "dict",
                                    "options": {
                                        "expand": {"type": "bool"},
                                        "timestamp": {"type": "bool"},
                                    },
                                },
                                "timeout": {"type": "int"},
                            },
                        },
                        "length": {"type": "int"},
                        "location": {"type": "str"},
                        "logging": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "level": {
                                    "type": "str",
                                    "choices": [
                                        "0",
                                        "1",
                                        "2",
                                        "3",
                                        "4",
                                        "5",
                                        "6",
                                        "7",
                                        "all",
                                    ],
                                },
                                "limit": {"type": "int"},
                            },
                        },
                        "login": {"type": "str", "default": "default"},
                        "logout_warning": {"type": "int"},
                        "motd": {"type": "bool", "default": True},
                        "name": {"type": "str", "required": True},
                        "notify": {"type": "bool"},
                        "padding": {"type": "str"},
                        "parity": {
                            "type": "str",
                            "choices": ["even", "mark", "none", "odd", "space"],
                        },
                        "password": {
                            "type": "dict",
                            "options": {
                                "hash": {"type": "int", "choices": [0, 7]},
                                "value": {"type": "str", "no_log": True},
                            },
                            "no_log": False,
                        },
                        "privilege": {
                            "type": "int",
                            "choices": [
                                0,
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                7,
                                8,
                                9,
                                10,
                                11,
                                12,
                                12,
                                13,
                                14,
                                15,
                            ],
                        },
                        "session": {
                            "type": "dict",
                            "options": {
                                "disconnect_warning": {"type": "int"},
                                "limit": {"type": "int"},
                                "timeout": {"type": "int"},
                            },
                        },
                        "speed": {"type": "int"},
                        "stopbits": {"type": "str", "choices": ["1", "1.5", "2"]},
                        "transport": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "all": {"type": "bool"},
                                "name": {
                                    "type": "str",
                                    "choices": ["input", "output", "preferred"],
                                },
                                "none": {"type": "bool"},
                                "pad": {"type": "bool"},
                                "rlogin": {"type": "bool"},
                                "ssh": {"type": "bool"},
                                "telnet": {"type": "bool"},
                            },
                        },
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "overridden",
                "replaced",
                "deleted",
                "rendered",
                "parsed",
                "gathered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
