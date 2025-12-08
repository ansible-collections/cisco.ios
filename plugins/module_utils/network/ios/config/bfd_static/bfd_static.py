#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_bfd_static config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_static import (
    Bfd_staticTemplate,
)


class Bfd_static(ResourceModule):
    """
    The ios_bfd_static config class
    """

    def __init__(self, module):
        super(Bfd_static, self).__init__(
            empty_fact_val={"bfd_static_routes": []},
            facts_module=Facts(module),
            module=module,
            resource="bfd_static",
            tmplt=Bfd_staticTemplate(),
        )
        self.parsers = [
            "bfd_static_vrf",
            "bfd_static_vrf_src",
            "bfd_static_interface",
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
        wantd = self._list_to_dict(self.want)
        haved = self._list_to_dict(self.have)

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
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Bfd_static network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)

    def _list_to_dict(self, entry_list):
        """Convert list of BFD static route entries to dict keyed by unique identifier"""
        entry_dict = {}

        if not entry_list:
            return entry_dict

        for entry in entry_list:
            # Create unique key based on route parameters
            key_parts = [entry.get("destination", "")]

            # Add distinguishing parameters based on route type
            if entry.get("vrf"):
                key_parts.append(f"vrf_{entry['vrf']}")
                if entry.get("next_hop"):
                    key_parts.append(f"nh_{entry['next_hop']}")
                elif entry.get("source_vrf") and entry.get("source_ip"):
                    key_parts.append(f"src_{entry['source_vrf']}_{entry['source_ip']}")
            elif entry.get("interface"):
                key_parts.append(f"int_{entry['interface']}")

            key = "_".join(key_parts)
            entry_dict[key] = entry

        return entry_dict
