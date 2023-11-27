# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Evpn_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Evpn_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Evpn_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "default_gateway.advertise",
            "getval": re.compile(
                r"""
                \sdefault-gateway\sadvertise
                $""",
                re.VERBOSE,
            ),
            "setval": "default-gateway advertise",
            "result": {"default_gateway": {"advertise": True}},
        },
        {
            "name": "flooding_suppression.address_resolution.disable",
            "getval": re.compile(
                r"""
                \sflooding-suppression\saddress-resolution\sdisable
                $""",
                re.VERBOSE,
            ),
            "setval": "flooding-suppression address-resolution disable",
            "result": {
                "flooding_suppression": {
                    "address_resolution": {
                        "disable": True,
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "ip.local_learning.disable",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\sdisable
                $""",
                re.VERBOSE,
            ),
            "setval": "ip local-learning disable",
            "result": {
                "ip": {
                    "local_learning": {
                        "disable": True,
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "replication_type",
            "getval": re.compile(
                r"""
                \sreplication-type\s(?P<replication_type>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "replication-type {{replication_type}}",
            "result": {"replication_type": "{{replication_type}}"},
            "shared": True,
        },
        {
            "name": "route_target.auto.vni",
            "getval": re.compile(
                r"""
                \sroute-target\sauto\svni
                $""",
                re.VERBOSE,
            ),
            "setval": "route-target auto vni",
            "result": {"route_target": {"auto": {"vni": True}}},
            "shared": True,
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""
                \srouter-id\s(?P<router_id>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "router-id {{ router_id }}",
            "result": {"router_id": "{{router_id}}"},
            "shared": True,
        },
    ]
    # fmt: on
