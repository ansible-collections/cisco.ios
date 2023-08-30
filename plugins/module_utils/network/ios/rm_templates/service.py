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


class ServiceTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(ServiceTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "call_home",
            "getval": re.compile(
                r"""
                ^service\s(?P<call_home>call-home)
                """, re.VERBOSE,
            ),
            "setval": "service call-home",
            "result": {
                "call_home": "{{ not not call_home }}",
            },
        },
        {
            "name": "compress_config",
            "getval": re.compile(
                r"""
                ^service\s(?P<compress_config>compress-config)
                """, re.VERBOSE,
            ),
            "setval": "service compress-config",
            "result": {
                "compress_config": "{{ not not compress_config }}",
            },
        },
        {
            "name": "config",
            "getval": re.compile(
                r"""
                ^service\s(?P<config>config)
                """, re.VERBOSE,
            ),
            "setval": "service config",
            "result": {
                "config": "{{ not not config }}",
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
                ^service\s(?P<disable_ip_fast_frag>disable-ip-fast-frag)
                """, re.VERBOSE,
            ),
            "setval": "service disable-ip-fast-frag",
            "result": {
                "disable_ip_fast_frag": "{{ not not disable_ip_fast_frag }}",
            },
        },
        {
            "name": "exec_callback",
            "getval": re.compile(
                r"""
                ^service\s(?P<exec_callback>exec-callback)
                """, re.VERBOSE,
            ),
            "setval": "service exec-callback",
            "result": {
                "exec_callback": "{{ not not exec_callback }}",
            },
        },
        {
            "name": "exec_wait",
            "getval": re.compile(
                r"""
                ^service\s(?P<exec_wait>exec-wait)
                """, re.VERBOSE,
            ),
            "setval": "service exec-wait",
            "return": {
                "exec_wait": "{{ not not exec_wait }}",
            },
        },
        {
            "name": "hide_telnet_addresses",
            "getval": re.compile(
                r"""
                ^service\s(?P<hide_telnet_addresses>hide-telnet-addresses)
                """, re.VERBOSE,
            ),
            "setval": "service hide-telnet-addresses",
            "result": {
                "hide_telnet_addresses": "{{ not not hide_telnet_addresses }}",
            },
        },
        {
            "name": "internal",
            "getval": re.compile(
                r"""
                ^service\s(?P<internal>internal)
                """, re.VERBOSE,
            ),
            "setval": "service internal",
            "result": {
                "internal": "{{ not not internal }}",
            },
        },
        {
            "name": "linenumber",
            "getval": re.compile(
                r"""
                ^service\s(?P<linenumber>linenumber)
                """, re.VERBOSE,
            ),
            "setval": "service linenumber",
            "result": {
                "linenumber": "{{ not not linenumber }}",
            },
        },
        {
            "name": "log",
            "getval": re.compile(
                r"""
                ^service\slog(\s(?P<backtrace>backtrace))?
                """, re.VERBOSE,
            ),
            "setval": "service log backtrace",
            "result": {
                "log": "{{ not not backtrace }}",
            },
        },
        {
            "name": "log_hidden",
            "getval": re.compile(
                r"""
                ^service\s(?P<log_hidden>log-hidden)
                """, re.VERBOSE,
            ),
            "setval": "service log-hidden",
            "result": {
                "log_hidden": "{{ not not log_hidden }}",
            },
        },
        {
            "name": "nagle",
            "getval": re.compile(
                r"""
                ^service\s(?P<nagle>nagle)
                """, re.VERBOSE,
            ),
            "setval": "service nagle",
            "result": {
                "nagle": "{{ not not nagle }}",
            },
        },
        {
            "name": "old_slip_prompts",
            "getval": re.compile(
                r"""
                ^service\s(?P<old_slip_prompts>old-slip-prompts)
                """, re.VERBOSE,
            ),
            "setval": "service old-slip-prompts",
            "result": {
                "old_slip_prompts": "{{ not not old_slip_prompts }}",
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
                ^service\s(?P<password_encryption>password-encryption)
                """, re.VERBOSE,
            ),
            "setval": "service password-encryption",
            "result": {
                "password_encryption": "{{ not not password_encryption }}",
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
                ^service\s(?P<pt_vty_logging>pt-vty-logging)
                """, re.VERBOSE,
            ),
            "setval": "service pt-vty-logging",
            "result": {
                "pt_vty_logging": "{{ not not pt_vty_logging }}",
            },
        },
        {
            "name": "scripting",
            "getval": re.compile(
                r"""
                ^service\s(?P<scripting>scripting)
                """, re.VERBOSE,
            ),
            "setval": "service scripting",
            "result": {
                "scripting": "{{ not not scripting }}",
            },
        },
        {
            "name": "sequence_numbers",
            "getval": re.compile(
                r"""
                ^service\s(?P<sequence_numbers>sequence-numbers)
                """, re.VERBOSE,
            ),
            "setval": "service sequence-numbers",
            "result": {
                "sequence_numbers": "{{ not not sequence_numbers }}",
            },
        },
        {
            "name": "slave_coredump",
            "getval": re.compile(
                r"""
                ^service\s(?P<slave_coredump>slave-coredump)
                """, re.VERBOSE,
            ),
            "setval": "service slave-coredump",
            "result": {
                "slave_coredump": "{{ not not slave_coredump }}",
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
            "name": "timestamps",
            "getval": re.compile(
                r"""
                ^service\stimestamps
                (\s(?P<msg>\S+))?
                (\s(?P<timestamp>\S+))?
                (\s(?P<msec>msec))?
                (\s(?P<localtime>localtime))?
                (\s(?P<show_timezone>show-timezone))?
                (\s(?P<year>year))?
                """, re.VERBOSE,
            ),
            "remval": "service timestamps{{ (' ' + msg) if msg is defined else '' }}",
            "setval": "service timestamps"
                      "{{ (' ' + msg) if msg is defined else '' }}"
                      "{% if msg is defined %}"
                      "{{ (' ' + timestamp) if timestamp is defined else '' }}"
                      "{% if timestamp == 'datetime' and datetime_options is defined %}"
                      "{{ ' msec' if datetime_options.msec else '' }}"
                      "{{ ' localtime' if datetime_options.localtime else '' }}"
                      "{{ ' show-timezone' if datetime_options.show_timezone else '' }}"
                      "{{ ' year' if datetime_options.year else '' }}"
                      "{% endif %}"
                      "{% endif %}"
                      "",
            "result": {
                "timestamps": [
                    {
                        "msg": "{{ msg if msg is defined else 'debug' }}",
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
