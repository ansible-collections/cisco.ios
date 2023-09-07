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

import re

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
        _get_snmp_data = connection.get("show running-config | section ^snmp")
        return _get_snmp_data

    def get_snmpv3_user_data(self, connection):
        """get snmpv3 user data from the device

        :param connection: the device connection

        :rtype: string
        :returns: snmpv3 user data

        Note: The seperate method is needed because the snmpv3 user data is not returned within the snmp-server config
        """
        try:
            _get_snmpv3_user = connection.get("show snmp user")
        except Exception as e:
            if "agent not enabled" in str(e):
                return ""
            raise Exception("Unable to get snmp user data: %s" % str(e))
        return _get_snmpv3_user

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
        """Parse the snmpv3_user data and return a list of users
        example data-
        User name: TESTU25
        Engine ID: 000000090200000000000A0B
        storage-type: nonvolatile        active access-list: 22
        Authentication Protocol: MD5
        Privacy Protocol: None
        Group-name: TESTG
        :param snmpv3_user: the snmpv3_user data which is a string

        :rtype: list
        :returns: list of users
        """
        user_sets = snmpv3_user.split("User ")
        user_list = []
        re_snmp_auth = re.compile(r"^Authentication Protocol:\s*(MD5|SHA)")
        re_snmp_priv = re.compile(r"^Privacy Protocol:\s*(3DES|AES|DES)([0-9]*)")
        re_snmp_acl = re.compile(r"^.*active\s+(access-list: (\S+)|)\s*(IPv6 access-list: (\S+)|)")
        for user_set in user_sets:
            one_set = {}
            lines = user_set.splitlines()
            for line in lines:
                if line.startswith("name"):
                    one_set["username"] = line.split(": ")[1]
                    continue
                if line.startswith("Group-name:"):
                    one_set["group"] = line.split(": ")[1]
                    continue
                re_match = re_snmp_auth.search(line)
                if re_match:
                    one_set["authentication"] = {"algorithm": re_match.group(1).lower()}
                    continue
                re_match = re_snmp_priv.search(line)
                if re_match:
                    one_set["encryption"] = {"priv": re_match.group(1).lower()}
                    if re_match.group(2):
                        one_set["encryption"]["priv_option"] = re_match.group(2)
                    continue
                re_match = re_snmp_acl.search(line)
                if re_match:
                    if re_match.group(2):
                        one_set["acl_v4"] = re_match.group(2)
                    if re_match.group(4):
                        one_set["acl_v6"] = re_match.group(4)
                    continue
                one_set["version"] = "v3"  # defaults to version 3 data
            if len(one_set):
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
        snmpv3_user = ""

        if not data:
            data = self.get_snmp_data(connection)
            snmpv3_user = self.get_snmpv3_user_data(connection)  # gathers v3 user data

        # parse native config using the Snmp_server template
        snmp_server_parser = Snmp_serverTemplate(lines=data.splitlines(), module=self._module)
        # parse snmpv3_user data using the get_snmpv3_user_facts method
        snmp_user_data = self.get_snmpv3_user_facts(snmpv3_user)
        objs = snmp_server_parser.parse()

        # add snmpv3_user data to the objs dictionary
        if snmp_user_data:
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
