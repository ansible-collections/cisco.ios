#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_l3_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l3_interfaces import (
    L3_interfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
    validate_n_expand_ipv4,
)


class L3_interfaces(ResourceModule):
    """
    The ios_l3_interfaces class
    """

    def __init__(self, module):
        super(L3_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l3_interfaces",
            tmplt=L3_interfacesTemplate(),
        )
        self.parsers = [
            "mac_address",
            "ipv4.address",
            "ipv4.pool",
            "ipv4.dhcp",
            "ipv4.source_interface",
            "ipv4.mtu",
            "ipv4.redirects",
            "ipv4.unreachables",
            "ipv4.proxy_arp",
            "ipv6.address",
            "ipv6.autoconfig",
            "ipv6.dhcp",
            "ipv6.enable",
        ]
        self.gen_parsers = [
            "autostate",
        ]

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        if self.want:
            wantd = {}
            for each in self.want:
                wantd.update({each["name"]: each})
        else:
            wantd = {}
        if self.have:
            haved = {}
            for each in self.have:
                haved.update({each["name"]: each})
        else:
            haved = {}

        for each in wantd, haved:
            self.list_to_dict(each)

        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            have = haved.pop(k, {})
            # New interface (doesn't use fact file)
            if k[:4] == "Vlan":
                have.setdefault("autostate", True)
                want.setdefault("autostate", True)
            self._compare(want=want, have=have)

    def _compare(self, want, have):
        begin = len(self.commands)
        self.compare(parsers=self.gen_parsers, want=want, have=have)
        self._compare_lists(want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def _compare_lists(self, want, have):
        helper_address_dict_wantd = want.get("helper_addresses", {})
        if helper_address_dict_wantd:
            for value in ["ipv4"]:
                for k, val in helper_address_dict_wantd.get(value, {}).items():
                    hacl = have.get("helper_addresses", {}).get(value, {})
                    hacl_val = hacl.pop(k, {})
                    if hacl_val and hacl_val != val:
                        self.compare(
                            parsers=["helper_addresses_ipv4"],
                            want={},
                            have={value: hacl_val},
                        )
                    self.compare(
                        parsers=["helper_addresses_ipv4"],
                        want={value: val},
                        have={value: hacl_val},
                    )
        helper_address_dict_haved = have.get("helper_addresses", {})
        if helper_address_dict_haved:
            for value in ["ipv4"]:
                for k, val in helper_address_dict_haved.get(value, {}).items():
                    self.compare(
                        parsers=["helper_addresses_ipv4"],
                        want={},
                        have={value: val},
                    )
        for afi in ("ipv4", "ipv6"):
            wacls = want.pop(afi, {})
            hacls = have.pop(afi, {})

            for key, entry in wacls.items():
                if entry.get("secondary", False) is True:
                    continue
                # entry is set as primary
                hacl = hacls.get(key, {})
                if hacl.get("secondary", False) is True:
                    hacl = {}
                self.validate_ips(afi, want=entry, have=hacl)

                if hacl:
                    hacls.pop(key, {})

                self.compare(
                    parsers=self.parsers,
                    want={afi: entry},
                    have={afi: hacl},
                )

            for key, entry in wacls.items():
                if entry.get("secondary", False) is False:
                    continue
                # entry is set as secondary
                hacl = hacls.get(key, {})
                if hacl.get("secondary", False) is False:
                    # hacl is set as primary, if wacls has no other primary entry we must keep
                    # this entry as primary (so we'll compare entry to hacl and not
                    # generate commands)
                    if list(
                        filter(
                            lambda w: w.get("secondary", False) is False,
                            wacls.values(),
                        ),
                    ):
                        # another primary is in wacls
                        hacl = {}
                self.validate_ips(afi, want=entry, have=hacl)

                if hacl:
                    hacls.pop(key, {})

                self.compare(
                    parsers=self.parsers,
                    want={afi: entry},
                    have={afi: hacl},
                )

            # remove remaining items in have for replaced
            # these can be subnets that are no longer used
            # or secondaries that have moved to primary
            # or primary that has moved to secondary
            for key, entry in hacls.items():
                self.validate_ips(afi, have=entry)
                self.compare(parsers=self.parsers, want={}, have={afi: entry})

    def validate_ips(self, afi, want=None, have=None):
        if afi == "ipv4" and want:
            v4_addr = validate_n_expand_ipv4(self._module, want) if want.get("address") else {}
            if v4_addr:
                want["address"] = v4_addr

        if afi == "ipv4" and have:
            v4_addr_h = validate_n_expand_ipv4(self._module, have) if have.get("address") else {}
            if v4_addr_h:
                have["address"] = v4_addr_h

    def list_to_dict(self, param):
        def list_to_dict_by_destination_ip(helper_list):
            return {item["destination_ip"]: item for item in helper_list}

        if param:
            for k, val in param.items():
                val["name"] = normalize_interface(val["name"])
                helper_addresses_dict = val.get("helper_addresses", {})
                for value in ["ipv4"]:
                    if value in helper_addresses_dict:
                        helper_addresses_dict[value] = list_to_dict_by_destination_ip(
                            helper_addresses_dict[value],
                        )
                if "ipv4" in val:
                    temp = {}
                    for each in val["ipv4"]:
                        if each.get("address") and each.get("address") != "dhcp":
                            temp.update({each["address"]: each})
                        elif each.get("address") == "dhcp":
                            # deprecated attribute
                            temp.update(
                                {
                                    "dhcp": {
                                        "dhcp": {
                                            "client_id": each.get("dhcp_client"),
                                            "hostname": each.get("dhcp_hostname"),
                                        },
                                    },
                                },
                            )
                        if not each.get("address"):
                            temp.update({list(each.keys())[0]: each})
                    val["ipv4"] = temp
                if "ipv6" in val:
                    temp = {}
                    for each in val["ipv6"]:
                        if each.get("address"):
                            each["address"] = each["address"].lower()
                            temp.update({each["address"]: each})
                        if not each.get("address"):
                            temp.update({list(each.keys())[0]: each})
                    val["ipv6"] = temp
