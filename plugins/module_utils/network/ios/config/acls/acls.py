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
        self.default_acls = set(
            [
                "implicit_deny_v6",
                "implicit_permit_v6",
                "preauth_v6",
                "IP-Adm-V4-Int-ACL-global",
                "implicit_deny",
                "implicit_permit",
                "preauth_v4",
                "sl_def_acl",
            ],
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
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            if wantd.get("ipv4") and not haved.get("ipv4"):
                haved["ipv4"] = {}
            if wantd.get("ipv6") and not haved.get("ipv6"):
                haved["ipv6"] = {}
            for key, hvalue in haved.items():
                wvalue = wantd.pop(key, {})
                if wvalue:
                    wplists = wvalue.get("acls", {})
                    hplists = hvalue.get("acls", {})
                    hvalue["acls"] = {
                        k: v for k, v in hplists.items() if k in wplists or not wplists
                    }

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have, afi=k)

        for k, want in wantd.items():
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
        for wname, wentry in wplists.items():
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
            for hname, hval in hplists.items():
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

        # case 1 - loop on want and compare with have data here
        for wseq, wentry in want.items():
            hentry = have.pop(wseq, {})
            rem_hentry, rem_wentry = {}, {}

            if hentry:  # if there is have information with same sequence
                # the protocol options are processed here
                hentry = self.sanitize_protocol_options(wentry, hentry)

            if hentry != wentry:  # if want and have is different
                if hentry:  # separate remarks from have in an ace entry
                    rem_hentry["remarks"] = pop_remark(hentry, afi)
                if wentry:  # separate remarks from want in an ace entry
                    rem_wentry["remarks"] = pop_remark(wentry, afi)

                if hentry:  # have aces processing starts here
                    if self.state == "merged":
                        self._module.fail_json(
                            msg="Cannot update existing sequence {0} of ACLs {1} with state merged."
                            " Please use state replaced or overridden.".format(
                                hentry.get("sequence", ""),
                                name,
                            ),
                        )  # if merged then don't update anything and fail

                    # i.e if not merged
                    if rem_hentry.get("remarks") != rem_wentry.get("remarks"):
                        self.addcmd(
                            {
                                "sequence": hentry.get("sequence", None),
                            },
                            "remarks_no_data",
                            negate=True,
                        )  # remove all remarks for a ace if want and have don't match
                        # as if we randomly add aces we cannot maintain order we have to
                        # add all of them again, for that ace
                        rem_hentry["remarks"] = {}
                        # and me empty our have as we would add back
                        # all our remarks for that ace anyways

                    # remove ace if not in want
                    # we might think why not update it directly,
                    # if we try to update without negating the entry appliance
                    # reports % Duplicate sequence number
                    if hentry != wentry:
                        self.addcmd(add_afi(hentry, afi), "aces", negate=True)
                        # once an ace is negated intentionally emptying out have so that
                        # the remarks are repopulated, as the remarks and ace behavior is sticky
                        # if an ace is taken out all the remarks is removed automatically.
                        rem_hentry["remarks"] = {}

                if rem_wentry.get("remarks"):  # add remark if not in have
                    if rem_hentry.get("remarks"):
                        self.addcmd(
                            {
                                "sequence": hentry.get("sequence", None),
                            },
                            "remarks_no_data",
                            negate=True,
                        )  # but delete all remarks before to protect order
                    for k_wrems, wrems in rem_wentry.get("remarks").items():
                        self.addcmd(
                            {
                                "remarks": wrems,
                                "sequence": wentry.get("sequence", ""),
                            },
                            "remarks",
                        )

                # add ace if not in have
                if hentry != wentry:
                    if len(wentry) == 1 and wentry.get(
                        "sequence",
                    ):  # if the ace entry just has sequence then do nothing
                        continue
                    else:  # add normal ace entries from want
                        self.addcmd(add_afi(wentry, afi), "aces")

        # case 2 - loop over remaining have and remove them
        for hseq in have.values():
            if hseq.get("remarks"):  # remove all remarks in that
                self.addcmd(
                    {
                        "sequence": hseq.get("sequence", None),
                    },
                    "remarks_no_data",
                    negate=True,
                )
                hseq.pop("remarks")
            # deal with the rest of ace entry
            self.addcmd(
                add_afi(hseq, afi),
                "aces",
                negate=True,
            )

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
                        if acl.get("name", None) in self.default_acls:
                            continue
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
                                        ace["destination"]["port_protocol"][k] = (
                                            self.port_protocl_no_to_protocol(v, ace.get("protocol"))
                                        )
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

    def port_protocl_no_to_protocol(self, num, protocol):
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
        if protocol == "udp" and num in ["135"]:
            return num
        return map_protocol.get(num, num)
