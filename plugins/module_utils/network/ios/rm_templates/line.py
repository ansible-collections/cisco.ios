# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Line parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class LineTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(LineTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "line",
            "getval": re.compile(
                r"""
                ^line\s+(?P<name>con\s+[0-9]+|vty\s+[0-9]+\s+[0-9]*)
                """, re.VERBOSE,
            ),
            "setval": "line {{ name }}",
            "result": {
                "lines": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "access_classes_in",
            "getval": re.compile(
                r"""
                ^\s+access-class\s+(?P<access_classes_in>\S+)\s+in
                """, re.VERBOSE,
            ),
            "setval": " access-class {{ access_classes_in }} in",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "access_classes_in": "{{ access_classes_in }}",
                    },
                },
            },
        },
        {
            "name": "access_classes_out",
            "getval": re.compile(
                r"""
                ^\s+access-class\s+(?P<access_classes_in>\S+)\s+out
                """, re.VERBOSE,
            ),
            "setval": " access-class {{ access_classes_out }} out",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "access_classes_out": "{{ access_classes_out }}",
                    },
                },
            },
        },
        {
            "name": "accounting.arap",
            "getval": re.compile(
                r"""
                ^\s+accounting\s+arap\s+(?P<arap>\S+)
                """, re.VERBOSE,
            ),
            "setval": " accounting arap {{ accounting.arap }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "accounting": {
                            "arap": "{{ arap|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "accounting.commands",
            "compval": "commands",
            "getval": re.compile(
                r"""
                ^\s+accounting\s+commands\s+(?P<level>\d+)\s+(?P<command>\S+)
                """, re.VERBOSE,
            ),
            "setval": " accounting commands {{ commands.level }} {{ commands.command }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "accounting": {
                            "commands": {
                                "{{ level|d() }}": {
                                    "level": "{{ level }}",
                                    "command": "{{ command }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "accounting.connection",
            "getval": re.compile(
                r"""
                ^\s+accounting\s+connection\s+(?P<connection>\S+)
                """, re.VERBOSE,
            ),
            "setval": " accounting connection {{ accounting.connection }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "accounting": {
                            "connection": "{{ connection|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "accounting.exec",
            "getval": re.compile(
                r"""
                ^\s+accounting\s+exec\s+(?P<exec>\S+)
                """, re.VERBOSE,
            ),
            "setval": " accounting exec {{ accounting.exec }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "accounting": {
                            "exec": "{{ exec|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "accounting.resource",
            "getval": re.compile(
                r"""
                ^\s+accounting\s+resource\s+(?P<resource>\S+)
                """, re.VERBOSE,
            ),
            "setval": " accounting resource {{ accounting.resource }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "accounting": {
                            "resource": "{{ resource|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "authorization.arap",
            "getval": re.compile(
                r"""
                ^\s+authorization\s+arap\s+(?P<arap>\S+)
                """, re.VERBOSE,
            ),
            "setval": " authorization arap {{ authorization.arap }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "authorization": {
                            "arap": "{{ arap|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "authorization.commands",
            "compval": "commands",
            "getval": re.compile(
                r"""
                ^\s+authorization\s+commands\s+(?P<level>\d+)\s+(?P<command>\S+)
                """, re.VERBOSE,
            ),
            "setval": " authorization commands {{ commands.level }} {{ commands.command }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "authorization": {
                            "commands": {
                                "{{ level|d() }}": {
                                    "level": "{{ level }}",
                                    "command": "{{ command }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "authorization.exec",
            "getval": re.compile(
                r"""
                ^\s+authorization\s+exec\s+(?P<exec>\S+)
                """, re.VERBOSE,
            ),
            "setval": " authorization exec {{ authorization.exec }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "authorization": {
                            "exec": "{{ exec|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "authorization.reverse_access",
            "getval": re.compile(
                r"""
                ^\s+authorization\s+reverse-access\s+(?P<reverse_access>\S+)
                """, re.VERBOSE,
            ),
            "setval": " authorization reverse-access {{ authorization.reverse_access }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "authorization": {
                            "reverse-access": "{{ reverse-access|d(default) }}",
                        },
                    },
                },
            },
        },
        {
            "name": "escape_character",
            "getval": re.compile(
                r"""
                ^\s+escape-character
                (\s+(?P<soft>soft))?
                \s+(?P<value>\S+)
                """, re.VERBOSE,
            ),
            "setval": " escape-character"
                      "{{ ' soft' if escape_character.soft|d(False) else '' }}"
                      "{{ ' ' + escape_character.value }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "escape_character": {
                            "soft": "{{ True if soft }}",
                            "value": "{{ value }}",
                        },
                    },
                },
            },
        },
        {
            "name": "exec.banner",
            "getval": re.compile(
                r"""
                ^\s+exec-banner
                """, re.VERBOSE,
            ),
            "setval": " exec-banner",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "exec": {
                            "banner": True,
                        },
                    },
                },
            },
        },
        {
            "name": "exec.character_bits",
            "getval": re.compile(
                r"""
                ^\s+exec-character-bits\s+(?P<character_bits>7|8)
                """, re.VERBOSE,
            ),
            "setval": " exec-character-bits {{ exec.character_bits }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "exec": {
                            "character_bits": "{{ character_bits }}",
                        },
                    },
                },
            },
        },
        {
            "name": "exec.prompt.expand",
            "getval": re.compile(
                r"""
                ^\s+exec\s+prompt\s+expand
                """, re.VERBOSE,
            ),
            "setval": "{{ ' exec prompt expand' if expand|d(False) }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "exec": {
                            "prompt": {
                                "expand": True,
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "exec.prompt.timestamp",
            "getval": re.compile(
                r"""
                ^\s+exec\s+prompt\s+timestamp
                """, re.VERBOSE,
            ),
            "setval": "{{ ' exec prompt timestamp' if timestamp|d(False) }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "exec": {
                            "prompt": {
                                "timestamp": True,
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "exec.timeout",
            "getval": re.compile(
                r"""
                ^\s+exec-timeout\s+(?P<timeout>\d+)
                """, re.VERBOSE,
            ),
            "setval": " exec-timeout {{ exec.timeout }} 0",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "exec": {
                            "timeout": "{{ timeout }}",
                        },
                    },
                },
            },
        },
        {
            "name": "length",
            "getval": re.compile(
                r"""
                ^\s+length\s(?P<length>\d+)
                """, re.VERBOSE,
            ),
            "setval": " length {{ length|string }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "length": "{{ length }}",
                    },
                },
            },
        },
        {
            "name": "location",
            "getval": re.compile(
                r"""
                ^\s+location\s+(?P<location>.+)$
                """, re.VERBOSE,
            ),
            "setval": " location {{ location }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "location": "{{ location }}",
                    },
                },
            },
        },
        {
            "name": "logging",
            "getval": re.compile(
                r"""
                ^\s+logging\s+synchronous
                (\s+(?P<level>\S+))?
                (\s+(?P<limit>\d+))?
                """, re.VERBOSE,
            ),
            "setval": " logging synchronous"
                      "{{ ' level ' + logging.level if logging.level is defined else '' }}"
                      "{{ ' limit ' + logging.limit if logging.limit is defined else '' }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "logging": {
                            "enable": True,
                            "level": "{{ level }}",
                            "limit": "{{ limit }}",
                        },
                    },
                },
            },
        },
        {
            "name": "login",
            "getval": re.compile(
                r"""
                ^\s+login\s+authentication\s+(?P<login>\S+)
                """, re.VERBOSE,
            ),
            "setval": " login authentication {{ login }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "login": "{{ login|d('default') }}",
                    },
                },
            },
        },
        {
            "name": "logout_warning",
            "getval": re.compile(
                r"""
                ^\s+logout-warning\s+(?P<logout_warning>\d+)
                """, re.VERBOSE,
            ),
            "setval": " logout-warning {{ logout_warning }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "logout_warning": "{{ logout_warning }}",
                    },
                },
            },
        },
        {
            "name": "motd",
            "getval": re.compile(
                r"""
                ^\s+motd-banner
                """, re.VERBOSE,
            ),
            "setval": " motd-banner",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "motd": True,
                    },
                },
            },
        },
        {
            "name": "notify",
            "getval": re.compile(
                r"""
                ^\s+notify
                """, re.VERBOSE,
            ),
            "setval": " notify",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "notify": True,
                    },
                },
            },
        },
        {
            "name": "padding",
            "getval": re.compile(
                r"""
                ^\s+padding\s+(?P<padding>\S+)
                """, re.VERBOSE,
            ),
            "setval": " padding {{ padding }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "padding": "{{ padding }}",
                    },
                },
            },
        },
        {
            "name": "parity",
            "getval": re.compile(
                r"""
                ^\s+parity\s+(?P<parity>even|mark|none|odd|space)
                """, re.VERBOSE,
            ),
            "setval": " parity {{ parity }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "parity": "{{ parity }}",
                    },
                },
            },
        },
        {
            "name": "password",
            "getval": re.compile(
                r"""
                ^\s+password
                (\s+(?P<hash>0|7))?
                (\s+(?P<value>\S+))?
                """, re.VERBOSE,
            ),
            "setval": "{% if 'value' in password and password.value is defined %}"
                      " password"
                      "{{ ' ' + password.hash|string if password.hash is defined else '' }}"
                      "{{ ' ' + password.value }}"
                      "{% endif %}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "password": {
                            "hash": "{{ hash }}",
                            "value": "{{ value }}",
                        },
                    },
                },
            },
        },
        {
            "name": "privilege",
            "getval": re.compile(
                r"""
                ^\s+privilege\s+level\s+(?P<privilege>\d+)
                """, re.VERBOSE,
            ),
            "setval": " privilege level {{ privilege }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "privilege": "{{ privilege }}",
                    },
                },
            },
        },
        {
            "name": "session.disconnect_warning",
            "getval": re.compile(
                r"""
                ^\s+session-disconnect-warning\s+(?P<disconnect_warning>\d+)
                """, re.VERBOSE,
            ),
            "setval": " session-disconnect-warning {{ session.disconnect_warning }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "session": {
                            "disconnect_warning": "{{ disconnect_warning }}",
                        },
                    },
                },
            },
        },
        {
            "name": "session.limit",
            "getval": re.compile(
                r"""
                ^\s+session-limit\s+(?P<limit>\d+)
                """, re.VERBOSE,
            ),
            "setval": " session-limit {{ session.limit }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "session": {
                            "limit": "{{ limit }}",
                        },
                    },
                },
            },
        },
        {
            "name": "session.timeout",
            "getval": re.compile(
                r"""
                ^\s+session-timeout\s+(?P<timeout>\d+)
                """, re.VERBOSE,
            ),
            "setval": " session-timeout {{ session.timeout }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "session": {
                            "timeout": "{{ timeout }}",
                        },
                    },
                },
            },
        },
        {
            "name": "speed",
            "getval": re.compile(
                r"""
                ^\s+speed\s+(?P<speed>\d+)
                """, re.VERBOSE,
            ),
            "setval": " speed {{ speed }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "speed": "{{ speed }}",
                    },
                },
            },
        },
        {
            "name": "stopbits",
            "getval": re.compile(
                r"""
                ^\s+stopbits\s+(?P<stopbits>1|1.5|2)
                """, re.VERBOSE,
            ),
            "setval": " stopbits {{ stopbits }}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "stopbits": "{{ stopbits }}",
                    },
                },
            },
        },
        {
            "name": "transport",
            "getval": re.compile(
                r"""
                ^\s+transport\s+(?P<transport_name>input|output|preferred)
                (\s+(?P<t_all>all))?
                (\s+(?P<t_none>none))?
                (\s+(?P<t_pad>pas))?
                (\s+(?P<t_telnet>telnet))?
                (\s+(?P<t_rlogin>rlogin))?
                (\s+(?P<t_ssh>ssh))?
                """, re.VERBOSE,
            ),
            "setval": " transport {{ transport.name }}"
                      "{% if transport.all|d(False) %}"
                      " all"
                      "{% elif transport.none|d(False) %}"
                      " none"
                      "{% else %}"
                      "{{ ' pad' if transport.pad|d(False) }}"
                      "{{ ' telnet' if transport.telnet|d(False) }}"
                      "{{ ' rlogin' if transport.rlogin|d(False) }}"
                      "{{ ' ssh' if transport.ssh|d(False) }}"
                      "{% endif %}",
            "result": {
                "lines": {
                    "{{ name|d() }}": {
                        "transport": [
                            {
                                "name": "{{ transport_name }}",
                                "all": "{{ True if t_all is defined }}",
                                "none": "{{ True if t_none is defined }}",
                                "pad": "{{ True if t_pad is defined }}",
                                "telnet": "{{ True if t_telnet is defined }}",
                                "rlogin": "{{ True if t_rlogin is defined }}",
                                "ssh": "{{ True if t_ssh is defined }}",
                            },
                        ],
                    },
                },
            },
        },
    ]
    # fmt: on
