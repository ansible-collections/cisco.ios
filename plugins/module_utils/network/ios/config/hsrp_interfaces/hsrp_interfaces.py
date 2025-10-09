#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_hsrp_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.hsrp_interfaces import (
    Hsrp_interfacesTemplate,
)


class Hsrp_interfaces(ResourceModule):
    """
    The ios_hsrp_interfaces config class
    """

    def __init__(self, module):
        super(Hsrp_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="hsrp_interfaces",
            tmplt=Hsrp_interfacesTemplate(),
        )
        self.parsers = [
            "bfd",
            "version",
            "delay",
            "mac_refresh",
            "use_bia",
            "redirect.timers",
            "redirect.advertisement.authentication",
        ]
        self.complex_parsers = [
            "follow",
            "mac_address",
            "group_name",
            "preempt",
            "priority",
            "timers",
            "authentication",
            "ipv6.autoconfig",
        ]
        self.complex_list_parsers = [
            "ip",
            "ipv6_addr",
            "track",
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
        if self.want:
            wantd = {}
            for each in self.want:
                wantd.update({each["name"]: each})
        else:
            wantd = {}
        if self.have:
            haved = {}
            for each in self.have:
                haved.update({each["name"]: each})
        else:
            haved = {}

        for each in wantd, haved:
            self.list_to_dict(each)

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
        for the Hsrp_interfaces network resource.
        """
        begin_count = len(self.commands)

        self.handle_defaults(want, have)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_complex_attrs(
            want.get("standby_options", {}),
            have.get("standby_options", {}),
        )

        end_count = len(self.commands)
        if end_count != begin_count:
            # standby version when configured shall be at the first but when removed shall be at last
            # TODO cleanup the first negation command
            if "no standby version 2" in self.commands[begin_count:end_count]:
                self.commands.append("no standby version 2")

            self.commands.insert(begin_count, self._tmplt.render(want or have, "name", False))

    def _compare_complex_attrs(self, want_group, have_group):
        for grp_no, standby_want in want_group.items():
            standby_have = have_group.pop(grp_no, {})

            # compare non list attributes directly
            self.compare(parsers=self.complex_parsers, want=standby_want, have=standby_have)
            # compare list attributes directly
            for x in self.complex_list_parsers:
                for wkey, wentry in standby_want.get(x, {}).items():
                    hentry = standby_have.get(x, {}).pop(wkey, {})
                    if wentry != hentry:
                        if wkey == "autoconfig":
                            continue
                        wentry.update({"group_no": grp_no})
                        if hentry:
                            hentry.update({"group_no": grp_no})
                        self.compare(
                            parsers=self.complex_list_parsers,
                            want={x: wentry},
                            have={x: hentry},
                        )
                # remove extra ip/v6 or track
                for hkey, hentry in standby_have.get(x, {}).items():
                    hentry.update({"group_no": grp_no})
                    self.compare(parsers=self.complex_list_parsers, want={}, have={x: hentry})

        # remove group via numbers
        for not_req_grp in have_group.values():
            self.commands.append(f"no standby {not_req_grp.get('group_no')}")

    def handle_defaults(self, want, have):
        if not want.get("version") and want.get("standby_options"):
            want["version"] = 1
        if not have.get("version") and have.get("standby_options"):
            have["version"] = 1

    def list_to_dict(self, param):
        if param:
            for _k, val in param.items():
                temp_standby_grp = {}

                for standby_grp in val.get("standby_options", {}):
                    temp_ip = {}
                    if standby_grp.get("ip"):
                        for ips in standby_grp.get("ip", {}):
                            temp_ip[ips.get("virtual_ip")] = ips
                        standby_grp["ip"] = temp_ip
                    temp_ipv6 = {}
                    if standby_grp.get("ipv6"):
                        for ip6s in standby_grp.get("ipv6").get("addresses", {}):
                            temp_ipv6[ip6s.upper()] = {"address": ip6s.upper()}
                        standby_grp["ipv6_addr"] = temp_ipv6
                    temp_track = {}
                    if standby_grp.get("track"):
                        for trk in standby_grp.get("track", {}):
                            temp_track[trk.get("track_no")] = trk
                        standby_grp["track"] = temp_track
                    temp_standby_grp[standby_grp.get("group_no")] = standby_grp

                if val.get("standby_options", {}):
                    val["standby_options"] = temp_standby_grp
