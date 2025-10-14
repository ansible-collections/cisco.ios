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
    cmd = "ipv6 address {ip}"
    if config_data.get("ipv6"):
        config = config_data.get("ipv6")
        cmd = cmd.format(ip=config["address"])
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


def ipv4_dhcp(config_data):
    _data = config_data.get("ipv4", {}).get("dhcp")
    if not _data.get("enable", True):
        return ""
    cmd = "ip address dhcp"
    if _data.get("client_id"):
        cmd += " client-id {client_id}".format(**_data)
    if _data.get("hostname"):
        cmd += " hostname {hostname}".format(**_data)
    return cmd


class L3_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L3_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "autostate",
            "getval": re.compile(r"""\s+no\s+autostate$""", re.VERBOSE),
            "setval": "autostate",
            "result": {"{{ name }}": {"autostate": False}},
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""\s+mac-address
                    (\s(?P<mac_address>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "mac-address {{ mac_address }}",
            "result": {"{{ name }}": {"mac_address": "{{ mac_address }}"}},
        },
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
            "name": "helper_addresses_ipv4",
            "getval": re.compile(
                r"""
                ^\s*ip\s+helper-address
                (\s(?P<global>global))?
                (\svrf\s(?P<vrf>\S+))?
                \s+(?P<destination_ip>\S+)
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ip helper-address "
                      "{{ 'global ' if ipv4.global|d(False) else ''}}"
                      "{{ 'vrf ' + ipv4.vrf|string + ' ' if ipv4.vrf is defined else ''}}"
                      "{{ ipv4.destination_ip|string }}",
            "compval": "ipv4",
            "result": {
                "{{ name }}": {
                    "helper_addresses": {
                        "ipv4": [{
                            "destination_ip": "{{ destination_ip }}",
                            "global": "{{ not not global }}",
                            "vrf": "{{ vrf }}",
                        }],
                    },
                },
            },
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
            "setval": "ip address {{ ipv4.address }}"
            "{{ ' secondary' if ipv4.secondary|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "address": "{{ ipv4 }}",
                            "netmask": "{{ netmask }}",
                            "secondary": "{{ True if secondary is defined }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv4.pool",
            "getval": re.compile(
                r"""
                \s+ip\saddress\spool\s(?P<pool>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "ip address pool {{ ipv4.pool }}",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "pool": "{{ pool }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv4.mtu",
            "getval": re.compile(
                r"""
                \s+ip\smtu\s(?P<mtu>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip mtu {{ ipv4.mtu }}",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "mtu": "{{ mtu }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv4.redirects",
            "getval": re.compile(
                r"""
                \s+ip\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "ip redirects",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "redirects": True,
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv4.unreachables",
            "getval": re.compile(
                r"""
                \s+ip\sunreachables
                $""", re.VERBOSE,
            ),
            "setval": "ip unreachables",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "unreachables": True,
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv4.proxy_arp",
            "getval": re.compile(
                r"""
                \s+ip\sproxy-arp
                $""", re.VERBOSE,
            ),
            "setval": "ip proxy-arp",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "proxy_arp": True,
                        },
                    ],
                },
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
            "setval": ipv4_dhcp,
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
                    ],
                },
            },
        },
        {
            "name": "ipv4.source_interface",
            "getval": re.compile(
                r"""\s+ip\sunnumbered
                    (\s(?P<src_name>\S+))
                    (\s(?P<poll>poll))?
                    (\s(?P<point_to_point>point-to-point))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "ip unnumbered {{ ipv4.source_interface.name }}"
            "{{ ' poll' if ipv4.source_interface.poll|d(False) else ''}}"
            "{{ ' point-to-point' if ipv4.source_interface.point_to_point|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "source_interface": {
                                "name": "{{ src_name }}",
                                "poll": "{{ True if poll is defined }}",
                                "point_to_point": "{{ True if point_to_point is defined }}",
                            },
                        },
                    ],
                },
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
                    ],
                },
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
            "setval": "{{ 'ipv6 address autoconfig' if ipv6.autoconfig.enable|d(False) or ipv6.autoconfig.default|d(False) else ''}}"
            "{{ ' default' if ipv6.autoconfig.default|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {
                            "autoconfig": {
                                "enable": "{{ True if enable is defined }}",
                                "default": "{{ True if default is defined }}",
                            },
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv6.dhcp",
            "getval": re.compile(
                r"""\s+ipv6\saddress\sdhcp
                    (\s(?P<rapid_commit>rapid-commit))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": "{{ 'ipv6 address dhcp' if ipv6.dhcp.enable|d(False)|d(False) or ipv6.dhcp.rapid_commit|d(False)|d(False)else ''}}"
            "{{ ' rapid-commit' if ipv6.dhcp.rapid_commit|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {
                            "dhcp": {
                                "enable": True,
                                "rapid_commit": "{{ True if rapid_commit is defined }}",
                            },
                        },
                    ],
                },
            },
        },
        {
            "name": "ipv6.enable",
            "getval": re.compile(r"""\s+ipv6\s+enable$""", re.VERBOSE),
            "setval": "ipv6 enable",
            "result": {
                "{{ name }}": {
                    "ipv6": [
                        {"enable": True},
                    ],
                },
            },
        },
    ]
    # fmt: on
