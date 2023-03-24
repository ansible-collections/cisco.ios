# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Static_routes parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Static_routesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Static_routesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "ipv4",
            "getval": re.compile(
                r"""
                ^ip\sroute
                (\stopology\s(?P<topology>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<dest>\S+))
                (\s(?P<netmask>\S+))
                (\s(?P<interface>(ACR|ATM-ACR|Analysis-Module|AppNav-Compress|AppNav-UnCompress|Async|Auto-Template|BD-VIF|BDI|BVI|Bluetooth|CDMA-Ix|CEM-ACR|CEM-PG|CTunnel|Container|Dialer|EsconPhy|Ethernet-Internal|Fcpa|Filter|Filtergroup|GigabitEthernet|IMA-ACR|LongReachEthernet|Loopback|Lspvif|MFR|Multilink|NVI|Null|PROTECTION_GROUP|Port-channel|Portgroup|Pos-channel|SBC|SDH_ACR|SERIAL-ACR|SONET_ACR|SSLVPN-VIF|SYSCLOCK|Serial-PG|Service-Engine|TLS-VIF|Tunnel|VPN|Vif|Vir-cem-ACR|Virtual-PPP|Virtual-TokenRing)\d+))?
                (\s(?P<forward_router_address>(?!multicast|dhcp|global|tag|track|permanent|name)\S+))?
                (\s(?P<distance_metric>\d+))?
                (\stag\s(?P<tag>\d+))?
                (\s(?P<permanent>permanent))?
                (\sname\s(?P<next_hop_name>\S+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<multicast>multicast))?
                (\s(?P<dhcp>dhcp))?
                (\s(?P<global>global))?
                $""", re.VERBOSE),
            "setval": "ip route"
            "{{ (' topology ' + topology) if topology is defined else '' }}"
            "{{ (' vrf ' + vrf) if vrf is defined else '' }}"
            "{{ (' ' + dest) if dest is defined else '' }}"
            "{{ (' ' + netmask) if netmask is defined else '' }}"
            "{{ (' ' + interface) if interface is defined else '' }}"
            "{{ (' ' + forward_router_address) if forward_router_address is defined else '' }}"
            "{{ (' ' + distance_metric|string) if distance_metric is defined else '' }}"
            "{{ (' tag ' + tag|string) if tag is defined else '' }}"
            "{{ (' permanent' ) if permanent|d(False) else '' }}"
            "{{ (' name ' + name) if name is defined else '' }}"
            "{{ (' track ' + track|string) if track is defined else '' }}"
            "{{ (' multicast' ) if multicast|d(False) else '' }}"
            "{{ (' dhcp' ) if dhcp|d(False) else '' }}"
            "{{ (' global' ) if global|d(False) else '' }}",
            "result": {
                "{{ dest }}_{{ vrf|d() }}_{{ topology|d() }}_ipv4": [
                    {
                        "_vrf" : "{{ vrf }}",
                        "_topology" : "{{ topology }}",
                        "_afi": "ipv4",
                        "_dest": "{{ dest }}",
                        "_netmask": "{{ netmask }}",
                        "interface": "{{ interface }}",
                        "forward_router_address": "{{ forward_router_address }}",
                        "distance_metric": "{{ distance_metric }}",
                        "tag": "{{ tag }}",
                        "permanent": "{{ not not permanent }}",
                        "name": "{{ next_hop_name }}",
                        "track": "{{ track }}",
                        "multicast": "{{ not not multicast }}",
                        "dhcp": "{{ not not dhcp }}",
                        "global": "{{ not not global }}",
                    },
                ],
            },
        },
        {
            "name": "ipv6",
            "getval": re.compile(
                r"""
                ^ipv6\sroute
                (\stopology\s(?P<topology>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<dest>\S+))
                (\s(?P<interface>(ACR|ATM-ACR|Analysis-Module|AppNav-Compress|AppNav-UnCompress|Async|Auto-Template|BD-VIF|BDI|BVI|Bluetooth|CDMA-Ix|CEM-ACR|CEM-PG|CTunnel|Container|Dialer|EsconPhy|Ethernet-Internal|Fcpa|Filter|Filtergroup|GigabitEthernet|IMA-ACR|LongReachEthernet|Loopback|Lspvif|MFR|Multilink|NVI|Null|PROTECTION_GROUP|Port-channel|Portgroup|Pos-channel|SBC|SDH_ACR|SERIAL-ACR|SONET_ACR|SSLVPN-VIF|SYSCLOCK|Serial-PG|Service-Engine|TLS-VIF|Tunnel|VPN|Vif|Vir-cem-ACR|Virtual-PPP|Virtual-TokenRing)\d+))?
                (\s(?P<forward_router_address>(?!multicast|unicast|tag|track|permanent|name)\S+))?
                (\s(?P<distance_metric>\d+))?
                (\s(?P<multicast>multicast))?
                (\s(?P<unicast>unicast))?
                (\stag\s(?P<tag>\d+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<permanent>permanent))?
                (\sname\s(?P<next_hop_name>\S+))?
                $""", re.VERBOSE),
            "setval": "ipv6 route"
            "{{ (' topology ' + topology) if topology is defined else '' }}"
            "{{ (' vrf ' + vrf) if vrf is defined else '' }}"
            "{{ (' ' + dest) if dest is defined else '' }}"
            "{{ (' ' + interface) if interface is defined else '' }}"
            "{{ (' ' + forward_router_address) if forward_router_address is defined else '' }}"
            "{{ (' ' + distance_metric|string) if distance_metric is defined else '' }}"
            "{{ (' multicast' ) if multicast|d(False) else '' }}"
            "{{ (' unicast' ) if unicast|d(False) else '' }}"
            "{{ (' tag ' + tag|string) if tag is defined else '' }}"
            "{{ (' track ' + track|string) if track is defined else '' }}"
            "{{ (' permanent' ) if permanent|d(False) else '' }}"
            "{{ (' name ' + name) if name is defined else '' }}",
            "result": {
                "{{ dest }}_{{ vrf|d() }}_{{ topology|d() }}_ipv6": [
                    {
                        "_vrf" : "{{ vrf }}",
                        "_topology" : "{{ topology }}",
                        "_afi": "ipv6",
                        "_dest": "{{ dest }}",
                        "interface": "{{ interface }}",
                        "forward_router_address": "{{ forward_router_address }}",
                        "distance_metric": "{{ distance_metric }}",
                        "tag": "{{ tag }}",
                        "permanent": "{{ not not permanent }}",
                        "name": "{{ next_hop_name }}",
                        "track": "{{ track }}",
                        "multicast": "{{ not not multicast }}",
                        "unicast": "{{ not not unicast }}",
                    },
                ],
            },
        },
    ]
    # fmt: on
