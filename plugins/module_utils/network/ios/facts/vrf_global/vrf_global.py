# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios vrf_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_global.vrf_global import (
    Vrf_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_global import (
    Vrf_globalTemplate,
)


class Vrf_globalFacts(object):
    """The ios vrf_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Vrf_globalArgs.argument_spec

    def get_config(self, connection):
        """Get the configuration from the device"""
        raw_config = connection.get("show running-config | section ^vrf definition")
        return self._filter_global_config(raw_config)

    def _filter_global_config(self, config_text):
        """
        Filter out address-family specific configuration from VRF config.
        Only return global VRF configuration lines.
        """
        if not config_text:
            return ""

        lines = config_text.splitlines()
        filtered_lines = []
        inside_address_family = False

        for line in lines:
            if re.match(r"\s+address-family\s+", line):
                inside_address_family = True
                continue

            if re.match(r"\s+exit-address-family", line):
                inside_address_family = False
                continue

            if not inside_address_family:
                filtered_lines.append(line)

        return "\n".join(filtered_lines)

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vrf_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """

        facts = {}
        objs = []

        if not data:
            data = self.get_config(connection)

        vrf_global_parser = Vrf_globalTemplate(lines=data.splitlines(), module=self._module)
        objs = vrf_global_parser.parse()

        objs["vrfs"] = list(objs["vrfs"].values()) if "vrfs" in objs else []

        ansible_facts["ansible_network_resources"].pop("vrf_global", None)
        params = utils.remove_empties(
            vrf_global_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["vrf_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
