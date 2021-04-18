# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Logging_global parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)

class Logging_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Logging_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "host",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<filtered>filtered)*
                \s*(?P<xml>xml)*
                \s*(?P<sequence_num_session>sequence-num-session)*
                \s*(?P<vrf>\svrf\s\S+)*
                \s*(?P<discriminator>discriminator\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [
                        {"hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "discriminator" : "{{ discriminator.split('discriminator ')[1] }}",
                        "vrf" : "{{ vrf.split('vrf ')[1] }}",
                        "xml" : "{{ True if xml is defined }}",
                        "filtered" : "{{ True if filtered is defined }}",
                        "sequence_num_session" : "{{ True if sequence_num_session is defined }}" }
                        ]
                }
            },
        },
        {
            "name": "host.transport",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<transport>transport\stcp|udp)*
                \s*(?P<audit>audit)*
                \s*(?P<sequence_num_session>sequence-num-session)*
                \s*(?P<xml>xml)*
                \s*(?P<discriminator>discriminator\s.+$)*
                \s*(?P<port>port\s[1-9][0-9]*)*
                \s*(?P<filtered>filtered\sstream\s[1-9][0-9]*)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "transport": {
                            "{{ transport.split('transport ')[1] if transport is defined }}" : {
                                    "audit" : "{{ True if audit is defined }}",
                                    "sequence_num_session" : "{{ True if sequence_num_session is defined }}",
                                    "xml" : "{{ True if xml is defined }}",
                                    "discriminator" : "{{ discriminator.split('discriminator ')[1] if discriminator is defined }}",
                                    "port" : "{{ port.split('port ')[1] if port is defined }}",
                                    "filtered" : "{{ port.split('port ')[1] if port is defined }}",
                                }
                            }
                        }
                    ]
                }
            },
        },
        {
            "name": "host.transport.udp.session_id",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<transport>transport\sudp\ssession-id)*
                \s*(?P<tag>hostname|ipv4|ipv6)*
                \s*(?P<text>\sstring\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "transport": {
                            "udp" : {
                                "session_id": {
                                    "tag" : "{{ tag }}",
                                    "text" : "{{ text.split('string ')[1] if text is defined }}",
                                    }
                                }
                            }
                        }
                    ]
                }
            },
        },
        {
            "name": "host.transport.tcp.session_id",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<transport>transport\stcp\ssession-id)*
                \s*(?P<tag>hostname|ipv4|ipv6)*
                \s*(?P<text>\sstring\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "transport": {
                                "tcp": {
                                    "session_id": {
                                        "tag" : "{{ tag }}",
                                        "text" : "{{ text.split('string ')[1] if text is defined }}",
                                    }
                                }
                            }    
                        }
                    ]
                }
            },
        },
        {
            "name": "host.transport.tcp.filtered",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<transport>transport\stcp\sfiltered)*
                \s*(?P<stream>stream\s[1-9][0-9]*)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "transport": {
                                "tcp" : {
                                    "filtered": {
                                        "stream" : "{{ stream.split('stream ')[1] if stream is defined }}",
                                    }
                                }
                            }        
                        }
                    ]
                }
            },
        },
        {
            "name": "host.transport.udp.filtered",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<transport>transport\sudp\sfiltered)*
                \s*(?P<stream>stream\s[1-9][0-9]*)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}",
                        "transport": {
                                "udp" : {
                                    "filtered": {
                                        "stream" : "{{ stream.split('stream ')[1] if stream is defined }}",
                                    }
                                }
                            }   
                        }
                    ]
                }
            },
        },
        {
            "name": "host.session_id",
            "getval": re.compile(
                r"""
                ^logging\shost
                \s*(?P<hostname>\S+)*
                \s*(?P<ipv6>\sipv6\s\S+)*
                \s*(?P<session_id>session-id)*
                \s*(?P<tag>hostname|ipv4|ipv6)*
                \s*(?P<text>\sstring\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "{{ hostname if hostname is defined or ipv6.split('ipv6 ')[1] if ipv6 is defined }}" : {
                    "host": [{
                        "hostname" : "{{ hostname }}",
                        "ipv6" : "{{ ipv6.split('ipv6 ')[1] if ipv6 is defined }}", 
                        "session_id": {
                            "tag" : "{{ tag }}",
                            "text" : "{{ text.split('string ')[1] if text is defined }}",  
                            }
                        }
                    ]
                }
            },
        },
        {
            "name": "buffered",
            "getval": re.compile(
                r"""
                ^logging\sbuffered
                \s*(?P<filtered>filtered)*
                \s*(?P<xml>xml)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                \s*(?P<discriminator>discriminator\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging buffered",
            "result": { 
                "logging": {
                    "buffered" : {
                        "filtered" : "{{ True if filtered is defined }}",
                        "xml" : "{{ True if xml is defined }}",
                        "severity" : "{{ severity if severity is defined }}",
                        "discriminator" : "{{ discriminator.split('discriminator ')[1] if discriminator is defined }}",
                    }
                }
            },
        },
        {
            "name": "buffered.size",
            "getval": re.compile(
                r"""
                ^logging\sbuffered
                \s*(?P<size>[1-9][0-9]*)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings$)*
                $""", re.VERBOSE),
            "setval": "logging buffer",
            "result": { 
                "logging": {
                    "buffered" : {
                        "size" : "{{ size }}",
                        "severity" : "{{ severity if severity is defined }}",
                    }
                }
            },
        },
        {
            "name": "buginf",
            "getval": re.compile(
                r"""
                ^logging
                \s*(?P<buginf>buginf)*
                $""", re.VERBOSE),
            "setval": "logging {{ buginf }}",
            "result": { 
                "logging": { 
                    "{{ buginf }}": "{{ True if buginf is defined }}"
                } 
            },
        },
        {
            "name": "cns_events",
            "getval": re.compile(
                r"""
                ^logging
                \s*cns-events*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                $""", re.VERBOSE),
            "setval": "logging cns-events",
            "result": { 
                "logging": {
                    "cns_events": "{{ severity }}"   
                }
            },
        },
        {
            "name": "console",
            "getval": re.compile(
                r"""
                ^logging\sconsole
                \s*(?P<filtered>filtered)*
                \s*(?P<xml>xml)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings|guaranteed$)*
                \s*(?P<discriminator>discriminator\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging console",
            "result": { 
                "logging": {
                    "console": {
                        "severity" : "{{ severity }}",
                        "discriminator" : "{{ discriminator }}",
                        "filtered" : "{{ True if filtered is defined }}",
                        "xml" : "{{ True if xml is defined }}",
                    }
                }
            },
        },
        {
            "name": "count",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<count>count)
                $""", re.VERBOSE),
            "setval": "logging {{ count }}",
            "result": { 
                "logging": {
                    "count": "{{ True if count is defined }}"
                } 
            },
        },
        {
            "name": "delimiter",
            "getval": re.compile(
                r"""
                ^logging
                \s*(?P<delimiter>delimiter)*
                \s*(?P<tcp>tcp)*
                $""", re.VERBOSE),
            "setval": "logging delimiter tcp",
            "result": { 
                "logging": {
                    "delimiter": {
                        "tcp": "{{ True if tcp is defined }}"
                    }    
                } 
            },
        },
        {
            "name": "discriminator",
            "getval": re.compile(
                r"""
                ^logging\sdiscriminator\s(?P<discriminator>.+$)
                $""", re.VERBOSE),
            "setval": "logging discriminator",
            "result": { 
                "logging": { 
                    "discriminator": "{{ discriminator }}"
                } 
            },
        },
        {
            "name": "dmvpn",
            "getval": re.compile(
                r"""
                ^logging\sdmvpn
                \s*(?P<rate_limit>rate-limit)*
                \s*(?P<rate>\d+)*
                $""", re.VERBOSE),
            "setval": "logging dmvpn",
            "result": { 
                "logging": {
                    "dmvpn": {
                        "rate_limit": "{{ rate }}",
                    }
                } 
            },
        },
        {
            "name": "esm",
            "getval": re.compile(
                r"""
                ^logging\sesm\s(?P<config>config)
                $""", re.VERBOSE),
            "setval": "logging esm",
            "result": {
                "logging": {
                    "esm" : { 
                        "config": "{{ True if config is defined }}"
                    }
                } 
            },
        },
        {
            "name": "exception",
            "getval": re.compile(
                r"""
                ^logging\sexception
                \s(?P<exception>[1-9][0-9]*)
                $""", re.VERBOSE),
            "setval": "logging exception",
            "result": { 
                "logging": {
                    "exception": "{{ exception }}"
                } 
            },
        },
        {
            "name": "facility",
            "getval": re.compile(
                r"""
                ^logging\sfacility
                \s(?P<facility>auth|cron|daemon|kern|local0|local1|local2|local3|local4|local5|local6|local7|lpr|mail|news|sys10|sys11|sys12|sys13|sys14|sys9|syslog|user|uucp)
                $""", re.VERBOSE),
            "setval": "logging facility",
            "result": {
                "logging" : {
                    "facility": "{{ facility }}"
                } 
            },
        },
        # { #breaks the code maybe Checking
        #     "name": "filter",
        #     "getval": re.compile(
        #         r"""
        #         ^logging
        #         \s*filter*
        #         \s*(?P<url>\S+)*
        #         \s*(?P<order>\d+)*
        #         \s*(?P<args>args\s\S+)*
        #         $""", re.VERBOSE),
        #     "setval": "logging filter",
        #     "result": { 
        #         "logging": {
        #             "filter": {
        #                 "url" : "{{ url }}",
        #                 "order" : "{{ order }}",
        #                 "args" : "{{ args }}",
        #             }
        #         } 
        #     },
        # },
        {
            "name": "history",
            "getval": re.compile(
                r"""
                ^logging\shistory
                \s*(?P<size>\d+)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                $""", re.VERBOSE),
            "setval": "logging history",
            "result": { 
                "logging": {
                    "history": { 
                        "severity" : "{{ severity }}",
                        "size" : "{{ size }}" 
                    }
                }
            },
        },
        {
            "name": "message_counter",
            "getval": re.compile(
                r"""
                ^logging\smessage-counter
                \s(?P<counter>log|debug|syslog)
                $""", re.VERBOSE),
            "setval": "logging message-counter",
            "result": { 
                "{{ counter }}" : {
                    "message_counter": "{{ counter }}",
                }
            },
        },
        {
            "name": "monitor",
            "getval": re.compile(
                r"""
                ^logging\smonitor
                \s*(?P<filtered>filtered)*
                \s*(?P<xml>xml)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                \s*(?P<discriminator>discriminator\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging monitor",
            "result": { 
                "logging": {
                    "monitor" :{
                        "filtered" : "{{ True if filtered is defined }}",
                        "xml" : "{{ True if xml is defined }}",
                        "severity" : "{{ severity }}",
                        "discriminator" : "{{ discriminator }}",
                    }
                }
            },
        },
        {
            "name": "logging_on",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<on>on)
                $""", re.VERBOSE),
            "setval": "logging",
            "result": {
                "logging": {
                    "logging_on" : "{{ True if on is defined }}"
                }
            },
        },
        {
            "name": "origin_id",
            "getval": re.compile(
                r"""
                ^logging\sorigin-id
                \s*(?P<tag>hostname|ipv4|ipv6)*
                \s*(?P<text>\sstring\s.+$)*
                $""", re.VERBOSE),
            "setval": "logging host",
            "result": { 
                "logging" : {
                    "origin_id": {
                            "tag" : "{{ tag }}",
                            "text" : "{{ text.split('string ')[1] if text is defined }}",  
                    }  
                }
            },
        },
        {
            "name": "persistent",
            "getval": re.compile(
                r"""
                ^logging\spersistent
                \s*(?P<immediate>immediate)*
                \s*(?P<notify>notify)*
                \s*(?P<protected>protected)*
                \s*(?P<batch>batch\s\d+)*
                \s*(?P<filesize>filesize\s\d+)*
                \s*(?P<size>size\s\d+)*
                \s*(?P<threshold>threshold\s\d+)*
                \s*(?P<url>url\s\S+)*
                $""", re.VERBOSE),
            "setval": "logging persistent",
            "result": { 
                "logging":{
                    "persistent" : [{
                        "batch": "{{ batch.split('batch ')[1] if batch is defined }}",
                        "filesize": "{{ filesize.split('filesize ')[1] if filesize is defined }}",
                        "immediate": "{{ True if immediate is defined }}",
                        "notify": "{{ True if notify is defined }}",
                        "protected": "{{ True if protected is defined }}",
                        "size": "{{ size.split('size ')[1] if size is defined }}",
                        "threshold": "{{ threshold.split('threshold ')[1] if threshold is defined }}",
                        "url": "{{ url.split('url ')[1] if url is defined }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "policy_firewall",
            "getval": re.compile(
                r"""
                ^logging\spolicy-firewall
                \s*(?P<rate_limit>rate-limit)*
                \s*(?P<rate>\d+)*
                $""", re.VERBOSE),
            "setval": "logging policy-firewall",
            "result": { 
                "logging": {
                    "policy_firewall": {
                        "rate_limit": "{{ rate }}",
                    }
                } 
            },
        },
        {
            "name": "queue_limit",
            "getval": re.compile(
                r"""
                ^logging\squeue-limit
                \s*(?P<size>[1-9][0-9]*)*
                \s*(?P<esm>esm\s[1-9][0-9]*)*
                \s*(?P<trap>trap\s[1-9][0-9]*)*
                $""", re.VERBOSE),
            "setval": "logging queue_limit",
            "result": { 
                "logging": {
                    "queue_limit": {
                        "size": "{{ size }}",
                        "esm": "{{ esm.split('esm ')[1] if esm is defined }}",
                        "trap": "{{ trap.split('trap ')[1] if trap is defined }}",
                    }
                } 
            },
        },
        {
            "name": "rate_limit",
            "getval": re.compile(
                r"""
                ^logging\srate-limit
                (\s(?P<option>all|console))?
                (\s(?P<size>[1-9][0-9]*))?
                (\sexcept\s(?P<except>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": "logging rate_limit",
            "result": { 
                "logging": {
                    "rate_limit": {
                        "size": "{{ size }}",
                        "all": "{{ True if option == 'all' }}",
                        "console": "{{ True if option == 'console' }}",
                    }
                } 
            },
        },
        {
            "name": "reload",
            "getval": re.compile(
                r"""
                ^logging
                \s*(?P<reload>reload)*
                \s*(?P<message_limit>message-limit\s[1-9][0-9]*)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                $""", re.VERBOSE),
            "setval": "logging reload",
            "result": { 
                "logging": {
                    "reload": {
                        "severity": "{{ severity }}",
                        "message_limit": "{{ message_limit.split('message-limit ')[1] if message_limit is defined }}",
                    }
                } 
            },
        },
        {
            "name": "server_arp",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<server_arp>server-arp)
                $""", re.VERBOSE),
            "setval": "logging server-arp",
            "result": {
                "logging": {
                    "server_arp" : "{{ True if server_arp is defined }}"
                }
            },
        },
        {
            "name": "snmp_trap",
            "getval": re.compile(
                r"""
                ^logging
                \s*(?P<snmp_trap>snmp-trap)*
                \s*(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)*
                $""", re.VERBOSE),
            "setval": "logging snmp_trap",
            "result": { 
                "logging": {
                    "snmp_trap": "{{ severity }}",                      
                }
            },
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<source_interface>source-interface)
                \s(?P<interface>\.+)
                \s*(?P<vrf>vrf\s\S+)*
                $""", re.VERBOSE),
            "setval": "logging snmp_trap",
            "result": { 
                "{{ interface }}": {
                        "source_interface": [{
                            "interface": "{{ interface }}",
                            "vrf": "{{ vrf.split('vrf ')[1] if text is defined }}",                       
                        }
                    ]
                } 
            },
        },
        {
            "name": "trap",
            "getval": re.compile(
                r"""
                ^logging\strap
                \s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)
                $""", re.VERBOSE),
            "setval": "logging trap",
            "result": { 
                "logging": {
                    "trap": "{{ severity }}",                       
                }
            },
        },
        {
            "name": "userinfo",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<userinfo>userinfo)
                $""", re.VERBOSE),
            "setval": "logging userinfo",
            "result": { 
                "logging": {
                    "userinfo":  "{{ True if userinfo is defined }}"
                }
            },
        },
    ]
    # fmt: on
