# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios prefix_lists fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.prefix_lists.prefix_lists import (
    Prefix_listsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.prefix_lists import (
    Prefix_listsTemplate,
)


class Prefix_listsFacts(object):
    """The cisco.ios prefix_lists facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Prefix_listsArgs.argument_spec

    def get_prefix_list_data(self, connection):
        return connection.get("show running-config | section ^ip prefix-list|^ipv6 prefix-list")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Prefix_lists network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_prefix_list_data(connection)

        # parse native config using the Prefix_lists template
        prefix_lists_parser = Prefix_listsTemplate(lines=data.splitlines())
        objs = prefix_lists_parser.parse()

        final_objs = []

        _prefix_list = {"ipv4": [], "ipv6": []}
        if objs:
            for prefixes in list(objs.values()):
                _afi = prefixes.pop("afi")
                _prefix_list[_afi].append(
                    prefixes,
                )
            if _prefix_list.get("ipv4"):
                final_objs.append({"afi": "ipv4", "prefix_lists": _prefix_list.pop("ipv4")})
            if _prefix_list.get("ipv6"):
                final_objs.append({"afi": "ipv6", "prefix_lists": _prefix_list.pop("ipv6")})

            ansible_facts["ansible_network_resources"].pop("prefix_lists", None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": final_objs}),
        )

        facts["prefix_lists"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
