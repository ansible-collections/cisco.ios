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
        if config_data.get("vrf"):
            cmd += " vrf {vrf}".format(vrf=config_data.get("vrf"))
        if config_data.get("version"):
            cmd += " version {version}".format(version=config_data.get("version"))
        if config_data.get("version_option"):
            cmd += " {version}".format(version=config_data.get("version_option"))
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
                (\smatch\s(?P<match>\S+))?
                (\sread\s(?P<read>\S+))?
                (\swrite\s(?P<write>\S+))?
                (\snotify\s(?P<notify>\S+))?
                (\saccess(\sipv6\s(?P<acl_v6>\S+))?(\s(?P<acl_v4>\S+|\d+))?)?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server group "
                      "{{ group if group is defined else '' }}"
                      "{{ (' ' + version) if version is defined else '' }}"
                      "{{ (' ' + version_option) if version_option is defined else '' }}"
                      "{{ (' context ' + context) if context is defined else '' }}"
                      "{{ (' match ' + match) if match is defined else '' }}"
                      "{{ (' read ' + read) if read is defined else '' }}"
                      "{{ (' write ' + write) if write is defined else '' }}"
                      "{{ (' notify ' + notify) if notify is defined else '' }}"
                      "{{ (' access') if acl_v6 is defined or acl_v4 is defined else '' }}"
                      "{{ (' ipv6 ' + acl_v6) if acl_v6 is defined else '' }}"
                      "{{ (' ' + acl_v4|string) if acl_v4 is defined else '' }}",
            "result": {
                "groups": [
                    {
                        "group": "{{ group }}",
                        "version": "{{ version }}",
                        "version_option": "{{ version_option }}",
                        "context": "{{ context }}",
                        "match": "{{ match }}",
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
                (\svrf\s(?P<vrf>\S+))?
                (\sversion\s(?P<version>1|3|2c))?
                (\s(?P<version_option>auth|noauth|priv))?
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
                (\s(?P<version_option>encrypted))?
                (\saccess(\sipv6\s(?P<acl_v6>\S+))?(\s(?P<acl_v4>\S+|\d+))?)?
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
                      "{% if authentication is defined and 'algorithm' in authentication and 'password' in authentication %}"
                      "{{ (' auth ' + authentication.algorithm + ' ' + authentication.password) }}"
                      "{% if encryption is defined and 'priv' in encryption and 'password' in encryption %}"
                      "{{ (' priv ' + encryption.priv) }}"
                      "{{ (' ' + encryption.priv_option) if 'priv_option' in encryption else '' }}"
                      "{{ (' ' + encryption.password) }}"
                      "{% endif %}"
                      "{% endif %}"
                      "{{ (' access') if acl_v6 is defined or acl_v4 is defined else '' }}"
                      "{{ (' ipv6 ' + acl_v6) if acl_v6 is defined else '' }}"
                      "{{ (' ' + acl_v4|string) if acl_v4 is defined else '' }}"
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
                ^snmp(-server|\sifmib)\sifindex
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
                (\sprecedence\s(?P<precedence>\d+))?
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
        # only traps
        {
            "name": "traps.aaa_server",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\saaa_server
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps aaa_server",
            "result": {
                "traps": {
                    "aaa_server": True,
                },
            },
        },
        {
            "name": "traps.auth_framework",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sauth-framework
                (\s(?P<sec_violation>sec-violation))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps auth-framework"
                      "{{ (' sec-violation') if traps.auth_framework.sec_violation|d(False) is defined else '' }}",
            "result": {
                "traps": {
                    "auth_framework": {
                        "enable": True,
                        "sec_violation": "{{ not not sec_violation }}",
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
                (\s(?P<state_changes>state-changes))?
                (\s(?P<all>all))?
                (\s(?P<backward_trans>backward-trans))?
                (\s(?P<limited>limited))?
                (\sthreshold(?P<prefix>prefix))?\s*$
                """, re.VERBOSE,
            ),
            "setval": cmd_option_trap_bgp,
            "remval": "snmp-server enable traps bgp",
            "result": {
                "traps": {
                    "bgp": {
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
            "name": "traps.bgp.cbgp2",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sbgp\scbgp2
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps bgp cbgp2",
            "result": {
                "traps": {
                    "bgp": {
                        "cbgp2": True,
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
            "name": "traps.bulkstat",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sbulkstat
                (\s(?P<collection>collection))?
                (\s(?P<transfer>transfer))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps bulkstat"
                      "{{ ' collection' if traps.bulkstat.collection|d(False) else '' }}"
                      "{{ ' transfer' if traps.bulkstat.transfer|d(False) else '' }}",
            "result": {
                "traps": {
                    "bulkstat": {
                        "enable": True,
                        "collection": "{{ not not collection }}",
                        "transfer": "{{ not not transfer }}",
                    },
                },
            },
        },
        {
            "name": "traps.call_home",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\scall-home
                (\s(?P<message_send_fail>message-send-fail))?
                (\s(?P<server_fail>server-fail))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps call-home"
                      "{{ ' message-send-fail' if traps.call_home.message_send_fail|d(False) else '' }}"
                      "{{ ' server-fail' if traps.call_home.server_fail|d(False) else '' }}",
            "result": {
                "traps": {
                    "call_home": {
                        "enable": True,
                        "message_send_fail": "{{ not not message_send_fail }}",
                        "server_fail": "{{ not not server_fail }}",
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
            "setval": "snmp-server enable traps cef"
                      "{{ ' resource-failure' if traps.cef.resource_failure|d(False) else '' }}"
                      "{{ ' peer-state-change' if traps.cef.peer_state_change|d(False) else '' }}"
                      "{{ ' peer-fib-state-change' if traps.cef.peer_fib_state_change|d(False) else '' }}"
                      "{{ ' inconsistency' if traps.cef.inconsistency|d(False) else '' }}",
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
                ^snmp-server\senable\straps\sconfig\s*$
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
            "name": "traps.config_copy",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\s(config-copy|copy-config)
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
            "name": "traps.cpu",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\scpu
                ((?P<threshold_old>_threshold))?
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps cpu"
                      "{{ ' threshold' if traps.cpu.threshold|d(False) else '' }}",
            "result": {
                "traps": {
                    "cpu": {
                        "enable": True,
                        "threshold": "{{ not not threshold or not not threshold_old }}",
                    },
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
            "name": "traps.dlsw",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sdlsw
                (\s(?P<circuit>circuit))?
                (\s(?P<tconn>tconn))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps dlsw"
                      "{{ ' circuit' if traps.dlsw.circuit|d(False) else '' }}"
                      "{{ ' tconn' if traps.dlsw.tconn|d(False) else '' }}",
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
            "name": "traps.entity",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sentity\s*$
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
            "name": "traps.entity_diag",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sentity-diag
                (\s(?P<boot_up_fail>boot-up-fail))?
                (\s(?P<hm_test_recover>hm-test-recover))?
                (\s(?P<hm_thresh_reached>hm-thresh-reached))?
                (\s(?P<scheduled_test_fail>scheduled-test-fail))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps entity-diag"
                      "{{ ' boot-up-fail' if traps.entity_diag.boot_up_fail|d(False) else '' }}"
                      "{{ ' hm-test-recover' if traps.entity_diag.hm_test_recover|d(False) else '' }}"
                      "{{ ' hm-thresh-reached' if traps.entity_diag.hm_thresh_reached|d(False) else '' }}"
                      "{{ ' scheduled-test-fail' if traps.entity_diag.scheduled_test_fail|d(False) else '' }}",
            "result": {
                "traps": {
                    "entity_diag": {
                        "enable": True,
                        "boot_up_fail": "{{ not not boot_up_fail }}",
                        "hm_test_recover": "{{ not not hm_test_recover }}",
                        "hm_thresh_reached": "{{ not not hm_thresh_reached }}",
                        "scheduled_test_fail": "{{ not not scheduled_test_fail }}",
                    },
                },
            },
        },
        {
            "name": "traps.entity_perf",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sentity-perf
                (\s(?P<throughput_notif>throughput-notif))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps entity-perf"
                      "{{ ' throughput-notif' if traps.entity_perf.throughput_notif|d(False) else '' }}",
            "result": {
                "traps": {
                    "entity_perf": {
                        "enable": True,
                        "throughput_notif": "{{ not not throughput_notif }}",
                    },
                },
            },
        },
        {
            "name": "traps.entity_state",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sentity-state
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps entity-state",
            "result": {
                "traps": {
                    "entity_state": True,
                },
            },
        },
        {
            "name": "traps.envmon",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\senvmon
                (\s(?P<fan>fan))?
                (\s(?P<shutdown>shutdown))?
                (\s(?P<supply>supply))?
                (\s(?P<temperature>temperature))?
                (\s(?P<status>status))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps envmon"
                      "{{ ' fan' if traps.envmon.fan_enable|d(False) else '' }}"
                      "{{ ' shutdown' if traps.envmon.shutdown|d(False) else '' }}"
                      "{{ ' supply' if traps.envmon.supply|d(False) else '' }}"
                      "{{ ' temperature' if traps.envmon.temperature|d(False) else '' }}"
                      "{{ ' status' if traps.envmon.status|d(False) else '' }}",
            "result": {
                "traps": {
                    "envmon": {
                        "enable": True,
                        "fan_enable": "{{ True if fan else False }}",
                        "shutdown": "{{ True if shutdown else False }}",
                        "supply": "{{ True if supply else False }}",
                        "temperature": "{{ True if temperature else False }}",
                        "status": "{{ True if status else False }}",
                    },
                },
            },
        },
        {
            "name": "traps.errdisable",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\serrdisable
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps errdisable",
            "result": {
                "traps": {
                    "errdisable": True,
                },
            },
        },
        {
            "name": "traps.ether_oam",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sether-oam
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ether-oam",
            "result": {
                "traps": {
                    "ether_oam": True,
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
                      "{{ ' status' if traps.ethernet.evc.status|d(False) else ''}}"
                      "{{ ' create' if traps.ethernet.evc.create|d(False) else ''}}"
                      "{{ ' delete' if traps.ethernet.evc.delete|d(False) else ''}}",
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
            "name": "traps.flash",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sflash
                (\s(?P<insertion>insertion))?
                (\s(?P<removal>removal))?
                (\s(?P<lowspace>lowspace))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps flash"
                      "{{ ' insertion' if traps.flash.insertion|d(False) else '' }}"
                      "{{ ' removal' if traps.flash.removal|d(False) else '' }}"
                      "{{ ' lowspace' if traps.flash.lowspace|d(False) else '' }}",
            "result": {
                "traps": {
                    "flash": {
                        "enable": True,
                        "insertion": "{{ not not insertion }}",
                        "removal": "{{ not not removal }}",
                        "lowspace": "{{ not not lowspace }}",
                    },
                },
            },
        },
        {
            "name": "traps.flex_links",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sflex-links
                (\s(?P<status>status))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps flex-links"
                      "{{ ' status' if traps.flex_links.status|d(False) else '' }}",
            "result": {
                "traps": {
                    "flex_links": {
                        "enable": True,
                        "status": "{{ not not status }}",
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
            "setval": "snmp-server enable traps firewall"
                      "{{ ' serverstatus' if traps.firewall.serverstatus|d(False) else '' }}",
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
            "name": "traps.frame_relay",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\s(framerelay|frame-relay)$
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
                (\sinterval(?P<interval>\d+))?
                (\scount(?P<count>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps frame-relay subif"
                      "{{ ' interval ' + interval|string if traps.frame_relay.subif.interval|d(False) else '' }}"
                      "{{ ' count ' + count|string if traps.frame_relay.subif.count|d(False) else '' }}",
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
            "name": "traps.l2tc",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sl2tc
                (\s(?P<threshold>threshold))?
                (\s(?P<sys_threshold>sys-threshold))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps l2tc"
                      "{{ ' threshold' if traps.l2tc.threshold|d(False) else '' }}"
                      "{{ ' sys-threshold' if traps.l2tc.sys_threshold|d(False) else '' }}",
            "result": {
                "traps": {
                    "l2tc": {
                        "enable": True,
                        "sys_threshold": "{{ not not sys_threshold }}",
                        "threshold": "{{ not not threshold }}",
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
            "name": "traps.license",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\slicense
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps license",
            "result": {
                "traps": {
                    "license": True,
                },
            },
        },
        {
            "name": "traps.lisp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\slisp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps lisp",
            "result": {
                "traps": {
                    "lisp": True,
                },
            },
        },
        {
            "name": "traps.local_auth",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\slocal-auth
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps local-auth",
            "result": {
                "traps": {
                    "local_auth": True,
                },
            },
        },
        {
            "name": "traps.mac_notification",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smac-notification
                (\s(?P<change>change))?
                (\s(?P<move>move))?
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mac-notification"
                      "{{ ' change' if traps.mac_notification.change|d(False) else '' }}"
                      "{{ ' move' if traps.mac_notification.move|d(False) else '' }}"
                      "{{ ' threshold' if traps.mac_notification.threshold|d(False) else '' }}",
            "result": {
                "traps": {
                    "mac_notification": {
                        "enable": True,
                        "change": "{{ not not change }}",
                        "move": "{{ not not move }}",
                        "threshold": "{{ not not threshold }}",
                    },
                },
            },
        },
        {
            "name": "traps.memory",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smemory
                (\s(?P<bufferpeak>bufferpeak))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps memory"
                      "{{ ' bufferpeak' if traps.memory.bufferpeak|d(False) else '' }}",
            "result": {
                "traps": {
                    "memory": {
                        "enable": True,
                        "bufferpeak": "{{ not not bufferpeak }}",
                    },
                },
            },
        },
        {
            "name": "traps.mpls.fast_reroute",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\sfast-reroute
                (\s(?P<protected>protected))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls fast-reroute"
                      "{{ ' protected' if traps.mpls.fast_reroute.protected|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "fast_reroute": {
                            "enable": True,
                            "protected": "{{ not not protected }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.ldp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\sldp
                (\s(?P<pv_limit>pv-limit))?
                (\s(?P<session_down>session-down))?
                (\s(?P<session_up>session-up))?
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls ldp"
                      "{{ ' pv-limit' if traps.mpls.ldp.pv_limit|d(False) else '' }}"
                      "{{ ' session-down' if traps.mpls.ldp.session_down|d(False) else '' }}"
                      "{{ ' session-up' if traps.mpls.ldp.session_up|d(False) else '' }}"
                      "{{ ' threshold' if traps.mpls.ldp.threshold|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "ldp": {
                            "enable": True,
                            "pv_limit": "{{ not not pv_limit }}",
                            "session_down": "{{ not not session_down }}",
                            "session_up": "{{ not not session_up }}",
                            "threshold": "{{ not not threshold }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.rfc.ldp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\srfc\sldp
                (\s(?P<pv_limit>pv-limit))?
                (\s(?P<session_down>session-down))?
                (\s(?P<session_up>session-up))?
                (\s(?P<threshold>threshold))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls rfc ldp"
                      "{{ ' pv-limit'     if traps.mpls.rfc.ldp.pv_limit|d(False) else '' }}"
                      "{{ ' session-down' if traps.mpls.rfc.ldp.session_down|d(False) else '' }}"
                      "{{ ' session-up'   if traps.mpls.rfc.ldp.session_up|d(False) else '' }}"
                      "{{ ' threshold'    if traps.mpls.rfc.ldp.threshold|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "rfc": {
                            "ldp": {
                                "enable": True,
                                "pv_limit": "{{ not not pv_limit }}",
                                "session_down": "{{ not not session_down }}",
                                "session_up": "{{ not not session_up }}",
                                "threshold": "{{ not not threshold }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.rfc.traffic_eng",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\srfc\straffic-eng
                (\s(?P<down>down))?
                (\s(?P<reoptimized>reoptimized))?
                (\s(?P<reroute>reroute))?
                (\s(?P<up>up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls rfc traffic-eng"
                      "{{ ' down'           if traps.mpls.rfc.traffic_eng.down|d(False) else '' }}"
                      "{{ ' reoptimized'    if traps.mpls.rfc.traffic_eng.reoptimized|d(False) else '' }}"
                      "{{ ' reroute'        if traps.mpls.rfc.traffic_eng.reroute|d(False) else '' }}"
                      "{{ ' up'             if traps.mpls.rfc.traffic_eng.up|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "rfc": {
                            "traffic_eng": {
                                "enable": True,
                                "down": "{{ not not down }}",
                                "reoptimized": "{{ not not reoptimized }}",
                                "reroute": "{{ not not reroute }}",
                                "up": "{{ not not up }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.rfc.vpn",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\srfc\svpn
                (\s(?P<illegal_label>illegal-label))?
                (\s(?P<max_thresh_cleared>max-thresh-cleared))?
                (\s(?P<max_threshold>max-threshold))?
                (\s(?P<mid_threshold>mid-threshold))?
                (\s(?P<vrf_down>vrf-down))?
                (\s(?P<vrf_up>vrf-up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls rfc vpn"
                      "{{ ' illegal-label'      if traps.mpls.rfc.vpn.illegal_label|d(False) else '' }}"
                      "{{ ' max-thresh-cleared' if traps.mpls.rfc.vpn.max_thresh_cleared|d(False) else '' }}"
                      "{{ ' max-threshold'      if traps.mpls.rfc.vpn.max_threshold|d(False) else '' }}"
                      "{{ ' mid-threshold'      if traps.mpls.rfc.vpn.mid_threshold|d(False) else '' }}"
                      "{{ ' vrf-down'           if traps.mpls.rfc.vpn.vrf_down|d(False) else '' }}"
                      "{{ ' vrf-up'             if traps.mpls.rfc.vpn.vrf_up|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "rfc": {
                            "vpn": {
                                "enable": True,
                                "illegal_label": "{{ not not illegal_label }}",
                                "max_thresh_cleared": "{{ not not max_thresh_cleared }}",
                                "max_threshold": "{{ not not max_threshold }}",
                                "mid_threshold": "{{ not not mid_threshold }}",
                                "vrf_down": "{{ not not vrf_down }}",
                                "vrf_up": "{{ not not vrf_up }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.traffic_eng",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls\straffic-eng
                (\s(?P<down>down))?
                (\s(?P<reroute>reroute))?
                (\s(?P<up>up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps mpls traffic-eng"
                      "{{ ' down' if traps.mpls.traffic_eng.down|d(False) else '' }}"
                      "{{ ' reroute' if traps.mpls.traffic_eng.reroute|d(False) else '' }}"
                      "{{ ' up' if traps.mpls.traffic_eng.up|d(False) else '' }}",
            "result": {
                "traps": {
                    "mpls": {
                        "traffic_eng": {
                            "enable": True,
                            "down": "{{ not not down }}",
                            "reroute": "{{ not not reroute }}",
                            "up": "{{ not not up }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.mpls.vpn",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\smpls(-|\s)vpn
                (\s(?P<illegal_label>illegal-label))?
                (\s(?P<max_thresh_cleared>max-thresh-cleared))?
                (\s(?P<max_threshold>max-threshold))?
                (\s(?P<mid_threshold>mid-threshold))?
                (\s(?P<vrf_down>vrf-down))?
                (\s(?P<vrf_up>vrf-up))?
                """, re.VERBOSE,
            ),
            "setval": "{% if 'vpn' in traps.mpls and traps.mpls.vpn.enable %}"
                      "snmp-server enable traps mpls vpn"
                      "{{ ' illegal-label' if traps.mpls.vpn.illegal_label|d(False) else '' }}"
                      "{{ ' max-thresh-cleared' if traps.mpls.vpn.max_thresh_cleared|d(False) else '' }}"
                      "{{ ' max-threshold' if traps.mpls.vpn.max_threshold|d(False) else '' }}"
                      "{{ ' mid-threshold' if traps.mpls.vpn.mid_threshold|d(False) else '' }}"
                      "{{ ' vrf-down' if traps.mpls.vpn.vrf_down|d(False) else '' }}"
                      "{{ ' vrf-up' if traps.mpls.vpn.vrf_up|d(False) else '' }}"
                      "{% endif %}",
            "result": {
                "traps": {
                    "mpls": {
                        "vpn": {
                            "enable": True,
                            "illegal_label": "{{ not not illegal_label }}",
                            "max_thresh_cleared": "{{ not not max_thresh_cleared }}",
                            "max_threshold": "{{ not not max_threshold }}",
                            "mid_threshold": "{{ not not mid_threshold }}",
                            "vrf_down": "{{ not not vrf_down }}",
                            "vrf_up": "{{ not not vrf_up }}",
                        },
                    },
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
            "name": "traps.nhrp.nhc",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\snhrp\snhc
                (\s(?P<down>down))?
                (\s(?P<up>up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps nhrp nhc"
                      "{{ ' down' if traps.nhrp.nhc.down|d(False) else '' }}"
                      "{{ ' up' if traps.nhrp.nhc.up|d(False) else '' }}",
            "result": {
                "traps": {
                    "nhrp": {
                        "enable": True,
                        "nhc": {
                            "enable": True,
                            "down": "{{ not not down }}",
                            "up": "{{ not not up }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.nhrp.nhp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\snhrp\snhp
                (\s(?P<down>down))?
                (\s(?P<up>up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps nhrp nhp"
                      "{{ ' down' if traps.nhrp.nhc.down|d(False) else '' }}"
                      "{{ ' up' if traps.nhrp.nhc.up|d(False) else '' }}",
            "result": {
                "traps": {
                    "nhrp": {
                        "enable": True,
                        "nhp": {
                            "enable": True,
                            "down": "{{ not not down }}",
                            "up": "{{ not not up }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.nhrp.nhs",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\snhrp\snhs
                (\s(?P<down>down))?
                (\s(?P<up>up))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps nhrp nhs"
                      "{{ ' down' if traps.nhrp.nhc.down|d(False) else '' }}"
                      "{{ ' up' if traps.nhrp.nhc.up|d(False) else '' }}",
            "result": {
                "traps": {
                    "nhrp": {
                        "enable": True,
                        "nhs": {
                            "enable": True,
                            "down": "{{ not not down }}",
                            "up": "{{ not not up }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.nhrp.quota_exceeded",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\snhrp
                (\s(?P<quota_exceeded>quota-exceeded))?$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps nhrp"
                      "{{ ' quota-exceeded' if traps.nhrp.quota_exceeded|d(False) else '' }}",
            "result": {
                "traps": {
                    "nhrp": {
                        "enable": True,
                        "quota_exceeded": "{{ not not quota_exceeded }}",
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
            "name": "traps.ospfv3.errors",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospfv3\serrors
                (\s(?P<bad_packet>bad-packet))?
                (\s(?P<config_error>config-error))?
                (\s(?P<virt_bad_packet>virt-bad-packet))?
                (\s(?P<virt_config_error>virt-config-error))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospfv3 errors"
                      "{{ ' bad-packet' if traps.ospfv3.errors.bad_packet|d(False) else '' }}"
                      "{{ ' config-error' if traps.ospfv3.errors.config_error|d(False) else '' }}"
                      "{{ ' virt-bad-packet' if traps.ospfv3.errors.virt_bad_packet|d(False) else '' }}"
                      "{{ ' virt-config-error' if traps.ospfv3.errors.virt_config_error|d(False) else '' }}",
            "result": {
                "traps": {
                    "ospfv3": {
                        "errors": {
                            "enable": True,
                            "bad_packet": "{{ not not bad_packet }}",
                            "config_error": "{{ not not config_error }}",
                            "virt_bad_packet": "{{ not not virt_bad_packet }}",
                            "virt_config_error": "{{ not not virt_config_error }}",
                        },
                    },
                },
            },
        },
        {
            "name": "traps.ospfv3.rate_limit",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospfv3\srate-limit
                (\s(?P<rate_limit>[0-9]+))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospfv3 rate_limit"
                      "{{ traps.ospfv3.rate_limit|int if traps.ospfv3.rate_limit|int > 0 else '' }}",
            "result": {
                "traps": {
                    "ospfv3": {
                        "rate_limit": "{{ rate_limit if rate_limit|int >=2  or rate_limit|int <= 60 }}",
                    },
                },
            },
        },
        {
            "name": "traps.ospfv3.state_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sospfv3\sstate-change
                (\s(?P<if_state_change>if-state-change))?
                (\s(?P<neighbor_restart_helper_status_change>neighbor-restart-helper-status-change))?
                (\s(?P<neighbor_state_change>neighbor-state-change))?
                (\s(?P<nssa_translator_status_change>nssa-translator-status-change))?
                (\s(?P<restart_status_change>restart-status-change))?
                (\s(?P<virtif_state_change>virtif-state-change))?
                (\s(?P<virtneighbor_restart_helper_status_change>virtneighbor-restart-helper-status-change))?
                (\s(?P<virtneighbor_state_change>virtneighbor-state-change))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps ospfv3 state-change"
                      "{{ ' if-state-change' if traps.ospfv3.state_change.if_state_change|d(False) else '' }}"
                      "{{ ' neighbor-restart-helper-status-change' if traps.ospfv3.state_change.neighbor_restart_helper_status_change|d(False) else '' }}"
                      "{{ ' neighbor-state-change' if traps.ospfv3.state_change.neighbor_state_change|d(False) else '' }}"
                      "{{ ' nssa-translator-status-change' if traps.ospfv3.state_change.nssa_translator_status_change|d(False) else '' }}"
                      "{{ ' restart-status-change' if traps.ospfv3.state_change.restart_status_change|d(False) else '' }}"
                      "{{ ' virtif-state-change' if traps.ospfv3.state_change.virtif_state_change|d(False) else '' }}"
                      "{{ ' virtneighbor-restart-helper-status-change' if traps.ospfv3.state_change.vn_restart_helper_status_change|d(False) else '' }}"
                      "{{ ' virtneighbor-state-change' if traps.ospfv3.state_change.vn_state_change|d(False) else '' }}",
            "result": {
                "traps": {
                    "ospfv3": {
                        "state_change": {
                            "enable": True,
                            "if_state_change": "{{ not not if_state_change }}",
                            "neighbor_restart_helper_status_change": "{{ not not neighbor_restart_helper_status_change }}",
                            "neighbor_state_change": "{{ not not neighbor_state_change }}",
                            "nssa_translator_status_change": "{{ not not nssa_translator_status_change }}",
                            "restart_status_change": "{{ not not restart_status_change }}",
                            "virtif_state_change": "{{ not not virtif_state_change }}",
                            "vn_restart_helper_status_change": "{{ not not virtneighbor_restart_helper_status_change }}",
                            "vn_state_change": "{{ not not virtneighbor_state_change }}",
                        },
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
            "name": "traps.port_security",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sport-security
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps port-security",
            "result": {
                "traps": {
                    "port_security": True,
                },
            },
        },
        {
            "name": "traps.power_ethernet",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\spower-ethernet
                (\s(?P<police>police))?$
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps power-ethernet"
                      "{{ ' police' if traps.power_ethernet.police|d(False) else '' }}",
            "result": {
                "traps": {
                    "power_ethernet": {
                        "enable": True,
                        "police": "{{ not not police }}",
                    },
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
            "name": "traps.rep",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\srep
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps rep",
            "result": {
                "traps": {
                    "rep": True,
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
            "name": "traps.rf",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\srf
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps rf",
            "result": {
                "traps": {
                    "rf": True,
                },
            },
        },
        {
            "name": "traps.smart_license",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\ssmart-license
                (\s(?P<entitlement>entitlement))?
                (\s(?P<global>global))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps smart-license"
                      "{{ ' entitlement' if traps.smart_license.entitlement|d(False) else '' }}"
                      "{{ ' global' if traps.smart_license.global|d(False) else '' }}",
            "result": {
                "traps": {
                    "smart_license": {
                        "enable": True,
                        "entitlement": "{{ not not entitlement }}",
                        "global": "{{ not not global }}",
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
                      "{{ ' coldstart' if traps.snmp.coldstart|d(False) else ''}}"
                      "{{ ' warmstart' if traps.snmp.warmstart|d(False) else ''}}",
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
            "name": "traps.stackwise",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sstackwise
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps stackwise",
            "result": {
                "traps": {
                    "stackwise": True,
                },
            },
        },
        {
            "name": "traps.stpx",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sstpx
                (\s(?P<inconsistency>inconsistency))?
                (\s(?P<root_inconsistency>root-inconsistency))?
                (\s(?P<loop_inconsistency>loop-inconsistency))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps stpx"
                      "{{ ' inconsistency' if traps.stpx.inconsistency|d(False) else '' }}"
                      "{{ ' root-inconsistency' if traps.stpx.root_inconsistency|d(False) else '' }}"
                      "{{ ' loop-inconsistency' if traps.stpx.loop_inconsistency|d(False) else '' }}",
            "result": {
                "traps": {
                    "stpx": {
                        "enable": True,
                        "inconsistency": "{{ not not inconsistency }}",
                        "loop_inconsistency": "{{ not not loop_inconsistency }}",
                        "root_inconsistency": "{{ not not root_inconsistency }}",
                    },
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
                ^snmp-server\senable\straps\stransceiver\sall
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps transceiver all",
            "result": {
                "traps": {
                    "transceiver_all": True,
                },
            },
        },
        {
            "name": "traps.trustsec",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\strustsec
                (?!\S)
                (\s(?P<authz_file_error>authz-file-error))?
                (\s(?P<cache_file_error>cache-file-error))?
                (\s(?P<keystore_file_error>keystore-file-error))?
                (\s(?P<keystore_sync_fail>keystore-sync-fail))?
                (\s(?P<random_number_fail>random-number-fail))?
                (\s(?P<src_entropy_fail>src-entropy-fail))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps trustsec"
                      "{{ ' authz-file-error' if traps.trustsec.authz_file_error|d(False) else '' }}"
                      "{{ ' cache-file-error' if traps.trustsec.cache_file_error|d(False) else '' }}"
                      "{{ ' keystore-file-error' if traps.trustsec.keystore_file_error|d(False) else '' }}"
                      "{{ ' keystore-sync-fail' if traps.trustsec.keystore_sync_fail|d(False) else '' }}"
                      "{{ ' random-number-fail' if traps.trustsec.random_number_fail|d(False) else '' }}"
                      "{{ ' src-entropy-fail' if traps.trustsec.src_entropy_fail|d(False) else '' }}",
            "result": {
                "traps": {
                    "trustsec": {
                        "enable": True,
                        "authz_file_error": "{{ not not authz_file_error }}",
                        "cache_file_error": "{{ not not cache_file_error }}",
                        "keystore_file_error": "{{ not not keystore_file_error }}",
                        "keystore_sync_fail": "{{ not not keystore_sync_fail }}",
                        "random_number_fail": "{{ not not random_number_fail }}",
                        "src_entropy_fail": "{{ not not src_entropy_fail }}",
                    },
                },
            },
        },
        {
            "name": "traps.trustsec_interface",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\strustsec-interface
                (\s(?P<unauthorized>unauthorized))?
                (\s(?P<sap_fail>sap-fail))?
                (\s(?P<authc_fail>authc-fail))?
                (\s(?P<supplicant_fail>supplicant-fail))?
                (\s(?P<authz_fail>authz-fail))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps trustsec-interface"
                      "{{ ' unauthorized' if traps.trustsec_interface.unauthorized|d(False) else '' }}"
                      "{{ ' sap-fail' if traps.trustsec_interface.sap_fail|d(False) else '' }}"
                      "{{ ' authc-fail' if traps.trustsec_interface.authc_fail|d(False) else '' }}"
                      "{{ ' supplicant-fail' if traps.trustsec_interface.supplicant_fail|d(False) else '' }}"
                      "{{ ' authz-fail' if traps.trustsec_interface.authz_fail|d(False) else '' }}",
            "result": {
                "traps": {
                    "trustsec_interface": {
                        "enable": True,
                        "unauthorized": "{{ not not unauthorized }}",
                        "sap_fail": "{{ not not sap_fail }}",
                        "authc_fail": "{{ not not authc_fail }}",
                        "supplicant_fail": "{{ not not supplicant_fail }}",
                        "authz_fail": "{{ not not authz_fail }}",
                    },
                },
            },
        },
        {
            "name": "traps.trustsec_policy",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\strustsec-policy
                (\s(?P<peer_policy_updated>peer-policy-updated))?
                (\s(?P<authz_sgacl_fail>authz-sgacl-fail))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps trustsec-policy"
                      "{{ ' peer-policy-updated' if traps.trustsec_policy.peer_policy_updated|d(False) else '' }}"
                      "{{ ' authz-sgacl-fail' if traps.trustsec_policy.authz_sgacl_fail|d(False) else '' }}",
            "result": {
                "traps": {
                    "trustsec_policy": {
                        "enable": True,
                        "peer_policy_updated": "{{ not not peer_policy_updated }}",
                        "authz_sgacl_fail": "{{ not not authz_sgacl_fail }}",
                    },
                },
            },
        },
        {
            "name": "traps.trustsec_server",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\strustsec-server
                (\s(?P<radius_server>radius-server))?
                (\s(?P<provision_secret>provision-secret))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps trustsec-server"
                      "{{ ' radius-server' if traps.trustsec_server.radius_server|d(False) else '' }}"
                      "{{ ' provision-secret' if traps.trustsec_server.provision_secret|d(False) else '' }}",
            "result": {
                "traps": {
                    "trustsec_server": {
                        "enable": True,
                        "radius_server": "{{ not not radius_server }}",
                        "provision_secret": "{{ not not provision_secret }}",
                    },
                },
            },
        },
        {
            "name": "traps.trustsec_sxp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\strustsec-sxp
                (\s(?P<conn_srcaddr_err>conn-srcaddr-err))?
                (\s(?P<msg_parse_err>msg-parse-err))?
                (\s(?P<conn_config_err>conn-config-err))?
                (\s(?P<binding_err>binding-err))?
                (\s(?P<conn_up>conn-up))?
                (\s(?P<conn_down>conn-down))?
                (\s(?P<binding_expn_fail>binding-expn-fail))?
                (\s(?P<oper_nodeid_change>oper-nodeid-change))?
                (\s(?P<binding_conflict>binding-conflict))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps trustsec-sxp"
                      "{{ ' conn-srcaddr-err' if traps.trustsec_sxp.conn_srcaddr_err|d(False) else '' }}"
                      "{{ ' msg-parse-err' if traps.trustsec_sxp.msg_parse_err|d(False) else '' }}"
                      "{{ ' conn-config-err' if traps.trustsec_sxp.conn_config_err|d(False) else '' }}"
                      "{{ ' binding-err' if traps.trustsec_sxp.binding_err|d(False) else '' }}"
                      "{{ ' conn-up' if traps.trustsec_sxp.conn_up|d(False) else '' }}"
                      "{{ ' conn-down' if traps.trustsec_sxp.conn_down|d(False) else '' }}"
                      "{{ ' binding-expn-fail' if traps.trustsec_sxp.binding_expn_fail|d(False) else '' }}"
                      "{{ ' oper-nodeid-change' if traps.trustsec_sxp.oper_nodeid_change|d(False) else '' }}"
                      "{{ ' binding-conflict' if traps.trustsec_sxp.binding_conflict|d(False) else '' }}",
            "result": {
                "traps": {
                    "trustsec_sxp": {
                        "enable": True,
                        "conn_srcaddr_err": "{{ not not conn_srcaddr_err }}",
                        "msg_parse_err": "{{ not not msg_parse_err }}",
                        "conn_config_err": "{{ not not conn_config_err }}",
                        "binding_err": "{{ not not binding_err }}",
                        "conn_up": "{{ not not conn_up }}",
                        "conn_down": "{{ not not conn_down }}",
                        "binding_expn_fail": "{{ not not binding_expn_fail }}",
                        "oper_nodeid_change": "{{ not not oper_nodeid_change }}",
                        "binding_conflict": "{{ not not binding_conflict }}",
                    },
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
            "name": "traps.udld",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\sudld
                (\s(?P<link_fail_rpt>link-fail-rpt))?
                (\s(?P<status_change>status-change))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps udld"
                      "{{ ' link-fail-rpt' if traps.udld.link_fail_rpt|d(False) else '' }}"
                      "{{ ' status-change' if traps.udld.status_change|d(False) else '' }}",
            "result": {
                "traps": {
                    "udld": {
                        "enable": True,
                        "link_fail_rpt": "{{ not not link_fail_rpt }}",
                        "status_change": "{{ not not status_change }}",
                    },
                },
            },
        },
        {
            "name": "traps.vlan_membership",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svlan-membership
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vlan-membership",
            "result": {
                "traps": {
                    "vlan_membership": True,
                },
            },
        },
        {
            "name": "traps.vlancreate",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svlancreate
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vlancreate",
            "result": {
                "traps": {
                    "vlancreate": True,
                },
            },
        },
        {
            "name": "traps.vlandelete",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svlandelete
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vlandelete",
            "result": {
                "traps": {
                    "vlandelete": True,
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
            "name": "traps.vswitch",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svswitch
                (\s(?P<dual_active>dual-active))?
                (\s(?P<vsl>vsl))?
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vswitch"
                      "{{ ' dual-active' if traps.vswitch.dual_active|d(False) else '' }}"
                      "{{ ' vsl' if traps.vswitch.vsl|d(False) else '' }}",
            "result": {
                "traps": {
                    "vswitch": {
                        "enable": True,
                        "dual_active": "{{ not not dual_active }}",
                        "vsl": "{{ not not vsl }}",
                    },
                },
            },
        },
        {
            "name": "traps.vtp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable\straps\svtp
                """, re.VERBOSE,
            ),
            "setval": "snmp-server enable traps vtp",
            "result": {
                "traps": {
                    "vtp": True,
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
