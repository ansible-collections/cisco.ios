#
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.interfaces import (
    InterfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


class Interfaces(ResourceModule):
    """
    The ios_interfaces config class
    """

    def __init__(self, module):
        super(Interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="interfaces",
            tmplt=InterfacesTemplate(),
        )
        self.parsers = [
            "description",
            "speed",
            "mtu",
            "duplex",
            "template",
            "mac_address",
            "service_policy.input",
            "service_policy.output",
            "service_policy.type_options.access_control",
            "service_policy.type_options.epbr",
            "service_policy.type_options.nwpi",
            "service_policy.type_options.packet_service",
            "service_policy.type_options.service_chain",
            "logging.trunk_status",
            "logging.subif_link_status",
            "logging.status",
            "logging.spanning_tree",
            "logging.nfas_status",
            "logging.bundle_status",
            "logging.link_status",
            "snmp.ifindex",
            "snmp.trap",
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
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        for each in wantd, haved:
            self.normalize_interface_names(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state in ["deleted", "purged"]:
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

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
        for the Interfaces network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        want_enabled = want.get("enabled")
        have_enabled = have.get("enabled")
        if want_enabled is not None:
            if want_enabled != have_enabled:
                if want_enabled is True:
                    self.addcmd(want, "enabled", True)
                else:
                    self.addcmd(want, "enabled", False)
        elif not want and self.state == "overridden":
            self.addcmd(have, "enabled", False)
        elif not want and self.state == "deleted":
            if have_enabled:
                self.addcmd(have, "enabled", False)
        if want.get("mode") != have.get("mode"):
            if want.get("mode") == "layer3":
                self.addcmd(want, "mode", True)
            else:
                if want:
                    self.addcmd(want, "mode", False)
                elif have.get("mode"):  # can oly have layer2 as switchport no show cli
                    # handles deleted as want be blank and only
                    self.addcmd(have, "mode", False)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "interface", False))

    def purge(self, have):
        """Handle operation for purged state"""
        self.commands.append(self._tmplt.render(have, "interface", True))

    def normalize_interface_names(self, param):
        if param:
            for k, val in param.items():
                val["name"] = normalize_interface(val["name"])
        return param
