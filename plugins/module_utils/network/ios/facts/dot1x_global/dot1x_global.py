# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios dot1x_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.dot1x_global.dot1x_global import (
    Dot1x_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.dot1x_global import (
    Dot1x_globalTemplate,
)


class Dot1x_globalFacts(object):
    """The ios dot1x_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Dot1x_globalArgs.argument_spec

    def get_dot1x_global_data(self, connection):
        # "all" prints the defaults, so a value that is off is told from one that is on
        return connection.get("show running-config all | include ^dot1x|^authentication")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Dot1x_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_dot1x_global_data(connection)

        dot1x_global_parser = Dot1x_globalTemplate(lines=data.splitlines(), module=self._module)
        objs = dot1x_global_parser.parse()

        ansible_facts["ansible_network_resources"].pop("dot1x_global", None)

        params = utils.remove_empties(
            dot1x_global_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["dot1x_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
