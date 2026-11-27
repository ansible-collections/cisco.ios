# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Radius_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_SERVERS = "servers"
_SERVER = "{{ name }}"
_ATTRS = "attributes"
_ATTR = "{{ number }}"


def _address(data):
    """address ipv4|ipv6 <host> auth-port N acct-port N, the ports of IOS are 1812 and 1813."""
    addr = data["address"]
    family = "ipv4" if addr.get("ipv4") else "ipv6"
    return "address {0} {1} auth-port {2} acct-port {3}".format(
        family,
        addr[family],
        addr.get("auth_port", 1812),
        addr.get("acct_port", 1813),
    )


def _dead_criteria(data):
    criteria = data["dead_criteria"]
    cmd = "radius-server dead-criteria"
    if criteria.get("time") is not None:
        cmd += " time {0}".format(criteria["time"])
    if criteria.get("tries") is not None:
        cmd += " tries {0}".format(criteria["tries"])
    return cmd


def _attribute(name, keyword, option):
    return {
        "name": name,
        "getval": re.compile(
            r"^radius-server\sattribute\s(?P<number>\d+)\s" + keyword + r"$",
        ),
        "setval": "radius-server attribute {{ number }} " + keyword.replace("\\s", " "),
        "compval": option,
        "result": {
            _ATTRS: {
                _ATTR: {
                    "number": "{{ number | int }}",
                    option: True,
                },
            },
        },
    }


class Radius_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Radius_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "timeout",
            "getval": re.compile(r"^radius-server\stimeout\s(?P<timeout>\d+)$"),
            "setval": "radius-server timeout {{ timeout }}",
            "remval": "radius-server timeout",
            "result": {"timeout": "{{ timeout | int }}"},
        },
        {
            "name": "retransmit",
            "getval": re.compile(r"^radius-server\sretransmit\s(?P<retransmit>\d+)$"),
            "setval": "radius-server retransmit {{ retransmit }}",
            "remval": "radius-server retransmit",
            "result": {"retransmit": "{{ retransmit | int }}"},
        },
        {
            "name": "deadtime",
            "getval": re.compile(r"^radius-server\sdeadtime\s(?P<deadtime>\d+)$"),
            "setval": "radius-server deadtime {{ deadtime }}",
            "remval": "radius-server deadtime",
            "result": {"deadtime": "{{ deadtime | int }}"},
        },
        {
            "name": "dead_criteria",
            "getval": re.compile(
                r"""^radius-server\sdead-criteria
                    (\stime\s(?P<time>\d+))?
                    (\stries\s(?P<tries>\d+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": _dead_criteria,
            "remval": "radius-server dead-criteria",
            "result": {
                "dead_criteria": {
                    "time": "{{ time | int if time is defined }}",
                    "tries": "{{ tries | int if tries is defined }}",
                },
            },
        },
        {
            "name": "load_balance",
            "getval": re.compile(r"^radius-server\sload-balance\smethod\sleast-outstanding(\s.*)?$"),
            "setval": "radius-server load-balance method least-outstanding",
            "result": {"load_balance": {"method": "least_outstanding"}},
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""^ip\sradius\ssource-interface\s(?P<ifname>\S+)
                    (\svrf\s(?P<vrf>\S+))?
                    \s*$""",
                re.VERBOSE,
            ),
            "setval": "ip radius source-interface {{ source_interface.name }}"
                      "{{ ' vrf ' + source_interface.vrf if source_interface.vrf is defined else '' }}",
            "result": {"source_interface": {"name": "{{ ifname }}", "vrf": "{{ vrf }}"}},
        },
        _attribute("attribute_on_for_login_auth", r"on-for-login-auth", "on_for_login_auth"),
        _attribute("attribute_access_request_include", r"access-request\sinclude", "access_request_include"),
        _attribute("attribute_include_in_access_req", r"include-in-access-req", "include_in_access_req"),
        _attribute("attribute_include_in_acct_req", r"include-in-acct-req", "include_in_acct_req"),
        {
            "name": "server",
            "getval": re.compile(r"^radius\sserver\s(?P<name>\S+)$"),
            "setval": "radius server {{ name }}",
            "result": {_SERVERS: {_SERVER: {"name": "{{ name }}"}}},
            "shared": True,
        },
        {
            "name": "server_address",
            "getval": re.compile(
                r"""^\s+address\s(?P<family>ipv4|ipv6)\s(?P<host>\S+)
                    (\sauth-port\s(?P<auth_port>\d+))?
                    (\sacct-port\s(?P<acct_port>\d+))?
                    \s*$""",
                re.VERBOSE,
            ),
            "setval": _address,
            "compval": "address",
            "result": {
                _SERVERS: {
                    _SERVER: {
                        "address": {
                            "ipv4": "{{ host if family == 'ipv4' }}",
                            "ipv6": "{{ host if family == 'ipv6' }}",
                            "auth_port": "{{ auth_port | int if auth_port is defined }}",
                            "acct_port": "{{ acct_port | int if acct_port is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "server_key",
            "getval": re.compile(r"^\s+key(\s(?P<type>[067]))?\s(?P<value>\S+)\s*$"),
            "setval": "key {{ key.type | default(0) }} {{ key.value }}",
            "remval": "key",
            "compval": "key",
            "result": {
                _SERVERS: {
                    _SERVER: {
                        "key": {
                            "type": "{{ type | int if type is defined else 0 }}",
                            "value": "{{ value }}",
                        },
                    },
                },
            },
        },
        {
            "name": "server_timeout",
            "getval": re.compile(r"^\s+timeout\s(?P<timeout>\d+)\s*$"),
            "setval": "timeout {{ timeout }}",
            "remval": "timeout",
            "compval": "timeout",
            "result": {_SERVERS: {_SERVER: {"timeout": "{{ timeout | int }}"}}},
        },
        {
            "name": "server_retransmit",
            "getval": re.compile(r"^\s+retransmit\s(?P<retransmit>\d+)\s*$"),
            "setval": "retransmit {{ retransmit }}",
            "remval": "retransmit",
            "compval": "retransmit",
            "result": {_SERVERS: {_SERVER: {"retransmit": "{{ retransmit | int }}"}}},
        },
    ]
    # fmt: on
