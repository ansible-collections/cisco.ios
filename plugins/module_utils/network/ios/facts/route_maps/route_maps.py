# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios route_maps fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.route_maps import (
    Route_mapsTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.route_maps.route_maps import (
    Route_mapsArgs,
)
import q
class Route_mapsFacts(object):
    """ The cisco.ios route_maps facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Route_mapsArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_route_maps_data(self, connection):
        return connection.get("sh running-config | section ^route-map")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Route_maps network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_route_maps_data(connection)
        # parse native config using the Route_maps template
        route_maps_parser = Route_mapsTemplate(lines=data.splitlines())
        objs = route_maps_parser.parse()
        #objs = list(route_maps_parser.parse().values())
        final_objs = []
        for k, v in iteritems(objs):
            temp_dict = {}
            temp_dict['entries'] = []
            for key, val in iteritems(v):
                if key == 'route_map':
                    temp_dict.update({'route_map': val})
                    continue
                if val.get('entries'):
                    if val['entries'].get('match'):
                        if val['entries']['match'].get('local_preference'):
                            local_preference_val = [each for each in val['entries']['match']['local_preference']['value'] if each]
                            if local_preference_val:
                                if isinstance(local_preference_val[0], str):
                                    val['entries']['match']['local_preference']['value'] = [each for each in
                                                                                            local_preference_val[0].split(' ')]
                                else:
                                    val['entries']['match']['local_preference']['value'] = local_preference_val
                            else:
                                val['entries']['match']['local_preference']['value'] = local_preference_val
                        if val['entries']['match'].get('policy_list'):
                            val['entries']['match']['policy_list'] = val['entries']['match']['policy_list'].split(' ')
                        if val['entries']['match'].get('security_group'):
                            if val['entries']['match']['security_group'].get('source'):
                                source = [each for each in val['entries']['match']['security_group']['source'] if each]
                                if source:
                                    if isinstance(source[0], str):
                                        val['entries']['match']['security_group']['source'] = [int(each) for each in source[0].split(' ')]
                                    else:
                                        val['entries']['match']['security_group']['source'] = source
                                else:
                                    val['entries']['match']['security_group']['source'] = source
                            if val['entries']['match']['security_group'].get('destination'):
                                destination = [each for each in val['entries']['match']['security_group']['destination'] if each]
                                if destination:
                                    if isinstance(destination[0], str):
                                        val['entries']['match']['security_group']['destination'] = [int(each) for each in destination[0].split(' ')]
                                    else:
                                        val['entries']['match']['security_group']['destination'] = destination
                                else:
                                    val['entries']['match']['security_group']['destination'] = destination
                        if val['entries']['match'].get('as_path'):
                            val['entries']['match']['as_path']['acl'] = val['entries']['match']['as_path']['acl'].split(' ')
                        if val['entries']['match'].get('ip'):
                            for k_ip, v_ip in iteritems(val['entries']['match']['ip']):
                                v_ip['acl'] = [each for each in v_ip['acl'] if each]
                                v_ip['prefix_list'] = [each for each in v_ip['prefix_list'] if each]
                                if v_ip['acl']:
                                    if 'src-pfx' in v_ip['acl'][0]:
                                        v_ip['acl'][0] = v_ip['acl'][0].split('src-pfx ')[1]
                                    elif 'dest-pfx' in v_ip['acl'][0]:
                                        v_ip['acl'][0] = v_ip['acl'][0].split('dest-pfx ')[1]
                                    v_ip['acl'] = v_ip['acl'][0].split(' ')
                                if v_ip['prefix_list']:
                                    v_ip['prefix_list'] = v_ip['prefix_list'][0].split(' ')
                    temp_dict['entries'].append(val['entries'])
            final_objs.append(temp_dict)

        ansible_facts['ansible_network_resources'].pop('route_maps', None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": final_objs})
        )

        facts['route_maps'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
