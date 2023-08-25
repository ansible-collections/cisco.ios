# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Prefix_lists parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def _tmplt_set_prefix_lists(config_data):
    if "prefix_list" in config_data:
        if config_data.get("afi") == "ipv4":
            config_data["afi"] = "ip"
        cmd = "{afi} prefix-list {name}".format(**config_data)
        if config_data.get("prefix_list"):
            if config_data["prefix_list"].get("description"):
                cmd += " description {description}".format(**config_data["prefix_list"])
            else:
                cmd += " seq {sequence} {action} {prefix}".format(**config_data["prefix_list"])
                if config_data["prefix_list"].get("ge"):
                    cmd += " ge {ge}".format(**config_data["prefix_list"])
                if config_data["prefix_list"].get("le"):
                    cmd += " le {le}".format(**config_data["prefix_list"])
        return cmd


class Prefix_listsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Prefix_listsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "entry",
            "getval": re.compile(
                r"""
                ^(?P<afi>ip|ipv6)\sprefix-list
                (\s(?P<name>\S+))
                (\sseq\s(?P<sequence>\d+))?
                (\s(?P<action>deny|permit))?
                (\s(?P<prefix>\S+))?
                (\sge\s(?P<ge>\d+))?
                (\sle\s(?P<le>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip' if afi == 'ipv4' else afi }} prefix-list {{ name }}"
            "{{ (' seq ' + sequence|string) if sequence|d('') else '' }}"
            " {{ action }}"
            " {{ prefix }}"
            "{{ (' ge ' + ge|string) if ge|d('') else '' }}"
            "{{ (' le ' + le|string) if le|d('') else '' }}",
            "shared": True,
            "result": {
                "{{ afi + name }}": {
                    "afi": "{{ 'ipv4' if afi is defined and afi=='ip' else 'ipv6' }}",
                    "name": "{{ name }}",
                    "entries": [
                        {
                            "sequence": "{{ sequence }}",
                            "action": "{{ action }}",
                            "prefix": "{{ prefix }}",
                            "ge": "{{ ge }}",
                            "le": "{{ le }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                ^(?P<afi>ip|ipv6)\sprefix-list
                (\s(?P<name>\S+))
                (\sdescription\s(?P<description>.+$))?
                """,
                re.VERBOSE,
            ),
            "setval": "{{ 'ip' if afi == 'ipv4' else afi }} prefix-list {{ name }} description {{ description }}",
            "shared": True,
            "result": {
                "{{ afi + name }}": {
                    "name": "{{ name }}",
                    "afi": "{{ 'ipv4' if afi is defined and afi=='ip' else 'ipv6' }}",
                    "description": "{{ description }}",
                },
            },
        },
    ]
