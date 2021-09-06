# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Ntp_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Ntp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ntp_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "access_group.peer",
            "getval": re.compile(
                r"""
                ^ntp\saccess-group
                (\s(?P<ipv4>ipv4))?
                (\s(?P<ipv6>ipv6))?
                \speer
                \s(?P<access_list>\S+)
                (\s(?P<kod>kod))?
                $""", re.VERBOSE),
            "setval": "ntp access-group peer {{ access_group.peer.access_list }}", # TODO
            "result": {
                "access_group": {
                    "peer": [
                        {
                            "access_list": "{{ access_list }}",
                            "kod": "{{ not not kod }}",
                            "ipv4": "{{ not not ipv4 }}",
                            "ipv6": "{{ not not ipv6 }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "access_group.query_only",
            "getval": re.compile(
                r"""
                ^ntp\saccess-group
                (\s(?P<ipv4>ipv4))?
                (\s(?P<ipv6>ipv6))?
                \squery-only
                \s(?P<access_list>\S+)
                (\s(?P<kod>kod))?
                $""", re.VERBOSE),
            "setval": "ntp access-group query-only {{ access_group.query_only.access_list }}", # TODO
            "result": {
                "access_group": {
                    "query_only": [
                        {
                            "access_list": "{{ access_list }}",
                            "kod": "{{ not not kod }}",
                            "ipv4": "{{ not not ipv4 }}",
                            "ipv6": "{{ not not ipv6 }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "access_group.serve",
            "getval": re.compile(
                r"""
                ^ntp\saccess-group
                (\s(?P<ipv4>ipv4))?
                (\s(?P<ipv6>ipv6))?
                \sserve
                \s(?P<access_list>\S+)
                (\s(?P<kod>kod))?
                $""", re.VERBOSE),
            "setval": "ntp access-group serve {{ access_group.serve.access_list }}", # TODO
            "result": {
                "access_group": {
                    "serve": [
                        {
                            "access_list": "{{ access_list }}",
                            "kod": "{{ not not kod }}",
                            "ipv4": "{{ not not ipv4 }}",
                            "ipv6": "{{ not not ipv6 }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "access_group.serve_only",
            "getval": re.compile(
                r"""
                ^ntp\saccess-group
                (\s(?P<ipv4>ipv4))?
                (\s(?P<ipv6>ipv6))?
                \sserve-only
                \s(?P<access_list>\S+)
                (\s(?P<kod>kod))?
                $""", re.VERBOSE),
            "setval": "ntp access-group serve-only {{ access_group.serve_only.access_list }}", # TODO
            "result": {
                "access_group": {
                    "serve_only": [
                        {
                            "access_list": "{{ access_list }}",
                            "kod": "{{ not not kod }}",
                            "ipv4": "{{ not not ipv4 }}",
                            "ipv6": "{{ not not ipv6 }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "allow.control.rate_limit",
            "getval": re.compile(
                r"""
                ^ntp\sallow\smode\scontrol\s(?P<rate_limit>\d+)
                $""", re.VERBOSE),
            "setval": "ntp allow mode control {{ allow.control.rate_limit }}",
            "result": {
                "allow": {
                    "control": {
                        "rate_limit": "{{ rate_limit }}",
                    },
                },
            },
        },
        {
            "name": "allow.private",
            "getval": re.compile(
                r"""
                ^ntp\sallow\smode\s(?P<private>private)
                $""", re.VERBOSE),
            "setval": "ntp allow mode private",
            "result": {
                "allow": {
                    "private": "{{ not not private }}",
                },
            },
        },
        {
            "name": "authenticate",
            "getval": re.compile(
                r"""
                ^ntp\s(?P<authenticate>authenticate)
                $""", re.VERBOSE),
            "setval": "ntp authenticate",
            "result": {
                "authenticate": "{{ not not authenticate }}",
            },
        },
        {
            "name": "authentication_keys",
            "getval": re.compile(
                r"""
                ^ntp\sauthentication-key\s(?P<id>\d+)
                \s(?P<algorithm>\S+)
                \s(?P<key>\S+)
                \s(?P<encryption>\d+)
                $""", re.VERBOSE),
            "setval": "ntp authentication-key {{ id }} {{ algorithm }} {{ key }} {{ encryption }}",
            "result": {
                "authentication_keys": [
                    {
                        "id": "{{ id }}",
                        "algorithm": "{{ algorithm }}",
                        "key": "{{ key }}",
                        "encryption": "{{ encryption }}",
                    },
                ],
            },
        },
        {
            "name": "broadcast_delay",
            "getval": re.compile(
                r"""
                ^ntp\sbroadcastdelay\s(?P<broadcast_delay>\d+)
                $""", re.VERBOSE),
            "setval": "ntp broadcastdelay {{ broadcast_delay }}",
            "result": {
                "broadcast_delay": "{{ broadcast_delay }}",
            },
        },
        {
            "name": "clock_period",
            "getval": re.compile(
                r"""
                ^ntp\sclock-period\s(?P<clock_period>\d+)
                $""", re.VERBOSE),
            "setval": "ntp clock-period {{ clock_period }}",
            "result": {
                "clock_period": "{{ clock_period }}",
            },
        },
        {
            "name": "logging",
            "getval": re.compile(
                r"""
                ^ntp\s(?P<logging>logging)
                $""", re.VERBOSE),
            "setval": "ntp logging",
            "result": {
                "logging": "{{ not not logging }}",
            },
        },
        {
            "name": "master.enabled",
            "getval": re.compile(
                r"""
                ^ntp\s(?P<master>master)
                $""", re.VERBOSE),
            "setval": "ntp master",
            "result": {
                "master":{
                    "enabled": "{{ not not master }}",
                },
            },
        },
        {
            "name": "master.stratum_number",
            "getval": re.compile(
                r"""
                ^ntp\smaster\s(?P<stratum_number>\d+)
                $""", re.VERBOSE),
            "setval": "ntp master {{ stratum_number }}",
            "result": {
                "master":{
                    "stratum_number": "{{ stratum_number }}",
                },
            },
        },
        {
            "name": "max_associations",
            "getval": re.compile(
                r"""
                ^ntp\smax-associations\s(?P<max_associations>\d+)
                $""", re.VERBOSE),
            "setval": "ntp max-associations {{ max_associations }}",
            "result": {
                "max_associations": "{{ max_associations }}",
            },
        },
        {
            "name": "max_distance",
            "getval": re.compile(
                r"""
                ^ntp\smaxdistance\s(?P<max_distance>\d+)
                $""", re.VERBOSE),
            "setval": "ntp maxdistance {{ max_distance }}",
            "result": {
                "max_distance": "{{ max_distance }}",
            },
        },
        {
            "name": "min_distance",
            "getval": re.compile(
                r"""
                ^ntp\smindistance\s(?P<min_distance>\d+)
                $""", re.VERBOSE),
            "setval": "ntp mindistance {{ min_distance }}",
            "result": {
                "min_distance": "{{ min_distance }}",
            },
        },
        {
            "name": "orphan",
            "getval": re.compile(
                r"""
                ^ntp\sorphan\s(?P<orphan>\d+)
                $""", re.VERBOSE),
            "setval": "ntp orphan {{ orphan }}",
            "result": {
                "orphan": "{{ orphan }}",
            },
        },
        {
            "name": "panic_update",
            "getval": re.compile(
                r"""
                ^ntp\spanic\s(?P<update>update)
                $""", re.VERBOSE),
            "setval": "ntp panic update",
            "result": {
                "panic_update": "{{ not not update }}",
            },
        },
        {
            "name": "passive",
            "getval": re.compile(
                r"""
                ^ntp\s(?P<passive>passive)
                $""", re.VERBOSE),
            "setval": "ntp passive",
            "result": {
                "passive": "{{ not not passive }}",
            },
        },
        {
            "name": "peers",
            "getval": re.compile(
                r"""
                ^ntp\speer
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<ipv4>ip))?
                (\s(?P<ipv6>ipv6))?
                \s(?P<peer>\S+)
                (\s(?P<burst>burst))?
                (\s(?P<iburst>iburst))?
                (\skey\s(?P<key>\d+))?
                (\sminpoll\s(?P<minpoll>\d+))?
                (\smaxpoll\s(?P<maxpoll>\d+))?
                (\s(?P<normal_sync>normal-sync))?
                (\s(?P<prefer>prefer))?
                (\ssource\s(?P<source>\S+))?
                (\sversion\s(?P<version>\d+))?
                $""", re.VERBOSE),
            "setval": "ntp peer 10.0.2.11 key 2 minpoll 5 prefer version 2", # TODO
            "result": {
                "peers": [
                    {
                        "peer": "{{ peer }}",
                        "use_ipv4": "{{ not not ipv4 }}",
                        "use_ipv6": "{{ not not ipv6 }}",
                        "vrf": "{{ vrf }}",
                        "burst": "{{ not not burst }}",
                        "iburst": "{{ not not iburst }}",
                        "key": "{{ key }}",
                        "minpoll": "{{ minpoll }}",
                        "maxpoll": "{{ maxpoll }}",
                        "normal_sync": "{{ not not normal_sync }}",
                        "prefer": "{{ not not prefer }}",
                        "source": "{{ source }}",
                        "version": "{{ version }}",
                    },
                ],
            },
        },
        {
            "name": "servers",
            "getval": re.compile(
                r"""
                ^ntp\sserver
                (\svrf\s(?P<vrf>\S+))?
                (\s(?P<ipv4>ip))?
                (\s(?P<ipv6>ipv6))?
                \s(?P<server>\S+)
                (\s(?P<burst>burst))?
                (\s(?P<iburst>iburst))?
                (\skey\s(?P<key>\d+))?
                (\sminpoll\s(?P<minpoll>\d+))?
                (\smaxpoll\s(?P<maxpoll>\d+))?
                (\s(?P<normal_sync>normal-sync))?
                (\s(?P<prefer>prefer))?
                (\ssource\s(?P<source>\S+))?
                (\sversion\s(?P<version>\d+))?
                $""", re.VERBOSE),
            "setval": "ntp server 10.0.2.11 key 2 minpoll 5 prefer version 2", # TODO
            "result": {
                "servers": [
                    {
                        "server": "{{ server }}",
                        "use_ipv4": "{{ not not ipv4 }}",
                        "use_ipv6": "{{ not not ipv6 }}",
                        "vrf": "{{ vrf }}",
                        "burst": "{{ not not burst }}",
                        "iburst": "{{ not not iburst }}",
                        "key": "{{ key }}",
                        "minpoll": "{{ minpoll }}",
                        "maxpoll": "{{ maxpoll }}",
                        "normal_sync": "{{ not not normal_sync }}",
                        "prefer": "{{ not not prefer }}",
                        "source": "{{ source }}",
                        "version": "{{ version }}",
                    },
                ],
            },
        },
        {
            "name": "trusted_keys",
            "getval": re.compile(
                r"""
                ^ntp\strusted-key
                \s((?P<range_start>\d+))
                (\s\-\s)?
                ((?P<range_end>\d+))?
                $""", re.VERBOSE),
            "setval": "ntp trusted-key {{ range_start }} - {{ range_end }}",
            "result": {
                "trusted_keys": [
                    {
                        "range_start":"{{ range_start }}",
                        "range_end":"{{ range_end }}",
                    },
                ],
            },
        },
        {
            "name": "source",
            "getval": re.compile(
                r"""
                ^ntp\ssource\s(?P<source>\S+)
                $""", re.VERBOSE),
            "setval": "ntp source {{ source }}",
            "result": {
                "source": "{{ source }}",
            },
        },
        {
            "name": "update_calendar",
            "getval": re.compile(
                r"""
                ^ntp\s(?P<update_calendar>update-calendar)
                $""", re.VERBOSE),
            "setval": "ntp update-calendar",
            "result": {
                "update_calendar": "{{ not not update_calendar }}",
            },
        },
    ]
    # fmt: on
