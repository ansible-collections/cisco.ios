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
        self.complex_parsers = ["track", "ipv6.link", "ipv6.prefix", "ipv6.autoconfig", "ip"]
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
                    elif key == "ipv6" and isinstance(value, list):
                        new_group[key] = list_to_dict(value, "ipv6")
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
            for _par in self.complex_parsers:
                _parser = _par
                if len(_parser) >= 4 and _parser[:4] == "ipv6":
                    _parser = "ipv6"
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
                        self.compare(parsers=[_par], want={}, have={_parser: having_parser_data})
                    self.compare(
                        parsers=[_par],
                        want={_parser: wanting_parser_data},
                        have={_parser: having_parser_data},
                    )

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
                # if haved and wantd != haved:
                #    self.compare(parsers=[_par], want={}, have={_parser: haved})
                if wantd:
                    self.compare(parsers=[_par], want={_parser: wantd}, have={_parser: haved})
            for key, value in parser_dict.items():
                haved = having_data.pop(value, {})
        # Removal of unecessary configs in have_standby_group
        for group_number, having_data in have_standby_group.items():
            if having_data:
                for _par in self.complex_parsers:
                    _parser = _par
                    if len(_parser) >= 4 and _parser[:4] == "ipv6":
                        _parser = "ipv6"
                    haved = having_data.pop(_parser, {})
                    for key, having_parser_data in haved.items():
                        having_parser_data.update({"group_no": group_number})
                        self.compare(parsers=[_par], want={}, have={_parser: having_parser_data})
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
