# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vrf_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import AnsibleFailJson, set_module_args

from .ios_module import TestIosModule


class TestIosVrfGlobalModule(TestIosModule):
    """Test the ios_vrf_global module."""

    module = ios_vrf_global

    def setUp(self):
        """Set up for ios_vrf_global module tests."""
        super(TestIosVrfGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_global.vrf_global."
            "Vrf_globalFacts.get_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosVrfGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_vrf_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition test
             description This is test VRF
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 10.2.3.4:300
             route-target export 23.1.3.4:400
             route-target import 123.3.4.5:700
             vnet tag 34
             vpn id 3:4
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF2",
                        description="This is a test VRF for merged state",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="2:3",
                        route_target=dict(export="23.1.3.4:400", import_config="10.1.3.4:400"),
                        vnet=dict(tag=200),
                        vpn=dict(id="2:45"),
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "description This is a test VRF for merged state",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 2:3",
            "route-target export 23.1.3.4:400",
            "route-target import 10.1.3.4:400",
            "vnet tag 200",
            "vpn id 2:45",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF2
             description This is a test VRF for merged state
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 2:3
             route-target export 23.1.3.4:400
             route-target import 10.1.3.4:400
             vnet tag 200
             vpn id 2:45
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF2",
                        description="This is a test VRF for merged state",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="2:3",
                        route_target=dict(export="23.1.3.4:400", import_config="10.1.3.4:400"),
                        vnet=dict(tag=200),
                        vpn=dict(id="2:45"),
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vrf_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF2
             description This is a test VRF for merged state
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 2:3
             route-target export 23.1.3.4:400
             route-target import 10.1.3.4:400
             vnet tag 200
             vpn id 2:45
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF6",
                        description="VRF6 description",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="6:7",
                        route_target=dict(export="3.1.3.4:400", import_config="1.12.3.4:200"),
                        vnet=dict(tag=500),
                        vpn=dict(id="4:5"),
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "vrf definition VRF6",
            "description VRF6 description",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 6:7",
            "route-target export 3.1.3.4:400",
            "route-target import 1.12.3.4:200",
            "vnet tag 500",
            "vpn id 4:5",
            "no vrf definition VRF2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF6
             description VRF6 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 6:7
             route-target export 3.1.3.4:400
             route-target import 1.12.3.4:200
             vnet tag 500
             vpn id 4:5
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF7",
                        description="VRF7 description",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="7:8",
                        route_target=dict(export="23.1.3.4:500", import_config="12.1.3.4:400"),
                        vnet=dict(tag=300),
                        vpn=dict(id="2:45"),
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "vrf definition VRF7",
            "description VRF7 description",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 7:8",
            "route-target export 23.1.3.4:500",
            "route-target import 12.1.3.4:400",
            "vnet tag 300",
            "vpn id 2:45",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF7
             description VRF7 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 7:8
             route-target export 23.1.3.4:500
             route-target import 12.1.3.4:400
             vnet tag 300
             vpn id 2:45
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF7",
                        description="VRF7 description",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="7:8",
                        route_target=dict(export="23.1.3.4:500", import_config="12.1.3.4:400"),
                        vnet=dict(tag=300),
                        vpn=dict(id="2:45"),
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    # def test_ios_vrf_global_deleted(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         router bgp 65000
    #          no bgp default ipv4-unicast
    #          bgp nopeerup-delay post-boot 10
    #          bgp bestpath compare-routerid
    #          bgp advertise-best-external
    #          timers bgp 100 200 150
    #          redistribute connected metric 10
    #          neighbor 192.0.2.1 remote-as 100
    #          neighbor 192.0.2.1 route-map test-route out
    #          address-family ipv4
    #           neighbor 192.0.2.28 activate
    #           neighbor 172.31.35.140 activate
    #         """,
    #     )
    #     set_module_args(dict(config=dict(as_number=65000), state="deleted"))
    #     commands = [
    #         "router bgp 65000",
    #         "bgp default ipv4-unicast",
    #         "no timers bgp 100 200 150",
    #         "no bgp advertise-best-external",
    #         "no bgp bestpath compare-routerid",
    #         "no bgp nopeerup-delay post-boot 10",
    #         "no neighbor 192.0.2.1",
    #         "no redistribute connected",
    #     ]
    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_vrf_global_deleted_empty(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         """,
    #     )
    #     set_module_args(dict(config=dict(as_number=65000), state="deleted"))
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(result["commands"], [])

    def test_ios_vrf_global_purged(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF7
             description VRF7 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 7:8
             route-target export 23.1.3.4:500
             route-target import 12.1.3.4:400
             vnet tag 300
             vpn id 2:45
            """,
        )
        set_module_args(dict(state="purged"))
        commands = ["no vrf definition VRF7"]
        self.execute_module(changed=True, commands=commands)

    def test_deprecated_attributes_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF2",
                        description="This is a test VRF for rendered state",
                        ipv4=dict(multicast=dict(multitopology=True)),
                        ipv6=dict(multicast=dict(multitopology=True)),
                        rd="2:3",
                        route_target=dict(export="23.1.3.4:400", import_config="10.1.3.4:400"),
                        vnet=dict(tag=200),
                        vpn=dict(id="2:45"),
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "description This is a test VRF for rendered state",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 2:3",
            "route-target export 23.1.3.4:400",
            "route-target import 10.1.3.4:400",
            "vnet tag 200",
            "vpn id 2:45",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_vrf_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    vrf definition test
                     vnet tag 34
                     description This is test VRF
                     ipv4 multicast multitopology
                     ipv6 multicast multitopology
                     rd 10.2.3.4:300
                     vpn id 3:4
                     route-target export 23.1.3.4:400
                     route-target import 123.3.4.5:700
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "test",
                "description": "This is test VRF",
                "ipv4": {"multicast": {"multitopology": True}},
                "ipv6": {"multicast": {"multitopology": True}},
                "rd": "10.2.3.4:300",
                "route_target": {"export": "23.1.3.4:400", "import_config": "123.3.4.5:700"},
                "vnet": {"tag": 34},
                "vpn": {"id": "3:4"},
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])
