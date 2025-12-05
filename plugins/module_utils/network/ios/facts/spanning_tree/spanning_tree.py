# -*- coding: utf-8 -*-
# Copyright 2023 Timur Nizharadze (@tnizharadze)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios spanning_tree fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.spanning_tree.spanning_tree import (
    Spanning_treeArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.spanning_tree import (
    Spanning_treeTemplate,
)


class Spanning_treeFacts(object):
    """The ios spanning_tree facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Spanning_treeArgs.argument_spec

        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_spanning_tree_data(self, connection):
        return connection.get("show running-config | section ^spanning-tree|^no spanning-tree")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Spanning_tree network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []
        if not data:
            data = self.get_spanning_tree_data(connection)

        # parse native config using the Spanning_tree template
        spanning_tree_parser = Spanning_treeTemplate(lines=data.splitlines(), module=self._module)
        objs = spanning_tree_parser.parse()

        ansible_facts["ansible_network_resources"].pop("spanning_tree", None)

        params = utils.remove_empties(
            spanning_tree_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["spanning_tree"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
