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
        {
            "name": "ip_bootp_server",
            "getval": re.compile(
                r"""
                ^ip\sbootp\sserver
                """, re.VERBOSE,
            ),
            "setval": "ip bootp server",
            "compval": "ip.bootp_server",
            "result": {
                "ip": {"bootp_server": True},
            },
        },
        {
            "name": "ip_finger",
            "getval": re.compile(
                r"""
                ^ip\sfinger
                """, re.VERBOSE,
            ),
            "setval": "ip finger",
            "compval": "ip.finger",
            "result": {
                "ip": {"finger": True},
            },
        },
        {
            "name": "ip_source_route",
            "getval": re.compile(
                r"""
                ^ip\ssource-route
                """, re.VERBOSE,
            ),
            "setval": "ip source-route",
            "compval": "ip.source_route",
            "result": {
                "ip": {"source_route": True},
            },
        },
        {
            "name": "ip_scp_server",
            "getval": re.compile(
                r"""
                ^ip\sscp\sserver\senable
                """, re.VERBOSE,
            ),
            "setval": "ip scp server enable",
            "compval": "ip.scp_server",
            "result": {
                "ip": {"scp_server": True},
            },
        },
        {
            "name": "ip_rcmd_rsh_enable",
            "getval": re.compile(
                r"""
                ^ip\srcmd\srsh-enable
                """, re.VERBOSE,
            ),
            "setval": "ip rcmd rsh-enable",
            "compval": "ip.rcmd.rsh_enable",
            "result": {
                "ip": {"rcmd": {"rsh_enable": True}},
            },
        },
        {
            "name": "ip_rcmd_rcp_enable",
            "getval": re.compile(
                r"""
                ^ip\srcmd\srcp-enable
                """, re.VERBOSE,
            ),
            "setval": "ip rcmd rcp-enable",
            "compval": "ip.rcmd.rcp_enable",
            "result": {
                "ip": {"rcmd": {"rcp_enable": True}},
            },
        },
        {
            "name": "ip_tftp_source_interface",
            "getval": re.compile(
                r"""
                ^ip\stftp\ssource-interface\s(?P<source_interface>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip tftp source-interface {{ ip.tftp.source_interface }}",
            "remval": "ip tftp source-interface",
            "compval": "ip.tftp.source_interface",
            "result": {
                "ip": {"tftp": {"source_interface": "{{ source_interface }}"}},
            },
        },
        {
            "name": "ip_ftp_source_interface",
            "getval": re.compile(
                r"""
                ^ip\sftp\ssource-interface\s(?P<source_interface>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ftp source-interface {{ ip.ftp.source_interface }}",
            "remval": "ip ftp source-interface",
            "compval": "ip.ftp.source_interface",
            "result": {
                "ip": {"ftp": {"source_interface": "{{ source_interface }}"}},
            },
        },
        # --- ip.http: the HTTP and HTTPS server and client ---
        {
            "name": "ip_http_server",
            "getval": re.compile(
                r"""
                ^ip\shttp\sserver
                $""", re.VERBOSE,
            ),
            "setval": "ip http server",
            "compval": "ip.http.server",
            "result": {
                "ip": {"http": {"server": True}},
            },
        },
        {
            "name": "ip_http_secure_server",
            "getval": re.compile(
                r"""
                ^ip\shttp\ssecure-server
                $""", re.VERBOSE,
            ),
            "setval": "ip http secure-server",
            "compval": "ip.http.secure_server",
            "result": {
                "ip": {"http": {"secure_server": True}},
            },
        },
        {
            "name": "ip_http_authentication",
            "getval": re.compile(
                r"""
                ^ip\shttp\sauthentication\s(?P<authentication>aaa|enable|local|tacacs)(\s.*)?
                $""", re.VERBOSE,
            ),
            "setval": "ip http authentication {{ ip.http.authentication }}",
            "remval": "ip http authentication",
            "compval": "ip.http.authentication",
            "result": {
                "ip": {"http": {"authentication": "{{ authentication }}"}},
            },
        },
        {
            "name": "ip_http_access_class",
            "getval": re.compile(
                r"""
                ^ip\shttp\saccess-class\sipv4\s(?P<access_class>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http access-class ipv4 {{ ip.http.access_class }}",
            "remval": "ip http access-class ipv4 {{ ip.http.access_class }}",
            "compval": "ip.http.access_class",
            "result": {
                "ip": {"http": {"access_class": "{{ access_class }}"}},
            },
        },
        {
            "name": "ip_http_port",
            "getval": re.compile(
                r"""
                ^ip\shttp\sport\s(?P<port>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http port {{ ip.http.port }}",
            "remval": "ip http port",
            "compval": "ip.http.port",
            "result": {
                "ip": {"http": {"port": "{{ port | int }}"}},
            },
        },
        {
            "name": "ip_http_secure_port",
            "getval": re.compile(
                r"""
                ^ip\shttp\ssecure-port\s(?P<secure_port>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http secure-port {{ ip.http.secure_port }}",
            "remval": "ip http secure-port",
            "compval": "ip.http.secure_port",
            "result": {
                "ip": {"http": {"secure_port": "{{ secure_port | int }}"}},
            },
        },
        {
            "name": "ip_http_max_connections",
            "getval": re.compile(
                r"""
                ^ip\shttp\smax-connections\s(?P<max_connections>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http max-connections {{ ip.http.max_connections }}",
            "remval": "ip http max-connections",
            "compval": "ip.http.max_connections",
            "result": {
                "ip": {"http": {"max_connections": "{{ max_connections | int }}"}},
            },
        },
        {
            "name": "ip_http_secure_trustpoint",
            "getval": re.compile(
                r"""
                ^ip\shttp\ssecure-trustpoint\s(?P<secure_trustpoint>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http secure-trustpoint {{ ip.http.secure_trustpoint }}",
            "remval": "ip http secure-trustpoint {{ ip.http.secure_trustpoint }}",
            "compval": "ip.http.secure_trustpoint",
            "result": {
                "ip": {"http": {"secure_trustpoint": "{{ secure_trustpoint }}"}},
            },
        },
        {
            "name": "ip_http_client_source_interface",
            "getval": re.compile(
                r"""
                ^ip\shttp\sclient\ssource-interface\s(?P<source_interface>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http client source-interface {{ ip.http.client.source_interface }}",
            "remval": "ip http client source-interface",
            "compval": "ip.http.client.source_interface",
            "result": {
                "ip": {"http": {"client": {"source_interface": "{{ source_interface }}"}}},
            },
        },
        {
            "name": "ip_http_client_secure_trustpoint",
            "getval": re.compile(
                r"""
                ^ip\shttp\sclient\ssecure-trustpoint\s(?P<secure_trustpoint>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip http client secure-trustpoint {{ ip.http.client.secure_trustpoint }}",
            "remval": "ip http client secure-trustpoint {{ ip.http.client.secure_trustpoint }}",
            "compval": "ip.http.client.secure_trustpoint",
            "result": {
                "ip": {"http": {"client": {"secure_trustpoint": "{{ secure_trustpoint }}"}}},
            },
        },
        # ---- tftp-server: the files served by the TFTP server ----
        {
            "name": "tftp_server",
            "getval": re.compile(
                r"""
                ^tftp-server\s(?P<file>[^\s:]+:\S+)
                (\salias\s(?P<alias>\S+))?
                (\s(?P<access_list>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "tftp-server {{ file }}"
                      "{{ (' alias ' + alias) if alias is defined else '' }}"
                      "{{ (' ' + access_list|string) if access_list is defined else '' }}",
            "result": {
                "tftp_server": {
                    "files": [
                        {
                            "file": "{{ file }}",
                            "alias": "{{ alias }}",
                            "access_list": "{{ access_list | int if access_list is defined }}",
                        },
                    ],
                },
            },
        },
        {
            # old form of the same line, "tftp-server flash file", read as "flash:file"
            "name": "tftp_server_old_form",
            "getval": re.compile(
                r"""
                ^tftp-server\s(?P<file_system>[^\s:]+)\s(?P<name>\S+)
                (\salias\s(?P<alias>\S+))?
                (\s(?P<access_list>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "tftp_server": {
                    "files": [
                        {
                            "file": "{{ file_system }}:{{ name }}",
                            "alias": "{{ alias }}",
                            "access_list": "{{ access_list | int if access_list is defined }}",
                        },
                    ],
                },
            },
        },
        # ip ssh: curated security relevant options, see the ip.ssh option
        {
            "name": "ip_ssh_version",
            "getval": re.compile(
                r"""
                ^ip\sssh\sversion\s(?P<version>[12])
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh version {{ ip.ssh.version }}",
            "compval": "ip.ssh.version",
            "result": {
                "ip": {"ssh": {"version": "{{ version | int }}"}},
            },
        },
        {
            "name": "ip_ssh_time_out",
            "getval": re.compile(
                r"""
                ^ip\sssh\stime-out\s(?P<time_out>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh time-out {{ ip.ssh.time_out }}",
            "compval": "ip.ssh.time_out",
            "result": {
                "ip": {"ssh": {"time_out": "{{ time_out | int }}"}},
            },
        },
        {
            "name": "ip_ssh_authentication_retries",
            "getval": re.compile(
                r"""
                ^ip\sssh\sauthentication-retries\s(?P<authentication_retries>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh authentication-retries {{ ip.ssh.authentication_retries }}",
            "compval": "ip.ssh.authentication_retries",
            "result": {
                "ip": {"ssh": {"authentication_retries": "{{ authentication_retries | int }}"}},
            },
        },
        {
            "name": "ip_ssh_dh_min_size",
            "getval": re.compile(
                r"""
                ^ip\sssh\sdh\smin\ssize\s(?P<dh_min_size>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh dh min size {{ ip.ssh.dh_min_size }}",
            "compval": "ip.ssh.dh_min_size",
            "result": {
                "ip": {"ssh": {"dh_min_size": "{{ dh_min_size | int }}"}},
            },
        },
        {
            "name": "ip_ssh_bulk_mode",
            "getval": re.compile(
                r"""
                ^ip\sssh\sbulk-mode\s(?P<bulk_mode>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh bulk-mode {{ ip.ssh.bulk_mode }}",
            "compval": "ip.ssh.bulk_mode",
            "result": {
                "ip": {"ssh": {"bulk_mode": "{{ bulk_mode | int }}"}},
            },
        },
        {
            "name": "ip_ssh_logging_events",
            "getval": re.compile(
                r"""
                ^ip\sssh\slogging\sevents
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh logging events",
            "compval": "ip.ssh.logging_events",
            "result": {
                "ip": {"ssh": {"logging_events": True}},
            },
        },
        {
            "name": "ip_ssh_source_interface",
            "getval": re.compile(
                r"""
                ^ip\sssh\ssource-interface\s(?P<source_interface>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh source-interface {{ ip.ssh.source_interface }}",
            "remval": "ip ssh source-interface",
            "compval": "ip.ssh.source_interface",
            "result": {
                "ip": {"ssh": {"source_interface": "{{ source_interface }}"}},
            },
        },
        {
            "name": "ip_ssh_rsa_keypair_name",
            "getval": re.compile(
                r"""
                ^ip\sssh\srsa\skeypair-name\s(?P<rsa_keypair_name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh rsa keypair-name {{ ip.ssh.rsa_keypair_name }}",
            "compval": "ip.ssh.rsa_keypair_name",
            "result": {
                "ip": {"ssh": {"rsa_keypair_name": "{{ rsa_keypair_name }}"}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_mac",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\smac\s(?P<mac>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm mac {{ ip.ssh.server.algorithm.mac | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.mac",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"mac": "{{ mac.split() }}"}}}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_kex",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\skex\s(?P<kex>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm kex {{ ip.ssh.server.algorithm.kex | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.kex",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"kex": "{{ kex.split() }}"}}}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_hostkey",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\shostkey\s(?P<hostkey>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm hostkey {{ ip.ssh.server.algorithm.hostkey | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.hostkey",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"hostkey": "{{ hostkey.split() }}"}}}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_encryption",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\sencryption\s(?P<encryption>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm encryption {{ ip.ssh.server.algorithm.encryption | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.encryption",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"encryption": "{{ encryption.split() }}"}}}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_publickey",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\spublickey\s(?P<publickey>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm publickey {{ ip.ssh.server.algorithm.publickey | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.publickey",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"publickey": "{{ publickey.split() }}"}}}},
            },
        },
        {
            "name": "ip_ssh_server_algorithm_authentication",
            "getval": re.compile(
                r"""
                ^ip\sssh\sserver\salgorithm\sauthentication\s(?P<authentication>.+)
                $""", re.VERBOSE,
            ),
            "setval": "ip ssh server algorithm authentication {{ ip.ssh.server.algorithm.authentication | join(' ') }}",
            "compval": "ip.ssh.server.algorithm.authentication",
            "result": {
                "ip": {"ssh": {"server": {"algorithm": {"authentication": "{{ authentication.split() }}"}}}},
            },
        },
    ]
