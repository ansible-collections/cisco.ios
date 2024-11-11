# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios vrf_interfaces facts class
It is in this file that the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_interfaces.vrf_interfaces import (
    Vrf_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_interfaces import (
    Vrf_interfacesTemplate,
)


class Vrf_interfacesFacts(object):
    """The cisco.ios vrf_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Vrf_interfacesArgs.argument_spec

    def get_vrf_interfaces_data(self, connection):
        """Fetch the configuration data for VRF interfaces.

        :param connection: The device connection object
        :returns: The raw configuration data from the device
        """
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vrf_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected config (optional)

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_vrf_interfaces_data(connection)

        # Parse native config using the Vrf_interfaces template
        vrf_interfaces_parser = Vrf_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )

        objs = list(vrf_interfaces_parser.parse().values())
        # Ensure previous facts are removed to avoid duplication
        ansible_facts["ansible_network_resources"].pop("vrf_interfaces", None)

        params = utils.remove_empties(
            vrf_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        # Update the ansible_facts dictionary with the VRF interface facts
        facts["vrf_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
