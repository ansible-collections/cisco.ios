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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
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
            # "compval": "as_number",
            "setval": "router bgp {{ as_number }}",
            "result": {"as_number": "{{ as_number }}"},
            # "shared": True,
        },
        {
            "name": "aggregate_address",
            "getval": re.compile(
                r"""
                \s*aggregate-address
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
            "setval": "",
            "result": {
                "aggregate_address": [
                    {
                        "address": "{{ address }}",
                        "netmask": "{{ netmask }}",
                        "advertise_map": "{{ advertise_map }}",
                        "as_confed_set": "{{ not not as_confed_set }}",
                        "as_set": "{{ not not as_set }}",
                        "attribute_map": "{{ attribute_map }}",
                        "suppress_map": "{{ suppress_map }}",
                        "summary_only": "{{ not not summary_only }}",
                    }
                ]
            },
        },
        {
            "name": "auto_summary",
            "getval": re.compile(
                r"""
                (\s*auto-summary))?
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
                \s*bmp\sbuffer-size
                (\s(?P<buffer_size>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp buffer-size",
            "result": {"bmp": {"buffer_size": "{{ buffer_size }}"}},
        },
        {
            "name": "bmp.initial_refresh.delay",
            "getval": re.compile(
                r"""
                \s*bmp\sbuffer-size\sinitial-refresh\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp initial-refresh delay",
            "result": {"bmp": {"initial_refresh": {"delay": "{{ delay }}"}}},
        },
        {
            "name": "bmp.initial_refresh.skip",
            "getval": re.compile(
                r"""
                \s*bmp\sbuffer-size\sinitial-refresh\sdelay\sskip
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp initial-refresh skip",
            "result": {"bmp": {"initial_refresh": {"skip": True}}},
        },
        {
            "name": "bmp.initial_refresh.server",
            "getval": re.compile(
                r"""
                \s*bmp\sbuffer-size\sinitial-refresh\sserver
                (\s(?P<server>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bmp server",
            "result": {"bmp": {"initial_refresh": {"server": "{{ server }}"}}},
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""
                (\s*default-information originate)?
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
            "setval": "default-metric",
            "result": {"default_metric": "{{ default_metric }}"},
        },
        {
            "name": "distance.admin",
            "getval": re.compile(
                r"""
                \s*distance
                (\s(?P<distance>\d+))?
                (\s(?P<address>\S+))?
                (\s(?P<wildcard_bit>\S+))?
                (\s(?P<acl>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance 12 10.0.2.15 255.255.255.0",
            "result": {
                "distance": {
                    "admin": {
                        "distance": "{{ distance }}",
                        "address": "{{ access_list }}",
                        "wildcard_bit": "{{ wildcard_bit }}",
                        "acl": "{{ acl }}",
                    }
                }
            },
        },
        {
            "name": "distance.bgp",
            "getval": re.compile(
                r"""
                \s*distance\sbgp
                (\s(?P<routes_external>\d+))?
                (\s(?P<routes_internal>\d+))?
                (\s(?P<routes_local>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance bgp 2 12 23",
            "result": {
                "distance": {
                    "bgp": {
                        "routes_external": "{{ routes_external }}",
                        "routes_internal": "{{ routes_internal }}",
                        "routes_local": "{{ routes_local }}",
                    }
                }
            },
        },
        {
            "name": "distance.mbgp",
            "getval": re.compile(
                r"""
                \s*distance\smbgp
                (\s(?P<routes_external>\d+))?
                (\s(?P<routes_internal>\d+))?
                (\s(?P<routes_local>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance mbgp 2 12 23",
            "result": {
                "distance": {
                    "mbgp": {
                        "routes_external": "{{ routes_external }}",
                        "routes_internal": "{{ routes_internal }}",
                        "routes_local": "{{ routes_local }}",
                    }
                }
            },
        },
        {
            "name": "distribute_lists",
            "getval": re.compile(
                r"""
                \s*distribute-list
                (\sprefix\s(?P<prefix>\S+))?
                (\sgateway\s(?P<gateway>\S+))?
                (\s(?P<acl>\S+))?
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                (\s(?P<interface>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distribute-list prefix workcheck out",
            "result": {
                "distribute_lists": [
                    {
                        "prefix": "{{ prefix }}",
                        "gateway": "{{ gateway }}",
                        "acl": "{{ acl }}",
                        "in": "{{ not not in }}",
                        "out": "{{ not not out }}",
                        "interface": "{{ interface }}",
                    }
                ]
            },
        },
        {
            "name": "maximum_paths.paths",
            "getval": re.compile(
                r"""
                \s*maximum-paths
                (\s(?P<paths>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths 2",
            "result": {"maximum_paths": {"paths": "{{ paths }}"}},
        },
        {
            "name": "maximum_paths.eibgp",
            "getval": re.compile(
                r"""
                \s*maximum-paths\seibgp
                (\s(?P<eibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths eibgp 2",
            "result": {"maximum_paths": {"eibgp": "{{ eibgp }}"}},
        },
        {
            "name": "maximum_paths.ibgp",
            "getval": re.compile(
                r"""
                \s*maximum-paths\sibgp
                (\s(?P<ibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths ibgp 2",
            "result": {"maximum_paths": {"ibgp": "{{ ibgp }}"}},
        },
        {
            "name": "maximum_secondary_paths.paths",
            "getval": re.compile(
                r"""
                \s*maximum-secondary-paths
                (\s(?P<paths>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-secondary-paths 2",
            "result": {"maximum_secondary_paths": {"paths": "{{ paths }}"}},
        },
        {
            "name": "maximum_secondary_paths.eibgp",
            "getval": re.compile(
                r"""
                \s*maximum-secondary-paths\seibgp
                (\s(?P<eibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths eibgp 2",
            "result": {"maximum_secondary_paths": {"eibgp": "{{ eibgp }}"}},
        },
        {
            "name": "maximum_secondary_paths.ibgp",
            "getval": re.compile(
                r"""
                \s*maximum-secondary-paths\sibgp
                (\s(?P<ibgp>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-secondary-paths ibgp 2",
            "result": {"maximum_secondary_paths": {"ibgp": "{{ ibgp }}"}},
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s*network
                (\s(?P<address>\S+))?
                (\smask\s(?P<netmask>\S+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\s(?P<backdoor>backdoor))?
                $""",
                re.VERBOSE,
            ),
            "setval": "network 51.0.0.0 mask 255.255.0.0 route-map map2 backdoor",
            "result": {
                "network": [
                    {
                        "address": "{{ address }}",
                        "netmask": "{{ netmask }}",
                        "route_map": "{{ route_map }}",
                        "backdoor": "{{ not not backdoor }}",
                    }
                ]
            },
        },
        {
            "name": "route_server_context.name",
            "getval": re.compile(
                r"""
                \s*route-server-context
                (\s(?P<name>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "route-server-context namer",
            "result": {"route_server_context": {"name": "{{ name }}"}},
        },
        {
            "name": "route_server_context.address_family",
            "getval": re.compile(
                r"""
                \s*address-family
                (\s(?P<afi>ipv4|ipv6))?
                (\s(?P<modifier>multicast|unicast))?
                (\simport-map\s(?P<import_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "route-server-context namer\ntest(config-router-rsctx)#address-family ipv6 unicast ?",
            "result": {
                "route_server_context": {
                    "address_family": {
                        "afi": "{{ afi }}",
                        "modifier": "{{ modifier }}",
                        "import_map": "{{ import_map }}",
                    }
                }
            },
        },
        {
            "name": "route_server_context.description",
            "getval": re.compile(
                r"""
                \s*description
                (\s(?P<description>.+$))?
                """,
                re.VERBOSE,
            ),
            "setval": "route-server-context namer\ntest(config-router-rsctx)#descirption LINE",
            "result": {"route_server_context": {"description": "{{ description }}"}},
        },
        {
            "name": "synchronization",
            "getval": re.compile(
                r"""\s*(?P<synchronization>synchronization)""", re.VERBOSE
            ),
            "setval": "synchronization",
            "result": {"synchronization": "{{ not not synchronization }}"},
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""
                \s*table-map
                (\s(?P<name>\S+))?
                (\s(?P<filter>filter))?
                $""",
                re.VERBOSE,
            ),
            "setval": "table-map newtbmap filter",
            "result": {
                "table_map": {"name": "{{ name }}", "filter": "{{ not not filter }}"}
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \s*timers\sbgp
                (\s(?P<keepalive>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers bgp 3 4 5 ",
            "result": {
                "timers": {
                    "keepalive": "{{ keepalive }}",
                    "holdtime": "{{ holdtime }}",
                    "min_holdtime": "{{ min_holdtime }}",
                }
            },
        },
        # bgp starts
        {
            "name": "bgp.additional_paths",
            "getval": re.compile(
                r"""
                \s*bgp\sadditional-paths
                (\s(?P<install>install))?
                (\s(?P<receive>receive))?
                (\s(?P<select>select))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths receive",
            "result": {
                "bgp": {
                    "additional_paths": {
                        "install": "{{ not not install }}",
                        "receive": "{{ not not receive }}",
                        "select": "{{ not not select }}",
                        "send": "{{ not not send }}",
                    }
                }
            },
        },
        {
            "name": "bgp.advertise_best_external",
            "getval": re.compile(r"""\s*(bgp advertise-best-external)""", re.VERBOSE),
            "setval": "bgp advertise-best-external",
            "result": {"bgp": {"additional_paths": True}},
        },
        {
            "name": "bgp.aggregate_timer",
            "getval": re.compile(
                r"""
                \s*bgp\saggregate-timer
                (\s(?P<aggregate_timer>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp aggregate-timer 0",
            "result": {"bgp": {"aggregate_timer": "{{ aggregate_timer }}"}},
        },
        {
            "name": "bgp.always_compare_med",
            "getval": re.compile(r"""\s*(bgp\salways-compare-med)""", re.VERBOSE),
            "setval": "bgp always-compare-med",
            "result": {"bgp": {"always_compare_med": True}},
        },
        {
            "name": "bgp.asnotation",
            "getval": re.compile(r"""\s*(bgp\sasnotation\sdot)""", re.VERBOSE),
            "setval": "bgp asnotation dot",
            "result": {"bgp": {"asnotation": True}},
        },
        {
            "name": "bgp.bestpath.aigp",
            "getval": re.compile(r"""\s*(bgp\sbestpath\saigp\signore)""", re.VERBOSE),
            "setval": "bgp bestpath aigp ignore",
            "result": {"bgp": {"bestpath": {"aigp": True}}},
        },
        {
            "name": "bgp.bestpath.compare_routerid",
            "getval": re.compile(
                r"""\s*(bgp\sbestpath\scompare-routerid)""", re.VERBOSE
            ),
            "setval": "bgp bestpath compare-routerid",
            "result": {"bgp": {"bestpath": {"compare_routerid": True}}},
        },
        {
            "name": "bgp.bestpath.cost_community",
            "getval": re.compile(
                r"""\s*(bgp\sbestpath\scost-community\signore)""", re.VERBOSE
            ),
            "setval": "bgp bestpath cost-community ignore",
            "result": {"bgp": {"bestpath": {"cost_community": True}}},
        },
        {
            "name": "bgp.bestpath.igp_metric",
            "getval": re.compile(
                r"""\s*(bgp\sbestpath\sigp-metric\signore)""", re.VERBOSE
            ),
            "setval": "bgp bestpath igp-metric ignore",
            "result": {"bgp": {"bestpath": {"igp_metric": True}}},
        },
        {
            "name": "bgp.bestpath.med",
            "getval": re.compile(
                r"""
                \s*bgp\sbestpath\smed
                (\s(?P<confed>confed))?
                (\s(?P<missing_as_worst>missing-as-worst))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp bestpath med confed missing-as-worst",
            "result": {
                "bgp": {
                    "bestpath": {
                        "med": {
                            "confed": "{{ not not confed }}",
                            "missing_as_worst": "{{ not not missing_as_worst }}",
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.client_to_client",
            "getval": re.compile(
                r"""
                \s*bgp\sclient-to-client
                (\s(?P<set>reflection))?
                (\s(?P<all>all))?
                (\sintra-cluster\scluster-id\s(?P<intra_cluster>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp client-to-client reflection intra-cluster cluster-id any",
            "result": {
                "bgp": {
                    "client_to_client": {
                        "set": "{{ not not set }}",
                        "all": "{{ not not all }}",
                        "intra_cluster": "{{ intra_cluster }}",
                    }
                }
            },
        },
        {
            "name": "bgp.cluster_id",
            "getval": re.compile(
                r"""
                \s*bgp\scluster-id
                (\s(?P<cluster_id>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp cluster-id 12",
            "result": {"bgp": {"cluster_id": "{{ not not cluster_id }}"}},
        },
        {
            "name": "bgp.confederation.peer",
            "getval": re.compile(
                r"""
                \s*bgp\sconfederation\speer
                (\s(?P<peer>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp confederation peers 222",
            "result": {"bgp": {"confederation": {"peer": "{{ not not peer }}"}}},
        },
        {
            "name": "bgp.confederation.identifier",
            "getval": re.compile(
                r"""
                \s*bgp\sconfederation\sidentifier
                (\s(?P<identifier>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp confederation identifier 2222",
            "result": {
                "bgp": {"confederation": {"identifier": "{{ not not identifier }}"}}
            },
        },
        {
            "name": "bgp.consistency_checker.auto_repair",
            "getval": re.compile(
                r"""
                \s*bgp\sconsistency-checker\sauto-repair
                (\sinterval\s(?P<interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp consistency-checker auto-repair interval 7",
            "result": {
                "bgp": {
                    "consistency_checker": {
                        "auto_repair": {"set": True, "interval": "{{ interval }}"}
                    }
                }
            },
        },
        {
            "name": "bgp.consistency_checker.error_message",
            "getval": re.compile(
                r"""
                \s*bgp\sconsistency-checker\serror-message
                (\sinterval\s(?P<interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp consistency-checker error-message interval 7",
            "result": {
                "bgp": {
                    "consistency_checker": {
                        "error_message": {"set": True, "interval": "{{ interval }}"}
                    }
                }
            },
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""
                \s*bgp\sdampening
                (\s(?P<penalty_half_time>\d+))?
                (\s(?P<reuse_route_val>\d+))?
                (\s(?P<suppress_route_val>\d+))?
                (\s(?P<max_suppress>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp dampening 2 3 4 5",
            "result": {
                "bgp": {
                    "dampening": {
                        "penalty_half_time": "{{ penalty_half_time }}",
                        "reuse_route_val": "{{ reuse_route_val }}",
                        "suppress_route_val": "{{ suppress_route_val }}",
                        "max_suppress": "{{ max_suppress }}",
                        "route_map": "{{ route_map }}",
                    }
                }
            },
        },
        {
            "name": "bgp.deterministic_med",
            "getval": re.compile(r"""\s*(bgp\sdeterministic-med)""", re.VERBOSE),
            "setval": "bgp deterministic-med",
            "result": {"bgp": {"deterministic_med": True}},
        },
        {
            "name": "bgp.dmzlink_bw",
            "getval": re.compile(r"""\s*(bgp\sdmzlink-bw)""", re.VERBOSE),
            "setval": "bgp dmzlink-bw",
            "result": {"bgp": {"dmzlink_bw": True}},
        },
        {
            "name": "bgp.enforce_first_as",
            "getval": re.compile(r"""\s*(bgp\senforce-first-as)""", re.VERBOSE),
            "setval": "bgp enforce-first-as",
            "result": {"bgp": {"enforce_first_as": True}},
        },
        {
            "name": "bgp.enhanced_error",
            "getval": re.compile(r"""\s*(bgp\senhanced-error)""", re.VERBOSE),
            "setval": "bgp enhanced-error",
            "result": {"bgp": {"enhanced_error": True}},
        },
        {
            "name": "bgp.fast_external_fallover",
            "getval": re.compile(r"""\s*(bgp\sfast-external-fallover)""", re.VERBOSE),
            "setval": "bgp fast-external-fallover",
            "result": {"bgp": {"fast_external_fallover": True}},
        },
        {
            "name": "bgp.graceful_restart.set",
            "getval": re.compile(
                r"""
                \s*bgp\sgraceful-restart
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
                \s*bgp\sgraceful-restart\sextended
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
                \s*bgp\sgraceful-restart\srestart-time
                (\s(?P<restart_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart restart-time 10",
            "result": {
                "bgp": {"graceful_restart": {"restart_time": "{{ restart_time }}"}}
            },
        },
        {
            "name": "bgp.graceful_restart.stalepath_time",
            "getval": re.compile(
                r"""
                \s*bgp\sgraceful-restart\sstalepath-time
                (\s(?P<stalepath_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-restart stalepath-time 10",
            "result": {
                "bgp": {"graceful_restart": {"stalepath_time": "{{ stalepath_time }}"}}
            },
        },
        {
            "name": "bgp.graceful_shutdown",
            "getval": re.compile(
                r"""
                \s*bgp\sgraceful-shutdown\sall
                (\s(?P<placeholder>neighbors|vrfs))?
                (\s(?P<time>\d+))?
                (\s(?P<activate>activate))?
                (\slocal-preference\s(?P<local_preference>\d+))?
                (\scommunity\s(?P<community>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp graceful-shutdown all neighbors 31 local-preference 23 community 22",
            "result": {
                "bgp": {
                    "graceful_shutdown": {
                        "{{ placeholder }}": {
                            "time": "{{ time }}",
                            "activate": "{{ not not activate }}",
                        },
                        "community": "{{ community }}",
                        "local_preference": "{{ local_preference }}",
                    }
                }
            },
        },
        {
            "name": "bgp.inject_map",
            "getval": re.compile(
                r"""
                \s*bgp\sinject-map
                (\s(?P<name>\S+))?
                (\sexist-map\s(?P<exist_map_name>\S+))?
                (\s(?P<copy_attributes>copy-attributes))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp inject-map map2 exist-map mp3 copy-attributes",
            "result": {
                "bgp": {
                    "inject_map": [
                        {
                            "name": "{{ name }}",
                            "exist_map_name": "{{ exist_map_name }}",
                            "copy_attributes": "{{ not not copy_attributes }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "bgp.listen.limit",
            "getval": re.compile(
                r"""
                \s*bgp\slisten\slimit
                (\s(?P<limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp listen limit 200",
            "result": {"bgp": {"listen": {"limit": "{{ limit }}"}}},
        },
        {
            "name": "bgp.listen.range",
            "getval": re.compile(
                r"""
                \s*bgp\slisten\srange
                (\s(?P<host_with_subnet>\S+))?
                (\speer_group\s(?P<peer_group>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": " bgp listen range 2001:DB8:ABCD:12::/64 peer-group bhak bgp listen range 10.0.2.0/24 peer-group mygrp",
            "result": {
                "bgp": {
                    "listen": {
                        "range": {
                            "host_with_subnet": "{{ host_with_subnet }}",
                            "peer_group": "{{ peer_group }}",
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.log_neighbor_changes",
            "getval": re.compile(r"""\s*(bgp\slog-neighbor-changes)""", re.VERBOSE),
            "setval": "bgp log-neighbor-changes",
            "result": {"bgp": {"log_neighbor_changes": True}},
        },
        {
            "name": "bgp.maxas_limit",
            "getval": re.compile(
                r"""
                \s*bgp\smaxas-limit
                (\s(?P<maxas_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxas_limit 200",
            "result": {"bgp": {"maxas_limit": "{{ maxas_limit }}"}},
        },
        {
            "name": "bgp.maxcommunity_limit",
            "getval": re.compile(
                r"""
                \s*bgp\smaxcommunity-limit
                (\s(?P<maxcommunity_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxcommunity-limit 200",
            "result": {"bgp": {"maxcommunity_limit": "{{ maxcommunity_limit }}"}},
        },
        {
            "name": "bgp.maxextcommunity_limit",
            "getval": re.compile(
                r"""
                \s*bgp\smaxextcommunity-limit
                (\s(?P<maxextcommunity_limit>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp maxextcommunity-limit 200",
            "result": {"bgp": {"maxextcommunity_limit": "{{ maxextcommunity_limit }}"}},
        },
        {
            "name": "bgp.nexthop.route_map",
            "getval": re.compile(
                r"""
                \s*bgp\snexthop\sroute-map
                (\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop route-map map1",
            "result": {"bgp": {"nexthop": {"route_map": "{{ route_map }}"}}},
        },
        {
            "name": "bgp.nexthop.trigger.delay",
            "getval": re.compile(
                r"""
                \s*bgp\snexthop\strigger\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger delay 2",
            "result": {"bgp": {"nexthop": {"trigger": {"delay": "{{ delay }}"}}}},
        },
        {
            "name": "bgp.nexthop.trigger.enable",
            "getval": re.compile(
                r"""
                \s*bgp\snexthop\strigger\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger enable",
            "result": {"bgp": {"nexthop": {"trigger": {"enable": True}}}},
        },
        {
            "name": "bgp.nopeerup_delay.cold_boot",
            "getval": re.compile(
                r"""
                \s*bgp\snopeerup-delay\scold-boot
                (\s(?P<cold_boot>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay cold-boot 2",
            "result": {"bgp": {"nopeerup_delay": {"cold_boot": "{{ cold_boot }}"}}},
        },
        {
            "name": "bgp.nopeerup_delay.post_boot",
            "getval": re.compile(
                r"""
                \s*bgp\snopeerup-delay\spost-boot
                (\s(?P<post_boot>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay post-boot 22",
            "result": {"bgp": {"nopeerup_delay": {"post_boot": "{{ post_boot }}"}}},
        },
        {
            "name": "bgp.nopeerup_delay.nsf_switchover",
            "getval": re.compile(
                r"""
                \s*bgp\snopeerup-delay\snsf-switchover
                (\s(?P<nsf_switchover>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay nsf-switchover 10",
            "result": {
                "bgp": {"nopeerup_delay": {"nsf_switchover": "{{ nsf_switchover }}"}}
            },
        },
        {
            "name": "bgp.nopeerup_delay.user_initiated",
            "getval": re.compile(
                r"""
                \s*bgp\snopeerup-delay\suser-initiated
                (\s(?P<user_initiated>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nopeerup-delay user-initiated 22",
            "result": {
                "bgp": {"nopeerup_delay": {"user_initiated": "{{ user_initiated }}"}}
            },
        },
        {
            "name": "bgp.recursion",
            "getval": re.compile(
                r"""
                \s*bgp\srecursion\shost
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
                \s*bgp\sredistribute-internal
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
                \s*bgp\srefresh\smax-eor-time
                (\s(?P<max_eor_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp refresh max-eor-time 700",
            "result": {"bgp": {"refresh": {"max_eor_time": "{{ max_eor_time }}"}}},
        },
        {
            "name": "bgp.refresh.stalepath_time",
            "getval": re.compile(
                r"""
                \s*bgp\srefresh\sstalepath-time
                (\s(?P<stalepath_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp refresh stalepath-time 700",
            "result": {"bgp": {"refresh": {"stalepath_time": "{{ stalepath_time }}"}}},
        },
        {
            "name": "bgp.regexp",
            "getval": re.compile(
                r"""
                \s*bgp\sregexp\sdeterministic
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp regexp deterministic ",
            "result": {"bgp": {"regexp": True}},
        },
        {
            "name": "bgp.router_id",
            "getval": re.compile(
                r"""
                \s*bgp\srouter-id
                (\s(?P<address>\S+))?
                (\sinterface\s(?P<interface>\S+))?
                (\svrf\s(?P<vrf>auto-assign))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp router-id vrf auto-assign or IP here",
            "result": {
                "bgp": {
                    "router_id": {
                        "address": "{{ address }}",
                        "interface": "{{ interface }}",
                        "vrf": "{{ not not vrf }}",
                    }
                }
            },
        },
        {
            "name": "bgp.scan_time",
            "getval": re.compile(
                r"""
                \s*bgp\sscan-time
                (\s(?P<scan_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp scan-time 22",
            "result": {"bgp": {"scan_time": "{{ scan_time }}"}},
        },
        {
            "name": "bgp.slow_peer.detection.set",
            "getval": re.compile(
                r"""
                \s*bgp\sslow-peer\sdetection
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
                \s*bgp\sslow-peer\sdetection\sthreshold
                (\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer detection threshold 345",
            "result": {
                "bgp": {"slow_peer": {"detection": {"threshold": "{{ threshold }}"}}}
            },
        },
        {
            "name": "bgp.slow_peer.split_update_group",
            "getval": re.compile(
                r"""
                \s*bgp\sslow-peer\ssplit-update-group
                (\s(?P<dynamic>dynamic))?
                (\s(?P<permanent>permanent))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group dynamic permanent",
            "result": {
                "bgp": {
                    "slow_peer": {
                        "split_update_group": {
                            "dynamic": "{{ dynamic }}",
                            "permanent": "{{ permanent }}",
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.snmp",
            "getval": re.compile(
                r"""
                \s*bgp\ssnmp\straps\sadd-type
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
                \s*bgp\ssso\sroute-refresh-enable
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
                \s*bgp\ssoft-reconfig-backup
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
                \s*bgp\ssuppress-inactive
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
                \s*bgp\stransport\spath-mtu-discovery
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
                \s*bgp\supdate-delay
                (\s(?P<update_delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp update-delay 2",
            "result": {"bgp": {"update_delay": "{{ update_delay }}"}},
        },
        {
            "name": "bgp.update_group",
            "getval": re.compile(
                r"""
                \s*bgp\supdate-group\ssplit\sas-override
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
                \s*bgp\supgrade-cli
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
                \s*bgp\supgrade-cli\saf-mode
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp upgrade-cli af-mode",
            "result": {"bgp": {"update_group": {"af_mode": True}}},
        },
        # bgp ends
        # neighbor starts
        {
            "name": "neighbors.remote_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sremote-as\s(?P<remote_as>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 remote-as 650",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "remote_as": "{{ remote_as }}",
                        "neighbor_address": "{{ neighbor_address }}",
                    }
                }
            },
        },
        {
            "name": "neighbors.peer_group",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \speer-group\s(?P<peer_group>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 peer-group 650",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "peer_group": "{{ peer_group }}",
                        "neighbor_address": "{{ neighbor_address }}",
                    }
                }
            },
        },
        {
            "name": "neighbors.bmp_activate",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<bmp_activate>bmp-activate)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 bmp-activate",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "bmp_activate": "{{ not not bmp_activate }}"
                    }
                }
            },
        },
        {
            "name": "neighbors.cluster_id",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<cluster_id>cluster-id)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 cluster-id",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"cluster_id": "{{ not not cluster_id }}"}
                }
            },
        },
        {
            "name": "neighbors.description",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<description>description)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 description",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "description": "{{ not not description }}"
                    }
                }
            },
        },
        {
            "name": "neighbors.disable_connected_check",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<disable_connected_check>disable-connected-check)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 disable-connected-check",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "disable_connected_check": "{{ not not disable_connected_check }}"
                    }
                }
            },
        },
        {
            "name": "neighbors.ebgp_multihop",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<enable>ebgp_multihop)
                (\s(?P<hop_count>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 ebgp-multihop 2",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "ebgp_multihop": {
                            "enable": "{{ not not enable }}",
                            "hop_count": "{{ hop_count }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.fall_over.bfd",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sfall-over
                \s(?P<set>bfd)
                (\s(?P<multi_hop>multi-hop))?
                (\s(?P<single_hop>single-hop))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 fall-over bfd",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "fall_over": {
                            "bfd": {
                                "set": "{{ not not set }}",
                                "multi_hop": "{{ not not multi_hop }}",
                                "single_hop": "{{ not not single_hop }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.fall_over.route_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sroute-map
                \s(?P<route_map>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 route_map map2",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "fall_over": {"route_map": "{{ not not route_map }}"}
                    }
                }
            },
        },
        {
            "name": "neighbors.ha_mode",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sha-mode
                \s(?P<set>graceful-restart)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 ha-mode graceful-restart",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "ha_mode": {
                            "set": "{{ not not set }}",
                            "disable": "{{ not not disable }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.inherit",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sinherit\speer-session
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 inherit peer-session newsession",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"inherit": "{{ inherit }}"}}
            },
        },
        {
            "name": "neighbors.local_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\s(?P<local_as>local-as)
                (\s(?P<number>\S+))?
                (\s(?P<dual_as>dual-as))?
                (\s(?P<no_prepend>no-prepend))?
                (\s(?P<replace_as>replace-as))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 local-as 65444 no-prepend",
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
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.log_neighbor_changes",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<set>log-neighbor-changes)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 log-neighbor-changes disable",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "log_neighbor_changes": {
                            "set": "{{ not not set }}",
                            "disable": "{{ not not disable }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.password",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\spassword
                \s(?P<encryption>\d+)
                (\s(?P<pass_key>.$))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.1.1 password 5 my pass",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "password": {
                            "encryption": "{{ encryption }}",
                            "pass_key": "{{ pass_key }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.path_attribute",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\spath-attribute
                (\s(?P<attr>)discard|treat-as-withdraw)?
                (\s(?P<type>\d+))?
                (\srange\s(?P<start>\d+)\s(?P<end>\d+))?
                (\s(?P<in>in))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 path-attribute discard range 23 50 in",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "path_attribute": {
                            "{{ 'discard' if attr=='discard' else 'treat_as_withdraw' }}": {
                                "type": "{{ type }}",
                                "range": {"start": "{{ start }}", "end": "{{ end }}"},
                                "in": "{{ not not in }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.shutdown",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sshutdown
                (\sgraceful(?P<graceful>)\d+)?
                (\scommunity(?P<community>\d+))?
                (\s(?P<local_preference>local-preference))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 shutdown graceful 31 community 22",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "shutdown": {
                            "set": True,
                            "graceful": "{{ graceful }}",
                            "community": "{{ community }}",
                            "local_preference": "{{ not not local_preference }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.soft_reconfiguration",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssoft-reconfiguration
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 soft-reconfiguration",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"soft_reconfiguration": True}}
            },
        },
        {
            "name": "neighbors.timers",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stimers
                (\s(?P<interval>)\d+)?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 timers 23 5534 22",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "timers": {
                            "interval": "{{ interval }}",
                            "holdtime": "{{ holdtime }}",
                            "min_holdtime": "{{ min_holdtime }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.transport.connection_mode",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\sconnection-mode
                (\s(?P<active>)active)?
                (\s(?P<passive>passive))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 transport connection-mode active",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "transport": {
                            "connection_mode": {
                                "active": "{{ not not active }}",
                                "passive": "{{ not not passive }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.transport.multi_session",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\smulti-session
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 transport multi-session",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"transport": {"multi_session": True}}
                }
            },
        },
        {
            "name": "neighbors.transport.path_mtu_discovery",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\spath-mtu-discovery
                (\s(?P<disable>)disable)?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 transport path-mtu-discovery disable",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "transport": {
                            "path_mtu_discovery": {
                                "set": True,
                                "disable": "{{ not not disable }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "neighbors.ttl_security",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sttl-security
                (\shops(?P<ttl_security>)\d+)?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 ttl-security hops 22",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"ttl_security": "{{ ttl_security }}"}
                }
            },
        },
        {
            "name": "neighbors.unsuppress_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sunsuppress-map
                (\s(?P<unsuppress_map>)\S+)?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 unsuppress-map maphere",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {"unsuppress_map": "{{ unsuppress_map }}"}
                }
            },
        },
        {
            "name": "neighbors.version",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sversion
                (\s(?P<version>)\d+)?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 version 2",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"version": "{{ version }}"}}
            },
        },
        {
            "name": "neighbors.weight",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sweight
                (\s(?P<weight>)\d+)?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor 10.0.2.14 weight 2",
            "result": {
                "neighbors": {"{{ neighbor_address }}": {"weight": "{{ weight }}"}}
            },
        },
        # neighbor ends
        {
            "name": "neighbors.remote_asTempalte",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sremote-as(?P<remote_as>\S+)
                (\s(?P<keepalive>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers bgp 3 4 5 ",
            "result": {
                "timers": {
                    "keepalive": "{{ keepalive }}",
                    "holdtime": "{{ holdtime }}",
                    "min_holdtime": "{{ min_holdtime }}",
                }
            },
        },
    ]
