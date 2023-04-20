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
                $""", re.VERBOSE,
            ),
            "setval": "ip route"
            "{{ (' topology ' + ipv4.topology) if ipv4.topology is defined else '' }}"
            "{{ (' vrf ' + ipv4.vrf) if ipv4.vrf is defined else '' }}"
            "{{ (' ' + ipv4.dest) if ipv4.dest is defined else '' }}"
            "{{ (' ' + ipv4.interface) if ipv4.interface is defined else '' }}"
            "{{ (' ' + ipv4.forward_router_address) if ipv4.forward_router_address is defined else '' }}"
            "{{ (' ' + ipv4.distance_metric|string) if ipv4.distance_metric is defined else '' }}"
            "{{ (' tag ' + ipv4.tag|string) if ipv4.tag is defined else '' }}"
            "{{ (' permanent' ) if ipv4.permanent|d(False) else '' }}"
            "{{ (' name ' + ipv4.name) if ipv4.name is defined else '' }}"
            "{{ (' track ' + ipv4.track|string) if ipv4.track is defined else '' }}"
            "{{ (' multicast' ) if ipv4.multicast|d(False) else '' }}"
            "{{ (' dhcp' ) if ipv4.dhcp|d(False) else '' }}"
            "{{ (' global' ) if ipv4.global|d(False) else '' }}",
            "result": {
                "{{ dest }}_{{ vrf|d() }}_{{ topology|d() }}_ipv4": [
                    {
                        "_vrf": "{{ vrf }}",
                        "_topology": "{{ topology }}",
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
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 route"
            "{{ (' topology ' + ipv6.topology) if ipv6.topology is defined else '' }}"
            "{{ (' vrf ' + ipv6.vrf) if ipv6.vrf is defined else '' }}"
            "{{ (' ' + ipv6.dest) if ipv6.dest is defined else '' }}"
            "{{ (' ' + ipv6.interface) if ipv6.interface is defined else '' }}"
            "{{ (' ' + ipv6.forward_router_address) if ipv6.forward_router_address is defined else '' }}"
            "{{ (' ' + ipv6.distance_metric|string) if ipv6.distance_metric is defined else '' }}"
            "{{ (' multicast' ) if ipv6.multicast|d(False) else '' }}"
            "{{ (' unicast' ) if ipv6.unicast|d(False) else '' }}"
            "{{ (' tag ' + ipv6.tag|string) if ipv6.tag is defined else '' }}"
            "{{ (' track ' + ipv6.track|string) if ipv6.track is defined else '' }}"
            "{{ (' permanent' ) if ipv6.permanent|d(False) else '' }}"
            "{{ (' name ' + ipv6.name) if ipv6.name is defined else '' }}",
            "result": {
                "{{ dest }}_{{ vrf|d() }}_{{ topology|d() }}_ipv6": [
                    {
                        "_vrf": "{{ vrf }}",
                        "_topology": "{{ topology }}",
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
