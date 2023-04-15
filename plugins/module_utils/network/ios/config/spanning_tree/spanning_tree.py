#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_spanning_tree config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
    get_from_dict,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
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
            "spanning_tree.backbonefast",
            "spanning_tree.bridge_assurance",
            "spanning_tree.etherchannel_guard_misconfig",
            "spanning_tree.extend_system_id",
            "spanning_tree.logging",
            "spanning_tree.loopguard_default",
            "spanning_tree.mode",
            "spanning_tree.pathcost_method",
            "spanning_tree.transmit_hold_count",
            "spanning_tree.portfast.network_default",
            "spanning_tree.portfast.edge_default",
            "spanning_tree.portfast.bpdufilter_default",
            "spanning_tree.portfast.bpduguard_default",
            "spanning_tree.uplinkfast.enabled",
            "spanning_tree.uplinkfast.max_update_rate",
            "spanning_tree.mst.simulate_pvst_global",
            "spanning_tree.mst.hello_time",
            "spanning_tree.mst.forward_time",
            "spanning_tree.mst.max_age",
            "spanning_tree.mst.max_hops",
        ]
        self.complex_parsers = [
            "spanning_tree.forward_time",
            "spanning_tree.hello_time",
            "spanning_tree.max_age",
            "spanning_tree.priority",
            "spanning_tree.mst.priority",
        ]
        self.mst_config_parsers = [
            "spanning_tree.mst.configuration",
            "spanning_tree.mst.configuration.name",
            "spanning_tree.mst.configuration.revision",
            "spanning_tree.mst.configuration.instances",
        ]

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
#        self._module.fail_json(
#            msg="VRF {0} has address-family configurations. "
#            "Please use the nxos_bgp_af module to remove those first.".format(name),
#        )
#        raise Exception(self.have)
        wantd = self.want
        haved = self.have

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

#        for k, want in iteritems(wantd):
#            self._compare(want=want, have=haved.pop(k, {}))
        self._compare_linear(want=wantd, have=haved)
        self._compare_complex(want=wantd, have=haved)

    def _compare_linear(self, want, have):
        self.compare(parsers=self.linear_parsers, want=want, have=have)

    def _compare_complex(self, want, have):
        for x in self.complex_parsers:
            wx = get_from_dict(want, x) or []
            hx = get_from_dict(have, x) or []
            if x == "spanning_tree.mst.priority":
                wparams = {}
                for each in wx:
                    if each['value'] not in wparams:
                        wparams.update({each['value']: set([None]) })
                    wparams[each['value']].update(set(each['instance']))
                if len(wparams) != 0:
                    raise Exception(wparams)
