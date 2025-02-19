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

import re

from ansible.module_utils._text import to_text
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acls.acls import (
    AclsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)


class AclsFacts(object):
    """The ios_acls fact class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = AclsArgs.argument_spec

    def get_acl_data(self, connection):
        # Removed the show access-list
        # Removed the show running-config | include ip(v6)* access-list|remark
        return connection.get("show running-config | section access-list")

    def get_acl_names(self, connection):
        # this information is required to scoop out the access lists which has no aces
        return connection.get("show access-lists | include access list")

    def populate_empty_acls(self, raw_acls, raw_acls_name):
        # this would update empty acls to the full acls entry
        if raw_acls and raw_acls_name:
            for aclnames, acldata in raw_acls_name.get("acls").items():
                if aclnames not in raw_acls.get("acls").keys():
                    if not raw_acls.get("acls"):
                        raw_acls["acls"] = {}
                    raw_acls["acls"][aclnames] = acldata
        elif raw_acls_name and not raw_acls:
            for aclnames, acldata in raw_acls_name.get("acls").items():
                if not raw_acls.get("acls"):
                    raw_acls["acls"] = {}
                raw_acls["acls"][aclnames] = acldata
        return raw_acls

    def sanitize_data(self, data):
        """removes matches or extra config info that is added on acl match"""
        re_data = ""
        remarks_idx = 0
        for da in data.split("\n"):
            if "match" in da:
                mod_da = re.sub(r"\([^()]*\)", "", da)
                re_data += mod_da[:-1] + "\n"
            elif re.match(r"\s*\d+\sremark.+", da, re.IGNORECASE) or re.match(
                r"\s*remark.+",
                da,
                re.IGNORECASE,
            ):
                remarks_idx += 1
                re_data += to_text(remarks_idx) + " " + da + "\n"
            else:
                re_data += da + "\n"
        return re_data

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for acls
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        namedata = ""

        if not data:
            data = self.get_acl_data(connection)
            namedata = self.get_acl_names(connection)

        if data:
            data = self.sanitize_data(data)

        # parse main information
        templateObjMain = NetworkTemplate(lines=data.splitlines(), tmplt=AclsTemplate())
        raw_acls = templateObjMain.parse()

        if namedata:
            # parse just names to update empty acls
            templateObjName = NetworkTemplate(
                lines=namedata.splitlines(),
                tmplt=AclsTemplate(),
            )
            raw_acl_names = templateObjName.parse()
            raw_acls = self.populate_empty_acls(raw_acls, raw_acl_names)

        temp_v4 = []
        temp_v6 = []

        if raw_acls.get("acls"):
            for k, v in iteritems(raw_acls.get("acls")):
                if v.get("afi") == "ipv4" and v.get("acl_type") in [
                    "standard",
                    "extended",
                ]:
                    del v["afi"]
                    temp_v4.append(v)
                elif v.get("afi") == "ipv6":
                    del v["afi"]
                    temp_v6.append(v)

            temp_v4 = sorted(temp_v4, key=lambda i: str(i["name"]))
            temp_v6 = sorted(temp_v6, key=lambda i: str(i["name"]))

            def factor_source_dest(ace, typ):
                temp = ace.get(typ, {})
                if temp.get("address"):
                    _temp_addr = temp.get("address", "")
                    ace[typ]["address"] = _temp_addr.split(" ")[0]
                    ace[typ]["wildcard_bits"] = _temp_addr.split(" ")[1]
                if temp.get("ipv6_address"):
                    _temp_addr = temp.get("ipv6_address", "")
                    if len(_temp_addr.split(" ")) == 2:
                        ipv6_add = ace[typ].pop("ipv6_address")
                        ace[typ]["address"] = ipv6_add.split(" ")[0]
                        ace[typ]["wildcard_bits"] = ipv6_add.split(" ")[1]
                    else:
                        ace[typ]["address"] = ace[typ].pop("ipv6_address")

            def process_protocol_options(each):
                for each_ace in each.get("aces"):
                    if each.get("acl_type") == "standard":
                        if len(each_ace.get("source", {})) == 1 and each_ace.get(
                            "source",
                            {},
                        ).get(
                            "address",
                        ):
                            each_ace["source"]["host"] = each_ace["source"].pop(
                                "address",
                            )
                        if each_ace.get("source", {}).get("address"):
                            addr = each_ace.get("source", {}).get("address")
                            if addr[-1] == ",":
                                each_ace["source"]["address"] = addr[:-1]
                    else:  # for extended acl
                        if each_ace.get("source", {}):
                            factor_source_dest(each_ace, "source")
                        if each_ace.get("destination", {}):
                            factor_source_dest(each_ace, "destination")

                    if each_ace.get("icmp_igmp_tcp_protocol"):
                        each_ace["protocol_options"] = {
                            each_ace["protocol"]: {
                                each_ace.pop("icmp_igmp_tcp_protocol").replace(
                                    "-",
                                    "_",
                                ): True,
                            },
                        }
                    if each_ace.get("protocol_number"):
                        each_ace["protocol_options"] = {
                            "protocol_number": each_ace.pop("protocol_number"),
                        }

            def collect_remarks(aces):
                """makes remarks list per ace"""
                ace_entry = []
                ace_rem = []
                rem = {}
                # every remarks is one list item which has a sequence number
                # every ace remark is preserved and ordered
                # at the end of each sequence it is flushed to a ace entry
                for i in aces:
                    # i here denotes an ace, which would be populated with remarks entries
                    if i.get("is_remark_for"):
                        if not rem.get(i.get("is_remark_for")):
                            rem[i.get("is_remark_for")] = {"remarks": []}
                            rem[i.get("is_remark_for")]["remarks"].append(
                                i.get("the_remark"),
                            )
                        else:
                            rem[i.get("is_remark_for")]["remarks"].append(
                                i.get("the_remark"),
                            )
                    else:
                        if rem:
                            if rem.get(i.get("sequence")):
                                ace_rem = rem.pop(i.get("sequence"))
                                i["remarks"] = ace_rem.get("remarks")
                        ace_entry.append(i)

                if rem:  # pending remarks
                    for pending_rem_seq, pending_rem_val in rem.items():
                        # there can be ace entry with just a remarks and no ace actually
                        # 10 remarks I am a remarks
                        # 20 ..... so onn
                        if pending_rem_seq != "remark":
                            ace_entry.append(
                                {
                                    "sequence": pending_rem_seq,
                                    "remarks": pending_rem_val.get("remarks"),
                                },
                            )
                        else:
                            # this handles the classic set of remarks at the end, which is not tied to
                            # any sequence number
                            pending_rem = rem.get("remark", {})
                            ace_entry.append({"remarks": pending_rem.get("remarks")})
                return ace_entry

            for each in temp_v4:
                if each.get("aces"):
                    # handling remarks for each ace entry
                    each["aces"] = collect_remarks(each.get("aces"))
                    process_protocol_options(each)

            for each in temp_v6:
                if each.get("aces"):
                    each["aces"] = collect_remarks(each.get("aces"))
                    process_protocol_options(each)

        objs = []
        if temp_v4:
            objs.append({"afi": "ipv4", "acls": temp_v4})
        if temp_v6:
            objs.append({"afi": "ipv6", "acls": temp_v6})

        facts = {}
        if objs:
            facts["acls"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for cfg in params["config"]:
                facts["acls"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
