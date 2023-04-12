#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_static_routes config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.static_routes import (
    Static_routesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    validate_n_expand_ipv4,
)


class Static_routes(ResourceModule):
    """
    The ios_static_routes config class
    """

    def __init__(self, module):
        super(Static_routes, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="static_routes",
            tmplt=Static_routesTemplate(),
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
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd, delete_spcl = self.list_to_dict(self.want, "want")
        haved, n_req = self.list_to_dict(self.have, "have")

        if delete_spcl and haved and self.state == "deleted":
            for pk, to_rem in delete_spcl.items():
                if pk in ["ipv4", "ipv6"]:
                    _afis = haved.get("_afis_")
                    for k, v in _afis.get(pk, {}).items():
                        for each_dest in to_rem:
                            if k.split("_")[0] == each_dest:
                                self.addcmd({pk: v}, pk, True)
                else:
                    _vrfs = haved.get(pk)
                    for ak, v in _vrfs.items():
                        for k, srts in v.items():
                            for each_dest in to_rem.get(ak):
                                if k.split("_")[0] == each_dest:
                                    self.addcmd({ak: srts}, ak, True)

        else:
            # if state is merged, merge want onto have and then compare
            if self.state == "merged":
                wantd = dict_merge(haved, wantd)

            for k, want in iteritems(wantd):
                self._compare_top_level_keys(want=want, have=haved.pop(k, {}))

            # if self.state in ["overridden", "deleted"]:
            if (self.state == "deleted" and not wantd) or self.state == "overridden":
                for k, have in iteritems(haved):
                    self._compare_top_level_keys(want={}, have=have)

    def _compare_top_level_keys(self, want, have):
        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted" and have:
            _have = {}
            for addf in ["ipv4", "ipv6"]:
                _temp_sr = {}
                for k, ha in iteritems(have.get(addf, {})):
                    if k in want.get(addf, {}):  # or not want.get(addf)
                        _temp_sr[k] = ha
                    if _temp_sr:
                        _have[addf] = _temp_sr
            if _have:
                have = _have
                want = {}

        if self.state != "deleted":
            for _afi, routes in want.items():
                self._compare(s_want=routes, s_have=have.pop(_afi, {}), afi=_afi)

        if self.state in ["overridden", "deleted"]:
            for _afi, routes in have.items():
                self._compare(s_want={}, s_have=routes, afi=_afi)

    def _compare(self, s_want, s_have, afi):
        for name, w_srs in s_want.items():
            have_srs = s_have.pop(name, {})
            self.compare(parsers=afi, want={afi: w_srs}, have={afi: have_srs})

        # remove remaining items in have for replaced state
        for name, h_srs in s_have.items():
            self.compare(parsers=afi, want={}, have={afi: h_srs})

    def list_to_dict(self, param, operation):
        _static_rts = {}
        _delete_spc = {}
        if param:
            for srs in param:
                _vrf = srs.get("vrf")
                _srts = {}
                for adfs in srs.get("address_families", []):
                    _afi = adfs.get("afi")
                    _routes = {}
                    for rts in adfs.get("routes", []):
                        _dest = rts.get("dest", "")
                        _sdest = rts.get("dest", "")
                        _topo = rts.get("topology", "")
                        #  below if specific to special deletes
                        if (
                            self.state == "deleted"
                            and operation == "want"
                            and not rts.get("next_hops")
                        ):
                            if _vrf:
                                if not _delete_spc.get(_vrf):
                                    _delete_spc[_vrf] = {}
                                if not _delete_spc[_vrf].get(_afi):
                                    _delete_spc[_vrf][_afi] = []
                                _delete_spc[_vrf][_afi].append(_dest)
                            else:
                                if not _delete_spc.get(_afi):
                                    _delete_spc[_afi] = []
                                _delete_spc[_afi].append(_dest)

                        for nxh in rts.get("next_hops", []):
                            _forw_rtr_add = nxh.get("forward_router_address", "").upper()
                            _intf = nxh.get("interface", "")
                            _key = _sdest + "_" + _topo + _forw_rtr_add + _intf

                            if _afi == "ipv4":
                                _dest = validate_n_expand_ipv4(self._module, {"address": _dest})
                            dummy_sr = {
                                "afi": _afi,
                                "dest": _dest,
                            }

                            if _vrf:
                                dummy_sr["vrf"] = _vrf
                            if _topo:
                                dummy_sr["topology"] = _topo
                            if _intf:
                                dummy_sr["interface"] = _intf
                            if _forw_rtr_add:
                                dummy_sr["forward_router_address"] = _forw_rtr_add
                            dummy_sr.update(nxh)

                            _routes[_key] = dummy_sr
                    _srts[_afi] = _routes
                _static_rts[_vrf if _vrf else "_afis_"] = _srts
        return _static_rts, _delete_spc
