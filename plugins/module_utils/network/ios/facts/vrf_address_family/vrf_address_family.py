# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios vrf_address_family fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_address_family.vrf_address_family import (
    Vrf_address_familyArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_address_family import (
    Vrf_address_familyTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    flatten_config,
)


class Vrf_address_familyFacts(object):
    """The ios vrf_address_family facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Vrf_address_familyArgs.argument_spec

    def get_config(self, connection):
        """Get the configuration from the device"""

        return connection.get("show running-config | section ^vrf")

    def _flatten_config(self, config):
        dataLines = config.split("\n")
        finalConfig = []

        for line in dataLines:
            if "address-family" in line and "exit-address-family" not in line:
                finalConfig.append(line)

        return "\n".join(finalConfig)

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vrf_address_family network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []
        obj = {}

        if not data:
            data = self.get_config(connection)

        address_data = flatten_config(data, "address-family")
        data = flatten_config(address_data, "vrf")
        finalConfig = self._flatten_config(data)

        # parse native config using the Vrf_address_family template
        vrf_address_family_parser = Vrf_address_familyTemplate(
            lines=finalConfig.splitlines(),
            module=self._module,
        )
        obj = vrf_address_family_parser.parse()
        objs = list(obj.values())

        for vrf in objs:
            af = vrf.get("address_families", {})
            if af:
                self._post_parse(vrf)
            else:
                vrf["address_families"] = []

        ansible_facts["ansible_network_resources"].pop("vrf_address_family", None)

        params = utils.remove_empties(
            vrf_address_family_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["vrf_address_family"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _post_parse(self, af_data):
        """Converts the intermediate data structure
            to valid format as per argspec.
        :param obj: dict
        """
        af = af_data.get("address_families", {})
        if af:
            af_data["address_families"] = list(af.values())
