#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_bgp_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)


class Bgp_global(ResourceModule):
    """
    The cisco.ios_bgp_global config class
    """

    parsers = [
        "as_number",
        "bgp.additional_paths",
        "bgp.dampening",
        "bgp.graceful_shutdown",
        "route_server_context",
        "synchronization",
        "table_map",
        "timers",
    ]

    def __init__(self, module):
        super(Bgp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_global",
            tmplt=Bgp_globalTemplate(),
        )

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        if self.want:
            wantd = {self.want["as_number"]: self.want}
        else:
            wantd = {}
        if self.have:
            haved = {self.have["as_number"]: self.have}
        else:
            haved = {}

        wantd, haved = self.list_to_dict(wantd, haved)
        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted" and self.have:
            if (
                not self.want
                or self.have.get("as_number") == self.want.get("as_number")
                and len(self.have) > 1
            ):
                self.addcmd(
                    {"as_number": haved[list(haved)[0]].pop("as_number")},
                    "as_number",
                    False,
                )
                self.compare(
                    parsers=self.parsers, want={}, have=haved[list(haved)[0]]
                )
                self._compare(want={}, have=haved[list(haved)[0]])
                self._list_params_compare(want={}, have=haved[list(haved)[0]])
            wantd = {}

        if self.state == "purged" and self.have:
            if (
                not self.want
                or (self.have.get("as_number") == self.want.get("as_number"))
                and len(self.have) >= 1
            ):
                self.addcmd(
                    {"as_number": haved[list(haved)[0]].pop("as_number")},
                    "as_number",
                    True,
                )
                wantd = {}

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospf_interfaces network resource.
        """
        if want != have and self.state != "deleted":
            self.addcmd(have, "as_number", False)
            self.compare(parsers=self.parsers, want=want, have=have)
            self._bgp_config_compare(want.get("bgp"), have.get("bgp"))
            self._list_params_compare(want, have)
        elif self.state == "deleted":
            self._bgp_config_compare(dict(), have.get("bgp"))

    def _bgp_config_compare(self, want, have):
        if want and have and want != have and isinstance(want, dict):
            set_have = True
            for k, val in iteritems(want):
                if isinstance(val, dict):
                    if k in have:
                        self.compare(
                            parsers=["bgp.config"],
                            want={"bgp": {k: val}},
                            have={"bgp": {k: have[k]}},
                        )
                    if k in have and self.state == "replaced":
                        if set_have:
                            self.compare(
                                parsers=["bgp.config"],
                                want=dict(),
                                have={"bgp": {k: have[k]}},
                            )
                        self.compare(
                            parsers=["bgp.config"],
                            want={"bgp": {k: val}},
                            have={"bgp": {k: have[k]}},
                        )
                    else:
                        self.compare(
                            parsers=["bgp.config"],
                            want={"bgp": {k: val}},
                            have=dict(),
                        )
        elif want and not have:
            for k, val in iteritems(want):
                if not isinstance(val, list):
                    self.compare(
                        parsers=["bgp.config"],
                        want={"bgp": {k: val}},
                        have=dict(),
                    )
        elif not want and have:
            for k, val in iteritems(have):
                if not isinstance(val, list):
                    self.compare(
                        parsers=["bgp.config"],
                        want=dict(),
                        have={"bgp": {k: val}},
                    )

    def _list_params_compare(self, want, have):
        def multi_compare(parser, want, have):
            if want:
                dict_iter = want
            else:
                dict_iter = have
            for k, v in iteritems(dict_iter):
                if parser == "neighbor":
                    type = None
                    if want.get("address") or have.get("address"):
                        type = "address"
                        want_type_val = want.get("address")
                        have_type_val = have.get("address")
                    if want.get("tag") or have.get("tag"):
                        type = "tag"
                        want_type_val = want.get("tag")
                        have_type_val = have.get("tag")
                    if want.get("ipv6_adddress") or have.get("ipv6_address"):
                        type = "ipv6_adddress"
                        want_type_val = want.get("ipv6_adddress")
                        have_type_val = have.get("ipv6_adddress")
                    if want and have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v, type: want_type_val}},
                            have={
                                parser: {
                                    k: have.get(k, {}),
                                    type: have_type_val,
                                }
                            },
                        )
                    elif not have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v, type: want_type_val}},
                            have=dict(),
                        )
                    elif not want:
                        self.compare(
                            parsers=[parser],
                            want=dict(),
                            have={parser: {k: v, type: have_type_val}},
                        )
                if parser == "redistribute":
                    if want and have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v}},
                            have={parser: {k: have.get(k, {})}},
                        )
                    elif not have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v}},
                            have=dict(),
                        )
                    elif not want:
                        self.compare(
                            parsers=[parser],
                            want=dict(),
                            have={parser: {k: v}},
                        )

        for every in ["bgp", "neighbor", "redistribute"]:

            param_want = want.get(every)
            param_have = have.get(every)
            if param_want and param_want != param_have:
                set_have = True
                if every == "bgp":
                    for each in ["bestpath", "nopeerup_delay"]:
                        set_have = True
                        for k, v in iteritems(param_want.get(each)):
                            if (
                                param_have
                                and k in param_have.get(each)
                                and self.state == "merged"
                            ):
                                if k in param_have.get(each):
                                    self.compare(
                                        parsers=[every + "." + each],
                                        want={"bgp": {each: {k: v}}},
                                        have={
                                            "bgp": {
                                                each: {
                                                    k: param_have.get(
                                                        each, {}
                                                    )[k]
                                                }
                                            }
                                        },
                                    )

                            elif param_have and self.state == "replaced":
                                if set_have and param_have.get(each):
                                    if isinstance(each, dict):
                                        for key_have, val_have in iteritems(
                                            param_have.get(each)
                                        ):
                                            multi_compare(
                                                parser=every,
                                                want=dict(),
                                                have=val_have,
                                            )
                                    else:
                                        # q(param_have, param_want)
                                        temp_have = {
                                            each: {i: param_have[each][i]}
                                            for i in list(param_have[each])
                                            if i not in param_want[each]
                                        }
                                        temp_want = {
                                            each: {i: param_want[each][i]}
                                            for i in list(param_want[each])
                                            if i not in param_have[each]
                                        }
                                        # q(temp_have)
                                        if temp_have:
                                            self.compare(
                                                parsers=[every + "." + each],
                                                want=dict(),
                                                have={"bgp": temp_have},
                                            )
                                        if temp_want:
                                            self.compare(
                                                parsers=[every + "." + each],
                                                want={"bgp": temp_want},
                                                have=dict(),
                                            )
                                    set_have = False
                            else:
                                self.compare(
                                    parsers=[every + "." + each],
                                    want={"bgp": {each: {k: v}}},
                                    have=dict(),
                                )
                if every == "neighbor" or every == "redistribute":
                    for k, v in iteritems(param_want):
                        if every == "neighbor":
                            if param_have and self.state == "merged":
                                multi_compare(
                                    parser=every,
                                    want=v,
                                    have=param_have.pop(k, {}),
                                )
                            elif param_have and self.state == "replaced":
                                if set_have:
                                    for key_have, val_have in iteritems(
                                        param_have
                                    ):
                                        multi_compare(
                                            parser=every,
                                            want=dict(),
                                            have=val_have,
                                        )
                                    set_have = False
                                multi_compare(
                                    parser=every, want=v, have=dict()
                                )
                            else:
                                multi_compare(
                                    parser=every, want=v, have=dict()
                                )
                            self.commands = (
                                [
                                    each
                                    for each in self.commands
                                    if "neighbor" not in each
                                ]
                                + [
                                    each
                                    for each in self.commands
                                    if "remote-as" in each
                                    and "neighbor" in each
                                ]
                                + [
                                    each
                                    for each in self.commands
                                    if "remote-as" not in each
                                    and "neighbor" in each
                                ]
                            )
                        elif every == "redistribute":
                            if param_have and self.state == "merged":
                                multi_compare(
                                    parser=every,
                                    want={k: v},
                                    have={k: param_have.pop(k, {})},
                                )
                            if param_have and self.state == "replaced":
                                if set_have:
                                    for key_have, val_have in iteritems(
                                        param_have
                                    ):
                                        multi_compare(
                                            parser=every,
                                            want=dict(),
                                            have=val_have,
                                        )
                                    set_have = False
                                multi_compare(
                                    parser=every, want={k: v}, have=dict()
                                )
                            else:
                                multi_compare(
                                    parser=every, want={k: v}, have=dict()
                                )
            elif param_have and self.state == "deleted":
                del_config_have = True
                if param_have:
                    for k, v in iteritems(param_have):
                        if every == "bgp" and del_config_have:
                            for each in ["bestpath", "nopeerup_delay"]:
                                for k, v in iteritems(param_have.get(each)):
                                    self.compare(
                                        parsers=[every + "." + each],
                                        want=dict(),
                                        have={"bgp": {each: {k: v}}},
                                    )
                            del_config_have = False
                        elif every == "neighbor":
                            multi_compare(parser=every, want=dict(), have=v)
                        elif every == "redistribute":
                            if param_have:
                                multi_compare(
                                    parser=every, want=dict(), have={k: v}
                                )

    def list_to_dict(self, wantd, haved):
        for thing in wantd, haved:
            if thing:
                for key, val in iteritems(thing):
                    for every in ["bgp", "neighbor", "redistribute"]:
                        value = val.get(every)
                        if value:
                            if isinstance(value, dict):
                                for k, v in iteritems(val.get(every)):
                                    if isinstance(v, list):
                                        temp = dict()
                                        temp[k] = {}
                                        for each in v:
                                            temp[k].update(each)
                                        val[every][k] = temp[k]
                            elif isinstance(value, list):
                                temp = dict()
                                temp[every] = {}
                                for each in value:
                                    if every == "neighbor":
                                        if each.get("address"):
                                            temp[every].update(
                                                {each.get("address"): each}
                                            )
                                        elif each.get("tag"):
                                            temp[every].update(
                                                {each.get("tag"): each}
                                            )
                                        elif each.get("ipv6_adddress"):
                                            temp[every].update(
                                                {
                                                    each.get(
                                                        "ipv6_adddress"
                                                    ): each
                                                }
                                            )
                                    elif every == "redistribute":
                                        temp[every].update(each)
                                val[every] = temp[every]
        return wantd, haved
