#
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acl_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acl_interfaces import (
    Acl_interfacesTemplate,
)


class Acl_interfaces(ResourceModule):
    """
    The ios_acl_interfaces class
    """

    def __init__(self, module):
        super(Acl_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="acl_interfaces",
            tmplt=Acl_interfacesTemplate(),
        )

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
        """Select the appropriate function based on the state provided
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        # convert list of dicts to dicts of dicts
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # turn all lists of dicts into dicts prior to merge
        for entry in wantd, haved:
            self._list_to_dict(entry)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        begin = len(self.commands)
        self._compare_lists(want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "interface", False))

    def _compare_lists(self, want, have):
        wdict = want.get("access_groups", {})
        hdict = have.get("access_groups", {})

        for afi in ("ipv4", "ipv6"):
            wacls = wdict.pop(afi, {}).pop("acls", {})
            hacls = hdict.pop(afi, {}).pop("acls", {})

            for key, entry in wacls.items():
                if entry != hacls.pop(key, {}):
                    entry["afi"] = afi
                    self.addcmd(entry, "access_groups", False)
            # remove remaining items in have for replaced
            for entry in hacls.values():
                entry["afi"] = afi
                self.addcmd(entry, "access_groups", True)

    def _list_to_dict(self, entry):
        for item in entry.values():
            for ag in item.get("access_groups", []):
                ag["acls"] = {
                    subentry["direction"]: {
                        "name": to_text(subentry["name"]),
                        "direction": subentry["direction"],
                    }
                    for subentry in ag.get("acls", [])
                }
            item["access_groups"] = {
                subentry["afi"]: subentry for subentry in item.get("access_groups", [])
            }
