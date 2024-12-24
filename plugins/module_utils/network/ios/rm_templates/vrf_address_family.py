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
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                $""", re.VERBOSE,
            ),
            "setval": "address-family {{ afi }} {{ safi }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{"address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                        },
                    },
                },
            },
        },
        {
            "name": "export.map",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+export\smap\s(?P<export_map>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "export map {{ export.map }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{"address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "export": {
                                "map": "{{ export_map }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "import_config.map",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+import\smap\s(?P<import_config_map>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "import map {{ import_config.map }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{"address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "import_config": {
                                "map": "{{ import_config_map }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "export.ipv4.multicast",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+export\sipv4\smulticast\s(?P<prefix>\d+)\smap\s(?P<export_map>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "export ipv4 multicast {{ export.ipv4.multicast.prefix }} map {{ export.ipv4.multicast.prefix.map }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{ "address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "export": {
                                "ipv4": {
                                    "multicast": {
                                        "prefix": "{{ prefix }}",
                                        "map": "{{ export_map }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "export.ipv4.unicast.allow_evpn",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+export\sipv4\sunicast\s(?P<prefix>\d+)\smap\s(?P<export_map>\S+)\s(?P<allow_evpn>allow-evpn)
                $""", re.VERBOSE,
            ),
            "setval": "export ipv4 unicast {{ export.prefix }} map {{ export.map }} allow-evpn",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{ "address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "export": {
                                "ipv4": {
                                    "unicast": {
                                        "prefix": "{{ prefix }}",
                                        "map": "{{ export_map }}",
                                        "allow_evpn": "{{ true if allow_evpn is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "import_config.ipv4.multicast",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+import\sipv4\smulticast\s(?P<prefix>\d+)\smap\s(?P<import_map>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "import ipv4 multicast {{ import.prefix }} map {{ import.map }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{ "address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "import_config": {
                                "ipv4": {
                                    "multicast": {
                                        "prefix": "{{ prefix }}",
                                        "map": "{{ import_map }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "import_config.ipv4.unicast",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+import\sipv4\sunicast\s(?P<limit>\d+)\smap\s(?P<import_map>\S+)\s(?P<allow_evpn>allow-evpn)
                $""", re.VERBOSE,
            ),
            "setval": "import ipv4 unicast {{ import.limit }} map {{ import.map }} allow-evpn",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{ "address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "import_config": {
                                "ipv4": {
                                    "unicast": {
                                        "limit": "{{ limit }}",
                                        "map": "{{ import_map }}",
                                        "allow_evpn": "{{ true if allow_evpn is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.next_hop.loopback",
            "getval": re.compile(
                r"""
                ^vrf\sdefinition\s(?P<name>\S+)
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+bgp\snext-hop\sloopback\s(?P<loopback>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "bgp next-hop loopback {{ bgp.next_hop.loopback }}",
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    "address_families": {
                        '{{"address_families_" + afi + "_" + safi }}': {
                            "afi": "{{ afi }}",
                            "safi": "{{ safi }}",
                            "bgp": {
                                "next_hop": {
                                    "loopback": "{{ loopback }}",
                                },
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
