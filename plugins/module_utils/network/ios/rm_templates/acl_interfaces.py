# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Acl_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Acl_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Acl_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            'name': 'interface',
            'getval': re.compile(
                r'''
              ^interface\s
              (?P<name>\S+)$''', re.VERBOSE,
            ),
            'setval': 'interface {{ name }}',
            'result': {
                '{{ name }}': {
                    'name': '{{ name }}',
                    'access_groups': {},
                },
            },
            'shared': True,
        },
        {
            "name": "access_groups",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)
                (\saccess-group\s(?P<acl_name>\S+))?
                (\straffic-filter\s(?P<acl_name_traffic>\S+))?
                \s(?P<direction>\S+)$
                """,
                re.VERBOSE,
            ),
            "setval": "{{ 'ip access-group' if afi == 'ipv4' else 'ipv6 traffic-filter' }} {{ name|string }} {{ direction }}",
            "result": {
                "{{ name }}": {
                    "access_groups": {
                        "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "acls": [
                                {
                                    "name": "{{ acl_name|string if acl_name is defined else acl_name_traffic }}",
                                    "direction": "{{ direction }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
