# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Monitor_sessionsArgs(object):  # pylint: disable=R0903  # NOSONAR
    """The arg spec for the ios_monitor_sessions module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "session": {"type": "int", "required": True},
                "sources": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "interfaces": {
                            "type": "list",
                            "elements": "str",
                            "required": True,
                        },
                        "direction": {
                            "type": "str",
                            "choices": ["rx", "tx", "both"],
                            "default": "both",
                        },
                    },
                },
                "destination": {
                    "type": "dict",
                    "options": {
                        "interface": {"type": "str", "required": True},
                        "encapsulation_replicate": {"type": "bool", "default": False},
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
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
        },
    }  # pylint: disable=C0301
