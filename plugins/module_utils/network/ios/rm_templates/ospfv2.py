from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def _tmplt_ospf_address_family_cmd(config_data):
    if "address_family" in config_data:
        command = ["address-family ipv4 multicast", "exit-address-family"]
        if config_data["address_family"].get("topology"):
            if "base" in config_data["address_family"].get("topology"):
                command.insert(1, "topology base")
            elif "name" in config_data["address_family"].get("topology"):
                cmd = "topology {name}".format(**config_data["address_family"].get("topology"))
                if "tid" in config_data["address_family"].get("topology"):
                    cmd += " tid {tid}".format(**config_data["address_family"].get("topology"))
                command.insert(1, cmd)
        return command


def _tmplt_ospf_area_filter(config_data):
    filter_list = config_data.get("filter_list", {})
    command = []
    for value in filter_list.values():
        name = value.get("name")
        direction = value.get("direction")
        
        if name and direction:
            cmd = "area {area_id} filter-list prefix {name} {direction}".format(
                area_id=config_data.get("area_id"), name=name, direction=direction
            )
            command.append(cmd)
    return command



def _tmplt_ospf_area_nssa(config_data):
    if "nssa" in config_data:
        nssa_data = config_data["nssa"]
        command = "area {area_id} nssa".format(**config_data)
        if "default_information_originate" in nssa_data:
            default_info = nssa_data["default_information_originate"]
            command += " default-information-originate"
            metric = default_info.get("metric")
            if metric is not None:
                command += " metric {metric}".format(metric=metric)
            metric_type = default_info.get("metric_type")
            if metric_type is not None:
                command += " metric-type {metric_type}".format(metric_type=metric_type)
            if default_info.get("nssa_only"):
                command += " nssa-only"
        if nssa_data.get("no_ext_capability"):
            command += " no-ext-capability"
        if nssa_data.get("no_redistribution"):
            command += " no-redistribution"
        if nssa_data.get("no_summary"):
            command += " no-summary"
        return command


def _tmplt_ospf_area_ranges(config_data):
    if "ranges" in config_data:
        commands = []
        for k, v in iteritems(config_data["ranges"]):
            cmd = "area {area_id} range".format(**config_data)
            temp_cmd = " {address} {netmask}".format(**v)
            if "advertise" in v:
                temp_cmd += " advertise"
            elif "not_advertise" in v:
                temp_cmd += " not-advertise"
            if "cost" in v:
                temp_cmd += " cost {cost}".format(**v)
            cmd += temp_cmd
            commands.append(cmd)
        return commands


def _tmplt_ospf_distance_ospf(config_data):
    if "ospf" in config_data["distance"]:
        command = "distance ospf"
        if "inter_area" in config_data["distance"]["ospf"]:
            command += " inter-area {inter_area}".format(**config_data["distance"]["ospf"])
        if config_data["distance"].get("ospf").get("intra_area"):
            command += " intra-area {intra_area}".format(**config_data["distance"]["ospf"])
        if config_data["distance"].get("ospf").get("external"):
            command += " external {external}".format(**config_data["distance"]["ospf"])
        return command


def _tmplt_ospf_distribute_list_acls(config_data):
    if "acls" in config_data.get("distribute_list"):
        command = []
        for k, v in iteritems(config_data["distribute_list"]["acls"]):
            cmd = "distribute-list {name} {direction}".format(**v)
            if "interface" in v:
                cmd += " {interface}".format(**v)
            if "protocol" in v:
                cmd += " {protocol}".format(**v)
            command.append(cmd)
        return command


def _tmplt_ospf_distribute_list_prefix(config_data):
    if "prefix" in config_data.get("distribute_list"):
        command = "distribute-list prefix {name}".format(**config_data["distribute_list"]["prefix"])
        if "gateway_name" in config_data["distribute_list"]["prefix"]:
            command += " gateway {gateway_name}".format(**config_data["distribute_list"]["prefix"])
        if "direction" in config_data["distribute_list"]["prefix"]:
            command += " {direction}".format(**config_data["distribute_list"]["prefix"])
        if "interface" in config_data["distribute_list"]["prefix"]:
            command += " {interface}".format(**config_data["distribute_list"]["prefix"])
        if "protocol" in config_data["distribute_list"]["prefix"]:
            command += " {protocol}".format(**config_data["distribute_list"]["prefix"])
        return command


def _tmplt_ospf_domain_id(config_data):
    if "domain_id" in config_data:
        command = "domain-id"
        if "ip_address" in config_data["domain_id"]:
            if "address" in config_data["domain_id"]["ip_address"]:
                command += " {address}".format(**config_data["domain_id"]["ip_address"])
                if "secondary" in config_data["domain_id"]["ip_address"]:
                    command += " {secondary}".format(**config_data["domain_id"]["ip_address"])
        elif "null" in config_data["domain_id"]:
            command += " null"
        return command


def _tmplt_ospf_event_log(config_data):
    if "event_log" in config_data:
        command = "event-log"
        if "one_shot" in config_data["event_log"]:
            command += " one-shot"
        if "pause" in config_data["event_log"]:
            command += " pause"
        if "size" in config_data["event_log"]:
            command += " size {size}".format(**config_data["event_log"])
        return command


