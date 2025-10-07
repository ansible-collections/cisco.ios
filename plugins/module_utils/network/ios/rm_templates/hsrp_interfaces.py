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
            "compval": "name",
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
                \s+standby\sversion\s(?P<version>\d+)
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
                    "bfd": "{{ True }}",
                },
            },
        },
        {
            "name": "use-bia",
            "getval": re.compile(
                r"""
                \s+standby\suse-bia\sscope\sinterface
                $""", re.VERBOSE,
            ),
            "setval": "standby use-bia scope interface",
            "result": {
                "{{ name }}": {
                    "use_bia": {
                        "scope": {
                            "interface": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "follow",
            "getval": re.compile(
                r"""
                \s+standby\sfollow\s(?P<follow>.+)
                $""", re.VERBOSE,
            ),
            "setval": "standby follow {{ follow }}",
            "result": {
                "{{ name }}": {
                    "follow": "{{ follow }}",
                },
            },
        },
        {
            "name": "timers.msec",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*timers\smsec\s(?P<hello_interval>\d+)\smsec\s(?P<hold_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ timers.group_no|string if timers.group_no is defined else '' }} timers msec"
            " {{ timers.msec.hello_interval|string }} msec {{ timers.msec.hold_time|string }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "timers": {
                            "msec": {
                                "hello_interval": "{{ hello_interval }}",
                                "hold_time": "{{ hold_time }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*timers\s(?P<hello_interval>\d+)\s(?P<hold_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ timers.group_no|string if timers.group_no is defined else '' }} timers {{ timers.hello_interval }} {{ timers.hold_time }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "timers": {
                            "hello_interval": "{{ hello_interval }}",
                            "hold_time": "{{ hold_time }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "follow.follow",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))
                \s+follow\s+
                (?P<follow>.+)
                $""", re.VERBOSE,
            ),
            "compval": "follow",
            "setval": "standby {{ follow.group_no|string if follow.group_no is defined else '' }} follow {{ follow.follow }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "follow": "{{ follow }}",
                    }],
                },
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*priority\s(?P<priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ priority.group_no|string if priority.group_no is defined else '' }} priority {{ priority.priority|string }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "priority": "{{ priority }}",
                    }],
                },
            },
        },
        {
            "name": "preempt",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*preempt
                (\s(?P<delay>delay))?
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                (\ssync\s(?P<sync>\d+))?
                $""", re.VERBOSE,
            ),
            "remval": "standby "
                      "{{ preempt.group_no|string if preempt.group_no is defined else ''}}"
                      " preempt",
            "setval": "standby "
                      "{{ preempt.group_no|string if preempt.group_no is defined else ''}}"
                      " preempt"
                      "{{ ' delay' if preempt.delay|d(False) else ''}}"
                      "{{ ' minimum ' + preempt.minimum|string if preempt.minimum is defined else ''}}"
                      "{{ ' reload ' + preempt.reload|string if preempt.reload is defined else ''}}"
                      "{{ ' sync ' + preempt.sync|string if preempt.sync is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "preempt": {
                            "enabled": True,
                            "delay": "{{ not not delay }}",
                            "minimum": "{{ minimum }}",
                            "reload": "{{ reload }}",
                            "sync": "{{ sync }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "track",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*track\s(?P<track_no>\d+)
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
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "track": [{
                            "track_no": "{{ track_no }}",
                            "decrement": "{{ decrement }}",
                            "shutdown": "{{ not not shutdown }}",
                        }],
                    }],
                },
            },
        },
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*ip\s+(?P<virtual_ip>\S+)
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
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "ip": [{
                            "virtual_ip": "{{ virtual_ip }}",
                            "secondary": "{{ not not secondary }}",
                        }],
                    }],
                },
            },
        },
        {
            "name": "autoconfig",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))
                \s+ipv6
                (?:\s+(?P<autoconfig>autoconfig))
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no|string if group_no is defined else ''}}"
                      " ipv6"
                      "{{ ' autoconfig' if autoconfig|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "ipv6": {
                            "autoconfig": "{{ not not autoconfig }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "address",
            "getval": re.compile(
                r"""
                \s+standby
                (\s(?P<group_no>\d+))
                \sipv6
                (\s(?P<address>\S+))
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no|string if group_no is defined else ''}}"
                      " ipv6"
                      "{{ ' ' + address if address is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [
                        {
                            "group_no": "{{ group_no }}",
                            "process_ipv6": True,
                            "ipv6_address{{ address }}": "{{ address }}",
                            "address": "{{ address }}",
                        },
                    ],
                },
            },
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*mac-address\s(?P<mac_address>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ mac_address.group_no|string if mac_address.group_no is defined else '' }} mac-address {{ mac_address.mac_address }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "mac_address": "{{ mac_address }}",
                    }],
                },
            },
        },
        {
            "name": "group_name",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*name\s+(?P<group_name>.+)$
                """, re.VERBOSE,
            ),
            "setval": "standby {{ group_name.group_no|string if group_name.group_no is defined else '' }} name {{ group_name.group_name }}",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "group_name": "{{ group_name }}",
                    }],
                },
            },
        },
        {
            "name": "authentication.plain_text",
            "getval": re.compile(
                r"""
                ^\s*standby\s+(?P<group_no>\d+)\s+authentication(?:\s+text)?\s+(?P<password_text>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": (
                "{% if authentication.advertisement.key_string is not defined%}"
                "standby {{ authentication.group_no|string }} "
                "authentication text {{ authentication.advertisement.password_text }}"
                "{% endif %}"
            ),
            "compval": "authentication",
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "password_text": "{{ password_text }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "authentication.md5",
            "getval": re.compile(
                r"""
                ^\s*standby\s+(?P<group_no>\d+)\s+authentication\s+md5\s+
                (?:
                    key-chain\s+(?P<key_chain>\S+)
                    |
                    key-string\s+(?:(?P<encryption>\d+)\s+)?(?P<password_text>\S+)
                    (?:\s+timeout\s+(?P<time_out>\d+))?
                )
                $""",
                re.VERBOSE,
            ),
            "compval": "authentication",
            "setval": (
                "{% if authentication.advertisement.key_string is defined or authentication.advertisement.key_chain is defined %}"
                "standby {{ authentication.group_no|string }} authentication md5 "
                "{% if authentication.advertisement.key_chain is defined %}"
                "key-chain {{ authentication.advertisement.key_chain }}"
                "{% else %}"
                "key-string "
                "{% if authentication.advertisement.encryption is defined %}"
                "{{ authentication.advertisement.encryption }} "
                "{% endif %}"
                "{{ authentication.advertisement.password_text }} "
                "{% if authentication.advertisement.time_out is defined %}"
                "timeout {{ authentication.advertisement.time_out|string }}"
                "{% endif %}"
                "{% endif %}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "key_chain": "{{ key_chain }}",
                                "key_string": "{{ True if key_chain is not defined else None}}",
                                "password_text": "{{ password_text }}",
                                "encryption": "{{ encryption }}",
                                "time_out": "{{ time_out }}",
                            },
                        },
                    }],
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
            "name": "redirect.md5.key_chain",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\sadvertisement\sauthentication\smd5\skey-chain\s(?P<key_chain>\S+)
                $""", re.VERBOSE,
            ),
            "compval": "redirect",
            "setval": "standby redirect advertisement authentication md5 key-chain {{ redirect.advertisement.authentication.key_chain }}",
            "result": {
                "{{ name }}": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "key_chain": "{{ key_chain }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "redirect.md5.key_string",
            "getval": re.compile(
                r"""
                \s*standby\s+
                redirect\s+
                advertisement\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<encryption>0|7)\s+
                (?P<password_text>\S+)\s*
                (?:\s*timeout\s+(?P<time_out>\d+))?
                $""", re.VERBOSE,
            ),
            "compval": "redirect",
            "setval": "standby redirect advertisement authentication md5 key-string {{ redirect.advertisement.authentication.encryption|string }} "
            "{{ redirect.advertisement.authentication.password_text }} "
            "{{ 'timeout ' + redirect.advertisement.authentication.time_out|string if redirect.advertisement.authentication.time_out is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "encryption": "{{ encryption }}",
                                "key_string": "{{ True }}",
                                "password_text": "{{ password_text }}",
                                "time_out": "{{ time_out }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "redirect.md5.key_string_without_encryption",
            "getval": re.compile(
                r"""
                \s*standby\s+
                redirect\s+
                advertisement\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<password_text>\S+)\s*
                (?:\s*timeout\s+(?P<time_out>\d+))?
                $""", re.VERBOSE,
            ),
            "compval": "redirect",
            "setval": "standby redirect advertisement authentication md5 key-string {{ redirect.advertisement.authentication.password_text }} "
            "{{ 'timeout ' + redirect.advertisement.authentication.time_out|string if redirect.advertisement.authentication.time_out is defined else '' }}",
            "result": {
                "{{ name }}": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "key_string": "{{ True }}",
                                "password_text": "{{ password_text }}",
                                "time_out": "{{ time_out }}",
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
