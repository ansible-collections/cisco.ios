# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios bgp_af fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.ansible.cisco.ios.plugins.module_utils.network.cisco.ios.rm_templates.bgp_af import (
    Bgp_afTemplate,
)
from ansible_collections.ansible.cisco.ios.plugins.module_utils.network.cisco.ios.argspec.bgp_af.bgp_af import (
    Bgp_afArgs,
)

class Bgp_afFacts(object):
    """ The cisco.ios bgp_af facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Bgp_afArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Bgp_af network resource

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

        # parse native config using the Bgp_af template
        bgp_af_parser = Bgp_afTemplate(lines=data.splitlines())
        objs = list(bgp_af_parser.parse().values())

        ansible_facts['ansible_network_resources'].pop('bgp_af', None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": objs})
        )

        facts['bgp_af'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
