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
            "hosts",
            "hosts.transport",
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
        ]

        self.exclude = {"want": [], "have": []}

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
            wantd = self.list_to_dict(self.want, "want")
        else:
            wantd = dict()
        if self.have:
            haved = self.list_to_dict(self.have, "have")
        else:
            haved = dict()

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

        # replaced state for handling list type attrs
        if self.state == "replaced":
            for k, have in iteritems(haved):
                if list(have.keys())[0] in self.exclude["want"]:
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

    def list_to_dict(self, param, op):
        """Converts a dict that contains list to a dict of dict
            The linear structure of the logging configuration
            converts every logging configuration to dict with unique key

        Args:
            param (dict): The have or want

        Returns:
            dict: for any defined configuration dict contains unique keys
        """

        _temp_param = {}
        for element, val in iteritems(param):
            if element == "message_counter":
                _temp = {}
                for ctr in val:
                    _temp.update({ctr: {"message_counter": ctr}})
                _temp_param.update(_temp)
                self.exclude[op].append("message_counter")
            if element == "discriminator":
                _temp = {}
                for ctr in val:
                    _temp.update(
                        {
                            self.trim_whitespace("discriminator_" + ctr): {
                                "discriminator": ctr
                            }
                        }
                    )
                _temp_param.update(_temp)
                self.exclude[op].append("discriminator")
            if element == "snmp_trap":
                _temp = {}
                for ctr in val:
                    _temp.update(
                        {
                            self.trim_whitespace("snmp_trap_" + ctr): {
                                "snmp_trap": ctr
                            }
                        }
                    )
                _temp_param.update(_temp)
                self.exclude[op].append("snmp_trap")
            if element == "source_interface":
                _temp = {}
                for interface in val:
                    _temp.update(
                        {
                            interface.get("interface"): {
                                "source_interface": interface
                            }
                        }
                    )
                _temp_param.update(_temp)
                self.exclude[op].append("source_interface")
            if element == "filter":
                _temp = {}
                for url in val:
                    _temp.update({url.get("url"): {"filter": url}})
                _temp_param.update(_temp)
                self.exclude[op].append("filter")
            if element == "hosts":
                _temp = {}
                for host in val:
                    if host.get("hostname"):
                        _temp.update({host.get("hostname"): {"hosts": host}})
                    elif host.get("ipv6"):
                        _temp.update({host.get("ipv6"): {"hosts": host}})
                _temp_param.update(_temp)
                self.exclude[op].append("hosts")

        for k, v in iteritems(param):
            if k not in self.exclude.get(op):
                _temp_param.update({k: {k: v}})

        param = _temp_param
        return param

    def trim_whitespace(self, word):
        return word.strip()
