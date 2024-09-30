# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Vrf_address_family parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

UNIQUE_AFI = "{{ 'address_families_'+ afi + '_' + safi }}"

class Vrf_address_familyTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vrf_address_familyTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "vrf definition {{ name }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                },
            },
            "shared": True,
        },
        {
            "name": "address_family",
            "getval": re.compile(
                r"""
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                $""", re.VERBOSE,
            ),
            "setval": "address-family {{ afi }} {{ safi }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        UNIQUE_AFI: {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                        },
                    },
                },
            },
        },
        {
            "name": "route_target.export",
            "getval": re.compile(
                r"""
                \s+route-target\sexport\s(?P<export>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "route-target export {{ route_target.export }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        "route_target": {
                            "export": "{{ export }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
