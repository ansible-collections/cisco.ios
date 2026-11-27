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
        ]

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
        self._same_source_interfaces(want_ip, have_ip)
        self.compare(parsers=self.ip_parsers, want={"ip": want_ip}, have={"ip": have_ip})

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
        for proto in ("tftp", "ftp"):
            want_name = (want_ip.get(proto) or {}).get("source_interface")
            have_name = (have_ip.get(proto) or {}).get("source_interface")
            if (
                want_name
                and have_name
                and normalize_interface(want_name) == normalize_interface(have_name)
            ):
                have_ip[proto]["source_interface"] = want_name

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
