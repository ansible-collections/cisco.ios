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

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)


class Acls(ResourceModule):
    """
    The ios_ntp_global config class
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
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
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

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            for k, v in haved.items():
                afi = k
                afi_want = wantd.get(k)
                if (afi_want and not afi_want.get("acls")) or not wantd:
                    for key, val in v["acls"].items():
                        val.update({"afi": afi, "name": key})
                        self.addcmd(val, "acls_name", True)
                elif afi_want:
                    for key, val in v["acls"].items():
                        want_acl = afi_want["acls"].get(key)
                        if want_acl:
                            val.update({"afi": afi, "name": key})
                            self.addcmd(val, "acls_name", True)

        # remove superfluous config for overridden and deleted
        if self.state == "overridden":
            for k, v in haved.items():
                afi = k
                afi_want = wantd.get(k)
                for key, val in v["acls"].items():
                    if afi_want:
                        acls_want = afi_want["acls"].get(key, {})
                        if not acls_want:
                            val.update({"afi": afi, "name": key})
                            self.addcmd(val, "acls_name", True)
                    else:
                        val.update({"afi": afi, "name": key})
                        self.addcmd(val, "acls_name", True)

        if wantd:
            for k, want in wantd.items():  # for aft type ipv4 and ipv6
                want.update({"afi": k})
                self._compare(want=want, have=haved.pop(k, {}))

        if self.state in ["replaced", "overridden"] and self.commands:
            self.commands = self._rearrange_replace_overridden_config_cmd(
                self.commands
            )

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the acls network resource.
        """

        if want != have and self.state != "deleted":
            if want.get("acls"):
                afi = want["afi"]
                for acl_name, acl_data in want["acls"].items():
                    if (
                        have.get("acls") and acl_name in have["acls"]
                    ):  # for existing acl
                        cmd_len = len(self.commands)
                        have_acl = have["acls"].pop(acl_name, {})
                        if have_acl:
                            for key, val in acl_data.get("aces").items():
                                have_ace = have_acl["aces"].pop(key, {})
                                if val.get("protocol_options"):
                                    if not val.get("protocol") and (
                                        list(val.get("protocol_options"))[0]
                                        == have_ace.get("protocol")
                                    ):
                                        have_ace.pop("protocol")
                                if have_ace and val != have_ace:
                                    if self.state == "merged" and have_ace.get(
                                        "sequence"
                                    ) == val.get("sequence"):
                                        self._module.fail_json(
                                            "Cannot update existing sequence {0} of ACLs {1} with state merged.".format(
                                                val.get("sequence"), acl_name
                                            )
                                            + " Please use state replaced or overridden."
                                        )
                                    self.compare(
                                        parsers="aces",
                                        want=dict(),
                                        have={"aces": have_ace, "afi": afi},
                                    )
                                    self.compare(
                                        parsers="aces",
                                        want={
                                            "aces": val,
                                            "afi": afi,
                                            "acl_type": acl_data.get(
                                                "acl_type"
                                            ),
                                        },
                                        have={"aces": have_ace, "afi": afi},
                                    )
                                elif not have_ace:
                                    self.compare(
                                        parsers="aces",
                                        want={"aces": val, "afi": afi},
                                        have=dict(),
                                    )
                        if (
                            self.state == "overridden"
                            or self.state == "replaced"
                        ):
                            if have_acl.get("aces"):
                                for key, val in have_acl["aces"].items():
                                    self.compare(
                                        parsers="aces",
                                        want=dict(),
                                        have={"aces": val, "afi": afi},
                                    )
                        if cmd_len != len(self.commands):
                            command = self.acl_name_config_cmd(
                                name=acl_name,
                                afi=afi,
                                acl_type=acl_data.get("acl_type"),
                            )
                            self.commands.insert(cmd_len, command)
                    else:  # for new acl
                        cmd_len = len(self.commands)
                        for k, val in acl_data.get("aces").items():
                            if val.get("remarks"):
                                for remark in val.get("remarks"):
                                    self.addcmd({"remarks": remark}, "remarks")
                            else:
                                self.compare(
                                    parsers="aces",
                                    want={
                                        "aces": val,
                                        "afi": afi,
                                        "acl_type": acl_data.get("acl_type"),
                                    },
                                    have=dict(),
                                )
                        if cmd_len != self.commands:
                            command = self.acl_name_config_cmd(
                                name=acl_name,
                                afi=afi,
                                acl_type=acl_data.get("acl_type"),
                            )
                            self.commands.insert(cmd_len, command)

    def acl_name_config_cmd(self, name, afi, acl_type):
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

    def _rearrange_replace_overridden_config_cmd(self, commands):
        """This function rearranges the config command for replace
           and overridden state. It'll place all ACL negate cmd first
           and then will place ACL config cmd with all negated ACE first
           and then the config ACEs cmds.
        """
        temp_acl_config = []
        acl = 0
        ace_config = False
        for cmd in commands:
            if "no ip access-list" in cmd or "no ipv6 access-list" in cmd:
                temp_acl_config.insert(0, cmd)
                ace_config = False
            elif "access-list" in cmd and "no" not in cmd:
                temp_acl_config.insert(acl, cmd)
                ace_config = False
            elif "no" in cmd and "access-list" not in cmd:
                if ace_config:
                    ace = len(temp_acl_config) - 1
                else:
                    ace = len(temp_acl_config)
                temp_acl_config.insert(ace, cmd)
            elif "no" not in cmd and "access-list" not in cmd:
                ace_config = True
                temp_acl_config.insert(acl, cmd)
                ace = len(temp_acl_config)
            acl += 1
        return temp_acl_config

    def list_to_dict(self, param):
        temp, count = dict(), 0
        if param:
            for each in param:  # ipv4 and ipv6 acl
                temp_acls = {}
                if each.get("acls"):
                    for acl in each.get("acls"):  # check each acl for aces
                        temp_aces = {}
                        if acl.get("aces"):
                            temp_rem = (
                                []
                            )  # holds remarks if defined within a ace
                            for ace in acl.get(
                                "aces"
                            ):  # each ace turned to dict
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
                                                    ks
                                                )
                                            )

                                if ace.get("remarks"):
                                    en_name = str(acl.get("name")) + "remark"
                                    temp_rem.extend(ace.pop("remarks"))

                                if ace.get("sequence"):
                                    temp_aces.update(
                                        {ace.get("sequence"): ace}
                                    )
                                elif ace:
                                    count += 1
                                    temp_aces.update({"_" + str(count): ace})

                            if temp_rem:  # add remarks to the temp ace
                                temp_aces.update(
                                    {en_name: {"remarks": temp_rem}}
                                )

                        if acl.get(
                            "acl_type"
                        ):  # update acl dict with req info
                            temp_acls.update(
                                {
                                    acl.get("name"): {
                                        "aces": temp_aces,
                                        "acl_type": acl["acl_type"],
                                    }
                                }
                            )
                        else:  # if no acl type then here eg: ipv6
                            temp_acls.update(
                                {acl.get("name"): {"aces": temp_aces}}
                            )
                each["acls"] = temp_acls
                temp.update({each["afi"]: {"acls": temp_acls}})
            return temp
