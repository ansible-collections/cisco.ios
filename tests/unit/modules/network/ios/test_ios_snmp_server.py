#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_snmp_server
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosSnmpServerModule(TestIosModule):
    module = ios_snmp_server

    def setUp(self):
        super(TestIosSnmpServerModule, self).setUp()
        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.snmp_server.snmp_server."
            "Snmp_serverFacts.get_snmp_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.mock_execute_show_command_user = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.snmp_server.snmp_server."
            "Snmp_serverFacts.get_snmpv3_user_data",
        )

        self.execute_show_command_user = self.mock_execute_show_command_user.start()

    def tearDown(self):
        super(TestIosSnmpServerModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()
        self.mock_execute_show_command_user.stop()

    def test_ios_snmp_server_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server engineID local AB0C5342FA0A
            snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
            snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA
            snmp-server user newuser newfamily v1 access 24
            snmp-server user paul familypaul v3 access ipv6 ipv6acl ipv4acl
            snmp-server user replaceUser replaceUser v3
            snmp-server group group0 v3 auth
            snmp-server group group1 v1 notify me access ipv6 ipv6acl 2
            snmp-server group group2 v3 priv
            snmp-server group group3 v1 access ipv6 ipv6acl
            snmp-server group group4 v1 access 2
            snmp-server group replaceUser v3 noauth
            snmp-server community commu1 view view1 RO ipv6 te
            snmp-server community commu2 RO 1322
            snmp-server community commu3 RW paul
            snmp-server trap timeout 2
            snmp-server trap-source GigabitEthernet0/0
            snmp-server source-interface informs Loopback999
            snmp-server packetsize 500
            snmp-server queue-length 2
            snmp-server location thi sis a good location
            snmp-server ip dscp 2
            snmp-server contact this is contact string
            snmp-server chassis-id this is a chassis id string
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
            snmp-server enable traps ethernet evc status create delete
            snmp-server enable traps bridge newroot topologychange
            snmp-server enable traps vtp
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
            snmp-server host 172.16.2.99 informs version 2c check  msdp
            snmp-server host 172.16.2.99 check  slb
            snmp-server host 172.16.2.99 checktrap  isis
            snmp-server host 172.16.2.1 version 3 priv newtera  rsrb
            snmp-server host 172.16.2.1 version 3 noauth replaceUser  slb
            snmp-server host 172.16.2.1 version 2c trapsac  tty
            snmp-server host 172.16.1.1 version 3 auth group0  tty
            snmp-server context contextWord1
            snmp-server context contextWord2
            snmp-server file-transfer access-group testAcl protocol ftp
            snmp-server file-transfer access-group testAcl protocol rcp
            snmp-server cache interval 2
            snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
            snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9
            snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11
            snmp-server accounting commands default
            snmp-server inform pending 2
            """,
        )

        playbook = {
            "config": {
                "accounting": {"command": "default"},
                "cache": 2,
                "chassis_id": "this is a chassis id string",
                "communities": [
                    {"acl_v6": "te", "name": "commu1", "ro": True, "view": "view1"},
                    {"acl_v4": "1322", "name": "commu2", "ro": True},
                    {"acl_v4": "paul", "name": "commu3", "rw": True},
                ],
                "contact": "this is contact string",
                "context": ["contextWord2", "contextWord1"],
                "engine_id": [
                    {"id": "AB0C5342FA0A", "local": True},
                    {
                        "id": "AB0C5342FAAA",
                        "remote": {"host": "172.16.0.1", "udp_port": 22},
                    },
                    {
                        "id": "AB0C5342FAAB",
                        "remote": {"host": "172.16.0.2", "udp_port": 23},
                    },
                ],
                "file_transfer": {
                    "access_group": "testAcl",
                    "protocol": ["ftp", "rcp"],
                },
                "groups": [
                    {"group": "group0", "version": "v3", "version_option": "auth"},
                    {
                        "acl_v4": "2",
                        "acl_v6": "ipv6acl",
                        "group": "group1",
                        "notify": "me",
                        "version": "v1",
                    },
                    {"group": "group2", "version": "v3", "version_option": "priv"},
                    {
                        "group": "replaceUser",
                        "version": "v3",
                        "version_option": "noauth",
                    },
                    {"acl_v6": "ipv6acl", "group": "group3", "version": "v1"},
                    {"acl_v4": "2", "group": "group4", "version": "v1"},
                ],
                "hosts": [
                    {
                        "community_string": "group0",
                        "host": "172.16.1.1",
                        "traps": ["tty"],
                        "version": "3",
                        "version_option": "auth",
                    },
                    {
                        "community_string": "newtera",
                        "host": "172.16.2.1",
                        "traps": ["rsrb"],
                        "version": "3",
                        "version_option": "priv",
                    },
                    {
                        "community_string": "replaceUser",
                        "host": "172.16.2.1",
                        "traps": ["slb"],
                        "version": "3",
                        "version_option": "noauth",
                    },
                    {
                        "community_string": "trapsac",
                        "host": "172.16.2.1",
                        "traps": ["tty"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "informs": True,
                        "traps": ["msdp"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "traps": ["slb"],
                    },
                    {
                        "community_string": "checktrap",
                        "host": "172.16.2.99",
                        "traps": ["isis"],
                    },
                ],
                "inform": {"pending": 2},
                "ip": {"dscp": 2},
                "location": "thi sis a good location",
                "packet_size": 500,
                "password_policy": [
                    {
                        "change": 3,
                        "digits": 23,
                        "lower_case": 12,
                        "max_len": 24,
                        "policy_name": "policy1",
                        "special_char": 32,
                        "upper_case": 12,
                    },
                    {
                        "change": 9,
                        "min_len": 12,
                        "policy_name": "policy2",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                    {
                        "change": 11,
                        "digits": 23,
                        "max_len": 12,
                        "min_len": 12,
                        "policy_name": "policy3",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                ],
                "queue_length": 2,
                "source_interface": "Loopback999",
                "system_shutdown": True,
                "trap_source": "GigabitEthernet0/0",
                "trap_timeout": 2,
                "traps": {
                    "auth_framework": {"enable": True},
                    "bfd": {"enable": True},
                    "bgp": {"cbgp2": True, "enable": True},
                    "bridge": {"enable": True, "newroot": True, "topologychange": True},
                    "casa": True,
                    "cef": {
                        "enable": True,
                        "inconsistency": True,
                        "peer_fib_state_change": True,
                        "peer_state_change": True,
                        "resource_failure": True,
                    },
                    "dlsw": {"enable": True},
                    "eigrp": True,
                    "energywise": True,
                    "ethernet": {
                        "cfm": {
                            "alarm": True,
                            "cc": {
                                "config": True,
                                "cross_connect": True,
                                "loop": True,
                                "mep_down": True,
                                "mep_up": True,
                            },
                            "crosscheck": {
                                "mep_missing": True,
                                "mep_unknown": True,
                                "service_up": True,
                            },
                        },
                        "evc": {"create": True, "delete": True, "status": True},
                    },
                    "event_manager": True,
                    "flowmon": True,
                    "frame_relay": {"enable": True},
                    "hsrp": True,
                    "ike": {
                        "policy": {"add": True, "delete": True},
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipmulticast": True,
                    "ipsec": {
                        "cryptomap": {
                            "add": True,
                            "attach": True,
                            "delete": True,
                            "detach": True,
                        },
                        "too_many_sas": True,
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipsla": True,
                    "isis": True,
                    "l2tun": {"pseudowire_status": True, "session": True},
                    "mpls": {
                        "vpn": {"enable": True},
                    },
                    "msdp": True,
                    "mvpn": True,
                    "ospf": {
                        "cisco_specific": {
                            "error": True,
                            "lsa": True,
                            "retransmit": True,
                            "state_change": {
                                "nssa_trans_change": True,
                                "shamlink": {"interface": True, "neighbor": True},
                            },
                        },
                        "error": True,
                        "lsa": True,
                        "retransmit": True,
                        "state_change": True,
                    },
                    "pim": {
                        "enable": True,
                        "invalid_pim_message": True,
                        "neighbor_change": True,
                        "rp_mapping_change": True,
                    },
                    "pki": True,
                    "pw_vc": True,
                    "rsvp": True,
                    "snmp": {
                        "authentication": True,
                        "coldstart": True,
                        "linkdown": True,
                        "linkup": True,
                        "warmstart": True,
                    },
                    "syslog": True,
                    "tty": True,
                    "vrfmib": {
                        "vnet_trunk_down": True,
                        "vnet_trunk_up": True,
                        "vrf_down": True,
                        "vrf_up": True,
                    },
                },
                "users": [
                    {
                        "acl_v4": "24",
                        "group": "newfamily",
                        "username": "newuser",
                        "version": "v1",
                    },
                    {
                        "acl_v4": "ipv4acl",
                        "acl_v6": "ipv6acl",
                        "group": "familypaul",
                        "username": "paul",
                        "version": "v3",
                    },
                    {
                        "group": "replaceUser",
                        "username": "replaceUser",
                        "version": "v3",
                    },
                ],
            },
        }
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_snmp_server_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server engineID local AB0C5342FA0A
            snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
            snmp-server enable traps casa
            snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
            snmp-server enable traps ospf cisco-specific state-change shamlink interface
            snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
            snmp-server enable traps ospf cisco-specific errors
            snmp-server enable traps ospf cisco-specific retransmit
            snmp-server enable traps ospf cisco-specific lsa
            snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config
            snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up
            snmp-server enable traps auth-framework sec-violation
            snmp-server enable traps ethernet cfm alarm
            snmp-server enable traps mpls vpn
            snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down
            snmp-server host 172.16.2.99 informs version 2c check  msdp
            snmp-server host 172.16.2.1 version 3 priv newtera  rsrb
            snmp-server host 172.16.2.1 version 3 noauth replaceUser  slb
            snmp-server context contextWord1
            snmp-server cache interval 2
            snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
            snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9
            snmp-server inform pending 2
            """,
        )

        self.execute_show_command_user.return_value = dedent(
            """\
            User name: paul
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list ipv6: ipv6only
            Authentication Protocol: MD5
            Privacy Protocol: AES128
            Group-name: familypaul

            User name: replaceUser
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-snmp-server user paul familypaul v3 access ipv6name: replaceUser
            """,
        )

        playbook = {
            "config": {
                "accounting": {"command": "default"},
                "cache": 2,
                "chassis_id": "this is a chassis id string",
                "communities": [
                    {"acl_v6": "te", "name": "commu1", "ro": True, "view": "view1"},
                    {"acl_v4": "1322", "name": "commu2", "ro": True},
                    {"acl_v4": "paul", "name": "commu3", "rw": True},
                ],
                "contact": "this is contact string",
                "context": ["contextWord2", "contextWord1"],
                "engine_id": [
                    {"id": "AB0C5342FA0A", "local": True},
                    {
                        "id": "AB0C5342FAAA",
                        "remote": {"host": "172.16.0.1", "udp_port": 22, "vrf": "mgmt"},
                    },
                    {
                        "id": "AB0C5342FAAB",
                        "remote": {"host": "172.16.0.2", "udp_port": 23},
                    },
                ],
                "file_transfer": {
                    "access_group": "testAcl",
                    "protocol": ["ftp", "rcp"],
                },
                "groups": [
                    {"group": "group0", "version": "v3", "version_option": "auth"},
                    {
                        "acl_v4": "2",
                        "acl_v6": "ipv6acl",
                        "group": "group1",
                        "notify": "me",
                        "version": "v1",
                    },
                    {"group": "group2", "version": "v3", "version_option": "priv"},
                    {
                        "group": "replaceUser",
                        "version": "v3",
                        "version_option": "noauth",
                    },
                    {"acl_v6": "ipv6acl", "group": "group3", "version": "v1"},
                    {"acl_v4": "2", "group": "group4", "version": "v1"},
                ],
                "hosts": [
                    {
                        "community_string": "group0",
                        "host": "172.16.1.1",
                        "traps": ["tty"],
                        "version": "3",
                        "version_option": "auth",
                    },
                    {
                        "community_string": "newtera",
                        "host": "172.16.2.1",
                        "traps": ["rsrb"],
                        "version": "3",
                        "version_option": "priv",
                    },
                    {
                        "community_string": "replaceUser",
                        "host": "172.16.2.1",
                        "traps": ["slb"],
                        "version": "3",
                        "version_option": "noauth",
                    },
                    {
                        "community_string": "trapsac",
                        "host": "172.16.2.1",
                        "traps": ["tty"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "informs": True,
                        "traps": ["msdp"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "traps": ["slb"],
                    },
                    {
                        "community_string": "checktrap",
                        "host": "172.16.2.99",
                        "traps": ["isis"],
                    },
                ],
                "inform": {"pending": 2},
                "ip": {"dscp": 2},
                "location": "thi sis a good location",
                "packet_size": 500,
                "password_policy": [
                    {
                        "change": 3,
                        "digits": 23,
                        "lower_case": 12,
                        "max_len": 24,
                        "policy_name": "policy1",
                        "special_char": 32,
                        "upper_case": 12,
                    },
                    {
                        "change": 9,
                        "min_len": 12,
                        "policy_name": "policy2",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                    {
                        "change": 11,
                        "digits": 23,
                        "max_len": 12,
                        "min_len": 12,
                        "policy_name": "policy3",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                ],
                "queue_length": 2,
                "source_interface": "Loopback999",
                "system_shutdown": True,
                "trap_source": "GigabitEthernet0/0",
                "trap_timeout": 2,
                "traps": {
                    "auth_framework": {"enable": True},
                    "bfd": {"enable": True},
                    "bgp": {
                        "cbgp2": True,
                        "enable": True,
                        "threshold": {"prefix": True},
                        "state_changes": {
                            "enable": True,
                            "all": True,
                            "limited": True,
                            "backward_trans": True,
                        },
                    },
                    "bridge": {"enable": True, "newroot": True, "topologychange": True},
                    "casa": True,
                    "cef": {
                        "enable": True,
                        "inconsistency": True,
                        "peer_fib_state_change": True,
                        "peer_state_change": True,
                        "resource_failure": True,
                    },
                    "dlsw": {"enable": True},
                    "eigrp": True,
                    "energywise": True,
                    "ethernet": {
                        "cfm": {
                            "alarm": True,
                            "cc": {
                                "config": True,
                                "cross_connect": True,
                                "loop": True,
                                "mep_down": True,
                                "mep_up": True,
                            },
                            "crosscheck": {
                                "mep_missing": True,
                                "mep_unknown": True,
                                "service_up": True,
                            },
                        },
                        "evc": {"create": True, "delete": True, "status": True},
                    },
                    "event_manager": True,
                    "flowmon": True,
                    "frame_relay": {"enable": True},
                    "hsrp": True,
                    "ike": {
                        "policy": {"add": True, "delete": True},
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipmulticast": True,
                    "ipsec": {
                        "cryptomap": {
                            "add": True,
                            "attach": True,
                            "delete": True,
                            "detach": True,
                        },
                        "too_many_sas": True,
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipsla": True,
                    "isis": True,
                    "l2tun": {"pseudowire_status": True, "session": True},
                    "mpls": {
                        "vpn": {"enable": True},
                    },
                    "msdp": True,
                    "mvpn": True,
                    "ospf": {
                        "cisco_specific": {
                            "error": True,
                            "lsa": True,
                            "retransmit": True,
                            "state_change": {
                                "nssa_trans_change": True,
                                "shamlink": {"interface": True, "neighbor": True},
                            },
                        },
                        "error": True,
                        "lsa": True,
                        "retransmit": True,
                        "state_change": True,
                    },
                    "pim": {
                        "enable": True,
                        "invalid_pim_message": True,
                        "neighbor_change": True,
                        "rp_mapping_change": True,
                    },
                    "pki": True,
                    "pw_vc": True,
                    "rsvp": True,
                    "snmp": {
                        "authentication": True,
                        "coldstart": True,
                        "linkdown": True,
                        "linkup": True,
                        "warmstart": True,
                    },
                    "syslog": True,
                    "tty": True,
                    "vrfmib": {
                        "vnet_trunk_down": True,
                        "vnet_trunk_up": True,
                        "vrf_down": True,
                        "vrf_up": True,
                    },
                },
                "users": [
                    {
                        "acl_v4": "24",
                        "group": "newfamily",
                        "username": "newuser",
                        "version": "v1",
                    },
                    {
                        "acl_v6": "ipv6only",
                        "group": "familypaul",
                        "username": "paul",
                        "version": "v3",
                    },
                    {
                        "group": "replaceUser",
                        "username": "replaceUser",
                        "version": "v3",
                    },
                    {
                        "acl_v4": "27",
                        "group": "mfamily",
                        "username": "flow",
                        "version": "v3",
                    },
                ],
            },
        }
        merged = [
            "snmp-server accounting commands default",
            "snmp-server chassis-id this is a chassis id string",
            "snmp-server contact this is contact string",
            "snmp-server file-transfer access-group testAcl protocol ftp rcp",
            "snmp-server ip dscp 2",
            "snmp-server location thi sis a good location",
            "snmp-server packetsize 500",
            "snmp-server queue-length 2",
            "snmp-server trap timeout 2",
            "snmp-server source-interface informs Loopback999",
            "snmp-server trap-source GigabitEthernet0/0",
            "snmp-server system-shutdown",
            "snmp-server enable traps bfd",
            "snmp-server enable traps bgp cbgp2",
            "snmp-server enable traps bgp state-changes all backward-trans limited threshold prefix",
            "snmp-server enable traps bridge newroot topologychange",
            "snmp-server enable traps eigrp",
            "snmp-server enable traps energywise",
            "snmp-server enable traps event-manager",
            "snmp-server enable traps flowmon",
            "snmp-server enable traps hsrp",
            "snmp-server enable traps ipsla",
            "snmp-server enable traps isis",
            "snmp-server enable traps msdp",
            "snmp-server enable traps mvpn",
            "snmp-server enable traps pki",
            "snmp-server enable traps pw vc",
            "snmp-server enable traps rsvp",
            "snmp-server enable traps syslog",
            "snmp-server enable traps tty",
            "snmp-server enable traps ipmulticast",
            "snmp-server enable traps ike policy add",
            "snmp-server enable traps ike policy delete",
            "snmp-server enable traps ike tunnel start",
            "snmp-server enable traps ike tunnel stop",
            "snmp-server enable traps ipsec cryptomap add",
            "snmp-server enable traps ipsec cryptomap delete",
            "snmp-server enable traps ipsec cryptomap attach",
            "snmp-server enable traps ipsec cryptomap detach",
            "snmp-server enable traps ipsec tunnel start",
            "snmp-server enable traps ipsec tunnel stop",
            "snmp-server enable traps ipsec too-many-sas",
            "snmp-server enable traps ospf errors",
            "snmp-server enable traps ospf retransmit",
            "snmp-server enable traps ospf lsa",
            "snmp-server enable traps ospf state-change",
            "snmp-server enable traps l2tun pseudowire status",
            "snmp-server enable traps l2tun session",
            "snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message",
            "snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart",
            "snmp-server enable traps frame-relay",
            "snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
            "snmp-server enable traps dlsw",
            "snmp-server enable traps ethernet evc status create delete",
            "snmp-server host 172.16.2.1 version 2c trapsac tty",
            "snmp-server host 172.16.1.1 version 3 auth group0 tty",
            "snmp-server host 172.16.2.99 check slb",
            "snmp-server host 172.16.2.99 checktrap isis",
            "snmp-server group group0 v3 auth",
            "snmp-server group group1 v1 notify me access ipv6 ipv6acl 2",
            "snmp-server group group2 v3 priv",
            "snmp-server group group3 v1 access ipv6 ipv6acl",
            "snmp-server group group4 v1 access 2",
            "snmp-server group replaceUser v3 noauth",
            "snmp-server engineID remote 172.16.0.1 udp-port 22 vrf mgmt AB0C5342FAAA",
            "snmp-server community commu1 view view1 ro ipv6 te",
            "snmp-server community commu2 ro 1322",
            "snmp-server community commu3 rw paul",
            "snmp-server context contextWord2",
            "snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
            "snmp-server user newuser newfamily v1 access 24",
            "snmp-server user paul familypaul v3 access ipv6 ipv6only",
            "snmp-server user replaceUser replaceUser v3 access 22",
            "snmp-server user flow mfamily v3 access 27",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_snmp_server_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server engineID local AB0C5342FA0A
            snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
            snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA
            snmp-server user new@user! new.family$ v1 access 24
            snmp-server user paul familypaul v3 access ipv6 ipv6acl
            snmp-server user replaceUser replaceUser v3
            snmp-server user flow mfamily v3 access 27
            snmp-server group group0 v3 auth
            snmp-server group group1 v1 notify me access ipv6 ipv6acl 2
            snmp-server group group2 v3 priv
            snmp-server group group3 v1 access ipv6 ipv6acl
            snmp-server group group4 v1 access 2
            snmp-server group replaceUser v3 noauth
            snmp-server community commu1 view view1 RO ipv6 te
            snmp-server community commu2 RO 1322
            snmp-server community commu3 RW paul
            snmp-server trap timeout 2
            snmp-server trap-source GigabitEthernet0/0
            snmp-server source-interface informs Loopback999
            snmp-server packetsize 500
            snmp-server queue-length 2
            snmp-server location thi sis a good location
            snmp-server ip dscp 2
            snmp-server contact this is contact string
            snmp-server chassis-id this is a chassis id string
            snmp-server system-shutdown
            snmp-server enable traps aaa_server
            snmp-server enable traps auth-framework sec-violation
            snmp-server enable traps bfd
            snmp-server enable traps bgp
            snmp-server enable traps bgp cbgp2
            snmp-server enable traps bridge newroot topologychange
            snmp-server enable traps bulkstat collection transfer
            snmp-server enable traps call-home message-send-fail server-fail
            snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency
            snmp-server enable traps config
            snmp-server enable traps config-copy
            snmp-server enable traps config-ctid
            snmp-server enable traps cpu threshold
            snmp-server enable traps dhcp
            snmp-server enable traps eigrp
            snmp-server enable traps energywise
            snmp-server enable traps entity
            snmp-server enable traps entity-diag boot-up-fail hm-test-recover hm-thresh-reached scheduled-test-fail
            snmp-server enable traps entity-perf throughput-notif
            snmp-server enable traps entity-state
            snmp-server enable traps envmon fan shutdown supply temperature status
            snmp-server enable traps errdisable
            snmp-server enable traps ether-oam
            snmp-server enable traps ethernet cfm alarm
            snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config
            snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up
            snmp-server enable traps ethernet evc status create delete
            snmp-server enable traps event-manager
            snmp-server enable traps flash insertion removal lowspace
            snmp-server enable traps flex-links status
            snmp-server enable traps flowmon
            snmp-server enable traps fru-ctrl
            snmp-server enable traps hsrp
            snmp-server enable traps ike policy add
            snmp-server enable traps ike policy delete
            snmp-server enable traps ike tunnel start
            snmp-server enable traps ike tunnel stop
            snmp-server enable traps ipmulticast
            snmp-server enable traps ipsec cryptomap add
            snmp-server enable traps ipsec cryptomap attach
            snmp-server enable traps ipsec cryptomap delete
            snmp-server enable traps ipsec cryptomap detach
            snmp-server enable traps ipsec too-many-sas
            snmp-server enable traps ipsec tunnel start
            snmp-server enable traps ipsec tunnel stop
            snmp-server enable traps ipsla
            snmp-server enable traps isis
            snmp-server enable traps license
            snmp-server enable traps l2tc threshold sys-threshold
            snmp-server enable traps lisp
            snmp-server enable traps local-auth
            snmp-server enable traps mac-notification change move threshold
            snmp-server enable traps memory bufferpeak
            snmp-server enable traps mpls fast-reroute protected
            snmp-server enable traps mpls rfc ldp
            snmp-server enable traps mpls rfc traffic-eng
            snmp-server enable traps mpls rfc vpn
            snmp-server enable traps mpls traffic-eng
            snmp-server enable traps mpls vpn
            snmp-server enable traps msdp
            snmp-server enable traps mvpn
            snmp-server enable traps nhrp nhc
            snmp-server enable traps nhrp nhp
            snmp-server enable traps nhrp nhs
            snmp-server enable traps nhrp quota-exceeded
            snmp-server enable traps ospf cisco-specific errors
            snmp-server enable traps ospf cisco-specific lsa
            snmp-server enable traps ospf cisco-specific retransmit
            snmp-server enable traps ospf cisco-specific state-change nssa-trans-change
            snmp-server enable traps ospf cisco-specific state-change shamlink interface
            snmp-server enable traps ospf cisco-specific state-change shamlink neighbor
            snmp-server enable traps ospf errors
            snmp-server enable traps ospf lsa
            snmp-server enable traps ospf retransmit
            snmp-server enable traps ospf state-change
            snmp-server enable traps ospfv3 errors
            snmp-server enable traps ospfv3 state-change
            snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message
            snmp-server enable traps pki
            snmp-server enable traps port-security
            snmp-server enable traps power-ethernet police
            snmp-server enable traps pw vc
            snmp-server enable traps rep
            snmp-server enable traps rf
            snmp-server enable traps smart-license
            snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart
            snmp-server enable traps stackwise
            snmp-server enable traps stpx inconsistency root-inconsistency loop-inconsistency
            snmp-server enable traps syslog
            snmp-server enable traps transceiver all
            snmp-server enable traps trustsec authz-file-error cache-file-error keystore-file-error keystore-sync-fail random-number-fail src-entropy-fail
            snmp-server enable traps trustsec-interface unauthorized sap-fail authc-fail supplicant-fail authz-fail
            snmp-server enable traps trustsec-policy peer-policy-updated authz-sgacl-fail
            snmp-server enable traps trustsec-server radius-server provision-secret
            snmp-server enable traps trustsec-sxp conn-srcaddr-err msg-parse-err conn-config-err binding-err conn-up conn-down binding-expn-fail
            snmp-server enable traps tty
            snmp-server enable traps udld link-fail-rpt status-change
            snmp-server enable traps vlan-membership
            snmp-server enable traps vlancreate
            snmp-server enable traps vlandelete
            snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down
            snmp-server enable traps vswitch dual-active vsl
            snmp-server enable traps vtp
            snmp-server host 172.16.2.99 informs version 2c check  msdp
            snmp-server host 172.16.2.99 check  slb
            snmp-server host 172.16.2.99 checktrap  isis
            snmp-server host 172.16.2.1 version 3 priv newtera  rsrb
            snmp-server host 172.16.2.1 version 3 noauth replaceUser  slb
            snmp-server host 172.16.2.1 version 2c trapsac  tty
            snmp-server host 172.16.1.1 version 3 auth group0  tty
            snmp-server context contextWord1
            snmp-server context contextWord2
            snmp-server cache interval 2
            snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3
            snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9
            snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11
            snmp-server accounting commands default
            snmp-server inform pending 2
            """,
        )
        playbook = {"config": {}}
        deleted = [
            "no snmp-server accounting commands default",
            "no snmp-server cache interval 2",
            "no snmp-server chassis-id this is a chassis id string",
            "no snmp-server contact this is contact string",
            "no snmp-server inform pending 2",
            "no snmp-server ip dscp 2",
            "no snmp-server location thi sis a good location",
            "no snmp-server packetsize 500",
            "no snmp-server queue-length 2",
            "no snmp-server trap timeout 2",
            "no snmp-server source-interface informs Loopback999",
            "no snmp-server trap-source GigabitEthernet0/0",
            "no snmp-server system-shutdown",
            "no snmp-server enable traps aaa_server",
            "no snmp-server enable traps auth-framework sec-violation",
            "no snmp-server enable traps bfd",
            "no snmp-server enable traps bgp",
            "no snmp-server enable traps bgp cbgp2",
            "no snmp-server enable traps bridge newroot topologychange",
            "no snmp-server enable traps bulkstat collection transfer",
            "no snmp-server enable traps call-home message-send-fail server-fail",
            "no snmp-server enable traps cef resource-failure peer-state-change peer-fib-state-change inconsistency",
            "no snmp-server enable traps config",
            "no snmp-server enable traps config-copy",
            "no snmp-server enable traps config-ctid",
            "no snmp-server enable traps cpu threshold",
            "no snmp-server enable traps dhcp",
            "no snmp-server enable traps eigrp",
            "no snmp-server enable traps energywise",
            "no snmp-server enable traps entity",
            "no snmp-server enable traps entity-diag boot-up-fail hm-test-recover hm-thresh-reached scheduled-test-fail",
            "no snmp-server enable traps entity-perf throughput-notif",
            "no snmp-server enable traps entity-state",
            "no snmp-server enable traps envmon fan shutdown supply temperature status",
            "no snmp-server enable traps errdisable",
            "no snmp-server enable traps ether-oam",
            "no snmp-server enable traps ethernet cfm alarm",
            "no snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config",
            "no snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up",
            "no snmp-server enable traps ethernet evc status create delete",
            "no snmp-server enable traps event-manager",
            "no snmp-server enable traps flash insertion removal lowspace",
            "no snmp-server enable traps flex-links status",
            "no snmp-server enable traps flowmon",
            "no snmp-server enable traps fru-ctrl",
            "no snmp-server enable traps hsrp",
            "no snmp-server enable traps ike policy add",
            "no snmp-server enable traps ike policy delete",
            "no snmp-server enable traps ike tunnel start",
            "no snmp-server enable traps ike tunnel stop",
            "no snmp-server enable traps ipmulticast",
            "no snmp-server enable traps ipsec cryptomap add",
            "no snmp-server enable traps ipsec cryptomap attach",
            "no snmp-server enable traps ipsec cryptomap delete",
            "no snmp-server enable traps ipsec cryptomap detach",
            "no snmp-server enable traps ipsec too-many-sas",
            "no snmp-server enable traps ipsec tunnel start",
            "no snmp-server enable traps ipsec tunnel stop",
            "no snmp-server enable traps ipsla",
            "no snmp-server enable traps isis",
            "no snmp-server enable traps license",
            "no snmp-server enable traps l2tc threshold sys-threshold",
            "no snmp-server enable traps lisp",
            "no snmp-server enable traps local-auth",
            "no snmp-server enable traps mac-notification change move threshold",
            "no snmp-server enable traps memory bufferpeak",
            "no snmp-server enable traps mpls fast-reroute protected",
            "no snmp-server enable traps mpls rfc ldp",
            "no snmp-server enable traps mpls rfc traffic-eng",
            "no snmp-server enable traps mpls rfc vpn",
            "no snmp-server enable traps mpls traffic-eng",
            "no snmp-server enable traps mpls vpn",
            "no snmp-server enable traps msdp",
            "no snmp-server enable traps mvpn",
            "no snmp-server enable traps nhrp nhc",
            "no snmp-server enable traps nhrp nhp",
            "no snmp-server enable traps nhrp nhs",
            "no snmp-server enable traps nhrp quota-exceeded",
            "no snmp-server enable traps ospf cisco-specific errors",
            "no snmp-server enable traps ospf cisco-specific lsa",
            "no snmp-server enable traps ospf cisco-specific retransmit",
            "no snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
            "no snmp-server enable traps ospf cisco-specific state-change shamlink interface",
            "no snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
            "no snmp-server enable traps ospf errors",
            "no snmp-server enable traps ospf lsa",
            "no snmp-server enable traps ospf retransmit",
            "no snmp-server enable traps ospf state-change",
            "no snmp-server enable traps ospfv3 errors",
            "no snmp-server enable traps ospfv3 state-change",
            "no snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message",
            "no snmp-server enable traps pki",
            "no snmp-server enable traps port-security",
            "no snmp-server enable traps power-ethernet police",
            "no snmp-server enable traps pw vc",
            "no snmp-server enable traps rep",
            "no snmp-server enable traps rf",
            "no snmp-server enable traps smart-license",
            "no snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart",
            "no snmp-server enable traps stackwise",
            "no snmp-server enable traps stpx inconsistency root-inconsistency loop-inconsistency",
            "no snmp-server enable traps syslog",
            "no snmp-server enable traps transceiver all",
            "no snmp-server enable traps trustsec authz-file-error cache-file-error keystore-file-error keystore-sync-fail random-number-fail src-entropy-fail",
            "no snmp-server enable traps trustsec-interface unauthorized sap-fail authc-fail supplicant-fail authz-fail",
            "no snmp-server enable traps trustsec-policy peer-policy-updated authz-sgacl-fail",
            "no snmp-server enable traps trustsec-server radius-server provision-secret",
            "no snmp-server enable traps trustsec-sxp conn-srcaddr-err msg-parse-err conn-config-err binding-err conn-up conn-down binding-expn-fail",
            "no snmp-server enable traps tty",
            "no snmp-server enable traps udld link-fail-rpt status-change",
            "no snmp-server enable traps vlan-membership",
            "no snmp-server enable traps vlancreate",
            "no snmp-server enable traps vlandelete",
            "no snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down",
            "no snmp-server enable traps vswitch dual-active vsl",
            "no snmp-server enable traps vtp",
            "no snmp-server host 172.16.1.1 version 3 auth group0 tty",
            "no snmp-server host 172.16.2.1 version 3 priv newtera rsrb",
            "no snmp-server host 172.16.2.1 version 3 noauth replaceUser slb",
            "no snmp-server host 172.16.2.1 version 2c trapsac tty",
            "no snmp-server host 172.16.2.99 informs version 2c check msdp",
            "no snmp-server host 172.16.2.99 check slb",
            "no snmp-server host 172.16.2.99 checktrap isis",
            "no snmp-server group group0 v3 auth",
            "no snmp-server group group1 v1 notify me access ipv6 ipv6acl 2",
            "no snmp-server group group2 v3 priv",
            "no snmp-server group group3 v1 access ipv6 ipv6acl",
            "no snmp-server group group4 v1 access 2",
            "no snmp-server group replaceUser v3 noauth",
            "no snmp-server engineID local AB0C5342FA0A",
            "no snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA",
            "no snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB",
            "no snmp-server community commu1 view view1 ro ipv6 te",
            "no snmp-server community commu2 ro 1322",
            "no snmp-server community commu3 rw paul",
            "no snmp-server context contextWord1",
            "no snmp-server context contextWord2",
            "no snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
            "no snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9",
            "no snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11",
            "no snmp-server user new@user! new.family$ v1 access 24",
            "no snmp-server user paul familypaul v3 access ipv6 ipv6acl",
            "no snmp-server user replaceUser replaceUser v3",
            "no snmp-server user flow mfamily v3 access 27",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        self.maxDiff = None
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_snmp_server_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
            snmp-server user newuser newfamily v1 access 24
            snmp-server user replaceUser replaceUser v3
            snmp-server group group2 v3 priv
            snmp-server group replaceUser v3 noauth
            snmp-server community commu3 RW paul
            snmp-server trap timeout 2
            snmp-server source-interface informs Loopback999
            snmp-server packetsize 500
            snmp-server queue-length 2
            snmp-server location thi sis a good location
            snmp-server ip dscp 2
            snmp-server contact this is contact string
            snmp-server chassis-id this is a chassis id string
            snmp-server system-shutdown
            snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart
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
            snmp-server enable traps ethernet evc status create delete
            snmp-server enable traps bridge newroot topologychange
            snmp-server enable traps vtp
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
            snmp-server enable traps mpls vpn
            snmp-server enable traps vrfmib vrf-up vrf-down vnet-trunk-up vnet-trunk-down
            snmp-server host 172.16.2.99 informs version 2c check  msdp
            snmp-server host 172.16.2.99 check  slb
            snmp-server host 172.16.1.1 version 3 auth group0  tty
            snmp-server context contextWord1
            snmp-server context contextBAD
            snmp-server file-transfer access-group testAcl protocol ftp
            snmp-server file-transfer access-group testAcl protocol rcp
            snmp-server password-policy policy3 define min-len 12 max-len 12 upper-case 12 special-char 22 digits 23 change 11
            snmp-server accounting commands default
            snmp-server inform pending 2
            snmp-server view no-write.test testiso excluded
            snmp-server view test-view! test-test included
            """,
        )

        playbook = {
            "config": {
                "accounting": {"command": "default"},
                "cache": 2,
                "chassis_id": "this is a chassis id string",
                "communities": [
                    {"acl_v6": "te", "name": "commu1", "ro": True, "view": "view1"},
                    {"acl_v4": "1322", "name": "commu2", "ro": True},
                    {"acl_v4": "paul", "name": "commu3", "rw": True},
                ],
                "contact": "this is contact string",
                "context": ["contextWord2", "contextWord1"],
                "engine_id": [
                    {"id": "AB0C5342FA0A", "local": True},
                    {
                        "id": "AB0C5342FAAA",
                        "remote": {"host": "172.16.0.1", "udp_port": 22},
                    },
                    {
                        "id": "AB0C5342FAAB",
                        "remote": {"host": "172.16.0.2", "udp_port": 23},
                    },
                ],
                "file_transfer": {
                    "access_group": "testAcl",
                    "protocol": ["ftp", "rcp"],
                },
                "groups": [
                    {"group": "group0", "version": "v3", "version_option": "auth"},
                    {
                        "acl_v4": "2",
                        "acl_v6": "ipv6acl",
                        "group": "group1",
                        "notify": "me",
                        "version": "v1",
                    },
                    {"group": "group2", "version": "v3", "version_option": "priv"},
                    {
                        "group": "replaceUser",
                        "version": "v3",
                        "version_option": "noauth",
                    },
                ],
                "hosts": [
                    {
                        "community_string": "group0",
                        "host": "172.16.1.1",
                        "traps": ["tty"],
                        "version": "3",
                        "version_option": "auth",
                    },
                    {
                        "community_string": "newtera",
                        "host": "172.16.2.1",
                        "traps": ["rsrb"],
                        "version": "3",
                        "version_option": "priv",
                    },
                    {
                        "community_string": "replaceUser",
                        "host": "172.16.2.1",
                        "traps": ["slb"],
                        "version": "3",
                        "version_option": "noauth",
                    },
                    {
                        "community_string": "trapsac",
                        "host": "172.16.2.1",
                        "traps": ["tty"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "informs": True,
                        "traps": ["msdp"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "traps": ["slb"],
                    },
                    {
                        "community_string": "checktrap",
                        "host": "172.16.2.99",
                        "traps": ["isis"],
                    },
                ],
                "inform": {"pending": 2},
                "ip": {"dscp": 2},
                "location": "thi sis a good location",
                "packet_size": 500,
                "password_policy": [
                    {
                        "change": 3,
                        "digits": 23,
                        "lower_case": 12,
                        "max_len": 24,
                        "policy_name": "policy1",
                        "special_char": 32,
                        "upper_case": 12,
                    },
                    {
                        "change": 9,
                        "min_len": 12,
                        "policy_name": "policy2",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                    {
                        "change": 11,
                        "digits": 23,
                        "max_len": 12,
                        "min_len": 12,
                        "policy_name": "policy3",
                        "special_char": 22,
                        "upper_case": 12,
                    },
                ],
                "queue_length": 2,
                "source_interface": "Loopback999",
                "system_shutdown": True,
                "trap_source": "GigabitEthernet0/0",
                "trap_timeout": 2,
                "traps": {
                    "auth_framework": {"enable": True, "sec_violation": True},
                    "bfd": {"enable": True},
                    "bgp": {"cbgp2": True, "enable": True},
                    "bridge": {"enable": True, "newroot": True, "topologychange": True},
                    "casa": True,
                    "cef": {
                        "enable": True,
                        "inconsistency": True,
                        "peer_fib_state_change": True,
                        "peer_state_change": True,
                        "resource_failure": True,
                    },
                    "dlsw": {"enable": True},
                    "eigrp": True,
                    "energywise": True,
                    "ethernet": {
                        "cfm": {
                            "alarm": True,
                            "cc": {
                                "config": True,
                                "cross_connect": True,
                                "loop": True,
                                "mep_down": True,
                                "mep_up": True,
                            },
                            "crosscheck": {
                                "mep_missing": True,
                                "mep_unknown": True,
                                "service_up": True,
                            },
                        },
                        "evc": {"create": True, "delete": True, "status": True},
                    },
                    "event_manager": True,
                    "flowmon": True,
                    "frame_relay": {"enable": True},
                    "hsrp": True,
                    "ike": {
                        "policy": {"add": True, "delete": True},
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipmulticast": True,
                    "ipsec": {
                        "cryptomap": {
                            "add": True,
                            "attach": True,
                            "delete": True,
                            "detach": True,
                        },
                        "too_many_sas": True,
                        "tunnel": {"start": True, "stop": True},
                    },
                    "ipsla": True,
                    "isis": True,
                    "l2tun": {"pseudowire_status": True, "session": True},
                    "mpls": {
                        "vpn": {"enable": True},
                    },
                    "msdp": True,
                    "mvpn": True,
                    "ospf": {
                        "cisco_specific": {
                            "error": True,
                            "lsa": True,
                            "retransmit": True,
                            "state_change": {
                                "nssa_trans_change": True,
                                "shamlink": {"interface": True, "neighbor": True},
                            },
                        },
                        "error": True,
                        "lsa": True,
                        "retransmit": True,
                        "state_change": True,
                    },
                    "pim": {
                        "enable": True,
                        "invalid_pim_message": True,
                        "neighbor_change": True,
                        "rp_mapping_change": True,
                    },
                    "pki": True,
                    "pw_vc": True,
                    "rsvp": True,
                    "snmp": {
                        "authentication": True,
                        "coldstart": True,
                        "linkdown": True,
                        "linkup": True,
                        "warmstart": True,
                    },
                    "syslog": True,
                    "tty": True,
                    "vrfmib": {
                        "vnet_trunk_down": True,
                        "vnet_trunk_up": True,
                        "vrf_down": True,
                        "vrf_up": True,
                    },
                },
                "users": [
                    {
                        "acl_v4": "24",
                        "group": "newfamily",
                        "username": "newuser",
                        "version": "v1",
                    },
                    {
                        "acl_v6": "ipv6acl",
                        "group": "familypaul",
                        "username": "paul",
                        "version": "v3",
                    },
                    {
                        "group": "replaceUser",
                        "username": "replaceUser",
                        "version": "v3",
                    },
                ],
                "views": [
                    {
                        "name": "no-write.test",
                        "family_name": "testiso",
                        "excluded": True,
                    },
                    {
                        "name": "newView",
                        "family_name": "TestFamilyName",
                        "included": True,
                    },
                ],
            },
        }
        overridden = [
            "snmp-server cache interval 2",
            "snmp-server trap-source GigabitEthernet0/0",
            "snmp-server enable traps casa",
            "snmp-server enable traps eigrp",
            "snmp-server enable traps event-manager",
            "snmp-server enable traps flowmon",
            "snmp-server enable traps ipsla",
            "snmp-server enable traps isis",
            "snmp-server enable traps msdp",
            "snmp-server enable traps mvpn",
            "snmp-server enable traps pki",
            "snmp-server enable traps pw vc",
            "snmp-server enable traps rsvp",
            "snmp-server enable traps syslog",
            "snmp-server enable traps tty",
            "snmp-server enable traps l2tun pseudowire status",
            "snmp-server enable traps l2tun session",
            "snmp-server enable traps pim neighbor-change rp-mapping-change invalid-pim-message",
            "snmp-server enable traps ethernet cfm alarm",
            "snmp-server host 172.16.2.1 version 3 priv newtera rsrb",
            "snmp-server host 172.16.2.1 version 3 noauth replaceUser slb",
            "snmp-server host 172.16.2.1 version 2c trapsac tty",
            "snmp-server host 172.16.2.99 checktrap isis",
            "snmp-server group group0 v3 auth",
            "snmp-server group group1 v1 notify me access ipv6 ipv6acl 2",
            "snmp-server engineID local AB0C5342FA0A",
            "snmp-server engineID remote 172.16.0.1 udp-port 22 AB0C5342FAAA",
            "snmp-server community commu1 view view1 ro ipv6 te",
            "snmp-server community commu2 ro 1322",
            "snmp-server context contextWord2",
            "no snmp-server context contextBAD",
            "snmp-server password-policy policy1 define max-len 24 upper-case 12 lower-case 12 special-char 32 digits 23 change 3",
            "snmp-server password-policy policy2 define min-len 12 upper-case 12 special-char 22 change 9",
            "snmp-server user paul familypaul v3 access ipv6 ipv6acl",
            "snmp-server view newView TestFamilyName included",
            "no snmp-server enable traps vtp",
            "no snmp-server view test-view! test-test included",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_snmp_server_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server host 172.16.2.99 informs version 2c check  msdp
            snmp-server host 172.16.2.99 check  slb
            snmp-server host 172.16.1.1 version 3 auth group0  tty
            """,
        )
        playbook = {
            "config": {
                "hosts": [
                    {
                        "community_string": "group0",
                        "host": "172.16.1.1",
                        "traps": ["tty"],
                        "version": "3",
                        "version_option": "auth",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "informs": True,
                        "traps": ["msdp"],
                        "version": "2c",
                    },
                    {
                        "community_string": "check",
                        "host": "172.16.2.99",
                        "traps": ["slb"],
                    },
                ],
            },
        }
        overridden = []
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_snmp_server_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    snmp-server engineID local AB0C5342FA0A
                    snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB
                    snmp-server user paul familypaul v3 access ipv6 ipv6acl
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
                    snmp-server enable traps envmon status
                    snmp-server enable traps envmon supply
                    snmp-server enable traps envmon temperature
                    snmp-server enable traps envmon fan supply
                    snmp-server enable traps envmon fan temperature
                    snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config
                    snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up
                    snmp-server host 172.16.2.99 informs version 2c check  msdp stun
                    snmp-server host 172.16.2.99 check  slb pki
                    snmp-server host 172.16.2.99 checktrap  isis hsrp
                    snmp-server host 172.16.2.1 version 3 priv newtera  rsrb pim rsvp slb pki
                    snmp-server host 172.16.2.1 version 3 noauth replaceUser  slb pki
                    snmp-server host 172.16.2.1 version 2c trapsac  tty bgp
                    snmp-server group mygrp v3 priv read readme write writeit notify notifyme access acessing
                    snmp-server host 172.16.1.1 version 3 auth group0  tty bgp
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = {
            "engine_id": [
                {"id": "AB0C5342FA0A", "local": True},
                {
                    "id": "AB0C5342FAAB",
                    "remote": {"host": "172.16.0.2", "udp_port": 23},
                },
            ],
            "users": [
                {
                    "username": "paul",
                    "group": "familypaul",
                    "version": "v3",
                    "acl_v6": "ipv6acl",
                },
            ],
            "traps": {
                "ospf": {
                    "state_change": True,
                    "error": True,
                    "retransmit": True,
                    "lsa": True,
                    "cisco_specific": {
                        "state_change": {
                            "nssa_trans_change": True,
                            "shamlink": {"interface": True, "neighbor": True},
                        },
                        "error": True,
                        "retransmit": True,
                        "lsa": True,
                    },
                },
                "envmon": {
                    "enable": True,
                    "status": True,
                    "supply": True,
                    "temperature": True,
                    "fan_enable": True,
                },
                "ethernet": {
                    "cfm": {
                        "cc": {
                            "mep_up": True,
                            "mep_down": True,
                            "cross_connect": True,
                            "loop": True,
                            "config": True,
                        },
                        "crosscheck": {
                            "mep_missing": True,
                            "mep_unknown": True,
                            "service_up": True,
                        },
                    },
                },
            },
            "hosts": [
                {
                    "host": "172.16.1.1",
                    "community_string": "group0",
                    "traps": ["tty", "bgp"],
                    "version": "3",
                    "version_option": "auth",
                },
                {
                    "host": "172.16.2.1",
                    "community_string": "newtera",
                    "traps": ["rsrb", "pim", "rsvp", "slb", "pki"],
                    "version": "3",
                    "version_option": "priv",
                },
                {
                    "host": "172.16.2.1",
                    "community_string": "replaceUser",
                    "traps": ["slb", "pki"],
                    "version": "3",
                    "version_option": "noauth",
                },
                {
                    "host": "172.16.2.1",
                    "community_string": "trapsac",
                    "traps": ["tty", "bgp"],
                    "version": "2c",
                },
                {
                    "host": "172.16.2.99",
                    "informs": True,
                    "community_string": "check",
                    "traps": ["msdp", "stun"],
                    "version": "2c",
                },
                {
                    "host": "172.16.2.99",
                    "community_string": "check",
                    "traps": ["slb", "pki"],
                },
                {
                    "host": "172.16.2.99",
                    "community_string": "checktrap",
                    "traps": ["isis", "hsrp"],
                },
            ],
            "groups": [
                {
                    "group": "mygrp",
                    "version": "v3",
                    "version_option": "priv",
                    "notify": "notifyme",
                    "read": "readme",
                    "write": "writeit",
                    "acl_v4": "acessing",
                },
            ],
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(result["parsed"], parsed)

    def test_ios_snmp_server_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server host 172.16.2.99 checktrap isis hsrp
            snmp-server host 172.16.2.1 version 3 priv newtera rsrb pim rsvp slb pki
            snmp-server host 172.16.2.1 version 3 noauth replace-User! slb pki
            snmp-server host 172.16.2.1 vrf vrf1 version 3 priv newtera1 rsrb pim
            """,
        )
        self.execute_show_command_user.return_value = dedent(
            """\
            User name: TESTU22
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active IPv6 access-list: testv6acl
            Authentication Protocol: MD5
            Privacy Protocol: AES128
            Group-name: TESTG

            User name: TESTU23
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: aclWord
            Authentication Protocol: MD5
            Privacy Protocol: AES128
            Group-name: TESTG

            User name: TESTU24
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: TESTG

            User name: TESTU25
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: TESTG

            User name: testus2
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active
            Authentication Protocol: MD5
            Privacy Protocol: AES128
            Group-name: TESTG

            User name: TESTU
            Engine ID: 800000090300525400012D4A
            storage-type: nonvolatile        active
            Authentication Protocol: MD5
            Privacy Protocol: AES128
            Group-name: TESTG
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = {
            "hosts": [
                {
                    "host": "172.16.2.1",
                    "community_string": "newtera",
                    "traps": ["rsrb", "pim", "rsvp", "slb", "pki"],
                    "version": "3",
                    "version_option": "priv",
                },
                {
                    "host": "172.16.2.1",
                    "community_string": "replace-User!",
                    "traps": ["slb", "pki"],
                    "version": "3",
                    "version_option": "noauth",
                },
                {
                    "host": "172.16.2.99",
                    "community_string": "checktrap",
                    "traps": ["isis", "hsrp"],
                },
                {
                    "host": "172.16.2.99",
                    "vrf": "vrf1",
                    "version": "3",
                    "version_option": "priv",
                    "community_string": "newtera1",
                    "traps": ["rsrb", "pim"],
                },
            ],
            "users": [
                {
                    "group": "TESTG",
                    "username": "TESTU",
                },
                {
                    "acl_v6": "testv6acl",
                    "group": "TESTG",
                    "username": "TESTU22",
                },
                {
                    "acl_v4": "aclWord",
                    "group": "TESTG",
                    "username": "TESTU23",
                },
                {
                    "acl_v4": "22",
                    "group": "TESTG",
                    "username": "TESTU24",
                },
                {
                    "acl_v4": "22",
                    "group": "TESTG",
                    "username": "TESTU25",
                },
                {
                    "group": "TESTG",
                    "username": "testus2",
                },
                {
                    "acl_v4": "22",
                    "group": "usrgrp",
                    "username": "us1",
                    "version": "v1",
                },
            ],
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_snmp_server_rendered(self):
        set_module_args(
            {
                "config": {
                    "engine_id": [
                        {"id": "AB0C5342FA0A", "local": True},
                        {
                            "id": "AB0C5342FAAB",
                            "remote": {"host": "172.16.0.2", "udp_port": 23},
                        },
                    ],
                    "views": [
                        {"family_name": "iso", "name": "ro"},
                        {"family_name": "internet", "included": True, "name": "ro"},
                        {"family_name": "iso", "included": True, "name": "rw"},
                        {"family_name": "internet", "included": True, "name": "rw"},
                    ],
                    "groups": [
                        {
                            "group": "mygrp",
                            "version": "v3",
                            "version_option": "priv",
                            "notify": "notifyme",
                            "read": "readme",
                            "write": "writeit",
                            "acl_v4": "acessing",
                        },
                    ],
                    "users": [
                        {
                            "username": "paul",
                            "group": "familypaul",
                            "version": "v3",
                            "acl_v4": "ipv6",
                        },
                    ],
                    "traps": {
                        "ospf": {
                            "state_change": True,
                            "error": True,
                            "retransmit": True,
                            "lsa": True,
                            "cisco_specific": {
                                "state_change": {
                                    "nssa_trans_change": True,
                                    "shamlink": {"interface": True, "neighbor": True},
                                },
                                "error": True,
                                "retransmit": True,
                                "lsa": True,
                            },
                        },
                        "ethernet": {
                            "cfm": {
                                "cc": {
                                    "mep_up": True,
                                    "mep_down": True,
                                    "cross_connect": True,
                                    "loop": True,
                                    "config": True,
                                },
                                "crosscheck": {
                                    "mep_missing": True,
                                    "mep_unknown": True,
                                    "service_up": True,
                                },
                            },
                        },
                    },
                    "hosts": [
                        {
                            "host": "172.16.1.1",
                            "community_string": "group0",
                            "traps": ["tty"],
                            "version": "3",
                            "version_option": "auth",
                            "vrf": "mgmt",
                        },
                        {
                            "host": "172.16.2.1",
                            "community_string": "newtera",
                            "traps": ["rsrb"],
                            "version": "3",
                            "version_option": "priv",
                        },
                        {
                            "host": "172.16.2.1",
                            "community_string": "replaceUser",
                            "traps": ["slb"],
                            "version": "3",
                            "version_option": "noauth",
                        },
                        {
                            "host": "172.16.2.1",
                            "community_string": "trapsac",
                            "traps": ["tty"],
                            "version": "2c",
                        },
                        {
                            "host": "172.16.2.99",
                            "informs": True,
                            "community_string": "check",
                            "traps": ["msdp"],
                            "version": "2c",
                        },
                        {
                            "host": "172.16.2.99",
                            "community_string": "check",
                            "traps": ["slb"],
                        },
                        {
                            "host": "172.16.2.99",
                            "community_string": "checktrap",
                            "traps": ["isis"],
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = [
            "snmp-server enable traps ospf cisco-specific errors",
            "snmp-server enable traps ospf cisco-specific retransmit",
            "snmp-server enable traps ospf cisco-specific lsa",
            "snmp-server enable traps ospf cisco-specific state-change nssa-trans-change",
            "snmp-server enable traps ospf cisco-specific state-change shamlink interface",
            "snmp-server enable traps ospf cisco-specific state-change shamlink neighbor",
            "snmp-server enable traps ospf errors",
            "snmp-server enable traps ospf retransmit",
            "snmp-server enable traps ospf lsa",
            "snmp-server enable traps ospf state-change",
            "snmp-server enable traps ethernet cfm cc mep-up mep-down cross-connect loop config",
            "snmp-server enable traps ethernet cfm crosscheck mep-missing mep-unknown service-up",
            "snmp-server host 172.16.1.1 vrf mgmt version 3 auth group0 tty",
            "snmp-server host 172.16.2.1 version 3 priv newtera rsrb",
            "snmp-server host 172.16.2.1 version 3 noauth replaceUser slb",
            "snmp-server host 172.16.2.1 version 2c trapsac tty",
            "snmp-server host 172.16.2.99 informs version 2c check msdp",
            "snmp-server host 172.16.2.99 check slb",
            "snmp-server host 172.16.2.99 checktrap isis",
            "snmp-server group mygrp v3 priv read readme write writeit notify notifyme access acessing",
            "snmp-server engineID local AB0C5342FA0A",
            "snmp-server engineID remote 172.16.0.2 udp-port 23 AB0C5342FAAB",
            "snmp-server user paul familypaul v3 access ipv6",
            "snmp-server view ro iso",
            "snmp-server view ro internet included",
            "snmp-server view rw iso included",
            "snmp-server view rw internet included",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), sorted(rendered))

    def test_ios_snmp_server_rendered_user_options(self):
        set_module_args(
            {
                "config": {
                    "users": [
                        {
                            "username": "paul",
                            "group": "familypaul",
                            "version": "v3",
                            "authentication": {
                                "algorithm": "md5",
                                "password": "somepass",
                            },
                            "encryption": {
                                "priv": "aes",
                                "priv_option": 128,
                                "password": "somepass",
                            },
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = [
            "snmp-server user paul familypaul v3 auth md5 somepass priv aes 128 somepass",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), sorted(rendered))

    def test_ios_snmpv3_user_server_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server user rhcisco testfamily v3 access ipv4
            """,
        )

        self.execute_show_command_user.return_value = dedent(
            """\
            User name: replaceUser
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: replaceUser

            User name: paul
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: familypaul

            User name: flow
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: mfamily
            """,
        )

        playbook = {
            "config": {
                "users": [
                    {
                        "acl_v6": "ipv6acl",
                        "group": "familypaul",
                        "username": "paul",
                        "version": "v3",
                    },
                    {
                        "acl_v4": "27",
                        "group": "mfamily",
                        "username": "flow",
                        "version": "v3",
                    },
                ],
            },
        }
        merged = [
            "snmp-server user paul familypaul v3 access ipv6 ipv6acl 22",
            "snmp-server user flow mfamily v3 access 27",
        ]

        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_snmpv3_user_server_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            snmp-server user newuser newfamily v1 access 24
            """,
        )

        self.execute_show_command_user.return_value = dedent(
            """\
            User name: replaceUser
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 22
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: replaceUser

            User name: flow
            Engine ID: 000000090200000000000A0B
            storage-type: nonvolatile        active access-list: 27
            Authentication Protocol: MD5
            Privacy Protocol: None
            Group-name: mfamily
            """,
        )

        playbook = {
            "config": {
                "users": [
                    {
                        "acl_v4": "22",
                        "authentication": {
                            "algorithm": "md5",
                            "password": "replaceUser",
                        },
                        "group": "replaceUser",
                        "username": "replaceUser",
                        "version": "v3",
                    },
                    {
                        "acl_v4": "27",
                        "group": "mfamily",
                        "username": "flow",
                        "version": "v3",
                    },
                ],
            },
        }
        overridden = [
            "snmp-server user replaceUser replaceUser v3 auth md5 replaceUser access 22",
            "snmp-server user flow mfamily v3 access 27",
            "no snmp-server user newuser newfamily v1 access 24",
        ]

        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_snmp_server_configuration_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
                snmp-server community community_name RO
                snmp-server packetsize 400
                snmp-server location in the server room
                """,
        )
        self.execute_show_command_user.return_value = ""
        playbook = {
            "config": {
                "location": "in the racks",
                "contact": "john@doe.org",
                "packet_size": 500,
                "communities": [
                    {
                        "acl_v4": "ADMIN-SUP",
                        "name": "community_name",
                        "ro": True,
                    },
                ],
            },
        }
        expected_commands = [
            "no snmp-server community community_name ro",
            "snmp-server community community_name ro ADMIN-SUP",
            "snmp-server contact john@doe.org",
            "snmp-server location in the racks",
            "snmp-server packetsize 500",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(expected_commands))

    def test_ios_snmp_server_configuration_idempotence(self):
        self.execute_show_command.return_value = dedent(
            """\
                snmp-server community community_name RO ADMIN-SUP
                snmp-server packetsize 500
                snmp-server location in the racks
                snmp-server contact john@doe.org
            """,
        )
        self.execute_show_command_user.return_value = ""
        playbook = {
            "config": {
                "location": "in the racks",
                "contact": "john@doe.org",
                "packet_size": 500,
                "communities": [
                    {
                        "acl_v4": "ADMIN-SUP",
                        "name": "community_name",
                        "ro": True,
                    },
                ],
            },
            "state": "merged",
        }
        set_module_args(playbook)
        result = self.execute_module()
        self.assertEqual(result["changed"], False)
        self.assertEqual(result["commands"], [])
