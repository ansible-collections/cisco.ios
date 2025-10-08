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
            import debugpy

            debugpy.listen(3000)
            debugpy.wait_for_client()
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
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_complex_attrs(
            want.get("standby_options", {}),
            have.get("standby_options", {}),
        )
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

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
                # remove extra ip or track
                for hkey, hentry in standby_have.get(x, {}).items():
                    self.compare(parsers=self.complex_list_parsers, want={}, have={x: hentry})

        # remove group via numbers
        for not_req_grp in have_group.values():
            self.commands.append(self._tmplt.render(not_req_grp, "group_no", True))

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
                            temp_ipv6[ip6s] = {"address": ip6s}
                        standby_grp["ipv6_addr"] = temp_ipv6
                    temp_track = {}
                    if standby_grp.get("track"):
                        for trk in standby_grp.get("track", {}):
                            temp_track[trk.get("track_no")] = trk
                        standby_grp["track"] = temp_track
                    temp_standby_grp[standby_grp.get("group_no")] = standby_grp

                if val.get("standby_options", {}):
                    val["standby_options"] = temp_standby_grp

    # def _xxcompare_complex_attrs(self, want, have):
    #     """Compare list items followed by non list items in standby_groups"""
    #     want_standby_group = want.get("standby_groups", {})
    #     have_standby_group = have.get("standby_groups", {})
    #     parser_dict = {
    #         "timers.msec": "timers",
    #         "follow.follow": "follow",
    #         "authentication.plain_text": "authentication",
    #         "authentication.md5": "authentication",
    #     }
    #     for group_number, wanting_data in want_standby_group.items():
    #         having_data = have_standby_group.get(group_number, {})
    #         if having_data.get("priority") == 100:
    #             # Default to priority to 100 if not specified, idempotent behavior
    #             wanting_data["priority"] = 100

    #         for _parser in self.complex_parsers:
    #             wantd = wanting_data.get(_parser, {})
    #             haved = having_data.get(_parser, {})
    #             for key, wanting_parser_data in wantd.items():
    #                 having_parser_data = {}
    #                 if haved:
    #                     having_parser_data = haved.pop(key, {})
    #                     if having_parser_data:
    #                         having_parser_data.update({"group_no": group_number})
    #                 wanting_parser_data.update({"group_no": group_number})
    #                 if having_parser_data and having_parser_data != wanting_parser_data:
    #                     self.compare(parsers=[_parser], want={}, have={_parser: having_parser_data})
    #                 self.compare(
    #                     parsers=[_parser],
    #                     want={_parser: wanting_parser_data},
    #                     have={_parser: having_parser_data},
    #                 )

    #         if wanting_data.get("ipv6"):
    #             wantd_ipv6 = wanting_data.pop("ipv6", {})
    #             haved_ipv6 = having_data.pop("ipv6", {})
    #             # this is to preserve the order in which ipv6 addresses are applied to the device
    #             is_ipv6_idempotent = False
    #             dt_want = {w_add: w_add for w_add in wantd_ipv6.get("addresses", {})}
    #             dt_have = {h_add: h_add for h_add in haved_ipv6.get("addresses", {})}
    #             if dt_want == dt_have:
    #                 is_ipv6_idempotent = True

    #             for key, w_ipv6 in wantd_ipv6.items():
    #                 if key == "addresses" and not is_ipv6_idempotent:
    #                     if self.state != "merged" and haved_ipv6.get("addresses"):
    #                         self.commands.append(f"no standby {group_number} ipv6")
    #                     for addr in w_ipv6:
    #                         self.commands.append(f"standby {group_number} ipv6 {addr}")
    #                 if key == "autoconfig":
    #                     if w_ipv6 is True and not haved_ipv6.get("autoconfig", False):
    #                         self.commands.append(f"standby {group_number} ipv6 autoconfig")
    #                     else:
    #                         self.commands.append(f"no standby {group_number} ipv6 autoconfig")

    #         for _par in self.non_complex_parsers:
    #             _parser = parser_dict.get(_par, _par)
    #             wantd = wanting_data.get(_parser, {})
    #             if _parser == _par:
    #                 haved = having_data.pop(_parser, {})
    #             else:
    #                 haved = having_data.get(_parser, {})
    #             if haved:
    #                 if isinstance(haved, dict):
    #                     haved.update({"group_no": group_number})
    #                 else:
    #                     haved = {"group_no": group_number, _parser: haved}
    #             if wantd:
    #                 if isinstance(wantd, dict):
    #                     wantd.update({"group_no": group_number})
    #                 else:
    #                     wantd = {"group_no": group_number, _parser: wantd}
    #                 self.compare(parsers=[_par], want={_parser: wantd}, have={_parser: haved})
    #         for key, value in parser_dict.items():
    #             haved = having_data.pop(value, {})

    #     # Removal of unecessary configs in have_standby_group
    #     for group_number, having_data in have_standby_group.items():
    #         if having_data:
    #             if having_data.get("ipv6"):
    #                 haved_ipv6 = having_data.pop("ipv6", {})
    #                 if haved_ipv6.get("addresses") or haved_ipv6.get("autoconfig", False):
    #                     self.commands.append(f"no standby {group_number} ipv6")
    #             for _parser in self.complex_parsers:
    #                 haved = having_data.pop(_parser, {})
    #                 for key, having_parser_data in haved.items():
    #                     having_parser_data.update({"group_no": group_number})
    #                     self.compare(parsers=[_parser], want={}, have={_parser: having_parser_data})
    #             for _par in self.non_complex_parsers:
    #                 _parser = parser_dict.get(_par, _par)
    #                 if _parser == _par:
    #                     haved = having_data.pop(_parser, {})
    #                 else:
    #                     haved = having_data.get(_parser, {})
    #                 if haved:
    #                     if isinstance(haved, dict):
    #                         haved.update({"group_no": group_number})
    #                     else:
    #                         haved = {"group_no": group_number, _parser: haved}
    #                     self.compare(parsers=[_par], want={}, have={_parser: haved})
    #             for key, value in parser_dict.items():
    #                 haved = having_data.pop(value, {})
