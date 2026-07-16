#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_bfd_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_interfaces import (
    Bfd_interfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


class Bfd_interfaces(ResourceModule):
    """
    The ios_bfd_interfaces config class
    """

    def __init__(self, module):
        super(Bfd_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bfd_interfaces",
            tmplt=Bfd_interfacesTemplate(),
        )
        self.parsers = ["bfd", "echo", "jitter", "local_address", "interval", "template"]

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

        for each in wantd, haved:
            self.normalize_interface_names(each)

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
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Bfd_interfaces network resource.
        """
        begin = len(self.commands)

        if want.get("bfd") is False:
            if have.get("bfd", True) is not False:
                self.commands.append("no bfd enable")
            if have.get("bfd"):
                self.have.pop("bfd", None)
            if want.get("bfd"):
                self.want.pop("bfd", None)

        self.compare(parsers=self.parsers, want=want, have=have)

        for tag in ["echo", "jitter"]:
            if want.get(tag) is False:
                if have.get(tag, True) is not False:
                    self.commands.append("no bfd " + tag)
                if have.get(tag):
                    self.have.pop(tag, None)
                if want.get(tag):
                    self.want.pop(tag, None)

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def normalize_interface_names(self, param):
        if param:
            for k, val in param.items():
                val["name"] = normalize_interface(val["name"])
        return param
