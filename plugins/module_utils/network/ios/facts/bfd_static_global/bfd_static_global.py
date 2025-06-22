# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios bfd_static_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bfd_static_global.bfd_static_global import (
    Bfd_static_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bfd_static_global import (
    Bfd_static_globalTemplate,
)


class Bfd_static_globalFacts(object):
    """The ios bfd_static_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bfd_static_globalArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bfd_static_global network resource

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

        # parse native config using the Bfd_static_global template
        bfd_static_global_parser = Bfd_static_globalTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = list(bfd_static_global_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("bfd_static_global", None)

        params = utils.remove_empties(
            bfd_static_global_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["bfd_static_global"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
