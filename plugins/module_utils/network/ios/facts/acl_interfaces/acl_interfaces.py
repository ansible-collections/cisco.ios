#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acl_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acl_interfaces.acl_interfaces import (
    Acl_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acl_interfaces import (
    Acl_interfacesTemplate,
)


class Acl_interfacesFacts(object):
    """The ios_acl_interfaces fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Acl_interfacesArgs.argument_spec

    def get_acl_interfaces_data(self, connection):
        return connection.get(
            "show running-config | include ^interface|ip access-group|ipv6 traffic-filter",
        )

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for interfaces
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_acl_interfaces_data(connection)

        config_parser = Acl_interfacesTemplate(lines=data.splitlines())
        entry = sorted(list(config_parser.parse().values()), key=lambda k, sk="name": k[sk])
        if entry:
            for item in entry:
                item["access_groups"] = sorted(
                    list(item["access_groups"].values()),
                    key=lambda k, sk="afi": k[sk],
                )

        ansible_facts["ansible_network_resources"].pop("acl_interfaces", None)
        facts = {"acl_interfaces": []}
        for cfg in entry:
            utils.remove_empties(cfg)
            if cfg.get("access_groups"):
                facts["acl_interfaces"].append(cfg)
        utils.validate_config(self.argument_spec, {"config": facts.get("acl_interfaces")})

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
