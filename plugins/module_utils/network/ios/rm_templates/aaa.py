# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Aaa parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


# the methods of a list, "group ISE" is one method
_METHODS = r"(?P<methods>(?:\s\S+)*)\s*$"


def _list_command(data):
    """aaa <section> <type> [<level>] <name> [<record>] <methods>"""
    words = ["aaa", data["section"], data["type"]]
    if data.get("level") is not None:
        words.append(str(data["level"]))
    words.append(data["name"])
    if data["section"] == "accounting":
        words.append(data["record"])
    words.extend(data.get("methods") or [])
    return " ".join(words)


def _list_removal(data):
    words = ["aaa", data["section"], data["type"]]
    if data.get("level") is not None:
        words.append(str(data["level"]))
    words.append(data["name"])
    return " ".join(words)


def _source_interface(data):
    return "ip {0} source-interface {1}".format(data["type"].rstrip("+"), data["source_interface"])


def _client(data):
    command = "client " + data["address"]
    if data.get("vrf"):
        command += " vrf " + data["vrf"]
    key = data.get("server_key")
    if key and key.get("key"):
        command += " server-key"
        if key.get("type"):
            command += " " + str(key["type"])
        command += " " + key["key"]
    return command


def _client_removal(data):
    command = "client " + data["address"]
    if data.get("vrf"):
        command += " vrf " + data["vrf"]
    return command


def _list_parser(name, section, types, extra="", record=False):
    """Parser of a method list line: aaa <section> <type> [<extra>] <list> [<record>] <methods>"""
    record_re = r"\s(?P<record>start-stop|stop-only|none)" if record else ""
    result_entry = {"name": "{{ lname }}", "methods": "{{ methods | trim }}"}
    if record:
        result_entry["record"] = "{{ record }}"
    key = "{{ lname }}"
    if extra:
        result_entry["level"] = "{{ level | int }}"
        key = "{{ level }} {{ lname }}"
    return {
        "name": name,
        "getval": re.compile(
            r"^aaa\s{0}\s(?P<atype>{1}){2}\s(?P<lname>\S+){3}{4}".format(
                section,
                types,
                extra,
                record_re,
                _METHODS,
            ),
        ),
        "setval": _list_command,
        "remval": _list_removal,
        "result": {section: {"{{ atype }}": {key: result_entry}}},
    }


class AaaTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(AaaTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "new_model",
            "getval": re.compile(r"^aaa\snew-model$"),
            "setval": "aaa new-model",
            "result": {"new_model": True},
        },
        {
            "name": "session_id",
            "getval": re.compile(r"^aaa\ssession-id\s(?P<session_id>common|unique)$"),
            "setval": "aaa session-id {{ session_id }}",
            "result": {"session_id": "{{ session_id }}"},
        },
        {
            "name": "authorization_config_commands",
            "getval": re.compile(r"^aaa\sauthorization\sconfig-commands$"),
            "setval": "aaa authorization config-commands",
            "compval": "authorization.config_commands",
            "result": {"authorization": {"config_commands": True}},
        },
        {
            "name": "authorization_console",
            "getval": re.compile(r"^aaa\sauthorization\sconsole$"),
            "setval": "aaa authorization console",
            "compval": "authorization.console",
            "result": {"authorization": {"console": True}},
        },
        _list_parser("authentication_list", "authentication", "login|enable|dot1x"),
        _list_parser("authorization_list", "authorization", "exec|network"),
        _list_parser("authorization_commands", "authorization", "commands", extra=r"\s(?P<level>\d+)"),
        _list_parser("accounting_list", "accounting", "exec|system|dot1x|network|identity", record=True),
        _list_parser("accounting_commands", "accounting", "commands", extra=r"\s(?P<level>\d+)", record=True),
        {
            "name": "group_server",
            "getval": re.compile(r"^aaa\sgroup\sserver\s(?P<type>radius|tacacs\+)\s(?P<gname>\S+)$"),
            "setval": "aaa group server {{ type }} {{ name }}",
            "result": {
                "group_servers": {
                    "{{ type }} {{ gname }}": {"type": "{{ type }}", "name": "{{ gname }}"},
                },
            },
            "shared": True,
        },
        {
            "name": "group_server_server",
            "getval": re.compile(r"^\sserver\sname\s(?P<server>\S+)$"),
            "setval": "server name {{ server }}",
            "result": {
                "group_servers": {
                    "{{ type }} {{ gname }}": {"servers": {"{{ server }}": {"name": "{{ server }}"}}},
                },
            },
        },
        {
            "name": "group_server_source_interface",
            "getval": re.compile(r"^\sip\s(?:radius|tacacs)\ssource-interface\s(?P<source_interface>\S+)$"),
            "setval": _source_interface,
            "remval": lambda data: "ip {0} source-interface".format(data["type"].rstrip("+")),
            "result": {
                "group_servers": {
                    "{{ type }} {{ gname }}": {"source_interface": "{{ source_interface }}"},
                },
            },
        },
        {
            "name": "group_server_vrf",
            "getval": re.compile(r"^\sip\svrf\sforwarding\s(?P<vrf>\S+)$"),
            "setval": "ip vrf forwarding {{ vrf }}",
            "remval": "ip vrf forwarding",
            "result": {"group_servers": {"{{ type }} {{ gname }}": {"vrf": "{{ vrf }}"}}},
        },
        {
            "name": "group_server_deadtime",
            "getval": re.compile(r"^\sdeadtime\s(?P<deadtime>\d+)$"),
            "setval": "deadtime {{ deadtime }}",
            "remval": "deadtime",
            "result": {"group_servers": {"{{ type }} {{ gname }}": {"deadtime": "{{ deadtime | int }}"}}},
        },
        {
            "name": "dynamic_author",
            "getval": re.compile(r"^aaa\sserver\sradius\sdynamic-author$"),
            "setval": "aaa server radius dynamic-author",
            "result": {},
            "shared": True,
        },
        {
            "name": "dynamic_author_client",
            "getval": re.compile(
                r"""^\sclient\s(?P<address>\S+)
                    (?:\svrf\s(?P<vrf>\S+))?
                    (?:\sserver-key(?:\s(?P<key_type>[067]))?\s(?P<key_value>\S+))?
                    (?:\s\S.*)?$""",
                re.VERBOSE,
            ),
            "setval": _client,
            "remval": _client_removal,
            "result": {
                "dynamic_author": {
                    "clients": {
                        "{{ address }}": {
                            "address": "{{ address }}",
                            "vrf": "{{ vrf }}",
                            "key_type": "{{ key_type }}",
                            "key_value": "{{ key_value }}",
                        },
                    },
                },
            },
        },
        {
            # the other aaa commands: their children must not end up on the previous group
            "name": "unsupported",
            "getval": re.compile(r"^aaa\s(?P<type>)(?P<gname>)\S.*$"),
            "setval": "",
            "result": {},
            "shared": True,
        },
    ]
    # fmt: on
