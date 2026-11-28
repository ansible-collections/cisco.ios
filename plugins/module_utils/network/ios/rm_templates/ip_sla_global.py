# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ip_sla_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_OPS = "operations"
_OP_ID = "{{ operation_id }}"


def _option(name, regex, setval, value, remval=None):
    """Build the parser of an option indented under the operation type line."""
    parser = {
        "name": name,
        "getval": re.compile(rf"^\s+{regex}$"),
        "setval": setval,
        "result": {_OPS: {_OP_ID: {name: value}}},
    }
    if remval:
        parser["remval"] = remval
    return parser


class Ip_sla_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ip_sla_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "logging_traps",
            "getval": re.compile(r"^ip\ssla\slogging\straps$"),
            "setval": "ip sla logging traps",
            "result": {"logging_traps": True},
        },
        {
            "name": "enable_reaction_alerts",
            "getval": re.compile(r"^ip\ssla\senable\sreaction-alerts$"),
            "setval": "ip sla enable reaction-alerts",
            "result": {"enable_reaction_alerts": True},
        },
        {
            "name": "operation_id",
            "getval": re.compile(r"^ip\ssla\s(?P<operation_id>\d+)$"),
            "setval": "ip sla {{ operation_id }}",
            "result": {_OPS: {_OP_ID: {"operation_id": "{{ operation_id | int }}"}}},
            "shared": True,
        },
        {
            "name": "schedule",
            "getval": re.compile(
                r"""^ip\ssla\sschedule\s(?P<operation_id>\d+)
                    (\slife\s(?P<life>forever|\d+))?
                    (\sstart-time\s(?P<start_time>now|pending|none|after\s\S+|\d\S*(\s[A-Za-z]+\s\d+)?))?
                    (\sageout\s(?P<ageout>\d+))?
                    (\s(?P<recurring>recurring))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "ip sla schedule {{ operation_id }}"
                      "{% if schedule.life is defined %} life {{ schedule.life }}{% endif %}"
                      "{% if schedule.start_time is defined %} start-time {{ schedule.start_time }}{% endif %}"
                      "{% if schedule.ageout is defined %} ageout {{ schedule.ageout }}{% endif %}"
                      "{% if schedule.recurring is defined and schedule.recurring %} recurring{% endif %}",
            "remval": "ip sla schedule {{ operation_id }}",
            "result": {
                _OPS: {
                    _OP_ID: {
                        "operation_id": "{{ operation_id | int }}",
                        "schedule": {
                            "life": "{{ life }}",
                            "start_time": "{{ start_time }}",
                            "ageout": "{{ ageout | int if ageout is defined }}",
                            "recurring": "{{ True if recurring is defined }}",
                        },
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "icmp_echo",
            "getval": re.compile(
                r"""^\sicmp-echo\s(?P<destination>\S+)
                    (\ssource-ip\s(?P<source_ip>\S+))?
                    (\ssource-interface\s(?P<source_interface>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "icmp-echo {{ icmp_echo.destination }}"
                      "{% if icmp_echo.source_ip is defined %} source-ip {{ icmp_echo.source_ip }}{% endif %}"
                      "{% if icmp_echo.source_interface is defined %} source-interface {{ icmp_echo.source_interface }}{% endif %}",
            "result": {
                _OPS: {
                    _OP_ID: {
                        "icmp_echo": {
                            "destination": "{{ destination }}",
                            "source_ip": "{{ source_ip }}",
                            "source_interface": "{{ source_interface }}",
                        },
                    },
                },
            },
        },
        {
            "name": "tcp_connect",
            "getval": re.compile(
                r"""^\stcp-connect\s(?P<destination>\S+)\s(?P<port>\d+)
                    (\ssource-ip\s(?P<source_ip>\S+))?
                    (\ssource-port\s(?P<source_port>\d+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "tcp-connect {{ tcp_connect.destination }} {{ tcp_connect.port }}"
                      "{% if tcp_connect.source_ip is defined %} source-ip {{ tcp_connect.source_ip }}{% endif %}"
                      "{% if tcp_connect.source_port is defined %} source-port {{ tcp_connect.source_port }}{% endif %}",
            "result": {
                _OPS: {
                    _OP_ID: {
                        "tcp_connect": {
                            "destination": "{{ destination }}",
                            "port": "{{ port | int }}",
                            "source_ip": "{{ source_ip }}",
                            "source_port": "{{ source_port | int if source_port is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "http",
            "getval": re.compile(r"^\shttp\s(?P<method>get|raw)\s(?P<url>\S+)$"),
            "setval": "http {{ http.method }} {{ http.url }}",
            "result": {_OPS: {_OP_ID: {"http": {"method": "{{ method }}", "url": "{{ url }}"}}}},
        },
        {
            # the single payload line inside the "http-raw-request" block
            "name": "http_raw_request",
            "getval": re.compile(r"^\s{3}(?!exit$)(?P<raw_request>\S.*)$"),
            "setval": "http-raw-request",
            "remval": "http-raw-request",
            "compval": "http.raw_request",
            "result": {_OPS: {_OP_ID: {"http": {"raw_request": "{{ raw_request }}"}}}},
        },
        _option("vrf", r"vrf\s(?P<vrf>\S+)", "vrf {{ vrf }}", "{{ vrf }}", "vrf"),
        _option(
            "frequency", r"frequency\s(?P<frequency>\d+)", "frequency {{ frequency }}",
            "{{ frequency | int }}", "frequency",
        ),
        _option(
            "threshold", r"threshold\s(?P<threshold>\d+)", "threshold {{ threshold }}",
            "{{ threshold | int }}", "threshold",
        ),
        _option(
            "timeout", r"timeout\s(?P<timeout>\d+)", "timeout {{ timeout }}",
            "{{ timeout | int }}", "timeout",
        ),
        _option("tag", r"tag\s(?P<tag>.+)", "tag {{ tag }}", "{{ tag }}", "tag"),
        _option("owner", r"owner\s(?P<owner>.+)", "owner {{ owner }}", "{{ owner }}", "owner"),
        _option(
            "request_data_size", r"request-data-size\s(?P<request_data_size>\d+)",
            "request-data-size {{ request_data_size }}", "{{ request_data_size | int }}",
            "request-data-size",
        ),
        _option("tos", r"tos\s(?P<tos>\d+)", "tos {{ tos }}", "{{ tos | int }}", "tos"),
        {
            # Last parser on purpose: any operation type line (one space indent) that the
            # parsers above did not accept, e.g. udp-jitter or "http get" with extra options.
            "name": "unsupported_type",
            "getval": re.compile(r"^\s(?P<other>[a-z]\S*.*)$"),
            "setval": "",
            "result": {_OPS: {_OP_ID: {"unsupported": True}}},
        },
    ]
    # fmt: on
