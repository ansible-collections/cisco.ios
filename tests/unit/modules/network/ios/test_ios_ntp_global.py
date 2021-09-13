#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_ntp_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
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
                            dict(
                                access_list="preauth_ipv6_acl",
                                ipv6=True,
                                kod=True,
                            ),
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
                    master=dict(stratum=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(peer="172.16.1.10", version=2),
                        dict(
                            key=2,
                            minpoll=5,
                            peer="172.16.1.11",
                            prefer=True,
                            version=2,
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com",
                            prefer=True,
                            use_ipv4=True,
                        ),
                        dict(peer="checkPeerDomainIpv6.com", use_ipv6=True),
                        dict(
                            peer="testPeerDomainIpv6.com",
                            prefer=True,
                            use_ipv6=True,
                        ),
                    ],
                    servers=[
                        dict(server="172.16.1.12", version=2),
                        dict(
                            server="172.16.1.13", source="GigabitEthernet0/1"
                        ),
                        dict(
                            server="checkServerDomainIpv6.com", use_ipv6=True
                        ),
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
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ntp allow mode control 4
            ntp allow mode private
            """
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="2", kod=True),
                            dict(
                                access_list="preauth_ipv6_acl",
                                ipv6=True,
                                kod=True,
                            ),
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
                    master=dict(stratum=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(peer="172.16.1.10", version=2),
                        dict(
                            key=2,
                            minpoll=5,
                            peer="172.16.1.11",
                            prefer=True,
                            version=2,
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com",
                            prefer=True,
                            use_ipv4=True,
                        ),
                        dict(peer="checkPeerDomainIpv6.com", use_ipv6=True),
                        dict(
                            peer="testPeerDomainIpv6.com",
                            prefer=True,
                            use_ipv6=True,
                        ),
                    ],
                    servers=[
                        dict(server="172.16.1.12", version=2),
                        dict(
                            server="172.16.1.13", source="GigabitEthernet0/1"
                        ),
                        dict(
                            server="checkServerDomainIpv6.com", use_ipv6=True
                        ),
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
        commands = [
            "ntp authenticate",
            "ntp broadcastdelay 22",
            "ntp logging",
            "ntp master 4",
            "ntp max-associations 34",
            "ntp maxdistance 3",
            "ntp mindistance 10",
            "ntp orphan 4",
            "ntp panic update",
            "ntp source GigabitEthernet0/1",
            "ntp update-calendar",
            "ntp access-group peer 2 kod",
            "ntp access-group ipv6 peer preauth_ipv6_acl kod",
            "ntp authentication-key 2 md5 SomeSecurePassword 7",
            "ntp peer 172.16.1.10 version 2",
            "ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
            "ntp peer ip checkPeerDomainIpv4.com prefer",
            "ntp peer ipv6 checkPeerDomainIpv6.com",
            "ntp peer ipv6 testPeerDomainIpv6.com prefer",
            "ntp server 172.16.1.12 version 2",
            "ntp server 172.16.1.13 source GigabitEthernet0/1",
            "ntp server ipv6 checkServerDomainIpv6.com",
            "ntp trusted-key 21",
            "ntp trusted-key 3 - 13",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_deleted(self):
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
        set_module_args(dict(config=dict(), state="deleted"))
        commands = [
            "no ntp allow mode control 4",
            "no ntp allow mode private",
            "no ntp authenticate",
            "no ntp broadcastdelay 22",
            "no ntp clock-period 5",
            "no ntp logging",
            "no ntp master 4",
            "no ntp max-associations 34",
            "no ntp maxdistance 3",
            "no ntp mindistance 10",
            "no ntp orphan 4",
            "no ntp panic update",
            "no ntp source GigabitEthernet0/1",
            "no ntp update-calendar",
            "no ntp access-group peer 2 kod",
            "no ntp access-group ipv4 peer DHCP-Server kod",
            "no ntp access-group ipv6 peer preauth_ipv6_acl kod",
            "no ntp access-group query-only 10",
            "no ntp authentication-key 2 md5 SomeSecurePassword 7",
            "no ntp peer 172.16.1.10 version 2",
            "no ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
            "no ntp peer ip checkPeerDomainIpv4.com prefer",
            "no ntp peer ipv6 checkPeerDomainIpv6.com",
            "no ntp peer ipv6 testPeerDomainIpv6.com prefer",
            "no ntp server 172.16.1.12 version 2",
            "no ntp server 172.16.1.13 source GigabitEthernet0/1",
            "no ntp server ipv6 checkServerDomainIpv6.com",
            "no ntp trusted-key 21",
            "no ntp trusted-key 3 - 13",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_deleted_blank(self):
        self.execute_show_command.return_value = dedent(
            """\
            """
        )
        set_module_args(dict(config=dict(), state="deleted"))
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_replaced_overridden(self):
        """ both the replaced and overridden states are supported to have same behaviour """
        self.execute_show_command.return_value = dedent(
            """\
            ntp allow mode control 4
            ntp allow mode private
            ntp authenticate
            ntp broadcastdelay 22
            ntp clock-period 15
            ntp logging
            ntp master 14
            ntp max-associations 134
            ntp maxdistance 3
            ntp mindistance 100
            ntp orphan 4
            ntp panic update
            ntp source Loopback888
            ntp update-calendar
            ntp access-group ipv4 peer DHCPAC kod
            ntp access-group ipv6 peer preauth_ipv6_acl kod
            ntp access-group peer 2 kod
            ntp access-group query-only 10
            ntp authentication-key 2 md5 SomeSecurePassword 7
            ntp peer 172.16.1.9 version 2
            ntp peer 172.16.1.1 key 2 minpoll 5 prefer version 2
            ntp peer ip checkPeerDomainIpv4.com prefer
            ntp peer ipv6 checkPeerDomainIpv6.com
            ntp peer ipv6 testPeerDomainIpv6.com prefer
            ntp server 172.16.1.19 version 2
            ntp server ipv6 checkServerDomainIpv6.com
            ntp server 172.16.1.111 source GigabitEthernet0/1
            ntp trusted-key 3 - 130
            ntp trusted-key 21
            """
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="2", kod=True),
                            dict(
                                access_list="preauth_ipv6_acl",
                                ipv6=True,
                                kod=True,
                            ),
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
                    master=dict(stratum=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(peer="172.16.1.10", version=2),
                        dict(
                            key=2,
                            minpoll=5,
                            peer="172.16.1.11",
                            prefer=True,
                            version=2,
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com",
                            prefer=True,
                            use_ipv4=True,
                        ),
                        dict(peer="checkPeerDomainIpv6.com", use_ipv6=True),
                        dict(
                            peer="testPeerDomainIpv6.com",
                            prefer=True,
                            use_ipv6=True,
                        ),
                    ],
                    servers=[
                        dict(server="172.16.1.12", version=2),
                        dict(
                            server="172.16.1.13", source="GigabitEthernet0/1"
                        ),
                        dict(
                            server="checkServerDomainIpv6.com", use_ipv6=True
                        ),
                    ],
                    source="GigabitEthernet0/1",
                    trusted_keys=[
                        dict(range_start=21),
                        dict(range_end=13, range_start=3),
                    ],
                    update_calendar=True,
                ),
                state="replaced",
            )
        )
        commands = [
            "no ntp allow mode private",
            "no ntp clock-period 15",
            "ntp master 4",
            "ntp max-associations 34",
            "ntp mindistance 10",
            "ntp source GigabitEthernet0/1",
            "no ntp access-group ipv4 peer DHCPAC kod",
            "no ntp access-group query-only 10",
            "ntp peer 172.16.1.10 version 2",
            "ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
            "no ntp peer 172.16.1.1 key 2 minpoll 5 prefer version 2",
            "no ntp peer 172.16.1.9 version 2",
            "ntp server 172.16.1.12 version 2",
            "ntp server 172.16.1.13 source GigabitEthernet0/1",
            "no ntp server 172.16.1.111 source GigabitEthernet0/1",
            "no ntp server 172.16.1.19 version 2",
            "no ntp trusted-key 3 - 130",
            "ntp trusted-key 3 - 13",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ntp_global_replaced_overridden_idempotent(self):
        """ both the replaced and overridden states are supported to have same behaviour """
        self.execute_show_command.return_value = dedent(
            """\
            ntp allow mode control 4
            ntp authenticate
            ntp broadcastdelay 22
            ntp logging
            ntp master 4
            ntp max-associations 34
            ntp maxdistance 3
            ntp mindistance 10
            ntp orphan 4
            ntp panic update
            ntp source Loopback888
            ntp update-calendar
            ntp access-group ipv6 peer preauth_ipv6_acl kod
            ntp access-group peer 2 kod
            ntp authentication-key 2 md5 SomeSecurePassword 7
            ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
            ntp peer ip checkPeerDomainIpv4.com prefer
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
                            dict(
                                access_list="preauth_ipv6_acl",
                                ipv6=True,
                                kod=True,
                            ),
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
                    master=dict(stratum=4),
                    max_associations=34,
                    max_distance=3,
                    min_distance=10,
                    orphan=4,
                    panic_update=True,
                    peers=[
                        dict(
                            key=2,
                            minpoll=5,
                            peer="172.16.1.11",
                            prefer=True,
                            version=2,
                        ),
                        dict(
                            peer="checkPeerDomainIpv4.com",
                            prefer=True,
                            use_ipv4=True,
                        ),
                    ],
                    servers=[
                        dict(
                            server="172.16.1.13", source="GigabitEthernet0/1"
                        ),
                        dict(
                            server="checkServerDomainIpv6.com", use_ipv6=True
                        ),
                    ],
                    source="Loopback888",
                    trusted_keys=[
                        dict(range_start=21),
                        dict(range_end=13, range_start=3),
                    ],
                    update_calendar=True,
                ),
                state="overridden",
            )
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
