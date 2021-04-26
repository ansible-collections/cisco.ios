#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_logging_global config file.
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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.logging_global import (
    Logging_globalTemplate,
)


class Logging_global(ResourceModule):
    """
    The ios_logging_global config class
    """

    def __init__(self, module):
        super(Logging_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="logging_global",
            tmplt=Logging_globalTemplate(),
        )
        self.parsers = [
            "host",
            "host.transport",
            "buffered",
            "buginf",
            "cns_events",
            "console",
            "count",
            "delimiter",
            "discriminator",
            "dmvpn",
            "esm",
            "exception",
            "facility",
            "filter",
            "history",
            "message_counter",
            "monitor",
            "logging_on",
            "origin_id",
            "persistent",
            "policy_firewall",
            "queue_limit",
            "rate_limit",
            "reload",
            "server_arp",
            "snmp_trap",
            "source_interface",
            "trap",
            "userinfo",
        ] #segrigate for O(1) operation

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
        if self.want:
            wantd = self.list_to_dict(self.want)
        else:
            wantd = dict()
        if self.have:
            haved = self.list_to_dict(self.have)
        else:
            haved = dict()

        # wantd = {entry['name']: entry for entry in self.want}
        # haved = {entry['name']: entry for entry in self.have}

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

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Logging_global network resource.
        """

        self.compare(parsers=self.parsers, want=want, have=have)

    # def list_to_dict(self, param):
    #     _temp_param = {"logging": {}}
    #     for element in param:
    #         if element.get("message_counter"):
    #             _temp = {}
    #             for idx, ctr in enumerate(element.get("message_counter"), start=1):
    #                 _temp.update({ctr: idx})
    #             element["message_counter"] = _temp
    #         if element.get("source_interface"):
    #             _temp = {}
    #             for interface in element.get("source_interface"):
    #                 _temp.update({interface.get("interface"): interface})
    #             element["source_interface"] = _temp
    #         if element.get("persistent"):
    #             _temp = {}
    #             for pers in element.get("persistent"):
    #                 _temp.update(pers)
    #             element["persistent"] = _temp
    #         if element.get("filter"):
    #             _temp = {}
    #             for url in element.get("filter"):
    #                 _temp.update({url.get("url"): url})
    #             element["filter"] = _temp
    #         if element.get("host"):
    #             _temp = {}
    #             for host in element.get("host"):
    #                 _temp.update({host.get("hostname"): host})
    #             element["host"] = _temp
        
    #     for element in param:
    #         _temp_param["logging"].update(element)
    #     param = _temp_param

    #     return param

    def list_to_dict(self, param):
        _temp_param = {"logging": {}}
        exculde = []
        for element in param:
            if element.get("message_counter"):
                _temp = {}
                for ctr in element.get("message_counter"):
                    _temp.update({ctr: { "message_counter": ctr }})
                _temp_param.update(_temp)
                exculde.append("message_counter")
            if element.get("source_interface"):
                _temp = {}
                for interface in element.get("source_interface"):
                    _temp.update({interface.get("interface"):{ "source_interface": interface }})
                _temp_param.update(_temp)
                exculde.append("source_interface")
            if element.get("filter"):
                _temp = {}
                for url in element.get("filter"):
                    _temp.update({url.get("url"):{ "filter":url }})
                _temp_param.update(_temp)
                exculde.append("filter")
            if element.get("host"):
                _temp = {}
                for host in element.get("host"):
                    _temp.update({host.get("hostname"):{ "host": host }})    
                _temp_param.update(_temp)
                exculde.append("host")
        else:
            for element in param:
                for k, v in iteritems(element):
                    if k not in exculde:
                        _temp_param["logging"].update({k:v})
        
        param = _temp_param
        return param

                    

