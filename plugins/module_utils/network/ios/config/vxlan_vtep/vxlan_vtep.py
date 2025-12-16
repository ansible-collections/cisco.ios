#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_vxlan_vtep config file.
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
    param_list_to_dict,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vxlan_vtep import (
    Vxlan_vtepTemplate,
)


class Vxlan_vtep(ResourceModule):
    """
    The ios_vxlan_vtep config class
    """

    def __init__(self, module):
        super(Vxlan_vtep, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vxlan_vtep",
            tmplt=Vxlan_vtepTemplate(),
        )
        self.parsers = [
            "source_interface",
            "host_reachability_bgp",
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

        wantd, haved = self._interface_list_to_dict(self.want, self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd_copy = wantd.copy()
            wantd = {}

        # remove superfluous config for deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    have = self._filtered_dict(wantd_copy.get(k), have)
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vxlan_vtep network resource.
        """

        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)

        self._compare_member_vnis(
            want.pop("member", {}).get("vni", {}),
            have.pop("member", {}).get("vni", {}),
        )

        if len(self.commands) != begin:
            self.commands.insert(
                begin,
                self._tmplt.render(want or have, "interface", False),
            )

    def _compare_member_vnis(self, wantmv, havemv):
        """Compare member VNIs dict"""

        PARSER_DICT = {
            "l2vni": "replication",
            "l3vni": "vrf",
        }

        for vni_type in ["l2vni", "l3vni"]:
            wantd = wantmv.get(vni_type, {})
            haved = havemv.get(vni_type, {})
            undel_vnis = haved.copy()

            for wvni, want in wantd.items():
                have = haved.pop(wvni, {})
                if want != have:
                    # remove exiting config of the member VNI
                    self.addcmd(undel_vnis.pop(wvni, {}), PARSER_DICT[vni_type], True)
                    if vni_type == "l3vni":
                        undel_vnis = self._remove_existing_vnis_vrfs(want["vrf"], undel_vnis)
                    self.addcmd(want, PARSER_DICT[vni_type])

            # remove remaining configs in have for replaced state
            for hvni, have in haved.items():
                if hvni in undel_vnis:
                    self.addcmd(have, PARSER_DICT[vni_type], True)

    def _interface_list_to_dict(self, want, have):
        """Convert all list of dicts to dicts of dicts"""

        wantd = {entry["interface"]: entry for entry in want}
        haved = {entry["interface"]: entry for entry in have}

        for each in wantd, haved:
            if each:
                for nvi, nvid in each.items():
                    member_vni = nvid.get("member", {}).get("vni")
                    if member_vni:
                        for vni_type in member_vni:
                            member_vni[vni_type] = param_list_to_dict(
                                member_vni[vni_type],
                                unique_key="vni",
                                remove_key=False,
                            )

        return wantd, haved

    def _remove_existing_vnis_vrfs(self, want_vrf, haved):
        """Remove member VNIs of corresponding VRF"""

        vrf_haved = next(
            (h for h in haved.values() if h["vrf"] == want_vrf),
            None,
        )
        if vrf_haved:
            self.addcmd(haved.pop(vrf_haved["vni"]), "vrf", True)
        return haved

    def _filtered_dict(self, want, have):
        """Remove other config from 'have' if 'member' key is present"""

        if "member" in want:
            have_member = {}
            want_vni_dict = want.get("member", {}).get("vni", {})
            have_vni_dict = have.get("member", {}).get("vni", {})

            for vni_type, have_vnis in have_vni_dict.items():
                want_vnis = want_vni_dict.get(vni_type, {})
                have_member[vni_type] = {
                    vni: have_vni_dict[vni_type].get(vni) for vni in have_vnis if vni in want_vnis
                }
            have = {
                "interface": have["interface"],
                "member": {"vni": have_member},
            }

        return have
