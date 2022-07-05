#
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_lag_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.lag_interfaces import (
    Lag_interfacesTemplate,
)


class Lag_interfaces(ResourceModule):
    """
    The ios_lag_interfaces config class
    """

    def __init__(self, module):
        super(Lag_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="lag_interfaces",
            tmplt=Lag_interfacesTemplate(),
        )

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
                    self._compare(wants={}, haveing=have)

        for k, want in iteritems(wantd):
            self._compare(wants=want, haveing=haved.pop(k, {}))

    def _compare(self, wants, haveing):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Lag_interfaces network resource.
        """

        for key, entry in wants.items():
            begin = len(self.commands)
            if entry != haveing.pop(key, {}):
                self.addcmd(entry, "channel", False)
            if len(self.commands) != begin:
                self.commands.insert(
                    begin,
                    self._tmplt.render(entry, "member", False),
                )

        # remove remaining items in have for replaced
        for entry in haveing.values():
            begin = len(self.commands)
            self.addcmd(entry, "channel", True)
            if len(self.commands) != begin:
                self.commands.insert(
                    begin,
                    self._tmplt.render(entry, "member", False),
                )

    def extract_channel_num(self, channel):
        try:
            return channel.lower().split("port-channel")[1], False
        except IndexError:
            return channel.lower().split("port-channel")[0], True

    def list_to_dict(self, params):
        channels = {}
        for ethChannels in params:
            tmp = {}
            for member in ethChannels.get("members", {}):
                member["channel"] = self.extract_channel_num(
                    ethChannels.get("name"),
                )[0]
                tmp[member.get("member")] = member
            update = self.extract_channel_num(ethChannels.get("name"))[1]
            if update:
                ethChannels["name"] = "Port-channel" + ethChannels.get("name")
            channels[ethChannels.get("name")] = tmp
        return channels
