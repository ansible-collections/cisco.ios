# pylint: skip-file
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acls fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acls.acls import (
    AclsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class AclsFacts(object):
    """ The ios_acls fact class
    """

    def __init__(self, module, subspec="config", options="options"):

        self._module = module
        self.argument_spec = AclsArgs.argument_spec

    def get_acl_data(self, connection):
        # Get the access-lists from the ios router
        return connection.get("sh access-list")

    def get_acl_remarks_data(self, connection):
        # Get the remarks on access-lists from the ios router
        return connection.get(
            "show running-config | include ip(v6)* access-list|remark"
        )

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for acls
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        remarks_data = None
        rem_par = dict()
        if not data:
            data = self.get_acl_data(connection)
            remarks_data = self.get_acl_remarks_data(connection)

        rmmod = NetworkTemplate(lines=data.splitlines(), tmplt=AclsTemplate())
        current = rmmod.parse()

        if (
            remarks_data
        ):  # remarks being fetched with a different command, call to parse
            rem_dt = NetworkTemplate(
                lines=remarks_data.splitlines(), tmplt=AclsTemplate()
            )
            rem_par = rem_dt.parse()
            if rem_par.get("acls"):
                del rem_par["acls"]

        temp_v4 = []
        temp_v6 = []

        if current.get("acls"):
            for k, v in iteritems(current.get("acls")):
                if v.get("afi") == "ipv4":
                    del v["afi"]
                    if rem_par.get(k) and v.get(
                        "aces"
                    ):  # add v4 remarks as per acl
                        v["aces"].append({"remarks": rem_par.get(k)})
                    elif rem_par.get(k) and not v.get("aces"):
                        v["aces"] = [{"remarks": rem_par.get(k)}]
                    temp_v4.append(v)

                elif v.get("afi") == "ipv6":
                    del v["afi"]
                    if rem_par.get(k) and v.get(
                        "aces"
                    ):  # add v6 remarks as per acl
                        v["aces"].append({"remarks": rem_par.get(k)})
                    elif rem_par.get(k) and not v.get("aces"):
                        v["aces"] = [{"remarks": rem_par.get(k)}]
                    temp_v6.append(v)

            temp_v4 = sorted(temp_v4, key=lambda i: str(i["name"]))
            temp_v6 = sorted(temp_v6, key=lambda i: str(i["name"]))

            for each in temp_v4:
                aces_ipv4 = each.get("aces")
                if aces_ipv4:
                    for each_ace in each.get("aces"):
                        if each_ace.get("icmp_igmp_tcp_protocol"):
                            each_ace["protocol_options"] = {
                                each_ace["protocol"]: {
                                    each_ace.pop(
                                        "icmp_igmp_tcp_protocol"
                                    ).replace("-", "_"): True
                                }
                            }

            for each in temp_v6:
                aces_ipv6 = each.get("aces")
                if aces_ipv6:
                    for each_ace in each.get("aces"):
                        if each_ace.get("icmp_igmp_tcp_protocol"):
                            each_ace["protocol_options"] = {
                                each_ace["protocol"]: {
                                    each_ace.pop(
                                        "icmp_igmp_tcp_protocol"
                                    ).replace("-", "_"): True
                                }
                            }

        objs = []
        if temp_v4:
            objs.append({"afi": "ipv4", "acls": temp_v4})
        if temp_v6:
            objs.append({"afi": "ipv6", "acls": temp_v6})

        facts = {}
        if objs:
            facts["acls"] = []
            params = utils.validate_config(
                self.argument_spec, {"config": objs}
            )
            for cfg in params["config"]:
                facts["acls"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
