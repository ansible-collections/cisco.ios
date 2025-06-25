# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(InterfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            'name': 'interface',
            'getval': re.compile(
                r'''
              ^interface\s
              (?P<name>\S+)$''', re.VERBOSE,
            ),
            'setval': 'interface {{ name }}',
            'result': {
                '{{ name }}': {
                    'name': '{{ name }}',
                    'enabled': True,
                },
            },
            'shared': True,
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s(?P<description>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                '{{ name }}': {
                    'description': "'{{ description }}'",
                },
            },
        },
        {
            "name": "enabled",
            "getval": re.compile(
                r"""
                (?P<negate>\sno)?
                (?P<shutdown>\sshutdown)
                $""", re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                '{{ name }}': {
                    'enabled': "{{ False if shutdown is defined and negate is not defined else True }}",
                },
            },
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""
                \s+mac-address
                (\s(?P<mac_address>.+))
                $""", re.VERBOSE,
            ),
            "setval": "mac-address {{ mac_address }}",
            "result": {
                '{{ name }}': {
                    'mac_address': "{{ mac_address }}",
                },
            },
        },
        {
            "name": "service_policy.input",
            "getval": re.compile(
                r"""
                \s+service-policy\sinput
                (\s(?P<enabled>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy input {{ service_policy.input }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "input": "{{ enabled }}",
                    },
                },
            },
        },
        {
            "name": "service_policy.output",
            "getval": re.compile(
                r"""
                \s+service-policy\soutput
                (\s(?P<enabled>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy output {{ service_policy.output }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "output": "{{ enabled }}",
                    },
                },
            },
        },
        {
            "name": "service_policy.type_options.access_control",
            "getval": re.compile(
                r"""
                \s+service-policy\stype\saccess-control
                (\sinput\s(?P<input>\S+))?
                (\soutput\s(?P<output>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy type access-control"
                      "{{ service_policy.type_options.access_control.input if service_policy.type_options.access_control.input is defined else '' }}"
                      "{{ service_policy.type_options.access_control.output if service_policy.type_options.access_control.output is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "type_options": {
                            "access_control": {
                                "input": "{{ input }}",
                                "output": "{{ output }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "service_policy.type_options.epbr",
            "getval": re.compile(
                r"""
                \s+service-policy\stype\sepbr
                (\sinput\s(?P<input>\S+))?
                (\soutput\s(?P<output>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy type epbr"
                      "{{ service_policy.type_options.epbr.input if service_policy.type_options.epbr.input is defined else '' }}"
                      "{{ service_policy.type_options.epbr.output if service_policy.type_options.epbr.output is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "type_options": {
                            "epbr": {
                                "input": "{{ input }}",
                                "output": "{{ output }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "service_policy.type_options.nwpi",
            "getval": re.compile(
                r"""
                \s+service-policy\stype\snwpi
                (\sinput\s(?P<input>\S+))?
                (\soutput\s(?P<output>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy type nwpi"
                      "{{ service_policy.type_options.nwpi.input if service_policy.type_options.nwpi.input is defined else '' }}"
                      "{{ service_policy.type_options.nwpi.output if service_policy.type_options.nwpi.output is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "type_options": {
                            "nwpi": {
                                "input": "{{ input }}",
                                "output": "{{ output }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "service_policy.type_options.packet_service",
            "getval": re.compile(
                r"""
                \s+service-policy\stype\spacket-service
                (\sinput\s(?P<input>\S+))?
                (\soutput\s(?P<output>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy type packet-service"
                      "{{ service_policy.type_options.packet_service.input if service_policy.type_options.packet_service.input is defined else '' }}"
                      "{{ service_policy.type_options.packet_service.output if service_policy.type_options.packet_service.output is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "type_options": {
                            "packet_service": {
                                "input": "{{ input }}",
                                "output": "{{ output }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "service_policy.type_options.service_chain",
            "getval": re.compile(
                r"""
                \s+service-policy\stype\sservice-chain
                (\sinput\s(?P<input>\S+))?
                (\soutput\s(?P<output>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "service-policy type service-chain"
                      "{{ service_policy.type_options.service_chain.input if service_policy.type_options.service_chain.input is defined else '' }}"
                      "{{ service_policy.type_options.service_chain.output if service_policy.type_options.service_chain.output is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "service_policy": {
                        "type_options": {
                            "service_chain": {
                                "input": "{{ input }}",
                                "output": "{{ output }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "logging.trunk_status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\strunk-status
                $""", re.VERBOSE,
            ),
            "setval": "logging event trunk-status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "trunk_status": True,
                    },
                },
            },
        },
        {
            "name": "logging.subif_link_status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\ssubif-link-status
                $""", re.VERBOSE,
            ),
            "setval": "logging event subif-link-status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "subif_link_status": True,
                    },
                },
            },
        },
        {
            "name": "logging.status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\sstatus
                $""", re.VERBOSE,
            ),
            "setval": "logging event status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "status": True,
                    },
                },
            },
        },
        {
            "name": "logging.spanning_tree",
            "getval": re.compile(
                r"""
                \s+logging\sevent\sspanning-tree
                $""", re.VERBOSE,
            ),
            "setval": "logging event spanning-tree",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "spanning_tree": True,
                    },
                },
            },
        },
        {
            "name": "logging.nfas_status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\snfas-status
                $""", re.VERBOSE,
            ),
            "setval": "logging event nfas-status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "nfas_status": True,
                    },
                },
            },
        },
        {
            "name": "logging.bundle_status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\sbundle-status
                $""", re.VERBOSE,
            ),
            "setval": "logging event bundle-status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "bundle_status": True,
                    },
                },
            },
        },
        {
            "name": "logging.link_status",
            "getval": re.compile(
                r"""
                \s+logging\sevent\slink-status
                $""", re.VERBOSE,
            ),
            "setval": "logging event link-status",
            "result": {
                "{{ name }}": {
                    "logging": {
                        "link_status": True,
                    },
                },
            },
        },
        {
            "name": "snmp.trap",
            "getval": re.compile(
                r"""
                \s+snmp\strap
                (\s(?P<ip>ip\sverify\sdrop-rate))?
                (\s(?P<link_status>link-status\spermit\sduplicates))?
                (\s(?P<mac_notification_added>mac-notification-added))?
                (\s(?P<mac_notification_removed>mac-notification-removed))?
                $""", re.VERBOSE,
            ),
            "setval": "snmp trap"
                      "{{ ' ip verify drop-rate' if snmp.trap.ip is defined else '' }}"
                      "{{ ' link-status permit duplicates' if snmp.trap.link_status is defined else '' }}"
                      "{{ ' mac-notification-added' if snmp.trap.mac_notification_added is defined else '' }}"
                      "{{ ' mac-notification-removed' if snmp.trap.mac_notification_removed is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "snmp": {
                        "trap": {
                            "ip": "{{ not not ip }}",
                            "link_status": "{{ not not link_status }}",
                            "mac_notification_added": "{{ not not mac_notification_added }}",
                            "mac_notification_removed": "{{ not not mac_notification_removed }}",
                        },
                    },
                },
            },
        },
        {
            "name": "snmp.ifindex",
            "getval": re.compile(
                r"""
                \s+snmp\sifindex
                (\s(?P<clear>clear))?
                (\s(?P<persist>persist))?
                $""", re.VERBOSE,
            ),
            "setval": "snmp ifindex"
                      "{{ ' clear' if snmp.ifindex.clear is defined else '' }}"
                      "{{ ' persist' if snmp.ifindex.persist is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "snmp": {
                        "ifindex": {
                            "clear": "{{ not not clear }}",
                            "persist": "{{ not not persist }}",
                        },
                    },
                },
            },
        },
        {  # only applicable for switches
            "name": "mode",
            "getval": re.compile(
                r"""
                (?P<negate>\sno)?
                (?P<switchport>\sswitchport)
                $""", re.VERBOSE,
            ),
            "setval": "switchport",
            "result": {
                '{{ name }}': {
                    'mode': "{{ 'layer2' if switchport is defined and negate is not defined else 'layer3' }}",
                },
            },
        },
        {
            "name": "speed",
            "getval": re.compile(
                r"""
                \s+speed\s(?P<speed>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "speed {{ speed|string }}",
            "result": {
                '{{ name }}': {
                    'speed': '{{ speed }}',
                },
            },
        },
        {
            "name": "mtu",
            "getval": re.compile(
                r"""
                \s+mtu\s(?P<mtu>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "mtu {{ mtu|string }}",
            "result": {
                '{{ name }}': {
                    'mtu': '{{ mtu }}',
                },
            },
        },
        {
            "name": "duplex",
            "getval": re.compile(
                r"""
                \s+duplex\s(?P<duplex>full|half|auto)
                $""", re.VERBOSE,
            ),
            "setval": "duplex {{ duplex }}",
            "result": {
                '{{ name }}': {
                    'duplex': '{{ duplex }}',
                },
            },
        },
        {
            "name": "template",
            "getval": re.compile(
                r"""
                \s+source\stemplate\s(?P<template>.+$)
                """, re.VERBOSE,
            ),
            "setval": "source template {{ template }}",
            "result": {
                '{{ name }}': {
                    'template': '{{ template }}',
                },
            },
        },
    ]
    # fmt: on
