#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_l3_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from copy import deepcopy
import re
# from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
#     utils,
# )
# from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
#     get_interface_type,
#     normalize_interface,
# )


from copy import deepcopy
from netaddr import IPAddress
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l3_interfaces.l3_interfaces import (
    L3_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l3_interfaces import (
    L3_InterfacesTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)
import q

class L3_InterfacesFacts(object):
    """ The ios l3 interfaces fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = L3_InterfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_l3_interfaces_data(self, connection):
        return connection.get("sh running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for l3 interfaces
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_l3_interfaces_data(connection)

        ipv4 = {"processes": []}
        rmmod = NetworkTemplate(
            lines=data.splitlines(), tmplt=L3_InterfacesTemplate()
        )
        current = rmmod.parse()

        ipv4 = []
        ipv6 = []
        config_list = []
        for key, value in iteritems(current.get('interface')):
            temp = []
            if "ipv4" in value:
                for each in value['ipv4']:
                    if each['address'] != 'dhcp':
                        cidr_bits = IPAddress(each['mask']).netmask_bits()
                        ipv4_cidr = "{0}/{1}".format(each['address'], cidr_bits)
                        each['address'] = ipv4_cidr
                        del each['mask']
                    ipv4.append(each)
            if "ipv6" in value:
                ipv6.extend(value['ipv6'])
            if ipv4:
                temp.append({"ipv4": ipv4})
                ipv4 = []
            if ipv6:
                if len(temp) == 0:
                    temp.append({"ipv6": ipv6})
                else:
                    temp[0].update({"ipv6": ipv6})
                ipv6 = []
            if temp:
                temp[0].update({"name": value["name"]})
                config_list.extend(temp)

        ansible_facts["ansible_network_resources"].pop("l3_interfaces", None)
        facts = {}
        if current:
            params = utils.validate_config(
                self.argument_spec, {"config": config_list}
            )
            params = utils.remove_empties(params)

            facts["l3_interfaces"] = params["config"]

            ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
