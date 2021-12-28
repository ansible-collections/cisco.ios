#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_vlans
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule
from textwrap import dedent


class TestIosVlansModule(TestIosModule):
    module = ios_vlans

    def setUp(self):
        super(TestIosVlansModule, self).setUp()

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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans."
            "VlansFacts.get_vlans_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.mock_l2_device_command = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_vlans._is_l2_device"
        )
        self._l2_device_command = self.mock_l2_device_command.start()

    def tearDown(self):
        super(TestIosVlansModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()
        self.mock_l2_device_command.stop()

    # def load_fixtures(self, commands=None, transport="cli"):
    #     def load_from_file(*args, **kwargs):
    #         return load_fixture("ios_vlans_config.cfg")

    #     self.mock_l2_device_command.side_effect = True
    #     self.execute_show_command.side_effect = load_from_file

    def test_ios_vlans_merged(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
                    )
                ],
                state="merged",
            )
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
        self.execute_show_command.side_effect = dedent(
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
            """
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
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_replaced(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
                ],
                state="replaced",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
            "vlan 123",
            "no state active",
            "no shutdown",
            "no mtu 610",
            "name Replace_RemoteIsInMyName",
            "remote-span",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_replaced_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_overridden(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 123",
            "no state active",
            "no shutdown",
            "no mtu 610",
            "name Override_RemoteIsInMyName",
            "remote-span",
            "no vlan 150",
            "no vlan 888",
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
        ]

        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_overridden_idempotent(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_delete_vlans_config(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
        )
        set_module_args(dict(config=[dict(vlan_id=150)], state="deleted"))
        result = self.execute_module(changed=True)
        commands = ["no vlan 150"]
        self.assertEqual(result["commands"], commands)

    def test_vlans_rendered(self):
        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = dedent(
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
            """
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
                    )
                ],
                state="rendered",
            )
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
