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
            "mac_refresh",
            "version",
            "delay",
            "bfd",
            "use-bia",
            "follow",
            "redirect.md5.key_chain",
            "redirect.md5.key_string",
            "redirect.md5.key_string_without_encryption",
            "redirect.timers",
        ]
        self.complex_parsers = ["track", "ip"]
        self.non_complex_parsers = [
            "priority",
            "timers.msec",
            "timers",
            "follow.follow",
            "preempt",
            "mac_address",
            "group_name",
            "authentication.plain_text",
            "authentication.md5",
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

        wantd = self.convert_list_to_dict(wantd)
        haved = self.convert_list_to_dict(haved)

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
            if not want.get("version") and want.get("standby_groups"):
                # Default to version 1 if not specified, idempotent behavior
                want["version"] = 1
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Hsrp_interfaces network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_complex_attrs(want, have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def convert_list_to_dict(self, data):
        def list_to_dict(lst, key_name):
            return {item[key_name]: item for item in lst if key_name in item}

        result = {}

        for iface_name, iface_data in data.items():
            iface_result = iface_data.copy()
            standby_groups = iface_data.get("standby_groups", [])
            group_dict = {}

            for group in standby_groups:
                group_no = group.get("group_no")
                if group_no is None:
                    continue

                new_group = {}

                for key, value in group.items():
                    if key == "ip" and isinstance(value, list):
                        new_group[key] = list_to_dict(value, "virtual_ip")
                    elif key == "track" and isinstance(value, list):
                        new_group[key] = list_to_dict(value, "track_no")
                    elif key != "group_no":
                        new_group[key] = value

                group_dict[group_no] = new_group

            iface_result["standby_groups"] = group_dict
            result[iface_name] = iface_result

        return result

    def _compare_complex_attrs(self, want, have):
        """Compare list items followed by non list items in standby_groups"""
        want_standby_group = want.get("standby_groups", {})
        have_standby_group = have.get("standby_groups", {})
        parser_dict = {
            "timers.msec": "timers",
            "follow.follow": "follow",
            "authentication.plain_text": "authentication",
            "authentication.md5": "authentication",
        }
        for group_number, wanting_data in want_standby_group.items():
            having_data = have_standby_group.get(group_number, {})
            if having_data.get("priority") == 100:
                # Default to priority to 100 if not specified, idempotent behavior
                wanting_data["priority"] = 100

            for _parser in self.complex_parsers:
                wantd = wanting_data.get(_parser, {})
                haved = having_data.get(_parser, {})
                for key, wanting_parser_data in wantd.items():
                    having_parser_data = {}
                    if haved:
                        having_parser_data = haved.pop(key, {})
                        if having_parser_data:
                            having_parser_data.update({"group_no": group_number})
                    wanting_parser_data.update({"group_no": group_number})
                    if having_parser_data and having_parser_data != wanting_parser_data:
                        self.compare(parsers=[_parser], want={}, have={_parser: having_parser_data})
                    self.compare(
                        parsers=[_parser],
                        want={_parser: wanting_parser_data},
                        have={_parser: having_parser_data},
                    )

            if wanting_data.get("ipv6"):
                wantd_ipv6 = wanting_data.pop("ipv6", {})
                haved_ipv6 = having_data.pop("ipv6", {})
                # this is to preserve the order in which ipv6 addresses are applied to the device
                is_ipv6_idempotent = False
                dt_want = {w_add: w_add for w_add in wantd_ipv6.get("addresses", {})}
                dt_have = {h_add: h_add for h_add in haved_ipv6.get("addresses", {})}
                if dt_want == dt_have:
                    is_ipv6_idempotent = True

                for key, w_ipv6 in wantd_ipv6.items():
                    if key == "addresses" and not is_ipv6_idempotent:
                        if self.state != "merged" and haved_ipv6.get("addresses"):
                            self.commands.append(f"no standby {group_number} ipv6")
                        for addr in w_ipv6:
                            self.commands.append(f"standby {group_number} ipv6 {addr}")
                    if key == "autoconfig":
                        if w_ipv6 is True and not haved_ipv6.get("autoconfig", False):
                            self.commands.append(f"standby {group_number} ipv6 autoconfig")
                        else:
                            self.commands.append(f"no standby {group_number} ipv6 autoconfig")

            for _par in self.non_complex_parsers:
                _parser = parser_dict.get(_par, _par)
                wantd = wanting_data.get(_parser, {})
                if _parser == _par:
                    haved = having_data.pop(_parser, {})
                else:
                    haved = having_data.get(_parser, {})
                if haved:
                    if isinstance(haved, dict):
                        haved.update({"group_no": group_number})
                    else:
                        haved = {"group_no": group_number, _parser: haved}
                if wantd:
                    if isinstance(wantd, dict):
                        wantd.update({"group_no": group_number})
                    else:
                        wantd = {"group_no": group_number, _parser: wantd}
                    self.compare(parsers=[_par], want={_parser: wantd}, have={_parser: haved})
            for key, value in parser_dict.items():
                haved = having_data.pop(value, {})

        # Removal of unecessary configs in have_standby_group
        for group_number, having_data in have_standby_group.items():
            if having_data:
                if having_data.get("ipv6"):
                    haved_ipv6 = having_data.pop("ipv6", {})
                    if haved_ipv6.get("addresses") or haved_ipv6.get("autoconfig", False):
                        self.commands.append(f"no standby {group_number} ipv6")
                for _parser in self.complex_parsers:
                    haved = having_data.pop(_parser, {})
                    for key, having_parser_data in haved.items():
                        having_parser_data.update({"group_no": group_number})
                        self.compare(parsers=[_parser], want={}, have={_parser: having_parser_data})
                for _par in self.non_complex_parsers:
                    _parser = parser_dict.get(_par, _par)
                    if _parser == _par:
                        haved = having_data.pop(_parser, {})
                    else:
                        haved = having_data.get(_parser, {})
                    if haved:
                        if isinstance(haved, dict):
                            haved.update({"group_no": group_number})
                        else:
                            haved = {"group_no": group_number, _parser: haved}
                        self.compare(parsers=[_par], want={}, have={_parser: haved})
                for key, value in parser_dict.items():
                    haved = having_data.pop(value, {})
