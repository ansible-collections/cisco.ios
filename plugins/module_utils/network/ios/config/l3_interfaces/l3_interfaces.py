#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_l3_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
#     ConfigBase,
# )
# from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
#     to_list,
#     remove_empties,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
#     Facts,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
#     dict_to_set,
#     normalize_interface,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
#     remove_command_from_config_list,
#     add_command_to_config_list,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
#     filter_dict_having_none_value,
#     remove_duplicate_interface,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
#     validate_n_expand_ipv4,
#     validate_ipv6,
# )
from ansible.module_utils.six import iteritems
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l3_interfaces import (
    L3_InterfacesTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
import q


class L3_Interfaces(ResourceModule):
    """
    The ios_l3_interfaces class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["l3_interfaces"]

    def __init__(self, module):
        super(L3_Interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l3_interfaces",
            tmplt=L3_InterfacesTemplate(),
        )

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        self.gen_config()
        self.run_commands()
        return self.result
    
    def push_sec_ip_to_zero_index(self, temp_dict):
        temp = []
        for index in range(len(temp_dict['ipv4'])):
            if 'secondary' in temp_dict['ipv4'][index]:
                temp.insert(0, temp_dict['ipv4'][index])
            else:
                temp.append(temp_dict['ipv4'][index])
        temp_dict['ipv4'] = temp
        return temp_dict

    def gen_config(self):
        """ Select the appropriate function based on the state provided

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        if self.want:
            wantd = {
                (entry["name"]): entry
                for entry in self.want
            }
            #wantd = {self.want[0].get("name"): self.want[0]}
        else:
            wantd = {}
        if self.have:
            haved = {
                (entry["name"]): entry
                for entry in self.have
            }
        else:
            haved = {}
        # if state is merged, merge want onto have
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)
        # if state is deleted, limit the have to anything in want
        # set want to nothing
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}
        # delete processes first so we do run into "more than one" errors
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self.addcmd(have, "pid", True)
        q(wantd, haved)
        for k, want in iteritems(wantd):
            have = haved.pop(k, {})
            if 'ipv6' in want:
                for each in want['ipv6']:
                    each['address'] = each['address'].upper()
            if 'ipv4' in want:
                if have:
                    have = self.push_sec_ip_to_zero_index(have)
                want = self.push_sec_ip_to_zero_index(want)
            self._compare(want=want, have=have)
        #q(self.commands)

    def _compare(self, want, have):
        parsers = [
            "ipv4",
            "ipv4_dhcp",
            "ipv6",
        ]

        if want != have:
            self.addcmd(want or have, "name", False)
            self.compare(parsers, want, have)
