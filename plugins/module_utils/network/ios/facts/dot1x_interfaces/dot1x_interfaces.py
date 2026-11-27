# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios dot1x_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.dot1x_interfaces.dot1x_interfaces import (
    Dot1x_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.dot1x_interfaces import (
    Dot1x_interfacesTemplate,
)


class Dot1x_interfacesFacts(object):
    """The ios dot1x_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Dot1x_interfacesArgs.argument_spec

    def get_dot1x_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Dot1x_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_dot1x_interfaces_data(connection)

        objs = []
        # An access switch has more than a thousand interfaces. The parser merges every line into the
        # result it has so far, which is quadratic for one big result: parse the interfaces one by one.
        for block in self._interface_blocks(data):
            parsed = Dot1x_interfacesTemplate(lines=block, module=self._module).parse()
            for entry in parsed.values():
                # an interface without 802.1X or MAB options is not part of this resource
                if len(entry) > 1:
                    objs.append(entry)

        ansible_facts["ansible_network_resources"].pop("dot1x_interfaces", None)

        params = utils.remove_empties(
            Dot1x_interfacesTemplate(module=self._module).validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["dot1x_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _interface_blocks(data):
        """The lines of the configuration, one list per interface."""
        block = []
        for line in data.splitlines():
            if line.startswith("interface "):
                if block:
                    yield block
                block = [line]
            elif block and line[:1] in (" ", "\t"):
                block.append(line)
            elif block:
                # whatever is not indented ends the interface
                yield block
                block = []
        if block:
            yield block
