#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios_prefix_lists config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.prefix_lists import (
    Prefix_listsTemplate,
)


class Prefix_lists(ResourceModule):
    """
    The cisco.ios_prefix_lists config class
    """

    def __init__(self, module):
        super(Prefix_lists, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="prefix_lists",
            tmplt=Prefix_listsTemplate(),
        )
        self.parsers = ["prefix_list"]

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
        wantd = {entry["afi"]: entry for entry in self.want}
        haved = {entry["afi"]: entry for entry in self.have}

        self._prefix_list_transform(wantd)
        self._prefix_list_transform(haved)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            for key, hvalue in haved.items():
                wvalue = wantd.pop(key, {})
                if wvalue:
                    wplists = wvalue.get("prefix_lists", {})
                    hplists = hvalue.get("prefix_lists", {})
                    hvalue["prefix_lists"] = {
                        k: v for k, v in hplists.items() if k in wplists or not wplists
                    }

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Prefix_lists network resource.
        """
        wplists = want.get("prefix_lists", {})
        hplists = have.get("prefix_lists", {})
        for wk, wentry in wplists.items():
            hentry = hplists.pop(wk, {})
            self.compare(["description"], want=wentry, have=hentry)
            # compare sequences
            self._compare_seqs(wentry.pop("entries", {}), hentry.pop("entries", {}))

        if self.state in ["overridden", "deleted"]:
            # remove remaining prefix lists
            for h in hplists.values():
                self.commands.append(
                    "no {0} prefix-list {1}".format(h["afi"].replace("ipv4", "ip"), h["name"]),
                )

    def _compare_seqs(self, want, have):
        for wseq, wentry in want.items():
            hentry = have.pop(wseq, {})
            if hentry != wentry:
                if hentry:
                    if self.state == "merged":
                        self._module.fail_json(
                            msg="Cannot update existing sequence {0} of prefix list {1} with state merged."
                            " Please use state replaced or overridden.".format(
                                hentry["sequence"],
                                hentry["name"],
                            ),
                        )
                    else:
                        self.addcmd(hentry, "entry", negate=True)
                self.addcmd(wentry, "entry")
        # remove remaining entries from have prefix list
        for hseq in have.values():
            self.addcmd(hseq, "entry", negate=True)

    def _prefix_list_transform(self, entry):
        for afi, value in entry.items():
            if "prefix_lists" in value:
                for plist in value["prefix_lists"]:
                    plist.update({"afi": afi})
                    if "entries" in plist:
                        for seq in plist["entries"]:
                            seq.update({"afi": afi, "name": plist["name"]})
                        plist["entries"] = {x["sequence"]: x for x in plist["entries"]}
                value["prefix_lists"] = {entry["name"]: entry for entry in value["prefix_lists"]}
