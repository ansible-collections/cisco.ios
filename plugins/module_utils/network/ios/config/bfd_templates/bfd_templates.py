#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_bfd_templates config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_templates import (
    Bfd_templatesTemplate,
)


class Bfd_templates(ResourceModule):
    """
    The ios_bfd_templates config class
    """

    def __init__(self, module):
        super(Bfd_templates, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bfd_templates",
            tmplt=Bfd_templatesTemplate(),
        )
        self.parsers = ["interval", "dampening", "authentication", "echo"]

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
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            # Filter to only templates specified in want, or all if want is empty
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            # For deleted state, compare empty want with have to generate  no commands
            for k, have in haved.items():
                self._compare(want={"name": have["name"], "hop": have["hop"]}, have=have)

        # if state is purged, remove entire templates at top level
        elif self.state == "purged":
            # Filter to only templates specified in want, or all if want is empty
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            for k, have in haved.items():
                self.purge(have)

        # remove superfluous config for overridden
        elif self.state == "overridden":
            for k, have in haved.items():
                if k not in wantd:
                    self.purge(have)
            # Process templates in the original order from self.want to ensure deterministic output
            for entry in self.want:
                k = entry["name"]
                if k in wantd:
                    self._compare(want=wantd[k], have=haved.pop(k, {}))

        else:
            # Process templates in the original order from self.want to ensure deterministic output
            for entry in self.want:
                k = entry["name"]
                if k in wantd:
                    self._compare(want=wantd[k], have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Bfd_templates network resource.
        """
        begin = len(self.commands)

        # Handle echo removal - needs to come first in command order
        # Check if echo should be removed (present in have but not in want, or explicitly False in want)
        parsers = self.parsers
        if have.get("echo") and not want.get("echo"):
            self.commands.append("no echo")
            # Exclude echo from parsers since we've already handled it
            parsers = [p for p in self.parsers if p != "echo"]

        self.compare(parsers=parsers, want=want, have=have)

        # Handle authentication replacement - need to negate old auth before adding new one
        if have.get("authentication") and want.get("authentication"):
            if have["authentication"] != want["authentication"]:
                # Find the index of the new authentication command
                auth_cmd_prefix = (
                    f"authentication {want['authentication']['type'].replace('_', '-')}"
                )
                for i in range(begin, len(self.commands)):
                    if self.commands[i].startswith(auth_cmd_prefix):
                        # Insert the no command before the new authentication
                        no_auth_cmd = self._tmplt.render(have, "authentication", True)
                        self.commands.insert(i, no_auth_cmd)
                        break

        # Insert the bfd-template header command at the beginning
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def purge(self, have):
        """Handle operation for purged state - removes entire template"""
        self.commands.append(self._tmplt.render(have, "name", True))
