#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_user_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.user_global import (
    User_globalTemplate,
)


class User_global(ResourceModule):
    """
    The ios_user_global config class
    """

    def __init__(self, module):
        super(User_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="user_global",
            tmplt=User_globalTemplate(),
        )
        self.parsers = []
        self.list_parsers = [
            "enable",
            "users",
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
        wantd = self._users_list_to_dict(self.want)
        haved = self._users_list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            wantd = {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the User_global network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_lists_attrs(want, have)

    def _compare_lists_attrs(self, want, have):
        """Compare list of dict"""
        for _parser in self.list_parsers:
            i_want = want.get(_parser, {})
            i_have = have.get(_parser, {})
            for key, wanting in iteritems(i_want):
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser)
            for key, haveing in iteritems(i_have):
                self.addcmd(haveing, _parser, negate=True)

    def _users_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "enable": "level",
            "users": "name",
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data:
                if k == "enable":
                    tmp_data[k] = {str(i.get(_v, 15)): i for i in tmp_data[k]}
                else:
                    tmp_data[k] = {str(i[_v]): i for i in tmp_data[k]}
        return tmp_data
