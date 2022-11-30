# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The L2_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class L2_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "access.vlan",
            "getval": re.compile(
                r"""
                \s+switchport\saccess\svlan\s(?P<vlan>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport access vlan {{ access.vlan }}",
            "remval": "switchport access vlan",
            "result": {
                "{{ name }}": {
                    "access": {
                        "vlan": "{{ vlan }}",
                    },
                },
            },
        },
        {
            "name": "access.vlan_name",
            "getval": re.compile(
                r"""
                \s+switchport\saccess\svlan\sname\s(?P<vlan_name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport access vlan name {{ access.vlan_name }}",
            "result": {
                "{{ name }}": {
                    "access": {
                        "vlan_name": "{{ vlan_name }}",
                    },
                },
            },
        },
        {
            "name": "voice.vlan",
            "getval": re.compile(
                r"""
                \s+switchport\svoice\svlan\s(?P<vlan>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport voice vlan {{ voice.vlan|string }}",
            "remval": "switchport voice vlan",
            "result": {
                "{{ name }}": {
                    "voice": {
                        "vlan": "{{ vlan }}",
                    },
                },
            },
        },
        {
            "name": "voice.vlan_tag",
            "getval": re.compile(
                r"""
                \s+switchport\svoice\svlan\s(?P<vlan_tag>dot1p|none|untagged)
                $""", re.VERBOSE,
            ),
            "setval": "switchport voice vlan {{ voice.vlan_tag }}",
            "remval": "switchport voice vlan",
            "result": {
                "{{ name }}": {
                    "voice": {
                        "vlan_tag": "{{ vlan_tag }}",
                    },
                },
            },
        },
        {
            "name": "voice.vlan_name",
            "getval": re.compile(
                r"""
                \s+switchport\svoice\svlan\sname\s(?P<vlan_name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport voice vlan name {{ voice.vlan_name }}",
            "result": {
                "{{ name }}": {
                    "voice": {
                        "vlan_name": "{{ vlan_name }}",
                    },
                },
            },
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                \s+switchport\smode\s(?P<mode>access|trunk|dynamic|dynamic\sauto|dynamic\sdesirable|private-vlan\shost|private-vlan\spromiscuous|private-vlan\strunk\ssecondary|dot1q-tunnel)
                $""", re.VERBOSE,
            ),
            "setval": "switchport mode "
                      "{{ 'trunk' if mode == 'trunk' }}"
                      "{{ 'access' if mode == 'access' }}"
                      "{{ 'dynamic' if mode == 'dynamic' }}"
                      "{{ 'dynamic desirable' if mode == 'dynamic_desirable' }}"
                      "{{ 'dynamic auto' if mode == 'dynamic_auto' }}"
                      "{{ 'dot1q-tunnel' if mode == 'dot1q_tunnel' }}"
                      "{{ 'private-vlan host' if mode == 'private_vlan_host' }}"
                      "{{ 'private-vlan promiscuous' if mode == 'private_vlan_promiscuous' }}"
                      "{{ 'private-vlan trunk secondary' if mode == 'private_vlan_trunk' }}",
            "remval": "switchport mode",
            "result": {
                "{{ name }}": {
                    "mode": "{{ mode }}",
                },
            },
        },
        {
            "name": "trunk.allowed_vlans",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\sallowed\svlan\s(?P<allowed_vlan>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "allowed_vlans": "{{ allowed_vlan.split(',') }}",
                    },
                },
            },
        },
        {
            "name": "trunk.allowed_vlans_add",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\sallowed\svlan\sadd\s(?P<allowed_vlans_add>\S+$)
                """, re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "allowed_vlans_add": ["{{ allowed_vlans_add.split(',') }}"],
                    },
                },
            },
        },
        {
            "name": "trunk.encapsulation",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\sencapsulation\s(?P<encapsulation>dot1q|isl|negotiate)
                $""", re.VERBOSE,
            ),
            "setval": "switchport trunk encapsulation {{ trunk.encapsulation }}",
            "remval": "switchport trunk encapsulation",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "encapsulation": "{{ encapsulation }}",
                    },
                },
            },
        },
        {
            "name": "trunk.native_vlan",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\snative\svlan\s(?P<native_vlan>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport trunk native vlan {{ trunk.native_vlan }}",
            "remval": "switchport trunk native vlan",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "native_vlan": "{{ native_vlan }}",
                    },
                },
            },
        },
        {
            "name": "trunk.pruning_vlans",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\spruning\svlan\s(?P<pruning_vlans>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "pruning_vlans": "{{ pruning_vlans.split(',') }}",
                    },
                },
            },
        },
        {
            "name": "trunk.pruning_vlans_add",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\spruning\svlan\sadd\s(?P<pruning_vlans_add>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ name }}": {
                    "trunk": {
                        "pruning_vlans_add": ["{{ pruning_vlans_add.split(',') }}"],
                    },
                },
            },
        },
    ]
    # fmt: on
