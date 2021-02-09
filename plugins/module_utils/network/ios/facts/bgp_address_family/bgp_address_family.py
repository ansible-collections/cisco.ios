# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios bgp_address_family fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_address_family import (
    Bgp_AddressFamilyTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_address_family.bgp_address_family import (
    Bgp_AddressFamilyArgs,
)

class Bgp_AddressFamilyFacts(object):
    """ The cisco.ios_bgp_address_family facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Bgp_AddressFamilyArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)
    
    def get_bgp_address_family_data(self, connection):
        return connection.get("sh running-config | section ^router bgp")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Bgp_address_family network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_bgp_address_family_data(connection)

        # parse native config using the Bgp_address_family template
        bgp_af_parser = Bgp_AddressFamilyTemplate(lines=data.splitlines())
        objs = bgp_af_parser.parse()
        objs = utils.remove_empties(objs)
        temp_af = []
        for k, v in iteritems(objs['address_family']):
            temp_dict = {}
            temp = [every for every in k.split('_') if every != '']
            temp_dict['afi'] = temp.pop(0)
            if len(temp) > 1:
                temp_dict['vrf'] = [each.split(' ')[1] for each in temp if 'vrf' in each][0]
                temp_dict['af_modifier'] = [each for each in temp if 'vrf' not in each][0]
            elif len(temp) == 1:
                if 'vrf' in temp[0]:
                    temp_dict['vrf'] = temp[0].split('vrf ')[1]
                else:
                    temp_dict['af_modifier'] = temp[0]
            v.update(temp_dict)
            temp_af.append(v)

        objs['address_family'] = temp_af

        ansible_facts['ansible_network_resources'].pop('bgp_address_family', None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": objs})
        )

        facts['bgp_address_family'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
