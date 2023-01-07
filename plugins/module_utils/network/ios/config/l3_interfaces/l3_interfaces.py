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

import re

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
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
    validate_ipv6,
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
            "ipv4.address",
            "ipv4.pool",
            "ipv4.dhcp",
            "ipv6.address",
            "ipv6.autoconfig",
            "ipv6.dhcp",
        ]
        self.interfaces_before = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            if (any('vrf forwarding' in cmd for cmd in self.commands)
                and self._module.params.get("restore_commands")):
                self.interfaces_before = self.get_l3_interfaces()
                self.run_commands()
                self.vrf_fixup()
            else:
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
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        begin = len(self.commands)
        self._compare_lists(want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(
                begin,
                self._tmplt.render(want or have, "name", False),
            )

    def _compare_lists(self, want, have):
        self.compare(parsers=['ipv4.vrf', 'vrf'],
                     want=want,
                     have=have,
                     )

        for afi in ("ipv4", "ipv6"):
            wacls = want.pop(afi, {})
            hacls = have.pop(afi, {})

            for key, entry in wacls.items():
                self.validate_ips(afi, want=entry, have=hacls.get(key, {}))
                # Always reapply commands part of the intent (want) when there's
                # a VRF change
                if want.get('vrf') != have.get('vrf'):
                    hacls.pop(key, {})

                self.compare(
                    parsers=self.parsers,
                    want={afi: entry},
                    have={afi: hacls.pop(key, {})},
                )
            # remove remaining items in have for replaced
            for key, entry in hacls.items():
                self.validate_ips(afi, have=entry)
                self.compare(parsers=self.parsers, want={}, have={afi: entry})

    def get_l3_interfaces(self):
        """
        Uses the Facts module to obtain the current interfaces configuration.
        This is further used by vrf_fixup to snapshot the configuration before
        and after applying/removing VRFs

        :rtype: list
        :return: list containing re.groupdict matching interfaces and params
        """
        intf_sect_pattern = r"^interface\s(?P<intf>\S+)\n(?P<params>(?:\s.*?\n)+)"
        cfg = self._connection.get_config()
        m = re.finditer(intf_sect_pattern, cfg, re.M)
        if m:
            return [i.groupdict() for i in m]

    def vrf_fixup(self):
        """
        Applying/removing VRFs to/from interfaces, removes certain parameters
        like ip addresses. These parameters must be reapplied. Instead of mapping out
        every command potentially removed, this function compares before and
        after snapshots to discover removed commands.

        The following is performed
            1. Creates a dict of already deployed commands.
            2. Takes an after snapshot of the interfaces configuration.
            3. Generates a list of removed commands by comparing the before and after
               snapshot.
            4. Repopulates self.commands with removed commands *unless* the removed
               commands are part of the play/intent.
            5. Runs self.run_commands with the new self.commands list
            6. Rebuilds self.commands with *all* commands deployed for
               correct representation in the Result Values.

        :return: None
        """
        # create dict of deployed commands
        _k = []
        deployed = {}
        for cmd in self.commands:
            if cmd.startswith("interface"):
                k_struct = cmd.split(" ")[1]
                deployed[k_struct] = []
                _k = deployed[k_struct]
            else:
                _k.append(cmd)

        # take the after snapshot
        interfaces_after = self.get_l3_interfaces()

        def get_before_after(intf):
            """
            Gets the before and after snapshot for the given intf.
            :param intf: str
            :return: list containing dict entries of interfaces before and after
            """
            ret = []
            for entries in (self.interfaces_before, interfaces_after):
                ret.append(next((entry for entry in entries
                                 if entry.get("intf") == intf), None))
            return ret

        def include_criteria(cmd):
            """
            Checks if the removed cmd is part of the play or removed as part of
            applying/removing VRF. Uses the parsers to compare the removed command
            with the deployed commands. A match in both assumes the command is put
            there as a result of the play and should not be reapplied

            :param cmd: str
            :return: True if cmd should be reapplied to device
            """
            for pattern in L3_interfacesTemplate.PARSERS:
                pattern = pattern.get("getval")
                # add space for deployed commands for matching PARSERS regex
                deployed_cmds = [ f' {cmd}' for cmd in deployed.get(interface) ]
                if (re.search(pattern, cmd)
                        and any(re.search(pattern, _cmd) for _cmd in deployed_cmds)
                        or "no ip address" in cmd):
                    return False
            return True

        # Iterate over the changed interfaces and regenerate self.commands
        # with commands that must be reapplied
        self.commands = []
        for interface in deployed.keys():
            if not any('vrf forwarding' in p for p in deployed[interface]):
                continue
            before, after = get_before_after(interface)
            res = list(set(before.get("params").splitlines())
                       - set(after.get("params").splitlines()))
            commands = [cmd.lstrip() for cmd in res if include_criteria(cmd)]
            if commands:
                self.commands.append(f"interface {interface}")
                self.commands += commands
                deployed[interface] += commands
        # Reapply the removed commands if any
        if self.commands:
            self.run_commands()

        # Regenerate command list for correct repr in return values
        self.commands = []
        for intf, params in deployed.items():
            self.commands.append(f"interface {intf}")
            for param in params:
                self.commands.append(param)

    def validate_ips(self, afi, want=None, have=None):
        if afi == "ipv4" and want:
            v4_addr = validate_n_expand_ipv4(self._module, want) if want.get("address") else {}
            if v4_addr:
                want["address"] = v4_addr
        elif afi == "ipv6" and want:
            if want.get("address"):
                validate_ipv6(want["address"], self._module)

        if afi == "ipv4" and have:
            v4_addr_h = validate_n_expand_ipv4(self._module, have) if have.get("address") else {}
            if v4_addr_h:
                have["address"] = v4_addr_h
        elif afi == "ipv6" and have:
            if have.get("address"):
                validate_ipv6(have["address"], self._module)

    def list_to_dict(self, param):
        if param:
            for _k, val in iteritems(param):
                val["name"] = normalize_interface(val["name"])
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
                                            "client_id": each.get(
                                                "dhcp_client",
                                            ),
                                            "hostname": each.get(
                                                "dhcp_hostname",
                                            ),
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
