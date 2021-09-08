#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_ntp_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args
from .ios_module import TestIosModule


class TestIosNtpGlobalModule(TestIosModule):
    module = ios_ntp_global

    def setUp(self):
        super(TestIosNtpGlobalModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ntp_global.ntp_global."
            "Ntp_globalFacts.get_ntp_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosNtpGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_ntp_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ntp allow mode control 4
            ntp allow mode private
            ntp authenticate
            ntp broadcastdelay 22
            ntp clock-period 5
            ntp logging
            ntp master 4
            ntp max-associations 34
            ntp maxdistance 3
            ntp mindistance 10
            ntp orphan 4
            ntp panic update
            ntp source GigabitEthernet0/1
            ntp update-calendar
            ntp access-group ipv4 peer DHCP-Server kod
            ntp access-group ipv6 peer preauth_ipv6_acl kod
            ntp access-group peer 2 kod
            ntp access-group query-only 10
            ntp authentication-key 2 md5 SomeSecurePassword 7
            ntp peer 172.16.1.10 version 2
            ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
            ntp peer ip checkPeerDomainIpv4.com prefer
            ntp peer ipv6 checkPeerDomainIpv6.com
            ntp peer ipv6 testPeerDomainIpv6.com prefer
            ntp server 172.16.1.12 version 2
            ntp server ipv6 checkServerDomainIpv6.com
            ntp server 172.16.1.13 source GigabitEthernet0/1
            ntp trusted-key 3 - 13
            ntp trusted-key 21
            """
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="2", kod=True),
                            dict(access_list="preauth_ipv6_acl", ipv6=True, kod=True),
                        ]
                    ),
                    allow=dict(control=dict(rate_limit=4)),
                    authenticate=True,
                    authentication_keys=[
                        dict(
                            algorithm="md5",
                            encryption=7,
                            id=2,
                            key="SomeSecurePassword",
                        )
                    ],
                    broadcast_delay=22,
                    logging=True,
                    master=dict(stratum_number=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(peer="172.16.1.10", version=2),
                        dict(
                            key=2, minpoll=5, peer="172.16.1.11", prefer=True, version=2
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com", prefer=True, use_ipv4=True
                        ),
                        dict(peer="checkPeerDomainIpv6.com", use_ipv6=True),
                        dict(peer="testPeerDomainIpv6.com", prefer=True, use_ipv6=True),
                    ],
                    servers=[
                        dict(server="172.16.1.12", version=2),
                        dict(server="172.16.1.13", source="GigabitEthernet0/1"),
                        dict(server="checkServerDomainIpv6.com", use_ipv6=True),
                    ],
                    source="GigabitEthernet0/1",
                    trusted_keys=[
                        dict(range_start=21),
                        dict(range_end=13, range_start=3),
                    ],
                    update_calendar=True,
                ),
                state="merged",
            )
        )
        commands = []
        result = self.execute_module(changed=False)
        print(result["commands"])
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ntp allow mode control 4
            ntp allow mode private
            ntp authenticate
            ntp broadcastdelay 22
            ntp clock-period 5
            ntp logging
            ntp master 4
            ntp max-associations 34
            ntp maxdistance 3
            ntp mindistance 10
            ntp orphan 4
            ntp panic update
            ntp source GigabitEthernet0/1
            ntp update-calendar
            ntp access-group ipv4 peer DHCP-Server kod
            ntp access-group ipv6 peer preauth_ipv6_acl kod
            ntp access-group peer 2 kod
            ntp access-group query-only 10
            ntp authentication-key 2 md5 SomeSecurePassword 7
            ntp peer 172.16.1.10 version 2
            ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
            ntp peer ip checkPeerDomainIpv4.com prefer
            ntp peer ipv6 checkPeerDomainIpv6.com
            ntp peer ipv6 testPeerDomainIpv6.com prefer
            ntp server 172.16.1.12 version 2
            ntp server ipv6 checkServerDomainIpv6.com
            ntp server 172.16.1.13 source GigabitEthernet0/1
            ntp trusted-key 3 - 13
            ntp trusted-key 21
            """
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="2", kod=True),
                            dict(access_list="preauth_ipv6_acl", ipv6=True, kod=True),
                        ]
                    ),
                    allow=dict(control=dict(rate_limit=4)),
                    authenticate=True,
                    authentication_keys=[
                        dict(
                            algorithm="md5",
                            encryption=7,
                            id=2,
                            key="SomeSecurePassword",
                        )
                    ],
                    broadcast_delay=22,
                    logging=True,
                    master=dict(stratum_number=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(peer="172.16.1.10", version=2),
                        dict(
                            key=2, minpoll=5, peer="172.16.1.11", prefer=True, version=2
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com", prefer=True, use_ipv4=True
                        ),
                        dict(peer="checkPeerDomainIpv6.com", use_ipv6=True),
                        dict(peer="testPeerDomainIpv6.com", prefer=True, use_ipv6=True),
                    ],
                    servers=[
                        dict(server="172.16.1.12", version=2),
                        dict(server="172.16.1.13", source="GigabitEthernet0/1"),
                        dict(server="checkServerDomainIpv6.com", use_ipv6=True),
                    ],
                    source="GigabitEthernet0/1",
                    trusted_keys=[
                        dict(range_start=21),
                        dict(range_end=13, range_start=3),
                    ],
                    update_calendar=True,
                ),
                state="merged",
            )
        )
        commands = []
        result = self.execute_module(changed=False)
        print(result["commands"])
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_l3_interfaces_overridden(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface GigabitEthernet0/1
    #          description Configured by Ansible
    #          duplex auto
    #          speed auto
    #         interface GigabitEthernet0/2
    #          description This is test
    #          duplex auto
    #          speed 1000
    #         interface GigabitEthernet0/3
    #          description Configured by Ansible Network
    #          ipv6 address FD5D:12C9:2201:1::1/64
    #         interface GigabitEthernet0/3.100
    #          encapsulation dot1Q 20
    #          ip address 192.168.0.3 255.255.255.0
    #         interface Serial1/0
    #          description Configured by PAUL
    #         """
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="GigabitEthernet0/1",
    #                     ipv4=[dict(address="192.168.0.1/24", secondary=True)],
    #                 ),
    #                 dict(
    #                     name="GigabitEthernet0/2", ipv4=[dict(address="192.168.0.2/24")]
    #                 ),
    #                 dict(name="Serial1/0", ipv4=[dict(address="192.168.0.3/24")]),
    #             ],
    #             state="overridden",
    #         )
    #     )
    #     commands = [
    #         "interface GigabitEthernet0/3",
    #         "no ipv6 address fd5d:12c9:2201:1::1/64",
    #         "interface GigabitEthernet0/3.100",
    #         "no ip address 192.168.0.3 255.255.255.0",
    #         "interface GigabitEthernet0/1",
    #         "ip address 192.168.0.1 255.255.255.0 secondary",
    #         "interface GigabitEthernet0/2",
    #         "ip address 192.168.0.2 255.255.255.0",
    #         "interface Serial1/0",
    #         "ip address 192.168.0.3 255.255.255.0",
    #     ]

    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_l3_interfaces_deleted_all(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface GigabitEthernet0/1
    #          description Configured by Ansible
    #          duplex auto
    #          speed auto
    #         interface GigabitEthernet0/2
    #          description This is test
    #          duplex auto
    #          speed 1000
    #         interface GigabitEthernet0/3
    #          description Configured by Ansible Network
    #          ipv6 address FD5D:12C9:2201:1::1/64
    #         interface GigabitEthernet0/3.100
    #          encapsulation dot1Q 20
    #          ip address 192.168.0.3 255.255.255.0
    #         interface Serial1/0
    #          description Configured by PAUL
    #         """
    #     )
    #     set_module_args(dict(state="deleted"))
    #     commands = [
    #         "interface GigabitEthernet0/3",
    #         "no ipv6 address fd5d:12c9:2201:1::1/64",
    #         "interface GigabitEthernet0/3.100",
    #         "no ip address 192.168.0.3 255.255.255.0",
    #     ]

    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_l3_interfaces_replaced(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface GigabitEthernet0/1
    #          description Configured by Ansible
    #          duplex auto
    #          speed auto
    #         interface GigabitEthernet0/2
    #          description This is test
    #          duplex auto
    #          speed 1000
    #         interface GigabitEthernet0/3
    #          description Configured by Ansible Network
    #          ipv6 address FD5D:12C9:2201:1::1/64
    #         interface GigabitEthernet0/3.100
    #          encapsulation dot1Q 20
    #          ip address 192.168.0.3 255.255.255.0
    #         interface Serial1/0
    #          description Configured by PAUL
    #         """
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="GigabitEthernet0/3",
    #                     ipv6=[dict(address="FD5D:12C9:2202:1::1/64")],
    #                 ),
    #                 dict(
    #                     name="GigabitEthernet0/2", ipv4=[dict(address="192.168.0.2/24")]
    #                 ),
    #                 dict(name="Serial1/0", ipv4=[dict(address="192.168.0.5/24")]),
    #                 dict(
    #                     name="GigabitEthernet0/3.100",
    #                     ipv4=[dict(address="192.168.0.4/24")],
    #                 ),
    #             ],
    #             state="replaced",
    #         )
    #     )
    #     commands = [
    #         "interface GigabitEthernet0/3",
    #         "no ipv6 address fd5d:12c9:2201:1::1/64",
    #         "ipv6 address fd5d:12c9:2202:1::1/64",
    #         "interface GigabitEthernet0/2",
    #         "ip address 192.168.0.2 255.255.255.0",
    #         "interface Serial1/0",
    #         "ip address 192.168.0.5 255.255.255.0",
    #         "interface GigabitEthernet0/3.100",
    #         "no ip address 192.168.0.3 255.255.255.0",
    #         "ip address 192.168.0.4 255.255.255.0",
    #     ]

    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_l3_interfaces_parsed(self):
    #     set_module_args(
    #         dict(
    #             running_config="interface GigabitEthernet0/3.100\nencapsulation dot1Q 20\n ip address 192.168.0.3 255.255.255.0\n",
    #             state="parsed",
    #         )
    #     )
    #     result = self.execute_module(changed=False)
    #     parsed_list = [
    #         {"name": "GigabitEthernet0/3.100", "ipv4": [{"address": "192.168.0.3/24"}]}
    #     ]
    #     self.assertEqual(parsed_list, result["parsed"])

    # def test_ios_l3_interfaces_rendered(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="GigabitEthernet0/3",
    #                     ipv4=[
    #                         dict(
    #                             address="dhcp",
    #                             dhcp_client="GigabitEthernet0/3",
    #                             dhcp_hostname="abc.com",
    #                         )
    #                     ],
    #                     ipv6=[dict(address="FD5D:12C9:2202:1::1/64")],
    #                 ),
    #                 dict(
    #                     name="GigabitEthernet0/2", ipv4=[dict(address="192.168.0.2/24")]
    #                 ),
    #                 dict(
    #                     name="GigabitEthernet0/4",
    #                     ipv4=[dict(address="192.168.0.4/24", secondary=True)],
    #                 ),
    #                 dict(name="Serial1/0", ipv4=[dict(address="192.168.0.5/24")]),
    #             ],
    #             state="rendered",
    #         )
    #     )
    #     commands = [
    #         "interface GigabitEthernet0/3",
    #         "ip address dhcp client-id GigabitEthernet0/3 hostname abc.com",
    #         "ipv6 address fd5d:12c9:2202:1::1/64",
    #         "interface GigabitEthernet0/2",
    #         "ip address 192.168.0.2 255.255.255.0",
    #         "interface GigabitEthernet0/4",
    #         "ip address 192.168.0.4 255.255.255.0 secondary",
    #         "interface Serial1/0",
    #         "ip address 192.168.0.5 255.255.255.0",
    #     ]

    #     result = self.execute_module(changed=False)
    #     self.assertEqual(sorted(result["rendered"]), sorted(commands))

    # def test_ios_l3_interfaces_merged(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface GigabitEthernet0/1
    #          description Configured by Ansible
    #          duplex auto
    #          speed auto
    #         interface GigabitEthernet0/2
    #          description This is test
    #          duplex auto
    #          speed 1000
    #         interface GigabitEthernet0/3
    #          description Configured by Ansible Network
    #          ipv6 address FD5D:12C9:2201:1::1/64
    #         interface GigabitEthernet0/3.100
    #          encapsulation dot1Q 20
    #          ip address 192.168.0.3 255.255.255.0
    #         interface Serial1/0
    #          description Configured by PAUL
    #         """
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="GigabitEthernet0/1",
    #                     ipv4=[
    #                         dict(
    #                             dhcp=dict(
    #                                 client_id="GigabitEthernet0/2", hostname="test.com"
    #                             )
    #                         )
    #                     ],
    #                 ),
    #                 dict(name="GigabitEthernet0/2", ipv4=[dict(pool="PoolName1")]),
    #                 dict(name="Serial1/0", ipv6=[dict(autoconfig=dict(default=True))]),
    #                 dict(name="Serial2/0", ipv6=[dict(dhcp=dict(rapid_commit=True))]),
    #                 dict(
    #                     name="Serial3/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:1::1/64", anycast=True)],
    #                 ),
    #                 dict(
    #                     name="Serial4/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:2::1/64", cga=True)],
    #                 ),
    #                 dict(
    #                     name="Serial5/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:3::1/64", eui=True)],
    #                 ),
    #                 dict(
    #                     name="Serial6/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:4::1/64", link_local=True)],
    #                 ),
    #                 dict(
    #                     name="Serial7/0",
    #                     ipv6=[
    #                         dict(
    #                             address="FD5D:12C9:2201:5::1/64",
    #                             segment_routing=dict(ipv6_sr=True),
    #                         )
    #                     ],
    #                 ),
    #                 dict(
    #                     name="Serial8/0",
    #                     ipv6=[
    #                         dict(
    #                             address="FD5D:12C9:2201:6::1/64",
    #                             segment_routing=dict(default=True),
    #                         )
    #                     ],
    #                 ),
    #             ],
    #             state="merged",
    #         )
    #     )
    #     commands = [
    #         "interface GigabitEthernet0/1",
    #         "ip address dhcp client-id GigabitEthernet0/2 hostname test.com",
    #         "interface GigabitEthernet0/2",
    #         "ip address pool PoolName1",
    #         "interface Serial1/0",
    #         "ipv6 address autoconfig default",
    #         "interface Serial2/0",
    #         "ipv6 address dhcp rapid-commit",
    #         "interface Serial3/0",
    #         "ipv6 address fd5d:12c9:2201:1::1/64 anycast",
    #         "interface Serial7/0",
    #         "ipv6 address fd5d:12c9:2201:5::1/64 segment-routing ipv6-sr",
    #         "interface Serial8/0",
    #         "ipv6 address fd5d:12c9:2201:6::1/64 segment-routing default",
    #         "interface Serial4/0",
    #         "ipv6 address fd5d:12c9:2201:2::1/64 cga",
    #         "interface Serial6/0",
    #         "ipv6 address fd5d:12c9:2201:4::1/64 link-local",
    #         "interface Serial5/0",
    #         "ipv6 address fd5d:12c9:2201:3::1/64 eui",
    #     ]

    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_l3_interfaces_idemp_merged(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface GigabitEthernet0/3.100
    #          encapsulation dot1Q 20
    #          ip address 192.168.0.3 255.255.255.0
    #         interface GigabitEthernet0/1
    #          ip address dhcp client-id GigabitEthernet0/2 hostname test.com
    #         interface Serial2/0
    #          ipv6 address dhcp rapid-commit
    #         interface Serial3/0
    #          ipv6 address fd5d:12c9:2201:1::1/64 anycast
    #         interface Serial7/0
    #          ipv6 address fd5d:12c9:2201:5::1/64 segment-routing ipv6-sr
    #         interface Serial8/0
    #          ipv6 address fd5d:12c9:2201:6::1/64 segment-routing default
    #         interface Serial4/0
    #          ipv6 address fd5d:12c9:2201:2::1/64 cga
    #         interface Serial6/0
    #          ipv6 address fd5d:12c9:2201:4::1/64 link-local
    #         interface Serial5/0
    #          ipv6 address fd5d:12c9:2201:3::1/64 eui
    #         """
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="GigabitEthernet0/1",
    #                     ipv4=[
    #                         dict(
    #                             dhcp=dict(
    #                                 client_id="GigabitEthernet0/2", hostname="test.com"
    #                             )
    #                         )
    #                     ],
    #                 ),
    #                 dict(
    #                     name="GigabitEthernet0/3.100",
    #                     ipv4=[dict(address="192.168.0.3/24")],
    #                 ),
    #                 dict(name="Serial2/0", ipv6=[dict(dhcp=dict(rapid_commit=True))]),
    #                 dict(
    #                     name="Serial3/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:1::1/64", anycast=True)],
    #                 ),
    #                 dict(
    #                     name="Serial4/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:2::1/64", cga=True)],
    #                 ),
    #                 dict(
    #                     name="Serial5/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:3::1/64", eui=True)],
    #                 ),
    #                 dict(
    #                     name="Serial6/0",
    #                     ipv6=[dict(address="FD5D:12C9:2201:4::1/64", link_local=True)],
    #                 ),
    #                 dict(
    #                     name="Serial7/0",
    #                     ipv6=[
    #                         dict(
    #                             address="FD5D:12C9:2201:5::1/64",
    #                             segment_routing=dict(ipv6_sr=True),
    #                         )
    #                     ],
    #                 ),
    #                 dict(
    #                     name="Serial8/0",
    #                     ipv6=[
    #                         dict(
    #                             address="FD5D:12C9:2201:6::1/64",
    #                             segment_routing=dict(default=True),
    #                         )
    #                     ],
    #                 ),
    #             ],
    #             state="merged",
    #         )
    #     )
    #     commands = []
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))
