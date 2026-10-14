# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Monitor_sessionsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Monitor_sessionsTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "source",
            "getval": re.compile(
                r"""^monitor\ssession\s(?P<session>\d+)
                    \ssource\sinterface\s
                    (?P<interface>.+)
                    \s+(?P<direction>rx|tx)
                    $""",
                re.VERBOSE,
            ),
            "setval": "monitor session {{ session }} source interface {{ source.interface }}"
                      "{{ ' ' + source.direction if source.direction is defined and source.direction != 'both' else '' }}",
            "result": {
                "{{ session }}": {
                    "session": "{{ session }}",
                    "sources": [
                        {
                            "interface": "{{ interface }}",
                            "direction": "{{ direction }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "source_both",
            "getval": re.compile(
                r"""^monitor\ssession\s(?P<session>\d+)
                    \ssource\sinterface\s
                    (?P<interface>.+)
                    $""",
                re.VERBOSE,
            ),
            "setval": "monitor session {{ session }} source interface {{ source.interface }}",
            "result": {
                "{{ session }}": {
                    "session": "{{ session }}",
                    "sources": [
                        {
                            "interface": "{{ interface }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "destination",
            "getval": re.compile(
                r"""^monitor\ssession\s(?P<session>\d+)
                    \sdestination\sinterface\s
                    (?P<interface>\S+)
                    \s+encapsulation\sreplicate
                    $""",
                re.VERBOSE,
            ),
            "setval": "monitor session {{ session }} destination interface {{ destination.interface }} encapsulation replicate",
            "result": {
                "{{ session }}": {
                    "session": "{{ session }}",
                    "destination": {
                        "interface": "{{ interface }}",
                        "encapsulation_replicate": True,
                    },
                },
            },
        },
        {
            "name": "destination_no_enc",
            "getval": re.compile(
                r"""^monitor\ssession\s(?P<session>\d+)
                    \sdestination\sinterface\s
                    (?P<interface>\S+)
                    $""",
                re.VERBOSE,
            ),
            "setval": "monitor session {{ session }} destination interface {{ destination.interface }}",
            "result": {
                "{{ session }}": {
                    "session": "{{ session }}",
                    "destination": {
                        "interface": "{{ interface }}",
                        "encapsulation_replicate": False,
                    },
                },
            },
        },
    ]
    # fmt: on
