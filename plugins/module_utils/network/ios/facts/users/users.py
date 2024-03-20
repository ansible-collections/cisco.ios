# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios users fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.users.users import (
    UsersArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.users import (
    UsersTemplate,
)


class UsersFacts(object):
    """The ios users facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = UsersArgs.argument_spec

    def get_users_data(self, connection):
        return connection.get("show running-config | section ^username|^user-name|^enable")

    def sort_list_dicts(self, objs):
        p_key = {
            "enable": "level",
            "users": "name",
        }
        for k, _v in p_key.items():
            if k in objs:
                if k == "enable":
                    objs[k] = sorted(objs[k], key=lambda _k: str(_k.get(_v, 15)))
                else:
                    objs[k] = sorted(objs[k], key=lambda _k: str(_k[_v]))
        return objs

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Users network resource

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
            data = self.get_users_data(connection)

        # parse native config using the Users template
        users_parser = UsersTemplate(lines=data.splitlines(), module=self._module)
        objs = users_parser.parse()

        objs["users"] = list(objs.get("users", {}).values())
        if objs:
            self.sort_list_dicts(objs)

        ansible_facts["ansible_network_resources"].pop("users", None)

        params = utils.remove_empties(
            users_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["users"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
