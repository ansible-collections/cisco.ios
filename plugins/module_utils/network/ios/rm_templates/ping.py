# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ping parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class PingTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(PingTemplate, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            'name': 'rate',
            'getval': re.compile(
                r'''
                ^Success\srate\sis
                (\s(?P<pct>\d+))?
                (\spercent\s\((?P<rx>\d+)/(?P<tx>\d+)\))?
                (,\s+round-trip\smin/avg/max\s=)?
                (\s(?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+))?
                (\s+\w+\s*$|.*\s*$)?
                ''', re.VERBOSE,
            ),
            "setval": "ping"
            "{{ (' vrf ' + vrf) if vrf is defined else '' }}"
            "{{ (' ' + afi|string ) if afi is defined else '' }}"
            "{{ (' ' + dest ) if dest is defined else '' }}"
            "{{ (' repeat ' + count|string ) if count is defined else '' }}"
            "{{ (' df-bit' ) if df_bit|d(False) else '' }}"
            "{{ (' timeout ' + timeout|string) if timeout is defined else '' }}"
            "{{ (' ingress ' + ingress) if ingress is defined else '' }}"
            "{{ (' egress ' + egress) if egress is defined else '' }}"
            "{{ (' source ' + source) if source is defined else '' }}",
            'result': {
                "ping": {
                    'loss_percentage': '{{ 100 - pct|int }}%',
                    'loss': '{{ 100 - pct|int }}',
                    'rx': '{{ rx|int }}',
                    'tx': '{{ tx|int }}',
                    'rtt': {
                        'min': '{{ min }}',
                        'avg': '{{ avg }}',
                        'max': '{{ max }}',
                    },
                },
            },
        },
    ]
    # fmt: on
