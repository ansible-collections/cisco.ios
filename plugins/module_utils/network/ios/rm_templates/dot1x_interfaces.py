# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Dot1x_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


# The facts parse one interface at a time, so the result needs no key per interface, and no template
# to render for it on every line. Every Jinja template that is rendered is compiled again, that is what
# makes parsing a switch with more than a thousand interfaces slow.
_NAME = "interface"
_AUTH = "authentication"


def _dash(value):
    return str(value).replace("_", "-")


def _port_control(data):
    return "authentication port-control " + _dash(data["authentication"]["port_control"])


def _reauthenticate(data):
    value = data["authentication"]["timer"]["reauthenticate"]
    return "authentication timer reauthenticate " + (
        "server" if value.get("server") else str(value["seconds"])
    )


def _host_mode(data):
    return "authentication host-mode " + _dash(data["authentication"]["host_mode"])


def _event_fail(data):
    fail = data["authentication"]["event"]["fail"]
    command = "authentication event fail"
    if fail.get("retry") is not None:
        command += " retry {0}".format(fail["retry"])
    if fail.get("action") == "next_method":
        return command + " action next-method"
    return command + " action authorize vlan {0}".format(fail["vlan"])


def server_dead_lines(dead):
    """The lines of "authentication event server dead": the vlan and the voice domain are lines of their own."""
    prefix = "authentication event server dead action "
    lines = []
    if dead.get("vlan") is not None:
        lines.append("{0}{1} vlan {2}".format(prefix, dead["action"], dead["vlan"]))
    if dead.get("voice"):
        lines.append(prefix + "authorize voice")
    return lines


def _event_server_dead(data):
    return server_dead_lines(data["authentication"]["event"]["server_dead"])