def _tmplt_ospf_limit(config_data):
    if "limit" in config_data:
        command = "limit retransmissions"
        if "dc" in config_data["limit"]:
            if "number" in config_data["limit"]["dc"]:
                command += " dc {number}".format(**config_data["limit"]["dc"])
            if "disable" in config_data["limit"]["dc"]:
                command += " dc disable"
        if "non_dc" in config_data["limit"]:
            if "number" in config_data["limit"]["non_dc"]:
                command += " non-dc {number}".format(**config_data["limit"]["non_dc"])
            if "disable" in config_data["limit"]["dc"]:
                command += " non-dc disable"
        return command


def _tmplt_ospf_vrf_local_rib_criteria(config_data):
    if "local_rib_criteria" in config_data:
        command = "local-rib-criteria"
        if "forwarding_address" in config_data["local_rib_criteria"]:
            command += " forwarding-address"
        if "inter_area_summary" in config_data["local_rib_criteria"]:
            command += " inter-area-summary"
        if "nssa_translation" in config_data["local_rib_criteria"]:
            command += " nssa-translation"
        return command


def _tmplt_ospf_log_adjacency_changes(config_data):
    if "log_adjacency_changes" in config_data:
        command = "log-adjacency-changes"
        if "detail" in config_data["log_adjacency_changes"]:
            command += " detail"
        return command


def _tmplt_ospf_max_lsa(config_data):
    if "max_lsa" in config_data:
        command = "max-lsa {number}".format(**config_data["max_lsa"])
        if "threshold_value" in config_data["max_lsa"]:
            command += " {threshold_value}".format(**config_data["max_lsa"])
        if "ignore_count" in config_data["max_lsa"]:
            command += " ignore-count {ignore_count}".format(**config_data["max_lsa"])
        if "ignore_time" in config_data["max_lsa"]:
            command += " ignore-time {ignore_time}".format(**config_data["max_lsa"])
        if "reset_time" in config_data["max_lsa"]:
            command += " reset-time {reset_time}".format(**config_data["max_lsa"])
        if "warning_only" in config_data["max_lsa"]:
            command += " warning-only"
        return command


def _tmplt_ospf_max_metric(config_data):
    if "max_metric" in config_data:
        command = "max-metric"
        if "router_lsa" in config_data["max_metric"]:
            command += " router-lsa"
        if "external_lsa" in config_data["max_metric"]:
            command += " external-lsa {external_lsa}".format(**config_data["max_metric"])
        if "include_stub" in config_data["max_metric"]:
            command += " include-stub"
        if "on_startup" in config_data["max_metric"]:
            if "time" in config_data["max_metric"]["on_startup"]:
                command += " on-startup {time}".format(**config_data["max_metric"]["on_startup"])
            elif "wait_for_bgp" in config_data["max_metric"]["on_startup"]:
                command += " on-startup wait-for-bgp"
        if "summary_lsa" in config_data["max_metric"]:
            command += " summary-lsa {summary_lsa}".format(**config_data["max_metric"])
        return command


def _tmplt_ospf_mpls_ldp(config_data):
    if "ldp" in config_data["mpls"]:
        command = "mpls ldp"
        if "autoconfig" in config_data["mpls"]["ldp"]:
            command += " autoconfig"
            if "area" in config_data["mpls"]["ldp"]["autoconfig"]:
                command += " area {area}".format(**config_data["mpls"]["ldp"]["autoconfig"])
        elif "sync" in config_data["mpls"]["ldp"]:
            command += " sync"
    return command


def _tmplt_ospf_mpls_traffic_eng(config_data):
    if "traffic_eng" in config_data["mpls"]:
        command = "mpls traffic-eng"
        if "area" in config_data["mpls"]["traffic_eng"]:
            command += " area {area}".format(**config_data["mpls"]["traffic_eng"])
        elif "autoroute_exclude" in config_data["mpls"]["traffic_eng"]:
            command += " autoroute-exclude prefix-list {autoroute_exclude}".format(
                **config_data["mpls"]["traffic_eng"]
            )
        elif "interface" in config_data["mpls"]["traffic_eng"]:
            command += " interface {int_type}".format(
                **config_data["mpls"]["traffic_eng"]["interface"]
            )
            if "area" in config_data["mpls"]["traffic_eng"]["interface"]:
                command += " area {area}".format(**config_data["mpls"]["traffic_eng"]["interface"])
        elif "mesh_group" in config_data["mpls"]["traffic_eng"]:
            command += " mesh-group {id} {interface}".format(
                **config_data["mpls"]["traffic_eng"]["mesh_group"]
            )
            if "area" in config_data["mpls"]["traffic_eng"]["mesh_group"]:
                command += " area {area}".format(**config_data["mpls"]["traffic_eng"]["mesh_group"])
        elif "multicast_intact" in config_data["mpls"]["traffic_eng"]:
            command += " multicast-intact"
        elif "router_id_interface" in config_data["mpls"]["traffic_eng"]:
            command += " router-id {router_id_interface}".format(
                **config_data["mpls"]["traffic_eng"]
            )
        return command


