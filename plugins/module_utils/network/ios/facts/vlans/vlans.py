#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios vlans fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlans.vlans import (
    VlansArgs,
)


class VlansFacts(object):
    """The ios vlans fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = VlansArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_vlans_data(self, connection):
        """Checks device is L2/L3 and returns
        facts gracefully. Does not fail module.
        """
        check_os_type = connection.get_device_info()
        if check_os_type.get("network_os_type") == "L3":
            return ""
        return connection.get("show vlan")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for vlans
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        objs = []
        mtu_objs = []
        remote_objs = []
        final_objs = []
        if not data:
            data = self.get_vlans_data(connection)
        # operate on a collection of resource x
        config = data.split("\n")
        # Get individual vlan configs separately
        vlan_info = ""
        temp = ""
        vlan_name = True
        for conf in config:
            if len(list(filter(None, conf.split(" ")))) <= 2 and vlan_name:
                temp = temp + conf
                if len(list(filter(None, temp.split(" ")))) <= 2:
                    continue
            if "VLAN Name" in conf:
                vlan_info = "Name"
            elif "VLAN Type" in conf:
                vlan_info = "Type"
                vlan_name = False
            elif "Remote SPAN" in conf:
                vlan_info = "Remote"
                vlan_name = False
            elif "VLAN AREHops" in conf or "STEHops" in conf:
                vlan_info = "Hops"
                vlan_name = False
            elif "Primary Secondary" in conf:
                vlan_info = "Primary"
                vlan_name = False
            if temp:
                conf = temp
                temp = ""
            if conf and " " not in filter(None, conf.split("-")) and not conf.split(" ")[0] == "":
                obj = self.render_config(self.generated_spec, conf, vlan_info)
                if "mtu" in obj:
                    mtu_objs.append(obj)
                elif "remote_span" in obj:
                    remote_objs = obj
                elif obj:
                    objs.append(obj)
        # Appending MTU value to the retrieved dictionary
        for o, m in zip(objs, mtu_objs):
            o.update(m)
            final_objs.append(o)

        # Appending Remote Span value to related VLAN:
        if remote_objs:
            if remote_objs.get("remote_span"):
                for each in remote_objs.get("remote_span"):
                    for every in final_objs:
                        if each == every.get("vlan_id"):
                            every.update({"remote_span": True})
                            break
        facts = {}
        if final_objs:
            facts["vlans"] = []
            params = utils.validate_config(
                self.argument_spec,
                {"config": objs},
            )

            for cfg in params["config"]:
                facts["vlans"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def render_config(self, spec, conf, vlan_info):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        config = deepcopy(spec)

        if vlan_info == "Name" and "VLAN Name" not in conf:
            conf = list(filter(None, conf.split(" ")))
            config["vlan_id"] = int(conf[0])
            config["name"] = conf[1]
            state_idx = 2
            for i in range(2, len(conf)):  # check for index where state starts
                if conf[i] in ["suspended", "active"]:
                    state_idx = i
                    break
                elif conf[i].split("/")[0] in ["sus", "act"]:
                    state_idx = i
                    break
                config["name"] += " " + conf[i]
            try:
                if len(conf[state_idx].split("/")) > 1:
                    _state = conf[state_idx].split("/")[0]
                    if _state == "sus":
                        config["state"] = "suspend"
                    elif _state == "act":
                        config["state"] = "active"
                    config["shutdown"] = "enabled"
                else:
                    if conf[state_idx] == "suspended":
                        config["state"] = "suspend"
                    elif conf[state_idx] == "active":
                        config["state"] = "active"
                    config["shutdown"] = "disabled"
            except IndexError:
                pass
        elif vlan_info == "Type" and "VLAN Type" not in conf:
            conf = list(filter(None, conf.split(" ")))
            config["mtu"] = int(conf[3])
        elif vlan_info == "Remote":
            if len(conf.split(",")) > 1 or conf.isdigit():
                remote_span_vlan = []
                if len(conf.split(",")) > 1:
                    remote_span_vlan = conf.split(",")
                else:
                    remote_span_vlan.append(conf)
                remote_span = []
                for each in remote_span_vlan:
                    split_sp_list = each.split("-")
                    if len(split_sp_list) > 1:  # break range
                        for r_sp in range(
                            int(split_sp_list[0]),
                            int(split_sp_list[1]) + 1,
                        ):
                            remote_span.append(r_sp)
                    else:
                        remote_span.append(int(each))
                config["remote_span"] = remote_span

        return utils.remove_empties(config)
