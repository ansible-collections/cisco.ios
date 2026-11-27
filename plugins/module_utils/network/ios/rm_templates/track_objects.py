# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Track_objects parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ipaddress import ip_network

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_OBJ_ID = "{{ object_id }}"


def _ip_route_header(data):
    """Render the header of a tracked route, IOS wants the prefix as address and mask."""
    net = ip_network(data["ip_route"]["prefix"], strict=False)
    return "track {0} ip route {1} {2} reachability".format(
        data["object_id"],
        net.network_address,
        net.netmask,
    )


class Track_objectsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Track_objectsTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "object_id",
            "getval": re.compile(r"^track\s(?P<object_id>\d+)$"),
            "setval": "track {{ object_id }}",
            "result": {_OBJ_ID: {"object_id": "{{ object_id | int }}"}},
            "shared": True,
        },
        {
            "name": "interface",
            "getval": re.compile(
                r"""^track\s(?P<object_id>\d+)\sinterface\s(?P<name>\S+)
                    \s(?P<parameter>line-protocol|ip\srouting)$""",
                re.VERBOSE,
            ),
            "setval": "track {{ object_id }} interface {{ interface.name }} "
                      "{{ 'line-protocol' if interface.parameter == 'line_protocol' else 'ip routing' }}",
            "result": {
                _OBJ_ID: {
                    "object_id": "{{ object_id | int }}",
                    "interface": {
                        "name": "{{ name }}",
                        "parameter": "{{ 'line_protocol' if parameter == 'line-protocol' else 'ip_routing' }}",
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "ip_sla",
            "getval": re.compile(
                r"""^track\s(?P<object_id>\d+)\sip\ssla\s(?P<operation_id>\d+)
                    \s(?P<parameter>reachability|state)$""",
                re.VERBOSE,
            ),
            "setval": "track {{ object_id }} ip sla {{ ip_sla.operation_id }} {{ ip_sla.parameter }}",
            "result": {
                _OBJ_ID: {
                    "object_id": "{{ object_id | int }}",
                    "ip_sla": {
                        "operation_id": "{{ operation_id | int }}",
                        "parameter": "{{ parameter }}",
                    },
                },
            },
            "shared": True,
        },
        {
            # IOS prints "address mask", newer releases may print "address/length"
            "name": "ip_route",
            "getval": re.compile(
                r"""^track\s(?P<object_id>\d+)\sip\sroute
                    \s(?P<prefix>\d+\.\d+\.\d+\.\d+(?:/\d+)?)
                    (?:\s(?P<mask>\d+\.\d+\.\d+\.\d+))?
                    \sreachability$""",
                re.VERBOSE,
            ),
            "setval": _ip_route_header,
            "result": {
                _OBJ_ID: {
                    "object_id": "{{ object_id | int }}",
                    "ip_route": {"prefix": "{{ prefix }}", "mask": "{{ mask }}"},
                },
            },
            "shared": True,
        },
        {
            "name": "boolean_list",
            "getval": re.compile(
                r"^track\s(?P<object_id>\d+)\slist\sboolean\s(?P<operator>and|or)$",
            ),
            "setval": "track {{ object_id }} list boolean {{ boolean_list.operator }}",
            "result": {
                _OBJ_ID: {
                    "object_id": "{{ object_id | int }}",
                    "boolean_list": {"operator": "{{ operator }}"},
                },
            },
            "shared": True,
        },
        {
            # Last of the headers on purpose: whatever track type is not handled above, so that its
            # sub-commands are not attached to the previous object.
            "name": "unsupported_type",
            "getval": re.compile(r"^track\s(?P<object_id>\d+)\s\S.*$"),
            "setval": "",
            "result": {_OBJ_ID: {"object_id": "{{ object_id | int }}", "unsupported": True}},
            "shared": True,
        },
        {
            "name": "boolean_object",
            "getval": re.compile(r"^\sobject\s(?P<member>\d+)(?:\s(?P<negate>not))?$"),
            "setval": "object {{ member }}{{ ' not' if negate|default(false) else '' }}",
            "result": {
                _OBJ_ID: {
                    "boolean_list": {
                        "objects": [
                            {
                                "object_id": "{{ member | int }}",
                                "negate": "{{ True if negate is defined else False }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "vrf",
            "getval": re.compile(r"^\sip\svrf\s(?P<vrf>\S+)$"),
            "setval": "ip vrf {{ ip_route.vrf }}",
            "remval": "ip vrf {{ ip_route.vrf }}",
            "compval": "ip_route.vrf",
            "result": {_OBJ_ID: {"ip_route": {"vrf": "{{ vrf }}"}}},
        },
        {
            "name": "delay",
            "getval": re.compile(
                r"^\sdelay(?:\sdown\s(?P<down>\d+))?(?:\sup\s(?P<up>\d+))?$",
            ),
            "setval": "delay"
                      "{% if delay.down is defined %} down {{ delay.down }}{% endif %}"
                      "{% if delay.up is defined %} up {{ delay.up }}{% endif %}",
            "remval": "delay",
            "result": {
                _OBJ_ID: {
                    "delay": {
                        "down": "{{ down | int if down is defined }}",
                        "up": "{{ up | int if up is defined }}",
                    },
                },
            },
        },
    ]
    # fmt: on
