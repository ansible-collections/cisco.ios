# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.monitor_sessions.monitor_sessions import (
    Monitor_sessionsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.monitor_sessions import (
    Monitor_sessionsTemplate,
)


def _expand_range(iface_str):
    """Expand IOS range notation 'Gi1/0/1 - 3' into individual interface names."""
    m = re.match(r"^(.+?)(\d+)\s*-\s*(\d+)$", iface_str.strip())
    if m:
        prefix, start, end = m.group(1), int(m.group(2)), int(m.group(3))
        return ["{0}{1:d}".format(prefix, i) for i in range(start, end + 1)]
    return [iface_str.strip()]


class Monitor_sessionsFacts(object):
    """The ios monitor_sessions facts class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Monitor_sessionsArgs.argument_spec

    def get_monitor_sessions_data(self, connection):
        return connection.get("show running-config | section ^monitor session")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Monitor_sessions network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_monitor_sessions_data(connection)

        monitor_sessions_parser = Monitor_sessionsTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        parsed = monitor_sessions_parser.parse()

        for session in parsed.values():
            for source in session.get("sources", []):
                if "interface" in source:
                    iface_str = source.pop("interface")
                    source["interfaces"] = [
                        iface for s in iface_str.split(",") for iface in _expand_range(s)
                    ]

        objs = sorted(parsed.values(), key=lambda x: int(x["session"]))

        ansible_facts["ansible_network_resources"].pop("monitor_sessions", None)

        params = utils.remove_empties(
            monitor_sessions_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["monitor_sessions"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
