# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The acls parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""
import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_l3_interfaces_ipv4(config_data):
    try:
        acl_id = int(config_data.get("name"))
        if not config_data.get("acl_type"):
            if acl_id >= 1 and acl_id <= 99:
                config_data["acl_type"] = "standard"
            if acl_id >= 100 and acl_id <= 199:
                config_data["acl_type"] = "extended"
    except ValueError:
        pass
    afi = config_data.get("afi")
    if afi == "ipv4":
        command = "ip access-list {acl_type} {name}".format(**config_data)
    elif afi == "ipv6":
        command = "ipv6 access-list {name}".format(**config_data)
    return command

def _tmplt_l3_interfaces_ipv6(config_data):
    pass

class L3_InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(AclsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "interface",
            "getval": re.compile(
                r"""^interaface*
                    \s*(?P<name>\S+)
                    $""",
                re.VERBOSE,
            ),
            "compval": "interface {{ name }}",
            "setval": _tmplt_access_list_name,
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                }
            },
            "shared": True,
        },
        {
            "name": "ipv4",
            "getval": re.compile(
                r"""\s+ip\saddress*
                    \s*(?P<ipv4>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\ssecondary|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<ipv4_dhcp>dhcp\sclient-id\s\S+\shostname\s\S+|dhcp\sclient-id\s\S+|dhcp\shostname\s\S+|dhcp)*
                    \s*()
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_interfaces_attributes,
            "compval": "aces",
            "result": {
                "{{ name }}": {
                    "ipv4":[
                        {
                            "address": "{{ ipv4.split(' ')[0] if ipv4 is defined }}",
                            "netmask": "{{ ipv4.split(' ')[1] if ipv4 is defined }}",
                            "secondary": "{{ ipv4.split(' ')[2] if ipv4 is defined and 'secondary' in ipv4 }}",
                            "dhcp_client": "{{ ipv4_dhcp.split('/')[1].split(' ')[0] if ipv4_dhcp is defined and 'client-id' in ipv4_dhcp }}",
                            "dhcp_hostname": "{{ ipv4_dhcp.split('hostname ')[1] if ipv4_dhcp is defined and 'hostname' in ipv4_dhcp }}",
                        },
                    ],
                }
            },
        },
        {
            "name": "ipv6",
            "getval": re.compile(
                r"""\s+ipv6\saddress*
                    \s*((?P<ipv6>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_interfaces_ipv6,
            "compval": "aces",
            "result": {
                "{{ name }}": {                 
                    "ipv6":[
                        {
                            "address": "{{ ipv6 }}"
                        }
                    ],
                }
            },
        },
    ]
