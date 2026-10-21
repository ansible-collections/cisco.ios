# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_flow_monitor_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.flow_monitor_interfaces import (
    Flow_monitor_interfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


class Flow_monitor_interfaces(ResourceModule):
    """
    The ios_flow_monitor_interfaces config class
    """

    def __init__(self, module):
        super(Flow_monitor_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="flow_monitor_interfaces",
            tmplt=Flow_monitor_interfacesTemplate(),
        )
        self.parsers = []

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
        wantd = {entry["name"]: entry for entry in (self.want or [])}
        haved = {entry["name"]: entry for entry in (self.have or [])}

        for each in wantd, haved:
            self._normalize_interface_names(each)

        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._delete_interface_flow_monitors(have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Compare want vs have for a single interface and generate commands."""
        intf_name = want.get("name") or have.get("name")

        want_monitors = {(m["monitor"], m["direction"]): m for m in want.get("flow_monitors", [])}
        have_monitors = {(m["monitor"], m["direction"]): m for m in have.get("flow_monitors", [])}

        cmds = []

        if self.state in ["replaced", "overridden"]:
            for key, have_m in have_monitors.items():
                if key not in want_monitors:
                    proto = have_m.get("protocol", "ip")
                    cmds.append(
                        "no {0} flow monitor {1} sampler {2} {3}".format(
                            proto,
                            have_m["monitor"],
                            have_m["sampler"],
                            have_m["direction"],
                        ),
                    )

        for key, want_m in want_monitors.items():
            have_m = have_monitors.get(key, {})
            if want_m != have_m:
                proto = want_m.get("protocol", "ip")
                cmds.append(
                    "{0} flow monitor {1} sampler {2} {3}".format(
                        proto,
                        want_m["monitor"],
                        want_m["sampler"],
                        want_m["direction"],
                    ),
                )

        if cmds:
            self.commands.append("interface {0}".format(intf_name))
            self.commands.extend(cmds)

    def _delete_interface_flow_monitors(self, have):
        """Remove all flow monitor assignments from an interface."""
        cmds = []
        for m in have.get("flow_monitors", []):
            proto = m.get("protocol", "ip")
            cmds.append(
                "no {0} flow monitor {1} sampler {2} {3}".format(
                    proto,
                    m["monitor"],
                    m["sampler"],
                    m["direction"],
                ),
            )
        if cmds:
            self.commands.append("interface {0}".format(have["name"]))
            self.commands.extend(cmds)

    def _normalize_interface_names(self, param):
        if param:
            for k, val in param.items():
                val["name"] = normalize_interface(val["name"])
        return param
