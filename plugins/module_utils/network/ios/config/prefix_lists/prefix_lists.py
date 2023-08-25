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

from ansible.module_utils.six import iteritems
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

        # Convert each of config list to dict
        for each in wantd, haved:
            self.list_to_dict(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(wants={}, haveing=have)

        for k, want in iteritems(wantd):
            self._compare(wants=want, haveing=haved.pop(k, {}))

    def _compare(self, wants, haveing):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Lag_interfaces network resource.
        """

        for key, entry in wants.items():
            begin = len(self.commands)
            if entry != haveing.pop(key, {}):
                self.addcmd(entry, "channel", False)
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(entry, "member", False))

        # remove remaining items in have for replaced
        for key, entry in haveing.items():
            if key:
                begin = len(self.commands)
                self.addcmd(entry, "channel", True)
                if len(self.commands) != begin:
                    self.commands.insert(begin, self._tmplt.render(entry, "member", False))

    def list_to_dict(self, param):
        if param:
            for key, val in iteritems(param):
                if val.get("prefix_lists"):
                    temp_prefix_list = {}
                    for each in val["prefix_lists"]:
                        temp_entries = dict()
                        if each.get("entries"):
                            for every in each["entries"]:
                                temp_entries.update({str(every["sequence"]): every})
                        temp_prefix_list.update(
                            {
                                each["name"]: {
                                    "description": each.get("description"),
                                    "entries": temp_entries,
                                },
                            },
                        )
                    val["prefix_lists"] = temp_prefix_list
