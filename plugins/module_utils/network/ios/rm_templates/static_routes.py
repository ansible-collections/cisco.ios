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
                (\s(?P<forward_router_address>\S+))
                (\s(?P<distance_metric>\d+))?
                (\stag\s(?P<tag>\d+))?
                (\s(?P<permanent>permanent))?
                (\sname\s(?P<next_hop_name>\S+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<multicast>multicast))?
                (\s(?P<dhcp>dhcp))?
                (\s(?P<global>global))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
            },
            "shared": True
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
                (\s(?P<forward_router_address>\S+))
                (\s(?P<distance_metric>\d+))?
                (\s(?P<multicast>multicast))?
                (\s(?P<unicast>unicast))?
                (\stag\s(?P<tag>\d+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<permanent>permanent))?
                (\sname\s(?P<next_hop_name>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
            },
        },
    ]
    # fmt: on


#   (ACR|ATM-ACR|Analysis-Module|AppNav-Compress|AppNav-UnCompress|Async|Auto-Template|BD-VIF|BDI|BVI|Bluetooth|CDMA-Ix|CEM-ACR|CEM-PG|CTunnel|Container|Dialer|EsconPhy|Ethernet-Internal|Fcpa|Filter|Filtergroup|GigabitEthernet|IMA-ACR|LongReachEthernet|Loopback|Lspvif|MFR|Multilink|NVI|Null|PROTECTION_GROUP|Port-channel|Portgroup|Pos-channel|SBC|SDH_ACR|SERIAL-ACR|SONET_ACR|SSLVPN-VIF|SYSCLOCK|Serial-PG|Service-Engine|TLS-VIF|Tunnel|VPN|Vif|Vir-cem-ACR|Virtual-PPP|Virtual-TokenRing)

# test_cisco(config)#do show running-config | include ip route|ipv6 route
# ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.12 34 tag 22 name nm12 track 11
# ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route track 150
# ip route 198.51.100.0 255.255.255.0 198.51.101.20 175 tag 70 name replaced_route track 150
# ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
# ip route 198.51.100.0 255.255.255.0 GigabitEthernet2 198.51.101.11 22 tag 22 permanent name nm1 multicast
# ipv6 route 2001:DB8:0:3::/64 GigabitEthernet4 multicast permanent name onlyname
# ipv6 route 2001:DB8:0:3::/64 GigabitEthernet3 unicast tag 11 permanent name qq
# ipv6 route 2001:DB8:0:3::/64 GigabitEthernet2 tag 2 permanent name nm1
# ipv6 route 2001:DB8:0:3::/64 Null0
# ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::3 22 multicast permanent name pp1
# ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 22 track 22 name name1
