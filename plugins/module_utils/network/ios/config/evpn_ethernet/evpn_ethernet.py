#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_evpn_ethernet config file.
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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.evpn_ethernet import (
    Evpn_ethernetTemplate,
)


class Evpn_ethernet(ResourceModule):
    """
    The ios_evpn_ethernet config class
    """

    def __init__(self, module):
        super(Evpn_ethernet, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="evpn_ethernet",
            tmplt=Evpn_ethernetTemplate(),
        )
        self.parsers = [
            "redundancy.all_active",
            "redundancy.single_active",
            "identifier",
            "df_election.wait_time",
            "df_election.preempt_time",
        ]  # mind the order of the parsers

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
        wantd = {entry["segment"]: entry for entry in self.want}
        haved = {entry["segment"]: entry for entry in self.have}

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    if self.state == "deleted":
                        self._compare(want={}, have=have)
                    else:
                        self.purge(have)

        if self.state == "purged":
            for k, have in haved.items():
                self.purge(have)
        else:
            for k, want in wantd.items():
                self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Evpn_ethernet network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "segment", False))

    def purge(self, have):
        """Handle operation for purged state"""
        self.commands.append(self._tmplt.render(have, "segment", True))