class Dot1x_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Dot1x_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(r"^interface\s(?P<name>\S+)\s*$"),
            "setval": "interface {{ name }}",
            "result": {_NAME: {"name": "{{ name }}"}},
        },
        {
            # "mab eap" is read as enabled as well, the module does not change the eap option
            "name": "mab",
            "getval": re.compile(r"^\s+mab(?:\s.*)?\s*$"),
            "setval": "mab",
            "result": {_NAME: {"mab": True}},
        },
        {
            "name": "dot1x_pae",
            "getval": re.compile(r"^\s+dot1x\spae\s(?P<pae>authenticator|supplicant|both)\s*$"),
            "setval": "dot1x pae {{ dot1x.pae }}",
            "compval": "dot1x.pae",
            "result": {_NAME: {"dot1x": {"pae": "{{ pae }}"}}},
        },
        {
            "name": "dot1x_tx_period",
            "getval": re.compile(r"^\s+dot1x\stimeout\stx-period\s(?P<tx_period>\d+)\s*$"),
            "setval": "dot1x timeout tx-period {{ dot1x.timeout.tx_period }}",
            "compval": "dot1x.timeout.tx_period",
            "result": {_NAME: {"dot1x": {"timeout": {"tx_period": "{{ tx_period }}"}}}},
        },
        {
            "name": "dot1x_max_reauth_req",
            "getval": re.compile(r"^\s+dot1x\smax-reauth-req\s(?P<max_reauth_req>\d+)\s*$"),
            "setval": "dot1x max-reauth-req {{ dot1x.max_reauth_req }}",
            "compval": "dot1x.max_reauth_req",
            "result": {_NAME: {"dot1x": {"max_reauth_req": "{{ max_reauth_req }}"}}},
        },
        {
            "name": "port_control",
            "getval": re.compile(r"^\s+authentication\sport-control\s(?P<value>auto|force-authorized|force-unauthorized)\s*$"),
            "setval": _port_control,
            "compval": "authentication.port_control",
            "result": {_NAME: {_AUTH: {"port_control": "{{ value | replace('-', '_') }}"}}},
        },
        {
            "name": "periodic",
            "getval": re.compile(r"^\s+authentication\speriodic\s*$"),
            "setval": "authentication periodic",
            "compval": "authentication.periodic",
            "result": {_NAME: {_AUTH: {"periodic": True}}},
        },
        {
            "name": "reauthenticate",
            "getval": re.compile(r"^\s+authentication\stimer\sreauthenticate\s(?:(?P<server>server)|(?P<seconds>\d+))\s*$"),
            "setval": _reauthenticate,
            "compval": "authentication.timer.reauthenticate",
            "result": {
                _NAME: {
                    _AUTH: {
                        "timer": {
                            "reauthenticate": {
                                "server": "{{ True if server is defined }}",
                                "seconds": "{{ seconds if seconds is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "violation",
            "getval": re.compile(r"^\s+authentication\sviolation\s(?P<violation>protect|replace|restrict|shutdown)\s*$"),
            "setval": "authentication violation {{ authentication.violation }}",
            "compval": "authentication.violation",
            "result": {_NAME: {_AUTH: {"violation": "{{ violation }}"}}},
        },
        {
            "name": "control_direction",
            "getval": re.compile(r"^\s+authentication\scontrol-direction\s(?P<direction>both|in)\s*$"),
            "setval": "authentication control-direction {{ authentication.control_direction }}",
            "compval": "authentication.control_direction",
            "result": {_NAME: {_AUTH: {"control_direction": "{{ direction }}"}}},
        },
        {
            "name": "host_mode",
            "getval": re.compile(r"^\s+authentication\shost-mode\s(?P<value>multi-auth|multi-domain|multi-host|single-host)\s*$"),
            "setval": _host_mode,
            "compval": "authentication.host_mode",
            "result": {_NAME: {_AUTH: {"host_mode": "{{ value | replace('-', '_') }}"}}},
        },
        {
            "name": "order",
            "getval": re.compile(r"^\s+authentication\sorder\s(?P<methods>(?:dot1x|mab|webauth)(?:\s(?:dot1x|mab|webauth))*)\s*$"),
            "setval": "authentication order {{ authentication.order | join(' ') }}",
            "compval": "authentication.order",
            "result": {_NAME: {_AUTH: {"order": "{{ methods.split() }}"}}},
        },
        {
            "name": "priority",
            "getval": re.compile(r"^\s+authentication\spriority\s(?P<methods>(?:dot1x|mab|webauth)(?:\s(?:dot1x|mab|webauth))*)\s*$"),
            "setval": "authentication priority {{ authentication.priority | join(' ') }}",
            "compval": "authentication.priority",
            "result": {_NAME: {_AUTH: {"priority": "{{ methods.split() }}"}}},
        },
        {
            "name": "event_fail",
            "getval": re.compile(
                r"^\s+authentication\sevent\sfail(?:\sretry\s(?P<retry>\d+))?\saction\s"
                r"(?:(?P<authorize>authorize)\svlan\s(?P<vlan>\d+)|(?P<next>next-method))\s*$",
            ),
            "setval": _event_fail,
            "compval": "authentication.event.fail",
            "result": {
                _NAME: {
                    _AUTH: {
                        "event": {
                            "fail": {
                                "retry": "{{ retry if retry is defined }}",
                                "action": "{{ 'authorize' if authorize is defined else 'next_method' }}",
                                "vlan": "{{ vlan if vlan is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "event_no_response",
            "getval": re.compile(r"^\s+authentication\sevent\sno-response\saction\sauthorize\svlan\s(?P<vlan>\d+)\s*$"),
            "setval": "authentication event no-response action authorize vlan {{ authentication.event.no_response.vlan }}",
            "compval": "authentication.event.no_response",
            "result": {_NAME: {_AUTH: {"event": {"no_response": {"vlan": "{{ vlan }}"}}}}},
        },
        {
            "name": "event_server_dead",
            "getval": re.compile(
                r"^\s+authentication\sevent\sserver\sdead\saction\s(?P<action>authorize|reinitialize)"
                r"(?:\svlan\s(?P<vlan>\d+)|\s(?P<voice>voice))?\s*$",
            ),
            "setval": _event_server_dead,
            "compval": "authentication.event.server_dead",
            "result": {
                _NAME: {
                    _AUTH: {
                        "event": {
                            "server_dead": {
                                "action": "{{ action }}",
                                "vlan": "{{ vlan if vlan is defined }}",
                                "voice": "{{ True if voice is defined }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "event_server_alive",
            "getval": re.compile(r"^\s+authentication\sevent\sserver\salive\saction\s(?P<action>reinitialize)\s*$"),
            "setval": "authentication event server alive action {{ authentication.event.server_alive.action }}",
            "compval": "authentication.event.server_alive",
            "result": {_NAME: {_AUTH: {"event": {"server_alive": {"action": "{{ action }}"}}}}},
        },
    ]
    # fmt: on
