# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Hsrp_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Hsrp_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Hsrp_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

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
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "mac_refresh",
            "getval": re.compile(
                r"""
                \s+standby\smac-refresh\s(?P<mac_refresh_number>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby mac-refresh {{ mac_refresh|string }}",
            "result": {
                "{{ name }}": {
                    "mac_refresh": "{{ mac_refresh_number }}",
                },
            },
        },
        {
            "name": "version",
            "getval": re.compile(
                r"""
                \s*standby\sversion\s(?P<version>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby version {{ version|string }}",
            "result": {
                "{{ name }}": {
                    "version": "{{ version }}",
                },
            },
        },
        {
            "name": "delay",
            "getval": re.compile(
                r"""
                \s+standby\sdelay
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby delay"
                      "{{ ' minimum ' + delay.minimum|string if delay.minimum is defined else ''}}"
                      "{{ ' reload ' + delay.reload|string if delay.reload is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "delay": {
                        "minimum": "{{ minimum }}",
                        "reload": "{{ reload }}",
                    },
                },
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s+standby\sbfd\s
                $""", re.VERBOSE,
            ),
            "setval": "standby bfd",
            "result": {
                "{{ name }}": {
                    "bfd": True,
                },
            },
        },
        {
            "name": "use_bia",
            "getval": re.compile(
                r"""
                \s+standby\suse-bia
                (\s(?P<bia>\sscope\sinterface))?
                $""", re.VERBOSE,
            ),
            "remval": "standby use-bia",
            "setval": "standby use-bia"
            "{{ ' scope interface' if use_bia.scope|d(False) is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "use_bia": {
                        "set": True,
                        "scope": "{{ not not bia }}",
                    },
                },
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \s*standby\s(?P<grp_no>\d+)
                \s*timers
                (?:\smsec\s(?P<msec_hello_interval>\d+)|\s(?P<hello_interval>\d+))
                (?:\smsec\s(?P<msec_hold_time>\d+)|\s(?P<hold_time>\d+))
                $""", re.VERBOSE,
            ),
            "setval": "standby"
            "{{ ' ' + group_no|string if group_no is defined else ''}}"
            " timers"
            "{{ (' msec ' + timer.msec.hello_interval|string) "
            "if timer.msec.hello_interval is defined "
            "else (' ' + timer.hello_interval|string) "
            "if timer.hello_interval is defined else '' }}"
            "{{ (' msec ' + timer.msec.hold_time|string) "
            "if timer.msec.hold_time is defined "
            "else (' ' + timer.hold_time|string) "
            "if timer.hold_time is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "timers": {
                            "hello_interval": "{{ hello_interval }}",
                            "hold_time": "{{ hold_time }}",
                            "msec": {
                                "hello_interval": "{{ msec_hello_interval }}",
                                "hold_time": "{{ msec_hold_time }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "follow",
            "getval": re.compile(
                r"""
                \s*standby\s(?P<grp_no>\d+)
                \s*follow\s(?P<description>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no|string if group_no is defined else '' }} follow {{ follow }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "follow": "{{ description }}",
                    },
                },
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)?\s*priority\s(?P<priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no|string if group_no is defined else '' }} priority {{ priority|string }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "priority": "{{ priority }}",
                    },
                },
            },
        },
        {
            "name": "preempt",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)?\s*preempt
                (\s(?P<delay>delay))?
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                (\ssync\s(?P<sync>\d+))?
                $""", re.VERBOSE,
            ),
            "remval": "standby "
                      "{{ group_no|string if group_no is defined else ''}}"
                      " preempt",
            "setval": "standby "
                      "{{ group_no|string if group_no is defined else ''}}"
                      " preempt"
                      "{{ ' delay' if preempt.delay|d(False) else ''}}"
                      "{{ ' minimum ' + preempt.minimum|string if preempt.minimum is defined else ''}}"
                      "{{ ' reload ' + preempt.reload|string if preempt.reload is defined else ''}}"
                      "{{ ' sync ' + preempt.sync|string if preempt.sync is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "preempt": {
                            "enabled": True,
                            "delay": "{{ not not delay }}",
                            "minimum": "{{ minimum }}",
                            "reload": "{{ reload }}",
                            "sync": "{{ sync }}",
                        },
                    },
                },
            },
        },
        {
            "name": "track",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)\s*track\s(?P<track_no>\d+)
                (\sdecrement\s(?P<decrement>\d+))?
                (\s(?P<shutdown>shutdown))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + track.group_no|string if track.group_no is defined else ''}}"
                      " track"
                      "{{ ' ' + track.track_no|string if track.track_no is defined else ''}}"
                      "{{ ' decrement ' + track.decrement|string if track.decrement is defined else ''}}"
                      "{{ ' shutdown' if track.shutdown|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "track": [{
                            "track_no": "{{ track_no }}",
                            "decrement": "{{ decrement }}",
                            "shutdown": "{{ not not shutdown }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)\s*ip\s+(?P<virtual_ip>\S+)
                (\s(?P<secondary>secondary))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + ip.group_no|string if ip.group_no is defined else ''}}"
                      " ip"
                      "{{ ' ' + ip.virtual_ip if ip.virtual_ip is defined else ''}}"
                      "{{ ' secondary' if ip.secondary|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "ip": [{
                            "virtual_ip": "{{ virtual_ip }}",
                            "secondary": "{{ not not secondary }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "ipv6.autoconfig",
            "getval": re.compile(
                r"""
                \s*standby(\s+(?P<grp_no>\d+))\s+ipv6\sautoconfig
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no|string if group_no is defined else ''}}"
                      " ipv6"
                      "{{ ' autoconfig' if ipv6.autoconfig|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "ipv6": {
                            "autoconfig": True,
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6_addr",
            "getval": re.compile(
                r"""
                \s+standby(\s(?P<grp_no>\d+))\sipv6
                (\s(?P<address>\S+))
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + ipv6_addr.group_no|string if ipv6_addr.group_no is defined else ''}}"
                      " ipv6"
                      "{{ ' ' + ipv6_addr.address if ipv6_addr.address is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "ipv6": {"addresses": ["{{ address }}"]},
                    },
                },
            },
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)?\s*mac-address\s(?P<mac_address>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no|string if group_no is defined else '' }} mac-address {{ mac_address }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "mac_address": "{{ mac_address }}",
                    },
                },
            },
        },
        {
            "name": "group_name",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<grp_no>\d+)?\s*name\s+(?P<group_name>.+)$
                """, re.VERBOSE,
            ),
            "setval": "standby {{ group_no|string if group_no is defined else '' }} name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "group_name": "{{ group_name }}",
                    },
                },
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s*standby\s(?P<grp_no>\d+)
                \s*authentication
                (\smd5\skey-chain\s(?P<key_chain>\S+)|
                \smd5\skey-string\s(?:(?P<encryption>\d+)\s)?(?P<key_string>\S+)|
                \s(?P<password_text>\S+))?
                (\stimeout\s(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
            "{{ ' ' + group_no|string if group_no is defined else ''}}"
            " authentication"
            "{{ (' ' + authentication.password_text|string) "
            "if authentication.password_text is defined else '' }}"
            "{{ (' md5 key-chain ' + authentication.key_chain|string) "
            "if authentication.key_chain is defined else '' }}"
            "{{ (' md5 key-string ' + authentication.encryption|string + ' ' + authentication.key_string) "
            "if authentication.key_string is defined and authentication.encryption is defined "
            "else (' md5 key-string ' + authentication.key_string) "
            "if authentication.key_string is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "authentication": {
                            "key_chain": "{{ key_chain }}",
                            "key_string": "'{{ key_string }}'",
                            "encryption": "{{ encryption|string }}",
                            "password_text": "{{ password_text }}",
                            "time_out": "{{ timeout }}",
                        },
                    },
                },
            },
        },
        {
            "name": "redirect.timers",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\stimers\s(?P<adv_timer>\d+)\s(?P<holddown_timer>\d+)
                $""", re.VERBOSE,
            ),
            "compval": "redirect",
            "setval": "standby redirect timers {{ redirect.timers.adv_timer|string }} {{ redirect.timers.holddown_timer|string }}",
            "result": {
                "{{ name }}": {
                    "redirect": {
                        "timers": {
                            "adv_timer": "{{ adv_timer }}",
                            "holddown_timer": "{{ holddown_timer }}",
                        },
                    },
                },
            },
        },
        {
            "name": "redirect.advertisement.authentication",
            "getval": re.compile(
                r"""
                \s*standby\sredirect
                \sadvertisement\sauthentication
                (\smd5\skey-chain\s(?P<key_chain>\S+)|
                \smd5\skey-string\s(?:(?P<encryption>\d+)\s)?(?P<key_string>\S+))?
                (\stimeout\s(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect advertisement authentication"
            "{{ (' md5 key-chain ' + redirect.advertisement.authentication.key_chain|string) "
            "if redirect.advertisement.authentication.key_chain is defined else '' }}"
            "{{ (' md5 key-string ' + "
            "(redirect.advertisement.authentication.encryption|string + ' ') "
            "if redirect.advertisement.authentication.encryption is defined else '' "
            "+ redirect.advertisement.authentication.key_string|string) "
            "if redirect.advertisement.authentication.key_string is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "key_chain": "{{ key_chain }}",
                                "key_string": "'{{ key_string }}'",
                                "encryption": "{{ encryption }}",
                                "time_out": "{{ timeout }}",
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
