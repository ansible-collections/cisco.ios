# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.monitor_sessions import (
    Monitor_sessionsTemplate,
)


class Monitor_sessions(ResourceModule):  # NOSONAR
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
        self._erspan = set()

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
        merged = dict(haved)
        merged.update(wantd)
        self._erspan = {sid for sid, entry in merged.items() if self._uses_erspan(entry)}

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

        replace = self.state in ["replaced", "overridden"]
        self._generate_source_commands(session_id, want_sources, have_sources, replace=replace)

        if self._norm_dest(want_dest) == self._norm_dest(have_dest):
            return

        if session_id in self._erspan:
            if want_dest:
                self._set_erspan_destination(session_id, want_dest)
            return

        if have_dest:
            should_negate = (not want_dest and self.state in ["replaced", "overridden"]) or (
                want_dest
                and have_dest.get("interface")
                and want_dest.get("interface")
                and want_dest["interface"] != have_dest["interface"]
            )
            if should_negate:
                self.commands.append(
                    "no monitor session {0} destination interface {1}".format(
                        session_id,
                        have_dest["interface"],
                    ),
                )
        if want_dest and want_dest.get("interface"):
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
                self._remove_source_ifaces(session_id, direction, to_remove)
            if to_add:
                self._add_source_ifaces(session_id, direction, to_add, want_sources)

    def _remove_source_ifaces(self, session_id, direction, ifaces):
        joined = " , ".join(sorted(ifaces))
        if session_id in self._erspan:
            self.commands.append("monitor session {0} type erspan-source".format(session_id))
            cmd = "no source interface {0}".format(joined)
        else:
            cmd = "no monitor session {0} source interface {1}".format(session_id, joined)
        if direction != "both":
            cmd += " {0}".format(direction)
        self.commands.append(cmd)

    def _add_source_ifaces(self, session_id, direction, to_add, want_sources):
        # Preserve user-specified order; fall back to sorted
        ordered = [
            i
            for s in want_sources
            if self._norm_dir(s.get("direction")) == direction
            for i in s["interfaces"]
            if i in to_add
        ]
        if not ordered:
            ordered = sorted(to_add)
        joined = " , ".join(ordered)
        if session_id in self._erspan:
            self.commands.append("monitor session {0} type erspan-source".format(session_id))
            cmd = "source interface {0}".format(joined)
        else:
            cmd = "monitor session {0} source interface {1}".format(session_id, joined)
        if direction != "both":
            cmd += " {0}".format(direction)
        self.commands.append(cmd)

    def _set_erspan_destination(self, session_id, dest):
        self.commands.append("monitor session {0} type erspan-source".format(session_id))
        self.commands.append("destination")
        if dest.get("erspan_id") is not None:
            self.commands.append("erspan-id {0}".format(dest["erspan_id"]))
        if dest.get("ip_address"):
            self.commands.append("ip address {0}".format(dest["ip_address"]))
        if dest.get("origin_ip_address"):
            self.commands.append("origin ip address {0}".format(dest["origin_ip_address"]))

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
            result.extend(Monitor_sessionsTemplate.expand_range(iface))
        return result

    @staticmethod
    def _norm_dir(direction):
        """Normalize direction to one of: rx, tx, both."""
        if not direction or direction == "both":
            return "both"
        return direction

    @staticmethod
    def _uses_erspan(entry):
        if not entry:
            return False
        if entry.get("session_type") == "erspan-source":
            return True
        dest = entry.get("destination") or {}
        return bool(dest.get("ip_address") or dest.get("erspan_id") or dest.get("origin_ip_address"))

    @staticmethod
    def _norm_dest(dest):
        if not dest:
            return {}
        out = {}
        for key in ("interface", "erspan_id", "ip_address", "origin_ip_address"):
            if dest.get(key) is not None:
                out[key] = dest[key]
        if dest.get("encapsulation_replicate"):
            out["encapsulation_replicate"] = True
        return out
