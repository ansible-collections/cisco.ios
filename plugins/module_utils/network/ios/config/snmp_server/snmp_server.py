#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_snmp_server config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.snmp_server import (
    Snmp_serverTemplate,
)


class Snmp_server(ResourceModule):
    """
    The ios_snmp_server config class
    """

    def __init__(self, module):
        super(Snmp_server, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="snmp_server",
            tmplt=Snmp_serverTemplate(),
        )
        self.parsers = [
            "accounting",
            "cache",
            "chassis_id",
            "contact",
            "context",
            "drop",
            "file_transfer",
            "if_index",
            "inform",
            "ip",
            "location",
            "manager",
            "packet_size",
            "queue_length",
            "trap_timeout",
            "source_interface",
            "trap_source",
            "system_shutdown",
        ]
        self.list_parsers = [
            "hosts",
            "groups",
            "engine_id",
            "communities",
            "password_policy",
            "users",
            "views",
        ]
        self.complex_parsers = [
            "traps.auth_framework",
            "traps.bfd",
            "traps.bgp",
            "traps.bridge",
            "traps.casa",
            "traps.cnpd",
            "traps.config",
            "traps.config_copy",
            "traps.config_ctid",
            "traps.dhcp",
            "traps.eigrp",
            "traps.entity",
            "traps.event_manager",
            "traps.flowmon",
            "traps.fru_ctrl",
            "traps.hsrp",
            "traps.ipsla",
            "traps.msdp",
            "traps.mvpn",
            "traps.pki",
            "traps.rsvp",
            "traps.syslog",
            "traps.transceiver_all",
            "traps.tty",
            "traps.vrrp",
            "traps.ipmulticast",
            "traps.ike.policy.add",
            "traps.ike.policy.delete",
            "traps.ike.tunnel.start",
            "traps.ike.tunnel.stop",
            "traps.ipsec.cryptomap.add",
            "traps.ipsec.cryptomap.delete",
            "traps.ipsec.cryptomap.attach",
            "traps.ipsec.cryptomap.detach",
            "traps.ipsec.tunnel.start",
            "traps.ipsec.tunnel.stop",
            "traps.ipsec.too_many_sas",
            "traps.ospf.cisco_specific.error",
            "traps.ospf.cisco_specific.retransmit",
            "traps.ospf.cisco_specific.lsa",
            "traps.ospf.cisco_specific.state_change.nssa_trans_change",
            "traps.ospf.cisco_specific.state_change.shamlink.interface",
            "traps.ospf.cisco_specific.state_change.shamlink.neighbor",
            "traps.ospf.error",
            "traps.ospf.retransmit",
            "traps.ospf.lsa",
            "traps.ospf.state_change",
            "traps.l2tun.pseudowire_status",
            "traps.l2tun.session",
            "traps.cpu",
            "traps.firewall",
            "traps.pim",
            "traps.snmp",
            "traps.frame_relay",
            "traps.cef",
            "traps.dlsw",
            "traps.ethernet",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = self._snmp_list_to_dict(self.want)
        haved = self._snmp_list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            # haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        # # remove superfluous config for overridden and deleted
        # if self.state in ["overridden", "deleted"]:
        #     for k, have in iteritems(haved):
        #         if k not in wantd:
        #             self._compare(want={}, have=have)

        # for k, want in iteritems(wantd):
        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Snmp_server network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self.compare(parsers=self.complex_parsers, want=want, have=have)
        self._compare_lists_attrs(want, have)

    def _compare_lists_attrs(self, want, have):
        """Compare list of dict"""
        for _parser in self.list_parsers:
            i_want = want.get(_parser, {})
            i_have = have.get(_parser, {})
            for key, wanting in iteritems(i_want):
                haveing = i_have.pop(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser)
            for key, haveing in iteritems(i_have):
                self.addcmd(haveing, _parser, negate=True)

    def _snmp_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "hosts": "host",
            "groups": "group",
            "engine_id": "id",
            "communities": "name",
            "password_policy": "policy_name",
            "users": "username",
            "views": "name",
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data:
                uq_key = p_key[k]
                if k == "hosts":
                    tmp_data[k] = {
                        str(
                            i[uq_key]
                            + i.get("version", "")
                            + i.get("community_string", "")
                        ): i
                        for i in tmp_data[k]
                    }
                else:
                    tmp_data[k] = {str(i[uq_key]): i for i in tmp_data[k]}
        return tmp_data
