# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios logging_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.logging_global.logging_global import (
    Logging_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.logging_global import (
    Logging_globalTemplate,
)


class Logging_globalFacts(object):
    """The ios logging_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Logging_globalArgs.argument_spec

    def get_logging_data(self, connection):
        return connection.get("show running-config | include logging")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Logging_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objFinal = []

        if not data:
            data = self.get_logging_data(connection)

        # parse native config using the Logging_global template
        logging_global_parser = Logging_globalTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objFinal = logging_global_parser.parse()

        if objFinal:
            for k, v in iteritems(objFinal):
                if type(v) == list and k not in [
                    "hosts",
                    "source_interface",
                    "filter",
                ]:
                    v.sort()
                    objFinal[k] = v
                elif type(v) == list and k == "hosts":
                    objFinal[k] = sorted(
                        objFinal[k],
                        key=lambda item: item["host"] if item.get("host") else item.get("ipv6"),
                    )
                elif type(v) == list and k == "source_interface":
                    objFinal[k] = sorted(
                        objFinal[k],
                        key=lambda item: item["interface"],
                    )
                elif type(v) == list and k == "filter":
                    objFinal[k] = sorted(
                        objFinal[k],
                        key=lambda item: item["url"],
                    )
        ansible_facts["ansible_network_resources"].pop("logging_global", None)

        params = utils.remove_empties(
            logging_global_parser.validate_config(
                self.argument_spec,
                {"config": objFinal},
                redact=True,
            ),
        )

        facts["logging_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
