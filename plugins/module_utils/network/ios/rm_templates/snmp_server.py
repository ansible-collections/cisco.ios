# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Snmp_server parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Snmp_serverTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Snmp_serverTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "accounting",
            "getval": re.compile(
                r"""
                ^snmp-server\saccounting\scommands
                (\s(?P<command>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "accounting": {
                    "command": "{{ command }}",
                },
            },
        },
        {
            "name": "cache",
            "getval": re.compile(
                r"""
                ^snmp-server\scache\sinterval
                (\s(?P<interval>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "cache": "{{ interval }}",
            },
        },
        {
            "name": "chassis_id",
            "getval": re.compile(
                r"""
                ^snmp-server\schassis-id
                (\s(?P<uqString>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "chassis_id": "{{ uqString }}",
            },
        },
        {
            "name": "communities",
            "getval": re.compile(
                r"""
                ^snmp-server\scommunity
                (\s(?P<name>\S+))?
                (\sview\s(?P<view>\S+))?
                (\s(?P<ro>RO))?
                (\s(?P<rw>RW))?
                (\sipv6\s(?P<acl_v6>\S+))?
                (\s(?P<acl_v4>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "communities": [
                    {
                        "name": "{{ name }}",
                        "view": "{{ view }}",
                        "ro": "{{ not not ro }}",
                        "rw": "{{ not not rw }}",
                        "acl_v6": "{{ acl_v6 }}",
                        "acl_v4": "{{ acl_v4 }}",
                    },
                ]
            },
        },
        {
            "name": "contact",
            "getval": re.compile(
                r"""
                ^snmp-server\scontact
                (\s(?P<contact>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "contact": "{{ contact }}",
            },
        },
        {
            "name": "context",
            "getval": re.compile(
                r"""
                ^snmp-server\scontext
                (\s(?P<context>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "context": ["{{ contact }}",],
            },
        },
        {
            "name": "drop",
            "getval": re.compile(
                r"""
                ^snmp-server\sdrop
                (\s(?P<vrf_traffic>vrf-traffic))?
                (\s(?P<unknown_user>unknown-user))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "drop":{
                    "vrf_traffic": "{{ not not vrf_traffic }}",
                    "unknown_user": "{{ not not unknown_user }}",
                }
            },
        },
        {
            "name": "engine_id",
            "getval": re.compile(
                r"""
                ^snmp-server\sengineID
                (\s(?P<local>local))?
                (\sremote\s(?P<remotehost>\S+))?
                (\sudp-port\s(?P<udp_port>\d+))?
                (\svrf(?P<vrf>\S+))?
                (\s(?P<id>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "engine_id":[
                    {
                        "id": "'{{ id }}'",
                        "local": "{{ not not local }}",
                        "remote": {
                            "host": "{{ remotehost }}",
                            "udp_port": "{{ udp_port }}",
                            "vrf": "{{ vrf }}",
                        },
                    },
                ]
            },
        },
        {
            "name": "file_transfer",
            "getval": re.compile(
                r"""
                ^snmp-server\sfile-transfer
                (\saccess_group\s(?P<access_group>\S+))?
                (\sprotocol(?P<protocol>ftp|rcp|tftp))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "file_transfer":{
                    "access_group": "{{ access_group }}",
                    "protocol": ["{{ protocol }}",],
                },
            },
        },
        {
            "name": "groups",
            "getval": re.compile(
                r"""
                ^snmp-server\sgroup
                (\sgroup\s(?P<group>\S+))?
                (\sversion(?P<version>v1|v3|v2c))?
                (\scontext\s(?P<context>\S+))?
                (\snotify\s(?P<notify>\S+))?
                (\sread\s(?P<read>\S+))?
                (\swrite\s(?P<write>\S+))?
                (\saccess\s(?P<acl_v4>\S+))?
                (\saccess\sipv6\s(?P<acl_v6>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "groups":[
                    {
                        "group": "{{ group }}",
                        "version": "{{ version }}",
                        "context": "{{ context }}",
                        "notify": "{{ notify }}",
                        "read": "{{ read }}",
                        "write": "{{ write }}",
                        "acl_v4": "{{ acl_v4 }}",
                        "acl_v6": "{{ acl_v6 }}",
                    },
                ]
            },
        },
        {
            "name": "if_index",
            "getval": re.compile(
                r"""
                ^snmp-server\sifindex
                (\s(?P<if_index>persist))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "if_index": "{{ not not if_index }}",
            },
        },
        {
            "name": "inform",
            "getval": re.compile(
                r"""
                ^snmp-server\sinform
                (\spending(?P<pending>\d+))?
                (\sretries(?P<retries>\d+))?
                (\stimeout(?P<timeout>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "inform": {
                    "pending":"{{ pending }}",
                    "retries":"{{ retries }}",
                    "timeout":"{{ timeout }}",
                }
            },
        },
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                ^snmp-server\sip
                (\sdscp(?P<dscp>\d+))?
                (\sprecedence(?P<precedence>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "dscp":"{{ dscp }}",
                    "precedence":"{{ precedence }}",
                }
            },
        },
        {
            "name": "location",
            "getval": re.compile(
                r"""
                ^snmp-server\slocation
                (\s(?P<location>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "location": "{{ location }}",
            },
        },
        {
            "name": "manager",
            "getval": re.compile(
                r"""
                ^snmp-server\smanager
                (\ssession-timeout\s(?P<location>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "manager": "{{ manager }}",
            },
        },
        {
            "name": "packet_size",
            "getval": re.compile(
                r"""
                ^snmp-server\spacketsize
                (\s(?P<packet_size>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "packet_size": "{{ packet_size }}",
            },
        },
        {
            "name": "queue_length",
            "getval": re.compile(
                r"""
                ^snmp-server\squeue-length
                (\s(?P<queue_length>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "queue_length": "{{ queue_length }}",
            },
        },
        {
            "name": "system_shutdown",
            "getval": re.compile(
                r"""
                ^snmp-server
                (\s(?P<system_shutdown>system-shutdown))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "system_shutdown": "{{ not not system_shutdown }}",
            },
        },
        {
            "name": "trap_timeout",
            "getval": re.compile(
                r"""
                ^snmp-server\strap\stimeout
                (\s(?P<timeout>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "trap_timeout": "{{ timeout }}",
            },
        },
        {
            "name": "key_b",
            "getval": re.compile(
                r"""
                \s+key_b\s(?P<key_b>\S+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
            },
        },
    ]
    # fmt: on
