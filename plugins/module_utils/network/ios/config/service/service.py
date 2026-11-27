#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_service class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
    get_from_dict,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.service import (
    ServiceTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


class Service(ResourceModule):
    """
    The ios_service class
    """

    def __init__(self, module):
        super(Service, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="service",
            tmplt=ServiceTemplate(),
        )
        self.parsers = [
            "call_home",
            "compress_config",
            "config",
            "counters",
            "dhcp",
            "disable_ip_fast_frag",
            "exec_callback",
            "exec_wait",
            "hide_telnet_addresses",
            "internal",
            "linenumber",
            "log",
            "log_hidden",
            "nagle",
            "old_slip_prompts",
            "pad",
            "pad_cmns",
            "pad_from_xot",
            "pad_to_xot",
            "password_encryption",
            "password_recovery",
            "private_config_encryption",
            "prompt",
            "pt_vty_logging",
            "scripting",
            "sequence_numbers",
            "slave_coredump",
            "slave_log",
            "tcp_keepalives_in",
            "tcp_keepalives_out",
            "tcp_small_servers",
            "telnet_zeroidle",
            "udp_small_servers",
            "unsupported_transceiver",
        ]
        self.ip_parsers = [
            "ip_bootp_server",
            "ip_finger",
            "ip_source_route",
            "ip_scp_server",
            "ip_rcmd_rsh_enable",
            "ip_rcmd_rcp_enable",
            "ip_tftp_source_interface",
            "ip_ftp_source_interface",
            # ip.http
            "ip_http_server",
            "ip_http_secure_server",
            "ip_http_access_class",
            "ip_http_secure_trustpoint",
            "ip_http_client_source_interface",
            "ip_http_client_secure_trustpoint",
            "ip_ssh_version",
            "ip_ssh_time_out",
            "ip_ssh_authentication_retries",
            "ip_ssh_dh_min_size",
            "ip_ssh_bulk_mode",
            "ip_ssh_logging_events",
            "ip_ssh_source_interface",
            "ip_ssh_rsa_keypair_name",
            "ip_ssh_server_algorithm_mac",
            "ip_ssh_server_algorithm_kex",
            "ip_ssh_server_algorithm_hostkey",
            "ip_ssh_server_algorithm_encryption",
            "ip_ssh_server_algorithm_publickey",
            "ip_ssh_server_algorithm_authentication",
        ]
        # IOS prints the default of these with "show running-config all", a value that is the
        # default is the same as no value
        self.ip_default_parsers = {
            "ip_http_authentication": ("ip.http.authentication", "enable"),
            "ip_http_port": ("ip.http.port", 80),
            "ip_http_secure_port": ("ip.http.secure_port", 443),
            "ip_http_max_connections": ("ip.http.max_connections", 300),
        }

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state
        """
        wantd = self._service_list_to_dict(self.want)
        haved = self._service_list_to_dict(self.have)

        # the ip section is only managed when the task has it, so that the states of existing
        # playbooks keep leaving the ip services alone
        task_ip = wantd.pop("ip", None)
        have_ip = haved.pop("ip", None) or {}

        # the files of the tftp-server are only managed when the task has them
        task_tftp_server = wantd.pop("tftp_server", None)
        have_tftp_server = (haved.pop("tftp_server", None) or {}).get("files", [])

        service_default = {
            "counters": 0,
            "dhcp": True,
            "prompt": True,
            "slave_log": True,
            "password_recovery": True,
        }

        if "private_config_encryption" in haved:
            service_default["private_config_encryption"] = True

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        elif self.state == "deleted":
            wantd = self._service_list_to_dict(service_default)

        # if state is replaced
        elif self.state in ["replaced", "overridden"]:
            wantd = dict_merge(self._service_list_to_dict(service_default), wantd)

        self._compare(want=wantd, have=haved)
        self._compare_ip(task_ip, have_ip)
        self._compare_tftp_server(task_tftp_server, have_tftp_server)

    def _compare_ip(self, task_ip, have_ip):
        """The ip section: legacy services and the source interfaces of the file transfers."""
        if self.state == "deleted":
            if not task_ip:
                return
            # only what the task names is removed
            want_ip = {}
            have_ip = self._keep_named(have_ip, task_ip)
        elif task_ip is None:
            return
        else:
            want_ip = task_ip
            if self.state == "merged":
                want_ip = dict_merge(have_ip, task_ip)
        self._ssh_scope(task_ip, want_ip, have_ip)
        self._same_source_interfaces(want_ip, have_ip)
        self.compare(parsers=self.ip_parsers, want={"ip": want_ip}, have={"ip": have_ip})
        self._compare_ip_defaults({"ip": want_ip}, {"ip": have_ip})

    def _compare_ip_defaults(self, want, have):
        """The options that have a default: a task without the option, or with the default, is the
        same as the device with the default."""
        for parser, (path, default) in self.ip_default_parsers.items():
            want_value, have_value = get_from_dict(want, path), get_from_dict(have, path)
            if want_value is None:
                if have_value is not None and have_value != default:
                    self.addcmd(have, parser, True)
            elif want_value != (have_value if have_value is not None else default):
                self.addcmd(want, parser, False)

    def _keep_named(self, have, named):
        """The part of have that the task names."""
        kept = {}
        for key, value in have.items():
            if key not in named:
                continue
            if isinstance(value, dict) and isinstance(named[key], dict):
                value = self._keep_named(value, named[key])
            kept[key] = value
        return kept

    @staticmethod
    def _same_source_interfaces(want_ip, have_ip):
        """ "Gi0/0" in the task and "GigabitEthernet0/0" on the device are the same interface,
        the device side takes the spelling of the task."""
        pairs = [(want_ip.get(proto) or {}, have_ip.get(proto) or {}) for proto in ("tftp", "ftp")]
        pairs.append(
            (
                (want_ip.get("http") or {}).get("client") or {},
                (have_ip.get("http") or {}).get("client") or {},
            ),
        )
        for want_part, have_part in pairs:
            want_name = want_part.get("source_interface")
            have_name = have_part.get("source_interface")
            if (
                want_name
                and have_name
                and normalize_interface(want_name) == normalize_interface(have_name)
            ):
                have_part["source_interface"] = want_name

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Service network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_lists_attrs(want, have)

    def _compare_lists_attrs(self, want, have):
        """Compare list of dict"""
        i_want = want.get("timestamps", {})
        i_have = have.get("timestamps", {})
        for key, wanting in i_want.items():
            haveing = i_have.pop(key, {})
            if wanting != haveing:
                self.addcmd(wanting, key + "_timestamps", False)
        for key, haveing in i_have.items():
            self.addcmd(haveing, key + "_timestamps", negate=True)

    def _service_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "timestamps": "msg",
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data:
                tmp_data[k] = {str(i[p_key.get(k)]): i for i in tmp_data[k]}
        return tmp_data

    # ---- tftp-server: the files served by the TFTP server ----
    def _compare_tftp_server(self, task, have_files):
        """tftp-server lines. enable: false removes all of them, files is what is served."""
        if task is None:
            return
        files = task.get("files") or []
        if task.get("enable") is False:
            if files:
                self._module.fail_json(
                    msg="tftp_server: files cannot be set together with enable false.",
                )
            final = []
        elif self.state == "deleted":
            # everything but the files the task names
            final = [
                have
                for have in have_files
                if not any(
                    have["file"] == f["file"]
                    and (not f.get("alias") or f["alias"] == have.get("alias"))
                    for f in files
                )
            ]
        elif not files:
            return
        else:
            want = {self._tftp_server_key(f): f for f in files}
            have = {self._tftp_server_key(f): f for f in have_files}
            if self.state == "merged":
                # what the task leaves out stays as it is on the device
                final = dict(have)
                final.update({key: {**have.get(key, {}), **f} for key, f in want.items()})
            else:
                final = want
            final = list(final.values())
        self._tftp_server_commands(have_files, final)

    @staticmethod
    def _tftp_server_key(entry):
        return (entry["file"], entry.get("alias") or "")

    @staticmethod
    def _tftp_server_by_file(entries):
        by_file = {}
        for entry in entries:
            by_file.setdefault(entry["file"], []).append(entry)
        return by_file

    def _tftp_server_commands(self, have_files, final):
        """Per file: lines are only added when nothing has to go.

        IOS does not remove the line that is named when a file has several (a plain one and one with an alias):
        "no tftp-server F alias A" took the plain line. So when a line has to go, all the lines of the file are
        removed and the ones that stay or change are added again.
        """
        have_by_file = self._tftp_server_by_file(have_files)
        final_by_file = self._tftp_server_by_file(final)
        remove, add = [], []
        for file in list(have_by_file) + [f for f in final_by_file if f not in have_by_file]:
            have_lines = have_by_file.get(file, [])
            final_lines = final_by_file.get(file, [])
            if {self._tftp_server_key(e): e for e in have_lines} == {
                self._tftp_server_key(e): e for e in final_lines
            }:
                continue
            if all(line in final_lines for line in have_lines):
                add += [line for line in final_lines if line not in have_lines]
            else:
                remove += have_lines
                add += final_lines
        for entry in remove:
            self.addcmd(entry, "tftp_server", True)
        for entry in add:
            self.addcmd(entry, "tftp_server", False)

    def _ssh_scope(self, task_ip, want_ip, have_ip):
        """ip.ssh: IOS always prints the options of ssh with "show running-config all", also with
        their default value. An option that the task does not name is therefore left alone, in every
        state, and the lists of algorithms are replaced as a whole (the order matters).
        State deleted resets what has no default: the source interface and the key pair."""
        task_ssh = (task_ip or {}).get("ssh") or {}
        have_ssh = have_ip.get("ssh") or {}
        if self.state == "deleted":
            kept = {
                k: v for k, v in have_ssh.items() if k in ("source_interface", "rsa_keypair_name")
            }
            want_ip.pop("ssh", None)
            if kept:
                have_ip["ssh"] = kept
            else:
                have_ip.pop("ssh", None)
            return
        if not task_ssh:
            want_ip.pop("ssh", None)
            have_ip.pop("ssh", None)
            return
        want_ssh = self._overlay(have_ssh, task_ssh)
        want_name = want_ssh.get("source_interface")
        have_name = have_ssh.get("source_interface")
        if (
            want_name
            and have_name
            and normalize_interface(want_name) == normalize_interface(have_name)
        ):
            have_ssh["source_interface"] = want_name
        want_ip["ssh"] = want_ssh
        have_ip["ssh"] = have_ssh

    def _overlay(self, base, top):
        """top on base, a list or a value of top replaces the one of base."""
        result = deepcopy(base)
        for key, value in top.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = self._overlay(result[key], value)
            elif value is not None:
                result[key] = deepcopy(value)
        return result
