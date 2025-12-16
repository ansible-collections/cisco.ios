# (c) 2021 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vrf_address_family
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosVrfAddressFamilyModule(TestIosModule):
    """Tests the ios_vrf_address_family module."""

    module = ios_vrf_address_family

    def setUp(self):
        """Setup for ios_vrf_address_family module tests."""
        super(TestIosVrfAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vrf_address_family.vrf_address_family."
            "Vrf_address_familyFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        """Tear down for ios_vrf_address_family module tests."""
        super(TestIosVrfAddressFamilyModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_ios_vrf_address_family_merged_idempotent(self):
        """Test the idempotent nature of the ios_vrf_address_family module in merged state."""
        run_cfg = dedent(
            """\
            vrf definition test
             address-family ipv4 unicast
              import map "import-map"
              export map "testing-map"
              export ipv4 unicast 37 map test allow-evpn
              inter-as-hybrid csc next-hop 1.2.3.4
              route-target export 10.12.0.1:20
              route-target import 10.0.0.1:30
              mdt auto-discovery ingress-replication inter-as mdt-hello-enable
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                bgp=dict(next_hop=dict(loopback=23)),
                                export=dict(
                                    map="testing-map",
                                    ipv4=dict(
                                        unicast=dict(
                                            prefix=37,
                                            map="test",
                                            allow_evpn=True,
                                        ),
                                    ),
                                ),
                                import_config=dict(
                                    map="import-map",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                                route_target=dict(
                                    exports=[
                                        dict(
                                            rt_value="10.12.0.1:20",
                                            stitching=False,
                                        ),
                                    ],
                                    imports=[
                                        dict(
                                            rt_value="10.0.0.1:30",
                                            stitching=False,
                                        ),
                                    ],
                                ),
                                mdt=dict(
                                    auto_discovery=dict(
                                        ingress_replication=dict(
                                            inter_as=dict(mdt_hello_enable=True),
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vrf_address_family_merged(self):
        """Test the merged state of the ios_vrf_address_family module."""
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF1",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                export=dict(
                                    map="testing-map",
                                ),
                                import_config=dict(
                                    map="import-map",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                                route_target=dict(
                                    exports=[
                                        dict(
                                            rt_value="10.12.0.1:20",
                                            stitching=True,
                                        ),
                                    ],
                                    imports=[
                                        dict(
                                            rt_value="10.0.0.1:10",
                                            stitching=False,
                                        ),
                                        dict(
                                            rt_value="10.0.0.1:30",
                                            stitching=True,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "vrf definition VRF1",
            "address-family ipv4 unicast",
            "export map testing-map",
            "import map import-map",
            "inter-as-hybrid csc next-hop 1.2.3.4",
            "route-target export 10.12.0.1:20 stitching",
            "route-target import 10.0.0.1:10",
            "route-target import 10.0.0.1:30 stitching",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted((result["commands"])), sorted((commands)))

    def test_ios_vrf_address_family_replaced(self):
        """Test the replaced state of the ios_vrf_address_family module."""
        run_cfg = dedent(
            """\
            vrf definition VRF1
             address-family ipv4 unicast
              import map "import-map"
              export map "testing-map"
              inter-as-hybrid csc next-hop 1.2.3.4
              route-target export 10.12.0.1:20
              route-target import 10.0.0.1:10
             exit-address-family
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF2",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                export=dict(
                                    map="testing-map",
                                ),
                                import_config=dict(
                                    map="import-map",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                                route_target=dict(
                                    exports=[
                                        dict(
                                            rt_value="10.12.0.1:20",
                                            stitching=False,
                                        ),
                                    ],
                                    imports=[
                                        dict(
                                            rt_value="10.0.0.1:10",
                                            stitching=False,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "vrf definition VRF2",
            "address-family ipv4 unicast",
            "export map testing-map",
            "import map import-map",
            "inter-as-hybrid csc next-hop 1.2.3.4",
            "route-target export 10.12.0.1:20",
            "route-target import 10.0.0.1:10",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(sorted((result["commands"])), sorted((commands)))

    def test_ios_vrf_address_family_replaced_idempotent(self):
        """Test the idempotent nature of the ios_vrf_address_family module in replaced state."""
        run_cfg = dedent(
            """\
            vrf definition VRF2
             address-family ipv4 unicast
              import map "import-map"
              export map "testing-map"
              inter-as-hybrid csc next-hop 1.2.3.4
              route-target export 10.12.0.1:20
              route-target import 10.0.0.1:10
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF2",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                export=dict(
                                    map="testing-map",
                                ),
                                import_config=dict(
                                    map="import-map",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                                route_target=dict(
                                    exports=[
                                        dict(
                                            rt_value="10.12.0.1:20",
                                            stitching=False,
                                        ),
                                    ],
                                    imports=[
                                        dict(
                                            rt_value="10.0.0.1:10",
                                            stitching=False,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vrf_address_family_overridden_idempotent(self):
        """Test the idempotent nature of the ios_vrf_address_family module in overridden state."""
        run_cfg = dedent(
            """\
            vrf definition VRF7
             address-family ipv4 unicast
              bgp next-hop loopback 40
              import map import-map1
              export map testing-map2
              inter-as-hybrid csc next-hop 1.2.3.4
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF7",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                bgp=dict(next_hop=dict(loopback=40)),
                                export=dict(
                                    map="testing-map2",
                                ),
                                import_config=dict(
                                    map="import-map1",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_vrf_address_family_deleted_idempotent(self):
        """Test the idempotent nature of the ios_vrf_address_family module in deleted state."""
        run_cfg = dedent(
            """\
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(dict(config=[], state="deleted"))

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_rendered(self):
        """Test the rendered state of the ios_vrf_address_family module."""
        set_module_args(
            dict(
                config=[
                    dict(
                        name="VRF1",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                export=dict(
                                    map="testing-map",
                                ),
                                import_config=dict(
                                    map="import-map",
                                ),
                                inter_as_hybrid=dict(
                                    csc=dict(next_hop="1.2.3.4"),
                                ),
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "vrf definition VRF1",
            "address-family ipv4 unicast",
            "export map testing-map",
            "import map import-map",
            "inter-as-hybrid csc next-hop 1.2.3.4",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_vrf_address_family_parsed(self):
        """Test the parsed state of the ios_vrf_address_family module."""
        run_cfg = dedent(
            """\
            vrf definition test
             address-family ipv4 unicast
              import map "import-map"
              export map "testing-map"
              inter-as-hybrid csc next-hop 1.2.3.4
              mdt auto-discovery ingress-replication inter-as mdt-hello-enable
             exit-address-family
            """,
        )
        set_module_args(dict(running_config=run_cfg, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "test",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "safi": "unicast",
                        "import_config": {
                            "map": "import-map",
                        },
                        "export": {
                            "map": "testing-map",
                        },
                        "inter_as_hybrid": {
                            "csc": {
                                "next_hop": "1.2.3.4",
                            },
                        },
                        "mdt": {
                            "auto_discovery": {
                                "ingress_replication": {
                                    "inter_as": {
                                        "mdt_hello_enable": True,
                                    },
                                },
                            },
                        },
                    },
                ],
            },
        ]

        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_vrf_address_family_parsed_mdt_bug(self):
        """Test parsing of various MDT configurations reported in a bug."""
        run_cfg = dedent(
            """\
            vrf definition DNB_Multicast_mottak
             rd 201627:3814
             !
             address-family ipv4
              mdt auto-discovery mldp
              mdt strict-rpf interface
              mdt partitioned mldp p2mp
              mdt data mpls mldp 255
              mdt overlay use-bgp
             exit-address-family
            !
            """,
        )
        set_module_args(dict(running_config=run_cfg, state="parsed"))
        result = self.execute_module(changed=False)
        expected_parsed = [
            {
                "name": "DNB_Multicast_mottak",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "safi": "unicast",
                        "mdt": {
                            "auto_discovery": {"mldp": True},
                            "strict_rpf": {"interface": True},
                            "partitioned": {"mldp": {"p2mp": True}},
                            "data": {"mpls": {"mldp": 255}},
                            "overlay": {"use_bgp": {"set": True}},
                        },
                    },
                ],
            },
        ]
        self.assertEqual(result["parsed"], expected_parsed)

    def test_ios_vrf_address_family_merged_mdt(self):
        """Test adding a new MDT config to an existing VRF AF in merged state."""
        run_cfg = dedent(
            """\
            vrf definition DNB_Multicast_mottak
             rd 201627:3814
             !
             address-family ipv4
              mdt strict-rpf interface
              mdt data mpls mldp 255
             exit-address-family
            !
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    {
                        "name": "DNB_Multicast_mottak",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "mdt": {
                                    "strict_rpf": {"interface": True},
                                    "data": {"mpls": {"mldp": 255}},
                                    "log_reuse": True,
                                },
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        expected_commands = [
            "vrf definition DNB_Multicast_mottak",
            "address-family ipv4 unicast",
            "mdt log-reuse",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_ios_vrf_address_family_replaced_mdt(self):
        """Test replacing MDT config on an existing VRF AF in replaced state."""
        run_cfg = dedent(
            """\
            vrf definition DNB_Multicast_mottak
             rd 201627:3814
             !
             address-family ipv4
              mdt auto-discovery mldp
              mdt overlay use-bgp
             exit-address-family
            !
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    {
                        "name": "DNB_Multicast_mottak",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "mdt": {
                                    "data": {"mpls": {"mldp": 100}},
                                    "strict_rpf": {"interface": True},
                                },
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        expected_commands = [
            "vrf definition DNB_Multicast_mottak",
            "address-family ipv4 unicast",
            "no mdt auto-discovery mldp",
            "no mdt overlay use-bgp",
            "mdt data mpls mldp 100",
            "mdt strict-rpf interface",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(expected_commands))

    def test_ios_vrf_address_family_overridden_mdt(self):
        """Test overriding MDT config on an existing VRF AF in overridden state."""
        run_cfg = dedent(
            """\
            vrf definition DNB_Multicast_mottak
             rd 201627:3814
             !
             address-family ipv4
              mdt auto-discovery mldp
              mdt strict-rpf interface
              mdt partitioned mldp p2mp
              mdt data mpls mldp 255
              mdt overlay use-bgp
             exit-address-family
            !
            """,
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=[
                    {
                        "name": "DNB_Multicast_mottak",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "mdt": {
                                    "log_reuse": True,
                                },
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )

        expected_commands = [
            "vrf definition DNB_Multicast_mottak",
            "address-family ipv4 unicast",
            "no mdt auto-discovery mldp",
            "no mdt strict-rpf interface",
            "no mdt partitioned mldp p2mp",
            "no mdt data mpls mldp 255",
            "no mdt overlay use-bgp",
            "mdt log-reuse",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(expected_commands))
