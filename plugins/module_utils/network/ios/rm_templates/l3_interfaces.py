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


class L3_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L3_interfacesTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
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
            "name": "ipv4.dhcp",
            "getval": re.compile(
                r"""\s+ip\saddress\s
                    ((?P<dhcp>dhcp))
                    (\sclient-id\s(?P<client_id>\S+))?
                    (\shostname\s(?P<hostname>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "ip address dhcp"
            "{{ (' client-id ' + ipv4.dhcp.client_id) if ipv4.dhcp.client_id is defined else ''}}"
            "{{ (' hostname ' + ipv4.dhcp.hostname) if ipv4.dhcp.hostname is defined else ''}}",
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
            "setval": "ipv6 address autoconfig"
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
            "setval": "ipv6 address dhcp"
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
    ]
    # fmt: on
