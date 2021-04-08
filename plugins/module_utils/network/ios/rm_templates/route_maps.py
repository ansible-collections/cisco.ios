# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Route_maps parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_route_map(config_data):
    pass


class Route_mapsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Route_mapsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "route_map_line",
            "getval": re.compile(
                r"""
                ^route-map*
                \s*(?P<route_map>\S+)*
                \s*(?P<action>deny|permit)*
                \s*(?P<sequence>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map,
            "result": {
                "{{ route_map }}": {
                    "route_map": "{{ route_map }}",
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "action": "{{ action }}",
                            "sequence": "{{ sequence }}",
                        }
                    },
                }
            },
            "shared": True,
        },
        {
            "name": "continue",
            "getval": re.compile(
                r"""
                \s+continue*
                \s*(?P<entry_sequence>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "continue": {
                                "set": "{{ True if entry_sequence is not defined }}",
                                "entry_sequence": "{{ entry_sequence }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description*
                \s*(?P<description>\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {"description": "{{ description }}"}
                    }
                }
            },
        },
        {
            "name": "match.additional_paths",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<additional_paths>additional-paths\sadvertise-set)*
                \s*(?P<all>all)*
                \s*(?P<best>best\s\d)*
                \s*(?P<best_range>best-range\s\d\s\d)*
                \s*(?P<group_best>group-best)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "additional_paths",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "additional_paths": {
                                    "all": "{{ True if all is defined }}",
                                    "best": "{{ best }}",
                                    "best_range": {
                                        "lower_limit": "{{ best_range.split(' ')[1] if best_range is defined }}",
                                        "upper_limit": "{{ best_range.split(' ')[2] if best_range is defined }}",
                                    },
                                    "group_best": "{{ True if group_best is defined }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<as_path>as-path.*|as-path)*
                \s*(?P<clns>clns\s(address\s\S+|next-hop\s\S+|route-source\s\S+))*
                \s*(?P<community>community\s\S+\s\S+\sexact-match|community\s\S+)*
                \s*(?P<extcommunity>extcommunity\s\S+)*
                \s*(?P<interface>interface\s\S.*)*
                \s*(?P<length>length\s\d+\s\d+)*
                \s*(?P<local_preference>local-preference\s\d.*|local-preference)*
                \s*(?P<mdt_group>mdt-group\s\S+|mdt-group)*
                \s*(?P<metric>metric\sexternal\s\d+\s(\+|-)\s\d+|metric\s\d+\s(\+|-)\s\d+|metric\sexternal\s\d+|metric\s\d+)*
                \s*(?P<mpls_label>mpls-label)*
                \s*(?P<policy_list>policy-list\s\S.*)*
                \s*(?P<rpki>rpki\s(invalid|not-found|valid))*
                \s*(?P<security_group>security-group\s(destination\stag\s\d.*|source\stag\s\d.*))*
                \s*(?P<tag>tag\slist\s\S.*|tag\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "as_path": {
                                    "set": "{{ True if as_path is defined and as_path.split(' ')|length == 1 }}",
                                    "acl": "{{ as_path.split('as-path ')[1] if as_path is defined and as_path.split(' ')|length > 1 }}",
                                },
                                "clns": {
                                    "address": "{{ clns.split('clns address ')[1] if clns is defined }}",
                                    "next_hop": "{{ clns.split('clns next-hop ')[1] if clns is defined }}",
                                    "route_source": "{{ clns.split('clns route-source ')[1] if clns is defined }}",
                                },
                                "community": {
                                    "name": "{{ community.split(' ')[1] if community is defined }}",
                                    "exact_match": "{{ community.split(' ')[2] if community is defined and 'exact-match' in community }}",
                                },
                                "extcommunity": "{{ extcommunity.split('extcommunity ')[1] if extcommunity is defined }}",
                                "interface": "{{ interface.split('interface ')[1] if interface is defined }}",
                                "length": {
                                    "minimum": "{{ length.split(' ')[1] if length is defined }}",
                                    "maximum": "{{ length.split(' ')[2] if length is defined }}",
                                },
                                "local_preference": {
                                    "set": "{{ True if local_preference is defined and local_preference.split(' ')|length == 1 }}",
                                    "value": [
                                        "{{ local_preference.split('local-preference ')[1] if local_preference is defined }}"
                                    ],
                                },
                                "mdt_group": {
                                    "set": "{{ True if mdt_group is defined and mdt_group.split(' ')|length == 1 }}",
                                    "acl": "{{ mdt_group.split('mdt-group ')[1] if mdt_group is defined }}",
                                },
                                "metric": {
                                    "external": "{{ True if metric is defined and 'external' in metric }}",
                                    "value": "{% if metric is defined and 'external' in metric %}{{ metric.split(' ')[2] }}\
                                            {% elif metric is defined and 'external' not in metric %}{{ metric.split(' ')[1] }}{% endif %}",
                                    "deviation": "{% if metric is defined and '+' in metric %}{{ 'plus' }}\
                                            {% elif metric is defined and '-' in metric %}{{ 'minus' }}{% endif %}",
                                    "deviation_value": "{% if metric is defined and 'external' in metric and ('+' in metric or '-' in metric) %}{{ metric.split(' ')[4] }}\
                                            {% elif metric is defined and 'external' not in metric and ('+' in metric or '-' in metric) %}{{ metric.split(' ')[3] }}{% endif %}",
                                },
                                "mpls_label": "{{ True if mpls_label is defined }}",
                                "policy_list": "{{ policy_list.split('policy-list ')[1] if policy_list is defined }}",
                                "rpki": {
                                    "invalid": "{{ True if rpki is defined and 'invalid' in rpki }}",
                                    "not_found": "{{ True if rpki is defined and 'not-found' in rpki }}",
                                    "valid": "{{ True if rpki is defined and 'valid' in rpki }}",
                                },
                                "security_group": {
                                    "destination": [
                                        "{{ security_group.split('destination tag ')[1] if security_group is defined and 'destination' in security_group }}"
                                    ],
                                    "source": [
                                        "{{ security_group.split('source tag ')[1] if security_group is defined and 'source' in security_group }}"
                                    ],
                                },
                                "tag": {
                                    "value": "{{ tag.split('tag ')[1] if tag is defined and 'list' not in tag }}",
                                    "list": "{{ tag.split('tag list ')[1] if tag is defined and 'list' in tag }}",
                                },
                                "track": "{{ track.split('track ')[1] if track is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<ip>ip)*
                \s*(?P<address>address\sprefix-list\s\S.*|address\s\S.*)*
                \s*(?P<flowspec>flowspec\sdest-pfx\s(prefix-list\s\S.*|\S.*)|flowspec\ssrc-pfx\s(prefix-list\s\S.*|\S.*))*
                \s*(?P<next_hop>next-hop\sprefix-list\s\S.*|next-hop\s\S.*|next-hop)*
                \s*(?P<redistribution_source>redistribution-source\sprefix-list\s\S.*|redistribution-source\s\S.*|redistribution-source)*
                \s*(?P<route_source>route-source\sredistribution-source\sprefix-list\s\S.*|route-source\sredistribution-source\s\S.*|route-source\sprefix-list\s\S.*|route-source\s\S.*|route-source\sredistribution-source|route-source)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "ip",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "ip": {
                                    "address": {
                                        "acl": [
                                            "{{ address.split('address ')[1] if address is defined and 'prefix-list' not in address else none }}"
                                        ],
                                        "prefix_list": [
                                            "{{ address.split('address prefix-list ')[1] if address is defined and 'prefix-list' in address else None }}"
                                        ],
                                    },
                                    "flowspec": {
                                        "dest_pfx": "{{ True if flowspec is defined and 'dest-pfx' in flowspec }}",
                                        "src_pfx": "{{ True if flowspec is defined and 'src-pfx' in flowspec }}",
                                        "acl": [
                                            "{{ flowspec.split('flowspec ')[1]|d() if flowspec is defined and 'prefix-list' not in flowspec else '' }}"
                                        ],
                                        "prefix_list": [
                                            "{{ flowspec.split('flowspec prefix-list ')[1]|d() if flowspec is defined and 'prefix-list' in flowspec else ''}}"
                                        ],
                                    },
                                    "next_hop": {
                                        "set": "{{ True if next_hop is defined and next_hop.split(' ')|length == 1 }}",
                                        "acl": [
                                            "{{ next_hop.split('next-hop ')[1] if next_hop is defined and 'prefix-list' not in next_hop else '' }}"
                                        ],
                                        "prefix_list": [
                                            "{{ next_hop.split('next-hop prefix-list ')[1] if next_hop is defined and 'prefix-list' in next_hop and next_hop.split('next-hop prefix-list ')[1] is not none else '' }}"
                                        ],
                                    },
                                    "redistribution_source": {
                                        "set": "{{ True if redistribution_source is defined and redistribution_source.split(' ')|length == 1 }}",
                                        "acl": [
                                            "{{ redistribution_source.split('redistribution-source ')[1]|d() if redistribution_source is defined and 'prefix-list' not in redistribution_source else '' }}"
                                        ],
                                        "prefix_list": [
                                            "{{ redistribution_source.split('redistribution-source prefix-list ')[1]|d() if redistribution_source is defined and 'prefix-list' in redistribution_source else '' }}"
                                        ],
                                    },
                                    "route_source": {
                                        "set": "{{ True if route_source is defined and route_source.split(' ')|length == 1 }}",
                                        "redistribution_source": "{{ True if route_source is defined and 'redistribution-source' in route_source }}",
                                        "acl": [
                                            "{{ route_source.split('route-source ')[1] if route_source is defined and 'prefix-list' not in route_source else '' }}"
                                        ],
                                        "prefix_list": [
                                            "{{ route_source.split('route-source prefix-list ')[1] if route_source is defined and 'prefix-list' in route_source else '' }}"
                                        ],
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<ipv6>ipv6)*
                \s*(?P<address>address\sprefix-list\s\S.*|address\s\S.*)*
                \s*(?P<flowspec>flowspec\sdest-pfx\s(prefix-list\s\S.*|\S.*)|flowspec\ssrc-pfx\s(prefix-list\s\S.*|\S.*))*
                \s*(?P<next_hop>next-hop\sprefix-list\s\S.*|next-hop\s\S.*)*
                \s*(?P<route_source>route-source\sprefix-list\s\S.*|route-source\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "ipv6",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "ipv6": {
                                    "address": {
                                        "acl": "{{ address.split('address ')[1] if address is defined and 'prefix-list' not in address }}",
                                        "prefix_list": "{{ address.split('address prefix-list ')[1] if address is defined and 'prefix-list' in address }}",
                                    },
                                    "flowspec": {
                                        "dest_pfx": "{{ True if flowspec is defined and 'dest-pfx' in flowspec }}",
                                        "src_pfx": "{{ True if flowspec is defined and 'src-pfx' in flowspec }}",
                                        "acl": "{{ flowspec.split('flowspec ')[1] if flowspec is defined and 'prefix-list' not in flowspec }}",
                                        "prefix_list": "{{ flowspec.split('flowspec prefix-list ')[1] if flowspec is defined and 'prefix-list' in flowspec }}",
                                    },
                                    "next_hop": {
                                        "acl": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and 'prefix-list' not in next_hop }}",
                                        "prefix_list": "{{ next_hop.split('next-hop prefix-list ')[1] if next_hop is defined and 'prefix-list' in next_hop }}",
                                    },
                                    "route_source": {
                                        "acl": "{{ route_source.split('route-source ')[1] if route_source is defined and 'prefix-list' not in route_source }}",
                                        "prefix_list": "{{ route_source.split('route-source prefix-list ')[1] if route_source is defined and 'prefix-list' in route_source }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.source_protocol",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<source_protocol>source-protocol)*
                \s*(?P<bgp>bgp\s\S+)*
                \s*(?P<connected>connected)*
                \s*(?P<eigrp>eigrp\s\d+)*
                \s*(?P<isis>isis)*
                \s*(?P<lisp>lisp)*
                \s*(?P<mobile>mobile)*
                \s*(?P<ospf>ospf\s\d+)*
                \s*(?P<ospfv3>ospfv3\s\d+)*
                \s*(?P<rip>rip)*
                \s*(?P<static>static)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "ipv6",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "source_protocol": {
                                    "bgp": "{{ bgp.split('bgp ')[1] if bgp is defined }}",
                                    "connected": "{{ True if connected is defined }}",
                                    "eigrp": "{{ eigrp.split('eigrp ')[1] if eigrp is defined }}",
                                    "isis": "{{ True if isis is defined }}",
                                    "lisp": "{{ True if lisp is defined }}",
                                    "mobile": "{{ True if mobile is defined }}",
                                    "ospf": "{{ ospf.split('ospf ')[1] if ospf is defined }}",
                                    "ospfv3": "{{ ospfv3.split('ospfv3 ')[1] if ospfv3 is defined }}",
                                    "rip": "{{ True if rip is defined }}",
                                    "static": "{{ True if static is defined }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<aigp_metric>aigp-metric\sigp-metric|aigp-metric\s\d+)*
                \s*(?P<as_path>as-path\s(prepend\s(last-as\s\d+|\S+)|tag))*
                \s*(?P<automatic_tag>automatic-tag)*
                \s*(?P<clns>clns\snext-hop\s\S.*)*
                \s*(?P<comm_list>comm-list\s\S+\sdelete)*
                \s*(?P<dampening>dampening\s\d+\s\d+\s\d+\s\d+)*
                \s*(?P<default>default\sinterface\s\S.*)*
                \s*(?P<extcomm_list>extcomm-list\s\S+\sdelete)*
                \s*(?P<global>global)*
                \s*(?P<interface>interface\s\S.*)*
                \s*(?P<level>level\s(level-1-2|level-1|level-2|nssa-only))*
                \s*(?P<lisp>lisp\slocator-set\s\S+)*
                \s*(?P<local_preference>local-preference\s\d+)*
                \s*(?P<metric>metric\s((\+\d+|-\d+)|(\d+\s\d+\s\d+\s\d+\s\d+|\d+)))*
                \s*(?P<metric_type>metric-type\s(external|internal|type_1|type_2))*
                \s*(?P<mpls_label>mpls-label)*
                \s*(?P<origin>origin\s(igp|incomplete))*
                \s*(?P<tag>tag\s(([0-9]{1,3}\.?){4}|\d+))*
                \s*(?P<traffic_index>traffic-index\s\d+)*
                \s*(?P<vrf>vrf\s\S+)*
                \s*(?P<weight>weight\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "aigp_metric": {
                                    "value": "{{ aigp_metric.split('as-path ')[1] if aigp_metric is defined and 'igp-metric' not in aigp_metric }}",
                                    "igp_metric": "{{ True if aigp_metric is defined and 'igp-metric' in aigp_metric }}",
                                },
                                "as_path": {
                                    "prepend": {
                                        "as_number": "{{ as_path.split('as-path prepend ')[1] if as_path is defined and 'prepend' in as_path and 'last-as' not in as_path }}",
                                        "last_as": "{{ as_path.split('as-path prepend last-as ')[1] if as_path is defined and 'prepend' in as_path and 'last-as' in as_path }}",
                                    },
                                    "tag": "{{ True if as_path is defined and 'tag' in as_path }}",
                                },
                                "automatic_tag": "{{ True if automatic_tag is defined }}",
                                "clns": "{{ clns.split('clns next-hop ')[1] if clns is defined }}",
                                "comm_list": "{{ comm_list.split(' ')[1] if comm_list is defined }}",
                                "dampening": {
                                    "penalty_half_time": "{{ dampening.split(' ')[1] if dampening is defined }}",
                                    "reuse_route_val": "{{ dampening.split(' ')[2] if dampening is defined }}",
                                    "suppress_route_val": "{{ dampening.split(' ')[3] if dampening is defined }}",
                                    "max_suppress": "{{ dampening.split(' ')[4] if dampening is defined }}",
                                },
                                "default": "{{ default.split('default interface ')[1] if default is defined }}",
                                "extcomm_list": "{{ extcomm_list.split(' ')[1] if extcomm_list is defined }}",
                                "global": "{{ True if global is defined }}",
                                "interface": "{{ interface.split('interface ')[1] if interface is defined }}",
                                "level": {
                                    "level_1": "{{ True if level is defined and 'level-1' in level and 'level-1-2' not in level }}",
                                    "level_1_2": "{{ True if level is defined and 'level-1-2' in level }}",
                                    "level_2": "{{ True if level is defined and 'level-2' in level }}",
                                    "nssa_only": "{{ True if level is defined and 'nssa-only' in level }}",
                                },
                                "lisp": "{{ lisp.split('lisp locator-set ')[1] if lisp is defined }}",
                                "local_preference": "{{ local_preference.split('local-preference ')[1] if local_preference is defined }}",
                                "metric": {
                                    # "deviation": "{%- if metric is defined and '+' in metric -%}{{ 'plus\' }}\
                                    #     {% elif metric is defined and '-' in metric %}{{ 'minus' }}{% endif %}",
                                    "metric_value": "{{ metric.split(' ')[1] if metric is defined }}",
                                    "eigrp_delay": "{{ metric.split(' ')[2] if metric is defined and metric.split(' ')|length > 2 }}",
                                    "metric_reliability": "{{ metric.split(' ')[3] if metric is defined and metric.split(' ')|length > 2 }}",
                                    "metric_bandwidth": "{{ metric.split(' ')[4] if metric is defined and metric.split(' ')|length > 2 }}",
                                    "mtu": "{{ metric.split(' ')[5] if metric is defined and metric.split(' ')|length > 2 }}",
                                },
                                "metric_type": {
                                    "external": "{{ True if metric_type is defined and 'external' in metric_type }}",
                                    "internal": "{{ True if metric_type is defined and 'internal' in metric_type }}",
                                    "type_1": "{{ True if metric_type is defined and 'type-1' in metric_type }}",
                                    "type_2": "{{ True if metric_type is defined and 'type-2' in metric_type }}",
                                },
                                "mpls_label": "{{ True if mpls_label is defined }}",
                                "origin": {
                                    "igp": "{{ True if origin is defined and 'igp' in origin }}",
                                    "incomplete": "{{ True if origin is defined and 'incomplete' in origin }}",
                                },
                                "tag": "{{ tag.split('tag ')[1] if tag is defined }}",
                                "traffic_index": "{{ traffic_index.split('traffic-index ')[1] if traffic_index is defined }}",
                                "vrf": "{{ vrf.split('vrf ')[1] if vrf is defined }}",
                                "weight": "{{ weight.split('weight ')[1] if weight is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ip",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<ip>ip)*
                \s*(?P<address>address\sprefix-list\s\S+)*
                \s*(?P<default>default)*
                \s*(?P<df>df\s\d)*
                \s*(?P<global>global\snext-hop\s(verify-availability\s([0-9]{1,3}\.?){4}\s\d+\strack\s\d+|(([0-9]{1,3}\.?){4}).*))*
                \s*(?P<precedence>precedence\s(critical|flash|flash-override|immediate|internet|network|priority|routine)|precedence)*
                \s*(?P<qos_group>qos_group\s\d+)*
                \s*(?P<tos>tos\s(max-reliability|max-throughput|min-delay|min-monetary-cost|normal)|tos)*
                \s*(?P<vrf>vrf\s\S+\snext-hop\s\S.*)*
                \s*(?P<next_hop>next-hop\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "ip",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "ip": {
                                    "address": "{{ address.split('address prefix-list ')[1] if address is defined }}",
                                    "default": "{{ True if default is defined }}",
                                    "df": "{{ df.split('df ')[1] if df is defined }}",
                                    "global": {
                                        "address": "{% if global is defined and 'verify-availability' not in global %}{{ global.split('global next-hop ')[1] }}\
                                                {% elif global is defined and 'verify-availability' in global %}{{ global.split(' ')[3] }}{% endif %}",
                                        "verify_availability": {
                                            "address": "{{ global.split(' ')[3] if global is defined and 'verify-availability' in global }}",
                                            "sequence": "{{ global.split(' ')[4] if global is defined and 'verify-availability' in global }}",
                                            "track": "{{ global.split('track ')[1] if global is defined and 'verify-availability' in global }}",
                                        },
                                    },
                                    "next_hop": {
                                        "address": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and 'peer-address' not in next_hop and 'self' not in next_hop and next_hop.split(' ')|length == 2 }}",
                                        "dynamic": "{{ True if next_hop is defined and 'dynamic dhcp' in next_hop }}",
                                        "encapsulate": "{{ next_hop.split('next-hop encapsulate l3vpn ')[1] if next_hop is defined and 'encapsulate' in next_hop }}",
                                        "peer_address": "{{ True if next_hop is defined and 'peer-address' in next_hop }}",
                                        "recursive": {
                                            "address": "{{  next_hop.split('next-hop recursive ')[1] if next_hop is defined and 'global' not in next_hop and 'vrf' not in next_hop }}",
                                            "global": "{{ next_hop.split('next-hop recursive global ')[1] if next_hop is defined and 'global' in next_hop }}",
                                            "vrf": {
                                                "name": "{{ next_hop.split(' ')[3] if next_hop is defined and 'vrf' in next_hop }}",
                                                "address": "{{ next_hop.split(' ')[4] if next_hop is defined and 'vrf' in next_hop }}",
                                            },
                                        },
                                        "self": "{{ True if next_hop is defined and 'self' in next_hop }}",
                                        "verify_availability": {
                                            "set": "{{ True if next_hop is defined and 'verify_availability' in next_hop and 'track' not in next_hop }}",
                                            "address": "{{ next_hop.split(' ')[2] if next_hop is defined and 'verify_availability' in next_hop and 'track' in next_hop }}",
                                            "sequence": "{{ next_hop.split(' ')[3] if next_hop is defined and 'verify_availability' in next_hop and 'track' in next_hop }}",
                                            "track": "{{ next_hop.split('track ')[1] if next_hop is defined and 'verify_availability' in next_hop and 'track' in next_hop }}",
                                        },
                                    },
                                    "precedence": {
                                        "set": "{{ True if precedence is defined and precedence.split(' ')|length == 1 }}",
                                        "critical": "{{ True if precedence is defined and 'critical' in precedence }}",
                                        "flash": "{{ True if precedence is defined and 'flash' in precedence }}",
                                        "flash_override": "{{ True if precedence is defined and 'flash-override' in precedence }}",
                                        "immediate": "{{ True if precedence is defined and 'immediate' in precedence }}",
                                        "internet": "{{ True if precedence is defined and 'internet' in precedence }}",
                                        "network": "{{ True if precedence is defined and 'network' in precedence }}",
                                        "priority": "{{ True if precedence is defined and 'priority' in precedence }}",
                                        "routine": "{{ True if precedence is defined and 'routine' in precedence }}",
                                        "precedence": "{{ True if precedence is defined and 'precedence' in precedence }}",
                                    },
                                    "qos_group": "{{ qos_group.split('qos-group ')[1] if qos_group is defined }}",
                                    "tos": {
                                        "set": "{{ True if tos is defined and tos.split(' ')|length == 1 }}",
                                        "max_reliability": "{{ True if tos is defined and 'max-reliability' in tos }}",
                                        "max_throughput": "{{ True if tos is defined and 'max-throughput' in tos }}",
                                        "min_delay": "{{ True if tos is defined and 'min-delay' in tos }}",
                                        "min_monetary_cost": "{{ True if tos is defined and 'min-monetary-cost' in tos }}",
                                        "normal": "{{ True if tos is defined and 'normal' in tos }}",
                                    },
                                    "vrf": {
                                        "name": "{{ vrf.split(' ')[1] if vrf is defined }}",
                                        "address": "{{ vrf.split('next-hop ')[1] if vrf is defined and 'verify-availability' not in vrf }}",
                                        "verify_availability": {
                                            "set": "{{ True if vrf is defined and 'track' not in vrf }}",
                                            "address": "{{ vrf.split(' ')[4] if vrf is defined and 'track' in vrf }}",
                                            "sequence": "{{ vrf.split(' ')[5] if vrf is defined and 'track' in vrf }}",
                                            "track": "{{ vrf.split('track ')[1] if vrf is defined and 'track' in vrf }}",
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ipv6",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<ipv6>ipv6)*
                \s*(?P<address>address\sprefix-list\s\S+)*
                \s*(?P<default>default\snext-hop\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+)*
                \s*(?P<global>global\snext-hop\sverify-availability\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+\s\d+\strack\s\d+)*
                \s*(?P<precedence>precedence\s\d+)*
                \s*(?P<vrf>vrf\s\S+\snext-hop\sverify-availability\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+\s\d+\strack\s\d+)*
                \s*(?P<next_hop>next-hop\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "compval": "ipv6",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "ip": {
                                    "address": "{{ address.split('address prefix-list ')[1] if address is defined }}",
                                    "default": "{{ default.split('default next-hop ')[1] if default is defined }}",
                                    "global": {
                                        "verify_availability": {
                                            "address": "{{ global.split(' ')[3] if global is defined and 'verify-availability' in global }}",
                                            "sequence": "{{ global.split(' ')[4] if global is defined and 'verify-availability' in global }}",
                                            "track": "{{ global.split('track ')[1] if global is defined and 'verify-availability' in global }}",
                                        }
                                    },
                                    "next_hop": {
                                        "address": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and next_hop.split(' ')|length == 2 and 'peer-address' not in next_hop }}",
                                        "encapsulate": "{{ next_hop.split('next-hop encapsulate l3vpn ')[1] if next_hop is defined and 'encapsulate' in next_hop}}",
                                        "peer_address": "{{ True if next_hop is defined and next_hop.split(' ')|length == 2 and 'peer-address' in next_hop }}",
                                        "recursive": "{{ next_hop.split('next-hop recursive ')[1] if next_hop is defined }}",
                                    },
                                    "precedence": "{{ precedence.split(' ')[1] if precedence is defined }}",
                                    "vrf": {
                                        "name": "{{ vrf.split(' ')[1] if vrf is defined }}",
                                        "verify_availability": {
                                            "address": "{{ vrf.split(' ')[4] if vrf is defined and 'verify-availability' in vrf }",
                                            "sequence": "{{ vrf.split(' ')[5] if vrf is defined and 'verify-availability' in vrf }}",
                                            "track": "{{ vrf.split('track ')[1] if vrf is defined and 'verify-availability' in vrf }}",
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
    ]
