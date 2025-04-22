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
            "name": "mac_refresh",
            "getval": re.compile(
                r"""
                \s+standby\smac-refresh\s(?P<mac_refresh_number>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby mac-refresh {{ standby_mac_refresh }}",
            "result": {
                "standby_mac_refresh": {
                    "mac_refresh": "{{ mac_refresh_number }}",
                },
            },
        },
        {
            "name": "standby_version",
            "getval": re.compile(
                r"""
                \s+standby\sversion\s(?P<version>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby version {{ version }}",
            "result": {
                "standby_version": {
                    "version": "{{ version }}",
                },
            },
        },
        {
            "name": "standby.delay",
            "getval": re.compile(
                r"""
                \s+standby\sdelay
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby delay"
                      "{{ ' ' + minimum if standby.delay.minimum is not None else ''}}"
                      "{{ ' ' + reload if standby.delay.reload is not None else ''}}",
            "result": {
                "standby.delay": {
                    "delay": {
                        "minimum": "{{ minimum }}",
                        "reload": "{{ reload }}",
                    },
                },
            },
        },
        {
            "name": "standby_bfd",
            "getval": re.compile(
                r"""
                \s+standby\sbfd\s
                $""", re.VERBOSE,
            ),
            "setval": "standby bfd",
            "result": {
                "standby_bfd": {
                    "bfd": "{{ True }}",
                },
            },
        },
        {
            "name": "use-bia.scope",
            "getval": re.compile(
                r"""
                \s+standby\suse-bia\sscope\sinterface
                $""", re.VERBOSE,
            ),
            "setval": "standby use-bia scope interface",
            "result": {
                "use-bia.scope": {
                    "use_bia": {
                        "scope": {
                            "interface": "{{ True }}",
                        },
                    },
                },
            },
        },
        {
            "name": "standby_follow",
            "getval": re.compile(
                r"""
                \s+standby\sfollow\s(?P<follow>.+)
                $""", re.VERBOSE,
            ),
            "setval": "standby follow {{ follow }}",
            "result": {
                "standby_follow": {
                    "follow": "{{ follow }}",
                },
            },
        },
        {
            "name": "standby_timers.msec",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*timers\smsec\s(?P<hello_interval_millis>\d+)\smsec\s(?P<hold_time_millis>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if standby_timers.msec.group_no is not None else '' }} timers msec {{ standby_timers.msec.hello_interval_millis }} msec {{ standby_timers.msec.hold_time_millis }}",
            "result": {
                "standby_timers.msec": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "timers": {
                            "msec": {
                                "hello_interval": "{{ hello_interval_millis }}",
                                "hold_time": "{{ hold_time_millis }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_timers.hello_interval",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*timers\s(?P<hello_interval>\d+)\s(?P<hold_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} timers {{ hello_interval }} {{ hold_time }}",
            "result": {
                "standby_timers.msec": {
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
            "name": "standby_group_follow",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))
                \s+follow\s+
                (?P<follow>.+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} follow {{ follow }}",
            "result": {
                "standby_group_follow": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "follow": "{{ follow }}",
                    }],
                },
            },
        },
        {
            "name": "standby_priority",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*priority\s(?P<priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} priority {{ priority }}",
            "result": {
                "standby_priority": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "priority": "{{ priority }}",
                    }],
                },
            },
        },
        {
            "name": "standby.preempt",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*preempt
                (\s(?P<delay>delay))?
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                (\ssync\s(?P<sync>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.preempt.group_no is not None else ''}}"
                      " preempt"
                      "{{ ' delay' if standby.preempt.delay|d(False) else ''}}"
                      "{{ ' ' + minimum if standby.preempt.minimum is not None else ''}}"
                      "{{ ' ' + reload if standby.preempt.reload is not None else ''}}"
                      "{{ ' ' + sync if standby.preempt.sync is not None else ''}}",
            "result": {
                "standby.preempt": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "preempt": {
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
            "name": "standby.track",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*track\s(?P<track_no>\d+)
                (\sdecrement\s(?P<decrement>\d+))?
                (\s(?P<shutdown>shutdown))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.track.group_no is not None else ''}}"
                      " track"
                      "{{ ' ' + track_no if standby.track.track_no is not None else ''}}"
                      "{{ ' ' + decrement if standby.track.decrement is not None else ''}}"
                      "{{ ' shutdown' if standby.track.shutdown|d(False) else ''}}",
            "result": {
                "standby.track": {
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
            "name": "standby.ip",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*ip\s+(?P<virtual_ip>\S+)
                (\s(?P<secondary>secondary))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.ip.group_no is not None else ''}}"
                      " ip"
                      "{{ ' ' + virtual_ip if standby.ip.virtual_ip is not None else ''}}"
                      "{{ ' secondary' if standby.ip.secondary|d(False) else ''}}",
            "result": {
                "standby.ip": {
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
            "name": "standby.ipv6.link",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))?
                \s+ipv6\s+
                (?P<ipv6_link>[a-fA-F0-9:]+)
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.ipv6.link.group_no is not None else ''}}"
                      " ipv6"
                      "{{ ' ' + ipv6_link if standby.ipv6.link.ipv6_link is not None else ''}}",
            "result": {
                "stanby.ipv6.link": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "ipv6": {
                            "virtual_ipv6": "{{ ipv6_link }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "standby.ipv6.prefix",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))?
                \s+ipv6\s+
                (?P<ipv6_link_prefix>[a-fA-F0-9:]+\/\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.ipv6.prefix.group_no is not None else ''}}"
                      " ipv6"
                      "{{ ' ' + ipv6_link_prefix if standby.ipv6.prefix.ipv6_link_prefix is not None else ''}}",
            "result": {
                "stanby.ipv6.prefix": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "ipv6": {
                            "virtual_ipv6_prefix": "{{ ipv6_link_prefix }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "standby.ipv6.autoconfig",
            "getval": re.compile(
                r"""
                \s*standby
                (?:\s+(?P<group_no>\d+))
                \s+ipv6
                (?:\s+(?P<autoconfig>autoconfig))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.ipv6.autoconfig.group_no is not None else ''}}"
                      " ipv6"
                      "{{ ' autoconfig' if standby.ipv6.autoconfig|d(False) else ''}}",
            "result": {
                "stanby.ipv6.autoconfig": {
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
            "name": "standby_mac_address",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*mac-address\s(?P<mac_address>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} mac-address {{ mac_address }}",
            "result": {
                "standby_mac_address": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "mac_address": "{{ mac_address }}",
                    }],
                },
            },
        },
        {
            "name": "standby_group_name",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*name\s+(?P<name>.+)$
                """, re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} name {{ name }}",
            "result": {
                "standby_group_name": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "group_name": "{{ name }}",
                    }],
                },
            },
        },
        # {
        #     "name": "name",
        #     "getval": re.compile(
        #         r"""
        #         ^name\s+(?P<name>.+)$
        #         """, re.VERBOSE,
        #     ),
        #     "setval": "name {{ name }}",
        #     "result": {
        #         "name": "{{ name }}",
        #     }
        # },
        {
            "name": "standby_authentication.plain_text",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*authentication\stext\s(?P<password_text>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication text {{ password_text }}",
            "result": {
                "standby_authentication.plain_text": {
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
            "name": "standby_authentication.text",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*authentication\s(?P<password_text>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication {{ ' ' + password_text if standby_authentication.text.password_text.lower() != 'md5' else '' }}",
            "result": {
                "standby_authentication.text": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "password_text": "{{ password_text if password_text.lower() != 'md5' else ''}}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_authentication.md5.key_chain",
            "getval": re.compile(
                r"""
                \s+standby\s*(?P<group_no>\d+)?\s*authentication\smd5\skey-chain\s(?P<key_chain>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication md5 key-chain {{ key_chain }}",
            "result": {
                "standby_authentication.md5.key_chain": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "key_chain": "{{ key_chain }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_authentication.md5.key_string",
            "getval": re.compile(
                r"""
                \s*standby\s+
                (?P<group_no>\d+)\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<key_encryption>0|7)\s+
                (?P<password>\S+)\s*
                (?:\s*timeout\s+(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication md5 key-string {{ key_encryption }} {{ password }} {{ 'timeout ' timeout if timeout is not None else '' }}",
            "result": {
                "standby_authentication.md5.key_string": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "key_string": "{{ True }}",
                                "encryption" : "{{ key_encryption }}",
                                "password_text": "{{ password }}",
                                "timeout": "{{ timeout }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_authentication.md5.key_string_without_encryption",
            "getval": re.compile(
                r"""
                \s*standby\s+
                (?P<group_no>\d+)\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<password>\S+)\s*
                (?:\s*timeout\s+(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication md5 key-string {{ key_type }} {{ key_string }} {{ 'timeout ' timeout if timeout is not None else '' }}",
            "result": {
                "standby_authentication.md5.key_string_without_encryption": {
                    "standby_groups": [{
                        "group_no": "{{ group_no }}",
                        "authentication": {
                            "advertisement": {
                                "key_string": "{{ True }}",
                                "password_text": "{{ password }}",
                                "timeout": "{{ timeout }}",
                            },
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_redirect.timers",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\stimers\s(?P<timers>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect timers {{ timers }}",
            "result": {
                "standby_redirect.timers": {
                    "standby_groups": [{
                        "redirect": {
                            "timers": "{{ timers }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_redirect.unknown",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\sunknown
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect unknown",
            "result": {
                "standby_redirect.unknown": {
                    "standby_groups": [{
                        "redirect": {
                            "unknown": "{{ True }}",
                        },
                    }],
                },
            },
        },
        {
            "name": "standby_redirect.md5.key_chain",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\sadvertisement\sauthentication\smd5\skey-chain\s(?P<key_chain>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect advertisement authentication md5 key-chain {{ key_chain }}",
            "result": {
                "standby_redirect.md5.key_chain": {
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
            "name": "standby_redirect.md5.key_string",
            "getval": re.compile(
                r"""
                \s*standby\s+
                redirect\s+
                advertisement\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<key_encryption>0|7)\s+
                (?P<password>\S+)\s*
                (?:\s*timeout\s+(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect advertisement authentication md5 key-string {{ key_encryption }} {{ password }} {{ 'timeout ' timeout if timeout is not None else '' }}",
            "result": {
                "standby_redirect.md5.key_string": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "encryption" : "{{ encryption }}",
                                "key_string": "{{ True }}",
                                "password_text": "{{ password }}",
                                "timeout": "{{ timeout }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "standby_redirect.md5.key_string_without_encryption",
            "getval": re.compile(
                r"""
                \s*standby\s+
                redirect\s+
                advertisement\s+
                authentication\s+md5\s+
                key-string\s+
                (?P<password>\S+)\s*
                (?:\s*timeout\s+(?P<timeout>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect advertisement authentication md5 key-string {{ password }} {{ 'timeout ' timeout if timeout is not None else '' }}",
            "result": {
                "standby_redirect.md5.key_string_without_encryption": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "key_string": "{{ True }}",
                                "password_text": "{{ password }}",
                                "timeout": "{{ timeout }}",
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
