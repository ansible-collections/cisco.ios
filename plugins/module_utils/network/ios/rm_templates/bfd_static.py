# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bfd_static parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Bfd_staticTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bfd_staticTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
                {
                    "name": "bfd_static_vrf",
                    "getval": re.compile(
                        r"""
                        ip\sroute\sstatic\sbfd\svrf\s(?P<vrf_name>\S+)\s(?P<destination>\S+)\s(?P<next_hop>\S+)
                        (\s(group\s(?P<group_name>\S+)|(?P<passive>passive)|(?P<log>log)|(?P<unassociate>unassociate)))*
                        $""", re.VERBOSE,
                    ),
                    "setval": "ip route static bfd vrf {{ vrf_name }} {{ destination }} {{ next_hop }}"
                            "{{ ' group ' + group_name if group_name is defined }}"
                            "{{ ' passive' if passive is defined }}"
                            "{{ ' log' if log is defined }}"
                            "{{ ' unassociate' if unassociate is defined }}",
                    "result": {
                        "bfd_static_routes": {
                            "vrf_routes": [
                                {
                                    "vrf_name": "{{ vrf_name }}",
                                    "destination": "{{ destination }}",
                                    "next_hop": "{{ next_hop }}",
                                    "group_name": "{{ group_name if group_name is defined }}",
                                    "passive": "{{ True if passive is defined else False }}",
                                    "log": "{{ True if log is defined else False }}",
                                    "unassociate": "{{ True if unassociate is defined else False }}",
                                },
                            ],
                        },
                    },
                    "shared": True,
                },
                {
                    "name": "bfd_static_vrf_src",
                    "getval": re.compile(
                        r"""
                        ^ip\sroute\sstatic\sbfd\svrf\s(?P<vrf_name>\S+)\s(?P<destination>\S+)\svrf\s(?P<src_vrf>\S+)\s(?P<src_ip>\S+)
                        (\s(group\s(?P<group_name>\S+)|(?P<passive>passive)|(?P<log>log)|(?P<unassociate>unassociate)))*
                        $""", re.VERBOSE,
                    ),
                    "setval": "ip route static bfd vrf {{ vrf_name }} {{ destination }} vrf {{ src_vrf }} {{ src_ip }}"
                            "{{ ' group ' + group_name if group_name is defined }}"
                            "{{ ' passive' if passive is defined }}"
                            "{{ ' log' if log is defined }}"
                            "{{ ' unassociate' if unassociate is defined }}",
                    "result": {
                        "bfd_static_routes": {
                            "vrf_src_routes": [
                                {
                                    "vrf_name": "{{ vrf_name }}",
                                    "destination": "{{ destination }}",
                                    "src_vrf": "{{ src_vrf }}",
                                    "src_ip": "{{ src_ip }}",
                                    "group_name": "{{ group_name if group_name is defined }}",
                                    "passive": "{{ True if passive is defined else False }}",
                                    "log": "{{ True if log is defined else False }}",
                                    "unassociate": "{{ True if unassociate is defined else False }}",
                                },
                            ],
                        },
                    },
                    "shared": True,
                },
                {
                    "name": "bfd_static_interface",
                    "getval": re.compile(
                        r"""
                        ^ip\sroute\sstatic\sbfd\s(?P<interface>\S+)\s(?P<destination>\S+)
                        (\s(group\s(?P<group_name>\S+)|(?P<passive>passive)|(?P<log>log)|(?P<unassociate>unassociate)))*
                        $""", re.VERBOSE,
                    ),
                    "setval": "ip route static bfd {{ interface }} {{ destination }}"
                            "{{ ' group ' + group_name if group_name is defined }}"
                            "{{ ' passive' if passive is defined }}"
                            "{{ ' log' if log is defined }}"
                            "{{ ' unassociate' if unassociate is defined }}",
                    "result": {
                        "bfd_static_routes": {
                            "interface_routes": [
                                {
                                    "interface": "{{ interface }}",
                                    "destination": "{{ destination }}",
                                    "group_name": "{{ group_name if group_name is defined }}",
                                    "passive": "{{ True if passive is defined else False }}",
                                    "log": "{{ True if log is defined else False }}",
                                    "unassociate": "{{ True if unassociate is defined else False }}",
                                },
                            ],
                        },
                    },
                    "shared": True,
                },

    ]
    # fmt: on
