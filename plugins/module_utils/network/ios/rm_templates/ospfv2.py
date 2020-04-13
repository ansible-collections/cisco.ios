import re

def _tmplt_ospf_vrf_cmd(process):
    command = "router ospf {id}".format(**process)
    if 'vrf' in process:
        command += ' vrf {vrf}'.format(**process)
    return command


class Ospfv2Template(object):
    PARSERS = [
        {
            'name': 'vrf',
            'getval': re.compile(r'''
                    ospf
                    *\s(?P<id>\S+)
                    \svrf
                    \s(?P<vrf>\S+)$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'id': '{{ id|int }}',
                'vrf': '{{ vrf }}'
            },
            'shared': True
        },
        {
            'name': 'id',
            'getval': re.compile(r'''
                    ospf
                    *\s
                    (?P<id>\S+)''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'id': '{{ id|int }}',
            },
            'shared': True
        },
        {
            'name': 'adjacency',
            'getval': re.compile(
                r'''\s+adjacency
                    \sstagger*
                    \s*((?P<min>\d+)|(?P<none_adj>none))*
                    \s*(?P<max>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'adjacency': {
                    'min_adjacency': '{{ min|int }}',
                    'max_adjacency': '{{ max|int }}',
                    'none': '{{ True if none_adj is defined else None }}'
                }
            }
        },
        {
            'name': 'address_family.snmp_context',
            'getval': re.compile(
                r'''\s+snmp
                    \scontext
                    \s(?P<name>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'address_family': {
                    'topology': {
                        'base': '{{ True if base is defined }}',
                        'name': '{{ name }}',
                        'tid': '{{ tid.split(' ')[1] }}'
                    }
                }
            }
        },
        {
            'name': 'address_family.topology',
            'getval': re.compile(
                r'''\s+topology
                    \s(?P<base>base)*
                    \s*(?P<name>\S+)*
                    \s*(?P<tid>tid\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'address_family': {
                    'topology': {
                        'base': '{{ True if base is defined }}',
                        'name': '{{ name }}',
                        'tid': '{{ tid.split(' ')[1] }}'
                    }
                }
            }
        },
        {
            'name': 'area.authentication',
            'getval': re.compile(
                r'''\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<auth>authentication)*
                    \s*(?P<md>message-digest)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'authentication': {
                            'enable': '{{ True if auth is defined and md is undefined }}',
                            'message_digest': '{{ not not md }}'
                        }
                    }
                }
            }
        },
        {
            'name': 'area.capapbility',
            'getval': re.compile(
                r'''\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<capability>capability)*
                    \s*(?P<df>default-exclusion)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'capability': '{{ not not capability }}'
                    }
                }
            }
        },
        {
            'name': 'area.default_cost',
            'getval': re.compile(
                r'''\s+area
                    \s(?P<area_id>\S+)*
                    \sdefault-cost*
                    \s*(?P<default_cost>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'default_cost': '{{ default_cost|int }}'
                    }
                }
            }
        },
        {
            'name': 'area.filter_list',
            'getval': re.compile(
                r'''\s+area
                    \s*(?P<area_id>\S+)*
                    \s*filter-list\sprefix*
                    \s*(?P<name>\S+)*
                    \s*(?P<dir>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'filter_list': [
                            {
                                'name': '{{ name }}',
                                'direction': '{{ dir }}',
                            },
                        ]
                    }
                }
            }
        },
        {
            'name': 'area.nssa',
            'getval': re.compile(
                r'''\s+area\s(?P<area_id>\S+)
                    \s(?P<nssa>nssa)*
                    \s*(?P<no_redis>no-redistribution)*
                    \s*(?P<def_origin>default-information-originate)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<no_summary>no-summary)*
                    \s*(?P<no_ext>no-ext-capability)*$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'nssa': {
                            'set': '{{ True if nssa is defined and def_origin is undefined and no_ext is undefined and no_redis is undefined and nssa_only is undefined }}',
                            'default_information_originate': {
                                'set': '{{ True if def_origin is defined and metric is undefined and metric_type is undefined and nssa_only is undefined }}',
                                'metric': '{{ metric.split(' ')[1]|int }}',
                                'metric_type': '{{ metric_type.split(' ')[1]|int }}',
                                'nssa_only': '{{ True if nssa_only is defined }}'
                            },
                            'no_ext_capability': '{{ True if no_ext is defined }}',
                            'no_redistribution': '{{ True if no_redis is defined }}',
                            'no_summary': '{{ True if no_summary is defined }}'
                        }
                    }
                }
            }
        },
        {
            'name': 'area.nssa.translate',
            'getval': re.compile(
                r'''\s+area\s(?P<area_id>\S+) 
                    \s(?P<nssa>nssa)*
                    \stranslate\stype7*
                    \s((?P<translate_always>always)|(?P<translate_supress>suppress-fa))
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'nssa': {
                            'set': '{{ True if nssa is defined and translate is undefined }}',
                            'translate': '{{ translate_always if translate_always is defined else translate_supress if translate_supress is defined }}'
                        }
                    }
                }
            }
        },
        {
            'name': 'area.range',
            'getval': re.compile(
                r'''\s+area\s(?P<area_id>\S+)
                    \srange
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<netmask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*((?P<advertise>advertise)|(?P<not_advertise>not-advertise))*
                    \s*(?P<cost>cost\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'range': {
                            'address': '{{ address }}',
                            'netmask': '{{ netmask }}',
                            'advertise': '{{ True if advertise is defined }}',
                            'cost': '{{ cost.split(' ')[1]|int }}',
                            'not_advertise': '{{ True if not_advertise is defined }}'
                        }
                    }
                }
            }
        },
        {
            'name': 'area.sham_link',
            'getval': re.compile(
                r'''\s+area\s(?P<area_id>\S+)
                    \ssham-link
                    \s(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<destination>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<cost>cost\s\d+)*
                    \s*(?P<ttl_security>ttl-security\shops\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'sham_link': {
                            'source': '{{ source }}',
                            'destination': '{{ destination }}',
                            'cost': '{{ cost.split(' ')[1]|int }}',
                            'ttl_security': '{{ ttl_security.split("hops ")[1] }}'
                        }
                    }
                }
            }
        },
        {
            'name': 'area.stub',
            'getval': re.compile(
                r'''\s+area\s(?P<area_id>\S+)
                    \s(?P<stub>stub)*
                    \s*(?P<no_ext>no-ext-capability)*
                    \s*(?P<no_sum>no-summary)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'areas': {
                    '{{ area_id }}': {
                        'area_id': '{{ area_id }}',
                        'stub': {
                            'set': '{{ True if stub is defined and no_ext is undefined and no_sum is undefined }}',
                            'no_ext_capability': '{{ True if no_ext is defined }}',
                            'no_summary': '{{ True if no_sum is defined }}',
                        }
                    }
                }
            }
        },
        {
            'name': 'auto_cost',
            'getval': re.compile(
                r'''\s+(?P<auto_cost>auto-cost)*
                    \s*(?P<ref_band>reference-bandwidth\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'auto_cost': {
                    'set': '{{ True if auto_cost is defined and ref_band is undefined }}',
                    'reference_bandwidth': '{{ ref_band.split(" ")[1] }}'
                }
            }
        },
        {
            'name': 'bfd',
            'getval': re.compile(
                r'''\s+bfd*
                    \s*(?P<bfd>all-interfaces)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'bfd': '{{ True if bfd is defined }}'
            }
        },
        {
            'name': 'capability',
            'getval': re.compile(
                r'''\s+capability*
                    \s*((?P<lls>lls)|(?P<opaque>opaque)|(?P<transit>transit)|(?P<vrf_lite>vrf-lite))
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'capability': {
                    'lls': '{{ True if lls is defined }}',
                    'opaque': '{{ True if opaque is defined }}',
                    'transit': '{{ True if transit is defined }}',
                    'vrf_lite': '{{ True if vrf_lite is defined }}',
                }
            }
        },
        {
            'name': 'compatible',
            'getval': re.compile(
                r'''\s+compatible*
                    \s*((?P<rfc1583>rfc1583)|(?P<rfc1587>rfc1587)|(?P<rfc5243>rfc5243))
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'compatible': {
                    'rfc1583': '{{ True if rfc1583 is defined }}',
                    'rfc1587': '{{ True if rfc1587 is defined }}',
                    'rfc5243': '{{ True if rfc5243 is defined }}',
                }
            }
        },
        {
            'name': 'default_information',
            'getval': re.compile(
                r'''\s+default-information*
                    \s*(?P<originate>originate)*
                    \s*(?P<always>always)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<route_map>route-map\s\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'default_information': {
                    'originate': '{{ True if originate is defined }}',
                    'always': '{{ True if always is defined }}',
                    'metric': '{{ metric.split(' ')[1]|int }}',
                    'metric_type': '{{ metric_type.split(' ')[1]|int }}',
                    'route_map': '{{ route_map.split(' ')[1] }}',
                }
            }
        },
        {
            'name': 'default_metric',
            'getval': re.compile(
                r'''\s+default-metric(?P<default_metric>\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'default_metric': '{{ default_metric| int}}'
            }
        },
        {
            'name': 'discard_route',
            'getval': re.compile(
                r'''\s+(?P<discard_route>discard-route)*
                    \s*(?P<external>external\s\d+)*
                    \s*(?P<internal>internal\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'discard_route': {
                    'set': '{{ True if discard_route is defined and external is undefined and internal is undefined }}',
                    'external': '{{ external.split(' ')[1]|int }}',
                    'internal': '{{ internal.split(' ')[1]|int }}',
                }
            }
        },
        {
            'name': 'distance.admin_distance',
            'getval': re.compile(
                r'''\s+distance
                    \s(?P<admin_dist>\S+)*
                    \s*(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<wildcard>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<acl>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'distance': {
                    'admin_distance': {
                        'distance': '{{ admin_dist }}',
                        'address': '{{ source }}',
                        'wildcard_bits': '{{ wildcard }}',
                        'acl': '{{ acl }}',
                    }
                }
            }
        },
        {
            'name': 'distance.ospf',
            'getval': re.compile(
                r'''\s+distance
                    \sospf*
                    \s*(?P<intra>intra-area\s\d+)*
                    \s*(?P<inter>inter-area\s\d+)*
                    \s*(?P<external>external\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'distance': {
                    'ospf': {
                        'inter_area': '{{ inter.split(' ')[1]|int }}',
                        'intra_area': '{{ intra.split(' ')[1]|int }}',
                        'external': '{{ external.split(' ')[1]|int }}',
                    }
                }
            }
        },
        {
            'name': 'distribute_list.acl',
            'getval': re.compile(
                r'''\s+distribute-list
                    \s(?P<name>\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'distribute_list': [
                    {
                        'acl': [
                            {
                                'name': '{{ name }}',
                                'direction': '{{ dir }}',
                                'interface': '{{ int_pro if dir == "in" }}',
                                'protocol': '{{ int_pro if dir == "out" }}',
                            },
                        ]
                    }
                ]
            }
        },
        {
            'name': 'distribute_list.prefix',
            'getval': re.compile(
                r'''\s+distribute-list
                    \s(?P<prefix>prefix\s\S+)*
                    \s*(?P<gateway>gateway\s\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'distribute_list': [
                    {
                        'prefix': [
                            {
                                'name': '{{ prefix.split(' ')[1] }}',
                                'gateway_name': '{{ gateway.split(' ')[1] if prefix is defined }}',
                                'direction': '{{ dir if gateway is undefined }}',
                                'interface': '{{ int_pro if dir == "in" }}',
                                'protocol': '{{ int_pro if dir == "out" }}',
                            },
                        ],
                    }
                ]
            }
        },
        {
            'name': 'distribute_list.route_map',
            'getval': re.compile(
                r'''\s+distribute-list
                    \s(?P<route_map>route-map\s\S+)*
                    \s*(?P<dir>\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'distribute_list': [
                    {
                        'route_map': {
                                'name': '{{ route_map.split(' ')[1] }}',
                                'direction': '{{ dir }}',
                        },
                    }
                ]
            }
        },
        {
            'name': 'domain_id',
            'getval': re.compile(
                r'''\s+domain-id
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<secondary>secondary)*
                    \s*(?P<null>null)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'domain_id': {
                    'ip_address': {
                        'address': '{{ address }}',
                        'secondary': '{{ True if secondary is defined }}'
                    },
                    'null': '{{ True if null is defined }}'
                }
            }
        },
        {
            'name': 'domain_tag',
            'getval': re.compile(
                r'''\s+domain-tag
                    \s(?P<tag>\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'domain_tag': '{{ tag|int }}'
            }
        },
        {
            'name': 'event_log',
            'getval': re.compile(
                r'''\s+(?P<event_log>event-log)*
                    \s*(?P<one_shot>one-shot)*
                    \s*(?P<pause>pause)*
                    \s*(?P<size>size\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'event_log': {
                    'enable': '{{ True if event_log is defined and one_shot is undefined and pause is undefined and size is undefined }}',
                    'one_shot': '{{ True if one_shot is defined }}',
                    'pause': '{{ True if pause is defined }}',
                    'size': '{{ size.split(' ')[1]|int }}'
                }
            }
        },
        {
            'name': 'help',
            'getval': re.compile(
                r'''\s+(?P<help>help)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'help': '{{ True if help is defined }}'
            }
        },
        {
            'name': 'ignore',
            'getval': re.compile(
                r'''\s+(?P<ignore>ignore)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'ignore': '{{ True if ignore is defined }}'
            }
        },
        {
            'name': 'interface_id',
            'getval': re.compile(
                r'''\s+(?P<interface_id>interface-id\ssnmp-if-index)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'interface_id': '{{ True if interface_id is defined }}'
            }
        },
        {
            'name': 'ispf',
            'getval': re.compile(
                r'''\s+(?P<ispf>ispf)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'ispf': '{{ True if ispf is defined }}'
            }
        },
        {
            'name': 'limit',
            'getval': re.compile(
                r'''\s+limit\sretransmissions
                    \s((?P<dc_num>dc\s\d+)|(?P<dc_disable>dc\sdisable))*
                    \s*((?P<non_dc_num>non-dc\s\d+)|(?P<non_dc_disable>non-dc\sdisable))
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'limit': {
                    'dc': {
                        'number': '{{ dc_num.split(' ')[1]|int }}',
                        'disable': '{{ True if dc_disable is defined }}'
                    },
                    'non_dc': {
                        'number': '{{ non_dc_num.split(' ')[1]|int }}',
                        'disable': '{{ True if dc_disable is defined }}'
                    }
                }
            }
        },
        {
            'name': 'local_rib_criteria',
            'getval': re.compile(
                r'''\s+(?P<local>local-rib-criteria)*
                    \s*(?P<forward>forwarding-address)*
                    \s*(?P<inter>inter-area-summary)*
                    \s*(?P<nssa>nssa-translation)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'local_rib_criteria': {
                    'enable': '{{ True if local is defined and forward is undefined and inter is undefined and nssa is undefined }}',
                    'forwarding_address': '{{ True if forward is defined }}',
                    'inter_area_summary': '{{ True if inter is defined }}',
                    'nssa_translation': '{{ True if nssa is defined }}',
                }
            }
        },
        {
            'name': 'log_adjacency_changes',
            'getval': re.compile(
                r'''\s+(?P<log>log-adjacency-changes)*
                    \s*(?P<detail>detail)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'log_adjacency_changes': {
                    'set': '{{ True if log is defined and detail is undefined }}',
                    'detail': '{{ True if detail is defined }}',
                }
            }
        },
        {
            'name': 'max_lsa',
            'getval': re.compile(
                r'''\s+max-lsa
                    \s(?P<number>\d+)*
                    \s*(?P<threshold>\d+)*
                    \s*(?P<ignore_count>ignore-count\s\d+)*
                    \s*(?P<ignore_time>ignore-time\s\d+)*
                    \s*(?P<reset_time>reset-time\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'max_lsa': {
                    'number': '{{ number }}',
                    'threshold_value': '{{ threshold }}',
                    'ignore_count': '{{ ignore_count.split(' ')[1] }}',
                    'ignore_time': '{{ ignore_time.split(' ')[1] }}',
                    'reset_time': '{{ reset_time.split(' ')[1] }}',
                    'warning_only': '{{ True if warning is defined }}',
                }
            }
        },
        {
            'name': 'mpls.ldp',
            'getval': re.compile(
                r'''\s+mpls
                    \sldp*
                    \s*(?P<autoconfig>autoconfig*\s*(?P<area>area\s\S+))*
                    \s*(?P<sync>sync)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'mpls': {
                    'ldp': {
                        'autoconfig': {
                            'set': '{{ True if autoconfig is defined and area is undefined }}',
                            'area': '{{ area.split(' ')[1] }}'
                        },
                        'sync': '{{ True if sync is defined }}'
                    },
                }
            }
        },
        {
            'name': 'mpls.traffic_eng',
            'getval': re.compile(
                r'''\s+mpls
                    \straffic-eng*
                    \s*(?P<area>area\s\S+)*
                    \s*(?P<autoroute>autoroute-exclude\s\S+\s\S+)*
                    \s*(?P<interface>interface\s(?P<int_type>\S+\s\S+)\s(?P<int_area>area\s\S+))*
                    \s*(?P<mesh>mesh-group\s\d+\s(?P<mesh_int>\S+\s\S+)\s(?P<mesh_area>area\s\d+))*
                    \s*(?P<multicast>multicast-intact)*
                    \s*(?P<router>router-id\s(?P<router_int>\S+\s\S+))
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'mpls': {
                    'traffic_eng': {
                        'area': '{{ area.split(' ')[1] }}',
                        'autoroute_exclude': '{{ autoroute.split(' ')[2] }}',
                        'interface': {
                            'interface_type': '{{ int_type }}',
                            'area': '{{ int_area.split(' ')[1] }}'
                        },
                        'mesh_group': {
                            'id': '{{ mesh.split(' ')[1] }}',
                            'interface': '{{ mest_int }}',
                            'area': '{{ mesh_area.split(' ')[1] }}',
                        },
                        'multicast_intact': '{{ True if multicast is defined }}',
                        'router_id_interface': '{{ router_int }}'
                    }
                }
            }
        },
        {
            'name': 'neighbor',
            'getval': re.compile(
                r'''\s+neighbor
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<cost>cost\s\d+)*
                    \s*(?P<db_filter>database-filter\sall\sout)*
                    \s*(?P<poll>poll-interval\s\d+)*
                    \s*(?P<priority>priority\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'neighbor': {
                    'address': '{{ address }}',
                    'cost': '{{ cost.split(' ')[1] }}',
                    'database_filter': '{{ True if db_filter is defined }}',
                    'poll_interval': '{{ poll.split(' ')[1] }}',
                    'priority': '{{ priority.split(' ')[1] }}'
                }
            }
        },
        {
            'name': 'network',
            'getval': re.compile(
                r'''\s+network
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<wildcard>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<area>area\s\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'network': {
                    'address': '{{ address }}',
                    'wildcard_bits': '{{ wildcard }}',
                    'area': '{{ area.split(' ')[1] }}',
                }
            }
        },
        {
            'name': 'nsf.cisco',
            'getval': re.compile(
                r'''\s+nsf
                    \s(?P<cisco>cisco)*
                    \s*(?P<helper>helper)*
                    \s*(?P<disable>disable)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'nsf': {
                    'cisco': {
                        'helper': '{{ True if helper is defined }}',
                        'disable': '{{ True if disable is defined }}',
                    }
                }
            }
        },
        {
            'name': 'nsf.ietf',
            'getval': re.compile(
                r'''\s+nsf
                    \s(?P<ietf>ietf)*
                    \s*(?P<helper>helper)*
                    \s*(?P<disable>disable)*
                    \s*(?P<strict>strict-lsa-checking)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'nsf': {
                    'ietf': {
                        'helper': '{{ True if helper is defined }}',
                        'disable': '{{ True if disable is defined }}',
                        'strict_lsa_checking': '{{ True if strict is defined }}'
                    }
                }
            }
        },
        {
            'name': 'passive_interface',
            'getval': re.compile(
                r'''\s+passive-interface
                    \s(?P<interface>\S+\s\S+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'passive_interface': '{{ interface }}',
            }
        },
        {
            'name': 'prefix_suppression',
            'getval': re.compile(
                r'''\s+(?P<prefix_sup>prefix-suppression)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'prefix_suppression': '{{ True if prefix_sup is defined }}',
            }
        },
        {
            'name': 'priority',
            'getval': re.compile(
                r'''\s+priority
                    \s(?P<priority>\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'priority': '{{ priority }}',
            }
        },
        {
            'name': 'queue_depth.hello',
            'getval': re.compile(
                r'''\s+queue-depth
                    \shello*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'queue_depth': {
                    'hello': {
                        'max_packets': '{{ max_packets }}',
                        'unlimited': '{{ True if unlimited is defined }}',
                    }
                }
            }
        },
        {
            'name': 'queue_depth.update',
            'getval': re.compile(
                r'''\s+queue-depth
                    \supdate*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'queue_depth': {
                    'update': {
                        'max_packets': '{{ max_packets }}',
                        'unlimited': '{{ True if unlimited is defined }}',
                    }
                }
            }
        },
        {
            'name': 'router_id',
            'getval': re.compile(
                r'''\s+router-id
                    \s(?P<id>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'router_id': '{{ id }}'
            }
        },
        {
            'name': 'shutdown',
            'getval': re.compile(
                r'''\s+(?P<shutdown>shutdown)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'shutdown': '{{ True if shutdown is defined }}'
            }
        },
        {
            'name': 'summary_address',
            'getval': re.compile(
                r'''\s+summary-address
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<not_adv>not-advertise)*
                    \s*(?P<nssa>nssa-only)*
                    \s*(?P<tag>tag\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'summary_address': {
                    'address': '{{ address }}',
                    'mask': '{{ mask }}',
                    'not_advertise': '{{ True if not_adv is defined }}',
                    'nssa_only': '{{ True if nssa is defined }}',
                    'tag': '{{ tag.split(' ')[1] }}'
                }
            }
        },
        {
            'name': 'timers.lsa',
            'getval': re.compile(
                r'''\s+timers
                    \slsa
                    \sarrival
                    \s(?P<lsa>\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'timers': {
                    'lsa': '{{ lsa }}'
                }
            }
        },
        {
            'name': 'timers.pacing',
            'getval': re.compile(
                r'''\s+timers
                    \spacing
                    \s(?P<flood>flood\s\d+)*
                    \s*(?P<lsa_group>lsa-group\s\d+)*
                    \s*(?P<retransmission>retransmission\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'timers': {
                    'pacing': {
                        'flood': '{{ flood.split(' ')[1] }}',
                        'lsa_group': '{{ lsa_group.split(' ')[1] }}',
                        'retransmission': '{{ retransmission.split(' ')[1] }}',
                    }
                }
            }
        },
        {
            'name': 'timers.throttle.lsa',
            'getval': re.compile(
                r'''\s+timers
                    \sthrottle
                    \s*(?P<lsa>lsa)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'timers': {
                    'throttle': {
                        'lsa': {
                            'first_delay': '{{ first_delay }}',
                            'min_delay': '{{ min_delay }}',
                            'max_delay': '{{ max_delay }}',
                        },
                    }
                }
            }
        },
        {
            'name': 'timers.throttle.spf',
            'getval': re.compile(
                r'''\s+timers
                    \sthrottle
                    \s*(?P<spf>spf)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'timers': {
                    'throttle': {
                        'spf': {
                            'receive_delay': '{{ first_delay }}',
                            'between_delay': '{{ min_delay }}',
                            'max_delay': '{{ max_delay }}',
                        },
                    }
                }
            }
        },
        {
            'name': 'traffic_share',
            'getval': re.compile(
                r'''\s+(?P<traffic>traffic-share\smin\sacross-interfaces)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'traffic_share': '{{ True if traffic is defined }}'
            }
        },
        {
            'name': 'ttl_security',
            'getval': re.compile(
                r'''\s+ttl-security
                    \s(?P<interfaces>all-interfaces)*
                    \s*(?P<hops>hops\s\d+)
                    *$''', re.VERBOSE),
            'setval': _tmplt_ospf_vrf_cmd,
            'result': {
                'ttl_security': {
                    'set': '{{ True if interfaces is defined and hops is undefined }}',
                    'hops': '{{ hops.split(' ')[1] }}'
                }
            }
        },
    ]
