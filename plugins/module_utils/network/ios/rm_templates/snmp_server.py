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


def cmd_option_engine_id(config_data):
    cmd = ""
    if config_data:
        cmd = "snmp-server engineID "
        if config_data.get("local"):
            cmd += "local"
        if config_data.get("remote"):
            rm = config_data.get("remote")
            if rm.get("host"):
                cmd += "remote {host}".format(host=rm.get("host"))
            if rm.get("udp_port"):
                cmd += " udp-port {udp_port}".format(udp_port=rm.get("udp_port"))
            if rm.get("vrf"):
                cmd += " vrf {vrf}".format(vrf=rm.get("vrf"))
        if config_data.get("id"):
            cmd += " {id}".format(id=config_data.get("id"))
    return cmd


def cmd_option_file_transfer(config_data):  # contain sub list attr
    cmd = ""
    if config_data.get("file_transfer"):
        conf = config_data.get("file_transfer")
        cmd = "snmp-server file-transfer"
        if conf.get("access_group"):
            cmd += " access-group {ag}".format(ag=conf.get("access_group"))
        if conf.get("protocol"):
            cmd += " protocol"
            for protocol in list(conf.get("protocol").keys()):
                cmd += " {protocol}".format(protocol=protocol)
    return cmd


def cmd_option_hosts(config_data):  # contain sub list attr
    cmd = ""
    if config_data:
        cmd = "snmp-server host"
        if config_data.get("host"):
            cmd += " {host}".format(host=config_data.get("host"))
        if config_data.get("informs"):
            cmd += " informs"
        if config_data.get("version"):
            cmd += " version {version}".format(version=config_data.get("version"))
        if config_data.get("version_option"):
            cmd += " {version}".format(version=config_data.get("version_option"))
        if config_data.get("vrf"):
            cmd += " vrf {vrf}".format(vrf=config_data.get("vrf"))
        if config_data.get("community_string"):
            cmd += " {community_string}".format(
                community_string=config_data.get("community_string"),
            )
        if config_data.get("traps"):
            for protocol in list(config_data.get("traps").keys()):
                cmd += " {protocol}".format(protocol=protocol)
    return cmd


def cmd_option_trap_bgp(config_data):
    cmd = ""
    conf = config_data.get("traps", {}).get("bgp", {})
    if conf:
        if conf.get("enable"):
            cmd += "snmp-server enable traps bgp"
        if conf.get("cbgp2"):
            cmd += " cbgp2"
        if conf.get("state_changes"):
            if conf.get("state_changes").get("enable"):
                cmd += " state-changes"
            if conf.get("state_changes").get("all"):
                cmd += " all"
            if conf.get("state_changes").get("backward_trans"):
                cmd += " backward-trans"
            if conf.get("state_changes").get("limited"):
                cmd += " limited"
        if conf.get("threshold"):
            cmd += " threshold"
            if conf.get("threshold").get("prefix"):
                cmd += " prefix"
    return cmd


