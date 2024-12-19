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

# UNIQUE_AFI = "{{ 'address_families_'+ afi + '_' + safi }}"


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
                (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
                \s+export\sipv4\smulticast\s(?P<prefix>\d+)\smap\s(?P<export_map>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "export ipv4 multicast {{ export.prefix }} map {{ export.map }}",
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
        # {
        #     "name": "export.ipv4.unicast.allow_evpn",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+export\sipv4\sunicast\s(?P<prefix>\d+)\smap\s(?P<export_map>\S+)\s(?P<allow_evpn>allow-evpn)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "export ipv4 unicast {{ export.prefix }} map {{ export.map }} allow-evpn",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{ "address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "export": {
        #                         "ipv4": {
        #                             "unicast": {
        #                                 "prefix": "{{ prefix }}",
        #                                 "map": "{{ export_map }}",
        #                                 "allow_evpn": "{{ true if allow_evpn is defined }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "import_config.ipv4.multicast",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+import\sipv4\smulticast\s(?P<prefix>\d+)\smap\s(?P<import_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "import ipv4 multicast {{ import.prefix }} map {{ import.map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{ "address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "import_config": {
        #                         "ipv4": {
        #                             "multicast": {
        #                                 "prefix": "{{ prefix }}",
        #                                 "map": "{{ import_map }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "import_config.ipv4.unicast",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+import\sipv4\sunicast\s(?P<limit>\d+)\smap\s(?P<import_map>\S+)\s(?P<allow_evpn>allow-evpn)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "import ipv4 multicast {{ import.limit }} map {{ import.map }} allow-evpn",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{ "address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "import_config": {
        #                         "ipv4": {
        #                             "unicast": {
        #                                 "limit": "{{ limit }}",
        #                                 "map": "{{ import_map }}",
        #                                 "allow_evpn": "{{ true if allow_evpn is defined }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "maximum.routes.limit.threshold.reinstall",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+maximum\sroutes\s(?P<limit>\d+)\s(?P<threshold>\d+)\sreinstall(?P<threshold_val>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "maximum routes {{ maximum.limit }} {{ maximum.threshold }} reinstall {{ maximum.threshold_val }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi}}",
        #                     "safi": "{{safi}}",
        #                     "maximum": {
        #                         "routes": {
        #                             "limit": "{{ limit }}",
        #                             "threshold": "{{ threshold }}",
        #                             "reinstall": {
        #                                 "threshold": "{{ threshold_val }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "maximum.routes.limit.warning_only",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+maximum\sroutes\s(?P<limit>\d+)\swarning-only
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "maximum routes {{ maximum.routes.limit }} warning-only",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi}}",
        #                     "safi": "{{safi}}",
        #                     "maximum": {
        #                         "routes": {
        #                             "limit": "{{ limit }}",
        #                             "warning_only": "{{ true }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        {
            "name": "bgp.next_hop.loopback",
            "getval": re.compile(
                r"""
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
        # {
        #     "name": "inter_as_hybrid.csc.next_hop",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+inter-as-hybrid\scsc\snext-hop\s(?P<inter_as_hybrid_csc_next_hop>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "inter-as-hybrid csc next-hop {{ inter_as_hybrid.csc.next_hop }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "inter_as_hybrid": {
        #                         "csc": {
        #                             "next_hop": "{{ inter_as_hybrid_csc_next_hop }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "inter_as_hybrid.next_hop",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+inter-as-hybrid\snext-hop\s(?P<inter_as_hybrid_next_hop>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "inter-as-hybrid next-hop {{ inter_as_hybrid.next_hop }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "inter_as_hybrid": {
        #                         "next_hop": "{{ inter_as_hybrid_next_hop }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.ingress_replication.inter_as.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\singress-replication\sinter-as\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery ingress-replication inter-as mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "ingress_replication": {
        #                                 "inter_as": {
        #                                     "mdt_hello_enable": "{{ true }}",
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.pim.inter_as.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\spim\sinter-as\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery pim inter-as mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "pim": {
        #                                 "inter_as": {
        #                                     "mdt_hello_enable": "{{ true }}",
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.pim.inter_as.pim_tlv_announce.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\spim\sinter-as\spim-tlv-announce\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery pim inter-as pim-tlv-announce mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "pim": {
        #                                 "inter_as": {
        #                                     "pim_tlv_announce": {
        #                                         "mdt_hello_enable": "{{ true }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.ingress_replication.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\singress-replication\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery ingress-replication mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "ingress_replication": {
        #                                 "mdt_hello_enable": "{{ true }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.pim.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\spim\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery pim mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "pim": {
        #                                 "mdt_hello_enable": "{{ true }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.pim.pim_tlv_announce.mdt_hello_enable",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\spim\spim-tlv-announce\smdt-hello-enable
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery pim pim-tlv-announce mdt-hello-enable",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "pim": {
        #                                 "pim_tlv_announce": {
        #                                     "mdt_hello_enable": "{{ true }}",
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.auto_discovery.receiver_site",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sauto-discovery\sreceiver-site
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt auto-discovery receiver-site",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "auto_discovery": {
        #                             "receiver_site": "{{ true }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.ingress_replication.number",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\singress-replication\s(?P<mdt_data_ingress_replication_number>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data ingress-replication {{ mdt.data.ingress_replication.number }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "ingress_replication": {
        #                                 "number": "{{ mdt_data_ingress_replication_number }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.ingress_replication.immediate_switch",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\singress-replication\simmediate-switch
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data ingress-replication immediate-switch",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "ingress_replication": {
        #                                 "immediate_switch": "{{ true }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.ingress_replication.number.immediate_switch",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\singress-replication\s(?P<mdt_data_ingress_replication_number>\d+)\simmediate-switch
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data ingress-replication {{ mdt.data.ingress_replication.number }} immediate-switch",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "ingress_replication": {
        #                                 "number": "{{ mdt_data_ingress_replication_number }}",
        #                                 "immediate_switch": "{{ true }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.list.access_list",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\slist\s(?P<mdt_data_list_access_list>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data list {{ mdt.data.list.access_list }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "list": {
        #                                 "access_list_number": "{{ mdt_data_list_access_list }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.list.access_list_name",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\slist\s(?P<mdt_data_list_access_list_name>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data list {{ mdt.data.list.access_list_name }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "list": {
        #                                 "access_list_name": "{{ mdt_data_list_access_list_name }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.data.threshold",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdata\sthreshold\s(?P<mdt_data_threshold>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt data threshold {{ mdt.data.threshold }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "data": {
        #                             "threshold": "{{ mdt_data_threshold }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.default_ingress_replication",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdefault\singress-replication
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt default ingress-replication",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "default": {
        #                             "ingress_replication": "{{ true }}",
        #                         }
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.direct",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sdirect
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt direct",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "direct": "{{ true }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.log_reuse",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\slog-reuse
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt log-reuse",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "log_reuse": "{{ true }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.mode.gre",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\smode\sgre
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt mode gre",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "mode": {
        #                             "gre": "{{ true }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.mtu.value",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\smtu\s(?P<mtu_value>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt mtu {{ mdt.mtu.value }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "mtu": "{{ mtu_value }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.overlay.bgp.shared_tree_prune_delay",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\soverlay\sbgp\sshared-tree-prune-delay\s(?P<shared_tree_prune_delay>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt overlay bgp shared-tree-prune-delay {{ mdt.overlay.bgp.shared_tree_prune_delay }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "overlay": {
        #                             "bgp": {
        #                                 "shared_tree_prune_delay": "{{ shared_tree_prune_delay }}",
        #                             }
        #                         }
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.overlay.bgp.source_tree_prune_delay",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\soverlay\sbgp\ssource-tree-prune-delay\s(?P<source_tree_prune_delay>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt overlay bgp source-tree-prune-delay {{ mdt.overlay.bgp.source_tree_prune_delay }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "overlay": {
        #                             "bgp": {
        #                                 "source_tree_prune_delay": "{{ source_tree_prune_delay }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.overlay.use_bgp_spt_only",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\soverlay\suse-bgp\sspt-only
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt overlay use-bgp spt-only",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "overlay": {
        #                             "use_bgp": {
        #                                 "spt_only": "{{ true }}",
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.partitioned.ingress_replication",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\spartitioned\singress-replication
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt partitioned ingress-replication",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "partitioned": {
        #                             "ingress_replication": "{{ true }}",
        #                         }
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "mdt.strict_rpf_interface",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+mdt\sstrict-rpf\sinterface
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "mdt strict-rpf interface",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "mdt": {
        #                         "strict_rpf": {
        #                             "interface": "{{ true }}",
        #                         }
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "protection.local_prefixes",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+protection\slocal-prefixes
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "protection local-prefixes",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "protection": {
        #                         "local_prefixes": "{{ true }}",
        #                     }
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.recursion_policy.destination",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\srecursion-policy\sdestination
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate recursion-policy destination",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "recursion_policy": {
        #                             "destination": "{{ true }}",
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.all.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sall\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast all route-map {{ route_replicate.from.vrf.vrf_name.unicast.all.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "all": {
        #                                         "route_map": "{{ route_map }}",
        #                                     }
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.bgp.asn.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sbgp\s(?P<asn>\d+)\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast bgp {{ route_replicate.from.vrf.vrf_name.unicast.bgp.asn }} route-map {{ route_replicate.from.vrf.vrf_name.unicast.bgp.asn.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "bgp": {
        #                                         "as_number": "{{ asn }}",
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.connected.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sconnected\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast connected route-map {{ route_replicate.from.vrf.vrf_name.unicast.connected.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "connected": {
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.eigrp.asn.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\seigrp\s(?P<asn>\d+)\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast eigrp {{ route_replicate.from.vrf.vrf_name.unicast.eigrp.asn }} route-map {{ route_replicate.from.vrf.vrf_name.unicast.eigrp.asn.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "eigrp": {
        #                                         "as_number": "{{ asn }}",
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.isis.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sisis\s(?P<tag>\S+)\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast isis {{ route_replicate.from.vrf.vrf_name.unicast.isis.tag }} route-map {{ route_replicate.from.vrf.vrf_name.unicast.isis.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "isis": {
        #                                         "iso_tag": "{{ tag }}",
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.mobile.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\smobile\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast mobile route-map {{ route_replicate.from.vrf.vrf_name.unicast.mobile.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "mobile": {
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.odr.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sodr\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast odr route-map {{ route_replicate.from.vrf.vrf_name.unicast.odr.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "odr": {
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.ospf.id.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sospf\s(?P<process_id>\d+)\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast ospf {{ route_replicate.from.vrf.vrf_name.unicast.ospf.id }} route-map {{ route_replicate.from.vrf.vrf_name.unicast.ospf.id.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "ospf": {
        #                                         "process_id": "{{ process_id }}",
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.rip.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\srip\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast rip route-map {{ route_replicate.from.vrf.vrf_name.unicast.rip.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "rip": {
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_replicate.from.vrf.vrf_name.unicast.static.route_map",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-replicate\sfrom\svrf\s(?P<vrf_name>\S+)\sunicast\sstatic\sroute-map\s(?P<route_map>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-replicate from vrf {{ route_replicate.from.vrf.vrf_name }} unicast static route-map {{ route_replicate.from.vrf.vrf_name.unicast.static.route_map }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_replicate": {
        #                         "from_config": {
        #                             "vrf": {
        #                                 "name": "{{ vrf_name }}",
        #                                 "unicast": {
        #                                     "static": {
        #                                         "route_map": "{{ route_map }}",
        #                                     },
        #                                 },
        #                             },
        #                         },
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_target.export",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-target\sexport\s(?P<route_target_export>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-target export {{ route_target.export }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_target": {
        #                         "export": "{{ route_target_export }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
        # {
        #     "name": "route_target.import_config",
        #     "getval": re.compile(
        #         r"""
        #         ^vrf\sdefinition\s(?P<name>\S+)
        #         (?P<address_families>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         \s+route-target\simport\s(?P<route_target_import_config>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "route-target import {{ route_target.import_config }}",
        #     "result": {
        #         '{{ name }}': {
        #             'name': '{{ name }}',
        #             "address_families": {
        #                 '{{"address_families_" + afi + "_" + safi }}': {
        #                     "afi": "{{ afi }}",
        #                     "safi": "{{ safi }}",
        #                     "route_target": {
        #                         "import_config": "{{ route_target_import_config }}",
        #                     },
        #                 },
        #             },
        #         },
        #     },
        # },
    ]
    # fmt: on
