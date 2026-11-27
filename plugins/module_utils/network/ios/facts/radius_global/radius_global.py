# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios radius_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.radius_global.radius_global import (
    Radius_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.radius_global import (
    Radius_globalTemplate,
)


class Radius_globalFacts(object):
    """The ios radius_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Radius_globalArgs.argument_spec

    def get_radius_global_data(self, connection):
        return connection.get("show running-config | section ^radius|^ip radius source-interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Radius_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_radius_global_data(connection)

        radius_parser = Radius_globalTemplate(lines=data.splitlines(), module=self._module)
        objs = radius_parser.parse()

        # servers and attributes are collected keyed, the argspec wants lists
        servers = objs.pop("servers", {})
        attributes = objs.pop("attributes", {})
        objs["servers"] = [servers[name] for name in sorted(servers)]
        objs["attributes"] = [attributes[number] for number in sorted(attributes, key=int)]

        ansible_facts["ansible_network_resources"].pop("radius_global", None)

        params = utils.remove_empties(
            radius_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["radius_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
