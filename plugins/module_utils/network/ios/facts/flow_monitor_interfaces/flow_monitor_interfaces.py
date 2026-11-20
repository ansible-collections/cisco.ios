# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios flow_monitor_interfaces fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.flow_monitor_interfaces.flow_monitor_interfaces import (
    Flow_monitor_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.flow_monitor_interfaces import (
    Flow_monitor_interfacesTemplate,
)


class Flow_monitor_interfacesFacts(object):
    """The ios flow_monitor_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Flow_monitor_interfacesArgs.argument_spec

    def get_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Flow_monitor_interfaces network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_interfaces_data(connection)

        parser = Flow_monitor_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        parsed = parser.parse()

        # Filter to only interfaces that have flow_monitors configured
        objs = [v for v in parsed.values() if v.get("flow_monitors")]

        ansible_facts["ansible_network_resources"].pop("flow_monitor_interfaces", None)

        params = utils.remove_empties(
            parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["flow_monitor_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
