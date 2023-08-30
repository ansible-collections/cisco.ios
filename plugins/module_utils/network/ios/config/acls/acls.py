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

        for wseq, wentry in iteritems(want):
            hentry = have.pop(wseq, {})
            if hentry:
                hentry = self.sanitize_protocol_options(wentry, hentry)
            if hentry != wentry:
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
                        if hentry.get("remarks"):  # remove remark if not in want
                            for rems in hentry.get("remarks"):
                                if rems not in wentry.get("remarks", {}):
                                    self.addcmd({"remarks": rems}, "remarks", negate=True)
                        else:  # remove ace if not in want
                            self.addcmd(add_afi(hentry, afi), "aces", negate=True)
                if wentry.get("remarks"):  # add remark if not in have
                    for rems in wentry.get("remarks"):
                        if rems not in hentry.get("remarks", {}):
                            self.addcmd({"remarks": rems}, "remarks")
                else:  # add ace if not in have
                    self.addcmd(add_afi(wentry, afi), "aces")

        # remove remaining entries from have aces list
        for hseq in have.values():
            if hseq.get("remarks"):  # remove remarks that are extra in have
                for rems in hseq.get("remarks"):
                    self.addcmd({"remarks": rems}, "remarks", negate=True)
            else:  # remove extra aces
                self.addcmd(add_afi(hseq, afi), "aces", negate=True)

    def sanitize_protocol_options(self, wace, hace):
        """handles protocol and protocol options as optional attribute"""
        if wace.get("protocol_options"):
            if not wace.get("protocol") and (
                list(wace.get("protocol_options"))[0] == hace.get("protocol")
            ):
                hace.pop("protocol")
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

        temp, count = dict(), 0
        if param:
            for each in param:  # ipv4 and ipv6 acl
                temp_acls = {}
                if each.get("acls"):
                    for acl in each.get("acls"):  # check each acl for aces
                        temp_aces = {}
                        if acl.get("aces"):
                            temp_rem = []  # remarks if defined in an ace
                            for ace in acl.get("aces"):  # each ace turned to dict
                                if ace.get("destination") and ace.get("destination", {}).get(
                                    "port_protocol",
                                    {},
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

                                if ace.get("remarks"):
                                    en_name = str(acl.get("name")) + "remark"
                                    temp_rem.extend(ace.pop("remarks"))

                                if ace.get("sequence"):
                                    temp_aces.update({ace.get("sequence"): ace})
                                elif ace:
                                    count += 1
                                    temp_aces.update({"_" + str(count): ace})

                            if temp_rem:  # add remarks to the temp ace
                                temp_aces.update({en_name: {"remarks": temp_rem}})

                        if acl.get("acl_type"):  # update acl dict with req info
                            temp_acls.update(
                                {acl.get("name"): {"aces": temp_aces, "acl_type": acl["acl_type"]}},
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
