# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Evpn_ethernet parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Evpn_ethernetTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Evpn_ethernetTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "segment",
            "getval": re.compile(
                r"""^l2vpn\sevpn\sethernet-segment
                    (\s(?P<segment>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "l2vpn evpn ethernet-segment {{ segment }}",
            "result": {
                "{{ segment }}": {"segment": "{{ segment }}"},
            },
            "shared": True,
        },
        {
            "name": "df_election.wait_time",
            "getval": re.compile(
                r"""
                \s+df-election\swait-time\s(?P<wait_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "df-election wait-time {{ df_election.wait_time }}",
            "result": {
                "{{ segment }}": {
                    "df_election": {
                        "wait_time": "{{ wait_time }}",
                    },
                },
            },
        },
        {
            "name": "df_election.preempt_time",
            "getval": re.compile(
                r"""
                \s+df-election\spreempt-time\s(?P<preempt_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "df-election preempt-time {{ df_election.preempt_time }}",
            "result": {
                "{{ segment }}": {
                    "df_election": {
                        "preempt_time": "{{ preempt_time }}",
                    },
                },
            },
        },
        {
            "name": "redundancy.all_active",
            "getval": re.compile(
                r"""
                \s+redundancy\sall-active
                $""", re.VERBOSE,
            ),
            "setval": "redundancy all-active",
            "result": {
                "{{ segment }}": {
                    "redundancy": {
                        "all_active": True,
                    },
                },
            },
        },
        {
            "name": "redundancy.single_active",
            "getval": re.compile(
                r"""
                \s+redundancy\ssingle-active
                $""", re.VERBOSE,
            ),
            "setval": "redundancy single-active",
            "result": {
                "{{ segment }}": {
                    "redundancy": {
                        "single_active": True,
                    },
                },
            },
        },
        {
            "name": "identifier",
            "getval": re.compile(
                r"""
                \s+identifier\stype\s(?P<identifier_type>0|3)
                (\s(?P<system_mac>system-mac))?
                (\s(?P<esi_value>.+))
                $""",
                re.VERBOSE,
            ),
            "setval": "identifier type {{ identifier.identifier_type }} "
            "{% if identifier.identifier_type == '3' %}system-mac "
            "{{ identifier.esi_value }}{% else %}{{ identifier.esi_value }}{% endif %}",
            "result": {
                "{{ segment }}": {
                    "identifier": {
                        "identifier_type": "{{ identifier_type }}",
                        "esi_value": "{{ esi_value }}",
                    },
                },
            },
        },
    ]
    # fmt: on
