# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios bfd_templates fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_templates.bfd_templates import (
    Bfd_templatesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_templates import (
    Bfd_templatesTemplate,
)


class Bfd_templatesFacts(object):
    """The ios bfd_templates facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bfd_templatesArgs.argument_spec

    def get_bfd_templates_data(self, connection):
        return connection.get("show running-config | section ^bfd-template")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bfd_templates network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_bfd_templates_data(connection)

        # parse native config using the Bfd_templates template
        bfd_templates_parser = Bfd_templatesTemplate(lines=data.splitlines(), module=self._module)
        objs = list(bfd_templates_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("bfd_templates", None)

        params = utils.remove_empties(
            bfd_templates_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["bfd_templates"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
