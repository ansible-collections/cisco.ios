#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_line config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.line import (
    LineTemplate,
)


class Line(ResourceModule):
    """
    The ios_line config class
    """

    def __init__(self, module):
        super(Line, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="line",
            tmplt=LineTemplate(),
        )
        self.parsers = {
            "line": ["line"],
            "access_classes_in": ["access_classes_in"],
            "access_classes_out": ["access_classes_out"],
            "accounting": [
                "accounting.arap",
                "accounting.commands",
                "accounting.connection",
                "accounting.exec",
                "accounting.resource",
            ],
            "authorization": [
                "authorization.arap",
                "authorization.commands",
                "authorization.exec",
                "authorization.reverse_access",
            ],
            "escape_character": ["escape_character"],
            "exec": [
                "exec.banner",
                "exec.character_bits",
                "exec.prompt.expand",
                "exec.prompt.timestamp",
                "exec.timeout",
            ],
            "length": ["length"],
            "location": ["location"],
            "logging": ["logging"],
            "login": ["login"],
            "logout_warning": ["logout_warning"],
            "motd": ["motd"],
            "notify": ["notify"],
            "padding": ["padding"],
            "parity": ["parity"],
            "password": ["password"],
            "privilege": ["privilege"],
            "session": [
                "session.disconnect_warning",
                "session.limit",
                "session.timeout",
            ],
            "speed": ["speed"],
            "stopbits": ["stopbits"],
            "transport": ["transport"],
        }

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
        wantd = deepcopy(self.want)
        wantd["lines"] = self._convert_list_to_dict(data=wantd.get("lines", []))
        haved = deepcopy(self.have)
        haved["lines"] = self._convert_list_to_dict(data=haved.get("lines", []))

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {"lines": {"con 0": {"name": "con 0"}, "vty 0 4": {"name": "vty 0 4"}}}

        # remove superfluous config
        if self.state in ["overridden", "deleted"]:
            for k, have in haved["lines"].items():
                if k not in wantd["lines"]:
                    self._compare(want={}, have=have)
        elif self.state in ["replaced"]:
            only_have_line_k = [k for k in haved["lines"].keys() if k not in wantd["lines"].keys()]
            for k in only_have_line_k:
                haved["lines"].pop(k)

        for k, want in wantd["lines"].items():
            self._compare(want=want, have=haved["lines"].pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Line network resource.
        """
        config_default = {
            "accounting": {
                "arap": "default",
                "connection": "default",
                "exec": "default",
                "resource": "default",
            },
            "authorization": {
                "arap": "default",
                "exec": "default",
                "reverse_access": "default",
            },
            "escape_character": {
                "value": "DEFAULT",
            },
            "exec": {
                "banner": True,
                "character_bits": 7,
                "timeout": "10",
            },
            "login": "default",
            "logout_warning": 20,
            "motd": True,
            "privilege": 1,
        }
        begin = len(self.commands)
        if want != {}:
            want = dict_merge(config_default, want)
            have = dict_merge(config_default, have)
            self._compare_lists(want=want, have=have)
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(want or have, "line", False))
        else:
            self.commands.insert(begin, self._tmplt.render(have, "line", True))

    def _compare_lists(self, want, have):
        p_lvl_1 = [
            "accounting",
            "authorization",
            "exec",
        ]
        # Take commands that have a subdict
        for l1 in p_lvl_1:
            l1_want = want.pop(l1, {})
            l1_have = have.pop(l1, {})
            for l1_key, l1_w_entry in l1_want.items():
                if l1_key == "prompt":
                    l1_h_entry = l1_have.pop(l1_key, {})
                    for p_key, p_w_entry in l1_w_entry.items():
                        p_h_entry = l1_h_entry.pop(p_key, {})
                        if p_w_entry != p_h_entry:
                            self.addcmd(
                                data={p_key: p_w_entry},
                                tmplt="{0}.{1}.{2}".format(l1, l1_key, p_key),
                                negate=False,
                            )
                    for p_key, p_h_entry in l1_h_entry.items():
                        self.addcmd(data={p_key: p_h_entry}, tmplt=self.parsers[l1], negate=True)
                elif l1_key == "commands":
                    l1_w_entry = self._convert_list_to_dict(data=l1_w_entry, key="level")
                    l1_h_entry = self._convert_list_to_dict(
                        data=l1_have.pop(l1_key, []),
                        key="level",
                    )
                    for c_key, c_w_entry in l1_w_entry.items():
                        c_h_entry = l1_h_entry.pop(c_key, {})
                        self.compare(
                            parsers=self.parsers[l1],
                            want={l1_key: c_w_entry},
                            have={l1_key: c_h_entry},
                        )
                    for c_key, cc_h_entry in l1_h_entry.items():
                        self.compare(
                            parsers=self.parsers[l1],
                            want={},
                            have={l1_key: c_h_entry},
                        )
                else:
                    l1_h_entry = l1_have.pop(l1_key, "")
                    self.compare(
                        parsers=self.parsers[l1],
                        want={l1: {l1_key: l1_w_entry}},
                        have={l1: {l1_key: l1_h_entry}},
                    )
            for l1_key, l1_h_entry in l1_have.items():
                if l1_key == "prompt":
                    for p_key, p_h_entry in l1_h_entry.items():
                        self.addcmd(
                            data={p_key: p_h_entry},
                            tmplt="{0}.{1}.{2}".format(l1, l1_key, p_key),
                            negate=True,
                        )
                elif l1_key == "commands":
                    l1_h_entry = self._convert_list_to_dict(data=l1_h_entry, key="level")
                    for c_key, c_h_entry in l1_h_entry.items():
                        self.compare(
                            parsers=self.parsers[l1],
                            want={},
                            have={l1_key: c_h_entry},
                        )
                else:
                    self.compare(
                        parsers=self.parsers[l1],
                        want={},
                        have={l1_key: l1_h_entry},
                    )

        # Take commands that didn't have a subdict
        for key, w_entry in want.items():
            if key == "name":
                continue
            if key == "transport":
                h_entry = have.pop(key, [])
                w_entry = self._convert_list_to_dict(data=w_entry)
                h_entry = self._convert_list_to_dict(data=h_entry)
                for t_key, t_w_entry in w_entry.items():
                    t_h_entry = h_entry.pop(t_key, {})
                    self.compare(
                        parsers=self.parsers[key],
                        want={key: t_w_entry},
                        have={key: t_h_entry},
                    )
            else:
                h_entry = have.pop(key, {})
                self.compare(parsers=self.parsers[key], want={key: w_entry}, have={key: h_entry})
        for key, h_entry in have.items():
            if key == "name":
                continue
            if key == "transport":
                h_entry = self._convert_list_to_dict(data=h_entry)
                for t_key, t_h_entry in h_entry.items():
                    self.compare(
                        parsers=self.parsers[key],
                        want={},
                        have={key: t_h_entry},
                    )
            else:
                self.compare(parsers=self.parsers[key], want={}, have={key: h_entry})

    def _convert_list_to_dict(self, data, key="name"):
        return {_k.get(key, ""): _k for _k in data} if data else {}
