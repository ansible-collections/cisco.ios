#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_l3_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosL3InterfacesModule(TestIosModule):
    module = ios_l3_interfaces

    def setUp(self):
        super(TestIosL3InterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l3_interfaces.l3_interfaces."
            "L3_InterfacesFacts.get_l3_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL3InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_l3_interfaces_merged_common_ip(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface VirtualPortGroup0
             ip address 192.168.0.4 255.255.255.0
             ipv6 address fe80:0:3a2:84::3 link-local
            interface Serial3/0
             ipv6 address fd5d:12c9:2201:1::1/64
            interface Serial7/0
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3.100",
                        ipv4=[dict(address="192.168.0.3/24", secondary=True)],
                    ),
                    dict(
                        name="Serial3/0",
                        ipv6=[dict(address="FD5D:12C9:2201:1::1/64", cga=True)],
                    ),
                    dict(
                        name="VirtualPortGroup0",
                        ipv4=[dict(address="192.168.0.4/24", secondary=True)],
                        ipv6=[
                            dict(
                                address="fe80:0:3a2:84::3",
                                link_local=True,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_l3_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             description Configured by Ansible
             duplex auto
             speed auto
            interface GigabitEthernet0/2
             description This is test
             duplex auto
             speed 1000
            interface GigabitEthernet0/3
             description Configured by Ansible Network
             ipv6 address FD5D:12C9:2201:1::1/64
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface Serial1/0
             description Configured by PAUL
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[dict(address="192.168.0.1/24", secondary=True)],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[dict(address="192.168.0.2/24")],
                    ),
                    dict(name="Serial1/0", ipv4=[dict(address="192.168.0.3/24")]),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface GigabitEthernet0/3",
            "no ipv6 address fd5d:12c9:2201:1::1/64",
            "interface GigabitEthernet0/3.100",
            "no ip address 192.168.0.3 255.255.255.0",
            "interface GigabitEthernet0/1",
            "ip address 192.168.0.1 255.255.255.0 secondary",
            "interface GigabitEthernet0/2",
            "ip address 192.168.0.2 255.255.255.0",
            "interface Serial1/0",
            "ip address 192.168.0.3 255.255.255.0",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             description Configured by Ansible
             duplex auto
             speed auto
            interface GigabitEthernet0/2
             description This is test
             duplex auto
             speed 1000
            interface GigabitEthernet0/3
             description Configured by Ansible Network
             ipv6 address FD5D:12C9:2201:1::1/64
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface Serial1/0
             description Configured by PAUL
            """,
        )
        set_module_args(dict(state="deleted"))
        commands = [
            "interface GigabitEthernet0/3",
            "no ipv6 address fd5d:12c9:2201:1::1/64",
            "interface GigabitEthernet0/3.100",
            "no ip address 192.168.0.3 255.255.255.0",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             description Configured by Ansible
             duplex auto
             speed auto
            interface GigabitEthernet0/2
             description This is test
             duplex auto
             speed 1000
            interface GigabitEthernet0/3
             description Configured by Ansible Network
             ipv6 address FD5D:12C9:2201:1::1/64
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface Serial1/0
             description Configured by PAUL
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3",
                        ipv6=[dict(address="FD5D:12C9:2202:1::1/64")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[dict(address="192.168.0.2/24", secondary=False)],
                    ),
                    dict(name="Serial1/0", ipv4=[dict(address="192.168.0.5/24")]),
                    dict(
                        name="GigabitEthernet0/3.100",
                        ipv4=[dict(address="192.168.0.4/24")],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/3",
            "no ipv6 address fd5d:12c9:2201:1::1/64",
            "ipv6 address fd5d:12c9:2202:1::1/64",
            "interface GigabitEthernet0/2",
            "ip address 192.168.0.2 255.255.255.0",
            "interface Serial1/0",
            "ip address 192.168.0.5 255.255.255.0",
            "interface GigabitEthernet0/3.100",
            "no ip address 192.168.0.3 255.255.255.0",
            "ip address 192.168.0.4 255.255.255.0",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface GigabitEthernet0/3.100
                      encapsulation dot1Q 20
                      ip address 192.168.0.3 255.255.255.0
                      mac-address 0000.0000.0001
                      ip redirects
                      ip mtu 1500
                      ip helper-address global 10.0.0.1
                      ip unreachables
                      ip proxy-arp
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "GigabitEthernet0/3.100",
                "mac_address": "0000.0000.0001",
                "helper_addresses": {"ipv4": [{"global": True, "destination_ip": "10.0.0.1"}]},
                "ipv4": [
                    {"address": "192.168.0.3/24"},
                    {"redirects": True},
                    {"mtu": 1500},
                    {"unreachables": True},
                    {"proxy_arp": True},
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_l3_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3",
                        ipv4=[
                            dict(
                                address="dhcp",
                                dhcp_client="GigabitEthernet0/3",
                                dhcp_hostname="abc.com",
                            ),
                        ],
                        ipv6=[dict(address="FD5D:12C9:2202:1::1/64")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[
                            dict(address="192.168.0.2/24", redirects=True, mtu=1500),
                            dict(
                                dhcp=dict(
                                    enable=False,
                                    hostname="abc.com",
                                ),
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/4",
                        ipv4=[dict(address="192.168.0.4/24", secondary=True)],
                    ),
                    dict(name="Serial1/0", ipv4=[dict(address="192.168.0.5/24")]),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface GigabitEthernet0/3",
            "ip address dhcp client-id GigabitEthernet0/3 hostname abc.com",
            "ipv6 address fd5d:12c9:2202:1::1/64",
            "interface GigabitEthernet0/2",
            "ip address 192.168.0.2 255.255.255.0",
            "ip redirects",
            "ip mtu 1500",
            "interface GigabitEthernet0/4",
            "ip address 192.168.0.4 255.255.255.0 secondary",
            "interface Serial1/0",
            "ip address 192.168.0.5 255.255.255.0",
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    # --- NEW TEST CASE ADDED HERE ---
    def test_ios_l3_interfaces_mac_address_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan101",
                        mac_address="dead.beef.f00d",
                        ipv4=[dict(address="203.0.113.1/24")],
                        ipv6=[dict(address="2001:db8::1/64")],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface Vlan101",
            "mac-address dead.beef.f00d",
            "ip address 203.0.113.1 255.255.255.0",
            "ipv6 address 2001:db8::1/64",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_l3_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             description Configured by Ansible
             duplex auto
             speed auto
            interface GigabitEthernet0/2
             description This is test
             duplex auto
             speed 1000
            interface GigabitEthernet0/3
             description Configured by Ansible Network
             ipv6 address FD5D:12C9:2201:1::1/64
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface Serial1/0
             description Configured by PAUL
            interface Vlan901
             ip unnumbered Loopback2
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[
                            dict(
                                dhcp=dict(
                                    client_id="GigabitEthernet0/2",
                                    hostname="test.com",
                                ),
                            ),
                        ],
                    ),
                    dict(name="GigabitEthernet0/2", ipv4=[dict(pool="PoolName1")]),
                    dict(name="Serial1/0", ipv6=[dict(autoconfig=dict(default=True))]),
                    dict(name="Serial2/0", ipv6=[dict(dhcp=dict(rapid_commit=True))]),
                    dict(
                        name="Serial3/0",
                        ipv6=[dict(address="FD5D:12C9:2201:1::1/64", anycast=True)],
                    ),
                    dict(name="Vlan51", ipv4=[dict(address="192.168.0.4/31")]),
                    dict(
                        name="Serial4/0",
                        ipv6=[dict(address="FD5D:12C9:2201:2::1/64", cga=True)],
                    ),
                    dict(
                        name="Serial5/0",
                        ipv6=[dict(address="FD5D:12C9:2201:3::1/64", eui=True)],
                    ),
                    dict(
                        name="Serial6/0",
                        ipv6=[dict(address="FD5D:12C9:2201:4::1/64", link_local=True)],
                    ),
                    dict(
                        name="Serial7/0",
                        ipv6=[
                            dict(
                                address="FD5D:12C9:2201:5::1/64",
                                segment_routing=dict(ipv6_sr=True),
                            ),
                        ],
                    ),
                    dict(
                        name="Serial8/0",
                        ipv6=[
                            dict(
                                address="FD5D:12C9:2201:6::1/64",
                                segment_routing=dict(default=True),
                            ),
                        ],
                    ),
                    dict(
                        autostate=False,
                        name="Vlan901",
                        ipv6=[
                            dict(
                                enable=True,
                            ),
                        ],
                        ipv4=[
                            dict(
                                source_interface=dict(name="Loopback1"),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "interface GigabitEthernet0/1",
            "ip address dhcp client-id GigabitEthernet0/2 hostname test.com",
            "interface GigabitEthernet0/2",
            "ip address pool PoolName1",
            "interface Serial1/0",
            "ipv6 address autoconfig default",
            "interface Serial2/0",
            "ipv6 address dhcp rapid-commit",
            "interface Serial3/0",
            "ipv6 address fd5d:12c9:2201:1::1/64 anycast",
            "interface Serial7/0",
            "ipv6 address fd5d:12c9:2201:5::1/64 segment-routing ipv6-sr",
            "interface Serial8/0",
            "ipv6 address fd5d:12c9:2201:6::1/64 segment-routing default",
            "interface Serial4/0",
            "ipv6 address fd5d:12c9:2201:2::1/64 cga",
            "interface Serial6/0",
            "ipv6 address fd5d:12c9:2201:4::1/64 link-local",
            "interface Serial5/0",
            "ipv6 address fd5d:12c9:2201:3::1/64 eui",
            "interface Vlan51",
            "ip address 192.168.0.4 255.255.255.254",
            "interface Vlan901",
            "ip unnumbered Loopback1",
            "ipv6 enable",
            "no autostate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_idemp_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
            interface GigabitEthernet0/1
             ip address dhcp client-id GigabitEthernet0/2 hostname test.com
            interface Serial2/0
             ipv6 address dhcp rapid-commit
            interface Serial3/0
             ipv6 address fd5d:12c9:2201:1::1/64 anycast
            interface Serial7/0
             ipv6 address fd5d:12c9:2201:5::1/64 segment-routing ipv6-sr
            interface Serial8/0
             ipv6 address fd5d:12c9:2201:6::1/64 segment-routing default
            interface Serial4/0
             ipv6 address fd5d:12c9:2201:2::1/64 cga
            interface Serial6/0
             ipv6 address fd5d:12c9:2201:4::1/64 link-local
            interface Serial5/0
             ipv6 address fd5d:12c9:2201:3::1/64 eui
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[
                            dict(
                                dhcp=dict(
                                    client_id="GigabitEthernet0/2",
                                    hostname="test.com",
                                ),
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3.100",
                        ipv4=[dict(address="192.168.0.3/24")],
                    ),
                    dict(name="Serial2/0", ipv6=[dict(dhcp=dict(rapid_commit=True))]),
                    dict(
                        name="Serial3/0",
                        ipv6=[dict(address="FD5D:12C9:2201:1::1/64", anycast=True)],
                    ),
                    dict(
                        name="Serial4/0",
                        ipv6=[dict(address="FD5D:12C9:2201:2::1/64", cga=True)],
                    ),
                    dict(
                        name="Serial5/0",
                        ipv6=[dict(address="FD5D:12C9:2201:3::1/64", eui=True)],
                    ),
                    dict(
                        name="Serial6/0",
                        ipv6=[dict(address="FD5D:12C9:2201:4::1/64", link_local=True)],
                    ),
                    dict(
                        name="Serial7/0",
                        ipv6=[
                            dict(
                                address="FD5D:12C9:2201:5::1/64",
                                segment_routing=dict(ipv6_sr=True),
                            ),
                        ],
                    ),
                    dict(
                        name="Serial8/0",
                        ipv6=[
                            dict(
                                address="FD5D:12C9:2201:6::1/64",
                                segment_routing=dict(default=True),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_remove_primary_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/3.100
             encapsulation dot1Q 20
             ip address 192.168.0.3 255.255.255.0
             ip address 192.168.1.3 255.255.255.0 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3.100",
                        ipv4=[dict(address="192.168.1.3/24")],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface GigabitEthernet0/3.100",
            "ip address 192.168.1.3 255.255.255.0",
            "no ip address 192.168.0.3 255.255.255.0",
            "no ip address 192.168.1.3 255.255.255.0 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l3_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             no autostate
            interface Vlan901
             ip unnumbered Loopback2
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
        )
        result = self.execute_module(changed=False)
        gathered = [
            {
                "name": "GigabitEthernet0/1",
                "autostate": False,
            },
            {
                "name": "Vlan901",
                "ipv4": [{"source_interface": {"name": "Loopback2"}}],
                "autostate": True,
            },
        ]
        self.assertEqual(result["gathered"], gathered)

    def test_ios_l3_interfaces_helper_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface GigabitEthernet0/1
             description Configured by Ansible
             duplex auto
             speed auto
             ip helper-address 10.0.0.3
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/1",
                        helper_addresses={
                            "ipv4": [
                                dict(vrf="abc", destination_ip="10.0.0.1"),
                                dict(destination_ip="10.0.0.2"),
                                {"global": True, "destination_ip": "10.0.0.3"},
                            ],
                        },
                        ipv4=[
                            {
                                "address": "192.168.0.1/24",
                                "mtu": 4,
                            },
                        ],
                    ),
                ],
                state="overridden",
            ),
        )

        commands = [
            "interface GigabitEthernet0/1",
            "ip address 192.168.0.1 255.255.255.0",
            "ip helper-address vrf abc 10.0.0.1",
            "ip helper-address 10.0.0.2",
            "ip helper-address global 10.0.0.3",
            "no ip helper-address 10.0.0.3",
            "ip mtu 4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
