#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_vrf_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_global import (
    Vrf_globalTemplate,
)


class Vrf_global(ResourceModule):
    """
    The ios_vrf_global config class
    """

    def __init__(self, module):
        super(Vrf_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vrf_global",
            tmplt=Vrf_globalTemplate(),
        )
        self.parsers = [
            "description",
            "ipv4.multicast.multitopology",
            "ipv6.multicast.multitopology",
            "rd",
            "vnet.tag",
            "vpn.id",
        ]

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
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        haved, wantd = dict(), dict()
        self.want = self._handle_deprecates(self.want)

        if self.want:
            for entry in self.want.get("vrfs", []):
                wantd.update({(entry["name"]): entry})

        if self.have:
            for entry in self.have.get("vrfs", []):
                haved.update({(entry["name"]): entry})

        # if state is merged, merge want onto have
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want & set want to nothing
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        if self.state == "purged":
            for k, have in haved.items():
                self.purge(have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vrf_global network resource.
        """
        wanted = deepcopy(want)
        haved = deepcopy(have)

        rt_want = wanted.get("route_target", {})
        if rt_want:
            if rt_want.get("exports"):
                rt_want["exports"].sort()
            if rt_want.get("imports"):
                rt_want["imports"].sort()

        rt_have = haved.get("route_target", {})
        if rt_have:
            if rt_have.get("exports"):
                rt_have["exports"].sort()
            if rt_have.get("imports"):
                rt_have["imports"].sort()

        if wanted == haved:
            return

        self.addcmd(want or have, "name", False)
        self.compare(self.parsers, want, have)
        self._compare_route_targets(want, have)

    def _compare_route_targets(self, want, have):
        """Specialized comparison for route-target lists using set logic."""
        rt_want = want.get("route_target", {}) or {}
        rt_have = have.get("route_target", {}) or {}

        # Compare Exports
        want_exports = set(rt_want.get("exports") or [])
        have_exports = set(rt_have.get("exports") or [])

        for item in want_exports - have_exports:
            self.addcmd({"item": item}, "route_target.exports", negate=False)
        for item in have_exports - want_exports:
            self.addcmd({"item": item}, "route_target.exports", negate=True)

        # Compare Imports
        want_imports = set(rt_want.get("imports") or [])
        have_imports = set(rt_have.get("imports") or [])

        for item in want_imports - have_imports:
            self.addcmd({"item": item}, "route_target.imports", negate=False)
        for item in have_imports - want_imports:
            self.addcmd({"item": item}, "route_target.imports", negate=True)

    def purge(self, have):
        """Purge the VRF configuration"""
        self.commands.append("no vrf definition {0}".format(have["name"]))

    def _handle_deprecates(self, want):
        if not isinstance(want, dict) or "vrfs" not in want:
            return want
        for vrf_config in want["vrfs"]:
            if "route_target" in vrf_config:
                rt = vrf_config["route_target"]
                if "exports" in rt and isinstance(rt["exports"], str):
                    rt["exports"] = [rt["exports"]]
                if "imports" in rt and isinstance(rt["imports"], str):
                    rt["imports"] = [rt["imports"]]
        return want
