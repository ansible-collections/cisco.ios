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
                """, re.VERBOSE),
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
                """, re.VERBOSE),
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
                (\s(?P<uqString>.+$))?
                """, re.VERBOSE),
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
                (\s(?P<acl_v4>\S+|\d+))?
                """, re.VERBOSE),
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
                (\s(?P<contact>.+$))?
                """, re.VERBOSE),
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
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "context": ["{{ contact }}", ],
            },
        },
        {
            "name": "drop",
            "getval": re.compile(
                r"""
                ^snmp-server\sdrop
                (\s(?P<vrf_traffic>vrf-traffic))?
                (\s(?P<unknown_user>unknown-user))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "drop": {
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
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<id>\S+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "engine_id": [
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
                (\saccess-group\s(?P<access_group>\S+))?
                (\sprotocol\s(?P<protocol>ftp|rcp|tftp))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "file_transfer": {
                    "access_group": "{{ access_group }}",
                    "protocol": ["{{ protocol }}", ],
                },
            },
        },
        {
            "name": "groups",
            "getval": re.compile(
                r"""
                ^snmp-server\sgroup
                (\sgroup\s(?P<group>\S+))?
                (\sversion\s(?P<version>v1|v3|v2c))?
                (\scontext\s(?P<context>\S+))?
                (\snotify\s(?P<notify>\S+))?
                (\sread\s(?P<read>\S+))?
                (\swrite\s(?P<write>\S+))?
                (\saccess\s(?P<acl_v4>\S+))?
                (\saccess\sipv6\s(?P<acl_v6>\S+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "groups": [
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
                """, re.VERBOSE),
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
                (\spending\s(?P<pending>\d+))?
                (\sretries\s(?P<retries>\d+))?
                (\stimeout\s(?P<timeout>\d+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "inform": {
                    "pending": "{{ pending }}",
                    "retries": "{{ retries }}",
                    "timeout": "{{ timeout }}",
                }
            },
        },
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                ^snmp-server\sip
                (\sdscp\s(?P<dscp>\d+))?
                (\sprecedence(?P<precedence>\d+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "dscp": "{{ dscp }}",
                    "precedence": "{{ precedence }}",
                }
            },
        },
        {
            "name": "location",
            "getval": re.compile(
                r"""
                ^snmp-server\slocation
                (\s(?P<location>\S+))?
                """, re.VERBOSE),
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
                """, re.VERBOSE),
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
                """, re.VERBOSE),
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
                """, re.VERBOSE),
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
                """, re.VERBOSE),
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
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "trap_timeout": "{{ timeout }}",
            },
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""
                ^snmp-server\ssource-interface
                (\sinforms\s(?P<interface>\S+))?
                """, re.VERBOSE),
            "setval": "snmp-server source-interface informs Loopback999",
            "result": {
                "source_interface": "{{ interface }}",
            },
        },
        {
            "name": "trap_source",
            "getval": re.compile(
                r"""
                ^snmp-server\strap-source
                (\s(?P<interface>\S+))?
                """, re.VERBOSE),
            "setval": "snmp-server source-interface informs trap GigabitEthernet0/0",
            "result": {
                "trap_source": "{{ interface }}",
            },
        },
        {
            "name": "hosts",
            "getval": re.compile(
                r"""
                ^snmp-server
                (\shost\s(?P<host>\S+))?
                (\s(?P<informs>informs))?
                (\sversion\s(?P<version>1|3|2c))?
                (\s(?P<version_option>auth|noauth|priv))?
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<community_string>\w+))?
                (\s+(?P<traps>.+$))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "hosts": [
                    {
                        "host": "{{ host }}",
                        "informs": "{{ not not informs }}",
                        "community_string": "{{ community_string }}",
                        "traps": "{{ traps }}",
                        "version": "{{ version }}",
                        "version_option": "{{ version_option }}",
                        "vrf": "{{ vrf }}",
                    },
                ]
            },
        },
        {
            "name": "password_policy",
            "getval": re.compile(
                r"""
                ^snmp-server
                (\spassword-policy\s(?P<policy_name>\S+))?
                (\s(?P<define>define))?
                (\suser\s(?P<username>\S+))?
                (\smin-len\s(?P<min_len>\d+))?
                (\smax-len\s(?P<max_len>\d+))?
                (\supper-case\s(?P<upper_case>\d+))?
                (\slower-case\s(?P<lower_case>\d+))?
                (\sspecial-char\s(?P<special_char>\d+))?
                (\sdigits\s(?P<digits>\d+))?
                (\schange\s(?P<change>\d+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "password_policy": [
                    {
                        "policy_name": "{{ policy_name }}",
                        "username": "{{ username }}",
                        "min_len": "{{ min_len }}",
                        "max_len": "{{ max_len }}",
                        "upper_case": "{{ upper_case }}",
                        "lower_case": "{{ lower_case }}",
                        "special_char": "{{ special_char }}",
                        "change": "{{ change }}",
                        "digits": "{{ digits }}",
                    },
                ]
            },
        },
        {
            "name": "users",
            "getval": re.compile(
                r"""
                ^snmp-server
                (\suser\s(?P<username>\w+))?
                (\s(?P<group>\w+))?
                (\sremote\s(?P<remote>\S+))?
                (\sudp-port\s(?P<udp_port>\d+))?
                (\s(?P<version>v1|v3|v2c))?
                (\s(?P<version_option>auth|encrypted))?
                (\saccess\s(?P<acl_v4>\S+|\d+))?
                (\saccess\sipv6\s(?P<acl_v6>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "users": [
                    {
                        "username": "{{ username }}",
                        "group": "{{ group }}",
                        "remote": "{{ remote }}",
                        "udp_port": "{{ udp_port }}",
                        "version": "{{ version }}",
                        "version_option": "{{ version_option }}",
                        "acl_v4": "{{ acl_v4 }}",
                        "acl_v6": "{{ acl_v6 }}",
                        "vrf": "{{ vrf }}",
                    },
                ]
            },
        },
        {
            "name": "views",
            "getval": re.compile(
                r"""
                ^snmp-server
                (\sview\s(?P<name>\w+))?
                (\s(?P<family_name>\w+))?
                (\s(?P<excluded>excluded))?
                (\s(?P<included>included))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "users": [
                    {
                        "name": "{{ name }}",
                        "family_name": "{{ family_name }}",
                        "excluded": "{{ not not excluded }}",
                        "included": "{{ not not included }}",
                    },
                ]
            },
        },
        {  # only traps
            "name": "traps.auth_framework",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<auth_framework>auth-framework))?
                (\s(?P<sec_violation>sec-violation))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "auth_framework": {
                        "enable": "{{ not not auth_framework }}",
                        "sec_violation": "{{ not not excluded }}",
                    },
                },
            },
        },
        {
            "name": "traps.bfd",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sbfd
                (\s(?P<session_down>session-down))?
                (\s(?P<session_up>session-up))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "bfd": {
                        "session_down": "{{ not not session_down }}",
                        "session_up": "{{ not not session_up }}",
                    },
                },
            },
        },
        {
            "name": "traps.bgp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<bgp>bgp))?
                (\s(?P<cbgp2>cbgp2))?
                (\s(?P<state_changes>state-changes))?
                (\s(?P<all>all))?
                (\s(?P<backward_trans>backward-trans))?
                (\s(?P<limited>limited))?
                (\sthreshold(?P<prefix>prefix))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "bgp": {
                        "cbgp2": "{{ not not cbgp2 }}",
                        "enable": "{{ not not bgp }}",
                        "state_changes": {
                            "enable": "{{ not not state_changes }}",
                            "all": "{{ not not all }}",
                            "backward_trans": "{{ not not backward_trans }}",
                            "limited": "{{ not not limited }}",
                        },
                        "threshold": {
                            "prefix": "{{ not not prefix }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.bridge",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<bridge>bridge))?
                (\s(?P<newroot>newroot))?
                (\s(?P<topologychange>topologychange))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "bridge": {
                        "newroot": "{{ not not newroot }}",
                        "enable": "{{ not not bridge }}",
                        "topologychange": "{{ not not topologychange }}",
                    },
                },
            },
        },
        {
            "name": "traps.casa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<casa>casa))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "casa": "{{ not not casa }}",
                },
            },
        },
        {
            "name": "traps.cnpd",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<cnpd>cnpd))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "cnpd": "{{ not not cnpd }}",
                },
            },
        },
        {
            "name": "traps.config",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<config>config))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "config": "{{ not not config }}",
                },
            },
        },
        {
            "name": "traps.config_copy",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<config_copy>config-copy))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "config_copy": "{{ not not config_copy }}",
                },
            },
        },
        {
            "name": "traps.config_ctid",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<config_ctid>config-ctid))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "config_ctid": "{{ not not config_ctid }}",
                },
            },
        },
        {
            "name": "traps.dhcp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<dhcp>dhcp))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "dhcp": "{{ not not dhcp }}",
                },
            },
        },
        {
            "name": "traps.eigrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<eigrp>eigrp))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "eigrp": "{{ not not eigrp }}",
                },
            },
        },
        {
            "name": "traps.entity",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<entity>entity))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "entity": "{{ not not entity }}",
                },
            },
        },
        {
            "name": "traps.event_manager",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<event_manager>event-manager))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "event_manager": "{{ not not event_manager }}",
                },
            },
        },
        {
            "name": "traps.flowmon",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<flowmon>flowmon))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "flowmon": "{{ not not flowmon }}",
                },
            },
        },
        {
            "name": "traps.fru_ctrl",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<fru_ctrl>fru-ctrl))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "fru_ctrl": "{{ not not fru_ctrl }}",
                },
            },
        },
        {
            "name": "traps.hsrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<hsrp>hsrp))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "hsrp": "{{ not not hsrp }}",
                },
            },
        },
        {
            "name": "traps.ipsla",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<ipsla>ipsla))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "ipsla": "{{ not not ipsla }}",
                },
            },
        },
        {
            "name": "traps.msdp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<msdp>msdp))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps msdp",
            "result": {
                "traps": {
                    "msdp": "{{ not not msdp }}",
                },
            },
        },
        {
            "name": "traps.mvpn",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<mvpn>mvpn))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps mvpn",
            "result": {
                "traps": {
                    "msdp": "{{ not not mvpn }}",
                },
            },
        },
        {
            "name": "traps.pki",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<pki>pki))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps pki",
            "result": {
                "traps": {
                    "pki": "{{ not not pki }}",
                },
            },
        },
        {
            "name": "traps.rsvp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<rsvp>rsvp))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps rsvp",
            "result": {
                "traps": {
                    "rsvp": "{{ not not rsvp }}",
                },
            },
        },
        {
            "name": "traps.syslog",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<syslog>syslog))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps syslog",
            "result": {
                "traps": {
                    "syslog": "{{ not not syslog }}",
                },
            },
        },
        {
            "name": "traps.transceiver_all",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<transceiver_all>transceiver-all))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps transceiver-all",
            "result": {
                "traps": {
                    "transceiver_all": "{{ not not transceiver-all }}",
                },
            },
        },
        {
            "name": "traps.tty",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<tty>tty))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps tty",
            "result": {
                "traps": {
                    "tty": "{{ not not tty }}",
                },
            },
        },
        {
            "name": "traps.vrrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<vrrp>vrrp))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps vrrp",
            "result": {
                "traps": {
                    "vrrp": "{{ not not vrrp }}",
                },
            },
        },
        {
            "name": "traps.ipmulticast",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<ipmulticast>ipmulticast))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "ipmulticast": "{{ not not ipmulticast }}",
                },
            },
        },
        {
            "name": "traps.ike.policy.add",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\spolicy
                (\s(?P<add>add))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ike policy add",
            "result": {
                "traps": {
                    "ike": {
                        "policy": {
                            "add": "{{ not not add }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.policy.delete",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\spolicy
                (\s(?P<delete>delete))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ike policy delete",
            "result": {
                "traps": {
                    "ike": {
                        "policy": {
                            "delete": "{{ not not delete }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.tunnel.start",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\stunnel
                (\s(?P<start>start))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ike tunnel start",
            "result": {
                "traps": {
                    "ike": {
                        "tunnel": {
                            "start": "{{ not not start }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.tunnel.stop",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\stunnel
                (\s(?P<stop>stop))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ike tunnel stop",
            "result": {
                "traps": {
                    "ike": {
                        "tunnel": {
                            "stop": "{{ not not stop }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.add",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap
                (\s(?P<add>add))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec cryptomap add",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "add": "{{ not not add }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.delete",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap
                (\s(?P<delete>delete))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec cryptomap delete",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "delete": "{{ not not delete }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.attach",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap
                (\s(?P<attach>attach))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec cryptomap attach",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "attach": "{{ not not attach }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.detach",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap
                (\s(?P<detach>detach))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec cryptomap detach",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "detach": "{{ not not detach }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.tunnel.start",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\stunnel
                (\s(?P<start>start))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec tunnel start",
            "result": {
                "traps": {
                    "ipsec": {
                        "tunnel": {
                            "start": "{{ not not start }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.tunnel.stop",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\stunnel
                (\s(?P<stop>stop))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec tunnel stop",
            "result": {
                "traps": {
                    "ipsec": {
                        "tunnel": {
                            "stop": "{{ not not stop }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.too_many_sas",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec
                (\s(?P<too_many_sas>too-many-sas))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ipsec too-many-sas",
            "result": {
                "traps": {
                    "ipsec": {
                        "too_many_sas": "{{ not not too_many_sas }}",
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.error",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific
                (\s(?P<error>errors))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific errors",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "error": "{{ not not error }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.retransmit",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific
                (\s(?P<retransmit>retransmit))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific retransmit",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "retransmit": "{{ not not retransmit }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.lsa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific
                (\s(?P<lsa>lsa))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific lsa",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "lsa": "{{ not not lsa }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.state_change.nssa_trans_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change
                (\s(?P<nssa_trans_change>nssa-trans-change))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "nssa_trans_change": "{{ not not nssa_trans_change }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.state_change.shamlink.interface",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change\sshamlink
                (\s(?P<interface>interface))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific state-change shamlink interface",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "shamlink": {
                                    "interface": "{{ not not interface }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.state_change.shamlink.neighbor",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change\sshamlink
                (\s(?P<neighbor>neighbor))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "shamlink": {
                                    "neighbor": "{{ not not neighbor }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.error",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf
                (\s(?P<error>errors))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf errors",
            "result": {
                "traps": {
                    "ospf": {
                        "error": "{{ not not error }}",
                    },
                },
            },
        },
        {
            "name": "traps.ospf.retransmit",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf
                (\s(?P<retransmit>retransmit))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf retransmit",
            "result": {
                "traps": {
                    "ospf": {
                        "retransmit": "{{ not not retransmit }}",
                    },
                },
            },
        },
        {
            "name": "traps.ospf.lsa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf
                (\s(?P<lsa>lsa))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf lsa",
            "result": {
                "traps": {
                    "ospf": {
                        "lsa": "{{ not not lsa }}",
                    },
                },
            },
        },
        {
            "name": "traps.ospf.state_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf
                (\s(?P<state_change>state-change))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps ospf state-change",
            "result": {
                "traps": {
                    "ospf": {
                        "state_change": "{{ not not state_change }}",
                    },
                },
            },
        },
        {
            "name": "traps.l2tun.pseudowire_status",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sl2tun
                (\s(?P<pseudowire_status>pseudowire\sstatus))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps l2tun pseudowire status",
            "result": {
                "traps": {
                    "l2tun": {
                        "pseudowire_status": "{{ not not pseudowire_status }}",
                    },
                },
            },
        },
        {
            "name": "traps.l2tun.session",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sl2tun
                (\s(?P<session>session))?
                """, re.VERBOSE),
            "setval": "snmp-server enable traps l2tun session",
            "result": {
                "traps": {
                    "l2tun": {
                        "session": "{{ not not session }}",
                    },
                },
            },
        },
        {
            "name": "traps.cpu",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\traps
                (\s(?P<cpu>cpu))?
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "cpu": {
                        "enable": "{{ not not cpu }}",
                        "threshold": "{{ not not threshold }}",
                    },
                },
            },
        },
        {
            "name": "traps.firewall",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<firewall>firewall))?
                (\s(?P<serverstatus>serverstatus))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "firewall": {
                        "enable": "{{ not not firewall }}",
                        "serverstatus": "{{ not not serverstatus }}",
                    },
                },
            },
        },
        {
            "name": "traps.pim",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<pim>pim))?
                (\s(?P<neighbor_change>neighbor-change))?
                (\s(?P<rp_mapping_change>rp-mapping-change))?
                (\s(?P<invalid_pim_message>invalid-pim-message))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "pim": {
                        "enable": "{{ not not pim }}",
                        "neighbor_change": "{{ not not neighbor_change }}",
                        "rp_mapping_change": "{{ not not rp_mapping_change }}",
                        "invalid_pim_message": "{{ not not invalid_pim_message }}",
                    },
                },
            },
        },
        {
            "name": "traps.snmp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\ssnmp
                (\s(?P<authentication>authentication))?
                (\s(?P<linkdown>linkdown))?
                (\s(?P<linkup>linkup))?
                (\s(?P<coldstart>coldstart))?
                (\s(?P<warmstart>warmstart))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "snmp": {
                        "authentication": "{{ not not authentication }}",
                        "linkdown": "{{ not not linkdown }}",
                        "linkup": "{{ not not linkup }}",
                        "coldstart": "{{ not not coldstart }}",
                        "warmstart": "{{ not not warmstart }}",
                    },
                },
            },
        },
        {
            "name": "traps.frame_relay",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<frame_relay>frame-relay))?
                (\s(?P<subif>subif))?
                (\scount(?P<count>\d+))?
                (\sinterval(?P<interval>\d+))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "frame_relay": {
                        "enable": "{{ not not firewall }}",
                        "subif": {
                            "enable": "{{ not not subif }}",
                            "interval": "{{ interval }}",
                            "count": "{{ count }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.cef",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<cef>cef))?
                (\s(?P<resource_failure>resource-failure))?
                (\s(?P<peer_state_change>peer-state-change))?
                (\s(?P<peer_fib_state_change>peer-fib-state-change))?
                (\s(?P<inconsistency>inconsistency))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "bridge": {
                        "enable": "{{ not not cef }}",
                        "inconsistency": "{{ not not inconsistency }}",
                        "peer_fib_state_change": "{{ not not peer_fib_state_change }}",
                        "peer_state_change": "{{ not not peer_state_change }}",
                        "resource_failure": "{{ not not resource_failure }}",
                    },
                },
            },
        },
        {
            "name": "traps.dlsw",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps
                (\s(?P<dlsw>dlsw))?
                (\s(?P<circuit>circuit))?
                (\s(?P<tconn>tconn))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "dlsw": {
                        "enable": "{{ not not dlsw }}",
                        "circuit": "{{ not not circuit }}",
                        "tconn": "{{ not not tconn }}",
                    },
                },
            },
        },
        {
            "name": "traps.ethernet",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sethernet
                (\s(?P<cfm>cfm))?
                (\s(?P<alarm>alarm))?
                (\s(?P<evc>evc))?
                (\s(?P<create>create))?
                (\s(?P<delete>delete))?
                (\s(?P<status>status))?
                """, re.VERBOSE),
            "setval": "",
            "result": {
                "traps": {
                    "ethernet": {
                        "cfm": {
                            "alarm": "{{ not not alarm }}",
                        },
                        "evc": {
                            "create": "{{ not not create }}",
                            "delete": "{{ not not delete }}",
                            "status": "{{ not not status }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
