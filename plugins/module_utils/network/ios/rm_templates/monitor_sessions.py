# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_SESSION_KEY = "{{ session }}"
_IFACE_KEY = "{{ interface }}"


class Monitor_sessionsTemplate(NetworkTemplate):  # NOSONAR
    def __init__(self, lines=None, module=None):
        super(Monitor_sessionsTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    @staticmethod
    def expand_range(iface_str):
        """Expand IOS range notation (e.g. 'Gi1/0/1 - 3') into individual interface names."""
        m = re.match(r"^(.*[^\d])(\d+)\s*-\s*(\d+)$", iface_str.strip())
        if m:
            prefix, start, end = m.group(1), int(m.group(2)), int(m.group(3))
            return ["{0}{1:d}".format(prefix, i) for i in range(start, end + 1)]
        return [iface_str.strip()]

    # fmt: off
    PARSERS = [
        {
            "name": "source",
            "getval": re.compile(
                r"""^monitor\ssession\s(?P<session>\d+)
                    \ssource\sinterface\s
                    (?P<interface>.*\S)
                    \s+(?P<direction>rx|tx)
                    $""",
                re.VERBOSE,
            ),
            "setval": "monitor session {{ session }} source interface {{ source.interface }}"
                      "{{ ' ' + source.direction if source.direction is defined and source.direction != 'both' else '' }}",
            "result": {
                _SESSION_KEY: {
                    "session": _SESSION_KEY,
                    "sources": [
                        {
                            "interface": _IFACE_KEY,
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
                _SESSION_KEY: {
                    "session": _SESSION_KEY,
                    "sources": [
                        {
                            "interface": _IFACE_KEY,
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
                _SESSION_KEY: {
                    "session": _SESSION_KEY,
                    "destination": {
                        "interface": _IFACE_KEY,
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
                _SESSION_KEY: {
                    "session": _SESSION_KEY,
                    "destination": {
                        "interface": _IFACE_KEY,
                        "encapsulation_replicate": False,
                    },
                },
            },
        },
    ]
    # fmt: on
