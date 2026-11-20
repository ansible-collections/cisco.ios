# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios track fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ipaddress import ip_network

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.track_objects.track_objects import (
    Track_objectsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.track_objects import (
    Track_objectsTemplate,
)


class Track_objectsFacts(object):
    """The ios track facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Track_objectsArgs.argument_spec

    def get_track_objects_data(self, connection):
        return connection.get("show running-config | section ^track")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Track_objects network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_track_objects_data(connection)

        track_parser = Track_objectsTemplate(lines=data.splitlines(), module=self._module)
        parsed = track_parser.parse()

        unsupported = sorted(k for k, v in parsed.items() if v.get("unsupported"))
        if unsupported:
            self._module.warn(
                "tracked object(s) %s use a type that ios_track_objects does not manage and are ignored."
                % ", ".join(str(k) for k in unsupported),
            )
        objs = [self._clean(parsed[k]) for k in sorted(parsed, key=int) if k not in unsupported]

        ansible_facts["ansible_network_resources"].pop("track", None)

        params = utils.remove_empties(
            track_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["track_objects"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _clean(obj):
        """Turn "address mask" of a tracked route into address/length."""
        route = obj.get("ip_route")
        if route:
            mask = route.pop("mask", None)
            if mask:
                route["prefix"] = str(
                    ip_network("{0}/{1}".format(route["prefix"], mask), strict=False),
                )
        return obj
