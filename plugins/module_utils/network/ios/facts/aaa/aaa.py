# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios aaa fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.aaa.aaa import (
    AaaArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.aaa import (
    AaaTemplate,
)


def split_methods(text):
    """ "group ISE local" -> ["group ISE", "local"], the name of a group belongs to the method."""
    words = (text or "").split()
    methods = []
    i = 0
    while i < len(words):
        if words[i] in ("group", "cache") and i + 1 < len(words):
            methods.append("%s %s" % (words[i], words[i + 1]))
            i += 2
        else:
            methods.append(words[i])
            i += 1
    return methods


class AaaFacts(object):
    """The ios aaa facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = AaaArgs.argument_spec

    def get_aaa_data(self, connection):
        return connection.get("show running-config all | section ^aaa|^no aaa new-model")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Aaa network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_aaa_data(connection)

        aaa_parser = AaaTemplate(lines=data.splitlines(), module=self._module)
        objs = self._to_lists(aaa_parser.parse())

        ansible_facts["ansible_network_resources"].pop("aaa", None)

        params = utils.remove_empties(
            aaa_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["aaa"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _to_lists(parsed):
        """The parser keeps what is named by name (the order of the configuration is kept), the argspec has lists."""
        for section in ("authentication", "authorization", "accounting"):
            for kind, entries in list(parsed.get(section, {}).items()):
                if isinstance(entries, dict):
                    lists = []
                    for entry in entries.values():
                        entry["methods"] = split_methods(entry.get("methods"))
                        lists.append(entry)
                    parsed[section][kind] = lists

        groups = []
        for group in parsed.get("group_servers", {}).values():
            if not group.get("type") or not group.get("name"):
                # the children of a group type that is not managed, e.g. ldap
                continue
            group["servers"] = [s["name"] for s in group.get("servers", {}).values()]
            groups.append(group)
        if groups:
            parsed["group_servers"] = groups

        clients = []
        for client in parsed.get("dynamic_author", {}).get("clients", {}).values():
            key = client.pop("key_value", None)
            key_type = client.pop("key_type", None)
            if key:
                client["server_key"] = {"type": int(key_type or 0), "key": key}
            clients.append(client)
        if clients:
            parsed["dynamic_author"] = {"clients": clients}
        return parsed
