#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_ntp_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ntp_global import (
    Ntp_globalTemplate,
)


class Ntp_global(ResourceModule):
    """
    The ios_ntp_global config class
    """

    def __init__(self, module):
        super(Ntp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ntp_global",
            tmplt=Ntp_globalTemplate(),
        )
        self.parsers = [
            "allow.control.rate_limit",
            "allow.private",
            "authenticate",
            "broadcast_delay",
            "clock_period",
            "logging",
            "master.enabled",
            "master.stratum",
            "max_associations",
            "max_distance",
            "min_distance",
            "orphan",
            "panic_update",
            "passive",
            "source",
            "update_calendar",
        ]
        self.complex_parser = [
            "peer",
            "query_only",
            "serve",
            "serve_only",
            "authentication_keys",
            "peers",
            "servers",
            "trusted_keys",
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
        wantd = self._ntp_list_to_dict(self.want)
        haved = self._ntp_list_to_dict(self.have)

        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            wantd = {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ntp_global network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_access_groups(want, have)
        self._compare_lists_attrs(want, have)

    def _compare_lists_attrs(self, want, have):
        """Compare list of dict"""
        for _parser in self.complex_parser[4:8]:  # other list attrs
            i_want = want.get(_parser, {})
            i_have = have.get(_parser, {})
            for key, wanting in iteritems(i_want):
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    if (
                        _parser != "authentication_keys"
                        and haveing
                        and self.state in ["overridden", "replaced"]
                    ):
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser)
            for key, haveing in iteritems(i_have):
                self.addcmd(haveing, _parser, negate=True)

    def _compare_access_groups(self, want, have):
        w = want.get("access_group", {})
        h = have.get("access_group", {})
        for _parser in self.complex_parser[0:4]:  # access_group
            i_want = w.get(_parser, {})
            i_have = h.get(_parser, {})

            for key, wanting in iteritems(i_want):
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    self.addcmd(wanting, _parser)

            for key, haveing in iteritems(i_have):
                self.addcmd(haveing, _parser, negate=True)

    def _ntp_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "servers": "server",
            "peers": "peer",
            "authentication_keys": "id",
            "peer": "access_list",
            "query_only": "access_list",
            "serve": "access_list",
            "serve_only": "access_list",
            "trusted_keys": "range_start",
            "access_group": True,
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data and k != "access_group":
                tmp_data[k] = {str(i[p_key[k]]): i for i in tmp_data[k]}
            elif tmp_data.get("access_group") and k == "access_group":
                tmp_data[k] = self._ntp_list_to_dict(
                    tmp_data.get("access_group")
                )
        return tmp_data
