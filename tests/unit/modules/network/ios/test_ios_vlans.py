#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_vlans
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosVlansModule(TestIosModule):
    module = ios_vlans

    def setUp(self):
        super(TestIosVlansModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans."
            "VlansFacts.get_vlans_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.mock_execute_show_command_conf = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans."
            "VlansFacts.get_vlan_conf_data",
        )
        self.execute_show_command_conf = self.mock_execute_show_command_conf.start()
        self.mock_l2_device_command = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_vlans._is_l2_device",
        )
        self._l2_device_command = self.mock_l2_device_command.start()

    def tearDown(self):
        super(TestIosVlansModule, self).tearDown()
        self.mock_execute_show_command.stop()
        self.mock_execute_show_command_conf.stop()
        self.mock_l2_device_command.stop()

    def test_ios_vlans_merged(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_merged_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_replaced(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    ),
                    dict(
                        name="Replace_RemoteIsInMyName",
                        remote_span=True,
                        vlan_id=123,
                    ),
                    dict(
                        name="pvlan-primary",
                        private_vlan=dict(type="primary", associated=[11, 12]),
                        vlan_id=10,
                    ),
                    dict(
                        name="pvlan-community",
                        private_vlan=dict(type="community"),
                        vlan_id=11,
                    ),
                    dict(
                        name="pvlan-isolated",
                        private_vlan=dict(type="isolated"),
                        vlan_id=12,
                    ),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
            "vlan 123",
            "name Replace_RemoteIsInMyName",
            "no state active",
            "remote-span",
            "shutdown",
            "vlan 10",
            "name pvlan-primary",
            "private-vlan primary",
            "private-vlan association 11,12",
            "vlan 11",
            "name pvlan-community",
            "private-vlan community",
            "vlan 12",
            "name pvlan-isolated",
            "private-vlan isolated",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_replaced_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_overridden(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    ),
                    dict(
                        name="Override_RemoteIsInMyName",
                        remote_span=True,
                        vlan_id=123,
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no vlan 1",
            "no vlan 150",
            "no vlan 888",
            "no vlan 1002",
            "no vlan 1003",
            "no vlan 1004",
            "no vlan 1005",
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
            "vlan 123",
            "name Override_RemoteIsInMyName",
            "no state active",
            "remote-span",
            "shutdown",
        ]

        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_overridden_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_delete_vlans_config(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(dict(config=[dict(vlan_id=150)], state="deleted"))
        result = self.execute_module(changed=True)
        commands = [
            "vlan 150",
            "no name VLAN0150",
            "no state active",
            "no remote-span",
            "shutdown",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_vlans(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup
            1337 test                             active

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0

            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(dict(config=[dict(vlan_id=1337)], state="deleted"))
        result = self.execute_module(changed=True)
        commands = [
            "vlan 1337",
            "no name test",
            "no state active",
            "shutdown",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_purged_vlans(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup
            1337 test                             active

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0

            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(dict(config=[dict(vlan_id=1337)], state="purged"))
        result = self.execute_module(changed=True)
        commands = [
            "no vlan 1337",
        ]
        self.assertEqual(result["commands"], commands)

    def test_vlans_rendered(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "name test_vlan_200",
            "no shutdown",
            "remote-span",
            "state active",
            "vlan 200",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)

    def test_vlan_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    VLAN Name                             Status    Ports
                    ---- -------------------------------- --------- -------------------------------
                    1    default with space               active    Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45
                    2    dummy_NETWORK                    active
                    3    dummy_RACK_INFRA                 active    Fa0/46, Fa0/47, Fa0/48
                    10   pvlan-primary                    active
                    11   pvlan-isolated                   active
                    12   pvlan-community                  active
                    20   pvlan-2p                         active
                    21   pvlan-2i                         active
                    22   pvlan-2c                         active
                    1002 dummy-default                    act/unsup
                    1003 dummy-ring-default               act/unsup
                    1004 dummy-default                    act/unsup
                    1005 dummy-t-default                  act/unsup
                    1101 dummy_1101                       active
                    1102 dummy_1102                       active
                    1107 dummy_1107                       active

                    VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
                    ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
                    1    enet  100001     1500  -      -      -        -    -        0      0
                    2    enet  100002     1500  -      -      -        -    -        0      0
                    3    enet  100003     1500  -      -      -        -    -        0      0
                    10   enet  100010     1500  -      -      -        -    -        0      0
                    11   enet  100011     1500  -      -      -        -    -        0      0
                    12   enet  100012     1500  -      -      -        -    -        0      0
                    20   enet  100020     1500  -      -      -        -    -        0      0
                    21   enet  100021     1500  -      -      -        -    -        0      0
                    22   enet  100022     1500  -      -      -        -    -        0      0
                    1002 fddi  101002     1500  -      -      -        -    -        0      0
                    1003 tr    101003     1500  -      -      -        -    -        0      0
                    1004 fdnet 101004     1500  -      -      -        ieee -        0      0
                    1005 trnet 101005     1500  -      -      -        ibm  -        0      0
                    1101 enet  101101     1500  -      -      -        -    -        0      0
                    1102 enet  101102     1500  -      -      -        -    -        0      0
                    1107 enet  101107     1500  -      -      -        -    -        0      0

                    Remote SPAN VLANs
                    ------------------------------------------------------------------------------
                    1101-1105,1107

                    Primary Secondary Type              Ports
                    ------- --------- ----------------- ------------------------------------------
                    10      none      primary
                    none    11        isolated
                    none    12        community
                    20      21        isolated
                    20      22        community
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "name": "default with space",
                "vlan_id": 1,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "dummy_NETWORK",
                "vlan_id": 2,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "dummy_RACK_INFRA",
                "vlan_id": 3,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "pvlan-primary",
                "vlan_id": 10,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "primary"},
            },
            {
                "name": "pvlan-isolated",
                "vlan_id": 11,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "isolated"},
            },
            {
                "name": "pvlan-community",
                "vlan_id": 12,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "community"},
            },
            {
                "name": "pvlan-2p",
                "vlan_id": 20,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "primary", "associated": [21, 22]},
            },
            {
                "name": "pvlan-2i",
                "vlan_id": 21,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "isolated"},
            },
            {
                "name": "pvlan-2c",
                "vlan_id": 22,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "private_vlan": {"type": "community"},
            },
            {
                "name": "dummy-default",
                "vlan_id": 1002,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "dummy-ring-default",
                "vlan_id": 1003,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "dummy-default",
                "vlan_id": 1004,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "dummy-t-default",
                "vlan_id": 1005,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "dummy_1101",
                "vlan_id": 1101,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "remote_span": True,
            },
            {
                "name": "dummy_1102",
                "vlan_id": 1102,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "remote_span": True,
            },
            {
                "name": "dummy_1107",
                "vlan_id": 1107,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "remote_span": True,
            },
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(result["parsed"], parsed)

    def test_ios_vlans_gathered(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            VLAN Name                             Status    Ports
            ---- -------------------------------- --------- -------------------------------
            1    default                          active    Gi0/1, Gi0/2
            123  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                            Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                            Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                            Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                            Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
            150  VLAN0150                         active
            888  a_very_long_vlan_name_a_very_long_vlan_name
                                                  active
            1002 fddi-default                     act/unsup
            1003 trcrf-default                    act/unsup
            1004 fddinet-default                  act/unsup
            1005 trbrf-default                    act/unsup

            VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
            ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
            1    enet  100001     1500  -      -      -        -    -        0      0
            123  enet  100123     610   -      -      -        -    -        0      0
            150  enet  100150     1500  -      -      -        -    -        0      0
            888  enet  100888     1500  -      -      -        -    -        0      0
            1002 fddi  101002     1500  -      -      -        -    -        0      0
            1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
            1004 fdnet 101004     1500  -      -      -        ieee -        0      0
            1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


            VLAN AREHops STEHops Backup CRF
            ---- ------- ------- ----------
            1003 7       7       off

            Remote SPAN VLANs
            ------------------------------------------------------------------------------
            150

            Primary Secondary Type              Ports
            ------- --------- ----------------- ------------------------------------------
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = [
            {
                "name": "default",
                "vlan_id": 1,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "RemoteIsInMyName",
                "vlan_id": 123,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 610,
            },
            {
                "name": "VLAN0150",
                "vlan_id": 150,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "remote_span": True,
            },
            {
                "name": "a_very_long_vlan_name_a_very_long_vlan_name",
                "vlan_id": 888,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "fddi-default",
                "vlan_id": 1002,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "trcrf-default",
                "vlan_id": 1003,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 4472,
            },
            {
                "name": "fddinet-default",
                "vlan_id": 1004,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "trbrf-default",
                "vlan_id": 1005,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 4472,
            },
        ]
        result = self.execute_module(changed=False)

        self.maxDiff = None
        self.assertEqual(result["gathered"], gathered)

    def test_ios_vlans_config_merged(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            vlan configuration 102
             member evpn-instance 102 vni 10102
            vlan configuration 201
             member evpn-instance 201 vni 10201
            vlan configuration 202
             member evpn-instance 202 vni 10202
            vlan configuration 901
             member vni 50901
            vlan configuration 902
             member vni 50902
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vlan_id=101,
                        member=dict(
                            evi=101,
                            vni=10101,
                        ),
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan configuration 101",
            "member evpn-instance 101 vni 10101",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_config_merged_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command_conf.return_value = dedent(
            """\
            vlan configuration 101
              member evpn-instance 101 vni 10101
            vlan configuration 102
              member evpn-instance 102 vni 10102
            vlan configuration 201
              member evpn-instance 201 vni 10201
            vlan configuration 202
              member evpn-instance 202 vni 10202
            vlan configuration 901
              member vni 50901
            vlan configuration 902
              member vni 50902
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vlan_id=101,
                        member=dict(
                            evi=101,
                            vni=10101,
                        ),
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_config_overridden(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command_conf.return_value = dedent(
            """\
            vlan configuration 101
              member evpn-instance 101 vni 10101
            vlan configuration 102
              member evpn-instance 102 vni 10102
            vlan configuration 201
              member evpn-instance 201 vni 10201
            vlan configuration 202
              member evpn-instance 202 vni 10202
            vlan configuration 901
              member vni 50901
            vlan configuration 902
              member vni 50902
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vlan_id=101,
                        member=dict(
                            evi=102,
                            vni=10102,
                        ),
                    ),
                    dict(
                        vlan_id=102,
                        member=dict(
                            evi=101,
                            vni=10101,
                        ),
                    ),
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=True)
        commands = [
            "no vlan 201",
            "no vlan 202",
            "no vlan 901",
            "no vlan 902",
            "no vlan configuration 201",
            "no vlan configuration 202",
            "no vlan configuration 901",
            "no vlan configuration 902",
            "vlan configuration 101",
            "member evpn-instance 102 vni 10102",
            "vlan configuration 102",
            "member evpn-instance 101 vni 10101",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_delete_vlans_config_2(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command_conf.return_value = dedent(
            """\
            vlan configuration 101
             member evpn-instance 101 vni 10101
            vlan configuration 102
             member evpn-instance 102 vni 10102
            vlan configuration 201
             member evpn-instance 201 vni 10201
            vlan configuration 202
             member evpn-instance 202 vni 10202
            vlan configuration 901
             member vni 50901
            vlan configuration 902
             member vni 50902
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"vlan_id": 101},
                ],
                state="deleted",
            ),
        )
        result = self.execute_module(changed=True)
        commands = ["vlan configuration 101", "no member evpn-instance 101 vni 10101"]
        self.assertEqual(result["commands"], commands)

    def test_ios_purged_vlans_config(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command_conf.return_value = dedent(
            """\
            vlan configuration 101
             member evpn-instance 101 vni 10101
            vlan configuration 102
             member evpn-instance 102 vni 10102
            vlan configuration 201
             member evpn-instance 201 vni 10201
            vlan configuration 202
             member evpn-instance 202 vni 10202
            vlan configuration 901
             member vni 50901
            vlan configuration 902
             member vni 50902
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"vlan_id": 101},
                ],
                state="purged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = ["no vlan 101", "no vlan configuration 101"]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_config_rendered(self):
        self.mock_l2_device_command.side_effect = True
        self.mock_execute_show_command_conf.side_effect = ""
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vlan_id=101,
                        member=dict(
                            evi=101,
                            vni=10101,
                        ),
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "vlan configuration 101",
            "member evpn-instance 101 vni 10101",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    def test_ios_vlans_config_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    VLAN Name                             Status    Ports
                    ---- -------------------------------- --------- -------------------------------
                    1    default                          active    Gi0/1, Gi0/2
                    101  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                                    Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                                    Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
                                                                    Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
                                                                    Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
                    150  VLAN0150                         active
                    888  a_very_long_vlan_name_a_very_long_vlan_name
                                                        active
                    1002 fddi-default                     act/unsup
                    1003 trcrf-default                    act/unsup
                    1004 fddinet-default                  act/unsup
                    1005 trbrf-default                    act/unsup

                    VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
                    ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
                    1    enet  100001     1500  -      -      -        -    -        0      0
                    101  enet  100101     610   -      -      -        -    -        0      0
                    150  enet  100150     1500  -      -      -        -    -        0      0
                    888  enet  100888     1500  -      -      -        -    -        0      0
                    1002 fddi  101002     1500  -      -      -        -    -        0      0
                    1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
                    1004 fdnet 101004     1500  -      -      -        ieee -        0      0
                    1005 trbrf 101005     4472  -      -      15       ibm  -        0      0


                    VLAN AREHops STEHops Backup CRF
                    ---- ------- ------- ----------
                    1003 7       7       off

                    Remote SPAN VLANs
                    ------------------------------------------------------------------------------
                    150

                    Primary Secondary Type              Ports
                    ------- --------- ----------------- ------------------------------------------

                    vlan configuration 101
                     member evpn-instance 101 vni 10101
                    vlan configuration 102
                     member evpn-instance 102 vni 10102
                    vlan configuration 901
                     member vni 50901
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "name": "default",
                "vlan_id": 1,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "RemoteIsInMyName",
                "vlan_id": 101,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 610,
                "member": {"evi": 101, "vni": 10101},
            },
            {
                "name": "VLAN0150",
                "vlan_id": 150,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
                "remote_span": True,
            },
            {
                "name": "a_very_long_vlan_name_a_very_long_vlan_name",
                "vlan_id": 888,
                "state": "active",
                "shutdown": "disabled",
                "mtu": 1500,
            },
            {
                "name": "fddi-default",
                "vlan_id": 1002,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "trcrf-default",
                "vlan_id": 1003,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 4472,
            },
            {
                "name": "fddinet-default",
                "vlan_id": 1004,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 1500,
            },
            {
                "name": "trbrf-default",
                "vlan_id": 1005,
                "state": "active",
                "shutdown": "enabled",
                "mtu": 4472,
            },
            {"vlan_id": 102, "member": {"evi": 102, "vni": 10102}},
            {"vlan_id": 901, "member": {"vni": 50901}},
        ]

        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(result["parsed"], parsed)
