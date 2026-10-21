# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
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


class Monitor_sessionsFacts(object):  # NOSONAR
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

        if not data:
            data = self.get_monitor_sessions_data(connection)

        parsed = self._parse_lines(data or "")
        objs = sorted(parsed.values(), key=lambda x: int(x["session"]))

        ansible_facts["ansible_network_resources"].pop("monitor_sessions", None)

        monitor_sessions_parser = Monitor_sessionsTemplate(
            lines=(data or "").splitlines(),
            module=self._module,
        )
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

    @staticmethod
    def _expand_source_blob(iface_blob):
        """Split a source-interface string into individual names, expanding ranges."""
        result = []
        for part in iface_blob.split(","):
            result.extend(Monitor_sessionsTemplate.expand_range(part))
        return result

    @staticmethod
    def _split_source_and_direction(blob):
        """Return (interface_blob, direction_or_none) from a source interface clause."""
        blob = blob.strip()
        parts = blob.rsplit(None, 1)
        if len(parts) == 2 and parts[1] in ("rx", "tx"):
            return parts[0], parts[1]
        return blob, None

    def _add_source(self, session, iface_blob, direction=None):
        entry = {"interfaces": self._expand_source_blob(iface_blob)}
        if direction:
            entry["direction"] = direction
        session.setdefault("sources", []).append(entry)

    def _parse_lines(self, data):
        """Parse Cat9k one-liners and router ERSPAN/type submode blocks."""
        sessions = {}
        current_id = None
        in_dest = False

        def session(sid):
            sessions.setdefault(sid, {"session": sid})
            return sessions[sid]

        for raw in data.splitlines():
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped or stripped == "!":
                continue

            match = re.match(r"^monitor session (\d+) type (\S+)", line)
            if match:
                current_id = int(match.group(1))
                session(current_id)["session_type"] = match.group(2)
                in_dest = False
                continue

            match = re.match(r"^monitor session (\d+)\s+source interface\s+(.+)$", line)
            if match:
                current_id = None
                in_dest = False
                iface_blob, direction = self._split_source_and_direction(match.group(2))
                self._add_source(session(int(match.group(1))), iface_blob, direction)
                continue

            match = re.match(
                r"^monitor session (\d+)\s+destination interface\s+(\S+)(.*)$",
                line,
            )
            if match:
                current_id = None
                in_dest = False
                dest = {
                    "interface": match.group(2),
                    "encapsulation_replicate": "encapsulation replicate" in match.group(3),
                }
                session(int(match.group(1)))["destination"] = dest
                continue

            if current_id is None:
                continue

            if stripped == "destination":
                in_dest = True
                continue

            if stripped in ("shutdown", "no shutdown"):
                continue

            match = re.match(r"^source interface\s+(.+)$", stripped)
            if match:
                iface_blob, direction = self._split_source_and_direction(match.group(1))
                self._add_source(session(current_id), iface_blob, direction)
                continue

            if not in_dest:
                continue

            match = re.match(r"^erspan-id (\d+)$", stripped)
            if match:
                session(current_id).setdefault("destination", {})["erspan_id"] = int(match.group(1))
                continue
            match = re.match(r"^ip address (\S+)$", stripped)
            if match:
                session(current_id).setdefault("destination", {})["ip_address"] = match.group(1)
                continue
            match = re.match(r"^origin ip address (\S+)$", stripped)
            if match:
                session(current_id).setdefault("destination", {})["origin_ip_address"] = match.group(
                    1,
                )
                continue

        return sessions
