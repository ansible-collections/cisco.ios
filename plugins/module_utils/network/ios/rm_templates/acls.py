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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_access_list_name(config_data):
    try:
        acl_id = int(config_data.get("name"))
        if not config_data.get("acl_type"):
            if acl_id >= 1 and acl_id <= 99:
                config_data["acl_type"] = "standard"
            if acl_id >= 100 and acl_id <= 199:
                config_data["acl_type"] = "extended"
    except ValueError:
        pass
    afi = config_data.get("afi")
    if afi == "ipv4":
        command = "ip access-list {acl_type} {name}".format(**config_data)
    elif afi == "ipv6":
        command = "ipv6 access-list {name}".format(**config_data)
    return command


def _tmplt_access_list_entries(config_data):
    if "aces" in config_data:
        command = []

        def source_destination_common_config(config_data, command, type):
            if config_data[type].get("address"):
                command += " {address}".format(**config_data[type])
                if config_data[type].get("wildcard_bits"):
                    command += " {wildcard_bits}".format(**config_data[type])
            elif config_data[type].get("any"):
                command += " any".format(**config_data[type])
            elif config_data[type].get("host"):
                command += " host {host}".format(**config_data[type])
            elif config_data[type].get("object_group"):
                command += " object-group {object_group}".format(
                    **config_data[type]
                )
            if config_data[type].get("port_protocol"):
                port_proto_type = list(
                    config_data[type]["port_protocol"].keys()
                )[0]
                command += " {0} {1}".format(
                    port_proto_type,
                    config_data[type]["port_protocol"][port_proto_type],
                )
            return command

        command = ""
        proto_option = None
        if config_data.get("aces"):
            aces = config_data["aces"]
            if aces.get("sequence") and config_data.get("afi") == "ipv4":
                command += "{sequence}".format(**aces)
            if (
                aces.get("grant")
                and aces.get("sequence")
                and config_data.get("afi") == "ipv4"
            ):
                command += " {grant}".format(**aces)
            elif (
                aces.get("grant")
                and aces.get("sequence")
                and config_data.get("afi") == "ipv6"
            ):
                command += "{grant}".format(**aces)
            elif aces.get("grant"):
                command += "{grant}".format(**aces)
            if aces.get("protocol_options"):
                if "protocol_number" in aces["protocol_options"]:
                    command += " {protocol_number}".format(
                        **aces["protocol_options"]
                    )
                else:
                    command += " {0}".format(list(aces["protocol_options"])[0])
                    proto_option = aces["protocol_options"].get(
                        list(aces["protocol_options"])[0]
                    )
            elif aces.get("protocol"):
                command += " {protocol}".format(**aces)
            if aces.get("source"):
                command = source_destination_common_config(
                    aces, command, "source"
                )
            if aces.get("destination"):
                command = source_destination_common_config(
                    aces, command, "destination"
                )
            if proto_option:
                command += " {0}".format(
                    list(proto_option.keys())[0].replace("_", "-")
                )
            if aces.get("dscp"):
                command += " dscp {dscp}".format(**aces)
            if aces.get("sequence") and config_data.get("afi") == "ipv6":
                command += " sequence {sequence}".format(**aces)
            if aces.get("fragments"):
                command += " fragments {fragments}".format(**aces)
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
        return command


class AclsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(AclsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "acls_name",
            "getval": re.compile(
                r"""^(?P<acl_type>Standard|Extended)*
                    \s*(?P<afi>IP|IPv6)*
                    \s*access*
                    \s*list*
                    \s*(?P<acl_name>.+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": _tmplt_access_list_name,
            "result": {
                "acls": {
                    "{{ acl_name|d() }}": {
                        "name": "{{ acl_name }}",
                        "acl_type": "{{ acl_type.lower() if acl_type is defined }}",
                        "afi": "{{ 'ipv4' if afi == 'IP' else 'ipv6' }}",
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "_acls_name",
            "getval": re.compile(
                r"""^(ip|ipv6)
                    (\s(access-list))
                    (\s(standard|extended))
                    (\s(?P<acl_name_r>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "ip access-list",
            "result": {},
            "shared": True,
        },
        {
            "name": "remarks",
            "getval": re.compile(
                r"""\s+remark
                    (\s(?P<remarks>.+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "remark {{ remarks }}",
            "result": {
                "acls": {
                    "{{ acl_name_r|d() }}": {
                        "name": "{{ acl_name_r }}",
                        "aces": [{"remarks": ["{{ remarks }}"]}],
                    }
                }
            },
        },
        {
            "name": "remarks_type_linear",
            "getval": re.compile(
                r"""^(access-list)
                    (\s(?P<acl_name_linear>\S+))?
                    (\sremark\s(?P<remarks>.+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "remark {{ remarks }}",
            "result": {
                "acls": {
                    "{{ acl_name_linear|d() }}": {
                        "name": "{{ acl_name_linear }}",
                        "aces": [{"remarks": ["{{ remarks }}"]}],
                    }
                }
            },
        },
        {
            "name": "aces_ipv4_standard",
            "getval": re.compile(
                r"""\s*(?P<sequence>\d+)*
                        \s(?P<grant>deny|permit)?
                        (\s+(?P<address>(?!ahp|eigrp|esp|gre|icmp|igmp|ipv6|ipinip|ip|nos|object-group|ospf|pcp|pim|sctp|tcp|udp)\S+|\S+,))?
                        (\s*(?P<any>any))?
                        (\shost\s(?P<host>\S+))?
                        (,\swildcard\sbits\s(?P<wildcard>\S+))?
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
                                    "host": "{{ host }}",
                                },
                                "log": {"set": "{{ not not log }}"},
                            }
                        ],
                    }
                }
            },
        },
        {
            "name": "aces",
            "getval": re.compile(
                r"""\s*(?P<sequence>\d+)*
                        \s*(?P<grant>deny|permit)*
                        (\sevaluate\s(?P<evaluate>\S+))?
                        (\s(?P<protocol>ahp|eigrp|esp|gre|icmp|igmp|ipv6|ipinip|ip|nos|object-group|ospf|pcp|pim|sctp|tcp|udp))?
                        (\s(?P<protocol_num>\d+))?
                        (\s(?P<source>(any|\S+\s\S+|host\s\S+|object-group\s\S+))?)
                        (\s(?P<source_port_protocol>(eq|gts|gt|lt|neq)\s(\S+|\d+)))?
                        (\s(?P<destination>(any|\S+\s\S+|host\s\S+|object-group\s\S+))?)
                        (\s(?P<dest_port_protocol>(eq|gts|lt|neq)\s(\S+|\d+)))?
                        (\s(?P<icmp_igmp_tcp_protocol>administratively-prohibited|alternate-address|conversion-error|dod-host-prohibited|dod-net-prohibited|echo|echo-reply|general-parameter-problem|host-isolated|host-precedence-unreachable|host-redirect|host-tos-redirect|host-tos-unreachable|host-unknown|host-unreachable|information-reply|information-request|mask-reply|mask-request|mobile-redirect|net-redirect|net-tos-redirect|net-tos-unreachable|net-unreachable|network-unknown|no-room-for-option|option-missing|packet-too-big|parameter-problem|port-unreachable|precedence-unreachable|protocol-unreachable|reassembly-timeout|redirect|router-advertisement|router-solicitation|source-quench|source-route-failed|time-exceeded|timestamp-reply|timestamp-request|traceroute|ttl-exceeded|unreachable|dvmrp|host-query|mtrace-resp|mtrace-route|pim|trace|v1host-report|v2host-report|v2leave-group|v3host-report|ack|established|fin|psh|rst|syn|urg))?
                        (\sdscp\s(?P<dscp>\S+))?
                        (\sfragments\s(?P<fragment>\S+))?
                        (\s(?P<log_input>log-input\s\(tag\s=\s\S+\)|log-input))?
                        (\s(?P<log>log\s\(tag\s=\s\S+\)|log))?
                        (\soption\s(?P<option>\S+|\d+))?
                        (\sprecedence\s(?P<precedence>\S+|\d+))?
                        (\stime-range\s(?P<time_range>\S+))?
                        (\stos\s(?P<tos>\S+|\d+))?
                        (\sttl\seq\s(?P<ttl_eq>\d+))?
                        (\sttl\sgt\s(?P<ttl_gt>\d+))?
                        (\sttl\slt\s(?P<ttl_lt>\d+))?
                        (\sttl\sneg\s(?P<ttl_neg>\d+))?
                        (\ssequence\s(?P<sequence_ipv6>\d+))?
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
                                    "address": "{% if source is defined and '.' in source and 'host' not in source %}{{\
                                        source.split(' ')[0] }}{% elif source is defined and '::' in source %}{{ source }}{% endif %}",
                                    "wildcard_bits": "{{ source.split(' ')[1] if source is defined and '.' in source and 'host' not in source }}",
                                    "any": "{{ True if source is defined and source == 'any' }}",
                                    "host": "{{ source.split(' ')[1] if source is defined and 'host' in source }}",
                                    "object_group": "{{ source.split(' ')[1] if source is defined and 'object-group' in source }}",
                                    "port_protocol": {
                                        "{{ source_port_protocol.split(' ')[0] if source_port_protocol is defined else None }}": "{{\
                                            source_port_protocol.split(' ')[1] if source_port_protocol is defined else None }}"
                                    },
                                },
                                "destination": {
                                    "address": "{% if destination is defined and '.' in destination and 'host' not in destination %}{{\
                                        destination.split(' ')[0] }}{% elif std_dest is defined and '.' in std_dest and 'host' not in std_dest %}{{\
                                            std_dest.split(' ')[0] }}{% elif destination is defined and '::' in destination %}{{ destination }}{% endif %}",
                                    "wildcard_bits": "{% if destination is defined and '.' in destination and 'host' not in destination %}{{\
                                        destination.split(' ')[1] }}{% elif std_dest is defined and '.' in std_dest and 'host' not in std_dest %}{{\
                                            std_dest.split(' ')[1] }}{% endif %}",
                                    "any": "{{ True if destination is defined and destination == 'any' else None }}",
                                    "host": "{{ destination.split(' ')[1] if destination is defined and 'host' in destination }}",
                                    "object_group": "{{ destination.split(' ')[1] if destination is defined and 'object-group' in destination else None }}",
                                    "port_protocol": {
                                        "{{ dest_port_protocol.split(' ')[0] if dest_port_protocol is defined else None }}": "{{\
                                            dest_port_protocol.split(' ')[1] if dest_port_protocol is defined else None }}"
                                    },
                                },
                                "dscp": "{{ dscp }}",
                                "fragments": "{{ fragments }}",
                                "log": {
                                    "set": "{{ True if log is defined and 'tag' not in log }}",
                                    "user_cookie": "{{ log.split(' ')[-1].split(')')[0] if log is defined and 'tag' in log }}",
                                },
                                "log_input": {
                                    "set": "{{ True if log_input is defined and 'tag' not in log_input }}",
                                    "user_cookie": "{{ log_input.split(' ')[-1].split(')')[0] if log_input is defined and 'tag' in log_input }}",
                                },
                                "option": {
                                    "{{ option if option is defined else None }}": "{{ True if option is defined else None }}"
                                },
                                "precedence": "{{ precedence }}",
                                "time_range": "{{ time_range }}",
                                "tos": {
                                    "max_reliability": "{{ True if tos is defined and 'max-reliability' in tos }}",
                                    "max_throughput": "{{ True if tos is defined and 'max-throughput' in tos }}",
                                    "min_delay": "{{ True if tos is defined and 'min-delay' in tos }}",
                                    "min_monetary_cost": "{{ True if tos is defined and 'min-monetary-cost' in tos }}",
                                    "normal": "{{ True if tos is defined and 'normal' in tos }}",
                                    "service_value": "{{ tos if tos is defined }}",
                                },
                                "ttl": {
                                    "eq": "{{ ttl_eq }}",
                                    "gt": "{{ ttl_gt }}",
                                    "lt": "{{ ttl_lt }}",
                                    "neq": "{{ ttl_neq }}",
                                },
                            }
                        ],
                    }
                }
            },
        },
    ]
