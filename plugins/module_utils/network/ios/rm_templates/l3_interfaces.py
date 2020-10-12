from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)
import q


def _tmplt_l3_interface(config_data):
    command = "interface {name}".format(**config_data)
    return command


def _tmplt_l3_ipv4(config_data):
    from netaddr import IPNetwork
    if "ipv4" in config_data:
        command = []
        for each in config_data['ipv4']:
            cmd = "ip address"
            address = each.get('address')
            if address and address != 'dhcp':
                ip = IPNetwork(address)
                cmd += " {0} {1}".format(str(ip.ip), str(ip.netmask))
                if each.get('secondary'):
                    cmd += " secondary"
            elif address and address == 'dhcp':
                cmd += " dhcp"
                if each.get('client-id'):
                    cmd += " client-id GigabitEthernet 0/{client-id}".format(**each)
                if each.get('hostname'):
                    cmd += " hostname {hostname}".format(**each)
            command.append(cmd)
        return command

def _tmplt_l3_ipv4_dhcp(config_data):
    if "ipv4" in config_data and config_data['ipv4'][0].get('address') == 'dhcp':
        command = "ip address"
        address = config_data['ipv4'].get('address')
        if address and address == 'dhcp':
            command += " dhcp"
            if config_data['ipv4'].get('client-id'):
                command += " client-id GigabitEthernet 0/{client-id}".format(**config_data['ipv4'])
            if config_data['ipv4'].get('hostname'):
                command += " hostname {hostname}".format(**config_data['ipv4'])
        return command


def _tmplt_l3_ipv6(config_data):
    if "ipv6" in config_data:
        command = []
        for each in config_data['ipv6']:
            cmd = "ipv6 address"
            address = each.get('address')
            if address:
                cmd += " {address}".format(**each)
            command.append(cmd)
        return command



class L3_InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(L3_InterfacesTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                    ^interface*
                    \s*(?P<name>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_interface,
            "result": {
                "interface": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "ipv4",
            "getval": re.compile(
                r"""\s+ip\saddress*
                    \s*(?P<address>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))*
                    \s*(?P<mask>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))*
                    \s*(?P<secondary> secondary)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_ipv4,
            "result": {
                "interface": {
                    "{{ name }}": {
                        "ipv4": [{
                            "address": "{{ address }}",
                            "mask": "{{ mask }}",
                            "secondary": "{{ True if secondary is defined }}",
                        }]
                    }
                }
            },
        },
        {
            "name": "ipv4_dhcp",
            "getval": re.compile(
                r"""\s+ip\saddress*
                    \s*(?P<dhcp> dhcp)*
                    \s*(?P<client_id>client-id\s\S+)*
                    \s*(?P<hostname>hostname\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_ipv4_dhcp,
            "compval": "ipv4",
            "result": {
                "interface": {
                    "{{ name }}": {
                        "ipv4": [{
                            "address": "{{ dhcp }}",
                            "dhcp_client": "{{ client_id.split('/')[1] }}",
                            "dhcp_hostname": "{{ hostname.split(" ")[1] }}"
                        }]
                    }
                }
            },
        },
        {
            "name": "ipv6",
            "getval": re.compile(
                r"""\s+ipv6\saddress*
                    \s*(?P<v6_addr>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_ipv6,
            "result": {
                "interface": {
                    "{{ name }}": {
                        "ipv6": [{
                            "address": "{{ v6_addr }}",
                        }]
                    }
                }
            },
        },
    ]
