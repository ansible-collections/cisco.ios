# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Service parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def handleTimestamp(config_data):
    command = "service timestamps"
    command += " " + config_data.get("msg") if config_data.get("msg") else ""
    command += " " + config_data.get("timestamp") if config_data.get("timestamp") else ""

    if config_data.get("datetime_options"):
        datetime_op = config_data.get("datetime_options")
        command += " msec" if datetime_op.get("msec") else ""
        command += " localtime" if datetime_op.get("localtime") else ""
        command += " show-timezone" if datetime_op.get("show_timezone") else ""
        command += " year" if datetime_op.get("year") else ""

    return command


class ServiceTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(ServiceTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "call_home",
            "getval": re.compile(
                r"""
                ^service\scall-home
                """, re.VERBOSE,
            ),
            "setval": "service call-home",
            "result": {
                "call_home": True,
            },
        },
        {
            "name": "compress_config",
            "getval": re.compile(
                r"""
                ^service\scompress-config
                """, re.VERBOSE,
            ),
            "setval": "service compress-config",
            "result": {
                "compress_config": True,
            },
        },
        {
            "name": "config",
            "getval": re.compile(
                r"""
                ^service\sconfig
                """, re.VERBOSE,
            ),
            "setval": "service config",
            "result": {
                "config": True,
            },
        },
        {
            "name": "counters",
            "getval": re.compile(
                r"""
                ^service\scounters\smax\sage(\s(?P<max_age>\d+))?
                """, re.VERBOSE,
            ),
            "setval": "service counters max age {{ counters }}",
            "result": {
                "counters": "{{ max_age|int }}",
            },
        },
        {
            "name": "dhcp",
            "getval": re.compile(
                r"""
                ^service\sdhcp
                """, re.VERBOSE,
            ),
            "setval": "service dhcp",
            "result": {
                "dhcp": True,
            },
        },
        {
            "name": "disable_ip_fast_frag",
            "getval": re.compile(
                r"""
                ^service\sdisable-ip-fast-frag
                """, re.VERBOSE,
            ),
            "setval": "service disable-ip-fast-frag",
            "result": {
                "disable_ip_fast_frag": True,
            },
        },
        {
            "name": "exec_callback",
            "getval": re.compile(
                r"""
                ^service\sexec-callback
                """, re.VERBOSE,
            ),
            "setval": "service exec-callback",
            "result": {
                "exec_callback": True,
            },
        },
        {
            "name": "exec_wait",
            "getval": re.compile(
                r"""
                ^service\sexec-wait
                """, re.VERBOSE,
            ),
            "setval": "service exec-wait",
            "return": {
                "exec_wait": True,
            },
        },
        {
            "name": "hide_telnet_addresses",
            "getval": re.compile(
                r"""
                ^service\shide-telnet-addresses
                """, re.VERBOSE,
            ),
            "setval": "service hide-telnet-addresses",
            "result": {
                "hide_telnet_addresses": True,
            },
        },
        {
            "name": "internal",
            "getval": re.compile(
                r"""
                ^service\sinternal
                """, re.VERBOSE,
            ),
            "setval": "service internal",
            "result": {
                "internal": True,
            },
        },
        {
            "name": "linenumber",
            "getval": re.compile(
                r"""
                ^service\slinenumber
                """, re.VERBOSE,
            ),
            "setval": "service linenumber",
            "result": {
                "linenumber": True,
            },
        },
        {
            "name": "log",
            "getval": re.compile(
                r"""
                ^service\slog\sbacktrace?
                """, re.VERBOSE,
            ),
            "setval": "service log backtrace",
            "result": {
                "log": True,
            },
        },
        {
            "name": "log_hidden",
            "getval": re.compile(
                r"""
                ^service\slog-hidden
                """, re.VERBOSE,
            ),
            "setval": "service log-hidden",
            "result": {
                "log_hidden": True,
            },
        },
        {
            "name": "nagle",
            "getval": re.compile(
                r"""
                ^service\snagle
                """, re.VERBOSE,
            ),
            "setval": "service nagle",
            "result": {
                "nagle": True,
            },
        },
        {
            "name": "old_slip_prompts",
            "getval": re.compile(
                r"""
                ^service\sold-slip-prompts
                """, re.VERBOSE,
            ),
            "setval": "service old-slip-prompts",
            "result": {
                "old_slip_prompts": True,
            },
        },
        {
            "name": "pad",
            "getval": re.compile(
                r"""
                ^service\spad$
                """, re.VERBOSE,
            ),
            "setval": "service pad",
            "result": {
                "pad": True,
            },
        },
        {
            "name": "pad_cmns",
            "getval": re.compile(
                r"""
                ^service\spad\scmns
                """, re.VERBOSE,
            ),
            "setval": "service pad cmns",
            "result": {
                "pad_cmns": True,
            },
        },
        {
            "name": "pad_from_xot",
            "getval": re.compile(
                r"""
                ^service\spad\sfrom-xot
                """, re.VERBOSE,
            ),
            "setval": "service pad from-xot",
            "result": {
                "pad_from_xot": True,
            },
        },
        {
            "name": "pad_to_xot",
            "getval": re.compile(
                r"""
                ^service\spad\sto-xot
                """, re.VERBOSE,
            ),
            "setval": "service pad to-xot",
            "result": {
                "pad_to_xot": True,
            },
        },
        {
            "name": "password_encryption",
            "getval": re.compile(
                r"""
                ^service\spassword-encryption
                """, re.VERBOSE,
            ),
            "setval": "service password-encryption",
            "result": {
                "password_encryption": True,
            },
        },
        {
            "name": "password_recovery",
            "getval": re.compile(
                r"""
                ^service\spassword-recovery
                """, re.VERBOSE,
            ),
            "setval": "service password-recovery",
            "remval": "service password-recovery\nyes",
            "result": {
                "password_recovery": True,
            },
        },
        {
            "name": "prompt",
            "getval": re.compile(
                r"""
                ^service\sprompt\sconfig
                """, re.VERBOSE,
            ),
            "setval": "service prompt config",
            "result": {
                "prompt": True,
            },
        },
        {
            "name": "private_config_encryption",
            "getval": re.compile(
                r"""
                ^service\sprivate-config-encryption
                """, re.VERBOSE,
            ),
            "setval": "service private-config-encryption",
            "result": {
                "private_config_encryption": True,
            },
        },
        {
            "name": "pt_vty_logging",
            "getval": re.compile(
                r"""
                ^service\spt-vty-logging
                """, re.VERBOSE,
            ),
            "setval": "service pt-vty-logging",
            "result": {
                "pt_vty_logging": True,
            },
        },
        {
            "name": "scripting",
            "getval": re.compile(
                r"""
                ^service\sscripting
                """, re.VERBOSE,
            ),
            "setval": "service scripting",
            "result": {
                "scripting": True,
            },
        },
        {
            "name": "sequence_numbers",
            "getval": re.compile(
                r"""
                ^service\ssequence-numbers
                """, re.VERBOSE,
            ),
            "setval": "service sequence-numbers",
            "result": {
                "sequence_numbers": True,
            },
        },
        {
            "name": "slave_coredump",
            "getval": re.compile(
                r"""
                ^service\sslave-coredump
                """, re.VERBOSE,
            ),
            "setval": "service slave-coredump",
            "result": {
                "slave_coredump": True,
            },
        },
        {
            "name": "slave_log",
            "getval": re.compile(
                r"""
                ^service\sslave-log
                """, re.VERBOSE,
            ),
            "setval": "service slave-log",
            "result": {
                "slave_log": True,
            },
        },
        {
            "name": "tcp_keepalives_in",
            "getval": re.compile(
                r"""
                ^service\stcp-keepalives-in
                """, re.VERBOSE,
            ),
            "setval": "service tcp-keepalives-in",
            "result": {
                "tcp_keepalives_in": True,
            },
        },
        {
            "name": "tcp_keepalives_out",
            "getval": re.compile(
                r"""
                ^service\stcp-keepalives-out
                """, re.VERBOSE,
            ),
            "setval": "service tcp-keepalives-out",
            "result": {
                "tcp_keepalives_out": True,
            },
        },
        {
            "name": "tcp_small_servers",
            "getval": re.compile(
                r"""
                ^service\stcp-small-servers
                (\s(?P<max_servers>\d+))?
                (\s(?P<no_limit>no-limit))?
                """, re.VERBOSE,
            ),
            "setval": "service tcp-small-servers"
            "{{ (' ' + tcp_small_servers.max_servers|string) if tcp_small_servers.max_servers is defined else '' }}"
            "{{ (' no-limit') if tcp_small_servers.no_limit|d(False) else '' }}",
            "result": {
                "tcp_small_servers": {
                    "enable": True,
                    "max_servers": "{{ max_servers }}",
                    "no_limit": "{{ not not no_limit }}",
                },
            },
        },
        {
            "name": "udp_small_servers",
            "getval": re.compile(
                r"""
                ^service\sudp-small-servers
                (\s(?P<max_servers>\d+))?
                (\s(?P<no_limit>no-limit))?
                """, re.VERBOSE,
            ),
            "setval": "{{ ('service udp-small-servers') if udp_small_servers.enable|d(False) else '' }}"
            "{{ (' ' + udp_small_servers.max_servers|string) if udp_small_servers.max_servers is defined else '' }}"
            "{{ (' no-limit') if udp_small_servers.no_limit|d(False) else '' }}",
            "result": {
                "udp_small_servers": {
                    "enable": True,
                    "max_servers": "{{ max_servers }}",
                    "no_limit": "{{ not not no_limit }}",
                },
            },
        },
        {
            "name": "telnet_zeroidle",
            "getval": re.compile(
                r"""
                ^service\stelnet-zeroidle
                """, re.VERBOSE,
            ),
            "setval": "service telnet-zeroidle",
            "result": {
                "telnet_zeroidle": True,
            },
        },
        {
            "name": "log_timestamps",
            "getval": re.compile(
                r"""
                ^service\stimestamps\slog
                (\s(?P<timestamp>\S+))?
                (\s(?P<msec>msec))?
                (\s(?P<localtime>localtime))?
                (\s(?P<show_timezone>show-timezone))?
                (\s(?P<year>year))?
                """, re.VERBOSE,
            ),
            "remval": "service timestamps log",
            "setval": handleTimestamp,
            "result": {
                "timestamps": [
                    {
                        "msg": "log",
                        "timestamp": "{{ timestamp if timestamp is defined else 'uptime' }}",
                        "datetime_options": {
                            "msec": "{{ True if msec else False}}",
                            "localtime": "{{ True if localtime else False }}",
                            "show_timezone": "{{ True if show_timezone else False }}",
                            "year": "{{ True if year else False }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "debug_timestamps",
            "getval": re.compile(
                r"""
                ^service\stimestamps\sdebug
                (\s(?P<timestamp>\S+))?
                (\s(?P<msec>msec))?
                (\s(?P<localtime>localtime))?
                (\s(?P<show_timezone>show-timezone))?
                (\s(?P<year>year))?
                """, re.VERBOSE,
            ),
            "remval": "service timestamps debug",
            "setval": handleTimestamp,
            "result": {
                "timestamps": [
                    {
                        "msg": "debug",
                        "timestamp": "{{ timestamp if timestamp is defined else 'uptime' }}",
                        "datetime_options": {
                            "msec": "{{ True if msec else False}}",
                            "localtime": "{{ True if localtime else False }}",
                            "show_timezone": "{{ True if show_timezone else False }}",
                            "year": "{{ True if year else False }}",
                        },
                    },
                ],
            },
        },
        {
            "name": "unsupported_transceiver",
            "getval": re.compile(
                r"""
                ^service\sunsupported-transceiver
                """, re.VERBOSE,
            ),
            "setval": "service unsupported-transceiver",
            "result": {
                "unsupported_transceiver": True,
            },
        },
    ]
