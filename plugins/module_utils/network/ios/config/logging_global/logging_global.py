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

from ansible.module_utils._text import to_text
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
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
            "buffered",
            "buginf",
            "cns_events",
            "console",
            "count",
            "delimiter",
            "dmvpn",
            "esm",
            "exception",
            "facility",
            "history",
            "monitor",
            "logging_on",
            "origin_id",
            "persistent",
            "policy_firewall",
            "queue_limit",
            "rate_limit",
            "reload",
            "server_arp",
            "trap",
            "userinfo",
        ]
        self.list_parsers = ["hosts", "filter", "source_interface"]
        self.complex_parsers = [
            "message_counter",
            "discriminator",
            "snmp_trap",
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

        wantd = self.list_to_dict(self.want)
        haved = self.list_to_dict(self.have)

        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            wantd = {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Logging_global network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_lists_attrs(want, have)
        self._compare_complex_attrs(want, have)

    def _compare_lists_attrs(self, want, have):
        """Compare list of dict"""
        for _par in self.list_parsers:
            i_want = want.get(_par, {})
            i_have = have.get(_par, {})
            for key, wanting in iteritems(i_want):
                _parser = _par
                if wanting.get("transport") and _parser == "hosts":
                    _parser = "hosts.transport"
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser)
            for key, haveing in iteritems(i_have):
                _parser = _par
                if haveing.get("transport") and _parser == "hosts":
                    _parser = "hosts.transport"
                self.addcmd(haveing, _parser, negate=True)

    def _compare_complex_attrs(self, want, have):
        """Compare dict of list"""
        for _par in self.complex_parsers:
            i_want = want.get(_par, {})
            i_have = have.get(_par, {})
            for key, wanting in iteritems(i_want):
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _par, negate=True)
                    self.addcmd(wanting, _par)
            for key, haveing in iteritems(i_have):
                self.addcmd(haveing, _par, negate=True)

    def list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "filter": "url",
            "hosts": "host",
            "source_interface": "interface",
        }
        if data.get("hosts"):  # handle aliased hostname as host
            for v in data.get("hosts"):
                if v.get("hostname"):
                    v["host"] = v.pop("hostname")
        list_el = ["message_counter", "discriminator", "snmp_trap"]
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if tmp_data.get(k):
                tmp_data[k] = {
                    str(i[p_key[k]]) if i.get(p_key[k]) else str(i.get("ipv6")): i
                    for i in tmp_data[k]
                }
        for el in list_el:
            if tmp_data.get(el):
                tmp_data[el] = {self.trim_whitespace(el + i): {el: i} for i in tmp_data[el]}
        return tmp_data

    def trim_whitespace(self, word):
        return to_text(word).strip()
