# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios bfd_static fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_static.bfd_static import (
    Bfd_staticArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_static import (
    Bfd_staticTemplate,
)


class Bfd_staticFacts(object):
    """The ios bfd_static facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bfd_staticArgs.argument_spec

    def get_bfd_static_data(self, connection):
        """Get the 'show running-config | include ip route static bfd' from the device"""
        return connection.get("show running-config | include ip route static bfd")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bfd_static network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_bfd_static_data(connection)

        # parse native config using the Bfd_static template
        bfd_static_parser = Bfd_staticTemplate(lines=data.splitlines(), module=self._module)
        parsed_objs = bfd_static_parser.parse()

        # Transform parsed data to flat list format for facts
        objs = self._transform_parsed_data(parsed_objs)

        ansible_facts["ansible_network_resources"].pop("bfd_static", None)

        params = utils.remove_empties(
            bfd_static_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["bfd_static"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _transform_parsed_data(self, parsed_data):
        """Transform the nested parsed data to flat list format matching argspec"""
        transformed_routes = []

        if not parsed_data:
            return transformed_routes

        for parsed_dict in parsed_data.values():
            bfd_static_routes = parsed_dict.get("bfd_static_routes", {})

            # Process VRF routes with next hop
            for route in bfd_static_routes.get("vrf_routes", []):
                transformed_route = {
                    "destination": route.get("destination"),
                    "vrf": route.get("vrf_name"),
                    "next_hop": route.get("next_hop"),
                }
                if route.get("group_name"):
                    transformed_route["group_name"] = route["group_name"]
                if route.get("passive"):
                    transformed_route["passive"] = route["passive"]
                if route.get("log"):
                    transformed_route["log"] = route["log"]
                if route.get("unassociate"):
                    transformed_route["unassociate"] = route["unassociate"]

                transformed_routes.append(transformed_route)

            # Process VRF routes with source VRF and IP
            for route in bfd_static_routes.get("vrf_src_routes", []):
                transformed_route = {
                    "destination": route.get("destination"),
                    "vrf": route.get("vrf_name"),
                    "source_vrf": route.get("src_vrf"),
                    "source_ip": route.get("src_ip"),
                }
                if route.get("group_name"):
                    transformed_route["group_name"] = route["group_name"]
                if route.get("passive"):
                    transformed_route["passive"] = route["passive"]
                if route.get("log"):
                    transformed_route["log"] = route["log"]
                if route.get("unassociate"):
                    transformed_route["unassociate"] = route["unassociate"]

                transformed_routes.append(transformed_route)

            # Process interface routes
            for route in bfd_static_routes.get("interface_routes", []):
                transformed_route = {
                    "destination": route.get("destination"),
                    "interface": route.get("interface"),
                }
                if route.get("group_name"):
                    transformed_route["group_name"] = route["group_name"]
                if route.get("passive"):
                    transformed_route["passive"] = route["passive"]
                if route.get("log"):
                    transformed_route["log"] = route["log"]
                if route.get("unassociate"):
                    transformed_route["unassociate"] = route["unassociate"]

                transformed_routes.append(transformed_route)

        return transformed_routes
