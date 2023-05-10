# Copyright 2022 Red Hat
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
The arg spec for the ios_acl_interfaces module
"""


class Acl_interfacesArgs:  # pylint: disable=R0903
    """The arg spec for the ios_acl_interfaces module."""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "access_groups": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "afi": {"type": "str", "required": True, "choices": ["ipv4", "ipv6"]},
                        "acls": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "name": {"type": "str", "required": True},
                                "direction": {
                                    "type": "str",
                                    "required": True,
                                    "choices": ["in", "out"],
                                },
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
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "parsed",
                "rendered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
