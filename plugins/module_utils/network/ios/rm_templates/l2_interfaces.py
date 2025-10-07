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
            "name": "app_interface",
            "getval": re.compile(
                r"""
                \s+switchport\sapp-interface
                $""", re.VERBOSE,
            ),
            "setval": "switchport app-interface",
            "result": {
                "{{ name }}": {
                    "app_interface": True,
                },
            },
        },
        {
            "name": "nonegotiate",
            "getval": re.compile(
                r"""
                \s+switchport\snonegotiate
                $""", re.VERBOSE,
            ),
            "setval": "switchport nonegotiate",
            "result": {
                "{{ name }}": {
                    "nonegotiate": True,
                },
            },
        },
        {
            "name": "vepa",
            "getval": re.compile(
                r"""
                \s+switchport\svepa\senabled
                $""", re.VERBOSE,
            ),
            "setval": "switchport vepa enabled",
            "result": {
                "{{ name }}": {
                    "vepa": True,
                },
            },
        },
        {
            "name": "host",
            "getval": re.compile(
                r"""
                \s+switchport\shost
                $""", re.VERBOSE,
            ),
            "setval": "switchport host",
            "result": {
                "{{ name }}": {
                    "host": True,
                },
            },
        },
        {
            "name": "protected",
            "getval": re.compile(
                r"""
                \s+switchport\sprotected
                $""", re.VERBOSE,
            ),
            "setval": "switchport protected",
            "result": {
                "{{ name }}": {
                    "protected": True,
                },
            },
        },
        {
            "name": "block_options.multicast",
            "getval": re.compile(
                r"""
                \s+switchport\sblock\smulticast
                $""", re.VERBOSE,
            ),
            "setval": "switchport block multicast",
            "result": {
                "{{ name }}": {
                    "block_options": {
                        "multicast": True,
                    },
                },
            },
        },
        {
            "name": "block_options.unicast",
            "getval": re.compile(
                r"""
                \s+switchport\sblock\sunicast
                $""", re.VERBOSE,
            ),
            "setval": "switchport block unicast",
            "result": {
                "{{ name }}": {
                    "block_options": {
                        "unicast": True,
                    },
                },
            },
        },
        {
            "name": "spanning_tree.bpdufilter",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sbpdufilter
                (\s(?P<enabled>enabled))?
                (\s(?P<disabled>disabled))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bpdufilter"
                      "{{ ' enabled' if spanning_tree.bpdufilter.enabled|d(False) else ''}}"
                      "{{ ' disabled' if spanning_tree.bpdufilter.disabled|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "bpdufilter": {
                            "enabled": "{{ not not enabled }}",
                            "disabled": "{{ not not disabled }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.bpduguard",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sbpduguard
                (\s(?P<enabled>enabled))?
                (\s(?P<disabled>disabled))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bpduguard"
                      "{{ ' enabled' if spanning_tree.bpduguard.enabled|d(False) else ''}}"
                      "{{ ' disabled' if spanning_tree.bpduguard.disabled|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "bpduguard": {
                            "enabled": "{{ not not enabled }}",
                            "disabled": "{{ not not disabled }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.cost",
            "getval": re.compile(
                r"""
                \s+spanning-tree\scost
                (\s(?P<enabled>\d+))
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree cost {{ spanning_tree.cost }}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "cost": "{{ enabled }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.guard",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sguard
                (\s(?P<loop>loop))?
                (\s(?P<none>none))?
                (\s(?P<root>root))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree guard"
                      "{{ ' loop' if spanning_tree.guard.loop|d(False) else ''}}"
                      "{{ ' none' if spanning_tree.guard.none|d(False) else ''}}"
                      "{{ ' root' if spanning_tree.guard.root|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "guard": {
                            "loop": "{{ not not loop }}",
                            "none": "{{ not not none }}",
                            "root": "{{ not not root }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.link_type",
            "getval": re.compile(
                r"""
                \s+spanning-tree\slink-type
                (\s(?P<point_to_point>point-to-point))?
                (\s(?P<shared>shared))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree link-type"
                      "{{ ' point-to-point' if spanning_tree.link_type.point_to_point|d(False) else ''}}"
                      "{{ ' shared' if spanning_tree.link_type.shared|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "link_type": {
                            "point_to_point": "{{ not not point_to_point }}",
                            "shared": "{{ not not shared }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst",
            "getval": re.compile(
                r"""
                \s+spanning-tree\smst
                (\s(?P<instance_range>\d+|\d+-\d+))?
                (\scost\s(?P<cost>\d+))?
                (\sport-priority\s(?P<port_priority>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst"
                      "{{ ' ' + instance_range if spanning_tree.mst.instance_range else ''}}"
                      "{{ ' cost ' + cost if spanning_tree.mst.cost else ''}}"
                      "{{ ' port-priority ' + port_priority if spanning_tree.mst.port_priority else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "mst": {
                            "instance_range": "{{ instance_range }}",
                            "cost": "{{ cost }}",
                            "port_priority": "{{ port_priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.port_priority",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sport-priority\s(?P<port_priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree port-priority {{ spanning_tree.port_priority }}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "port_priority": "{{ port_priority }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.portfast",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sportfast
                (\s(?P<disabled>disabled))?
                (\s(?P<trunk>trunk))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast"
                      "{{ ' disabled' if spanning_tree.portfast.disabled|d(False) else ''}}"
                      "{{ ' trunk' if spanning_tree.portfast.trunk|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "portfast": {
                            "disabled": "{{ not not disabled }}",
                            "trunk": "{{ not not trunk }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.rootguard",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sbpduguard\srootguard
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bpduguard rootguard",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "rootguard": True,
                    },
                },
            },
        },
        {
            "name": "spanning_tree.vlan",
            "getval": re.compile(
                r"""
                \s+spanning-tree\svlan
                (\s(?P<instance_range>\d+|\d+-\d+))?
                (\scost\s(?P<cost>\d+))?
                (\sport-priority\s(?P<port_priority>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan"
                      "{{ ' ' + vlan_range if spanning_tree.vlan.vlan_range else ''}}"
                      "{{ ' cost ' + cost if spanning_tree.vlan.cost else ''}}"
                      "{{ ' port-priority ' + port_priority if spanning_tree.vlan.port_priority else ''}}",
            "result": {
                "{{ name }}": {
                    "spanning_tree": {
                        "vlan": {
                            "vlan_range": "{{ instance_range }}",
                            "cost": "{{ cost }}",
                            "port_priority": "{{ port_priority }}",
                        },
                    },
                },
            },
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
            "name": "private_vlan",
            "getval": re.compile(
                r"""
                ^\sswitchport\sprivate-vlan
                (\s(?P<association>association))?
                (\s(?P<host_association>host-association))?
                (\s(?P<host>host))?
                (\s(?P<mapping>mapping))?
                (\s(?P<primary_range>\d+))?
                (\s(?P<secondary_range>\d+))?
                (\s(?P<add>add))?
                (\s(?P<remove>remove))?
                (\s(?P<secondary_vlan_id>\S+))?
                \s*$""", re.VERBOSE,
            ),
            "setval": "switchport private-vlan"
            "{{ ' association' if private_vlan.association|d(False) else '' }}"
            "{{ ' host-association' if private_vlan.host_association|d(False) else '' }}"
            "{{ ' mapping' if private_vlan.mapping|d(False) else '' }}"
            "{{ ' host' if private_vlan.host|d(False) else '' }}"
            "{{ ' ' + private_vlan.primary_range|string if private_vlan.primary_range is defined else ''}}"
            "{{ ' ' + private_vlan.secondary_range|string if private_vlan.secondary_range is defined else ''}}"
            "{{ ' add' if private_vlan.add|d(False) else '' }}"
            "{{ ' remove' if private_vlan.remove|d(False) else '' }}"
            "{{ ' ' + private_vlan.secondary_vlan_id if private_vlan.secondary_vlan_id is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "private_vlan": {
                        "association": "{{ not not association }}",
                        "host_association": "{{ not not host_association }}",
                        "mapping": "{{ not not mapping }}",
                        "host": "{{ not not host }}",
                        "primary_range": "{{ primary_range }}",
                        "secondary_range": "{{ secondary_range }}",
                        "add": "{{ not not add }}",
                        "remove": "{{ not not remove }}",
                        "secondary_vlan_id": "{{ secondary_vlan_id }}",
                    },
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
