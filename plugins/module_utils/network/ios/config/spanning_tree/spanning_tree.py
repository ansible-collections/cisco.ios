# -*- coding: utf-8 -*-
# Copyright 2023 Timur Nizharadze (@tnizharadze)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_spanning_tree config file.
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
    get_from_dict,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.spanning_tree import (
    Spanning_treeTemplate,
)


class Spanning_tree(ResourceModule):
    """
    The ios_spanning_tree config class
    """

    def __init__(self, module):
        super(Spanning_tree, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="spanning_tree",
            tmplt=Spanning_treeTemplate(),
        )
        self.linear_parsers = [
            "backbonefast",
            "bridge_assurance",
            "etherchannel_guard_misconfig",
            "logging",
            "loopguard_default",
            "mode",
            "pathcost_method",
            "transmit_hold_count",
            "portfast.default",
            "portfast.network_default",
            "portfast.edge_default",
            "portfast.bpdufilter_default",
            "portfast.edge_bpdufilter_default",
            "portfast.bpduguard_default",
            "portfast.edge_bpduguard_default",
            "uplinkfast.enabled",
            "uplinkfast.max_update_rate",
            "mst.simulate_pvst_global",
        ]
        self.complex_parsers = [
            "forward_time",
            "hello_time",
            "max_age",
            "priority",
        ]
        self.mst_parsers = [
            "mst.hello_time",
            "mst.forward_time",
            "mst.max_age",
            "mst.max_hops",
            "mst.priority",
        ]
        self.mst_config_parsers = [
            "mst.configuration",
            "mst.configuration.name",
            "mst.configuration.revision",
            "mst.configuration.instances",
        ]
        self.negated_parsers = [
            "bridge_assurance",
            "etherchannel_guard_misconfig",
            "mst.simulate_pvst_global",
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
        wantd = self.want
        haved = self.have

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = self._dict_copy_merged(wantd, haved)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = self._dict_copy_deleted(want=wantd, have=haved)
            wantd = {}

        self._compare_linear(wantd, haved)
        self._compare_complex(wantd, haved)
        self._compare_mst(wantd, haved)
        self._compare_mst_config(wantd, haved)

    def _compare_linear(self, want, have):
        for x in self.linear_parsers:
            if x == "mode":
                wmode = get_from_dict(want, "mode")
                hmode = get_from_dict(have, "mode")
                if wmode is None and (hmode == "pvst" or hmode == "rapid-pvst"):
                    continue
            if x in self.negated_parsers:
                inw = get_from_dict(want, x)
                inh = get_from_dict(have, x)
                if inw == inh:
                    continue
                if inh is None and not inw:
                    self.addcmd(want, x, True)
                elif inw is None and not inh:
                    self.addcmd(have, x, False)
                elif inw and inh is not None and not inh:
                    self.addcmd(want, x, False)
                continue
            self.compare([x], want=want, have=have)

    def _compare_complex(self, want, have):
        for x in self.complex_parsers:
            self._compare_complex_dict(want, have, "vlan_list", "value", x)

    def _compare_mst(self, want, have):
        wmode = get_from_dict(want, "mode")
        hmode = get_from_dict(have, "mode")
        if not ((wmode is None and (hmode == "mst" or hmode is None)) or wmode == "mst"):
            return
        for x in self.mst_parsers:
            if x == "mst.priority":
                self._compare_complex_dict(want, have, "instance", "value", x)
            else:
                self.compare([x], want=want, have=have)

    def _compare_mst_config(self, want, have):
        cmd_len = len(self.commands)
        for x in self.mst_config_parsers:
            if x == "mst.configuration":
                wx = get_from_dict(want, x)
                hx = get_from_dict(have, x)
                if self.state == "deleted":
                    if hx is not None and not hx:
                        self.compare(parsers=[x], want={}, have=have)
                        return
                    elif hx:
                        self.compare(parsers=[x], want=have, have={})
                    else:
                        return
                elif self.state == "replaced":
                    if wx is None:
                        self.compare(parsers=[x], want={}, have=have)
                        return
                    elif wx:
                        self.compare(parsers=[x], want=want, have={})
                    else:
                        return
                elif wx:
                    self.compare(parsers=[x], want=want, have={})
                else:
                    return
            if x in [
                "mst.configuration.name",
                "mst.configuration.revision",
            ]:
                self.compare(parsers=[x], want=want, have=have)
            if x == "mst.configuration.instances":
                self._compare_complex_dict(want, have, "vlan_list", "instance", x)
        if (cmd_len + 1) == len(self.commands):
            self.commands.pop()
        elif (cmd_len + 1) < len(self.commands):
            self.commands.append("exit")

    def _compare_complex_dict(self, want, have, dkey, dvalue, x):
        wx = get_from_dict(want, x) or []
        hx = get_from_dict(have, x) or []

        wparams = {}
        while len(wx) > 0:
            each = wx.pop()
            if each[dvalue] not in wparams:
                wparams.update({each[dvalue]: set()})
            vlan_list = set(self._str_to_num_list(each[dkey]))
            wparams[each[dvalue]].update(vlan_list)

        hparams = {}
        while len(hx) > 0:
            each = hx.pop()
            if each[dvalue] not in hparams:
                hparams.update({each[dvalue]: set()})
            vlan_list = set(self._str_to_num_list(each[dkey]))
            hparams[each[dvalue]].update(vlan_list)

        wdiff = {}
        for k in wparams.keys():
            if k in hparams:
                wdiff[k] = wparams[k] - hparams[k]
            else:
                wdiff[k] = wparams[k]

        hdiff = {}
        for k in hparams.keys():
            if k in wparams:
                hdiff[k] = hparams[k] - wparams[k]
            else:
                hdiff[k] = hparams[k]

        for k in wdiff.keys():
            if len(wdiff[k]) == 0:
                wparams.pop(k)
            else:
                wparams[k] = self._num_list_to_str(sorted(list(wdiff[k])))

        for k in hdiff.keys():
            if len(hdiff[k]) == 0:
                hparams.pop(k)
            else:
                hparams[k] = self._num_list_to_str(sorted(list(hdiff[k])))

        if wparams != hparams:
            for k, v in iteritems(wparams):
                wx += [{dkey: v, dvalue: k}]

            for k, v in iteritems(hparams):
                hx += [{dkey: v, dvalue: k}]

        if self.state in ["replaced", "deleted"] and hx:
            self.addcmd(have, x, negate=True)
        if wx:
            self.addcmd(want, x)

    def _dict_copy_merged(self, want, have, x=""):
        hrec = {}
        have_dict = have if x == "" else get_from_dict(have, x)
        want_dict = want if x == "" else get_from_dict(want, x)
        for k, wx in iteritems(want_dict):
            if k not in have_dict:
                hrec.update({k: wx})

        for k, hx in iteritems(have_dict):
            dstr = k if x == "" else x + "." + k
            wx = get_from_dict(want, dstr)
            if wx is None:
                hrec.update({k: hx})
                continue
            if isinstance(wx, dict):
                hrec.update({k: self._dict_copy_merged(want, have, dstr)})
            else:
                if dstr in self.mst_parsers:
                    wmode = get_from_dict(want, "mode")
                    hmode = get_from_dict(have, "mode")
                    if not ((wmode is None and hmode == "mst") or wmode == "mst"):
                        self._module.fail_json(
                            msg="mst options like simulate_pvst_global, hello_time, forward_time, "
                            "max_age, max_hops and priority cannot be used until [spanning-tree "
                            "mode mst] is enabled or already configured in device!",
                        )
                        continue
                if not isinstance(wx, list):
                    hrec.update({k: wx if wx is not None else hx})
                else:
                    cmp_list = []
                    if dstr in self.complex_parsers:
                        cmp_list = self._compare_lists("vlan_list", "value", wx, hx)
                    elif dstr == "mst.priority":
                        cmp_list = self._compare_lists("instance", "value", wx, hx)
                    elif dstr == "mst.configuration.instances":
                        cmp_list = self._compare_lists("vlan_list", "instance", wx, hx)
                    if cmp_list:
                        hrec.update({k: cmp_list})
        return hrec

    def _dict_copy_deleted(self, want, have, x=""):
        hrec = {}
        have_dict = have if x == "" else get_from_dict(have, x)
        for k, hx in iteritems(have_dict):
            if not want:
                hrec.update({k: hx})
                continue
            dstr = k if x == "" else x + "." + k
            wx = get_from_dict(want, dstr)
            if wx is None:
                continue
            if dstr == "mst.configuration" and wx == hx:
                hrec.update({k: {}})
                continue
            if isinstance(wx, dict):
                hrec.update({k: self._dict_copy_deleted(want, have, dstr)})
            else:
                if dstr in self.mst_parsers:
                    wmode = get_from_dict(want, "mode")
                    if wmode == "mst":
                        continue
                if not isinstance(wx, list):
                    if wx == hx:
                        hrec.update({k: hx})
                else:
                    cmp_list = []
                    if dstr in self.complex_parsers:
                        cmp_list = self._compare_lists("vlan_list", "value", wx, hx)
                    elif dstr == "mst.priority":
                        cmp_list = self._compare_lists("instance", "value", wx, hx)
                    elif dstr == "mst.configuration.instances":
                        cmp_list = self._compare_lists("vlan_list", "instance", wx, hx)
                    if cmp_list:
                        hrec.update({k: cmp_list})
        return hrec

    def _compare_lists(self, dkey, dvalue, want, have):
        num_list = []

        wparams = {}
        for each in want:
            if each[dvalue] not in wparams:
                wparams.update({each[dvalue]: set()})
            num_set = set(self._str_to_num_list(each[dkey]))
            wparams[each[dvalue]].update(num_set)

        hparams = {}
        for each in have:
            if each[dvalue] not in hparams:
                hparams.update({each[dvalue]: set()})
            num_set = set(self._str_to_num_list(each[dkey]))
            hparams[each[dvalue]].update(num_set)

        if self.state == "merged":
            for k in set(wparams.keys()).union(set(hparams.keys())):
                if k in wparams and k in hparams:
                    diff_list = sorted(list(wparams[k].union(hparams[k])))
                elif k in wparams:
                    diff_list = sorted(list(wparams[k]))
                elif k in hparams:
                    diff_list = sorted(list(hparams[k]))
                num_list += [{dkey: self._num_list_to_str(diff_list), dvalue: k}]
        elif self.state == "deleted":
            for k in wparams.keys():
                if k in hparams:
                    diff_list = sorted(list(wparams[k].intersection(hparams[k])))
                    if diff_list:
                        num_list += [{dkey: self._num_list_to_str(diff_list), dvalue: k}]

        return num_list

    def _str_to_num_list(self, num_str):
        num_list = []
        for each in num_str.split(","):
            block = each.split("-")
            if len(block) > 1:
                num_list += list(range(int(block[0]), int(block[1]) + 1))
            else:
                num_list.append(int(block[0]))
        return sorted(num_list)

    def _num_list_to_str(self, num_list):
        seq = []
        out_list = []
        last = 0
        for index, val in enumerate(num_list):
            if last + 1 == val or index == 0:
                seq.append(val)
                last = val
            else:
                if len(seq) > 1:
                    out_list.append(str(seq[0]) + "-" + str(seq[len(seq) - 1]))
                else:
                    out_list.append(str(seq[0]))
                seq = []
                seq.append(val)
                last = val
            if index == len(num_list) - 1:
                if len(seq) > 1:
                    out_list.append(str(seq[0]) + "-" + str(seq[len(seq) - 1]))
                else:
                    out_list.append(str(seq[0]))
        return ",".join(map(str, out_list))
