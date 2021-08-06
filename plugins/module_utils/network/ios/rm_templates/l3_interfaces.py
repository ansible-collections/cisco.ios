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


class L3_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L3_interfacesTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {  #ipv4
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
                    (\s(?P<ipv4>\S+))?
                    (\s(?P<netmask>\S+))?
                    (\s(?P<secondary>secondary))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "ip address 10.1.1.2 255.255.255.0 secondary",
            "compval": "ipv4",
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
            "setval": "ip address pool Floor1 ww",
            "compval": "ipv4",
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
            "name": "ipv4.dhcp_config",
            "getval": re.compile(
                r"""\s+ip\saddress\sdhcp
                    (\sclient-id\s(?P<client_id>\S+))?
                    (\shostname\s(?P<hostname>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": " ip address dhcp client-id GigabitEthernet0/2 hostname test.com",
            "compval": "ipv4",
            "result": {
                "{{ name }}": {
                    "ipv4": [{
                            "dhcp_config": {
                                "client_id": "{{ client_id }}",
                                "hostname": "{{ hostname }}",
                            }
                        }
                    ]
                }
            },
        },
        {  #ipv6
            "name": "ipv6.address",
            "getval": re.compile(
                r"""\s+ipv6\saddress
                    (\s(?P<ipv6>\S+))?
                    (\s(?P<link_local>link-local))?
                    (\s(?P<anycast>anycast))?
                    (\s(?P<cga>cga))?
                    (\s(?P<eui>eui))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": "ipv6 address FD5D:12C9:2201:1::1/64 link-local",
            "compval": "ipv6",
            "result": {
                "{{ name }}": {
                    "ipv6": [{
                        "address": "{{ ipv6 }}",
                        "link_local": "{{ True if link_local is defined }}",
                        "anycast": "{{ True if anycast is defined }}",
                        "cga": "{{ True if cga is defined }}",
                        "eui": "{{ True if eui is defined }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv6.segment_routing",
            "getval": re.compile(
                r"""\s+ipv6\saddress
                    (\s(?P<ipv6>\S+))
                    (\s(?P<enable>segment-routing))
                    (\s(?P<default>default))?
                    (\s(?P<ipv6_sr>ipv6-sr))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": "ipv6 address FD5D:12C9:2201:1::1/64 segment_routing default",
            "compval": "ipv6",
            "result": {
                "{{ name }}": {
                    "ipv6": [{
                        "address": "{{ ipv6 }}",
                        "segment_routing":{
                            "enable": "{{ True if enable is defined }}",
                            "default": "{{ True if default is defined }}",
                            "ipv6_sr": "{{ True if ipv6_sr is defined }}",
                            }
                        }
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
            "setval": "ipv6 address autoconfig default",
            "compval": "ipv6",
            "result": {
                "{{ name }}": {
                    "ipv6": [{
                        "enable": "{{ True if enable is defined }}",
                        "default": "{{ True if default is defined }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv6.dhcp_config",
            "getval": re.compile(
                r"""\s+ipv6\saddress\s
                    ((?P<dhcp>dhcp))
                    (\s(?P<rapid_commit>rapid-commit))?
                    $""",
                    re.VERBOSE,
            ),
            "setval": "ipv6 address dhcp",
            "compval": "ipv6",
            "result": {
                "{{ name }}": {
                    "ipv6": [{
                        "dhcp_config": {
                            "enable": "{{ True if dhcp is defined }}",
                            "rapid_commit": "{{ True if rapid_commit is defined }}",
                            }
                        }
                    ]
                }
            },
        },
    ]
    # fmt: on
