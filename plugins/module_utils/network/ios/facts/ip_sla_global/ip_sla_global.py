# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios ip_sla_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ip_sla_global.ip_sla_global import (
    Ip_sla_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ip_sla_global import (
    Ip_sla_globalTemplate,
)


class Ip_sla_globalFacts(object):
    """The ios ip_sla_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ip_sla_globalArgs.argument_spec

    def get_ip_sla_global_data(self, connection):
        return connection.get("show running-config | section ^ip sla")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Ip_sla_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_ip_sla_global_data(connection)

        ip_sla_parser = Ip_sla_globalTemplate(lines=data.splitlines(), module=self._module)
        objs = ip_sla_parser.parse()

        # operations are collected keyed by id, the argspec wants a list
        operations = objs.pop("operations", {})
        unsupported = sorted(k for k, v in operations.items() if v.get("unsupported"))
        if unsupported:
            self._module.warn(
                "ip sla operation(s) %s use an operation type that ios_ip_sla_global does not manage "
                "and are ignored." % ", ".join(str(k) for k in unsupported),
            )
        objs["operations"] = [
            operations[k] for k in sorted(operations, key=int) if k not in unsupported
        ]

        ansible_facts["ansible_network_resources"].pop("ip_sla_global", None)

        params = utils.remove_empties(
            ip_sla_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["ip_sla_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
