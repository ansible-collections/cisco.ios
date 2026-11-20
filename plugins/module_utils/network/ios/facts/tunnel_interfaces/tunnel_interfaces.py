# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios tunnel_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.tunnel_interfaces.tunnel_interfaces import (
    Tunnel_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.tunnel_interfaces import (
    Tunnel_interfacesTemplate,
)


class Tunnel_interfacesFacts(object):
    """The ios tunnel_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Tunnel_interfacesArgs.argument_spec

    def get_tunnel_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface Tunnel")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Tunnel_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_tunnel_interfaces_data(connection)

        tunnel_parser = Tunnel_interfacesTemplate(lines=data.splitlines(), module=self._module)
        parsed = tunnel_parser.parse()
        unsupported = sorted(
            (n for n, v in parsed.items() if v.get("unsupported")),
            key=self._sort_key,
        )
        if unsupported:
            self._module.warn(
                "tunnel interface(s) %s use a tunnel mode that ios_tunnel_interfaces does not manage and are ignored."
                % ", ".join(unsupported),
            )
        objs = [
            parsed[name] for name in sorted(parsed, key=self._sort_key) if name not in unsupported
        ]

        ansible_facts["ansible_network_resources"].pop("tunnel_interfaces", None)

        params = utils.remove_empties(
            tunnel_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["tunnel_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _sort_key(name):
        digits = "".join(ch for ch in name if ch.isdigit())
        return (int(digits) if digits else 0, name)
