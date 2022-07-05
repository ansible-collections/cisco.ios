# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Lag_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Lag_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Lag_interfacesTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )

    # fmt: off
    PARSERS = [
        {
            'name': 'member',
            'getval': re.compile(
                r'''
              ^interface\s
              (?P<member>\S+)$''', re.VERBOSE,
            ),
            'setval': 'interface {{ member }}',
            'result': {
                '{{ member }}': {
                    'member': '{{ member }}',
                },
            },
            'shared': True,
        },
        {
            "name": "channel",
            "getval": re.compile(
                r"""
                \s+channel-group
                (\s(?P<channel>\d+))?
                (\smode\s(?P<mode>active|passive|on|desirable|auto))?
                (\slink\s(?P<link>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "channel-group"
            "{{ (' ' + channel|string) if channel is defined else '' }}"
            "{{ (' mode ' + mode) if mode is defined else '' }}"
            "{{ (' link ' + link|string) if link is defined else '' }}",
            "result": {
                '{{ member }}': {
                    'member': '{{ member }}',
                    'mode': '{{ mode }}',
                    'channel': 'Port-channel{{ channel }}',
                    'link': '{{ link }}',
                },
            },
        },
    ]
    # fmt: on
