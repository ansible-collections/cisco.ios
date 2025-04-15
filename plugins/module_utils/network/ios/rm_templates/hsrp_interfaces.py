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
        # {
        #     "name": "key_a",
        #     "getval": re.compile(
        #         r"""
        #         ^key_a\s(?P<key_a>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "",
        #     "result": {
        #     },
        #     "shared": True,
        # },
        # {
        #     "name": "key_b",
        #     "getval": re.compile(
        #         r"""
        #         \s+key_b\s(?P<key_b>\S+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "",
        #     "result": {
        #     },
        # },
        {
            "name": "standby_mac_refresh",
            "getval": re.compile(
                r"""
                \s+standby\smac-refresh\s(?P<mac_refresh_number>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby mac-refresh {{ standby_mac_refresh }}",
            "result": {
                "standby_groups": {
                "mac_refresh": "{{ mac_refresh_number }}",
                }
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
                "standby_groups": {
                "version": "{{ version }}",
                }
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
                "{{ name }}": {
                    "delay": {
                        "minimum": "{{ minimum }}",
                        "reload": "{{ reload }}"
                    },
                },
            },
        },
        # {
        #     "name": "delay.reload",
        #     "getval": re.compile(
        #         r"""
        #         \s+standby\sdelay\sreload\s(?P<reload_number>\d+)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "standby delay reload {{ delay.reload }}",
        #     "result": {
        #         "{{ name }}": {
        #             "delay": {
        #                 "reload": "{{ reload_number }}",
        #             },
        #         },
        #     },
        # },
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
                    "bfd": "{{ True }}"
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
                "{{ name }}": {
                    "use_bia": {
                        "scope": {
                            "interface": "{{ True }}"
                        }
                    },
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
            "setval": "standby version {{ standby_version }}",
            "result": {
                "version": "{{ version }}",
            },
        },
        {
            "name": "standby_follow",
            "getval": re.compile(
                r"""
                \s+standby\s((?:\s+(?P<group_no>\d+))?\sfollow\s(?P<follow>.+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} follow {{ follow }}",
            "result": {
                "group_no": "{{ group_no }}",
                "follow": "{{ follow }}",
            },
        },
        {
            "name": "standby_timers.msec",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\stimers\smsec\s(?P<hello_interval_millis>\d+)\smsec\s(?P<hold_time_millis>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} timers msec {{ hello_interval_millis }} msec {{ hold_time_millis }}",
            "result": {
                "group_no": "{{ group_no }}",
                "timers": {
                    "msec": {
                        "hello_interval": "{{ hello_interval_millis }}",
                        "hold_time": "{{ hold_time_millis }}"
                    }
                }
            },
        },
        {
            "name": "standby_timers.hello_interval",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\stimers\s(?P<hello_interval>\d+)\s(?P<hold_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} timers {{ hello_interval }} {{ hold_time }}",
            "result": {
                "group_no": "{{ group_no }}",
                "timers": {
                    "hello_interval": "{{ hello_interval }}",
                    "hold_time": "{{ hold_time }}"
                }
            },
        },
        {
            "name": "standby_priority",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\spriority\s(?P<priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} priority {{ priority }}",
            "result": {
                "group_no": "{{ group_no }}",
                "priority": "{{ priority }}",
            },
        },
        {
            "name": "standby.preempt",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\spreempt
                (\sdelay\s(?P<has_delay>\b+))?
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                (\ssync\s(?P<sync>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.preempt.group_no is not None else ''}}"
                      " preempt"
                      "{{ ' delay' if standby.preempt.has_delay else ''}}"
                      "{{ ' ' + minimum if standby.preempt.minimum is not None else ''}}"
                      "{{ ' ' + reload if standby.preempt.reload is not None else ''}}"
                      "{{ ' ' + sync if standby.preempt.sync is not None else ''}}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "preempt": {
                        "delay": "{{ true if has_delay else false }}",
                        "minimum": "{{ minimum }}",
                        "reload": "{{ reload }}",
                        "sync": "{{ sync }}",
                    },
                },
            },
        },
        {
            "name": "standby.track",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?
                \strack\s(?P<track_no>\d+)
                (\sdecrement\s(?P<decrement>\d+))?
                (\sshutdown\s(?P<has_shutdown>\b+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.track.group_no is not None else ''}}"
                      " track"
                      "{{ ' ' + track_no if standby.track.track_no is not None else ''}}"
                      "{{ ' ' + decrement if standby.track.decrement is not None else ''}}"
                      "{{ ' shutdown' if standby.track.has_shutdown else ''}}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "track": {
                        "track_no": "{{ track_no }}",
                        "decrement": "{{ decrement }}",
                        "shutdown": "{{ true if has_shutdown else false }}",
                    },
                },
            },
        },
        {
            "name": "standby.ip",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?
                \s+ip\s+(?P<virtual_ip>\S+) 
                (\ssecondary\s(?P<has_secondary>\b+))?
                $""", re.VERBOSE,
            ),
            "setval": "standby"
                      "{{ ' ' + group_no if standby.ip.group_no is not None else ''}}"
                      " ip"
                      "{{ ' ' + virtual_ip if standby.ip.virtual_ip is not None else ''}}"
                      "{{ ' secondary' if standby.ip.has_secondary else ''}}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "ip": {
                        "virtual_ip": "{{ virtual_ip }}",
                        "secondary": "{{ True if has_secondary else False }}",
                    },
                },
            },
        },
        # {
        #     "name": "standby.ipv6",
        #     "getval": re.compile(
        #         r"""
        #         \s+standby\s(?:\s+(?P<group_no>\d+))?\sip
        #         (\svirtual_ip\s(?P<virtual_ip>\S+))?
        #         (\ssecondary\s(?P<has_secondary>\b+))?
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "standby"
        #               "{{ ' ' + group_no if standby.ip.group_no is not None else ''}}"
        #               " ip"
        #               "{{ ' ' + virtual_ip if standby.ip.virtual_ip is not None else ''}}"
        #               "{{ ' secondary' if standby.ip.has_secondary else ''}}",
        #     "result": {
        #         "standby_groups": {
        #             "group_no": "{{ group_no }}",
        #             "ip": {
        #                 "virtual_ip": "{{ virtual_ip }}",
        #                 "secondary": "{{ True if has_secondary else False }}",
        #             },
        #         },
        #     },
        # },
        {
            "name": "standby_mac_address",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\smac-address\s(?P<mac_address>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} mac-address {{ mac_address }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "mac_address": "{{ mac_address }}",
                }
            },
        },
        {
            "name": "standby_name",
            "getval": re.compile(
                r"""
                ^standby\s+(?:\s+(?P<group_no>\d+))?\s+name\s+(?P<name>.+)$
                """, re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} name {{ name }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "name": "{{ name }}",
                }
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
                \s+standby\s(?:\s+(?P<group_no>\d+))?\sauthentication\stext\s(?P<password_text>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication text {{ password_text }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "authentication": {
                        "password_text": "{{ password_text }}"
                    }
                }
            },
        },
        {
            "name": "standby_authentication.text",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\sauthentication\s(?P<password_text>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication {{ ' ' + password_text if standby_authentication.text.password_text.lower() != 'md5' else '' }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "authentication": {
                        "password_text": "{{ password_text if password_text.lower() != 'md5' else ''}}"
                    }
                }
            },
        },
        {
            "name": "standby_authentication.md5.key_chain",
            "getval": re.compile(
                r"""
                \s+standby\s(?:\s+(?P<group_no>\d+))?\sauthentication\smd5\skey-chain\s(?P<key_chain>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication md5 key-chain {{ key_chain }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "authentication": {
                        "md5": {
                            "key_chain": "{{ key_chain }}"
                        }
                    }
                }
            },
        },
        {
            "name": "standby_authentication.md5.key_string",
            "getval": re.compile(
                r"""
                \s+standby\s(?P<group_no>\d+)\sauthentication\smd5\skey-string\s(?P<key_type>\d+)\s(?P<key_string>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby {{ group_no if group_no is not None else '' }} authentication md5 key-string {{ key_type }} {{ key_string }}",
            "result": {
                "standby_groups": {
                    "group_no": "{{ group_no }}",
                    "authentication": {
                        "md5": {
                            "key_string": {
                                "key_type" : "{{ key_type }}",
                                "password_text": "{{ key_string }}"
                            }
                        }
                    }
                }
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
                "standby_groups": {
                    "redirect": {
                        "timers": "{{ timers }}"
                    }
                }
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
                "standby_groups": {
                    "redirect": {
                        "unknown": "{{ True }}"
                    }
                }
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
                "standby_groups": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "md5": {
                                    "key_chain": "{{ key_chain }}"
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "standby_redirect.md5.key_string",
            "getval": re.compile(
                r"""
                \s+standby\sredirect\sadvertisement\sauthentication\smd5\skey-string\s(?P<key_type>\d+)\s(?P<key_string>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "standby redirect advertisement authentication md5 key-string {{ key_type }} {{ key_string }}",
            "result": {
                "standby_groups": {
                    "redirect": {
                        "advertisement": {
                            "authentication": {
                                "md5": {
                                    "key_string": {
                                        "key_type" : "{{ key_type }}",
                                        "key_string": "{{ key_string }}"
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
    ]
    # fmt: on
