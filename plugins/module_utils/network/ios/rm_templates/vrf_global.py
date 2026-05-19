# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vrf_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Vrf_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vrf_globalTemplate, self).__init__(
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
                ^vrf\sdefinition
                (\s(?P<name>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "vrf definition {{ name }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s(?P<description>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        'description': '{{ description }}',
                    },
                },
            },
        },
        {
            "name": "ipv4.multicast.multitopology",
            "getval": re.compile(
                r"""
                \s+ipv4\smulticast\s(?P<multitopology>multitopology)
                $""", re.VERBOSE,
            ),
            "setval": "ipv4 multicast multitopology",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        'ipv4': {
                            'multicast': {
                                'multitopology': "{{ true if multitopology is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.multicast.multitopology",
            "getval": re.compile(
                r"""
                \s+ipv6\smulticast\s(?P<multitopology>multitopology)
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 multicast multitopology",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        'ipv6': {
                            'multicast': {
                                'multitopology': "{{ true if multitopology is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "rd",
            "getval": re.compile(
                r"""
                \s+rd\s(?P<rd>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "rd {{ rd }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "rd": "{{ rd }}",
                    },
                },
            },
        },
        {
            "name": "route_target.exports",
            "getval": re.compile(
                r"""
                \s+route-target\sexport\s(?P<route_target_export>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "route-target export {{ item }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "route_target": {
                            "exports": "{{ [route_target_export] }}",
                        },
                    },
                },
            },
        },
        {
            "name": "route_target.imports",
            "getval": re.compile(
                r"""
                \s+route-target\simport\s(?P<route_target_import>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "route-target import {{ item }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "route_target": {
                            "imports": "{{ [route_target_import] }}",
                        },
                    },
                },
            },
        },
        {
            "name": "route_target.both",
            "getval": re.compile(
                r"""
                \s+route-target\sboth\s(?P<route_target_both>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "route-target both {{ item }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "route_target": {
                            "both_options": "{{ [route_target_both] }}",
                        },
                    },
                },
            },
        },
        {
            "name": "vnet.tag",
            "getval": re.compile(
                r"""
                \s+vnet\stag\s(?P<vnet_tag>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "vnet tag {{ vnet.tag }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "vnet": {
                            "tag": "{{ vnet_tag }}",
                        },
                    },
                },
            },
        },
        {
            "name": "vpn.id",
            "getval": re.compile(
                r"""
                \s+vpn\sid\s(?P<vpn_id>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "vpn id {{ vpn.id }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "vpn": {
                            "id": "{{ vpn_id }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
