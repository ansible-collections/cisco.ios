# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Evpn_evi parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Evpn_eviTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Evpn_eviTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "evi",
            "getval": re.compile(
                r"""^l2vpn\sevpn\sinstance\s
                    (?P<evi>\d+)\svlan-based
                $""",
                re.VERBOSE,
            ),
            "setval": "l2vpn evpn instance {{ evi }} vlan-based",
            "result": {"{{ evi }}": {"evi": "{{ evi }}"}},
            "shared": True,
        },
        {
            "name": "default_gateway.advertise.enable",
            "getval": re.compile(
                r"""
                \s+default-gateway\sadvertise\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "default-gateway advertise enable",
            "result": {"{{ evi }}": {"default_gateway": {"advertise": {"enable": True}}}},
        },
        {
            "name": "default_gateway.advertise.disable",
            "getval": re.compile(
                r"""
                \s+default-gateway\sadvertise\sdisable
                $""",
                re.VERBOSE,
            ),
            "setval": "default-gateway advertise disable",
            "result": {"{{ evi }}": {"default_gateway": {"advertise": {"disable": True}}}},
        },
        {
            "name": "encapsulation",
            "getval": re.compile(
                r"""
                \s+encapsulation\s(?P<encapsulation>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "encapsulation {{encapsulation}}",
            "result": {"{{ evi }}": {"encapsulation": "{{ encapsulation }}"}},
        },
        {
            "name": "ip.local_learning.enable",
            "getval": re.compile(
                r"""
                \s+ip\slocal-learning\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "ip local-learning enable",
            "result": {"{{ evi }}": {"ip": {"local_learning": {"enable": True}}}},
        },
        {
            "name": "ip.local_learning.disable",
            "getval": re.compile(
                r"""
                \s+ip\slocal-learning\sdisable
                $""",
                re.VERBOSE,
            ),
            "setval": "ip local-learning disable",
            "result": {"{{ evi }}": {"ip": {"local_learning": {"disable": True}}}},
        },
        {
            "name": "replication_type",
            "getval": re.compile(
                r"""
                \s+replication-type\s(?P<replication_type>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "replication-type {{ replication_type }}",
            "result": {"{{ evi }}": {"replication_type": "{{ replication_type }}"}},
        },
        {
            "name": "route_distinguisher",
            "getval": re.compile(
                r"""
                \s+rd\s(?P<route_distinguisher>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "rd {{ route_distinguisher }}",
            "result": {"{{ evi }}": {"route_distinguisher": "{{ route_distinguisher }}"}},
        },
    ]
    # fmt: on