class Snmp_serverTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Snmp_serverTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "accounting",
            "getval": re.compile(
                r"""
                ^snmp-server\saccounting\scommands
                (\s(?P<command>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server accounting commands {{ accounting.command }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server cache interval {{ cache }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server chassis-id {{ chassis_id }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server community "
                      "{{ name }}"
                      "{{ (' view ' + view) if view is defined else '' }}"
                      "{{ ' ro' if ro|d(False) else ''}}"
                      "{{ ' rw' if rw|d(False) else ''}}"
                      "{{ (' ipv6 ' + acl_v6) if acl_v6 is defined else '' }}"
                      "{{ (' ' + acl_v4) if acl_v4 is defined else '' }}",
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
                ],
            },
        },
        {
            "name": "contact",
            "getval": re.compile(
                r"""
                ^snmp-server\scontact
                (\s(?P<contact>.+$))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server contact {{ contact }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server context {{ context }}",
            "result": {
                "context": ["{{ context }}"],
            },
        },
        {
            "name": "drop",
            "getval": re.compile(
                r"""
                ^snmp-server\sdrop
                (\s(?P<vrf_traffic>vrf-traffic))?
                (\s(?P<unknown_user>unknown-user))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server drop"
                      "{{ ' vrf-traffic' if drop.vrf_traffic is defined else '' }}"
                      "{{ ' unknown-user' if drop.unknown_user is defined else '' }}",
            "result": {
                "drop": {
                    "vrf_traffic": "{{ not not vrf_traffic }}",
                    "unknown_user": "{{ not not unknown_user }}",
                },
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
                """, re.VERBOSE,
            ),
            "setval": cmd_option_engine_id,
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
                ],
            },
        },
        {
            "name": "file_transfer",
            "getval": re.compile(
                r"""
                ^snmp-server\sfile-transfer
                (\saccess-group\s(?P<access_group>\S+))?
                (\sprotocol\s(?P<protocol>ftp|rcp|tftp))?
                """, re.VERBOSE,
            ),
            "setval": cmd_option_file_transfer,
            "result": {
                "file_transfer": {
                    "access_group": "{{ access_group }}",
                    "protocol": ["{{ protocol }}"],
                },
            },
        },
        {
            "name": "groups",
            "getval": re.compile(
                r"""
                ^snmp-server\sgroup
                (\s(?P<group>\S+))?
                (\s(?P<version>v1|v3|v2c))?
                (\s(?P<version_option>auth|noauth|priv))?
                (\scontext\s(?P<context>\S+))?
                (\snotify\s(?P<notify>\S+))?
                (\sread\s(?P<read>\S+))?
                (\swrite\s(?P<write>\S+))?
                (\saccess\s(?P<acl_v4>\S+))?
                (\saccess\sipv6\s(?P<acl_v6>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server group "
                      "{{ group if group is defined else '' }}"
                      "{{ (' ' + version) if version is defined else '' }}"
                      "{{ (' ' + version_option) if version_option is defined else '' }}"
                      "{{ (' context ' + context) if context is defined else '' }}"
                      "{{ (' notify ' + notify) if notify is defined else '' }}"
                      "{{ (' read ' + read) if read is defined else '' }}"
                      "{{ (' write ' + write) if write is defined else '' }}"
                      "{{ (' access ' + acl_v4) if acl_v4 is defined else '' }}"
                      "{{ (' access ipv6 ' + acl_v6) if acl_v6 is defined else '' }}",
            "result": {
                "groups": [
                    {
                        "group": "{{ group }}",
                        "version": "{{ version }}",
                        "version_option": "{{ version_option }}",
                        "context": "{{ context }}",
                        "notify": "{{ notify }}",
                        "read": "{{ read }}",
                        "write": "{{ write }}",
                        "acl_v4": "{{ acl_v4 }}",
                        "acl_v6": "{{ acl_v6 }}",
                    },
                ],
            },
        },
        {
            "name": "hosts",
            "getval": re.compile(
                r"""
                ^snmp-server\shost
                (\s(?P<host>\S+))?
                (\s(?P<informs>informs))?
                (\sversion\s(?P<version>1|3|2c))?
                (\s(?P<version_option>auth|noauth|priv))?
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<community_string>\S+))?
                (\s+(?P<traps>.+$))?
                """, re.VERBOSE,
            ),
            "setval": cmd_option_hosts,
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
                ],
            },
        },
        {
            "name": "password_policy",
            "getval": re.compile(
                r"""
                ^snmp-server\spassword-policy
                (\s(?P<policy_name>\S+))?
                (\s(?P<define>define))?
                (\suser\s(?P<username>\S+))?
                (\smin-len\s(?P<min_len>\d+))?
                (\smax-len\s(?P<max_len>\d+))?
                (\supper-case\s(?P<upper_case>\d+))?
                (\slower-case\s(?P<lower_case>\d+))?
                (\sspecial-char\s(?P<special_char>\d+))?
                (\sdigits\s(?P<digits>\d+))?
                (\schange\s(?P<change>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server password-policy "
                      "{{ policy_name if policy_name is defined else '' }}"
                      "{{ (' user ' + username) if username is defined else ' define' }}"
                      "{{ (' min-len ' + min_len|string) if min_len is defined else '' }}"
                      "{{ (' max-len ' + max_len|string) if max_len is defined else '' }}"
                      "{{ (' upper-case ' + upper_case|string) if upper_case is defined else '' }}"
                      "{{ (' lower-case ' + lower_case|string) if lower_case is defined else '' }}"
                      "{{ (' special-char ' + special_char|string) if special_char is defined else '' }}"
                      "{{ (' digits ' + digits|string) if digits is defined else '' }}"
                      "{{ (' change ' + change|string) if change is defined else '' }}",
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
                ],
            },
        },
        {
            "name": "users",
            "getval": re.compile(
                r"""
                ^snmp-server\suser
                (\s(?P<username>\S+))?
                (\s(?P<group>\S+))?
                (\sremote\s(?P<remote>\S+))?
                (\sudp-port\s(?P<udp_port>\d+))?
                (\s(?P<version>v1|v3|v2c))?
                (\s(?P<version_option>auth|encrypted))?
                (\saccess\s(?P<acl_v4>\S+|\d+))?
                (\saccess\sipv6\s(?P<acl_v6>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server user "
                      "{{ username if username is defined else '' }}"
                      "{{ (' ' + group) if group is defined else '' }}"
                      "{{ (' remote ' + remote) if remote is defined else '' }}"
                      "{{ (' udp-port ' + udp_port|string) if udp_port is defined else '' }}"
                      "{{ (' ' + version) if version is defined else '' }}"
                      "{{ (' ' + version_option) if version_option is defined else '' }}"
                      "{{ (' auth ' + authentication.algorithm) if authentication is defined and authentication.algorithm is defined else '' }}"
                      "{{ (' ' + authentication.password) if authentication is defined and authentication.password is defined else '' }}"
                      "{{ (' priv ' + encryption.priv) if encryption is defined and encryption.priv is defined else '' }}"
                      "{{ (' ' + encryption.priv_option) if encryption is defined and encryption.priv_option is defined else '' }}"
                      "{{ (' ' + encryption.password) if encryption is defined and encryption.password is defined else '' }}"
                      "{{ (' access ' + acl_v4|string) if acl_v4 is defined else '' }}"
                      "{{ (' access ipv6 ' + acl_v6) if acl_v6 is defined else '' }}"
                      "{{ (' vrf ' + vrf) if vrf is defined else '' }}",
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
                ],
            },
        },
        {
            "name": "views",
            "getval": re.compile(
                r"""
                ^snmp-server\sview
                (\s(?P<name>\S+))?
                (\s(?P<family_name>[-\w]+))?
                (\s(?P<excluded>excluded))?
                (\s(?P<included>included))?
                $""", re.VERBOSE,
            ),
            "setval": "snmp-server view "
                      "{{ name if name is defined else '' }}"
                      "{{ (' ' + family_name) if family_name is defined else '' }}"
                      "{{ ' excluded' if excluded is defined else '' }}"
                      "{{ ' included' if included is defined else '' }}",
            "result": {
                "views": [
                    {
                        "name": "{{ name }}",
                        "family_name": "{{ family_name }}",
                        "excluded": "{{ not not excluded }}",
                        "included": "{{ not not included }}",
                    },
                ],
            },
        },
        {
            "name": "if_index",
            "getval": re.compile(
                r"""
                ^snmp-server\sifindex
                (\s(?P<if_index>persist))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server ifindex persist",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server inform"
                      "{{ (' pending ' + inform.pending|string) if inform.pending is defined else '' }}"
                      "{{ (' retries ' + inform.retries|string) if inform.retries is defined else '' }}"
                      "{{ (' timeout ' + inform.timeout|string) if inform.timeout is defined else '' }}",
            "result": {
                "inform": {
                    "pending": "{{ pending }}",
                    "retries": "{{ retries }}",
                    "timeout": "{{ timeout }}",
                },
            },
        },
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                ^snmp-server\sip\sdscp
                (\s(?P<dscp>\d+))?
                (\sprecedence(?P<precedence>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server ip dscp "
                      "{{ (ip.dscp|string) if ip.dscp is defined else '' }}"
                      "{{ (' precedence ' + ip.precedence) if ip.precedence is defined else '' }}",
            "result": {
                "ip": {
                    "dscp": "{{ dscp }}",
                    "precedence": "{{ precedence }}",
                },
            },
        },
        {
            "name": "location",
            "getval": re.compile(
                r"""
                ^snmp-server\slocation
                (\s(?P<location>.+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server location {{ location }}",
            "result": {
                "location": "{{ location }}",
            },
        },
        {
            "name": "manager",
            "getval": re.compile(
                r"""
                ^snmp-server\smanager
                (\ssession-timeout\s(?P<manager>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server manager session-timeout {{ manager }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server packetsize {{ packet_size }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server queue-length {{ queue_length }}",
            "result": {
                "queue_length": "{{ queue_length }}",
            },
        },
        {
            "name": "trap_timeout",
            "getval": re.compile(
                r"""
                ^snmp-server\strap\stimeout
                (\s(?P<ttimeout>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server trap timeout {{ trap_timeout }}",
            "result": {
                "trap_timeout": "{{ ttimeout }}",
            },
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""
                ^snmp-server\ssource-interface
                (\sinforms\s(?P<interface>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server source-interface informs {{ source_interface }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server trap-source {{ trap_source }}",
            "result": {
                "trap_source": "{{ interface }}",
            },
        },

        {  # only traps
            "name": "traps.auth_framework",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sauth-framework
                (\s(?P<sec_violation>sec-violation))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps"
                      "{{ (' auth-framework') if traps.auth_framework.enable is defined else '' }}"
                      "{{ (' sec-violation') if traps.auth_framework.sec_violation is defined else '' }}",
            "result": {
                "traps": {
                    "auth_framework": {
                        "enable": True,
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
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps bfd' if traps.bfd.enable is defined else '' }}"
                      "{{ (' session-down') if traps.bfd.session_down is defined else '' }}"
                      "{{ (' session-up') if traps.bfd.session_up is defined else '' }}",
            "result": {
                "traps": {
                    "bfd": {
                        "enable": True,
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
                ^snmp-server\senable\straps\sbgp
                (\s(?P<cbgp2>cbgp2))?
                (\s(?P<state_changes>state-changes))?
                (\s(?P<all>all))?
                (\s(?P<backward_trans>backward-trans))?
                (\s(?P<limited>limited))?
                (\sthreshold(?P<prefix>prefix))?
                """, re.VERBOSE,
            ),
            "setval": cmd_option_trap_bgp,
            "remval": "snmp-server enable traps bgp",
            "result": {
                "traps": {
                    "bgp": {
                        "cbgp2": "{{ not not cbgp2 }}",
                        "enable": True,
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
                ^snmp-server\senable\straps\sbridge
                (\s(?P<newroot>newroot))?
                (\s(?P<topologychange>topologychange))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps bridge' if traps.bridge.enable is defined else '' }}"
                      "{{ (' newroot') if traps.bridge.newroot|d(False) is defined else '' }}"
                      "{{ (' topologychange') if traps.bridge.topologychange|d(False) is defined else '' }}",
            "result": {
                "traps": {
                    "bridge": {
                        "newroot": "{{ not not newroot }}",
                        "enable": True,
                        "topologychange": "{{ not not topologychange }}",
                    },
                },
            },
        },
        {
            "name": "traps.casa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\scasa
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps casa",
            "result": {
                "traps": {
                    "casa": True,
                },
            },
        },
        {
            "name": "traps.cnpd",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\scnpd
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps cnpd",
            "result": {
                "traps": {
                    "cnpd": True,
                },
            },
        },
        {
            "name": "traps.config",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sconfig
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps config",
            "result": {
                "traps": {
                    "config": True,
                },
            },
        },
        {
            "name": "traps.isis",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sisis$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps isis",
            "result": {
                "traps": {
                    "isis": True,
                },
            },
        },
        {
            "name": "traps.config_copy",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sconfig-copy
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps config-copy",
            "result": {
                "traps": {
                    "config_copy": True,
                },
            },
        },
        {
            "name": "traps.config_ctid",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sconfig-ctid
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps config-ctid",
            "result": {
                "traps": {
                    "config_ctid": True,
                },
            },
        },
        {
            "name": "traps.dhcp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sdhcp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps dhcp",
            "result": {
                "traps": {
                    "dhcp": True,
                },
            },
        },
        {
            "name": "traps.eigrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\seigrp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps eigrp",
            "result": {
                "traps": {
                    "eigrp": True,
                },
            },
        },
        {
            "name": "traps.entity",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sentity
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps entity",
            "result": {
                "traps": {
                    "entity": True,
                },
            },
        },
        {
            "name": "traps.energywise",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senergywise$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps energywise",
            "result": {
                "traps": {
                    "energywise": True,
                },
            },
        },
        {
            "name": "traps.event_manager",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sevent-manager
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps event-manager",
            "result": {
                "traps": {
                    "event_manager": True,
                },
            },
        },
        {
            "name": "traps.flowmon",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sflowmon
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps flowmon",
            "result": {
                "traps": {
                    "flowmon": True,
                },
            },
        },
        {
            "name": "traps.fru_ctrl",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sfru-ctrl
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps fru-ctrl",
            "result": {
                "traps": {
                    "fru_ctrl": True,
                },
            },
        },
        {
            "name": "traps.hsrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\shsrp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps hsrp",
            "result": {
                "traps": {
                    "hsrp": True,
                },
            },
        },
        {
            "name": "traps.ipsla",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsla
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsla",
            "result": {
                "traps": {
                    "ipsla": True,
                },
            },
        },
        {
            "name": "traps.msdp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smsdp$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps msdp",
            "result": {
                "traps": {
                    "msdp": True,
                },
            },
        },
        {
            "name": "traps.pw_vc",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\spw\svc$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps pw vc",
            "result": {
                "traps": {
                    "pw_vc": True,
                },
            },
        },
        {
            "name": "traps.mvpn",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smvpn
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mvpn",
            "result": {
                "traps": {
                    "mvpn": True,
                },
            },
        },
        {
            "name": "traps.mpls_vpn",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\svpn
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls vpn",
            "result": {
                "traps": {
                    "mpls_vpn": True,
                },
            },
        },
        {
            "name": "traps.pki",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\spki
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps pki",
            "result": {
                "traps": {
                    "pki": True,
                },
            },
        },
        {
            "name": "traps.rsvp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\srsvp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps rsvp",
            "result": {
                "traps": {
                    "rsvp": True,
                },
            },
        },
        {
            "name": "traps.syslog",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\ssyslog
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps syslog",
            "result": {
                "traps": {
                    "syslog": True,
                },
            },
        },
        {
            "name": "traps.transceiver_all",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\stransceiver-all
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps transceiver-all",
            "result": {
                "traps": {
                    "transceiver_all": True,
                },
            },
        },
        {
            "name": "traps.tty",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\stty
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps tty",
            "result": {
                "traps": {
                    "tty": True,
                },
            },
        },
        {
            "name": "traps.envmon.shutdown",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sshutdown$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon shutdown",
            "result": {
                "traps": {
                    "envmon": {
                        "shutdown": True,
                    },
                },
            },
        },
        {
            "name": "traps.envmon.status",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sstatus$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon status",
            "result": {
                "traps": {
                    "envmon": {
                        "status": True,
                    },
                },
            },
        },
        {
            "name": "traps.envmon.supply",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\ssupply$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon supply",
            "result": {
                "traps": {
                    "envmon": {
                        "supply": True,
                    },
                },
            },
        },
        {
            "name": "traps.envmon.temperature",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\stemperature$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon temperature",
            "result": {
                "traps": {
                    "envmon": {
                        "temperature": True,
                    },
                },
            },
        },
        {
            "name": "traps.envmon.fan.enable",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sfan$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon fan",
            "result": {
                "traps": {
                    "envmon": {
                        "fan": {
                            "enable": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.envmon.fan.shutdown",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sfan\sshutdown$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon fan shutdown",
            "result": {
                "traps": {
                    "envmon": {
                        "fan": {
                            "shutdown": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.envmon.fan.status",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sfan\sstatus$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon fan status",
            "result": {
                "traps": {
                    "envmon": {
                        "fan": {
                            "status": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.envmon.fan.supply",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sfan\ssupply$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon fan supply",
            "result": {
                "traps": {
                    "envmon": {
                        "fan": {
                            "supply": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.envmon.fan.temperature",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon\sfan\stemperature$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon fan temperature",
            "result": {
                "traps": {
                    "envmon": {
                        "fan": {
                            "temperature": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.vrrp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svrrp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vrrp",
            "result": {
                "traps": {
                    "vrrp": True,
                },
            },
        },
        {
            "name": "traps.ipmulticast",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipmulticast
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipmulticast",
            "result": {
                "traps": {
                    "ipmulticast": True,
                },
            },
        },
        {
            "name": "traps.ike.policy.add",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\spolicy\sadd
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ike policy add",
            "result": {
                "traps": {
                    "ike": {
                        "policy": {
                            "add": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.policy.delete",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\spolicy\sdelete
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ike policy delete",
            "result": {
                "traps": {
                    "ike": {
                        "policy": {
                            "delete": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.tunnel.start",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\stunnel\sstart
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ike tunnel start",
            "result": {
                "traps": {
                    "ike": {
                        "tunnel": {
                            "start": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ike.tunnel.stop",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sike\stunnel\sstop
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ike tunnel stop",
            "result": {
                "traps": {
                    "ike": {
                        "tunnel": {
                            "stop": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.add",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap\sadd
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec cryptomap add",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "add": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.delete",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap\sdelete
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec cryptomap delete",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "delete": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.attach",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap\sattach
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec cryptomap attach",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "attach": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.cryptomap.detach",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\scryptomap\sdetach
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec cryptomap detach",
            "result": {
                "traps": {
                    "ipsec": {
                        "cryptomap": {
                            "detach": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.tunnel.start",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\stunnel\sstart
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec tunnel start",
            "result": {
                "traps": {
                    "ipsec": {
                        "tunnel": {
                            "start": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.tunnel.stop",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\stunnel\sstop
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec tunnel stop",
            "result": {
                "traps": {
                    "ipsec": {
                        "tunnel": {
                            "stop": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ipsec.too_many_sas",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sipsec\stoo-many-sas
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ipsec too-many-sas",
            "result": {
                "traps": {
                    "ipsec": {
                        "too_many_sas": True,
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.error",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\serrors
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific errors",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "error": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.retransmit",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\sretransmit
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific retransmit",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "retransmit": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.lsa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\slsa
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific lsa",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "lsa": True,
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospf.cisco_specific.state_change.nssa_trans_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change\snssa-trans-change
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "nssa_trans_change": True,
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
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change\sshamlink\sinterface
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific state-change shamlink interface",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "shamlink": {
                                    "interface": True,
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
                ^snmp-server\senable\straps\sospf\scisco-specific\sstate-change\sshamlink\sneighbor
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
            "result": {
                "traps": {
                    "ospf": {
                        "cisco_specific": {
                            "state_change": {
                                "shamlink": {
                                    "neighbor": True,
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
                ^snmp-server\senable\straps\sospf\serrors
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf errors",
            "result": {
                "traps": {
                    "ospf": {
                        "error": True,
                    },
                },
            },
        },
        {
            "name": "traps.ospf.retransmit",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\sretransmit
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf retransmit",
            "result": {
                "traps": {
                    "ospf": {
                        "retransmit": True,
                    },
                },
            },
        },
        {
            "name": "traps.ospf.lsa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\slsa
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf lsa",
            "result": {
                "traps": {
                    "ospf": {
                        "lsa": True,
                    },
                },
            },
        },
        {
            "name": "traps.ospf.state_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospf\sstate-change
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospf state-change",
            "result": {
                "traps": {
                    "ospf": {
                        "state_change": True,
                    },
                },
            },
        },
        {
            "name": "traps.l2tun.pseudowire_status",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sl2tun\spseudowire\sstatus
                (\s(?P<pseudowire_status>))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps l2tun pseudowire status",
            "result": {
                "traps": {
                    "l2tun": {
                        "pseudowire_status": True,
                    },
                },
            },
        },
        {
            "name": "traps.l2tun.session",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sl2tun\ssession
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps l2tun session",
            "result": {
                "traps": {
                    "l2tun": {
                        "session": True,
                    },
                },
            },
        },
        {
            "name": "traps.cpu",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\scpu
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps cpu' if traps.cpu.enable is defined else '' }}"
                      "{{ ' threshold' if traps.cpu.threshold is defined else '' }}",
            "result": {
                "traps": {
                    "cpu": {
                        "enable": True,
                        "threshold": "{{ not not threshold }}",
                    },
                },
            },
        },
        {
            "name": "traps.firewall",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sfirewall
                (\s(?P<serverstatus>serverstatus))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps firewall' if traps.firewall.enable is defined else '' }}"
                      "{{ ' serverstatus' if traps.firewall.serverstatus|d(False) else ''}}",
            "result": {
                "traps": {
                    "firewall": {
                        "enable": True,
                        "serverstatus": "{{ not not serverstatus }}",
                    },
                },
            },
        },
        {
            "name": "traps.pim",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\spim
                (\s(?P<neighbor_change>neighbor-change))?
                (\s(?P<rp_mapping_change>rp-mapping-change))?
                (\s(?P<invalid_pim_message>invalid-pim-message))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps pim' if traps.pim.enable is defined else '' }}"
                      "{{ ' neighbor-change' if traps.pim.neighbor_change|d(False) else ''}}"
                      "{{ ' rp-mapping-change' if traps.pim.rp_mapping_change|d(False) else ''}}"
                      "{{ ' invalid-pim-message' if traps.pim.invalid_pim_message|d(False) else ''}}",
            "result": {
                "traps": {
                    "pim": {
                        "enable": True,
                        "neighbor_change": "{{ not not neighbor_change }}",
                        "rp_mapping_change": "{{ not not rp_mapping_change }}",
                        "invalid_pim_message": "{{ not not invalid_pim_message }}",
                    },
                },
            },
        },
        {
            "name": "traps.vrfmib",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svrfmib
                (\s(?P<vrf_up>vrf-up))?
                (\s(?P<vrf_down>vrf-down))?
                (\s(?P<vnet_trunk_up>vnet-trunk-up))?
                (\s(?P<vnet_trunk_down>vnet-trunk-down))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vrfmib"
                      "{{ ' vrf-up' if traps.vrfmib.vrf_up|d(False) else ''}}"
                      "{{ ' vrf-down' if traps.vrfmib.vrf_down|d(False) else ''}}"
                      "{{ ' vnet-trunk-up' if traps.vrfmib.vnet_trunk_up|d(False) else ''}}"
                      "{{ ' vnet-trunk-down' if traps.vrfmib.vnet_trunk_down|d(False) else ''}}",
            "result": {
                "traps": {
                    "vrfmib": {
                        "vrf_up": "{{ not not vrf_up }}",
                        "vrf_down": "{{ not not vrf_down }}",
                        "vnet_trunk_up": "{{ not not vnet_trunk_up }}",
                        "vnet_trunk_down": "{{ not not vnet_trunk_down }}",
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
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps snmp"
                      "{{ ' authentication' if traps.snmp.authentication is defined else '' }}"
                      "{{ ' linkdown' if traps.snmp.linkdown|d(False) else ''}}"
                      "{{ ' linkup' if traps.snmp.linkup|d(False) else ''}}"
                      "{{ ' warmstart' if traps.snmp.warmstart|d(False) else ''}}"
                      "{{ ' coldstart' if traps.snmp.coldstart|d(False) else ''}}",
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
                ^snmp-server\senable\straps\sframe-relay$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps frame-relay",
            "result": {
                "traps": {
                    "frame_relay": {
                        "enable": True,
                    },
                },
            },
        },
        {
            "name": "traps.frame_relay.subif",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sframe-relay\ssubif
                (\scount(?P<count>\d+))?
                (\sinterval(?P<interval>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps frame-relay subif"
                      "{{ (' count ' + count|string) if traps.frame_relay.count else '' }}"
                      "{{ (' interval ' + interval|string) if traps.frame_relay.interval else '' }}",
            "result": {
                "traps": {
                    "frame_relay": {
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
                ^snmp-server\senable\straps\scef
                (\s(?P<resource_failure>resource-failure))?
                (\s(?P<peer_state_change>peer-state-change))?
                (\s(?P<peer_fib_state_change>peer-fib-state-change))?
                (\s(?P<inconsistency>inconsistency))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps cef' if traps.cef.enable is defined else '' }}"
                      "{{ ' resource-failure' if traps.cef.resource_failure|d(False) else ''}}"
                      "{{ ' peer-state-change' if traps.cef.peer_state_change|d(False) else ''}}"
                      "{{ ' peer-fib-state-change' if traps.cef.peer_fib_state_change|d(False) else ''}}"
                      "{{ ' inconsistency' if traps.cef.inconsistency|d(False) else ''}}",
            "result": {
                "traps": {
                    "cef": {
                        "enable": True,
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
                ^snmp-server\senable\straps\sdlsw
                (\s(?P<circuit>circuit))?
                (\s(?P<tconn>tconn))?
                """, re.VERBOSE,
            ),
            "setval": "{{ 'snmp-server enable traps dlsw' if traps.dlsw.enable is defined else '' }}"
                      "{{ ' circuit' if traps.dlsw.circuit|d(False) else ''}}"
                      "{{ ' tconn' if traps.dlsw.tconn|d(False) else ''}}",
            "result": {
                "traps": {
                    "dlsw": {
                        "enable": True,
                        "circuit": "{{ not not circuit }}",
                        "tconn": "{{ not not tconn }}",
                    },
                },
            },
        },
        {
            "name": "traps.ethernet.evc",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sethernet\sevc
                (\s(?P<status>status))?
                (\s(?P<create>create))?
                (\s(?P<delete>delete))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ethernet evc"
                      "{{ ' create' if traps.ethernet.evc.create|d(False) else ''}}"
                      "{{ ' delete' if traps.ethernet.evc.delete|d(False) else ''}}"
                      "{{ ' status' if traps.ethernet.evc.status|d(False) else ''}}",
            "result": {
                "traps": {
                    "ethernet": {
                        "evc": {
                            "create": "{{ not not create }}",
                            "delete": "{{ not not delete }}",
                            "status": "{{ not not status }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ethernet.cfm.cc",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sethernet\scfm\scc
                (\s(?P<mep_up>mep-up))?
                (\s(?P<mep_down>mep-down))?
                (\s(?P<cross_connect>cross-connect))?
                (\s(?P<loop>loop))?
                (\s(?P<config>config))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ethernet cfm cc"
                      "{{ ' mep-up' if traps.ethernet.cfm.cc.mep_up|d(False) else ''}}"
                      "{{ ' mep-down' if traps.ethernet.cfm.cc.mep_down|d(False) else ''}}"
                      "{{ ' cross-connect' if traps.ethernet.cfm.cc.cross_connect|d(False) else ''}}"
                      "{{ ' loop' if traps.ethernet.cfm.cc.loop|d(False) else ''}}"
                      "{{ ' config' if traps.ethernet.cfm.cc.config|d(False) else ''}}",
            "result": {
                "traps": {
                    "ethernet": {
                        "cfm": {
                            "cc": {
                                "mep_up": "{{ not not mep_up }}",
                                "mep_down": "{{ not not mep_down }}",
                                "cross_connect": "{{ not not cross_connect }}",
                                "loop": "{{ not not loop }}",
                                "config": "{{ not not config }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ethernet.cfm.crosscheck",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sethernet\scfm\scrosscheck
                (\s(?P<mep_missing>mep-missing))?
                (\s(?P<mep_unknown>mep-unknown))?
                (\s(?P<service_up>service-up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ethernet cfm crosscheck"
                      "{{ ' mep-missing' if traps.ethernet.cfm.crosscheck.mep_missing|d(False) else ''}}"
                      "{{ ' mep-unknown' if traps.ethernet.cfm.crosscheck.mep_unknown|d(False) else ''}}"
                      "{{ ' service-up' if traps.ethernet.cfm.crosscheck.service_up|d(False) else ''}}",
            "result": {
                "traps": {
                    "ethernet": {
                        "cfm": {
                            "crosscheck": {
                                "mep_missing": "{{ not not mep_missing }}",
                                "mep_unknown": "{{ not not mep_unknown }}",
                                "service_up": "{{ not not service_up }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ethernet.cfm.alarm",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sethernet\scfm\salarm
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ethernet cfm alarm",
            "result": {
                "traps": {
                    "ethernet": {
                        "cfm": {
                            "alarm": True,
                        },
                    },
                },
            },
        },
        {
            "name": "system_shutdown",
            "getval": re.compile(
                r"""
                ^snmp-server\ssystem-shutdown
                """, re.VERBOSE,
            ),
            "setval": "snmp-server system-shutdown",
            "result": {
                "system_shutdown": True,
            },
        },
    ]
    # fmt: on
