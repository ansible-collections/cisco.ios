#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_vlans
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule, load_fixture


class TestIosVlansModule(TestIosModule):
    module = ios_vlans

    def setUp(self):
        super(TestIosVlansModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans."
            "VlansFacts.get_vlans_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.mock_l2_device_command = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_vlans._is_l2_device",
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

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_vlans_config.cfg")

        self.mock_l2_device_command.side_effect = True
        self.execute_show_command.side_effect = load_from_file

    def test_ios_vlans_merged(self):
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
            "no state active",
            "no shutdown",
            "no mtu 610",
            "name Replace_RemoteIsInMyName",
            "remote-span",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_replaced_idempotent(self):
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
        set_module_args(dict(config=[dict(vlan_id=150)], state="deleted"))
        result = self.execute_module(changed=True)
        commands = ["no vlan 150"]
        self.assertEqual(result["commands"], commands)

    def test_vlans_rendered(self):
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
