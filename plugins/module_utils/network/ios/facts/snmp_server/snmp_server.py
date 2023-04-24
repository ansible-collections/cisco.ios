# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios snmp_server fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.snmp_server.snmp_server import (
    Snmp_serverArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.snmp_server import (
    Snmp_serverTemplate,
)


class Snmp_serverFacts(object):
    """The ios snmp_server facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Snmp_serverArgs.argument_spec

    def get_snmp_data(self, connection):
        _get_snmp_data = connection.get("show running-config | section ^snmp-server")
        _get_snmpv3_user = connection.get("show snmp user")
        return _get_snmp_data, _get_snmpv3_user

    def sort_list_dicts(self, objs):
        p_key = {
            "hosts": "host",
            "groups": "group",
            "engine_id": "id",
            "communities": "name",
            "password_policy": "policy_name",
            "users": "username",
            "views": "name",
        }
        for k, _v in p_key.items():
            if k in objs:
                objs[k] = sorted(objs[k], key=lambda _k: str(_k[p_key[k]]))
        return objs

    def host_traps_string_to_list(self, hosts):
        if hosts:
            for element in hosts:
                if element.get("traps", {}):
                    element["traps"] = list(element.get("traps").split())
            return hosts
    
    def get_snmpv3_user_facts(self, snmpv3_user):
        user_sets = snmpv3_user.split("User ")
        user_list = []
        for user_set in user_sets:
            one_set = {}
            lines = user_set.splitlines()
            for line in lines:
                if line.startswith("name"):
                    one_set["username"] = line.split(': ')[1]
                if line.startswith("Group-name:"):
                    one_set["group"] = line.split(': ')[1]
                if "IPv6 access-list:" in line:
                    one_set["acl_v6"] = line.split(': ')[-1]
                if "active access-list:" in line:
                    one_set["acl_v4"] = line.split(': ')[-1]
            if len(one_set) != 0:
                user_list.append(one_set)
        return user_list


    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Snmp_server network resource

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
            data, snmpv3_user = self.get_snmp_data(connection)

        # parse native config using the Snmp_server template
        snmp_server_parser = Snmp_serverTemplate(lines=data.splitlines(), module=self._module)
        snmp_user_data = self.get_snmpv3_user_facts(snmpv3_user)
        objs = snmp_server_parser.parse()
        
        if len(snmp_user_data) != 0:
            if objs.get("users") is None:
                objs["users"] = snmp_user_data
            else:
                objs["users"] = objs["users"] + snmp_user_data
        if objs:
            self.host_traps_string_to_list(objs.get("hosts"))
            self.sort_list_dicts(objs)

        ansible_facts["ansible_network_resources"].pop("snmp_server", None)

        params = utils.remove_empties(
            snmp_server_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["snmp_server"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
