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
The arg spec for the ios_vxlan_vtep module
"""


class Vxlan_vtepArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_vxlan_vtep module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "interface": {"type": "str", "required": True},
                "source_interface": {"type": "str"},
                "host_reachability_bgp": {
                    "type": "bool",
                },
                "member": {
                    "type": "dict",
                    "options": {
                        "vni": {
                            "type": "dict",
                            "options": {
                                "l2vni": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "vni": {"type": "int"},
                                        "replication": {
                                            "type": "dict",
                                            "options": {
                                                "type": {
                                                    "type": "str",
                                                    "choices": ["ingress", "static"],
                                                },
                                                "mcast_group": {
                                                    "type": "dict",
                                                    "options": {
                                                        "ipv4": {"type": "str"},
                                                        "ipv6": {"type": "str"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "l3vni": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "vni": {"type": "int"},
                                        "vrf": {"type": "str"},
                                    },
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
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
