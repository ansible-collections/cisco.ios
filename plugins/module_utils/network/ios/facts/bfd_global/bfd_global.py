# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios bfd_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.argspec.bfd_global.bfd_global import (
    Bfd_globalArgs,
)
from ansible_collections.cisco.ios.ios.plugins.module_utils.network.ios.rm_templates.bfd_global import (
    Bfd_globalTemplate,
)


class Bfd_globalFacts(object):
    """The ios bfd_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bfd_globalArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bfd_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get()

        # parse native config using the Bfd_global template
        bfd_global_parser = Bfd_globalTemplate(lines=data.splitlines(), module=self._module)
        objs = list(bfd_global_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("bfd_global", None)

        params = utils.remove_empties(
            bfd_global_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["bfd_global"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
