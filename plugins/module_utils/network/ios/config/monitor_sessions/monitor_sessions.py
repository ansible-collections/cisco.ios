# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.monitor_sessions import (
    Monitor_sessionsTemplate,
)


class Monitor_sessions(ResourceModule):
    """The ios_monitor_sessions config class"""

    def __init__(self, module):
        super(Monitor_sessions, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="monitor_sessions",
            tmplt=Monitor_sessionsTemplate(),
        )
        self.parsers = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands based on want, have and state."""

        wantd = {entry["session"]: entry for entry in self.want}
        haved = {entry["session"]: entry for entry in self.have}

        if self.state == "deleted":
            sessions_to_delete = {k: v for k, v in haved.items() if k in wantd or not wantd}
            for session_id in sessions_to_delete:
                self.commands.append("no monitor session {0}".format(session_id))
            return

        if self.state == "overridden":
            for session_id, have in haved.items():
                if session_id not in wantd:
                    self.commands.append("no monitor session {0}".format(session_id))

        for session_id, want in wantd.items():
            have = haved.get(session_id, {})
            self._compare_session(want, have)

    def _compare_session(self, want, have):
        """Compare a single session and generate required commands."""
        session_id = want["session"]

        want_sources = want.get("sources", [])
        have_sources = have.get("sources", [])
        want_dest = want.get("destination")
        have_dest = have.get("destination")

        replace = self.state == "replaced"
        self._generate_source_commands(session_id, want_sources, have_sources, replace=replace)

        if want_dest != have_dest:
            if have_dest and (self.state in ["replaced", "overridden"] or not want_dest):
                self.commands.append(
                    "no monitor session {0} destination interface {1}".format(
                        session_id,
                        have_dest["interface"],
                    ),
                )
            if want_dest:
                cmd = "monitor session {0} destination interface {1}".format(
                    session_id,
                    want_dest["interface"],
                )
                if want_dest.get("encapsulation_replicate"):
                    cmd += " encapsulation replicate"
                self.commands.append(cmd)

    def _generate_source_commands(self, session_id, want_sources, have_sources, replace=False):
        """Generate add/remove commands for source interfaces.

        IOS-XE groups all same-direction interfaces into a single running-config
        line and expands consecutive ports as ranges (e.g. Gi1/0/1 - 3).  We
        therefore compare on the *expanded* set of individual interface names
        per direction, not on the raw source-entry list.
        """
        want_by_dir = self._group_by_direction(want_sources)
        have_by_dir = self._group_by_direction(have_sources)

        all_dirs = set(want_by_dir) | set(have_by_dir)

        for direction in sorted(all_dirs):
            want_ifaces = want_by_dir.get(direction, set())
            have_ifaces = have_by_dir.get(direction, set())

            if want_ifaces == have_ifaces:
                continue

            to_remove = have_ifaces - want_ifaces
            to_add = want_ifaces - have_ifaces

            if replace and to_remove:
                cmd = "no monitor session {0} source interface {1}".format(
                    session_id, " , ".join(sorted(to_remove)),
                )
                if direction != "both":
                    cmd += " {0}".format(direction)
                self.commands.append(cmd)

            if to_add:
                # Preserve user-specified order; fall back to sorted
                ordered = [i for s in want_sources
                           if self._norm_dir(s.get("direction")) == direction
                           for i in s["interfaces"]
                           if i in to_add]
                if not ordered:
                    ordered = sorted(to_add)
                cmd = "monitor session {0} source interface {1}".format(
                    session_id, " , ".join(ordered),
                )
                if direction != "both":
                    cmd += " {0}".format(direction)
                self.commands.append(cmd)

    def _group_by_direction(self, sources):
        """Return {direction: frozenset(expanded_interfaces)} from a sources list."""
        by_dir = {}
        for s in sources:
            d = self._norm_dir(s.get("direction"))
            expanded = set(self._expand_interfaces(s["interfaces"]))
            by_dir.setdefault(d, set()).update(expanded)
        return by_dir

    @staticmethod
    def _expand_interfaces(iface_list):
        """Expand IOS range notation (e.g. 'Gi1/0/1 - 3') into individual names."""
        result = []
        for iface in iface_list:
            result.extend(Monitor_sessions._expand_range(iface))
        return result

    @staticmethod
    def _expand_range(iface_str):
        """Expand 'Gi1/0/1 - 3' → ['Gi1/0/1', 'Gi1/0/2', 'Gi1/0/3']."""
        m = re.match(r'^(.+?)(\d+)\s*-\s*(\d+)$', iface_str.strip())
        if m:
            prefix, start, end = m.group(1), int(m.group(2)), int(m.group(3))
            return ["{0}{1:d}".format(prefix, i) for i in range(start, end + 1)]
        return [iface_str.strip()]

    @staticmethod
    def _norm_dir(direction):
        """Normalize direction to one of: rx, tx, both."""
        if not direction or direction == "both":
            return "both"
        return direction
