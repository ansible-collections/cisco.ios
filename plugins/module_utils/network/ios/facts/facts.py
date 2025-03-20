#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The facts class for ios
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.acl_interfaces.acl_interfaces import (
    Acl_interfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.acls.acls import AclsFacts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_address_family.bgp_address_family import (
    Bgp_address_familyFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_global.bgp_global import (
    Bgp_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernetFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_evi.evpn_evi import (
    Evpn_eviFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.evpn_global.evpn_global import (
    Evpn_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.hostname.hostname import (
    HostnameFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.interfaces.interfaces import (
    InterfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2_interfaces.l2_interfaces import (
    L2_interfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l3_interfaces.l3_interfaces import (
    L3_InterfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lacp.lacp import LacpFacts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lacp_interfaces.lacp_interfaces import (
    Lacp_InterfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lag_interfaces.lag_interfaces import (
    Lag_interfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.legacy.base import (
    Config,
    Default,
    Hardware,
    Interfaces,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lldp_global.lldp_global import (
    Lldp_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.lldp_interfaces.lldp_interfaces import (
    Lldp_InterfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.logging_global.logging_global import (
    Logging_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ntp_global.ntp_global import (
    Ntp_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv2.ospfv2 import (
    Ospfv2Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv3.ospfv3 import (
    Ospfv3Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.prefix_lists.prefix_lists import (
    Prefix_listsFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.route_maps.route_maps import (
    Route_mapsFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.service.service import (
    ServiceFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.snmp_server.snmp_server import (
    Snmp_serverFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.static_routes.static_routes import (
    Static_routesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans import (
    VlansFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_address_family.vrf_address_family import (
    Vrf_address_familyFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_global.vrf_global import (
    Vrf_globalFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_interfaces.vrf_interfaces import (
    Vrf_interfacesFacts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vxlan_vtep.vxlan_vtep import (
    Vxlan_vtepFacts,
)


FACT_LEGACY_SUBSETS = dict(
    default=Default,
    hardware=Hardware,
    interfaces=Interfaces,
    config=Config,
)

FACT_RESOURCE_SUBSETS = dict(
    interfaces=InterfacesFacts,
    l2_interfaces=L2_interfacesFacts,
    vlans=VlansFacts,
    lag_interfaces=Lag_interfacesFacts,
    lacp=LacpFacts,
    lacp_interfaces=Lacp_InterfacesFacts,
    lldp_global=Lldp_globalFacts,
    lldp_interfaces=Lldp_InterfacesFacts,
    l3_interfaces=L3_InterfacesFacts,
    acl_interfaces=Acl_interfacesFacts,
    static_routes=Static_routesFacts,
    acls=AclsFacts,
    ospfv2=Ospfv2Facts,
    ospfv3=Ospfv3Facts,
    ospf_interfaces=Ospf_interfacesFacts,
    bgp_global=Bgp_globalFacts,
    bgp_address_family=Bgp_address_familyFacts,
    logging_global=Logging_globalFacts,
    route_maps=Route_mapsFacts,
    prefix_lists=Prefix_listsFacts,
    ntp_global=Ntp_globalFacts,
    service=ServiceFacts,
    snmp_server=Snmp_serverFacts,
    hostname=HostnameFacts,
    vxlan_vtep=Vxlan_vtepFacts,
    evpn_global=Evpn_globalFacts,
    evpn_ethernet=Evpn_ethernetFacts,
    evpn_evi=Evpn_eviFacts,
    vrf_address_family=Vrf_address_familyFacts,
    vrf_global=Vrf_globalFacts,
    vrf_interfaces=Vrf_interfacesFacts,
)


class Facts(FactsBase):
    """The fact class for ios"""

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None, resource_facts_type=None, data=None):
        """Collect the facts for ios
        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(
                FACT_RESOURCE_SUBSETS,
                resource_facts_type,
                data,
            )

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS, legacy_facts_type)

        return self.ansible_facts, self._warnings
