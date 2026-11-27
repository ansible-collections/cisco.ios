# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_aaa config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.aaa import (
    AaaTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


# the method lists of each section, in the order of the commands
LISTS = (
    ("authentication", ("login", "enable", "dot1x")),
    ("authorization", ("exec", "network", "commands")),
    ("accounting", ("exec", "system", "dot1x", "network", "identity", "commands")),
)
PARSERS = {
    ("authentication", None): "authentication_list",
    ("authorization", None): "authorization_list",
    ("authorization", "commands"): "authorization_commands",
    ("accounting", None): "accounting_list",
    ("accounting", "commands"): "accounting_commands",
}
FLAGS = {"config_commands": "authorization_config_commands", "console": "authorization_console"}
DYNAMIC_AUTHOR = "dynamic_author"


class Aaa(ResourceModule):
    """
    The ios_aaa config class
    """

    def __init__(self, module):
        super(Aaa, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="aaa",
            tmplt=AaaTemplate(),
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

    # ------------------------------------------------------------------ preparation
    def _prepare(self, config):
        """The configuration as dicts keyed by what names an item."""
        config = deepcopy(config) or {}
        lists = {}
        for section, kinds in LISTS:
            for kind in kinds:
                for entry in (config.get(section) or {}).get(kind) or []:
                    level = entry.get("level") if kind == "commands" else None
                    lists[(section, kind, level, entry["name"])] = {
                        "section": section,
                        "type": kind,
                        "level": level,
                        "name": entry["name"],
                        "record": entry.get("record"),
                        "methods": list(entry.get("methods") or []),
                    }
        groups = {}
        for group in config.get("group_servers") or []:
            group["servers"] = list(group.get("servers") or [])
            groups[(group["type"], group["name"])] = group
        clients = {
            c["address"]: c for c in (config.get("dynamic_author") or {}).get("clients") or []
        }
        authorization = config.get("authorization") or {}
        return {
            "new_model": config.get("new_model"),
            "session_id": config.get("session_id"),
            "flags": {name: authorization.get(name) for name in FLAGS},
            "lists": lists,
            "groups": groups,
            "clients": clients,
            # what the task has, overridden only touches these
            "kinds": {(key[0], key[1]) for key in lists},
            "has_groups": bool(groups),
            "has_clients": bool(clients),
        }

    # ------------------------------------------------------------------ commands
    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        want = self._prepare(self.want)
        have = self._prepare(self.have)
        self._align_source_interfaces(want["groups"], have["groups"])
        removals = []

        if self.state == "deleted":
            self._deleted(want, have, removals)
        else:
            self._compare_scalars(want, have)
            self._compare_groups(want, have, removals)
            self._compare_clients(want, have, removals)
            self._compare_lists(want, have, removals)
        # what is removed goes last: lists before the groups they use, then the clients
        self.commands.extend(removals)

    def _compare_scalars(self, want, have):
        """new_model, session_id and the flags are only changed when they are in the task."""
        wanted = {
            "new_model": want["new_model"] if want["new_model"] is not None else have["new_model"],
            "session_id": (
                want["session_id"] if want["session_id"] is not None else have["session_id"]
            ),
            "authorization": {
                name: value if value is not None else have["flags"][name]
                for name, value in want["flags"].items()
            },
        }
        haved = {
            "new_model": have["new_model"],
            "session_id": have["session_id"],
            "authorization": have["flags"],
        }
        self.compare(
            parsers=[
                "new_model",
                "session_id",
                "authorization_config_commands",
                "authorization_console",
            ],
            want=wanted,
            have=haved,
        )

    def _compare_lists(self, want, have, removals):
        for key, entry in want["lists"].items():
            if not entry["methods"] and entry["record"] != "none":
                self._module.fail_json(msg="%s: the methods are required." % self._describe(key))
            if entry["section"] == "accounting" and not entry["record"]:
                self._module.fail_json(msg="%s: record is required." % self._describe(key))
            current = have["lists"].get(key)
            if (
                current is None
                or current["methods"] != entry["methods"]
                or current["record"] != entry["record"]
            ):
                self.addcmd(entry, self._parser(entry), False)
        if self.state == "overridden":
            for key, entry in have["lists"].items():
                if key not in want["lists"] and (key[0], key[1]) in want["kinds"]:
                    removals.append(self._tmplt.render(entry, self._parser(entry), True))

    @staticmethod
    def _parser(entry):
        kind = "commands" if entry["type"] == "commands" else None
        return PARSERS[(entry["section"], kind)]

    @staticmethod
    def _describe(key):
        section, kind, level, name = key
        return "aaa %s %s%s %s" % (section, kind, " %s" % level if level is not None else "", name)

    # ------------------------------------------------------------------ group servers
    def _compare_groups(self, want, have, removals):
        for key, group in want["groups"].items():
            current = have["groups"].get(key)
            begin = len(self.commands)
            self._compare_group(group, current or {})
            if current is None or len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(group, "group_server", False))
        if self.state == "overridden" and want["has_groups"]:
            for key, group in have["groups"].items():
                if key not in want["groups"]:
                    removals.append(self._tmplt.render(group, "group_server", True))

    def _compare_group(self, want, have):
        data = {"type": want["type"], "name": want["name"]}
        merged = self.state == "merged"
        servers = want["servers"]
        current = have.get("servers") or []
        if merged:
            servers = current + [s for s in servers if s not in current]
        # the order is the order the servers are tried: change from where it differs
        common = 0
        while (
            common < len(servers) and common < len(current) and servers[common] == current[common]
        ):
            common += 1
        for server in current[common:]:
            self.addcmd(dict(data, server=server), "group_server_server", True)
        for server in servers[common:]:
            self.addcmd(dict(data, server=server), "group_server_server", False)
        for option, parser in (
            ("source_interface", "group_server_source_interface"),
            ("vrf", "group_server_vrf"),
            ("deadtime", "group_server_deadtime"),
        ):
            wanted, present = want.get(option), have.get(option)
            if wanted is not None and wanted != present:
                self.addcmd(dict(data, **{option: wanted}), parser, False)
            elif wanted is None and present is not None and not merged:
                self.addcmd(dict(data, **{option: present}), parser, True)

    @staticmethod
    def _align_source_interfaces(wanted, present):
        """ "Lo0" in the task and "Loopback0" on the device are the same interface,
        the device side takes the spelling of the task."""
        for key, group in wanted.items():
            name = group.get("source_interface")
            current = present.get(key, {}).get("source_interface")
            if name and current and normalize_interface(name) == normalize_interface(current):
                present[key]["source_interface"] = name

    # ------------------------------------------------------------------ dynamic author
    def _compare_clients(self, want, have, removals):
        header = self._tmplt.render({}, "dynamic_author", False)
        begin = len(self.commands)
        for address, client in want["clients"].items():
            current = have["clients"].get(address)
            if current is not None and (current.get("vrf") or None) != (client.get("vrf") or None):
                removals_first = self._tmplt.render(current, "dynamic_author_client", True)
                self.commands.append(removals_first)
                current = None
            if self._client_differs(client, current):
                self.addcmd(client, "dynamic_author_client", False)
        if len(self.commands) != begin:
            self.commands.insert(begin, header)
        if self.state == "overridden" and want["has_clients"]:
            gone = [c for a, c in have["clients"].items() if a not in want["clients"]]
            if gone:
                removals.append(header)
                removals.extend(self._tmplt.render(c, "dynamic_author_client", True) for c in gone)

    @staticmethod
    def _client_differs(want, have):
        """The device keeps the key encrypted, a plain text key cannot be compared with it:
        it is sent for a client that is new or has no key, a key of type 6 or 7 is compared."""
        if have is None:
            return True
        key = want.get("server_key")
        if not key:
            return False
        current = have.get("server_key")
        if not key.get("type"):
            return current is None
        return not current or (current["type"], current["key"]) != (key["type"], key["key"])

    # ------------------------------------------------------------------ deleted
    def _deleted(self, want, have, removals):
        everything = not self.want
        for key, entry in have["lists"].items():
            if key in want["lists"] or (everything and entry["name"] != "default"):
                # the default lists decide how the logins work, they are removed when the task names them
                removals.append(self._tmplt.render(entry, self._parser(entry), True))
        for key, group in have["groups"].items():
            if everything or key in want["groups"]:
                removals.append(self._tmplt.render(group, "group_server", True))
        if everything and have["clients"]:
            removals.append(self._tmplt.render({}, "dynamic_author", True))
        elif want["clients"]:
            gone = [c for a, c in have["clients"].items() if a in want["clients"]]
            if gone and len(gone) == len(have["clients"]):
                # IOS keeps the empty block when the last client goes
                removals.append(self._tmplt.render({}, "dynamic_author", True))
            elif gone:
                removals.append(self._tmplt.render({}, "dynamic_author", False))
                removals.extend(self._tmplt.render(c, "dynamic_author_client", True) for c in gone)
        for name, parser in FLAGS.items():
            if want["flags"][name] and have["flags"][name]:
                removals.append(self._tmplt.render({}, parser, True))