def _tmplt_ospf_neighbor(config_data):
    if "neighbor" in config_data:
        command = "neighbor"
        if "address" in config_data["neighbor"]:
            command += " {address}".format(**config_data["neighbor"])
        if "cost" in config_data["neighbor"]:
            command += " cost {cost}".format(**config_data["neighbor"])
        if "database_filter" in config_data["neighbor"]:
            command += " database-filter all out"
        if "poll_interval" in config_data["neighbor"]:
            command += " poll-interval {poll_interval}".format(**config_data["neighbor"])
        if "priority" in config_data["neighbor"]:
            command += " priority {priority}".format(**config_data["neighbor"])
        return command


def _tmplt_ospf_network(config_data):
    if "network" in config_data:
        command = []
        for each in config_data["network"]:
            cmd = "network"
            if "address" in each:
                cmd += " {address} {wildcard_bits}".format(**each)
            if "area" in each:
                cmd += " area {area}".format(**each)
            command.append(cmd)
        return command


def _tmplt_ospf_nsf_cisco(config_data):
    if "cisco" in config_data["nsf"]:
        command = "nsf cisco helper"
        if "disable" in config_data["nsf"]["cisco"]:
            command += " disable"
        return command


def _tmplt_ospf_nsf_ietf(config_data):
    if "ietf" in config_data["nsf"]:
        command = "nsf ietf helper"
        if "disable" in config_data["nsf"]["ietf"]:
            command += " disable"
        elif "strict_lsa_checking" in config_data["nsf"]["ietf"]:
            command += " strict-lsa-checking"
        return command


def _tmplt_ospf_queue_depth_hello(config_data):
    if "hello" in config_data["queue_depth"]:
        command = "queue-depth hello"
        if "max_packets" in config_data["queue_depth"]["hello"]:
            command += " {max_packets}".format(**config_data["queue_depth"]["hello"])
        elif "unlimited" in config_data["queue_depth"]["hello"]:
            command += " unlimited"
        return command


def _tmplt_ospf_queue_depth_update(config_data):
    if "update" in config_data["queue_depth"]:
        command = "queue-depth update"
        if "max_packets" in config_data["queue_depth"]["update"]:
            command += " {max_packets}".format(**config_data["queue_depth"]["update"])
        elif "unlimited" in config_data["queue_depth"]["update"]:
            command += " unlimited"
        return command


def _tmplt_ospf_passive_interfaces(config_data):
    if "passive_interfaces" in config_data:
        if config_data["passive_interfaces"].get("default"):
            cmd = "passive-interface default"
        if config_data["passive_interfaces"].get("interface"):
            if config_data["passive_interfaces"].get("set_interface"):
                for each in config_data["passive_interfaces"]["interface"]:
                    cmd = "passive-interface {0}".format(each)
            elif not config_data["passive_interfaces"].get("set_interface"):
                for each in config_data["passive_interfaces"]["interface"]:
                    cmd = "no passive-interface {0}".format(each)
        return cmd


def _tmplt_ospf_summary_address(config_data):
    if "summary_address" in config_data:
        command = "summary-address {address} {mask}".format(**config_data["summary_address"])
        if "not_advertise" in config_data["summary_address"]:
            command += " not-advertise"
        elif "nssa_only" in config_data["summary_address"]:
            command += " nssa-only"
            if "tag" in config_data["summary_address"]:
                command += " tag {tag}".format(**config_data["summary_address"])
        return command


def _tmplt_ospf_timers_pacing(config_data):
    if "pacing" in config_data["timers"]:
        command = "timers pacing"
        if "flood" in config_data["timers"]["pacing"]:
            command += " flood {flood}".format(**config_data["timers"]["pacing"])
        elif "lsa_group" in config_data["timers"]["pacing"]:
            command += " lsa-group {lsa_group}".format(**config_data["timers"]["pacing"])
        elif "retransmission" in config_data["timers"]["pacing"]:
            command += " retransmission {retransmission}".format(**config_data["timers"]["pacing"])
        return command


def _tmplt_ospf_ttl_security(config_data):
    if "ttl_security" in config_data:
        command = "ttl-security all-interfaces"
        if "hops" in config_data["ttl_security"]:
            command += " hops {hops}".format(**config_data["ttl_security"])
        return command
    
def _tmplt_ospf_area_nssa_translate(config_data):
    import q
    q(config_data)


