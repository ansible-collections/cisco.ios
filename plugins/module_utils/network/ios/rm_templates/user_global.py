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

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class User_globalTemplate(NetworkTemplate):
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
            "name": "users",
            "getval": re.compile(
                r"""
                ^username
                (\s(?P<name>\S+))?
                (\sprivilege\s(?P<privilege>\d+))?
                (\s(?P<type>password|secret))?
                (\s(?P<hash>[56789]))?
                (\s(?P<value>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "username {{ name }}"
                      "{{ ' privilege ' + privilege|string if privilege is defined and 0 <= privilege|int <= 15 and privilege|int != 1 else '' }}"
                      "{% if 'type' in password and password.type == 'password' %}"
                      "{{ ' password' }}"
                      "{{ ' ' + password.hash|string if 'hash' in password and password.hash|int in [ 0, 6, 7 ] else ' 0' }}"
                      "{{ ' ' + password.value }}"
                      "{% else %}"
                      "{{ ' secret' }}"
                      "{{ ' ' + password.hash|string if 'hash' in password and password.hash|int in [ 0, 5, 8, 9 ] else ' 0' }}"
                      "{{ ' ' + password.value }}"
                      "{% endif %}",
            "result": {
                "users": [
                    {
                        "name": "{{ name }}",
                        "privilege": "{{ privilege }}",
                        "password": {
                            "type": "{{ type }}",
                            "hash": "{{ hash }}",
                            "value": "{{ value }}",
                        },
                    },
                ],
            },
        },
    ]
    # fmt: on
