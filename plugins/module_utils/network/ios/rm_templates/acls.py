# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The acls parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""
import re

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def remarks_with_sequence(remarks_data):
    cmd = "remark"
    if remarks_data.get("remarks"):
        cmd += " " + remarks_data.get("remarks")
    if remarks_data.get("sequence"):
        cmd = to_text(remarks_data.get("sequence")) + " " + cmd
    return cmd


def _tmplt_access_list_entries(aces):
    def source_destination_common_config(config_data, command, attr):
        if config_data[attr].get("address"):
            command += " {address}".format(**config_data[attr])
            if config_data[attr].get("wildcard_bits"):
                command += " {wildcard_bits}".format(**config_data[attr])
        elif config_data[attr].get("any"):
            command += " any".format(**config_data[attr])
        elif config_data[attr].get("host"):
            command += " host {host}".format(**config_data[attr])
        elif config_data[attr].get("object_group"):
            command += " object-group {object_group}".format(**config_data[attr])
        if config_data[attr].get("port_protocol"):
            if config_data[attr].get("port_protocol").get("range"):
                command += " range {0} {1}".format(
                    config_data[attr]["port_protocol"]["range"].get("start"),
                    config_data[attr]["port_protocol"]["range"].get("end"),
                )
            else:
                port_proto_type = list(config_data[attr]["port_protocol"].keys())[0]
                command += " {0} {1}".format(
                    port_proto_type,
                    config_data[attr]["port_protocol"][port_proto_type],
                )
        return command

    command = ""
    proto_option = None
    if aces:
        if aces.get("sequence") and aces.get("afi") == "ipv4":
            command += "{sequence}".format(**aces)
        if aces.get("grant") and aces.get("sequence") and aces.get("afi") == "ipv4":
            command += " {grant}".format(**aces)
        elif aces.get("grant") and aces.get("sequence") and aces.get("afi") == "ipv6":
            command += "{grant}".format(**aces)
        elif aces.get("grant"):
            command += "{grant}".format(**aces)
        if aces.get("protocol_options"):
            if "protocol_number" in aces["protocol_options"]:
                command += " {protocol_number}".format(**aces["protocol_options"])
            else:
                command += " {0}".format(list(aces["protocol_options"])[0])
                proto_option = aces["protocol_options"].get(
                    list(aces["protocol_options"])[0],
                )
        elif aces.get("protocol"):
            command += " {protocol}".format(**aces)
        if aces.get("source"):
            command = source_destination_common_config(aces, command, "source")
        if aces.get("destination"):
            command = source_destination_common_config(aces, command, "destination")
        if isinstance(proto_option, dict):
            command += " {0}".format(list(proto_option.keys())[0].replace("_", "-"))
        if aces.get("dscp"):
            command += " dscp {dscp}".format(**aces)
        if aces.get("sequence") and aces.get("afi") == "ipv6":
            command += " sequence {sequence}".format(**aces)
        if aces.get("enable_fragments"):
            command += " fragments"
        if aces.get("log"):
            command += " log"
            if aces["log"].get("user_cookie"):
                command += " {user_cookie}".format(**aces["log"])
        if aces.get("log_input"):
            command += " log-input"
            if aces["log_input"].get("user_cookie"):
                command += " {user_cookie}".format(**aces["log_input"])
        if aces.get("option"):
            option_val = list(aces.get("option").keys())[0]
            command += " option {0}".format(option_val)
        if aces.get("precedence"):
            command += " precedence {precedence}".format(**aces)
        if aces.get("time_range"):
            command += " time-range {time_range}".format(**aces)
        if aces.get("tos"):
            command += " tos"
            if aces["tos"].get("service_value"):
                command += " {service_value}".format(**aces["tos"])
            elif aces["tos"].get("max_reliability"):
                command += " max-reliability"
            elif aces["tos"].get("max_throughput"):
                command += " max-throughput"
            elif aces["tos"].get("min_delay"):
                command += " min-delay"
            elif aces["tos"].get("min_monetary_cost"):
                command += " min-monetary-cost"
            elif aces["tos"].get("normal"):
                command += " normal"
        if aces.get("ttl"):
            command += " ttl {0}".format(list(aces["ttl"])[0])
            proto_option = aces["ttl"].get(list(aces["ttl"])[0])
            command += " {0}".format(proto_option)
    return command


class AclsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(AclsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "only_acls_name",
            "getval": re.compile(
                r"""^(?P<acl_type>Standard|Extended|Reflexive)*
                    \s*(?P<afi>IP|IPv6)*
                    \s*access*
                    \s*list*
                    \s*(?P<acl_name>.+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "acl_type": "{{ acl_type.lower() if acl_type is defined }}",
                        "afi": "{{ 'ipv4' if afi == 'IP' else 'ipv6' }}",
                    },
                },
            },
        },
        {
            "name": "acls_name",
            "getval": re.compile(
                r"""^(?P<afi>ip|ipv6|mac)
                    (\s(access-list))
                    (\s(?P<acl_type>standard|extended|reflexive))?
                    (\s(?P<acl_name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "name",
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "acl_type": "{{ acl_type.lower() if acl_type is defined }}",
                        "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "remarks",
            "getval": re.compile(
                r"""((?P<order>^\d+))
                    (\s*(?P<sequence>\d+))
                    (\sremark\s(?P<remarks>.+))
                    $""",
                re.VERBOSE,
            ),
            "setval": remarks_with_sequence,
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "aces": [
                            {
                                "the_remark": "'{{ remarks }}'",
                                "order": "{{ order }}",
                                "is_remark_for": "{{ sequence }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "remarks_no_data",
            "getval": re.compile(
                r"""(?P<order>^\d+)\s*remark\s(?P<remarks>.+)$""",
                re.VERBOSE,
            ),
            "setval": remarks_with_sequence,
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "aces": [
                            {
                                "the_remark": "'{{ remarks }}'",
                                "order": "{{ order }}",
                                "is_remark_for": "remark",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "remarks_ipv6",
            "getval": re.compile(
                r"""\s*(sequence\s(?P<sequence>\d+))
                    (\sremark\s(?P<remarks>.+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "remark {{ remarks }}",
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "aces": [
                            {
                                "sequence": "{{ sequence }}",
                                "remarks": ["'{{ remarks }}'"],
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "aces_ipv4_standard",
            "getval": re.compile(
                r"""^\s*((?P<sequence>\d+))?
                        (\s(?P<grant>deny|permit))
                        (\s+(?P<address>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))?
                        (\s(?P<wildcard>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))?
                        (\s*(?P<any>any))?
                        (\s(?P<log>log))?
                    $""",
                re.VERBOSE,
            ),
            "compval": "aces",
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "aces": [
                            {
                                "sequence": "{{ sequence }}",
                                "grant": "{{ grant }}",
                                "source": {
                                    "address": "{{ address }}",
                                    "wildcard_bits": "{{ wildcard }}",
                                    "any": "{{ not not any }}",
                                },
                                "log": {"set": "{{ not not log }}"},
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "aces",
            "getval": re.compile(
                r"""^\s*((?P<sequence>\d+))?
                        (\ssequence\s(?P<sequence_ipv6>\d+))?
                        (\s(?P<grant>deny|permit))
                        (\sevaluate\s(?P<evaluate>\S+))?
                        (\s(?P<protocol_num>\d+)\s)?
                        (\s*(?P<protocol>ahp|eigrp|esp|gre|icmp|igmp|ipinip|ipv6|ip|nos|ospf|pcp|pim|sctp|tcp|ip|udp))?
                        ((\s*(?P<source_any>any))|
                        (\s*object-group\s(?P<source_obj_grp>\S+))|
                        (\s*host\s(?P<source_host>\S+))|
                        (\s*(?P<ipv6_source_address>\S+/\d+))|
                        (\s*(?P<source_address>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s\S+)))?
                        (\seq\s(?P<seq>(\S+|\d+)))?
                        (\sgt\s(?P<sgt>(\S+|\d+)))?
                        (\slt\s(?P<slt>(\S+|\d+)))?
                        (\sneq\s(?P<sneq>(\S+|\d+)))?
                        (\srange\s(?P<srange_start>\d+)\s(?P<srange_end>\d+))?
                        (\s(?P<dest_any>any))?
                        (\sobject-group\s(?P<dest_obj_grp>\S+))?
                        (\shost\s(?P<dest_host>\S+))?
                        (\s(?P<ipv6_dest_address>\S+/\d+))?
                        (\s(?P<dest_address>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s\S+))?
                        (\seq\s(?P<deq>(\S+|\d+)))?
                        (\sgt\s(?P<dgt>(\S+|\d+)))?
                        (\slt\s(?P<dlt>(\S+|\d+)))?
                        (\sneq\s(?P<dneq>(\S+|\d+)))?
                        (\srange\s(?P<drange_start>\d+)\s(?P<drange_end>\d+))?
                        (\s(?P<icmp_igmp_tcp_protocol>administratively-prohibited|alternate-address|conversion-error|dod-host-prohibited|dod-net-prohibited|echo-reply|echo|general-parameter-problem|host-isolated|host-precedence-unreachable|host-redirect|host-tos-redirect|host-tos-unreachable|host-unknown|host-unreachable|information-reply|information-request|mask-reply|mask-request|mobile-redirect|net-redirect|net-tos-redirect|net-tos-unreachable|net-unreachable|network-unknown|no-room-for-option|option-missing|packet-too-big|parameter-problem|port-unreachable|precedence-unreachable|protocol-unreachable|reassembly-timeout|redirect|router-advertisement|router-solicitation|source-quench|source-route-failed|time-exceeded|timestamp-reply|timestamp-request|traceroute|ttl-exceeded|unreachable|dvmrp|host-query|mtrace-resp|mtrace-route|pim|trace|v1host-report|v2host-report|v2leave-group|v3host-report|ack|established|fin|psh|rst|syn|urg))?
                        (\sdscp\s(?P<dscp>\S+))?
                        (\s(?P<enable_fragments>fragments))?
                        (\slog-input\s\(tag\s=\s(?P<log_input>\S+\)|log-input))?
                        (\s(?P<log_input_only>log-input))?
                        (\slog\s\(tag\s=\s(?P<log>\S+\)|log))?
                        (\s(?P<log_only>log))?
                        (\soption\s(?P<option>\S+|\d+))?
                        (\sprecedence\s(?P<precedence>\S+))?
                        (\stime-range\s(?P<time_range>\S+))?
                        (\stos\s(?P<tos>\S+|\d+))?
                        (\sttl\seq\s(?P<ttl_eq>\d+))?
                        (\sttl\sgt\s(?P<ttl_gt>\d+))?
                        (\sttl\slt\s(?P<ttl_lt>\d+))?
                        (\sttl\sneg\s(?P<ttl_neg>\d+))?
                    """,
                re.VERBOSE,
            ),
            "setval": _tmplt_access_list_entries,
            "compval": "aces",
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "aces": [
                            {
                                "sequence": "{% if sequence is defined %}{{ sequence \
                                    }}{% elif sequence_ipv6 is defined %}{{ sequence_ipv6 }}{% endif %}",
                                "grant": "{{ grant }}",
                                "evaluate": "{{ evaluate }}",
                                "protocol": "{{ protocol }}",
                                "protocol_number": "{{ protocol_num }}",
                                "icmp_igmp_tcp_protocol": "{{ icmp_igmp_tcp_protocol }}",
                                "source": {
                                    "address": "{{ source_address }}",
                                    "ipv6_address": "{{ ipv6_source_address }}",
                                    "any": "{{ not not source_any }}",
                                    "host": "{{ source_host }}",
                                    "object_group": "{{ source_obj_grp }}",
                                    "port_protocol": {
                                        "eq": "{{ seq }}",
                                        "gt": "{{ sgt }}",
                                        "lt": "{{ slt }}",
                                        "neq": "{{ sneq }}",
                                        "range": {
                                            "start": "{{ srange_start if srange_start is defined else None }}",
                                            "end": "{{ srange_end if srange_end is defined else None }}",
                                        },
                                    },
                                },
                                "destination": {
                                    "address": "{{ dest_address }}",
                                    "ipv6_address": "{{ ipv6_dest_address }}",
                                    "any": "{{ not not dest_any }}",
                                    "host": "{{ dest_host }}",
                                    "object_group": "{{ dest_obj_grp }}",
                                    "port_protocol": {
                                        "eq": "{{ deq }}",
                                        "gt": "{{ dgt }}",
                                        "lt": "{{ dlt }}",
                                        "neq": "{{ dneq }}",
                                        "range": {
                                            "start": "{{ drange_start if drange_start is defined else None }}",
                                            "end": "{{ drange_end if drange_end is defined else None }}",
                                        },
                                    },
                                },
                                "dscp": "{{ dscp }}",
                                "enable_fragments": "{{ True if enable_fragments is defined else None }}",
                                "log": {
                                    "set": "{{ True if log_only is defined or log is defined }}",
                                    "user_cookie": "{{ log.split(')')[0] if log is defined }}",
                                },
                                "log_input": {
                                    "set": "{{ True if log_input_only is defined or log_input is defined }}",
                                    "user_cookie": "{{ log_input.split(')')[0] if log_input is defined }}",
                                },
                                "option": {
                                    "{{ option if option is defined else None }}": "{{ True if option is defined else None }}",
                                },
                                "precedence": "{{ precedence }}",
                                "time_range": "{{ time_range }}",
                                "tos": {
                                    "max_reliability": "{{ True if tos is defined and 'max-reliability' in tos else '' }}",
                                    "max_throughput": "{{ True if tos is defined and 'max-throughput' in tos else '' }}",
                                    "min_delay": "{{ True if tos is defined and 'min-delay' in tos else '' }}",
                                    "min_monetary_cost": "{{ True if tos is defined and 'min-monetary-cost' in tos else '' }}",
                                    "normal": "{{ True if tos is defined and 'normal' in tos else '' }}",
                                    "service_value": "{{ tos if tos is defined else None }}",
                                },
                                "ttl": {
                                    "eq": "{{ ttl_eq }}",
                                    "gt": "{{ ttl_gt }}",
                                    "lt": "{{ ttl_lt }}",
                                    "neq": "{{ ttl_neq }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
    ]
