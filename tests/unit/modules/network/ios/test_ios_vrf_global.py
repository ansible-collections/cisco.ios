# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vrf_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

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
             rd 2:3
             route-target export 192.0.2.0:100
             route-target export 192.0.2.0:101
             route-target import 192.0.2.3:300
             route-target import 192.0.2.3:301
             vnet tag 34
             vpn id 3:4
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        dict(
                            name="VRF2",
                            description="This is a test VRF for merged state",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="2:3",
                            route_target=dict(
                                exports=["192.0.2.1:400", "192.0.2.1:401", "192.0.2.1:402"],
                                imports=["192.0.2.6:400", "192.0.2.6:401", "192.0.2.6:402"],
                            ),
                            vnet=dict(tag=200),
                            vpn=dict(id="2:45"),
                        ),
                    ],
                ),
                state="merged",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "description This is a test VRF for merged state",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 2:3",
            "route-target export 192.0.2.1:400",
            "route-target export 192.0.2.1:401",
            "route-target export 192.0.2.1:402",
            "route-target import 192.0.2.6:400",
            "route-target import 192.0.2.6:401",
            "route-target import 192.0.2.6:402",
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
             route-target export 192.0.2.1:400
             route-target export 192.0.2.1:401
             route-target export 192.0.2.1:402
             route-target import 192.0.2.6:400
             route-target import 192.0.2.6:401
             route-target import 192.0.2.6:402
             vnet tag 200
             vpn id 2:45
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        dict(
                            name="VRF2",
                            description="This is a test VRF for merged state",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="2:3",
                            route_target=dict(
                                exports=["192.0.2.1:400", "192.0.2.1:401", "192.0.2.1:402"],
                                imports=["192.0.2.6:400", "192.0.2.6:401", "192.0.2.6:402"],
                            ),
                            vnet=dict(tag=200),
                            vpn=dict(id="2:45"),
                        ),
                    ],
                ),
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
             route-target export 192.0.2.1:400
             route-target export 192.0.2.1:401
             route-target import 192.0.2.6:400
             route-target import 192.0.2.6:401
             vnet tag 200
             vpn id 2:45
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        dict(
                            name="VRF2",
                        ),
                        dict(
                            name="VRF6",
                            description="VRF6 description",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="6:7",
                            route_target=dict(
                                exports=["192.0.2.2:300", "192.0.2.2:301", "192.0.2.2:302"],
                                imports=["192.0.2.3:400", "192.0.2.3:401", "192.0.2.3:402"],
                            ),
                            vnet=dict(tag=500),
                            vpn=dict(id="4:5"),
                        ),
                    ],
                ),
                state="overridden",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "no description This is a test VRF for merged state",
            "no ipv4 multicast multitopology",
            "no ipv6 multicast multitopology",
            "no rd 2:3",
            "no route-target export 192.0.2.1:400",
            "no route-target export 192.0.2.1:401",
            "no route-target import 192.0.2.6:400",
            "no route-target import 192.0.2.6:401",
            "no vnet tag 200",
            "no vpn id 2:45",
            "vrf definition VRF6",
            "description VRF6 description",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 6:7",
            "route-target export 192.0.2.2:300",
            "route-target export 192.0.2.2:301",
            "route-target export 192.0.2.2:302",
            "route-target import 192.0.2.3:400",
            "route-target import 192.0.2.3:401",
            "route-target import 192.0.2.3:402",
            "vnet tag 500",
            "vpn id 4:5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF2
            vrf definition VRF6
             description VRF6 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 6:7
             route-target export 192.0.2.2:300
             route-target export 192.0.2.2:301
             route-target import 192.0.2.3:400
             route-target import 192.0.2.3:401
             vnet tag 500
             vpn id 4:5
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        dict(
                            name="VRF2",
                        ),
                        dict(
                            name="VRF6",
                            description="VRF6 description",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="6:7",
                            route_target=dict(
                                exports=["192.0.2.2:300", "192.0.2.2:301"],
                                imports=["192.0.2.3:400", "192.0.2.3:401"],
                            ),
                            vnet=dict(tag=500),
                            vpn=dict(id="4:5"),
                        ),
                        dict(
                            name="VRF7",
                            description="VRF7 description",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="7:8",
                            route_target=dict(
                                exports=[
                                    "198.51.100.2:500",
                                    "198.51.100.2:501",
                                    "198.51.100.2:502",
                                ],
                                imports=[
                                    "198.51.100.5:400",
                                    "198.51.100.5:401",
                                    "198.51.100.5:402",
                                ],
                            ),
                            vnet=dict(tag=300),
                            vpn=dict(id="2:45"),
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        commands = [
            "vrf definition VRF7",
            "description VRF7 description",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 7:8",
            "route-target export 198.51.100.2:500",
            "route-target export 198.51.100.2:501",
            "route-target export 198.51.100.2:502",
            "route-target import 198.51.100.5:400",
            "route-target import 198.51.100.5:401",
            "route-target import 198.51.100.5:402",
            "vnet tag 300",
            "vpn id 2:45",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF2
            vrf definition VRF6
             vnet tag 500
             description VRF6 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 6:7
             vpn id 4:5
             route-target export 192.0.2.2:300
             route-target export 192.0.2.2:301
             route-target import 192.0.2.3:400
             route-target import 192.0.2.3:401
            vrf definition VRF7
             vnet tag 300
             description VRF7 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 7:8
             vpn id 2:45
             route-target export 198.51.100.2:500
             route-target export 198.51.100.2:501
             route-target export 198.51.100.2:502
             route-target import 198.51.100.5:400
             route-target import 198.51.100.5:401
             route-target import 198.51.100.5:402
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        dict(
                            name="VRF2",
                        ),
                        dict(
                            name="VRF6",
                            description="VRF6 description",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="6:7",
                            route_target=dict(
                                exports=["192.0.2.2:300", "192.0.2.2:301"],
                                imports=["192.0.2.3:400", "192.0.2.3:401"],
                            ),
                            vnet=dict(tag=500),
                            vpn=dict(id="4:5"),
                        ),
                        dict(
                            name="VRF7",
                            description="VRF7 description",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="7:8",
                            route_target=dict(
                                exports=[
                                    "198.51.100.2:500",
                                    "198.51.100.2:501",
                                    "198.51.100.2:502",
                                ],
                                imports=[
                                    "198.51.100.5:400",
                                    "198.51.100.5:401",
                                    "198.51.100.5:402",
                                ],
                            ),
                            vnet=dict(tag=300),
                            vpn=dict(id="2:45"),
                        ),
                    ],
                ),
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vrf_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF2
            vrf definition VRF6
             vnet tag 500
             description VRF6 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 6:7
             vpn id 4:5
             route-target export 192.0.2.2:300
             route-target export 192.0.2.2:301
             route-target export 192.0.2.2:302
             route-target import 192.0.2.3:400
             route-target import 192.0.2.3:401
             route-target import 192.0.2.3:402
            vrf definition VRF7
             vnet tag 300
             description VRF7 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 7:8
             vpn id 2:45
             route-target export 198.51.100.2:500
             route-target export 198.51.100.2:501
             route-target import 198.51.100.5:400
             route-target import 198.51.100.5:401
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    vrfs=[
                        {
                            "name": "VRF6",
                        },
                        {
                            "name": "VRF7",
                        },
                    ],
                ),
                state="deleted",
            ),
        )
        commands = [
            "vrf definition VRF6",
            "no description VRF6 description",
            "no ipv4 multicast multitopology",
            "no ipv6 multicast multitopology",
            "no rd 6:7",
            "no route-target export 192.0.2.2:300",
            "no route-target export 192.0.2.2:301",
            "no route-target export 192.0.2.2:302",
            "no route-target import 192.0.2.3:400",
            "no route-target import 192.0.2.3:401",
            "no route-target import 192.0.2.3:402",
            "no vnet tag 500",
            "no vpn id 4:5",
            "vrf definition VRF7",
            "no description VRF7 description",
            "no ipv4 multicast multitopology",
            "no ipv6 multicast multitopology",
            "no rd 7:8",
            "no route-target export 198.51.100.2:500",
            "no route-target export 198.51.100.2:501",
            "no route-target import 198.51.100.5:400",
            "no route-target import 198.51.100.5:401",
            "no vnet tag 300",
            "no vpn id 2:45",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_deleted_empty(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(config=dict(), state="deleted"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_global_purged(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf definition VRF7
             description VRF7 description
             ipv4 multicast multitopology
             ipv6 multicast multitopology
             rd 7:8
             route-target export 198.51.100.2:500
             route-target export 198.51.100.2:501
             route-target export 198.51.100.2:502
             route-target import 198.51.100.5:400
             route-target import 198.51.100.5:401
             route-target import 198.51.100.5:402
             vnet tag 300
             vpn id 2:45
            """,
        )
        set_module_args(dict(state="purged"))
        commands = ["no vrf definition VRF7"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_vrf_global_rendered(self):
        set_module_args(
            dict(
                config={
                    "vrfs": [
                        dict(
                            name="VRF2",
                            description="This is a test VRF for rendered state",
                            ipv4=dict(multicast=dict(multitopology=True)),
                            ipv6=dict(multicast=dict(multitopology=True)),
                            rd="2:3",
                            route_target=dict(
                                exports=["192.0.2.1:400", "192.0.2.1:401", "192.0.2.1:402"],
                                imports=["192.0.2.6:400", "192.0.2.6:401", "192.0.2.6:402"],
                            ),
                            vnet=dict(tag=200),
                            vpn=dict(id="2:45"),
                        ),
                    ],
                },
                state="rendered",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "description This is a test VRF for rendered state",
            "ipv4 multicast multitopology",
            "ipv6 multicast multitopology",
            "rd 2:3",
            "route-target export 192.0.2.1:400",
            "route-target export 192.0.2.1:401",
            "route-target export 192.0.2.1:402",
            "route-target import 192.0.2.6:400",
            "route-target import 192.0.2.6:401",
            "route-target import 192.0.2.6:402",
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
                     description This is test VRF
                     ipv4 multicast multitopology
                     ipv6 multicast multitopology
                     rd 2:3
                     route-target export 192.0.2.0:100
                     route-target export 192.0.2.0:101
                     route-target export 192.0.2.0:102
                     route-target import 192.0.2.3:300
                     route-target import 192.0.2.3:301
                     route-target import 192.0.2.3:302
                     vnet tag 34
                     vpn id 3:4
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "vrfs": [
                {
                    "name": "test",
                    "description": "This is test VRF",
                    "ipv4": {"multicast": {"multitopology": True}},
                    "ipv6": {"multicast": {"multitopology": True}},
                    "rd": "2:3",
                    "route_target": {
                        "exports": ["192.0.2.0:100", "192.0.2.0:101", "192.0.2.0:102"],
                        "imports": ["192.0.2.3:300", "192.0.2.3:301", "192.0.2.3:302"],
                    },
                    "vnet": {"tag": 34},
                    "vpn": {"id": "3:4"},
                },
            ],
        }
        self.assertEqual(sorted(parsed_list), sorted(result["parsed"]))
