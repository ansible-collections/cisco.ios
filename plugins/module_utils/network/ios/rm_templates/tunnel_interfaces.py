# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Tunnel_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_NAME = "{{ name }}"
_MODES = {"gre ip": "gre_ip", "gre ipv6": "gre_ipv6", "gre multipoint": "gre_multipoint"}


def _mode(data):
    return "tunnel mode " + {v: k for k, v in _MODES.items()}[data["mode"]]


def _option(name, regex, setval, value, remval=None):
    """Build the parser of a "tunnel <name>" line."""
    parser = {
        "name": name,
        "getval": re.compile(rf"^\s+tunnel\s{regex}$"),
        "setval": setval,
        "result": {_NAME: {name: value}},
    }
    if remval:
        parser["remval"] = remval
    return parser


class Tunnel_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Tunnel_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(r"^interface\s(?P<name>Tunnel\S+)$"),
            "setval": "interface {{ name }}",
            "result": {_NAME: {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            # any other interface: its children must not end up on the previous tunnel
            "name": "other_interface",
            "getval": re.compile(r"^interface\s(?P<other>\S+)$"),
            "setval": "",
            "result": {},
            "shared": True,
        },
        _option("source", r"source\s(?P<source>\S+)", "tunnel source {{ source }}", "{{ source }}", "tunnel source"),
        _option(
            "destination", r"destination\s(?P<destination>\S+)", "tunnel destination {{ destination }}",
            "{{ destination }}", "tunnel destination",
        ),
        {
            "name": "mode",
            "getval": re.compile(r"^\s+tunnel\smode\s(?P<mode>gre\s(?:ip|ipv6|multipoint))$"),
            "setval": _mode,
            "remval": "tunnel mode",
            "result": {_NAME: {"mode": "{{ mode.replace(' ', '_') }}"}},
        },
        {
            # e.g. "tunnel mode ipsec ipv4": the interface is not managed by this module
            "name": "unsupported_mode",
            "getval": re.compile(r"^\s+tunnel\smode\s(?!gre\s(?:ip|ipv6|multipoint)$)(?P<other>\S.*)$"),
            "setval": "",
            "result": {_NAME: {"unsupported": True}},
        },
        _option("key", r"key\s(?P<key>\d+)", "tunnel key {{ key }}", "{{ key | int }}", "tunnel key"),
        _option("vrf", r"vrf\s(?P<vrf>\S+)", "tunnel vrf {{ vrf }}", "{{ vrf }}", "tunnel vrf {{ vrf }}"),
        _option("ttl", r"ttl\s(?P<ttl>\d+)", "tunnel ttl {{ ttl }}", "{{ ttl | int }}", "tunnel ttl"),
        _option("checksum", r"(?P<checksum>checksum)", "tunnel checksum", "{{ True }}"),
        _option(
            "path_mtu_discovery", r"(?P<path_mtu_discovery>path-mtu-discovery)(?:\s\S.*)?", "tunnel path-mtu-discovery",
            "{{ True }}",
        ),
    ]
    # fmt: on
