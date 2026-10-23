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

    def test_ios_vrf_address_family_merged_bare_af_new(self):
        """Test that a bare address-family entry (no sub-config) generates the
        address-family block when the AF is not yet present on the device.

        Regression test for: ios_vrf_address_family silently drops address-family
        header when no sub-commands are generated for a new AF.
        """
        self.get_config.return_value = ""
        set_module_args(
            dict(
                config=[
                    dict(
                        name="TEST_VRF_01",
                        address_families=[
                            dict(afi="ipv4"),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "vrf definition TEST_VRF_01",
            "address-family ipv4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_address_family_merged_bare_af_idempotent(self):
        """Test that a bare address-family entry is idempotent when the AF is
        already present on the device with no sub-configuration.
        """
        run_cfg = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
             exit-address-family
            """,
        )
        self.get_config.return_value = run_cfg
        set_module_args(
            dict(
                config=[
                    dict(
                        name="TEST_VRF_01",
                        address_families=[
                            dict(afi="ipv4"),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def _bare_af_args(self, state):
        return dict(
            config=[dict(name="TEST_VRF_01", address_families=[dict(afi="ipv4")])],
            state=state,
        )

    def test_ios_vrf_address_family_merged_bare_af_keeps_existing_sub_config(self):
        """Merged is additive: a bare AF must not remove sub-config that is already on the device."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
              export map testing-map
             exit-address-family
            """,
        )
        set_module_args(self._bare_af_args("merged"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_merged_bare_af_multicast_only_creates_unicast(self):
        """A bare AF is unicast, so an existing multicast AF must not count as the AF being present."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4 multicast
             exit-address-family
            """,
        )
        set_module_args(self._bare_af_args("merged"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["vrf definition TEST_VRF_01", "address-family ipv4"])

    def test_ios_vrf_address_family_merged_bare_af_unicast_and_multicast(self):
        """With unicast and multicast present, a bare AF is compared with unicast only."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
              export map unicast-map
             exit-address-family
             address-family ipv4 multicast
              export map multicast-map
             exit-address-family
            """,
        )
        set_module_args(self._bare_af_args("merged"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_replaced_bare_af_clears_sub_config(self):
        """Replaced and overridden still treat a bare AF as an AF with no sub-config."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
              export map testing-map
             exit-address-family
            """,
        )
        set_module_args(self._bare_af_args("replaced"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["vrf definition TEST_VRF_01", "address-family ipv4", "no export map testing-map"],
        )

    _RT_HAVE = dedent(
        """\
        vrf definition TEST_VRF_01
         address-family ipv4
          route-target export 65000:1
          route-target import 65000:2
         exit-address-family
        """,
    )

    def _rt_args(self, state, exports=None, imports=None, safi="unicast"):
        route_target = {}
        if exports is not None:
            route_target["exports"] = exports
        if imports is not None:
            route_target["imports"] = imports
        return dict(
            config=[
                dict(
                    name="TEST_VRF_01",
                    address_families=[dict(afi="ipv4", safi=safi, route_target=route_target)],
                ),
            ],
            state=state,
        )

    def test_ios_vrf_address_family_deleted_address_family(self):
        """Deleting an address family must send a single 'no', not 'no no address-family'."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(
            dict(
                config=[dict(name="TEST_VRF_01", address_families=[dict(afi="ipv4")])],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["vrf definition TEST_VRF_01", "no address-family ipv4 unicast"],
        )

    def test_ios_vrf_address_family_merged_route_target_idempotent(self):
        """A route-target without 'stitching' equals the device one, which facts report as stitching False."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(
            self._rt_args(
                "merged",
                exports=[dict(rt_value="65000:1")],
                imports=[dict(rt_value="65000:2")],
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_replaced_route_target_idempotent(self):
        self.get_config.return_value = self._RT_HAVE
        set_module_args(
            self._rt_args(
                "replaced",
                exports=[dict(rt_value="65000:1", stitching=False)],
                imports=[dict(rt_value="65000:2")],
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_merged_route_target_stitching_is_a_change(self):
        """The same value with stitching is a different route-target and is still configured."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(self._rt_args("merged", exports=[dict(rt_value="65000:1", stitching=True)]))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf definition TEST_VRF_01",
                "address-family ipv4 unicast",
                "route-target export 65000:1 stitching",
            ],
        )

    def test_ios_vrf_address_family_merged_route_target_added(self):
        self.get_config.return_value = self._RT_HAVE
        set_module_args(
            self._rt_args(
                "merged",
                exports=[dict(rt_value="65000:1"), dict(rt_value="65000:9")],
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf definition TEST_VRF_01",
                "address-family ipv4 unicast",
                "route-target export 65000:9",
            ],
        )

    def test_ios_vrf_address_family_replaced_without_route_target_removes_it(self):
        """Replaced with an AF that has no route_target removes the route-targets on the device."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(self._bare_af_args("replaced"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf definition TEST_VRF_01",
                "address-family ipv4",
                "no route-target export 65000:1",
                "no route-target import 65000:2",
            ],
        )

    def test_ios_vrf_address_family_merged_without_route_target_keeps_it(self):
        """Merged never removes route-targets the task does not mention."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(self._bare_af_args("merged"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_merged_deprecated_route_target_idempotent(self):
        """The deprecated export/import_config route-target options are idempotent too."""
        self.get_config.return_value = self._RT_HAVE
        set_module_args(
            dict(
                config=[
                    dict(
                        name="TEST_VRF_01",
                        address_families=[
                            dict(
                                afi="ipv4",
                                safi="unicast",
                                route_target=dict(export="65000:1", import_config="65000:2"),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_merged_bare_af_with_options_idempotent(self):
        """A bare AF spec is the unicast AF, so its options are idempotent like an explicit unicast AF."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
              export map testing-map
              route-target export 65000:1
              route-target export 65000:9
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="TEST_VRF_01",
                        address_families=[
                            dict(
                                afi="ipv4",
                                export=dict(map="testing-map"),
                                route_target=dict(exports=[dict(rt_value="65000:9")]),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_vrf_address_family_overridden_bare_af_is_kept(self):
        """Overridden keeps the unicast AF for a bare want, it does not remove and re-add it."""
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
             exit-address-family
            """,
        )
        set_module_args(self._bare_af_args("overridden"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    _TWO_VRFS = dedent(
        """\
        vrf definition OTHER_VRF
         address-family ipv4
         exit-address-family
         address-family ipv6
         exit-address-family
        vrf definition TEST_VRF_01
         address-family ipv4
         exit-address-family
         address-family ipv6
         exit-address-family
        """,
    )

    def test_ios_vrf_address_family_deleted_only_touches_named_vrf(self):
        """Deleting from one VRF must not delete the address families of the other VRFs."""
        self.get_config.return_value = self._TWO_VRFS
        set_module_args(
            dict(
                config=[dict(name="TEST_VRF_01", address_families=[dict(afi="ipv4")])],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["vrf definition TEST_VRF_01", "no address-family ipv4 unicast"],
        )

    def test_ios_vrf_address_family_deleted_vrf_by_name(self):
        """A VRF named without address families loses all of them, other VRFs are kept."""
        self.get_config.return_value = self._TWO_VRFS
        set_module_args(dict(config=[dict(name="TEST_VRF_01")], state="deleted"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf definition TEST_VRF_01",
                "no address-family ipv4 unicast",
                "no address-family ipv6 unicast",
            ],
        )

    def test_ios_vrf_address_family_deleted_no_config_deletes_all(self):
        """Without a config all address families of all VRFs are deleted, one header per VRF."""
        self.get_config.return_value = self._TWO_VRFS
        set_module_args(dict(config=[], state="deleted"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf definition OTHER_VRF",
                "no address-family ipv4 unicast",
                "no address-family ipv6 unicast",
                "vrf definition TEST_VRF_01",
                "no address-family ipv4 unicast",
                "no address-family ipv6 unicast",
            ],
        )

    def test_ios_vrf_address_family_deleted_missing_address_family_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            vrf definition TEST_VRF_01
             address-family ipv4
             exit-address-family
            """,
        )
        set_module_args(
            dict(
                config=[dict(name="TEST_VRF_01", address_families=[dict(afi="ipv6")])],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
