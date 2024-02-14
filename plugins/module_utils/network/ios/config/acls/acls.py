#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acls class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)


class Acls(ResourceModule):
    """
    The ios_acls config class
    """

    def __init__(self, module):
        super(Acls, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="acls",
            tmplt=AclsTemplate(),
        )

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
        haved, wantd = dict(), dict()

        if self.have:
            haved = self.list_to_dict(self.have)
        if self.want:
            wantd = self.list_to_dict(self.want)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to want
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            if wantd.get("ipv4") and not haved.get("ipv4"):
                haved["ipv4"] = {}
            if wantd.get("ipv6") and not haved.get("ipv6"):
                haved["ipv6"] = {}
            for key, hvalue in iteritems(haved):
                wvalue = wantd.pop(key, {})
                if wvalue:
                    wplists = wvalue.get("acls", {})
                    hplists = hvalue.get("acls", {})
                    hvalue["acls"] = {
                        k: v for k, v in iteritems(hplists) if k in wplists or not wplists
                    }

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have, afi=k)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}), afi=k)

    def _compare(self, want, have, afi):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the acls network resource.
        """

        def rearrange_cmds(aces):
            non_negates = []
            negates = []
            for ace in aces:
                if ace.startswith("no"):
                    negates.append(ace)
                else:
                    non_negates.append(ace)
            if non_negates or negates:
                negates.extend(non_negates)
            return negates

        wplists = want.get("acls", {})
        hplists = have.get("acls", {})
        for wname, wentry in iteritems(wplists):
            hentry = hplists.pop(wname, {})
            acl_type = wentry["acl_type"] if wentry.get("acl_type") else hentry.get("acl_type")
            # If ACLs type is different between existing and wanted ACL, we need first remove it
            if acl_type != hentry.get("acl_type", acl_type):
                self.commands.append(
                    "no " + self.acl_name_cmd(wname, afi, hentry.get("acl_type", "")),
                )
                hentry.pop(
                    "aces",
                    {},
                )  # We remove ACEs because we have previously add a command to suppress completely the ACL

            begin = len(self.commands)  # to determine the index for acl command
            self._compare_aces(
                wentry.pop("aces", {}),
                hentry.pop("aces", {}),
                afi,
                wname,
            )  # handle aces

            end = len(self.commands)
            self.commands[begin:end] = rearrange_cmds(self.commands[begin:])

            if len(self.commands) != begin or (not have and want):
                _cmd = self.acl_name_cmd(wname, afi, acl_type)
                self.commands.insert(begin, _cmd)

        if self.state in ["overridden", "deleted"]:
            # remove remaining acls lists
            for hname, hval in iteritems(hplists):
                _cmd = self.acl_name_cmd(hname, afi, hval.get("acl_type", ""))
                self.commands.append("no " + _cmd)

    def _compare_aces(self, want, have, afi, name):
        """compares all aces"""

        def add_afi(entry, afi):
            """adds afi needed for
            setval processing"""
            if entry:
                entry["afi"] = afi
            return entry

        def pop_remark(r_entry, afi):
            """Takes out remarks from ace entry as remarks not same
            does not mean the ace entry to be re-introduced
            """
            if r_entry.get("remarks"):
                return r_entry.pop("remarks")
            else:
                return {}

        for wseq, wentry in iteritems(want):
            hentry = have.pop(wseq, {})
            rem_hentry, rem_wentry = {}, {}

            if hentry:
                hentry = self.sanitize_protocol_options(wentry, hentry)

            if hentry != wentry:  # will let in if ace is same but remarks is not same
                if hentry:
                    rem_hentry["remarks"] = pop_remark(hentry, afi)
                if wentry:
                    rem_wentry["remarks"] = pop_remark(wentry, afi)

                if hentry:
                    if self.state == "merged":
                        self._module.fail_json(
                            msg="Cannot update existing sequence {0} of ACLs {1} with state merged."
                            " Please use state replaced or overridden.".format(
                                hentry.get("sequence", ""),
                                name,
                            ),
                        )
                    else:  # other action states
                        if rem_hentry.get("remarks"):  # remove remark if not in want
                            for k_hrems, hrems in rem_hentry.get("remarks").items():
                                if k_hrems not in rem_wentry.get("remarks", {}).keys():
                                    if self.state in ["replaced", "overridden"]:
                                        self.addcmd(
                                            {
                                                "remarks": hrems,
                                                "sequence": hentry.get("sequence", ""),
                                            },
                                            "remarks_no_data",
                                            negate=True,
                                        )
                                        break
                                    else:
                                        self.addcmd(
                                            {
                                                "remarks": hrems,
                                                "sequence": hentry.get("sequence", ""),
                                            },
                                            "remarks",
                                            negate=True,
                                        )
                        # remove ace if not in want
                        if hentry != wentry:
                            self.addcmd(add_afi(hentry, afi), "aces", negate=True)
                if rem_wentry.get("remarks"):  # add remark if not in have
                    for k_wrems, wrems in rem_wentry.get("remarks").items():
                        if k_wrems not in rem_hentry.get("remarks", {}).keys():
                            self.addcmd(
                                {
                                    "remarks": wrems,
                                    "sequence": hentry.get("sequence", ""),
                                },
                                "remarks",
                            )
                        else:
                            rem_hentry.get("remarks", {}).pop(k_wrems)
                    # We remove remarks that are not in the wentry for this ACE
                    for k_hrems, hrems in rem_hentry.get("remarks", {}).items():
                        self.addcmd(
                            {"remarks": hrems, "sequence": hentry.get("sequence", "")},
                            "remarks",
                            negate=True,
                        )

                # add ace if not in have
                if hentry != wentry:
                    self.addcmd(add_afi(wentry, afi), "aces")

        # remove remaining entries from have aces list
        for hseq in have.values():
            if hseq.get("remarks"):  # remove remarks that are extra in have
                for krems, rems in hseq.get("remarks").items():
                    self.addcmd(
                        {"remarks": rems, "sequence": hseq.get("sequence", "")},
                        "remarks",
                        negate=True,
                    )
                hseq.pop("remarks")
            self.addcmd(add_afi(hseq, afi), "aces", negate=True)
            # else:  # remove extra aces
            #     self.addcmd(add_afi(hseq, afi), "aces", negate=True)

    def sanitize_protocol_options(self, wace, hace):
        """handles protocol and protocol options as optional attribute"""
        if wace.get("protocol_options"):
            if not wace.get("protocol") and (
                list(wace.get("protocol_options"))[0] == hace.get("protocol")
            ):
                hace.pop("protocol")
                hace["protocol_options"] = wace.get("protocol_options")
        return hace

    def acl_name_cmd(self, name, afi, acl_type):
        """generate parent acl command"""

        if afi == "ipv4":
            if not acl_type:
                try:
                    acl_id = int(name)
                    if not acl_type:
                        if acl_id >= 1 and acl_id <= 99:
                            acl_type = "standard"
                        if acl_id >= 100 and acl_id <= 199:
                            acl_type = "extended"
                except ValueError:
                    acl_type = "extended"
            command = "ip access-list {0} {1}".format(acl_type, name)
        elif afi == "ipv6":
            command = "ipv6 access-list {0}".format(name)
        return command

    def list_to_dict(self, param):
        """converts list attributes to dict"""

        temp = dict()
        if param:
            for each in param:  # ipv4 and ipv6 acl
                temp_acls = {}
                if each.get("acls"):
                    for acl in each.get("acls"):  # check each acl for aces
                        temp_aces = {}
                        if acl.get("aces"):
                            rem_idx = 0  # remarks if defined in an ace
                            for count, ace in enumerate(
                                acl.get("aces"),
                            ):  # each ace turned to dict
                                if (
                                    ace.get("destination")
                                    and ace.get("destination", {}).get(
                                        "port_protocol",
                                        {},
                                    )
                                    and not ace.get("destination", {})
                                    .get("port_protocol", {})
                                    .get("range")
                                ):
                                    for k, v in (
                                        ace.get("destination", {}).get("port_protocol", {}).items()
                                    ):
                                        ace["destination"]["port_protocol"][
                                            k
                                        ] = self.port_protocl_no_to_protocol(v)
                                if acl.get("acl_type") == "standard":
                                    for ks in list(ace.keys()):
                                        if ks not in [
                                            "sequence",
                                            "grant",
                                            "source",
                                            "remarks",
                                            "log",
                                        ]:  # failing for mutually exclusive standard acl key
                                            self._module.fail_json(
                                                "Unsupported attribute for standard ACL - {0}.".format(
                                                    ks,
                                                ),
                                            )

                                if ace.get(
                                    "remarks",
                                ):  # index aces inside of each ace don't cluster them all
                                    rem_ace = {}
                                    # en_name = str(acl.get("name")) + "remark"
                                    # temp_rem.extend(ace.pop("remarks"))
                                    for remks in ace.get("remarks"):
                                        rem_ace[remks.replace(" ", "_")] = remks
                                    ace["remarks"] = rem_ace

                                if ace.get("sequence"):
                                    temp_aces.update({ace.get("sequence"): ace})
                                elif ace.get("remarks"):
                                    temp_aces.update({"__{0}".format(rem_idx): ace})
                                    rem_idx += 1
                                elif ace:
                                    temp_aces.update({"_" + to_text(count): ace})

                            # if temp_rem:  # add remarks to the temp ace
                            #     temp_aces.update({en_name: {"remarks": temp_rem}})

                        if acl.get("acl_type"):  # update acl dict with req info
                            temp_acls.update(
                                {
                                    acl.get("name"): {
                                        "aces": temp_aces,
                                        "acl_type": acl["acl_type"],
                                    },
                                },
                            )
                        else:  # if no acl type then here eg: ipv6
                            temp_acls.update({acl.get("name"): {"aces": temp_aces}})
                each["acls"] = temp_acls
                temp.update({each["afi"]: {"acls": temp_acls}})
            return temp

    def port_protocl_no_to_protocol(self, num):
        map_protocol = {
            "179": "bgp",
            "19": "chargen",
            "514": "cmd",
            "13": "daytime",
            "9": "discard",
            "53": "domain",
            "7": "echo",
            "512": "exec",
            "79": "finger",
            "21": "ftp",
            "20": "ftp-data",
            "70": "gopher",
            "101": "hostname",
            "113": "ident",
            "194": "irc",
            "543": "klogin",
            "544": "kshell",
            "513": "login",
            "515": "lpd",
            "135": "msrpc",
            "119": "nntp",
            "5001": "onep-plain",
            "5002": "onep-tls",
            "496": "pim-auto-rp",
            "109": "pop2",
            "110": "pop3",
            "25": "smtp",
            "111": "sunrpc",
            "49": "tacacs",
            "517": "talk",
            "23": "telnet",
            "37": "time",
            "540": "uucp",
            "43": "whois",
            "80": "www",
        }  # NOTE - "514": "syslog" duplicate value device renders "cmd"
        return map_protocol.get(num, num)
