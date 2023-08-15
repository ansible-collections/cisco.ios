# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The User_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.generic import (
    IosNetworkTemplate,
)


class User_globalTemplate(IosNetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(User_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "enable",
            "getval": re.compile(
                r"""
                ^enable
                (\s(?P<type>password|secret))?
                (\slevel\s(?P<level>\d+))?
                (\s(?P<hash>[56789]))?
                (\s(?P<value>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "enable"
                      "{% if 'type' in password and password.type == 'password' %}"
                      "{{ ' password' }}"
                      "{{ ' level ' + level|string if level is defined and 1 <= level|int <= 14 else '' }}"
                      "{{ ' ' + password.hash|string if 'hash' in password and password.hash|int in [ 0, 6, 7 ] else ' 0' }}"
                      "{{ ' ' + password.value }}"
                      "{% else %}"
                      "{{ ' secret' }}"
                      "{{ ' level ' + level|string if level is defined and 1 <= level|int <= 14 else '' }}"
                      "{{ ' ' + password.hash|string if 'hash' in password and password.hash|int in [ 0, 5, 8, 9 ] else ' 0' }}"
                      "{{ ' ' + password.value }}"
                      "{% endif %}",
            "result": {
                "enable": [
                    {
                        "level": "{{ level }}",
                        "password": {
                            "type": "{{ type }}",
                            "hash": "{{ hash }}",
                            "value": "{{ value }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "user-name.name",
            "getval": re.compile(
                r"""
                ^user-name\s(?P<name>\S+)$
                """, re.VERBOSE,
            ),
            "remval": "user-name {{ name }}",
            "setval": "user-name {{ name }}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "name": "{{ name }}",
                        "command": "new",
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "user-name.privilege",
            "getval": re.compile(
                r"""
                ^\s+privilege\s(?P<privilege>\d+)$
                """, re.VERBOSE,
            ),
            "remval": None,
            "setval": "{{ ' privilege ' + parameters.privilege|string if 'privilege' in parameters and "
                      "0 <= parameters.privilege|int <= 15 and parameters.privilege|int != 1 else '' }}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "parameters": {
                            "privilege": "{{ privilege }}",
                        },
                    },
                },
            },
        },
        {
            "name": "user-name.view",
            "getval": re.compile(
                r"""
                ^\s+view(?P<view>\S+)$
                """, re.VERBOSE,
            ),
            "remval": None,
            "setval": "{{ ' view ' + parameters.view if parameters.view else '' }}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "parameters": {
                            "view": "{{ view }}",
                        },
                    },
                },
            },
        },
        {
            "name": "user-name.password",
            "getval": re.compile(
                r"""
                ^\s+(?P<type>password|secret)
                (\s(?P<hash>[056789]))?
                \s(?P<value>\S+)$
                """, re.VERBOSE,
            ),
            "remval": None,
            "setval": "{% if 'password' in parameters %}"
                      "{% if 'type' in parameters.password and parameters.password.type == 'password' %}"
                      "{{ ' password' }}"
                      "{{ ' ' + parameters.password.hash|string if 'hash' in parameters.password and parameters.password.hash in [ 0, 6, 7 ] else ' 0' }}"
                      "{{ ' ' + parameters.password.value }}"
                      "{% else %}"
                      "{{ ' secret' }}"
                      "{{ ' ' + parameters.password.hash|string if 'hash' in parameters.password and parameters.password.hash in [ 0, 5, 8, 9 ] "
                      "else ' 0' }}"
                      "{{ ' ' + parameters.password.value }}"
                      "{% endif %}"
                      "{% endif %}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "parameters": {
                            "password": {
                                "type": "{{ type }}",
                                "hash": "{{ hash }}",
                                "value": "{{ value }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "user-name.nopassword",
            "getval": re.compile(
                r"""
                ^\s+nopassword$
                """, re.VERBOSE,
            ),
            "remval": None,
            "setval": "{{ ' nopassword' if parameters.nopassword and not 'password' in parameters.else '' }}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "parameters": {
                            "nopassword": True,
                        },
                    },
                },
            },
        },
        {
            "name": "users",
            "getval": re.compile(
                r"""
                ^username
                (\s(?P<name>\S+))?
                (\sprivilege\s(?P<privilege>\d+))?
                (\sview\s(?P<view>\S+))?
                (\s(?P<nopassword>nopassword))?
                (\s(?P<type>password|secret))?
                (\s(?P<hash>[56789]))?
                (\s(?P<value>\S+))?
                """, re.VERBOSE,
            ),
            "remval": {
                "command": "username {{ name }}",
                "prompt": "This operation will remove all username related configurations with same name",
                "answer": "y",
                "newline": False,
            },
            "setval": "username {{ name }}"
                      "{{ ' privilege ' + parameters.privilege|string if 'privilege' in parameters and "
                      "0 <= parameters.privilege|int <= 15 and parameters.privilege|int != 1 else '' }}"
                      "{{ ' view ' + parameters.view if parameters.view is defined else '' }}"
                      "{% if 'password' in parameters %}"
                      "{% if 'type' in parameters.password and parameters.password.type == 'password' %}"
                      "{{ ' password' }}"
                      "{{ ' ' + parameters.password.hash|string if 'hash' in parameters.password and parameters.password.hash|int in [ 0, 6, 7 ] else ' 0' }}"
                      "{{ ' ' + parameters.password.value }}"
                      "{% else %}"
                      "{{ ' secret' }}"
                      "{{ ' ' + parameters.password.hash|string if 'hash' in parameters.password and parameters.password.hash|int in [ 0, 5, 8, 9 ] "
                      "else ' 0' }}"
                      "{{ ' ' + parameters.password.value }}"
                      "{% endif %}"
                      "{% else %}"
                      "{{ ' nopassword' if parameters.nopassword|default(False) }}"
                      "{% endif %}",
            "result": {
                "users": {
                    "{{ name|d() }}": {
                        "name": "{{ name }}",
                        "command": "old",
                        "parameters": {
                            "privilege": "{{ privilege }}",
                            "password": {
                                "type": "{{ type }}",
                                "hash": "{{ hash }}",
                                "value": "{{ value }}",
                            },
                            "nopassword": "{{ true if nopassword }}",
                            "view": "{{ view }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
