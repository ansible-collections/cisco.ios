# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios hsrp_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from collections import defaultdict

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.hsrp_interfaces import (
    Hsrp_interfacesTemplate,
)


class Hsrp_interfacesFacts(object):
    """The ios hsrp_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Hsrp_interfacesArgs.argument_spec

    def get_hsrp_data(self, connection):
        return connection.get("sh running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Hsrp_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_hsrp_data(connection)

        # parse native config using the Hsrp_interfaces template
        hsrp_interfaces_parser = Hsrp_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = list(hsrp_interfaces_parser.parse().values())

        def combine_by_group_no(data):
            combined = defaultdict(dict)
            ipv6_addresses = []
            for entry in data:
                if entry.get("process_ipv6", {}):
                    ipv6_addresses.append(entry.pop("address"))
                    del entry
                    continue
                group_no = entry.get("group_no")
                if group_no is not None:
                    combined[group_no].update(entry)
            if ipv6_addresses:
                combined[group_no]["ipv6"]["addresses"] = ipv6_addresses
            # Default to priority to 100 if not specified, idempotent behavior
            if not combined[group_no].get("priority"):
                combined[group_no]["priority"] = 100
            return list(combined.values())

        if objs:
            for obj in objs:
                if obj.get("standby_groups"):
                    if not obj.get("version"):
                        # Default to version 1 if not specified, idempotent behavior
                        obj["version"] = 1
                    standby_groups_data = obj.get("standby_groups")
                    combined_data = combine_by_group_no(standby_groups_data)

                    obj["standby_groups"] = combined_data

        ansible_facts["ansible_network_resources"].pop("hsrp_interfaces", None)

        params = utils.remove_empties(
            hsrp_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["hsrp_interfaces"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
