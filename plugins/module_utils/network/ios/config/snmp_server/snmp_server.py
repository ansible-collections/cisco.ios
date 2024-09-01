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

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
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
            "context",
            "password_policy",
            "users",
            "views",
        ]
        self.complex_parsers = [
            "traps.aaa_server",
            "traps.auth_framework",
            "traps.bfd",
            "traps.bgp",
            "traps.bgp.cbgp2",
            "traps.bridge",
            "traps.bulkstat",
            "traps.call_home",
            "traps.casa",
            "traps.cef",
            "traps.cnpd",
            "traps.config",
            "traps.config_copy",
            "traps.config_ctid",
            "traps.cpu",
            "traps.dhcp",
            "traps.dlsw",
            "traps.eigrp",
            "traps.energywise",
            "traps.entity",
            "traps.entity_diag",
            "traps.entity_perf",
            "traps.entity_state",
            "traps.envmon",
            "traps.errdisable",
            "traps.ether_oam",
            "traps.ethernet.cfm.alarm",
            "traps.ethernet.cfm.cc",
            "traps.ethernet.cfm.crosscheck",
            "traps.ethernet.evc",
            "traps.event_manager",
            "traps.flash",
            "traps.flex_links",
            "traps.firewall",
            "traps.flowmon",
            "traps.frame_relay",
            "traps.frame_relay.subif",
            "traps.fru_ctrl",
            "traps.hsrp",
            "traps.ike.policy.add",
            "traps.ike.policy.delete",
            "traps.ike.tunnel.start",
            "traps.ike.tunnel.stop",
            "traps.ipmulticast",
            "traps.ipsec.cryptomap.add",
            "traps.ipsec.cryptomap.attach",
            "traps.ipsec.cryptomap.delete",
            "traps.ipsec.cryptomap.detach",
            "traps.ipsec.too_many_sas",
            "traps.ipsec.tunnel.start",
            "traps.ipsec.tunnel.stop",
            "traps.ipsla",
            "traps.isis",
            "traps.l2tc",
            "traps.l2tun.pseudowire_status",
            "traps.l2tun.session",
            "traps.lisp",
            "traps.license",
            "traps.local_auth",
            "traps.mac_notification",
            "traps.memory",
            "traps.mpls.fast_reroute",
            "traps.mpls.ldp",
            "traps.mpls.rfc.ldp",
            "traps.mpls.rfc.traffic_eng",
            "traps.mpls.rfc.vpn",
            "traps.mpls.traffic_eng",
            "traps.mpls.vpn",
            "traps.msdp",
            "traps.mvpn",
            "traps.nhrp.nhc",
            "traps.nhrp.nhp",
            "traps.nhrp.nhs",
            "traps.nhrp.quota_exceeded",
            "traps.ospf.cisco_specific.error",
            "traps.ospf.cisco_specific.lsa",
            "traps.ospf.cisco_specific.retransmit",
            "traps.ospf.cisco_specific.state_change.nssa_trans_change",
            "traps.ospf.cisco_specific.state_change.shamlink.interface",
            "traps.ospf.cisco_specific.state_change.shamlink.neighbor",
            "traps.ospf.error",
            "traps.ospf.lsa",
            "traps.ospf.retransmit",
            "traps.ospf.state_change",
            "traps.ospfv3.errors",
            "traps.ospfv3.rate_limit",
            "traps.ospfv3.state_change",
            "traps.pim",
            "traps.pki",
            "traps.port_security",
            "traps.power_ethernet",
            "traps.pw_vc",
            "traps.rep",
            "traps.rsvp",
            "traps.rf",
            "traps.smart_license",
            "traps.snmp",
            "traps.stackwise",
            "traps.stpx",
            "traps.syslog",
            "traps.transceiver_all",
            "traps.trustsec",
            "traps.trustsec_interface",
            "traps.trustsec_policy",
            "traps.trustsec_server",
            "traps.trustsec_sxp",
            "traps.tty",
            "traps.udld",
            "traps.vlan_membership",
            "traps.vlancreate",
            "traps.vlandelete",
            "traps.vrfmib",
            "traps.vrrp",
            "traps.vswitch",
            "traps.vtp",
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
        want, have and desired state.
        """
        wantd = self._snmp_list_to_dict(self.want)
        haved = self._snmp_list_to_dict(self.have)

        wantd = self._handle_deprecates(want=wantd)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            wantd = {}

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
        """Compare list of dicts"""
        for _parser in self.list_parsers:
            i_want = want.get(_parser, {})
            i_have = have.get(_parser, {})
            have_keys = set(i_have.keys())
            for key, wanting in i_want.items():
                haveing = i_have.get(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        if not (
                            _parser == "users"
                            and wanting.get("username") == haveing.get("username")
                        ):
                            self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser)
                have_keys.discard(key)
            for key in have_keys:
                self.addcmd(i_have[key], _parser, negate=True)

    def _snmp_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "hosts": "host",
            "groups": "group",
            "engine_id": "id",
            "communities": "name",
            "context": True,
            "password_policy": "policy_name",
            "file_transfer": True,
            "users": "username",
            "views": "name",
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data:
                if k == "hosts":
                    tmp_host = dict()
                    for i in tmp_data[k]:
                        tmp = dict()
                        if i.get("traps"):
                            for t in i.get("traps"):
                                tmp.update({t: t})
                            i["traps"] = tmp
                        tmp_host.update(
                            {
                                str(
                                    i[p_key.get(k)]
                                    + i.get("version", "")
                                    + i.get("community_string", ""),
                                ): i,
                            },
                        )
                    tmp_data[k] = tmp_host
                elif k == "context":
                    tmp_data[k] = {i: {"context": i} for i in tmp_data[k]}
                elif k == "file_transfer":
                    if tmp_data.get(k):
                        if tmp_data[k].get("protocol"):
                            tmp = dict()
                            for t in tmp_data[k].get("protocol"):
                                tmp.update({t: t})
                            tmp_data[k]["protocol"] = tmp
                elif k == "groups":
                    tmp_data[k] = {
                        str(i[p_key.get(k)] + i.get("version_option", "") + i.get("context", "")): i
                        for i in tmp_data[k]
                    }
                elif k == "views":
                    tmp_data[k] = {
                        str(i[p_key.get(k)] + i.get("family_name", "")): i for i in tmp_data[k]
                    }
                else:
                    tmp_data[k] = {str(i[p_key.get(k)]): i for i in tmp_data[k]}
        return tmp_data

    def _handle_deprecates(self, want):
        """Remove deprecated attributes and set the replacment"""

        # Take in count the traps config mpls_vpn which is DEPRECATED and replaced by mpls.vpn
        if "traps" in want:
            if "mpls_vpn" in want["traps"]:
                want["traps"] = dict_merge(
                    want["traps"],
                    {"mpls": {"vpn": {"enable": want["traps"]["mpls_vpn"]}}},
                )
                want["traps"].pop("mpls_vpn")
            if "envmon" in want["traps"] and "fan" in want["traps"]["envmon"]:
                want["traps"]["envmon"]["fan_enable"] = want["traps"]["envmon"]["fan"].get(
                    "enable",
                    False,
                )
                want["traps"]["envmon"].pop("fan")

        return want
