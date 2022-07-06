# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios ntp_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ntp_global.ntp_global import (
    Ntp_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ntp_global import (
    Ntp_globalTemplate,
)


class Ntp_globalFacts(object):
    """The ios ntp_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ntp_globalArgs.argument_spec

    def sort_dicts(self, objs):
        p_key = {
            "servers": "server",
            "peers": "peer",
            "authentication_keys": "id",
            "peer": "access_list",
            "query_only": "access_list",
            "serve": "access_list",
            "serve_only": "access_list",
            "trusted_keys": "range_start",
            "access_group": True,
        }
        for k, _v in p_key.items():
            if k in objs and k != "access_group":
                objs[k] = sorted(objs[k], key=lambda _k: str(_k[p_key[k]]))
            elif objs.get("access_group") and k == "access_group":
                objs[k] = self.sort_dicts(objs.get("access_group"))
        return objs

    def get_ntp_data(self, connection):
        return connection.get("show running-config | section ^ntp")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Ntp_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_ntp_data(connection)

        # parse native config using the Ntp_global template
        ntp_global_parser = Ntp_globalTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = ntp_global_parser.parse()

        if objs:
            objs = self.sort_dicts(objs)

        ansible_facts["ansible_network_resources"].pop("ntp_global", None)

        params = utils.remove_empties(
            ntp_global_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["ntp_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