class Ospfv2Template(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospfv2Template, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "pid",
            "getval": re.compile(
                r"""
                ^router\sospf
                (\s(?P<pid>\d+))
                (\s(vrf\s(?P<vrf_value>\S+)))?
                $""",
                re.VERBOSE,
            ),
            "setval": "router ospf {{ process_id }}"
            "{{ (' vrf ' + vrf ) if vrf is defined else '' }}",
            "result": {
                "processes": {
                    "{{ pid }}": {"process_id": "{{ pid|int }}", "vrf": "{{ vrf_value }}"},
                },
            },
            "shared": True,
        },
        {
            "name": "adjacency",
            "getval": re.compile(
                r"""
                \sadjacency\sstagger
                (\s(?P<min>\d+))?
                (\s(?P<none>none))?
                (\s(?P<max>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "adjacency stagger {{ 'none' if adjacency.none else adjacency.min_adjacency }} {{ adjacency.max_adjacency }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "adjacency": {
                            "min_adjacency": "{{ min|int }}",
                            "max_adjacency": "{{ max|int }}",
                            "none": "{{ True if none_adj is defined else False }}",
                        },
                    },
                },
            },
        },
        {
            "name": "address_family",
            "getval": re.compile(
                r"""
                \stopology
                (\s(?P<base>base))?
                (\s(?P<name>\S+))?
                (\stid\s(?P<tid>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_address_family_cmd,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "address_family": {
                            "topology": {
                                "base": "{{ True if base is defined }}",
                                "name": "{{ name }}",
                                "tid": "{{ tid }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                (\s(?P<auth>authentication))?
                (\s(?P<md>message-digest))?
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} authentication"
            "{{ ' message-digest' if authentication.message_digest else '' }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "authentication": {
                                    "enable": "{{ True if auth is defined and md is undefined }}",
                                    "message_digest": "{{ not not md }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                (\s(?P<capability>capability))?
                \sdefault-exclusion
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} capability default-exclusion",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "capability": "{{ not not capability }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "default_cost",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                \sdefault-cost
                (\s(?P<default_cost>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} default-cost {{ default_cost }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "default_cost": "{{ default_cost|int }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "filter_list",
            "getval": re.compile(
                r"""
                \s+area
                (\s(?P<area_id>\S+))?
                \sfilter-list\sprefix
                (\s(?P<name>\S+))?
                (\s(?P<dir>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_filter,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "filter_list": [{"name": "{{ name }}", "direction": "{{ dir }}"}],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "nssa",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                (\s(?P<nssa>nssa))?
                (\s(?P<no_redis>no-redistribution))?
                (\s(?P<def_origin>default-information-originate))?
                (\smetric\s(?P<metric>\d+))?
                (\smetric-type\s(?P<metric_type>\d+))?
                (\s(?P<no_summary>no-summary))?
                (\s(?P<nssa_only>nssa-only))?
                (\s(?P<no_ext>no-ext-capability))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "set": "{{ True if def_origin is undefined and "
                                    "no_ext is undefined and no_redis is undefined and nssa_only is undefined }}",
                                    "default_information_originate": {
                                        "metric": "{{ metric|int }}",
                                        "metric_type": "{{ metric_type|int }}",
                                        "nssa_only": "{{ True if nssa_only is defined }}",
                                    },
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_redistribution": "{{ True if no_redis is defined }}",
                                    "no_summary": "{{ True if no_summary is defined }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "nssa.translate",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                \snssa
                \stranslate\stype7
                (\s(?P<translate_always>always|suppress-fa))?
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} nssa "
            "translate type7 {{ nssa.translate if nssa.translate is defined }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "translate": "{{ translate_always }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ranges",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))
                \srange
                (\s(?P<address>\S+))
                (\s(?P<netmask>\S+))
                (\s(?P<advertise>advertise))?
                (\s(?P<not_advertise>not-advertise))?
                (\s(cost\s(?P<cost>\d+)))
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_ranges,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "ranges": [
                                    {
                                        "address": "{{ address }}",
                                        "netmask": "{{ netmask }}",
                                        "advertise": "{{ True if advertise is defined }}",
                                        "cost": "{{ cost }}",
                                        "not_advertise": "{{ True if not_advertise is defined }}",
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "sham_link",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                \ssham-link
                (\s(?P<source>\S+))?
                (\s(?P<destination>\S+))?
                (\s(cost\s(?P<cost>\d+)))?
                (\s(ttl-security\shops\s(?P<ttl_security>\d+)))?
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} sham-link {{ sham_link.source }} {{ sham_link.destination }}"
            "{{ (' cost ' + sham_link.cost|string) if sham_link.cost is defined else '' }}"
            "{{ (' ttl-security hops ' + sham_link.ttl_security|string) if sham_link.ttl_security is defined else '' }}",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "sham_link": {
                                    "source": "{{ source }}",
                                    "destination": "{{ destination }}",
                                    "cost": "{{ cost }}",
                                    "ttl_security": "{{ ttl_security }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "stub",
            "getval": re.compile(
                r"""
                \sarea
                (\s(?P<area_id>\S+))?
                (\s(?P<stub>stub))?
                (\s(?P<no_ext>no-ext-capability))?
                (\s(?P<no_sum>no-summary))?
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} stub"
            "{{ (' no-ext-capability') if stub.no_ext_capability else ''}}"
            "{{ (' no-summary') if stub.no_summary else ''}}",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "stub": {
                                    "set": "{{ True if stub is defined and no_ext is undefined and no_sum is undefined }}",
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_summary": "{{ True if no_sum is defined }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "auto_cost",
            "getval": re.compile(
                r"""
                (\s(?P<auto_cost>auto-cost))
                (\sreference-bandwidth\s(?P<ref_band>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "auto-cost"
            "{{ ' reference-bandwidth ' + auto_cost.reference_bandwidth|string if auto_cost.reference_bandwidth is defined }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "auto_cost": {
                            "set": "{{ True }}",
                            "reference_bandwidth": "{{ ref_band }}",
                        },
                    },
                },
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \sbfd
                (\s(?P<bfd>all-interfaces))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bfd all-interfaces",
            "result": {"processes": {"{{ pid }}": {"bfd": "{{ True if bfd is defined }}"}}},
        },
        {
            "name": "capability.lls",
            "getval": re.compile(
                r"""
                \scapability
                (\s(?P<lls>lls))
                $""",
                re.VERBOSE,
            ),
            "setval": "capability lls",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "capability": {
                            "lls": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "capability.opaque",
            "getval": re.compile(
                r"""
                \scapability
                (\s(?P<opaque>opaque))
                $""",
                re.VERBOSE,
            ),
            "setval": "capability opaque",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "capability": {
                            "opaque": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "capability.transit",
            "getval": re.compile(
                r"""
                \scapability
                (\s(?P<transit>transit))
                $""",
                re.VERBOSE,
            ),
            "setval": "capability transit",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "capability": {
                            "transit": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "capability.vrf_lite",
            "getval": re.compile(
                r"""
                \scapability
                (\s(?P<vrf_lite>vrf-lite))
                $""",
                re.VERBOSE,
            ),
            "setval": "capability vrf-lite",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "capability": {
                            "vrf_lite": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "compatible",
            "getval": re.compile(
                r"""
                \scompatible
                (\s(?P<rfc>rfc1583|rfc1587|rfc5243))?
                $""",
                re.VERBOSE,
            ),
            "setval": "compatible"
            "{{ (' rfc1583') if compatible.rfc1583 else ''}}"
            "{{ (' rfc1587') if compatible.rfc1587 else ''}}"
            "{{ (' rfc5243') if compatible.rfc5243 else ''}}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "compatible": {
                            "rfc1583": "{{ True if 'rfc1583' in rfc else False }}",
                            "rfc1587": "{{ True if 'rfc1587' in rfc else False }}",
                            "rfc5243": "{{ True if 'rfc5243' in rfc else False }}",
                        },
                    },
                },
            },
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""
                \sdefault-information
                (\s(?P<originate>originate))?
                (\s(?P<always>always))?
                (\smetric\s(?P<metric>\d+))?
                (\smetric-type\s(?P<metric_type>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "default-information"
            "{{ ' originate' if default_information.originate is defined else ''}}"
            "{{ ' always' if default_information.always is defined else '' }}"
            "{{ (' metric ' + default_information.metric|string) if default_information.metric is defined else '' }}"
            "{{ (' metric-type ' + default_information.metric_type|string) if default_information.metric_type is defined else '' }}"
            "{{ ' route-map ' + default_information.route_map if default_information.route_map is defined and default_information.metric is defined else '' }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "default_information": {
                            "originate": "{{ True if originate is defined }}",
                            "always": "{{ True if always is defined }}",
                            "metric": "{{ metric }}",
                            "metric_type": "{{ metric_type }}",
                            "route_map": "{{ route_map }}",
                        },
                    },
                },
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""
                \sdefault-metric
                \s(?P<default_metric>\d+)?
                $""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric|string }}",
            "result": {"processes": {"{{ pid }}": {"default_metric": "{{ default_metric }}"}}},
        },
        {
            "name": "discard_route",
            "getval": re.compile(
                r"""
                (\s(?P<discard_route>discard-route))
                (\sexternal\s(?P<external>\d+))?
                (\sinternal\s(?P<internal>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "discard-route"
            "{{ ' external ' + discard_route.external|string if discard_route.external is defined else '' }}"
            "{{ ' internal ' + discard_route.internal|string if discard_route.internal is defined else '' }}",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "discard_route": {
                            "set": "{{ True }}",
                            "external": "{{ external }}",
                            "internal": "{{ internal }}",
                        },
                    },
                },
            },
        },
        {
            "name": "distance.admin_distance",
            "getval": re.compile(
                r"""
                \sdistance
                (\s(?P<admin_dist>\S+))
                (\s(?P<source>\S+))?
                (\s(?P<wildcard>\S+))?
                (\s(?P<acl>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "distance {{ admin_distance.distance }} "
            "{{ ( admin_distance.address + ' ' + admin_distance.wildcard_bits ) if admin_distance.address is defined else '' }}"
            "{{ ' ' + admin_distance.acl if admin_distance.acl is defined else '' }}",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distance": {
                            "admin_distance": {
                                "distance": "{{ admin_dist }}",
                                "address": "{{ source }}",
                                "wildcard_bits": "{{ wildcard }}",
                                "acl": "{{ acl }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "distance.ospf",
            "getval": re.compile(
                r"""
                \sdistance\sospf
                (\sintra-area\s(?P<intra>\d+))
                (\sinter-area\s(?P<inter>\d+))
                (\sexternal\s(?P<external>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distance_ospf,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distance": {
                            "ospf": {
                                "inter_area": "{{ inter|int }}",
                                "intra_area": "{{ intra|int }}",
                                "external": "{{ external|int }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "distribute_list.acls",
            "getval": re.compile(
                r"""
                \sdistribute-list
                (\s(?P<name>\S+))
                (\s(?P<dir>\S+))
                (\s(?P<int_pro>\S+\s\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_acls,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {
                            "acls": [
                                {
                                    "name": "{{ name }}",
                                    "direction": "{{ dir }}",
                                    "interface": '{{ int_pro if dir == "in" }}',
                                    "protocol": '{{ int_pro if dir == "out" }}',
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "distribute_list.prefix",
            "getval": re.compile(
                r"""
                \sdistribute-list
                (\sprefix\s(?P<prefix>\S+))
                (\sgateway\s(?P<gateway>\S+))?
                (\s(?P<dir>\S+))?
                (\s(?P<int_pro>\S+\s\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_prefix,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {
                            "prefix": {
                                "name": "{{ prefix }}",
                                "gateway_name": "{{ gateway }}",
                                "direction": "{{ dir if gateway is undefined }}",
                                "interface": '{{ int_pro if dir == "in" }}',
                                "protocol": '{{ int_pro if dir == "out" }}',
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "distribute_list.route_map",
            "getval": re.compile(
                r"""
                \sdistribute-list
                (\sroute-map\s(?P<route_map>\S+))
                (\s(?P<dir>\S+))
                $""",
                re.VERBOSE,
            ),
            "setval": "distribute-list route-map {{ distribute_list.route_map.name }} in",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {"route_map": {"name": "{{ route_map }}"}},
                    },
                },
            },
        },
        {
            "name": "domain_id",
            "getval": re.compile(
                r"""
                \sdomain-id
                (\s(?P<address>\S+))
                (\s(?P<secondary>secondary))?
                (\s(?P<null>null))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_domain_id,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "domain_id": {
                            "ip_address": {
                                "address": "{{ address }}",
                                "secondary": "{{ True if secondary is defined }}",
                            },
                            "null": "{{ True if null is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "domain_tag",
            "getval": re.compile(
                r"""
                \sdomain-tag
                (\s(?P<tag>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "domain-tag {{ domain_tag }}",
            "result": {"processes": {"{{ pid }}": {"domain_tag": "{{ tag|int }}"}}},
        },
        {
            "name": "event_log",
            "getval": re.compile(
                r"""
                (\s(?P<event_log>event-log))?
                (\s(?P<one_shot>one-shot))?
                (\s(?P<pause>pause))?
                (\ssize\s(?P<size>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_event_log,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "event_log": {
                            "enable": "{{ True if event_log is defined and one_shot is undefined and pause is undefined and size is undefined }}",
                            "one_shot": "{{ True if one_shot is defined }}",
                            "pause": "{{ True if pause is defined }}",
                            "size": "{{ size|int }}",
                        },
                    },
                },
            },
        },
        {
            "name": "help",
            "getval": re.compile(
                r"""
                \s(?P<help>help)
                $""",
                re.VERBOSE,
            ),
            "setval": "help",
            "result": {"processes": {"{{ pid }}": {"help": "{{ True if help is defined }}"}}},
        },
        {
            "name": "ignore",
            "getval": re.compile(
                r"""
                \s(?P<ignore>ignore)
                $""",
                re.VERBOSE,
            ),
            "setval": "ignore lsa mospf",
            "result": {"processes": {"{{ pid }}": {"ignore": "{{ True if ignore is defined }}"}}},
        },
        {
            "name": "interface_id",
            "getval": re.compile(
                r"""
                (\s(?P<interface_id>interface-id\ssnmp-if-index))?
                $""",
                re.VERBOSE,
            ),
            "setval": "interface-id snmp-if-index",
            "result": {
                "processes": {
                    "{{ pid }}": {"interface_id": "{{ True if interface_id is defined }}"},
                },
            },
        },
        {
            "name": "ispf",
            "getval": re.compile(
                r"""
                \s(?P<ispf>ispf)
                $""",
                re.VERBOSE,
            ),
            "setval": "ispf",
            "result": {"processes": {"{{ pid }}": {"ispf": "{{ True if ispf is defined }}"}}},
        },
        {
            "name": "limit",
            "getval": re.compile(
                r"""
                \slimit\sretransmissions
                (\sdc\s(?P<dc_num>\d+))?
                (\sdc\sdisable(?P<dc_disable>))?
                (\snon-dc\s(?P<non_dc_num>\d+))?
                (\snon-dc\sdisable(?P<non_dc_disable>))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_limit,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "limit": {
                            "dc": {
                                "number": "{{ dc_num|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                            "non_dc": {
                                "number": "{{ non_dc_num|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "local_rib_criteria",
            "getval": re.compile(
                r"""
                (\s(?P<local>local-rib-criteria))?
                (\s(?P<forward>forwarding-address))?
                (\s(?P<inter>inter-area-summary))?
                (\s(?P<nssa>nssa-translation))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_vrf_local_rib_criteria,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "local_rib_criteria": {
                            "enable": "{{ True if local is defined and forward is undefined and inter is undefined and nssa is undefined }}",
                            "forwarding_address": "{{ True if forward is defined }}",
                            "inter_area_summary": "{{ True if inter is defined }}",
                            "nssa_translation": "{{ True if nssa is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "log_adjacency_changes",
            "getval": re.compile(
                r"""
                (\s(?P<log>log-adjacency-changes))?
                (\s(?P<detail>detail))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_log_adjacency_changes,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "log_adjacency_changes": {
                            "set": "{{ True if log is defined and detail is undefined }}",
                            "detail": "{{ True if detail is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "max_lsa",
            "getval": re.compile(
                r"""\smax-lsa
                    (\s(?P<number>\d+))?
                    (\s(?P<threshold>\d+))?
                    (\s(?P<warning>warning-only))?
                    (\signore-count\s(?P<ignore_count>\d+))?
                    (\signore-time\s(?P<ignore_time>\d+))?
                    (\sreset-time\s(?P<reset_time>\d+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_lsa,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "max_lsa": {
                            "number": "{{ number }}",
                            "threshold_value": "{{ threshold }}",
                            "ignore_count": "{{ ignore_count }}",
                            "ignore_time": "{{ ignore_time }}",
                            "reset_time": "{{ reset_time }}",
                            "warning_only": "{{ True if warning is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "max_metric",
            "getval": re.compile(
                r"""
                \smax-metric
                (\s(?P<router_lsa>router-lsa))?
                (\s(?P<include_stub>include-stub))?
                (\sexternal-lsa\s(?P<external_lsa>\d+))?
                (\son-startup\s(?P<startup_time>\d+))?
                (\son-startup\s(?P<startup_wait>\S+))?
                (\ssummary-lsa\s(?P<summary_lsa>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_metric,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "max_metric": {
                            "router_lsa": "{{ True if router_lsa is defined }}",
                            "external_lsa": "{{ external_lsa }}",
                            "include_stub": "{{ ignore_count }}",
                            "on_startup": {
                                "time": "{{ startup_time }}",
                                "wait_for_bgp": "{{ True if startup_wait is defined }}",
                            },
                            "summary_lsa": "{{ summary_lsa }}",
                        },
                    },
                },
            },
        },
        {
            "name": "maximum_paths",
            "getval": re.compile(
                r"""
                \smaximum-paths
                \s(?P<paths>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths {{ maximum_paths }}",
            "result": {"processes": {"{{ pid }}": {"maximum_paths": "{{ paths }}"}}},
        },
        {
            "name": "mpls.ldp",
            "getval": re.compile(
                r"""
                \smpls\sldp
                (\s(?P<autoconfig>autoconfig))?
                (\sarea\s(?P<area>\S+))?
                (\s(?P<sync>sync))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_mpls_ldp,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "mpls": {
                            "ldp": {
                                "autoconfig": {
                                    "set": "{{ True if autoconfig is defined and area is undefined }}",
                                    "area": "{{ area }}",
                                },
                                "sync": "{{ True if sync is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "mpls.traffic_eng",
            "getval": re.compile(
                r"""\s+mpls
                    \straffic-eng*
                    \s*(?P<area>area\s\S+)*
                    \s*(?P<autoroute>autoroute-exclude\s\S+\s\S+)*
                    \s*(?P<interface>interface\s(?P<int_type>\S+\s\S+)\s(?P<int_area>area\s\S+))*
                    \s*(?P<mesh>mesh-group\s\d+\s(?P<mesh_int>\S+\s\S+)\s(?P<mesh_area>area\s\d+))*
                    \s*(?P<multicast>multicast-intact)*
                    \s*(?P<router>router-id\s(?P<router_int>\S+\s\S+))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_mpls_traffic_eng,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "mpls": {
                            "traffic_eng": {
                                "area": "{{ area.split(" ")[1] }}",
                                "autoroute_exclude": "{{ autoroute.split(" ")[2] }}",
                                "interface": {
                                    "interface_type": "{{ int_type }}",
                                    "area": "{{ int_area.split(" ")[1] }}",
                                },
                                "mesh_group": {
                                    "id": "{{ mesh.split(" ")[1] }}",
                                    "interface": "{{ mest_int }}",
                                    "area": "{{ mesh_area.split(" ")[1] }}",
                                },
                                "multicast_intact": "{{ True if multicast is defined }}",
                                "router_id_interface": "{{ router_int }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""
                \sneighbor
                (\s(?P<address>\S+))
                (\scost\s(?P<cost>\d+))
                (\sdatabase-filter\sall\sout\s(?P<db_filter>))?
                (\spoll-interval\s(?P<poll>\d+))?
                (\spriority\s(?P<priority>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_neighbor,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "neighbor": {
                            "address": "{{ address }}",
                            "cost": "{{ cost }}",
                            "database_filter": "{{ True if db_filter is defined }}",
                            "poll_interval": "{{ poll }}",
                            "priority": "{{ priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \snetwork
                (\s(?P<address>\S+))?
                (\s(?P<wildcard>\S+))?
                (\sarea\s(?P<area>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_network,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "network": [
                            {
                                "address": "{{ address }}",
                                "wildcard_bits": "{{ wildcard }}",
                                "area": "{{ area }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "nsf.cisco",
            "getval": re.compile(
                r"""
                \snsf
                (\s(?P<cisco>cisco))
                (\s(?P<helper>helper))?
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_nsf_cisco,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "nsf": {
                            "cisco": {
                                "helper": "{{ True if helper is defined }}",
                                "disable": "{{ True if disable is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "nsf.ietf",
            "getval": re.compile(
                r"""
                \snsf
                (\s(?P<ietf>ietf))
                (\s(?P<helper>helper))?
                (\s(?P<disable>disable))?
                (\s(?P<strict>strict-lsa-checking))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_nsf_ietf,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "nsf": {
                            "ietf": {
                                "helper": "{{ True if helper is defined }}",
                                "disable": "{{ True if disable is defined }}",
                                "strict_lsa_checking": "{{ True if strict is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "passive_interfaces.default",
            "getval": re.compile(
                r"""
                \spassive-interface
                \s(?P<default_value>default)
                $""",
                re.VERBOSE,
            ),
            "setval": "passive-interface default",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "passive_interfaces": {
                            "default": "{{ True if default_value is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "passive_interfaces.interface",
            "getval": re.compile(
                r"""
                (\s(?P<no>no))?
                \spassive-interface
                \s(?P<interface>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_passive_interfaces,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "passive_interfaces": {
                            "interface": {
                                "set_interface": "{{ not no }}",
                                "name": ["{{ interface if 'default' not in interface }}"],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "prefix_suppression",
            "getval": re.compile(
                r"""
                \s(?P<prefix_sup>prefix-suppression)
                $""",
                re.VERBOSE,
            ),
            "setval": "prefix-suppression",
            "result": {
                "processes": {
                    "{{ pid }}": {"prefix_suppression": "{{ True if prefix_sup is defined }}"},
                },
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \spriority
                \s(?P<priority>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "priority {{ priority }}",
            "result": {"processes": {"{{ pid }}": {"priority": "{{ priority }}"}}},
        },
        {
            "name": "queue_depth.hello",
            "getval": re.compile(
                r"""
                \squeue-depth\shello
                (\s(?P<max_packets>\d+))?
                (\s(?P<unlimited>unlimited))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_hello,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "queue_depth": {
                            "hello": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "queue_depth.update",
            "getval": re.compile(
                r"""
                \squeue-depth\supdate
                (\s(?P<max_packets>\d+))?
                (\s(?P<unlimited>unlimited))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_update,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "queue_depth": {
                            "update": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""
                \srouter-id
                (\s(?P<id>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "router-id {{ router_id }}",
            "result": {"processes": {"{{ pid }}": {"router_id": "{{ id }}"}}},
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s(?P<shutdown>shutdown)
                $""",
                re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "processes": {"{{ pid }}": {"shutdown": "{{ True if shutdown is defined }}"}},
            },
        },
        {
            "name": "summary_address",
            "getval": re.compile(
                r"""
                \ssummary-address
                (\s(?P<address>\S+))?
                (\s(?P<mask>\S+))?
                (\s(?P<not_adv>not-advertise))?
                (\s(?P<nssa>nssa-only))?
                (\stag\s(?P<tag>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_summary_address,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "summary_address": {
                            "address": "{{ address }}",
                            "mask": "{{ mask }}",
                            "not_advertise": "{{ True if not_adv is defined }}",
                            "nssa_only": "{{ True if nssa is defined }}",
                            "tag": "{{ tag }}",
                        },
                    },
                },
            },
        },
        {
            "name": "timers.lsa",
            "getval": re.compile(
                r"""
                \stimers
                \slsa
                \sarrival
                (\s(?P<lsa>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers lsa arrival {{ timers.lsa }}",
            
            "result": {"processes": {"{{ pid }}": {"timers": {"lsa": "{{ lsa }}"}}}},
        },
        {
            "name": "timers.pacing",
            "getval": re.compile(
                r"""
                \stimers\spacing
                (\sflood\s(?P<flood>\d+))?
                (\slsa-group\s(?P<lsa_group>\d+))?
                (\sretransmission\s(?P<retransmission>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_timers_pacing,
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "pacing": {
                                "flood": "{{ flood }}",
                                "lsa_group": "{{ lsa_group }}",
                                "retransmission": "{{ retransmission }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "timers.throttle.lsa",
            "getval": re.compile(
                r"""
                \stimers\sthrottle
                (\s(?P<lsa>lsa))?
                (\s(?P<first_delay>\d+))?
                (\s(?P<min_delay>\d+))?
                (\s(?P<max_delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers throttle lsa {{ throttle.lsa.first_delay }} {{ throttle.lsa.min_delay }} {{ throttle.lsa.max_delay }}",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "throttle": {
                                "lsa": {
                                    "first_delay": "{{ first_delay }}",
                                    "min_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "timers.throttle.spf",
            "getval": re.compile(
                r"""
                \stimers\sthrottle
                (\s(?P<spf>spf))?
                (\s(?P<first_delay>\d+))?
                (\s(?P<min_delay>\d+))?
                (\s(?P<max_delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "timers throttle spf {{ throttle.spf.receive_delay }} {{ throttle.spf.between_delay }} {{ throttle.spf.max_delay }}",
            
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "throttle": {
                                "spf": {
                                    "receive_delay": "{{ first_delay }}",
                                    "between_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traffic_share",
            "getval": re.compile(
                r"""
                \s(?P<traffic>traffic-share\smin\sacross-interfaces)
                $""",
                re.VERBOSE,
            ),
            "setval": "traffic-share min across-interfaces",
            "result": {
                "processes": {"{{ pid }}": {"traffic_share": "{{ True if traffic is defined }}"}},
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \sttl-security
                (\s(?P<interfaces>all-interfaces))?
                (\shops\s(?P<hops>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_ttl_security,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "ttl_security": {
                            "set": "{{ True if interfaces is defined and hops is undefined }}",
                            "hops": "{{ hops }}",
                        },
                    },
                },
            },
        },
    ]
