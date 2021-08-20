# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The L3_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def ip_tmplt(config_data):
    cmd = "{tp} address {ip}"
    if config_data.get("ipv4"):
        config = config_data.get("ipv4")
        cmd = cmd.format(tp="ip", ip=config["address"])
    elif config_data.get("ipv6"):
        config = config_data.get("ipv6")
        cmd = cmd.format(tp="ipv6", ip=config["address"])
    if config.get("segment_routing"):
        # if config.get("segment_routing").get("enable"):
        cmd += " segment-routing"
        if config.get("segment_routing").get("default"):
            cmd += " default"
        if config.get("segment_routing").get("ipv6_sr"):
            cmd += " ipv6-sr"
    if config.get("secondary"):
        cmd += " secondary"
    if config.get("link_local"):
        cmd += " link-local"
    if config.get("anycast"):
        cmd += " anycast"
    if config.get("cga"):
        cmd += " cga"
    if config.get("eui"):
        cmd += " eui"
    return cmd


def autoconfig_tmplt(config_data):
    cmd = "ipv6 address autoconfig"
    if config_data["ipv6"].get("autoconfig"):
        config = config_data.get("ipv6").get("autoconfig")
        if config.get("default"):
            cmd = cmd + " default"
    return cmd


def dhcp_tmplt(config_data):
    cmd = "{tp} address dhcp"
    if config_data.get("ipv4"):
        config = config_data.get("ipv4").get("dhcp")
        cmd = cmd.format(tp="ip")
    elif config_data.get("ipv6"):
        config = config_data.get("ipv6").get("dhcp")
        cmd = cmd.format(tp="ipv6")
    if config.get("rapid_commit"):
        cmd += " rapid-commit"
    if config.get("client_id"):
        cmd += " client-id {cid}".format(cid=config.get("client_id"))
    if config.get("hostname"):
        cmd += " hostname {hnm}".format(hnm=config.get("hostname"))
    return cmd


class L3_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L3_interfacesTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "ipv4.address",
            "getval": re.compile(
                r"""\s+ip\saddress
                    (\s(?P<ipv4>\S+))
                    (\s(?P<netmask>\S+))
                    (\s(?P<secondary>secondary))?
                    $""",
                re.VERBOSE,
            ),
            "setval": ip_tmplt,
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "address": "{{ ipv4 }}",
                            "netmask": "{{ netmask }}",
                            "secondary": "{{ True if secondary is defined }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv4.pool",
            "getval": re.compile(
                r"""
                \s+ip\saddress\spool\s(?P<pool>.+$)
                $""", re.VERBOSE),
            "setval": "ip address pool {{ ipv4.pool }}",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "pool": "{{ pool }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv4.dhcp",
            "getval": re.compile(
                r"""\s+ip\saddress\s
                    ((?P<dhcp>dhcp))
                    (\sclient-id\s(?P<client_id>\S+))?
                    (\shostname\s(?P<hostname>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": dhcp_tmplt,
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "dhcp": {
                                "enable": "{{ True if dhcp is defined }}",
                                "client_id": "{{ client_id }}",
                                "hostname": "{{ hostname }}",
                            },
                        },
                    ]
                }
            },
        },
        {
            "name": "ipv6.address",
            "getval": re.compile(
                r"""\s+ipv6\saddress
                    (\s(?P<ipv6>\b(?!autoconfig\b)\S+))
                    (\s(?P<link_local>link-local))?
                    (\s(?P<anycast>anycast))?
                    (\s(?P<cga>cga))?
                    (\s(?P<eui>eui))?
                    (\s(?P<enable>segment-routing))?
                    (\s(?P<default>default))?
                    (\s(?P<ipv6_sr>ipv6-sr))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": ip_tmplt,
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {
                            "address": "{{ ipv6 }}",
                            "link_local": "{{ True if link_local is defined }}",
                            "anycast": "{{ True if anycast is defined }}",
                            "cga": "{{ True if cga is defined }}",
                            "eui": "{{ True if eui is defined }}",
                            "segment_routing": {
                                "enable": "{{ True if enable is defined }}",
                                "default": "{{ True if default is defined }}",
                                "ipv6_sr": "{{ True if ipv6_sr is defined }}",
                            },
                        },
                    ]
                }
            },
        },
        {
            "name": "ipv6.autoconfig",
            "getval": re.compile(
                r"""\s+ipv6\saddress\s
                    ((?P<enable>autoconfig))
                    (\s(?P<default>default))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": autoconfig_tmplt,
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {
                            "autoconfig": {
                                "enable": "{{ True if enable is defined }}",
                                "default": "{{ True if default is defined }}",
                            },
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv6.dhcp",
            "getval": re.compile(
                r"""\s+ipv6\saddress\s
                    ((?P<dhcp>dhcp))
                    (\s(?P<rapid_commit>rapid-commit))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": dhcp_tmplt,
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {
                            "dhcp": {
                                "enable": "{{ True if dhcp is defined }}",
                                "rapid_commit": "{{ True if rapid_commit is defined }}",
                            },
                        },
                    ]
                }
            },
        },
    ]
    # fmt: on
