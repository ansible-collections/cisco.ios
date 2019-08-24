#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The arg spec for the ios_lldp_interfaces module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class Lldp_InterfacesArgs(object):
    """The arg spec for the ios_lldp_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "name": {"required": True, "type": "str"},
                "transmit": {"type": "bool"},
                "receive": {"type": "bool"},
                "med_tlv_select": {
                    "options": {"inventory_management": {"type": "bool"}},
                    "type": "dict",
                },
                "tlv_select": {
                    "options": {"power_management": {"type": "bool"}},
                    "type": "dict",
                },
            },
            "type": "list",
        },
        "state": {
            "choices": ["merged", "replaced", "overridden", "deleted"],
            "default": "merged",
            "type": "str",
        },
    }
