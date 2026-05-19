#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_vrf_address_family config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_address_family import (
    Vrf_address_familyTemplate,
)


class Vrf_address_family(ResourceModule):
    """
    The ios_vrf_address_family config class
    """

    def __init__(self, module):
        super(Vrf_address_family, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vrf_address_family",
            tmplt=Vrf_address_familyTemplate(),
        )
        self.parsers = [
            "address_family",
            "bgp.next_hop.loopback",
            "export.map",
            "import_config.map",
            "export.ipv4.multicast",
            "export.ipv4.unicast.allow_evpn",
            "import_config.ipv4.multicast",
            "import_config.ipv4.unicast",
            "inter_as_hybrid.csc.next_hop",
            "inter_as_hybrid.next_hop",
            "mdt.auto_discovery.ingress_replication.inter_as.mdt_hello_enable",
            "mdt.auto_discovery.pim.inter_as.mdt_hello_enable",
            "mdt.auto_discovery.pim.inter_as.pim_tlv_announce.mdt_hello_enable",
            "mdt.auto_discovery.ingress_replication.mdt_hello_enable",
            "mdt.auto_discovery.pim.mdt_hello_enable",
            "mdt.auto_discovery.pim.pim_tlv_announce.mdt_hello_enable",
            "mdt.auto_discovery.receiver_site",
            "mdt.data.ingress_replication.number",
            "mdt.data.ingress_replication.immediate_switch",
            "mdt.data.ingress_replication.number.immediate_switch",
            "mdt.data.list.access_list",
            "mdt.data.list.access_list_name",
            "mdt.data.threshold",
            "mdt.default_ingress_replication",
            "mdt.direct",
            "mdt.log_reuse",
            "mdt.mode.gre",
            "mdt.mtu.value",
            "mdt.overlay.bgp.shared_tree_prune_delay",
            "mdt.overlay.bgp.source_tree_prune_delay",
            "mdt.overlay.use_bgp_spt_only",
            "mdt.partitioned.ingress_replication",
            "mdt.strict_rpf_interface",
            "protection.local_prefixes",
            "route_replicate.recursion_policy.destination",
            "route_replicate.from.unicast.all.route_map",
            "route_replicate.from.unicast.bgp.asn.route_map",
            "route_replicate.from.unicast.connected.route_map",
            "route_replicate.from.unicast.eigrp.asn.route_map",
            "route_replicate.from.unicast.isis.route_map",
            "route_replicate.from.unicast.mobile.route_map",
            "route_replicate.from.unicast.odr.route_map",
            "route_replicate.from.unicast.ospf.id.route_map",
            "route_replicate.from.unicast.rip.route_map",
            "route_replicate.from.unicast.static.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.all.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.bgp.asn.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.connected.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.eigrp.asn.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.isis.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.mobile.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.odr.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.ospf.id.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.rip.route_map",
            "route_replicate.from.vrf.vrf_name.unicast.static.route_map",
            "route_target.exports",
            "route_target.imports",
            "mdt.auto_discovery.mldp",
            "mdt.data.mpls.mldp",
            "mdt.partitioned.mldp.p2mp",
            "mdt.overlay.use_bgp",
            "mdt.strict_rpf.interface",
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

        wantd = self._handle_deprecates(want=wantd)

        wantd = self._vrf_list_to_dict(wantd)
        haved = self._vrf_list_to_dict(haved)

        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            for vrfk, vrfv in haved.items():
                for afk, afv in vrfv.get("address_families", {}).items():
                    adrf = wantd.get(vrfk, {}).get("address_families", {})
                    if afk in adrf or not adrf:
                        self.commands.append(f"vrf definition {vrfk}")

                        self.addcmd(
                            {"afi": afv.get("afi"), "safi": afv.get("safi")},
                            "address_family",
                            True,
                        )

        if self.state in ["overridden"]:
            for vrfk, vrfv in haved.items():
                for k, have in vrfv.get("address_families", {}).items():
                    wantx = wantd.get(vrfk, {}).get("address_families", {})
                    if k not in wantx:
                        self.commands.append(f"vrf definition {vrfk}")

                        self.addcmd(
                            {"afi": have.get("afi"), "safi": have.get("safi")},
                            "address_family",
                            False,
                        )
                        self.compare(parsers=self.parsers, want={}, have=have)

        if self.state != "deleted":
            self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vrf network resource.
        """
        for name, entry in want.items():
            begin = len(self.commands)
            vrf_want = entry
            vrf_have = have.pop(name, {})
            self._compare_afs(vrf_want, vrf_have)
            if len(self.commands) != begin:
                self.commands.insert(begin, "vrf definition {0}".format(name))

    def _compare_afs(self, want, have):
        """Custom handling of afs option
        :params want: the want VRF dictionary
        :params have: the have VRF dictionary
        """
        waafs = want.get("address_families", {})
        haafs = have.get("address_families", {})
        for afk, afv in waafs.items():
            begin = len(self.commands)
            self._compare_single_af(want=afv, have=haafs.get(afk, {}))
            if len(self.commands) != begin:
                af_cmd = f"address-family {afv.get('afi')}"
                if afv.get("safi"):
                    af_cmd += f" {afv.get('safi')}"
                self.commands.insert(begin, af_cmd)

    def _compare_single_af(self, want, have):
        """Custom handling of single af option
        :params want: the want VRF dictionary
        :params have: the have VRF dictionary
        """
        if "route_target" in want:
            self._compare_route_targets(want, have)
        self.compare(parsers=self.parsers[1:], want=want, have=have)

    def _vrf_list_to_dict(self, entry):
        """Convert list of items to dict of items
           for efficient diff calculation.
        :params entry: data dictionary
        """

        for vrf in entry:
            if "address_families" in vrf:
                vrf["address_families"] = {
                    (x["afi"], x.get("safi")): x for x in vrf["address_families"]
                }

        entry = {x["name"]: x for x in entry}
        return entry

    def _compare_route_targets(self, want, have):
        """Custom handling for route targets lists for all states
        :params want: the want address family dictionary
        :params have: the have address family dictionary
        """
        want_rt = want.get("route_target", {})
        have_rt = have.get("route_target", {})

        want_exports = want_rt.get("exports", [])
        have_exports = have_rt.get("exports", [])

        if self.state in ["merged", "replaced", "overridden"]:
            for export_rt in want_exports:
                if export_rt not in have_exports:
                    rt_cmd = f"route-target export {export_rt['rt_value']}"
                    if export_rt.get("stitching"):
                        rt_cmd += " stitching"
                    self.commands.append(rt_cmd)

        if self.state in ["replaced", "overridden", "deleted"]:
            for export_rt in have_exports:
                if self.state == "deleted" or export_rt not in want_exports:
                    rt_cmd = f"no route-target export {export_rt['rt_value']}"
                    if export_rt.get("stitching"):
                        rt_cmd += " stitching"
                    self.commands.append(rt_cmd)

        want_imports = want_rt.get("imports", [])
        have_imports = have_rt.get("imports", [])

        if self.state in ["merged", "replaced", "overridden"]:
            for import_rt in want_imports:
                if import_rt not in have_imports:
                    rt_cmd = f"route-target import {import_rt['rt_value']}"
                    if import_rt.get("stitching"):
                        rt_cmd += " stitching"
                    self.commands.append(rt_cmd)

        if self.state in ["replaced", "overridden", "deleted"]:
            for import_rt in have_imports:
                if self.state == "deleted" or import_rt not in want_imports:
                    rt_cmd = f"no route-target import {import_rt['rt_value']}"
                    if import_rt.get("stitching"):
                        rt_cmd += " stitching"
                    self.commands.append(rt_cmd)

    def _handle_deprecates(self, want):
        if not isinstance(want, list):
            return want
        for vrf_config in want:
            if "address_families" in vrf_config:
                for af in vrf_config["address_families"]:
                    if "route_target" in af:
                        rt = af["route_target"]
                        if ("exports" in rt and isinstance(rt["exports"], list)) or (
                            "imports" in rt and isinstance(rt["imports"], list)
                        ):
                            continue
                        new_rt = {}
                        if "export" in rt:
                            export_value = rt["export"]
                            new_rt["exports"] = [{"rt_value": export_value, "stiching": False}]
                        if "import_config" in rt:
                            import_value = rt["import_config"]
                            new_rt["imports"] = [{"rt_value": import_value, "stiching": False}]
                        if new_rt:
                            af["route_target"] = new_rt
        return want
