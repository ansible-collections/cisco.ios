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
            if False:
                self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self.list_to_dict(self.want)
        haved = self.list_to_dict(self.have)

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
            self._compare_top_level_keys(want=want, have=haved.pop(k, {}))

    def _compare_top_level_keys(self, want, have):
        for _afi, routes in want.items():
            self._compare(s_want=routes, s_have=have.pop(_afi, {}), afi=_afi)

    def _compare(self, s_want, s_have, afi):
        for name, w_srs in s_want.items():
            have_srs = s_have.pop(name, {})
            self.compare(parsers=afi, want={afi: w_srs}, have={afi: have_srs})

        # remove remaining items in have for replaced state
        for name, h_srs in s_have.items():
            self.compare(parsers=afi, want={}, have={afi: h_srs})

    def list_to_dict(self, param):
        _static_rts = {}
        if param:
            for srs in param:
                _vrf = srs.get("vrf")
                # _add_fam = srs.get("address_families")
                _srts = {}
                for adfs in srs.get("address_families", []):
                    _afi = adfs.get("afi")
                    _routes = {}
                    for rts in adfs.get("routes", []):
                        _dest = rts.get("dest", "")
                        _topo = rts.get("topology", "")
                        for nxh in rts.get("next_hops", []):
                            _forw_rtr_add = nxh.get("forward_router_address", "").upper()
                            _intf = nxh.get("interface", "")
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
                            _key = _dest + _topo + _forw_rtr_add + _intf
                            _routes[_key] = dummy_sr
                    _srts[_afi] = _routes
                _static_rts[_vrf if _vrf else "afis"] = _srts
        return _static_rts
