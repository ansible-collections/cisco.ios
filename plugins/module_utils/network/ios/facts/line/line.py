# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios line fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.line.line import (
    LineArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.line import (
    LineTemplate,
)


class LineFacts(object):
    """The ios line facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = LineArgs.argument_spec

    def get_line_data(self, connection):
        return connection.get("show running-config | sec ^line")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Line network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []
        params = {}

        if not data:
            data = self.get_line_data(connection)

        # parse native config using the Line template
        line_parser = LineTemplate(lines=data.splitlines(), module=self._module)
        objs = line_parser.parse()
        objs["lines"] = list(objs["lines"].values())

        for obj in objs["lines"]:
            if "authorization" in obj and "commands" in obj["authorization"]:
                obj["authorization"]["commands"] = list(obj["authorization"]["commands"].values())
            elif "accounting" in obj and "commands" in obj["accounting"]:
                obj["accounting"]["commands"] = list(obj["accounting"]["commands"].values())

        ansible_facts["ansible_network_resources"].pop("line", None)
        params = utils.remove_empties(
            line_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["line"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
