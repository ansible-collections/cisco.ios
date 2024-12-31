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

from ansible.module_utils.six import iteritems
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
            "route_target.export",
            "route_target.import_config",
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

        wantd = self._vrf_list_to_dict(wantd)
        haved = self._vrf_list_to_dict(haved)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            for vrfk, vrfv in iteritems(haved):
                for afk, afv in iteritems(vrfv.get("address_families", {})):
                    adrf = wantd.get(vrfk, {}).get("address_families", {})
                    if afk in adrf or not adrf:
                        self.addcmd(
                            {"name": vrfk},
                            "name",
                            False,
                        )
                        self.addcmd(
                            {"afi": afv.get("afi"), "safi": afv.get("safi")},
                            "address_family",
                            True,
                        )

        if self.state in ["overridden"]:
            for vrfk, vrfv in iteritems(haved):
                for k, have in iteritems(vrfv.get("address_families", {})):
                    wantx = wantd.get(vrfk, {}).get("address_families", {})
                    if k not in wantx:
                        self.addcmd(
                            {"name": vrfk},
                            "name",
                            False,
                        )
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
        for name, entry in iteritems(want):
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
        for afk, afv in iteritems(waafs):
            begin = len(self.commands)
            self._compare_single_af(want=afv, have=haafs.get(afk, {}))
            if len(self.commands) != begin:
                self.commands.insert(begin, f"address-family {afv.get('afi')} {afv.get('safi')}")

    def _compare_single_af(self, want, have):
        """Custom handling of single af option
        :params want: the want VRF dictionary
        :params have: the have VRF dictionary
        """
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
