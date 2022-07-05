# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios lag_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from itertools import groupby

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.lag_interfaces.lag_interfaces import (
    Lag_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.lag_interfaces import (
    Lag_interfacesTemplate,
)


class Lag_interfacesFacts(object):
    """The ios lag_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Lag_interfacesArgs.argument_spec

    def get_lag_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Lag_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_lag_interfaces_data(connection)

        # parse native config using the Lag_interfaces template
        lag_interfaces_parser = Lag_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = self.process_facts(list(lag_interfaces_parser.parse().values()))
        ansible_facts["ansible_network_resources"].pop("lag_interfaces", None)

        params = utils.remove_empties(
            lag_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["lag_interfaces"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def process_facts(self, all_objs):
        lag_facts = []
        objs = []
        temp_channels = []

        def key_channel(k):
            return k.get("channel")

        for intrf in all_objs:
            if intrf.get("channel"):
                if intrf.get("channel") in temp_channels:
                    temp_channels.remove(intrf.get("channel"))
                objs.append(intrf)
            if "Port-channel" in intrf.get("member"):
                temp_channels.append(intrf.get("member"))

        objs = sorted(objs, key=key_channel)

        for empty_channel in temp_channels:
            objs.append({"channel": empty_channel})

        for key, value in groupby(objs, key_channel):
            if key:
                _v = list(value)
                for v in _v:
                    v.pop("channel")
                lag_facts.append({"name": key, "members": _v})

        return lag_facts
