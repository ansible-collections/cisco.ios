# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bgp_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Bgp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bgp_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    PARSERS = [
        {
            "name": "as_number",
            "getval": re.compile(
                r"""
                ^router\sbgp
                (\s(?P<as_number>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "router bgp {{ as_number|string }}",
            "result": {"as_number": "{{ as_number }}"},
        },
        {
            "name": "aggregate_addresses",
            "getval": re.compile(
                r"""
                \saggregate-address
                (\s(?P<address>\S+))?
                (\s(?P<netmask>\S+))?
                (\s(?P<as_set>as-set))?
                (\s(?P<summary_only>summary-only))?
                (\s(?P<as_confed_set>as-confed-set))?
                (\sadvertise-map\s(?P<advertise_map>\S+))?
                (\sattribute-map\s(?P<attribute_map>\S+))?
                (\ssuppress-map\s(?P<suppress_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "aggregate-address "
            "{{ address }} {{ netmask }}"
            "{{ ' as-set' if as_set|d(False) else ''}}"
            "{{ ' summary-only' if summary_only|d(False) else ''}}"
            "{{ ' as-confed-set' if as_confed_set|d(False) else ''}}"
            "{{ (' advertise-map ' + advertise_map) if advertise_map is defined else '' }}"
            "{{ (' attribute-map ' + attribute_map) if attribute_map is defined else '' }}"
            "{{ (' suppress-map ' + suppress_map) if suppress_map is defined else '' }}",
            "result": {
                "aggregate_addresses": [
                    {
                        "address": "{{ address }}",
                        "netmask": "{{ netmask }}",
                        "advertise_map": "{{ advertise_map }}",
                        "as_confed_set": "{{ not not as_confed_set }}",
                        "as_set": "{{ not not as_set }}",
                        "attribute_map": "{{ attribute_map }}",
                        "suppress_map": "{{ suppress_map }}",
                        "summary_only": "{{ not not summary_only }}",
                    },
                ],
            },
        },
        {
            "name": "auto_summary",
            "getval": re.compile(
                r"""
                ((\sauto-summary))?
                $""",
                re.VERBOSE,
            ),
            "setval": "auto-summary",
            "result": {"auto_summary": True},
        },
        {
            "name": "bmp.buffer_size",
            "getval": re.compile(
                r"""
                \sbmp\sbuffer-size
                (\s(?P<buffer_size>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp buffer-size {{ bmp.buffer_size|string }}",
            "result": {"bmp": {"buffer_size": "{{ buffer_size }}"}},
        },
        {
            "name": "bmp.initial_refresh.delay",
            "getval": re.compile(
                r"""
                \sbmp\sinitial-refresh\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp initial-refresh delay {{ bmp.initial_refresh.delay|string }}",
            "result": {"bmp": {"initial_refresh": {"delay": "{{ delay }}"}}},
        },
        {
            "name": "bmp.initial_refresh.skip",
            "getval": re.compile(
                r"""
                \sbmp\sinitial-refresh\sskip
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp initial-refresh skip",
            "result": {"bmp": {"initial_refresh": {"skip": True}}},
        },
        {
            "name": "bmp.server",
            "getval": re.compile(
                r"""
                \sbmp\sserver
                (\s(?P<server>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp server {{ bmp.server }}",
            "result": {"bmp": {"server": "{{ server|string }}"}},
        },
        {
            "name": "bmp.server_options.activate",
            "getval": re.compile(
                r"""
                \sactivate
                $""",
                re.VERBOSE,
            ),
            "setval": "activate",
            "result": {"bmp": {"server_options": {"activate": True}}},
        },
        {
            "name": "bmp.server_options.address",
            "getval": re.compile(
                r"""
                \saddress\s(?P<host>\S+)\s
                (\sport-number(?P<port>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "address "
            "{{ bmp.server_options.address.host }} port-number {{ bmp.server_options.address.port|string }}\nexit-bmp-server-mode",
            "result": {
                "bmp": {
                    "server_options": {"address": {"host": "{{ host }}", "port": "{{ port }}"}},
                },
            },
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""
                (\sdefault-information originate)?
                $""",
                re.VERBOSE,
            ),
            "setval": "default-information originate",
            "result": {"default_information": True},
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""
                ^default-metric\s(?P<default_metric>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric|string }}",
            "result": {"default_metric": "{{ default_metric }}"},
        },
        {
            "name": "distance.admin",
            "getval": re.compile(
                r"""
                \sdistance
                (\s(?P<distance>\d+))?
                (\s(?P<address>\S+))?
                (\s(?P<wildcard_bit>\S+))?
                (\s(?P<acl>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance"
            "{{ (' ' + distance.admin.distance|string) if distance.admin.distance is defined else '' }}"
            "{{ (' ' + distance.admin.address) if distance.admin.address is defined else '' }}"
            "{{ (' ' + distance.admin.wildcard_bit) if distance.admin.wildcard_bit is defined else '' }}"
            "{{ (' ' + distance.admin.acl) if distance.admin.acl is defined else '' }}",
            "result": {
                "distance": {
                    "admin": {
                        "distance": "{{ distance }}",
                        "address": "{{ address }}",
                        "wildcard_bit": "{{ wildcard_bit }}",
                        "acl": "{{ acl }}",
                    },
                },
            },
        },
        {
            "name": "distance.bgp",
            "getval": re.compile(
                r"""
                \sdistance\sbgp
                (\s(?P<routes_external>\d+))?
                (\s(?P<routes_internal>\d+))?
                (\s(?P<routes_local>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance bgp"
            "{{ (' ' + distance.bgp.routes_external|string) if distance.bgp.routes_external is defined else '' }}"
            "{{ (' ' + distance.bgp.routes_internal|string) if distance.bgp.routes_internal is defined else '' }}"
            "{{ (' ' + distance.bgp.routes_local|string) if distance.bgp.routes_local is defined else '' }}",
            "result": {
                "distance": {
                    "bgp": {
                        "routes_external": "{{ routes_external }}",
                        "routes_internal": "{{ routes_internal }}",
                        "routes_local": "{{ routes_local }}",
                    },
                },
            },
        },
        {
            "name": "distance.mbgp",
            "getval": re.compile(
                r"""
                \sdistance\smbgp
                (\s(?P<routes_external>\d+))?
                (\s(?P<routes_internal>\d+))?
                (\s(?P<routes_local>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance mbgp"
            "{{ (' ' + distance.mbgp.routes_external|string) if distance.mbgp.routes_external is defined else '' }}"
            "{{ (' ' + distance.mbgp.routes_internal|string) if distance.mbgp.routes_internal is defined else '' }}"
            "{{ (' ' + distance.mbgp.routes_local|string) if distance.mbgp.routes_local is defined else '' }}",
            "result": {
                "distance": {
                    "mbgp": {
                        "routes_external": "{{ routes_external }}",
                        "routes_internal": "{{ routes_internal }}",
                        "routes_local": "{{ routes_local }}",
                    },
                },
            },
        },
        {
            "name": "distributes",
            "getval": re.compile(
                r"""
                \sdistribute-list
                (\s(?P<acl>\S+))?
                (\sprefix\s(?P<prefix>\S+))?
                (\sgateway\s(?P<gateway>\S+))?
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                (\s(?P<interface>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distribute-list"
            "{{ (' prefix ' + prefix) if prefix is defined else '' }}"
            "{{ (' gateway ' + gateway) if gateway is defined else '' }}"
            "{{ (' ' + acl) if acl is defined else '' }}"
            "{{ (' in' ) if in|d(False) else '' }}"
            "{{ (' out' ) if out|d(False)  else '' }}"
            "{{ (' ' + interface) if interface is defined else '' }}",
            "result": {
                "distributes": [
                    {
                        "prefix": "{{ prefix }}",
                        "gateway": "{{ gateway }}",
                        "acl": "{{ acl }}",
                        "in": "{{ not not in }}",
                        "out": "{{ not not out }}",
                        "interface": "{{ interface }}",
                    },
                ],
            },
        },
        {
            "name": "maximum_paths.paths",
            "getval": re.compile(
                r"""
                \smaximum-paths
                (\s(?P<paths>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths {{ maximum_paths.paths|string }}",
            "result": {"maximum_paths": {"paths": "{{ paths }}"}},
        },
        {
            "name": "maximum_paths.eibgp",
            "getval": re.compile(
                r"""
                \smaximum-paths\seibgp
                (\s(?P<eibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths eibgp {{ maximum_paths.eibgp|string }}",
            "result": {"maximum_paths": {"eibgp": "{{ eibgp }}"}},
        },
        {
            "name": "maximum_paths.ibgp",
            "getval": re.compile(
                r"""
                \smaximum-paths\sibgp
                (\s(?P<ibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths ibgp {{ maximum_paths.ibgp|string }}",
            "result": {"maximum_paths": {"ibgp": "{{ ibgp }}"}},
        },
        {
            "name": "maximum_secondary_paths.paths",
            "getval": re.compile(
                r"""
                \smaximum-secondary-paths
                (\s(?P<paths>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-secondary-paths {{ maximum_secondary_paths.paths|string }}",
            "result": {"maximum_secondary_paths": {"paths": "{{ paths }}"}},
        },
        {
            "name": "maximum_secondary_paths.eibgp",
            "getval": re.compile(
                r"""
                \smaximum-secondary-paths\seibgp
                (\s(?P<eibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-secondary-paths eibgp {{ maximum_secondary_paths.eibgp|string }}",
            "result": {"maximum_secondary_paths": {"eibgp": "{{ eibgp }}"}},
        },
        {
            "name": "maximum_secondary_paths.ibgp",
            "getval": re.compile(
                r"""
                \smaximum-secondary-paths\sibgp
                (\s(?P<ibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-secondary-paths ibgp {{ maximum_secondary_paths.ibgp|string }}",
            "result": {"maximum_secondary_paths": {"ibgp": "{{ ibgp }}"}},
        },
        {
            "name": "networks",
            "getval": re.compile(
                r"""
                \snetwork
                (\s(?P<address>\S+))?
                (\smask\s(?P<netmask>\S+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\s(?P<backdoor>backdoor))?
                $""",
                re.VERBOSE,
            ),
            "setval": "network"
            "{{ (' ' + address) if address is defined else '' }}"
            "{{ (' mask ' + netmask) if netmask is defined else '' }}"
            "{{ (' route-map ' + route_map) if route_map is defined else '' }}"
            "{{ (' backdoor' ) if backdoor|d(False) else '' }}",
            "result": {
                "networks": [
                    {
                        "address": "{{ address }}",
                        "netmask": "{{ netmask }}",
                        "route_map": "{{ route_map }}",
                        "backdoor": "{{ not not backdoor }}",
                    },
                ],
            },
        },
        {
            "name": "route_server_context.name",
            "getval": re.compile(
                r"""
                \sroute-server_context
                (\s(?P<name>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "route-server-context {{ route_server_context.name }}",
            "result": {"route_server_context": {"name": "{{ name }}"}},
        },
        {
            "name": "route_server_context.address_family",
            "getval": re.compile(
                r"""
                \sroute-server_context\saddress-family
                (\s(?P<afi>ipv4|ipv6))?
                (\s(?P<modifier>multicast|unicast))?
                (\simport-map\s(?P<import_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "address-family"
            "{{ (' ' + route_server_context.address_family.afi) if route_server_context.address_family.afi is defined else '' }}"
            "{{ (' ' + route_server_context.address_family.modifier) if route_server_context.address_family.modifier is defined else '' }}"
            "{{ (' import-map ' + route_server_context.address_family.import_map) if route_server_context.address_family.import_map is defined else '' }}",
            "result": {
                "route_server_context": {
                    "address_family": {
                        "afi": "{{ afi }}",
                        "modifier": "{{ modifier }}",
                        "import_map": "{{ import_map }}",
                    },
                },
            },
        },
        {
            "name": "route_server_context.description",
            "getval": re.compile(
                r"""
                \sroute-server_context\sdescription
                (\s(?P<description>.+$))?
                """,
                re.VERBOSE,
            ),
            "setval": "description {{ route_server_context.description }}",
            "result": {"route_server_context": {"description": "{{ description }}"}},
        },
        {
            "name": "synchronization",
            "getval": re.compile(r"""\s(?P<synchronization>synchronization)""", re.VERBOSE),
            "setval": "synchronization",
            "result": {"synchronization": "{{ not not synchronization }}"},
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""
                \stable-map
                (\s(?P<name>\S+))?
                (\s(?P<filter>filter))?
                $""",
                re.VERBOSE,
            ),
            "setval": "table-map"
            "{{ (' ' + name) if name is defined else '' }}"
            "{{ (' filter' ) if filter|d(False) else '' }}",
            "result": {"table_map": {"name": "{{ name }}", "filter": "{{ not not filter }}"}},
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \stimers\sbgp
                (\s(?P<keepalive>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers bgp"
            "{{ (' ' + timers.keepalive|string) if timers.keepalive is defined else '' }}"
            "{{ (' ' + timers.holdtime|string) if timers.holdtime is defined else '' }}"
            "{{ (' ' + timers.min_holdtime|string) if timers.min_holdtime is defined else '' }}",
            "result": {
                "timers": {
                    "keepalive": "{{ keepalive }}",
                    "holdtime": "{{ holdtime }}",
                    "min_holdtime": "{{ min_holdtime }}",
                },
            },
        },
        # bgp starts
        {
            "name": "bgp.additional_paths",
            "getval": re.compile(
                r"""
                \sbgp\sadditional-paths
                (\s(?P<install>install))?
                (\s(?P<receive>receive))?
                (\s(?P<select>select))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths"
            "{{ (' install' ) if bgp.additional_paths.install|d(False) else '' }}"
            "{{ (' receive' ) if bgp.additional_paths.receive|d(False) else '' }}"
            "{{ (' select' ) if bgp.additional_paths.select|d(False) else '' }}"
            "{{ (' send' ) if bgp.additional_paths.send|d(False) else '' }}",
            "result": {
                "bgp": {
                    "additional_paths": {
                        "install": "{{ not not install }}",
                        "receive": "{{ not not receive }}",
                        "select": "{{ not not select }}",
                        "send": "{{ not not send }}",
                    },
                },
            },
        },
        {
            "name": "bgp.advertise_best_external",
            "getval": re.compile(r"""\s(bgp\sadvertise-best-external)""", re.VERBOSE),
            "setval": "{{ ('bgp advertise-best-external' ) if bgp.advertise_best_external|d(False) else '' }}",
            "result": {"bgp": {"advertise_best_external": True}},
        },
        {
            "name": "bgp.aggregate_timer",
            "getval": re.compile(
                r"""
                \sbgp\saggregate-timer
                (\s(?P<aggregate_timer>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp aggregate-timer {{ bgp.aggregate_timer|string }}",
            "result": {"bgp": {"aggregate_timer": "{{ aggregate_timer }}"}},
        },
        {
            "name": "bgp.always_compare_med",
            "getval": re.compile(r"""\s(bgp\salways-compare-med)""", re.VERBOSE),
            "setval": "{{ ('bgp always-compare-med' ) if bgp.always_compare_med|d(False) else '' }}",
            "result": {"bgp": {"always_compare_med": True}},
        },
        {
            "name": "bgp.asnotation",
            "getval": re.compile(r"""\s(bgp\sasnotation\sdot)""", re.VERBOSE),
            "setval": "{{ ('bgp asnotation dot' ) if bgp.asnotation|d(False) else '' }}",
            "result": {"bgp": {"asnotation": True}},
        },
        {
            "name": "bgp.bestpath_options.aigp",
            "getval": re.compile(r"""\s(bgp\sbestpath\saigp\signore)""", re.VERBOSE),
            "setval": "{{ ('bgp bestpath aigp ignore' ) if bgp.bestpath_options.aigp|d(False) else '' }}",
            "result": {"bgp": {"bestpath_options": {"aigp": True}}},
        },
        {
            "name": "bgp.bestpath_options.compare_routerid",
            "getval": re.compile(r"""\s(bgp\sbestpath\scompare-routerid)""", re.VERBOSE),
            "setval": "{{ ('bgp bestpath compare-routerid' ) if bgp.bestpath_options.compare_routerid|d(False) else '' }}",
            "result": {"bgp": {"bestpath_options": {"compare_routerid": True}}},
        },
        {
            "name": "bgp.bestpath_options.cost_community",
            "getval": re.compile(r"""\s(bgp\sbestpath\scost-community\signore)""", re.VERBOSE),
            "setval": "{{ ('bgp bestpath cost-community ignore' ) if bgp.bestpath_options.cost_community|d(False) else '' }}",
            "result": {"bgp": {"bestpath_options": {"cost_community": True}}},
        },
        {
            "name": "bgp.bestpath_options.igp_metric",
            "getval": re.compile(r"""\s(bgp\sbestpath\sigp-metric\signore)""", re.VERBOSE),
            "setval": "bgp bestpath igp-metric ignore",
            "result": {"bgp": {"bestpath_options": {"igp_metric": True}}},
        },
        {
            "name": "bgp.bestpath_options.med",
            "getval": re.compile(
                r"""
                \sbgp\sbestpath\smed
                (\s(?P<confed>confed))?
                (\s(?P<missing_as_worst>missing-as-worst))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp bestpath med"
            "{{ (' confed') if bgp.bestpath_options.med.confed|d(False) else '' }}"
            "{{ (' missing-as-worst') if bgp.bestpath_options.med.missing_as_worst|d(False) else '' }}",
            "result": {
                "bgp": {
                    "bestpath_options": {
                        "med": {
                            "confed": "{{ not not confed }}",
                            "missing_as_worst": "{{ not not missing_as_worst }}",
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.client_to_client",
            "getval": re.compile(
                r"""
                \sbgp\sclient-to-client
                (\s(?P<set>reflection))?
                (\s(?P<all>all))?
                (\sintra-cluster\scluster-id\s(?P<intra_cluster>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp client-to-client"
            "{{ (' reflection') if bgp.client_to_client.set|d(False) else '' }}"
            "{{ (' all') if bgp.client_to_client.all|d(False) else '' }}"
            "{{ (' intra-cluster cluster-id '+ bgp.client_to_client.intra_cluster ) if bgp.client_to_client.intra_cluster is defined else '' }}",
            "result": {
                "bgp": {
                    "client_to_client": {
                        "set": "{{ not not set }}",
                        "all": "{{ not not all }}",
                        "intra_cluster": "{{ intra_cluster }}",
                    },
                },
            },
        },
        {
            "name": "bgp.cluster_id",
            "getval": re.compile(
                r"""
                \sbgp\scluster-id
                (\s(?P<cluster_id>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp cluster-id {{ bgp.cluster_id }}",
            "result": {"bgp": {"cluster_id": "{{ not not cluster_id }}"}},
        },
        {
            "name": "bgp.confederation.peer",
            "getval": re.compile(
                r"""
                \sbgp\sconfederation\speer
                (\s(?P<peer>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp confederation peers {{ bgp.confederation.peer }}",
            "result": {"bgp": {"confederation": {"peers": "{{ peer }}"}}},
        },
        {
            "name": "bgp.confederation.identifier",
            "getval": re.compile(
                r"""
                \sbgp\sconfederation\sidentifier
                (\s(?P<identifier>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp confederation identifier {{ bgp.confederation.identifier }}",
            "result": {"bgp": {"confederation": {"identifier": "{{ identifier }}"}}},
        },
        {
            "name": "bgp.consistency_checker.auto_repair",
            "getval": re.compile(
                r"""
                \sbgp\sconsistency-checker\sauto-repair
                (\sinterval\s(?P<interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp consistency-checker auto-repair"
            "{{ (' interval '+ bgp.consistency_checker.auto_repair.interval|string) if bgp.consistency_checker.auto_repair.interval is defined else '' }}",
            "result": {
                "bgp": {
                    "consistency_checker": {
                        "auto_repair": {"set": True, "interval": "{{ interval }}"},
                    },
                },
            },
        },
        {
            "name": "bgp.consistency_checker.error_message",
            "getval": re.compile(
                r"""
                \sbgp\sconsistency-checker\serror-message
                (\sinterval\s(?P<interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp consistency-checker error-message"
            "{{ (' interval '+ bgp.consistency_checker.error_message.interval|string) if bgp.consistency_checker.error_message.interval is defined else '' }}",
            "result": {
                "bgp": {
                    "consistency_checker": {
                        "error_message": {"set": True, "interval": "{{ interval }}"},
                    },
                },
            },
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""
                \sbgp\sdampening
                (\s(?P<penalty_half_time>\d+))?
                (\s(?P<reuse_route_val>\d+))?
                (\s(?P<suppress_route_val>\d+))?
                (\s(?P<max_suppress>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp dampening"
            "{{ (' '+ bgp.dampening.penalty_half_time|string) if bgp.dampening.penalty_half_time is defined else '' }}"
            "{{ (' '+ bgp.dampening.reuse_route_val|string) if bgp.dampening.reuse_route_val is defined else '' }}"
            "{{ (' '+ bgp.dampening.suppress_route_val|string) if bgp.dampening.suppress_route_val is defined else '' }}"
            "{{ (' '+ bgp.dampening.max_suppress|string) if bgp.dampening.max_suppress is defined else '' }}"
            "{{ (' route-map '+ bgp.dampening.route_map|string) if bgp.dampening.route_map is defined else '' }}",
            "result": {
                "bgp": {
                    "dampening": {
                        "penalty_half_time": "{{ penalty_half_time }}",
                        "reuse_route_val": "{{ reuse_route_val }}",
                        "suppress_route_val": "{{ suppress_route_val }}",
                        "max_suppress": "{{ max_suppress }}",
                        "route_map": "{{ route_map }}",
                    },
                },
            },
        },
        {
            "name": "bgp.deterministic_med",
            "getval": re.compile(r"""\s(bgp\sdeterministic-med)""", re.VERBOSE),
            "setval": "bgp deterministic-med",
            "result": {"bgp": {"deterministic_med": True}},
        },
        {
            "name": "bgp.dmzlink_bw",
            "getval": re.compile(r"""\s(bgp\sdmzlink-bw)""", re.VERBOSE),
            "setval": "bgp dmzlink-bw",
            "result": {"bgp": {"dmzlink_bw": True}},
        },
        {
            "name": "bgp.enforce_first_as",
            "getval": re.compile(r"""\s(bgp\senforce-first-as)""", re.VERBOSE),
            "setval": "bgp enforce-first-as",
            "result": {"bgp": {"enforce_first_as": True}},
        },
        {
            "name": "bgp.enhanced_error",
            "getval": re.compile(r"""\s(bgp\senhanced-error)""", re.VERBOSE),
            "setval": "bgp enhanced-error",
            "result": {"bgp": {"enhanced_error": True}},
        },
        {
            "name": "bgp.fast_external_fallover",
            "getval": re.compile(r"""\s(bgp\sfast-external-fallover)""", re.VERBOSE),
            "setval": "bgp fast-external-fallover",
            "result": {"bgp": {"fast_external_fallover": True}},
        },
        {
            "name": "bgp.graceful_restart.set",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-restart
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart",
            "result": {"bgp": {"graceful_restart": {"set": True}}},
        },
        {
            "name": "bgp.graceful_restart.extended",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-restart\sextended
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart extended",
            "result": {"bgp": {"graceful_restart": {"extended": True}}},
        },
        {
            "name": "bgp.graceful_restart.restart_time",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-restart\srestart-time
                (\s(?P<restart_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart restart-time {{ bgp.graceful_restart.restart_time|string }}",
            "result": {"bgp": {"graceful_restart": {"restart_time": "{{ restart_time }}"}}},
        },
        {
            "name": "bgp.graceful_restart.stalepath_time",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-restart\sstalepath-time
                (\s(?P<stalepath_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart stalepath-time {{ bgp.graceful_restart.stalepath_time|string }}",
            "result": {"bgp": {"graceful_restart": {"stalepath_time": "{{ stalepath_time }}"}}},
        },
        {
            "name": "bgp.graceful_shutdown.neighbors",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-shutdown\sall\sneighbors
                (\s(?P<time>\d+))?
                (\s(?P<activate>activate))?
                (\slocal-preference\s(?P<local_preference>\d+))?
                (\scommunity\s(?P<community>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-shutdown all neighbors"
            "{{ (' ' + bgp.graceful_shutdown.neighbors.time|string) if bgp.graceful_shutdown.neighbors.time is defined else '' }}"
            "{{ (' activate') if bgp.graceful_shutdown.neighbors.activate|d(False) else '' }}"
            "{{ (' local-preference ' + bgp.graceful_shutdown.local_preference|string) if bgp.graceful_shutdown.local_preference is defined else '' }}"
            "{{ (' community ' + bgp.graceful_shutdown.community|string) if bgp.graceful_shutdown.community is defined else '' }}",
            "result": {
                "bgp": {
                    "graceful_shutdown": {
                        "neighbors": {"time": "{{ time }}", "activate": "{{ not not activate }}"},
                        "community": "{{ community }}",
                        "local_preference": "{{ local_preference }}",
                    },
                },
            },
        },
        {
            "name": "bgp.graceful_shutdown.vrfs",
            "getval": re.compile(
                r"""
                \sbgp\sgraceful-shutdown\sall\svrfs
                (\s(?P<time>\d+))?
                (\s(?P<activate>activate))?
                (\slocal-preference\s(?P<local_preference>\d+))?
                (\scommunity\s(?P<community>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-shutdown all vrfs"
            "{{ (' ' + bgp.graceful_shutdown.vrfs.time|string) if bgp.graceful_shutdown.vrfs.time is defined else '' }}"
            "{{ (' activate') if bgp.graceful_shutdown.vrfs.activate|d(False) else '' }}"
            "{{ (' local-preference ' + bgp.graceful_shutdown.local_preference|string) if bgp.graceful_shutdown.local_preference is defined else '' }}"
            "{{ (' community ' + bgp.graceful_shutdown.community|string) if bgp.graceful_shutdown.community is defined else '' }}",
            "result": {
                "bgp": {
                    "graceful_shutdown": {
                        "vrfs": {"time": "{{ time }}", "activate": "{{ not not activate }}"},
                        "community": "{{ community }}",
                        "local_preference": "{{ local_preference }}",
                    },
                },
            },
        },
        {
            "name": "inject_maps",
            "getval": re.compile(
                r"""
                \sbgp\sinject-map
                (\s(?P<name>\S+))?
                (\sexist-map\s(?P<exist_map_name>\S+))?
                (\s(?P<copy_attributes>copy-attributes))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp inject-map"
            "{{ (' '+ name) if name is defined else '' }}"
            "{{ (' exist-map '+ exist_map_name) if exist_map_name is defined else '' }}"
            "{{ (' copy-attributes') if copy_attributes|d(False) else '' }}",
            "result": {
                "bgp": {
                    "inject_maps": [
                        {
                            "name": "{{ name }}",
                            "exist_map_name": "{{ exist_map_name }}",
                            "copy_attributes": "{{ not not copy_attributes }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "bgp.listen.limit",
            "getval": re.compile(
                r"""
                \sbgp\slisten\slimit
                (\s(?P<limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp listen limit {{ bgp.listen.limit|string }}",
            "result": {"bgp": {"listen": {"limit": "{{ limit }}"}}},
        },
        {
            "name": "bgp.listen.range",
            "getval": re.compile(
                r"""
                \sbgp\slisten\srange
                (\s(?P<host_with_subnet>\S+))?
                (\speer-group\s(?P<peer_group>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp listen range"
            "{{ (' '+ bgp.listen.range.host_with_subnet) if bgp.listen.range.host_with_subnet is defined else '' }}"
            "{{ (' peer-group '+ bgp.listen.range.peer_group) if bgp.listen.range.peer_group is defined else '' }}",
            "result": {
                "bgp": {
                    "listen": {
                        "range": {
                            "host_with_subnet": "{{ host_with_subnet }}",
                            "peer_group": "{{ peer_group }}",
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.log_neighbor_changes",
            "getval": re.compile(r"""\s(bgp\slog-neighbor-changes)""", re.VERBOSE),
            "setval": "bgp log-neighbor-changes",
            "result": {"bgp": {"log_neighbor_changes": True}},
        },
        {
            "name": "bgp.maxas_limit",
            "getval": re.compile(
                r"""
                \sbgp\smaxas-limit
                (\s(?P<maxas_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxas-limit {{ bgp.maxas_limit|string }}",
            "result": {"bgp": {"maxas_limit": "{{ maxas_limit }}"}},
        },
        {
            "name": "bgp.maxcommunity_limit",
            "getval": re.compile(
                r"""
                \sbgp\smaxcommunity-limit
                (\s(?P<maxcommunity_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxcommunity-limit {{ bgp.maxcommunity_limit|string }}",
            "result": {"bgp": {"maxcommunity_limit": "{{ maxcommunity_limit }}"}},
        },
        {
            "name": "bgp.maxextcommunity_limit",
            "getval": re.compile(
                r"""
                \sbgp\smaxextcommunity-limit
                (\s(?P<maxextcommunity_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxextcommunity-limit {{ bgp.maxextcommunity_limit|string }}",
            "result": {"bgp": {"maxextcommunity_limit": "{{ maxextcommunity_limit }}"}},
        },
        {
            "name": "bgp.nexthop.route_map",
            "getval": re.compile(
                r"""
                \sbgp\snexthop\sroute-map
                (\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop route-map {{ bgp.nexthop.route_map }}",
            "result": {"bgp": {"nexthop": {"route_map": "{{ route_map }}"}}},
        },
        {
            "name": "bgp.nexthop.trigger.delay",
            "getval": re.compile(
                r"""
                \sbgp\snexthop\strigger\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger delay {{ bgp.nexthop.trigger.delay|string }}",
            "result": {"bgp": {"nexthop": {"trigger": {"delay": "{{ delay }}"}}}},
        },
        {
            "name": "bgp.nexthop.trigger.enable",
            "getval": re.compile(
                r"""
                \sbgp\snexthop\strigger\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger enable",
            "result": {"bgp": {"nexthop": {"trigger": {"enable": True}}}},
        },
        {
            "name": "bgp.nopeerup_delay_options.cold_boot",
            "getval": re.compile(
                r"""
                \sbgp\snopeerup-delay\scold-boot
                (\s(?P<cold_boot>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay cold-boot {{ bgp.nopeerup_delay_options.cold_boot|string }}",
            "result": {"bgp": {"nopeerup_delay_options": {"cold_boot": "{{ cold_boot }}"}}},
        },
        {
            "name": "bgp.nopeerup_delay_options.post_boot",
            "getval": re.compile(
                r"""
                \sbgp\snopeerup-delay\spost-boot
                (\s(?P<post_boot>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay post-boot {{ bgp.nopeerup_delay_options.post_boot|string }}",
            "result": {"bgp": {"nopeerup_delay_options": {"post_boot": "{{ post_boot }}"}}},
        },
        {
            "name": "bgp.nopeerup_delay_options.nsf_switchover",
            "getval": re.compile(
                r"""
                \sbgp\snopeerup-delay\snsf-switchover
                (\s(?P<nsf_switchover>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay nsf-switchover {{ bgp.nopeerup_delay_options.nsf_switchover|string }}",
            "result": {
                "bgp": {"nopeerup_delay_options": {"nsf_switchover": "{{ nsf_switchover }}"}},
            },
        },
        {
            "name": "bgp.nopeerup_delay_options.user_initiated",
            "getval": re.compile(
                r"""
                \sbgp\snopeerup-delay\suser-initiated
                (\s(?P<user_initiated>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay user-initiated {{ bgp.nopeerup_delay_options.user_initiated|string }}",
            "result": {
                "bgp": {"nopeerup_delay_options": {"user_initiated": "{{ user_initiated }}"}},
            },
        },
        {
            "name": "bgp.recursion",
            "getval": re.compile(
                r"""
                \sbgp\srecursion\shost
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp recursion host",
            "result": {"bgp": {"recursion": True}},
        },
        {
            "name": "bgp.redistribute_internal",
            "getval": re.compile(
                r"""
                \sbgp\sredistribute-internal
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp redistribute-internal",
            "result": {"bgp": {"redistribute_internal": True}},
        },
        {
            "name": "bgp.refresh.max_eor_time",
            "getval": re.compile(
                r"""
                \sbgp\srefresh\smax-eor-time
                (\s(?P<max_eor_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp refresh max-eor-time {{ bgp.refresh.max_eor_time|string }}",
            "result": {"bgp": {"refresh": {"max_eor_time": "{{ max_eor_time }}"}}},
        },
        {
            "name": "bgp.refresh.stalepath_time",
            "getval": re.compile(
                r"""
                \sbgp\srefresh\sstalepath-time
                (\s(?P<stalepath_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp refresh stalepath-time {{ bgp.refresh.stalepath_time|string }}",
            "result": {"bgp": {"refresh": {"stalepath_time": "{{ stalepath_time }}"}}},
        },
        {
            "name": "bgp.regexp",
            "getval": re.compile(
                r"""
                \sbgp\sregexp\sdeterministic
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp regexp deterministic",
            "result": {"bgp": {"regexp": True}},
        },
        {
            "name": "bgp.router_id",
            "getval": re.compile(
                r"""
                \sbgp\srouter-id
                (\s(?P<address>\S+))?
                (\sinterface\s(?P<interface>\S+))?
                (\svrf\s(?P<vrf>auto-assign))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp router-id"
            "{{ (' ' + bgp.router_id.address) if bgp.router_id.address is defined else '' }}"
            "{{ (' interface ' + bgp.router_id.interface) if bgp.router_id.interface is defined else '' }}"
            "{{ (' vrf auto-assign') if bgp.router_id.vrf|d(False) else '' }}",
            "result": {
                "bgp": {
                    "router_id": {
                        "address": "{{ address }}",
                        "interface": "{{ interface }}",
                        "vrf": "{{ not not vrf }}",
                    },
                },
            },
        },
        {
            "name": "bgp.scan_time",
            "getval": re.compile(
                r"""
                \sbgp\sscan-time
                (\s(?P<scan_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp scan-time {{ bgp.scan_time|string }}",
            "result": {"bgp": {"scan_time": "{{ scan_time }}"}},
        },
        {
            "name": "bgp.slow_peer.detection.set",
            "getval": re.compile(
                r"""
                \sbgp\sslow-peer\sdetection
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer detection",
            "result": {"bgp": {"slow_peer": {"detection": {"set": True}}}},
        },
        {
            "name": "bgp.slow_peer.detection.threshold",
            "getval": re.compile(
                r"""
                \sbgp\sslow-peer\sdetection\sthreshold
                (\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer detection threshold {{ bgp.slow_peer.detection.threshold|string }}",
            "result": {"bgp": {"slow_peer": {"detection": {"threshold": "{{ threshold }}"}}}},
        },
        {
            "name": "bgp.slow_peer.split_update_group",
            "getval": re.compile(
                r"""
                \sbgp\sslow-peer\ssplit-update-group
                (\s(?P<dynamic>dynamic))?
                (\s(?P<permanent>permanent))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group"
            "{{ (' dynamic') if bgp.slow_peer.split_update_group.dynamic|d(False) else '' }}"
            "{{ (' permanent') if bgp.slow_peer.split_update_group.permanent|d(False) else '' }}",
            "result": {
                "bgp": {
                    "slow_peer": {
                        "split_update_group": {
                            "dynamic": "{{ not not dynamic }}",
                            "permanent": "{{ not not permanent }}",
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.snmp",
            "getval": re.compile(
                r"""
                \sbgp\ssnmp\straps\sadd-type
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp snmp traps add-type",
            "result": {"bgp": {"snmp": True}},
        },
        {
            "name": "bgp.sso",
            "getval": re.compile(
                r"""
                \sbgp\ssso\sroute-refresh-enable
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp sso route-refresh-enable",
            "result": {"bgp": {"sso": True}},
        },
        {
            "name": "bgp.soft_reconfig_backup",
            "getval": re.compile(
                r"""
                \sbgp\ssoft-reconfig-backup
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp soft-reconfig-backup ",
            "result": {"bgp": {"soft_reconfig_backup": True}},
        },
        {
            "name": "bgp.suppress_inactive",
            "getval": re.compile(
                r"""
                \sbgp\ssuppress-inactive
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp suppress-inactive",
            "result": {"bgp": {"suppress_inactive": True}},
        },
        {
            "name": "bgp.transport",
            "getval": re.compile(
                r"""
                \sbgp\stransport\spath-mtu-discovery
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp transport path-mtu-discovery",
            "result": {"bgp": {"transport": True}},
        },
        {
            "name": "bgp.update_delay",
            "getval": re.compile(
                r"""
                \sbgp\supdate-delay
                (\s(?P<update_delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp update-delay {{ bgp.update_delay|string }}",
            "result": {"bgp": {"update_delay": "{{ update_delay }}"}},
        },
        {
            "name": "bgp.update_group",
            "getval": re.compile(
                r"""
                \sbgp\supdate-group\ssplit\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp update-group split as-override",
            "result": {"bgp": {"update_group": True}},
        },
        {
            "name": "bgp.upgrade_cli.set",
            "getval": re.compile(
                r"""
                \sbgp\supgrade-cli
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp upgrade-cli",
            "result": {"bgp": {"update_group": {"set": True}}},
        },
        {
            "name": "bgp.upgrade_cli.af_mode",
            "getval": re.compile(
                r"""
                \sbgp\supgrade-cli\saf-mode
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp upgrade-cli af-mode",
            "result": {"bgp": {"update_group": {"af_mode": True}}},
        },
        # bgp ends
        # neighbor remote-as starts
        {
            "name": "neighbor_address",
            "getval": re.compile(
                r"""
                \sneighbordel(?P<neighbor_address>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}",
            "result": {"del_neighbor": True},
        },
        {
            "name": "remote_as",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \sremote-as\s(?P<remote_as>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' remote-as ' + remote_as|string) if remote_as is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "remote_as": "{{ remote_as }}",
                        "neighbor_address": "{{ neighbor_address }}",
                    },
                },
            },
        },
        {
            "name": "peer_group",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \speer-group\s(?P<peer_group>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' peer-group ' + peer_group) if peer_group|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "peer_group": "{{ peer_group }}",
                        "neighbor_address": "{{ neighbor_address }}",
                    },
                },
            },
        },
        {
            "name": "bmp_activate",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \s(?P<bmp_activate>bmp-activate)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} bmp-activate",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"bmp_activate": "{{ not not bmp_activate }}"},
                },
            },
        },
        {
            "name": "cluster_id",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \s(?P<cluster_id>cluster-id)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} cluster-id",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"cluster_id": "{{ not not cluster_id }}"}},
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \sdescription\s(?P<description>.+$)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} description"
            "{{ (' ' + description) if description is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "description": "{{ description }}",
                    },
                },
            },
        },
        {
            "name": "disable_connected_check",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \s(?P<disable_connected_check>disable-connected-check)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} disable-connected-check",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "disable_connected_check": "{{ not not disable_connected_check }}",
                    },
                },
            },
        },
        {
            "name": "ebgp_multihop",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \s(?P<enable>ebgp_multihop)
                (\s(?P<hop_count>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ebgp-multihop"
            "{{ (' ' + hop_count|string) if hop_count is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "ebgp_multihop": {
                            "enable": "{{ not not enable }}",
                            "hop_count": "{{ hop_count }}",
                        },
                    },
                },
            },
        },
        {
            "name": "fall_over.bfd",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sfall-over
                \s(?P<set>bfd)
                (\s(?P<multi_hop>multi-hop))?
                (\s(?P<single_hop>single-hop))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} fall-over"
            "{{ (' bfd') if fall_over.bfd.set is defined else '' }}"
            "{{ (' multi-hop') if fall_over.bfd.multi_hop is defined else '' }}"
            "{{ (' single-hop') if fall_over.bfd.single_hop is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "fall_over": {
                            "bfd": {
                                "set": "{{ not not set }}",
                                "multi_hop": "{{ not not multi_hop }}",
                                "single_hop": "{{ not not single_hop }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "fall_over.route_map",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sroute-map
                \s(?P<route_map>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} route-map {{ fall_over.route_map }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "fall_over": {"route_map": "{{ not not route_map }}"},
                    },
                },
            },
        },
        {
            "name": "ha_mode",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sha-mode
                \s(?P<set>graceful-restart)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ha-mode"
            "{{ (' graceful-restart') if ha_mode.set|d(False) is defined else '' }}"
            "{{ (' disable') if ha_mode.disable is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "ha_mode": {"set": "{{ not not set }}", "disable": "{{ not not disable }}"},
                    },
                },
            },
        },
        {
            "name": "inherit",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sinherit\speer-session
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} inherit peer-session"
            "{{ (' ' + inherit) if inherit is defined else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"inherit": "{{ inherit }}"}}},
        },
        {
            "name": "local_as",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\s(?P<local_as>local-as)
                (\s(?P<number>\S+))?
                (\s(?P<dual_as>dual-as))?
                (\s(?P<no_prepend>no-prepend))?
                (\s(?P<replace_as>replace-as))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} local-as"
            "{{ (' ' + local_as.number|string) if local_as.number is defined else '' }}"
            "{{ (' dual-as') if local_as.dual_as is defined else '' }}"
            "{{ (' no-prepend') if local_as.no_prepend.set is defined else '' }}"
            "{{ (' replace-as') if local_as.no_prepend.replace_as is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "local_as": {
                            "set": "{{ not not local_as }}",
                            "number": "{{ number }}",
                            "dual_as": "{{ not not dual_as }}",
                            "no_prepend": {
                                "set": "{{ not not no_prepend }}",
                                "replace_as": "{{ not not replace_as }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)
                \s(?P<set>log-neighbor-changes)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' log-neighbor-changes') if log_neighbor_changes.set is defined else '' }}"
            "{{ (' disable') if log_neighbor_changes.disable is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "log_neighbor_changes": {
                            "set": "{{ not not set }}",
                            "disable": "{{ not not disable }}",
                        },
                    },
                },
            },
        },
        {
            "name": "password_options",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\spassword
                \s(?P<encryption>\d+)
                (\s(?P<pass_key>.$))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} password"
            "{{ (' '+ password_options.encryption|string) if password_options.encryption is defined else '' }}"
            "{{ (' '+ password_options.pass_key) if password_options.pass_key is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "password_options": {
                            "encryption": "{{ encryption }}",
                            "pass_key": "{{ pass_key }}",
                        },
                    },
                },
            },
        },
        {
            "name": "path_attribute.discard",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\spath-attribute\sdiscard
                (\s(?P<type>\d+))?
                (\srange\s(?P<start>\d+)\s(?P<end>\d+))?
                (\s(?P<in>in))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} path-attribute discard"
            "{{ (' ' + type) if path_attribute.discard.type is defined else '' }}"
            "{{ (' range '+ path_attribute.discard.range.start|string) if spath_attribute.discard.range.start is defined else '' }}"
            "{{ (' '+ path_attribute.discard.range.end|string) if spath_attribute.discard.range.end is defined else '' }}"
            "{{ (' in') if path_attribute.discard.in|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "path_attribute": {
                            "discard": {
                                "type": "{{ type }}",
                                "range": {"start": "{{ start }}", "end": "{{ end }}"},
                                "in": "{{ not not in }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "path_attribute.treat_as_withdraw",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\spath-attribute\streat-as-withdraw
                (\s(?P<type>\d+))?
                (\srange\s(?P<start>\d+)\s(?P<end>\d+))?
                (\s(?P<in>in))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} path-attribute treat-as-withdraw"
            "{{ (' ' + type) if path_attribute.treat_as_withdraw.type is defined else '' }}"
            "{{ (' range '+ path_attribute.treat_as_withdraw.range.start|string) if spath_attribute.treat_as_withdraw.range.start is defined else '' }}"
            "{{ (' '+ path_attribute.treat_as_withdraw.range.end|string) if spath_attribute.treat_as_withdraw.range.end is defined else '' }}"
            "{{ (' in') if path_attribute.treat_as_withdraw.in|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "path_attribute": {
                            "treat_as_withdraw": {
                                "type": "{{ type }}",
                                "range": {"start": "{{ start }}", "end": "{{ end }}"},
                                "in": "{{ not not in }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sshutdown
                (\sgraceful(?P<graceful>\d+))?
                (\scommunity(?P<community>\d+))?
                (\s(?P<local_preference>local-preference))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' shutdown') if shutdown.set|d(False) is defined else '' }}"
            "{{ (' graceful '+ shutdown.graceful|string) if shutdown.graceful is defined else '' }}"
            "{{ (' community '+ shutdown.community|string) if shutdown.community is defined else '' }}"
            "{{ (' local-preference') if shutdown.local_preference|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "shutdown": {
                            "set": True,
                            "graceful": "{{ graceful }}",
                            "community": "{{ community }}",
                            "local_preference": "{{ not not local_preference }}",
                        },
                    },
                },
            },
        },
        {
            "name": "soft_reconfiguration",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssoft-reconfiguration\sinbound
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' soft-reconfiguration inbound') if soft_reconfiguration|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"soft_reconfiguration": True}}},
        },
        {
            "name": "ntimers",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stimers
                (\s(?P<interval>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} timers"
            "{{ (' ' + ntimers.interval|string) if ntimers.interval is defined else '' }}"
            "{{ (' ' + ntimers.holdtime|string) if ntimers.holdtime is defined else '' }}"
            "{{ (' ' + ntimers.min_holdtime|string) if ntimers.min_holdtime is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "timers": {
                            "interval": "{{ interval }}",
                            "holdtime": "{{ holdtime }}",
                            "min_holdtime": "{{ min_holdtime }}",
                        },
                    },
                },
            },
        },
        {
            "name": "transport.connection_mode",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stransport\sconnection-mode
                (\s(?P<active>active))?
                (\s(?P<passive>passive))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport connection-mode"
            "{{ (' active') if transport.connection_mode.active|d(False) else '' }}"
            "{{ (' passive') if transport.connection_mode.passive|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "transport": {
                            "connection_mode": {
                                "active": "{{ not not active }}",
                                "passive": "{{ not not passive }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "transport.multi_session",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stransport\smulti-session
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport multi-session",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "transport": {"multi_session": True},
                    },
                },
            },
        },
        {
            "name": "transport.path_mtu_discovery",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stransport\spath-mtu-discovery
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport"
            "{{ (' path-mtu-discovery') if transport.path_mtu_discovery.set|d(False) else '' }}"
            "{{ (' disable') if transport.path_mtu_discovery.disable|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "transport": {
                            "path_mtu_discovery": {"set": True, "disable": "{{ not not disable }}"},
                        },
                    },
                },
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sttl-security
                (\shops(?P<ttl_security>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ttl-security"
            "{{ (' hops '+ ttl_security|string) if ttl_security is defined else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"ttl_security": "{{ ttl_security }}"}},
            },
        },
        {
            "name": "unsuppress_map",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sunsuppress-map
                (\s(?P<unsuppress_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} unsuppress-map"
            "{{ (' ' + unsuppress_map) if unsuppress_map is defined else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"unsuppress_map": "{{ unsuppress_map }}"}},
            },
        },
        {
            "name": "update_source",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\supdate-source
                (\s(?P<update_source>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} update-source"
            "{{ (' ' + update_source) if update_source is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "update_source": "{{ update_source }}",
                        "neighbor_address": "{{ neighbor_address }}",
                    },
                },
            },
        },
        {
            "name": "version",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sversion
                (\s(?P<version>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} version"
            "{{ (' ' + version|string) if version is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "version": "{{ version }}",
                    },
                },
            },
        },
        {
            "name": "weight",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sweight
                (\s(?P<weight>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} weight"
            "{{ (' ' + weight|string) if weight is defined else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"weight": "{{ weight }}"}}},
        },
        # neighbor remote-as ends
        # neighbor peer-group starts
        {
            "name": "activate",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sactivate
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' activate') if activate|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "activate": True,
                        "neighbor_address": "{{ neighbor_address }}",
                    },
                },
            },
        },
        {
            "name": "additional_paths",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadditional-paths
                (\s(?P<disable>disable))?
                (\s(?P<receive>receive))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} additional-paths"
            "{{ (' disable') if  additional_paths.disable|d(False) else '' }}"
            "{{ (' receive') if additional_paths.receive|d(False) else '' }}"
            "{{ (' send') if additional_paths.send|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "additional_paths": {
                            "disable": "{{ not not disable }}",
                            "receive": "{{ not not receive }}",
                            "send": "{{ not not send }}",
                        },
                    },
                },
            },
        },
        {
            "name": "advertise.additional_paths",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sadditional-paths
                (\s(?P<all>all))?
                (\sbest\s(?P<receive>\d+))?
                (\s(?P<group_best>group-best))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise additional-paths"
            "{{ (' all') if  advertise.additional_paths.all|d(False) else '' }}"
            "{{ (' best '+ best|string) if advertise.additional_paths.best|d(False) else '' }}"
            "{{ (' group-best') if advertise.additional_paths.group_best|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "advertise": {
                            "additional_paths": {
                                "all": "{{ not not all }}",
                                "best": "{{ receive }}",
                                "group_best": "{{ not not group_best }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertise.best_external",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sbest-external
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' advertise best-external') if  advertise.best_external|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"advertise": {"best-external": True}}},
            },
        },
        {
            "name": "advertise.diverse_path",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sdiverse-path
                (\s(?P<backup>backup))?
                (\s(?P<mpath>mpath))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise diverse-path"
            "{{ (' backup') if  advertise.diverse_path.backup|d(False) else '' }}"
            "{{ (' mpath') if advertise.diverse_path.mpath|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "advertise": {
                            "diverse_path": {
                                "backup": "{{ not not backup }}",
                                "mpath": "{{ not not mpath }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertise_map",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertise-map
                (\s(?P<name>\S+))?
                (\sexist-map\s(?P<exist_map>\S+))?
                (\snon-exist-map\s(?P<non_exist_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise-map"
            "{{ (' ' + name) if  advertise_map.name is defined else '' }}"
            "{{ (' exist-map ' + exist_map) if  advertise_map.exist_map is defined else '' }}"
            "{{ (' non-exist-map ' + non_exist_map) if advertise_map.non_exist_map is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "advertise_map": {
                            "name": "{{ name }}",
                            "exist_map": "{{ exist_map }}",
                            "non_exist_map": "{{ non_exist_map }}",
                        },
                    },
                },
            },
        },
        {
            "name": "advertisement_interval",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertisement-interval
                (\s(?P<advertisement_interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertisement-interval"
            "{{ (' ' + advertisement_interval|string) if advertisement_interval is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "advertisement_interval": "{{ advertisement_interval }}",
                    },
                },
            },
        },
        {
            "name": "aigp",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\saigp
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' aigp') if aigp.enable|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"aigp": {"enable": True}}}},
        },
        {
            "name": "aigp.send.cost_community",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\saigp\ssend\scost-community
                (\s(?P<id>\d+))\spoi
                (\s(?P<igp_cost>igp-cost))?
                (\s(?P<pre_bestpath>pre-bestpath))?
                (\s(?P<transitive>transitive))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} aigp send cost-community"
            "{{ (' ' + aigp.send.cost_community.id|string + ' poi') if  aigp.send.cost_community.id is defined else '' }}"
            "{{ (' igp-cost') if  aigp.send.cost_community.poi.igp_cost|d(False) else '' }}"
            "{{ (' pre-bestpath') if  aigp.send.cost_community.poi.pre_bestpath|d(False) else '' }}"
            "{{ (' transitive') if  aigp.send.cost_community.poi.transitive|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "aigp": {
                            "send": {
                                "cost_community": {
                                    "id": "{{ id }}",
                                    "poi": {
                                        "igp_cost": "{{ not not igp_cost }}",
                                        "pre_bestpath": "{{ not not pre_bestpath }}",
                                        "transitive": "{{ not not transitive }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "aigp.send.med",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\saigp\ssend\smed
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' aigp send med') if aigp.send.med|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"aigp": {"send": {"med": True}}}}},
        },
        {
            "name": "allow_policy",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sallow-policy
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' allow-policy') if allow_policy|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"allow_policy": True}}},
        },
        {
            "name": "allowas_in",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sallowas-in
                (\s(?P<allowas_in>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' allowas-in ' + allowas_in|string) if allowas_in is defined else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"allowas_in": "{{ allowas_in }}"}}},
        },
        {
            "name": "as_override",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' as-override') if as_override|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"as_override": True}}},
        },
        {
            "name": "bmp_activate",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sbmp-activate
                (\sserver\s(?P<server>\d+))?
                (\s(?P<all>all))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} bmp-activate"
            "{{ (' server '+ bmp_activate.server|string) if bmp_activate.server is defined else '' }}"
            "{{ (' all') if bmp_activate.all|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "bmp_activate": {"server": "{{ server }}", "all": "{{ not not  all }}"},
                    },
                },
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\scapability\sorf\sprefix-list
                (\s(?P<both>both))?
                (\s(?P<receive>receive))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} capability orf prefix-list"
            "{{ (' both') if capability.both|d(False) else '' }}"
            "{{ (' receive') if capability.receive|d(False) else '' }}"
            "{{ (' send') if capability.send|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "capability": {
                            "both": "{{ not not both }}",
                            "receive": "{{ not not receive }}",
                            "send": "{{ not not  send }}",
                        },
                    },
                },
            },
        },
        {
            "name": "default_originate",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sdefault-originate
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' default-originate') if default_originate.set|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"default_originate": {"set": True}}},
            },
        },
        {
            "name": "default_originate.route_map",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sdefault-originate
                (\sroute-map\s(?P<route_map>\S+))
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} default-originate"
            "{{ (' route-map' + default_originate.route_map) if default_originate.route_map is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "default-originate": {"route_map": "{{ route_map }}"},
                    },
                },
            },
        },
        {
            "name": "distribute_list",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sdistribute-list
                (\s(?P<acl>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} distribute-list"
            "{{ (' ' + distribute_list.acl) if distribute_list.acl is defined else '' }}"
            "{{ (' in') if distribute_list.in|d(False) else '' }}"
            "{{ (' out') if distribute_list.out|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "distribute_list": {
                            "acl": "{{ acl }}",
                            "in": "{{ not not in }}",
                            "out": "{{ not not out }}",
                        },
                    },
                },
            },
        },
        {
            "name": "dmzlink_bw",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sdmzlink-bw
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' dmzlink-bw') if dmzlink_bw|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"dmzlink_bw": True}}},
        },
        {
            "name": "filter_list",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sfilter-list
                (\s(?P<acl>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} filter-list"
            "{{ (' ' + filter_list.path_acl) if filter_list.path_acl is defined else '' }}"
            "{{ (' in') if filter_list.in|d(False) else '' }}"
            "{{ (' out') if filter_list.out|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "filter_list": {
                            "path_acl": "{{ acl }}",
                            "in": "{{ not not in }}",
                            "out": "{{ not not out }}",
                        },
                    },
                },
            },
        },
        {
            "name": "maximum_prefix",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\smaximum-prefix
                (\s(?P<max_no>\d+))
                (\s(?P<threshold_val>\d+))?
                (\srestart(?P<restart>\d+))?
                (\s(?P<warning_only>warning-only))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} maximum-prefix"
            "{{ (' ' + maximum_prefix.max_no|string) if maximum_prefix.max_no is defined else '' }}"
            "{{ (' ' + maximum_prefix.threshold_val|string) if maximum_prefix.threshold_val is defined else '' }}"
            "{{ (' restart ' + maximum_prefix.restart|string) if maximum_prefix.restart is defined else '' }}"
            "{{ (' warning-only') if maximum_prefix.warning_only|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "maximum_prefix": {
                            "max_no": "{{ max_no }}",
                            "threshold_val": "{{ threshold_val }}",
                            "restart": "{{ restart }}",
                            "warning_only": "{{ not not warning_only }}",
                        },
                    },
                },
            },
        },
        {
            "name": "next_hop_self.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\snext-hop-self
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-self') if next_hop_self.set|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"next_hop_self": {"set": True}}}},
        },
        {
            "name": "next_hop_self.all",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\snext-hop-self\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-self all') if next_hop_self.all|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"next_hop_self": {"all": True}}}},
        },
        {
            "name": "next_hop_unchanged.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-unchanged') if next_hop_unchanged.set|d(False) else ''}}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"next_hop_unchanged": {"set": True}}},
            },
        },
        {
            "name": "next_hop_unchanged.allpaths",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged\sallpaths
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-unchanged allpaths') if next_hop_unchanged.allpaths|d(False) else ''}}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"next_hop_unchanged": {"allpaths": True}}},
            },
        },
        {
            "name": "remove_private_as.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as') if remove_private_as.set|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"remove_private_as": {"set": True}}},
            },
        },
        {
            "name": "remove_private_as.all",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as all') if remove_private_as.all|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"remove_private_as": {"all": True}}},
            },
        },
        {
            "name": "remove_private_as.replace_as",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sreplace-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as replace-as') if remove_private_as.replace_as|d(False) else ''}}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"remove_private_as": {"replace_as": True}},
                },
            },
        },
        {
            "name": "route_maps",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sroute-map
                (\s(?P<route_maps>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ route_maps.neighbor_address }} route-map"
            "{{ (' ' + route_maps.name) if route_maps.name is defined else '' }}"
            "{{ (' in') if route_maps.in|d(False) else '' }}"
            "{{ (' out') if route_maps.out|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "route_maps": [
                            {
                                "name": "{{ route_maps }}",
                                "in": "{{ not not in }}",
                                "out": "{{ not not out }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "route_reflector_client",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sroute-reflector-client
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' route-reflector-client') if route_reflector_client|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                        "route_reflector_client": True,
                    },
                },
            },
        },
        {
            "name": "route_server_client.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sroute-server-client
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' route-server-client') if route_server_client.set|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"route_server_client": {"set": True}}},
            },
        },
        {
            "name": "route_server_client.context",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sroute-server-client
                (\scontext(?P<context>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} route-server-client"
            "{{ (' context ' + route_server_client.context) if route_server_client.context is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"route_server_client": {"context": "{{ context }}"}},
                },
            },
        },
        {
            "name": "send_community.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssend-community
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' send-community') if send_community.set|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"send_community": {"set": True}}}},
        },
        {
            "name": "send_community.both",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sboth
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' both') if send_community.both|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"send_community": {"both": True}}}},
        },
        {
            "name": "send_community.extended",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sextended
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' extended') if send_community.extended|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"send_community": {"extended": True}}},
            },
        },
        {
            "name": "send_community.standard",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sstandard
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' standard') if send_community.standard|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"send_community": {"standard": True}}},
            },
        },
        {
            "name": "send_label.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\ssend-label
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' send-label') if send_label.set|d(False) else '' }}",
            "result": {"neighbors": {"{{ neighbor_address }}": {"send_label": {"set": True}}}},
        },
        {
            "name": "send_label.explicit_null",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sexplicit-null
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-label"
            "{{ (' explicit-null') if send_label.explicit_null|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"send_label": {"explicit_null": True}}},
            },
        },
        {
            "name": "slow_peer.detection",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sslow-peer\sdetection
                (\s(?P<enable>enable))?
                (\s(?P<disable>disable))?
                (\sthreshold\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer detection"
            "{{ (' enable') if slow_peer.detection.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer.detection.disable|d(False) else '' }}"
            "{{ (' threshold ' + slow_peer.detection.threshold|string) if slow_peer.detection.threshold is defined else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "slow_peer": {
                            "detection": {
                                "enable": "{{ not not enable }}",
                                "disable": "{{ not not disable }}",
                                "threshold": "{{ threshold }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "slow_peer.split_update_group",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sslow-peer\ssplit-update-group
                (\s(?P<static>static))?
                (\s(?P<dynamic>dynamic))?
                (\s(?P<disable>disable))?
                (\s(?P<permanent>permanent))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer split-update-group"
            "{{ (' static') if slow_peer.split_update_group.static|d(False) else '' }}"
            "{{ (' dynamic') if slow_peer.split_update_group.dynamic.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer.split_update_group.dynamic.disable|d(False) else '' }}"
            "{{ (' permanent') if slow_peer.split_update_group.dynamic.permanent|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "slow_peer": {
                            "split_update_group": {
                                "static": "{{ not not static }}",
                                "dynamic": {
                                    "enable": "{{ not not dynamic }}",
                                    "disable": "{{ not not disable }}",
                                    "permanent": "{{ not not permanent }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "translate_update.set",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stranslate-update
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' translate_update') if translate_update.set|d(False) else '' }}",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"translate_update": {"set": True}}},
            },
        },
        {
            "name": "translate_update.nlri",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\stranslate-update\snlri
                (\s(?P<multicast>multicast))?
                (\s(?P<unicast>unicast))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} translate-update nlri"
            "{{ (' multicast') if translate_update.nlri.multicast|d(False) else '' }}"
            "{{ (' unicast') if translate_update.nlri.unicast|d(False) else '' }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "translate_update": {
                            "nlri": {
                                "multicast": "{{ not not multicast }}",
                                "unicast": "{{ not not unicast }}",
                            },
                        },
                    },
                },
            },
        },
        # neighbor peer-group ends
        # redistribute starts
        {
            "name": "application",
            "getval": re.compile(
                r"""
                \sredistribute\sapplication\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute application {{ application.name }}"
            "{{ (' metric ' + application.metric|string) if application.metric is defined else '' }}"
            "{{ (' route-map ' + application.route_map) if application.route_map is defined else '' }}",
            "remval": "redistribute application {{ application.name }}",
            "result": {
                "redistribute": [
                    {
                        "application": {
                            "name": "{{ name }}",
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "bgp",
            "getval": re.compile(
                r"""
                \sredistribute\sbgp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute bgp {{ bgp.name }}"
            "{{ (' metric ' + bgp.metric|string) if bgp.metric is defined else '' }}"
            "{{ (' route-map ' + bgp.route_map) if bgp.route_map is defined else '' }}",
            "remval": "redistribute bgp {{ bgp.name }}",
            "result": {
                "redistribute": [
                    {
                        "bgp": {
                            "name": "{{ name }}",
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "connected",
            "getval": re.compile(
                r"""
                \sredistribute\sconnected
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute connected"
            "{{ (' metric ' + connected.metric|string) if connected.metric is defined else '' }}"
            "{{ (' route-map ' + connected.route_map) if connected.route_map is defined else '' }}",
            "remval": "redistribute connected",
            "result": {
                "redistribute": [
                    {
                        "connected": {
                            "set": True,
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "eigrp",
            "getval": re.compile(
                r"""
                \sredistribute\seigrp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute eigrp {{ eigrp.name|string }}"
            "{{ (' metric ' + eigrp.metric|string) if eigrp.metric is defined else '' }}"
            "{{ (' route-map ' + eigrp.route_map) if eigrp.route_map is defined else '' }}",
            "remval": "redistribute eigrp {{ eigrp.name|string }}",
            "result": {
                "redistribute": [
                    {
                        "eigrp": {
                            "as_number": "{{ name }}",
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "isis",
            "getval": re.compile(
                r"""
                \sredistribute\sisis\s(?P<name>\S+)
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute isis {{ isis.area_tag }}"
            "{{ (' clns') if isis.clns|d(False) else '' }}"
            "{{ (' ip') if isis.ip|d(False) else '' }}"
            "{{ (' metric ' + isis.metric|string) if isis.metric is defined else '' }}"
            "{{ (' route-map ' + isis.route_map) if isis.route_map is defined else '' }}",
            "remval": "redistribute isis {{ isis.area_tag }}",
            "result": {
                "redistribute": [
                    {
                        "isis": {
                            "area_tag": "{{ name }}",
                            "clns": "{{ not not clns }}",
                            "ip": "{{ not not ip }}",
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "iso_igrp",
            "getval": re.compile(
                r"""
                \sredistribute\siso-igrp\s(?P<name>\S+)
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute iso-igrp {{ iso_igrp.area_tag }}"
            "{{ (' route-map ' + iso_igrp.route_map) if iso_igrp.route_map is defined else '' }}",
            "remval": "redistribute iso-igrp {{ iso_igrp.area_tag }}",
            "result": {
                "redistribute": [
                    {"iso_igrp": {"area_tag": "{{ name }}", "route_map": "{{ route_map }}"}},
                ],
            },
        },
        {
            "name": "lisp",
            "getval": re.compile(
                r"""
                \sredistribute\slisp
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute lisp"
            "{{ (' metric ' + lisp.metric|string) if lisp.metric is defined else '' }}"
            "{{ (' route-map ' + lisp.route_map) if lisp.route_map is defined else '' }}",
            "remval": "redistribute lisp",
            "result": {
                "redistribute": [
                    {
                        "lisp": {
                            "set": True,
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "mobile",
            "getval": re.compile(
                r"""
                \sredistribute\smobile
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute mobile"
            "{{ (' metric ' + mobile.metric|string) if mobile.metric is defined else '' }}"
            "{{ (' route-map ' + mobile.route_map) if mobile.route_map is defined else '' }}",
            "remval": "redistribute mobile",
            "result": {
                "redistribute": [
                    {
                        "mobile": {
                            "set": True,
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "odr",
            "getval": re.compile(
                r"""
                \sredistribute\sodr
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute odr"
            "{{ (' metric ' + odr.metric|string) if odr.metric is defined else '' }}"
            "{{ (' route-map ' + odr.route_map) if odr.route_map is defined else '' }}",
            "remval": "redistribute odr",
            "result": {
                "redistribute": [
                    {
                        "odr": {
                            "set": True,
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "ospf",
            "getval": re.compile(
                r"""
                \sredistribute\sospf\s(?P<process_id>\S+)
                (\s(?P<type_1>1))?
                (\s(?P<type_2>2))?
                (\s(?P<external>external))?
                (\s(?P<internal>internal))?
                (\s(?P<nssa_external>nssa-external))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospf {{ ospf.process_id }}"
            "{{ (' 1') if ospf.match.type_1|d(False) else '' }}"
            "{{ (' 2') if ospf.match.type_2|d(False) else '' }}"
            "{{ (' external') if ospf.match.external|d(False) else '' }}"
            "{{ (' internal') if ospf.match.internal|d(False) else '' }}"
            "{{ (' nssa-external') if ospf.match.nssa_external|d(False) else '' }}"
            "{{ (' metric ' + ospf.metric|string) if ospf.metric is defined else '' }}"
            "{{ (' route-map ' + ospf.route_map) if ospf.route_map is defined else '' }}"
            "{{ (' vrf ' + ospf.vrf) if ospf.vrf is defined else '' }}",
            "remval": "redistribute ospf {{ ospf.process_id }}",
            "result": {
                "redistribute": [
                    {
                        "ospf": {
                            "process_id": "{{ process_id }}",
                            "match": {
                                "type_1": "{{ not not type_1 }}",
                                "type_2": "{{ not not type_2 }}",
                                "external": "{{ not not external }}",
                                "internal": "{{ not not internal }}",
                                "nssa_external": "{{ not not nssa_external }}",
                            },
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                            "vrf": "{{ vrf }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "ospfv3",
            "getval": re.compile(
                r"""
                \sredistribute\sospfv3\s(?P<process_id>\S+)
                (\s(?P<type_1>1))?
                (\s(?P<type_2>2))?
                (\s(?P<external>external))?
                (\s(?P<internal>internal))?
                (\s(?P<nssa_external>nssa-external))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospfv3 {{ ospfv3.process_id }}"
            "{{ (' 1') if ospfv3.match.type_1|d(False) else '' }}"
            "{{ (' 2') if ospfv3.match.type_2|d(False) else '' }}"
            "{{ (' external') if ospfv3.match.external|d(False)  else '' }}"
            "{{ (' internal') if ospfv3.match.internal|d(False)  else '' }}"
            "{{ (' nssa-external') if ospfv3.match.nssa_external|d(False) else '' }}"
            "{{ (' metric ' + ospfv3.metric|string) if ospfv3.metric is defined else '' }}"
            "{{ (' route-map ' + ospfv3.route_map) if ospfv3.route_map is defined else '' }}",
            "remval": "redistribute ospfv3 {{ ospfv3.process_id }}",
            "result": {
                "redistribute": [
                    {
                        "ospfv3": {
                            "process_id": "{{ process_id }}",
                            "match": {
                                "type_1": "{{ not not type_2 }}",
                                "type_2": "{{ not not type_2 }}",
                                "external": "{{ not not external }}",
                                "internal": "{{ not not internal }}",
                                "nssa_external": "{{ not not nssa_external }}",
                            },
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "rip",
            "getval": re.compile(
                r"""
                \sredistribute\srip
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute rip"
            "{{ (' metric ' + rip.metric|string) if rip.metric is defined else '' }}"
            "{{ (' route-map ' + rip.route_map) if rip.route_map is defined else '' }}",
            "remval": "redistribute rip",
            "result": {
                "redistribute": [
                    {
                        "rip": {
                            "set": True,
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "static",
            "getval": re.compile(
                r"""
                \sredistribute\sstatic
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute static"
            "{{ (' clns') if static.clns|d(False) else '' }}"
            "{{ (' ip') if static.ip|d(False) else '' }}"
            "{{ (' metric ' + static.metric|string) if static.metric is defined else '' }}"
            "{{ (' route-map ' + static.route_map) if static.route_map is defined else '' }}",
            "remval": "redistribute static",
            "result": {
                "redistribute": [
                    {
                        "static": {
                            "set": True,
                            "clns": "{{ not not clns }}",
                            "ip": "{{ not not ip }}",
                            "metric": "{{ metric }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                \sredistribute\svrf
                (\s(?P<name>\S+))?
                (\s(?P<global>global))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute vrf {{ vrf.name }}"
            "{{ (' global') if vrf.global|d(False) else '' }}",
            "remval": "redistribute vrf {{ vrf.name }}",
            "result": {
                "redistribute": [{"vrf": {"name": "{{ name }}", "global": "{{ not not global }}"}}],
            },
        },
        # redistribute ends
    ]
