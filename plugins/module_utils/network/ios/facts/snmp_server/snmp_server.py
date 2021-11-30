# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import re

__metaclass__ = type

"""
The ios snmp_server fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy
from textwrap import dedent
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.snmp_server import (
    Snmp_serverTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.snmp_server.snmp_server import (
    Snmp_serverArgs,
)


class Snmp_serverFacts(object):
    """ The ios snmp_server facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Snmp_serverArgs.argument_spec

    def get_snmp_data(self, connection):
        return connection.get("show running-config | section ^snmp-server")
        return dedent(
            """\
            snmp-server engineID local AB0C5342FA0A
            snmp-server engineID remote 10.0.0.2 udp-port 23 AB0C5342FAAB
            snmp-server engineID remote 10.0.0.1 udp-port 22 AB0C5342FAAA
            snmp-server user paux fox v1 access 24
            snmp-server user paul familypaul2 v3 access ipv6 ipv6acl
            snmp-server user relaplacing relaplacing v3
            snmp-server group www v3 auth
            snmp-server group grp1 v1 notify me access 2
            snmp-server group newtera v3 priv
            snmp-server group relaplacing v3 noauth
            snmp-server community test view terst1 RO ipv6 te
            snmp-server community wete RO 1322
            snmp-server community weteww RW paul
            snmp-server trap timeout 2
            snmp-server trap-source GigabitEthernet0/0
            snmp-server source-interface informs Loopback999
            snmp-server packetsize 500
            snmp-server queue-length 2
            snmp-server location thi sis a good location
            snmp-server ip dscp 2
            snmp-server contact this is s good contact again
            snmp-server chassis-id this is a unique string
            snmp-server system-shutdown
            snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart
            snmp-server enable traps flowmon
            snmp-server enable traps tty
            snmp-server enable traps eigrp
            snmp-server enable traps casa
            snmp-server enable traps ospf state-change
            snmp-server enable traps ospf errors
            snmp-server enable traps ospf retransmit
            snmp-server enable traps ospf lsa
            snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
            snmp-server enable traps ospf cisco-specific state-change shamlink interface
            snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
            snmp-server enable traps ospf cisco-specific errors
            snmp-server enable traps ospf cisco-specific retransmit
            snmp-server enable traps ospf cisco-specific lsa
            snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config
            snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up
            snmp-server enable traps auth-framework sec-violation
            snmp-server enable traps energywise
            snmp-server enable traps pw vc
            snmp-server enable traps l2tun session
            snmp-server enable traps l2tun pseudowire status
            snmp-server enable traps ether-oam
            snmp-server enable traps mpls rfc ldp
            snmp-server enable traps mpls ldp
            snmp-server enable traps mpls rfc traffic-eng
            snmp-server enable traps mpls traffic-eng
            snmp-server enable traps ethernet evc status create delete
            snmp-server enable traps bridge newroot topologychange
            snmp-server enable traps stpx inconsistency root-inconsistency loop-inconsistency
            snmp-server enable traps vtp
            snmp-server enable traps vlancreate
            snmp-server enable traps vlandelete
            snmp-server enable traps ike policy add
            snmp-server enable traps ike policy delete
            snmp-server enable traps ike tunnel start
            snmp-server enable traps ike tunnel stop
            snmp-server enable traps ipsec cryptomap add
            snmp-server enable traps ipsec cryptomap delete
            snmp-server enable traps ipsec cryptomap attach
            snmp-server enable traps ipsec cryptomap detach
            snmp-server enable traps ipsec tunnel start
            snmp-server enable traps ipsec tunnel stop
            snmp-server enable traps ipsec too-many-sas
            snmp-server enable traps bfd
            snmp-server enable traps bgp
            snmp-server enable traps bgp cbgp2
            snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
            snmp-server enable traps dlsw
            snmp-server enable traps frame-relay
            snmp-server enable traps frame-relay subif
            snmp-server enable traps hsrp
            snmp-server enable traps ipmulticast
            snmp-server enable traps isis
            snmp-server enable traps msdp
            snmp-server enable traps mvpn
            snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message
            snmp-server enable traps rsvp
            snmp-server enable traps ipsla
            snmp-server enable traps slb real virtual csrp
            snmp-server enable traps syslog
            snmp-server enable traps event-manager
            snmp-server enable traps pki
            snmp-server enable traps ethernet cfm alarm
            snmp-server enable traps mpls vpn
            snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down
            snmp-server host 10.0.2.99 informs version 2c check  msdp stun
            snmp-server host 10.0.2.99 check  slb pki
            snmp-server host 10.0.2.99 checktrap  isis hsrp
            snmp-server host 10.0.2.1 version 3 priv newtera  rsrb pim rsvp slb pki
            snmp-server host 10.0.2.1 version 3 noauth relaplacing  slb pki
            snmp-server host 10.0.2.1 version 2c trapsac  tty bgp
            snmp-server host 10.0.1.1 version 3 auth www  tty bgp
            snmp-server context bad
            snmp-server context good
            snmp-server file-transfer access-group testAcl protocol ftp
            snmp-server file-transfer access-group testAcl protocol rcp
            snmp-server cache interval 2
            snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
            snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9
            snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11
            snmp-server accounting commands default
            snmp-server inform pending 2
            """
        )

    def sort_list_dicts(self, objs):
        p_key = {
            "hosts": "host",
            "groups": "group",
            "engine_id": "id",
            "communities": "name",
            "password_policy": "policy_name",
            "users": "username",
            "views": "name",
        }
        for k, _v in p_key.items():
            if k in objs:
                objs[k] = sorted(objs[k], key=lambda _k: str(_k[p_key[k]]))
        return objs

    def host_traps_string_to_list(self, hosts):
        if hosts:
            for element in hosts:
                if element.get("traps", {}):
                    element["traps"] = list(element.get("traps").split())
            return hosts

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Snmp_server network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_snmp_data(connection)

        # parse native config using the Snmp_server template
        snmp_server_parser = Snmp_serverTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = snmp_server_parser.parse()

        if objs:
            self.host_traps_string_to_list(objs.get("hosts"))
            self.sort_list_dicts(objs)

        ansible_facts["ansible_network_resources"].pop("snmp_server", None)

        params = utils.remove_empties(
            snmp_server_parser.validate_config(
                self.argument_spec, {"config": objs}, redact=True
            )
        )

        facts["snmp_server"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
