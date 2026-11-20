# (c) 2026 Red Hat Inc.
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

from ansible_collections.cisco.ios.plugins.modules import ios_track_objects
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


RUNNING = dedent(
    """\
    track 1 ip sla 1 state
     delay down 120 up 180
    track 2 ip route 192.0.2.0 255.255.255.240 reachability
     ip vrf MGMT
     delay down 10 up 5
    track 3 interface GigabitEthernet1 line-protocol
    track 10 list boolean and
     object 1
     object 2 not
     delay down 10
    """,
)


class TestIosTrackObjectsModule(TestIosModule):
    module = ios_track_objects

    def setUp(self):
        super(TestIosTrackObjectsModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.track_objects.track_objects."
            "Track_objectsFacts.get_track_objects_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosTrackObjectsModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True, failed=False):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def test_ios_track_objects_merged(self):
        result = self._run(
            "",
            {
                "config": [
                    {
                        "object_id": 1,
                        "ip_sla": {"operation_id": 1, "parameter": "state"},
                        "delay": {"down": 120, "up": 180},
                    },
                    {
                        "object_id": 2,
                        "ip_route": {"prefix": "192.0.2.0/28", "vrf": "MGMT"},
                        "delay": {"down": 10, "up": 5},
                    },
                    {"object_id": 3, "interface": {"name": "Gi1", "parameter": "line_protocol"}},
                    {"object_id": 4, "interface": {"name": "Gi2", "parameter": "ip_routing"}},
                    {
                        "object_id": 10,
                        "boolean_list": {
                            "operator": "and",
                            "objects": [{"object_id": 1}, {"object_id": 2, "negate": True}],
                        },
                        "delay": {"down": 10},
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "track 1 ip sla 1 state",
                "delay down 120 up 180",
                "track 2 ip route 192.0.2.0 255.255.255.240 reachability",
                "ip vrf MGMT",
                "delay down 10 up 5",
                "track 3 interface GigabitEthernet1 line-protocol",
                "track 4 interface GigabitEthernet2 ip routing",
                "track 10 list boolean and",
                "object 1",
                "object 2 not",
                "delay down 10",
            ],
        )

    def test_ios_track_objects_merged_idempotent(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 1,
                        "ip_sla": {"operation_id": 1, "parameter": "state"},
                        "delay": {"down": 120, "up": 180},
                    },
                    {
                        "object_id": 2,
                        "ip_route": {"prefix": "192.0.2.0/28", "vrf": "MGMT"},
                        "delay": {"down": 10, "up": 5},
                    },
                    {"object_id": 3, "interface": {"name": "Gi1", "parameter": "line_protocol"}},
                    {
                        "object_id": 10,
                        "boolean_list": {
                            "operator": "and",
                            "objects": [{"object_id": 2, "negate": True}, {"object_id": 1}],
                        },
                        "delay": {"down": 10},
                    },
                ],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_track_objects_merged_keeps_what_is_not_in_the_task(self):
        # only the up delay is given: type, vrf and the down delay stay
        result = self._run(
            RUNNING,
            {"config": [{"object_id": 2, "delay": {"up": 20}}], "state": "merged"},
        )
        self.assertEqual(result["commands"], ["track 2", "delay down 10 up 20"])

    def test_ios_track_objects_merged_adds_list_member_keeps_others(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 10,
                        "boolean_list": {"operator": "and", "objects": [{"object_id": 3}]},
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["track 10", "object 3"])

    def test_ios_track_objects_merged_negate_flip_of_member(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 10,
                        "boolean_list": {
                            "operator": "and",
                            "objects": [{"object_id": 1, "negate": True}],
                        },
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["track 10", "object 1 not"])

    def test_ios_track_objects_merged_new_object_needs_a_type(self):
        result = self._run(
            "",
            {"config": [{"object_id": 7, "delay": {"up": 5}}], "state": "merged"},
            failed=True,
        )
        self.assertIn("tracked object 7", result["msg"])

    def test_ios_track_objects_replaced_drops_what_is_not_in_the_task(self):
        # delay down is dropped: IOS keeps it on "delay up", so it is cleared first
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 2,
                        "ip_route": {"prefix": "192.0.2.0/28"},
                        "delay": {"up": 5},
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(
            result["commands"],
            ["track 2", "no ip vrf MGMT", "no delay", "delay up 5"],
        )

    def test_ios_track_objects_replaced_removes_list_members_and_delay(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 10,
                        "boolean_list": {"operator": "and", "objects": [{"object_id": 1}]},
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(result["commands"], ["track 10", "no object 2", "no delay"])

    def test_ios_track_objects_replaced_idempotent(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 1,
                        "ip_sla": {"operation_id": 1, "parameter": "state"},
                        "delay": {"down": 120, "up": 180},
                    },
                ],
                "state": "replaced",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_track_objects_replaced_changes_tracked_thing_in_place(self):
        # same kind: IOS changes it in place and keeps the delay
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 1,
                        "ip_sla": {"operation_id": 2, "parameter": "reachability"},
                        "delay": {"down": 120, "up": 180},
                    },
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(result["commands"], ["track 1 ip sla 2 reachability"])

    def test_ios_track_objects_replaced_recreates_when_kind_changes(self):
        # IOS: "Cannot change tracked object 3 - delete old config first"
        result = self._run(
            RUNNING,
            {
                "config": [
                    {"object_id": 3, "ip_sla": {"operation_id": 3, "parameter": "reachability"}},
                ],
                "state": "replaced",
            },
        )
        self.assertEqual(result["commands"], ["no track 3", "track 3 ip sla 3 reachability"])

    def test_ios_track_objects_replaced_without_type_fails(self):
        result = self._run(
            RUNNING,
            {"config": [{"object_id": 1}], "state": "replaced"},
            failed=True,
        )
        self.assertIn("state replaced", result["msg"])

    def test_ios_track_objects_overridden(self):
        result = self._run(
            RUNNING,
            {
                "config": [
                    {
                        "object_id": 1,
                        "ip_sla": {"operation_id": 1, "parameter": "state"},
                        "delay": {"down": 120, "up": 180},
                    },
                ],
                "state": "overridden",
            },
        )
        self.assertEqual(result["commands"], ["no track 2", "no track 3", "no track 10"])

    def test_ios_track_objects_deleted_object(self):
        result = self._run(
            RUNNING,
            {"config": [{"object_id": 3}, {"object_id": 99}], "state": "deleted"},
        )
        self.assertEqual(result["commands"], ["no track 3"])

    def test_ios_track_objects_deleted_all(self):
        result = self._run(RUNNING, {"state": "deleted"})
        self.assertEqual(
            result["commands"],
            ["no track 1", "no track 2", "no track 3", "no track 10"],
        )

    def test_ios_track_objects_deleted_all_empty_device(self):
        result = self._run("", {"state": "deleted"}, changed=False)
        self.assertEqual(result["commands"], [])

    def test_ios_track_objects_rendered(self):
        set_module_args(
            {
                "config": [
                    {
                        "object_id": 3,
                        "interface": {"name": "GigabitEthernet1", "parameter": "line_protocol"},
                    },
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], ["track 3 interface GigabitEthernet1 line-protocol"])

    def test_ios_track_objects_parsed(self):
        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "object_id": 1,
                    "ip_sla": {"operation_id": 1, "parameter": "state"},
                    "delay": {"down": 120, "up": 180},
                },
                {
                    "object_id": 2,
                    "ip_route": {"prefix": "192.0.2.0/28", "vrf": "MGMT"},
                    "delay": {"down": 10, "up": 5},
                },
                {
                    "object_id": 3,
                    "interface": {"name": "GigabitEthernet1", "parameter": "line_protocol"},
                },
                {
                    "object_id": 10,
                    "boolean_list": {
                        "operator": "and",
                        "objects": [
                            {"object_id": 1, "negate": False},
                            {"object_id": 2, "negate": True},
                        ],
                    },
                    "delay": {"down": 10},
                },
            ],
        )

    def test_ios_track_objects_parsed_prefix_length_and_delay_variants(self):
        set_module_args(
            {
                "running_config": dedent(
                    """\
                    track 5 ip route 198.51.100.0/24 reachability
                     delay up 10
                    track 6 interface Tunnel1 ip routing
                     delay down 20
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {"object_id": 5, "ip_route": {"prefix": "198.51.100.0/24"}, "delay": {"up": 10}},
                {
                    "object_id": 6,
                    "interface": {"name": "Tunnel1", "parameter": "ip_routing"},
                    "delay": {"down": 20},
                },
            ],
        )

    def test_ios_track_objects_gathered_ignores_unsupported_objects(self):
        self.execute_show_command.return_value = dedent(
            """\
            track timer interface 5
            track 4 ip route 192.0.2.0 255.255.255.0 metric threshold
             delay down 30
            track 5 list threshold weight
             object 1 weight 10
            track 6 ip sla 6 state
             delay up 15
            """,
        )
        set_module_args({"state": "gathered"})
        with patch.object(ios_track_objects.AnsibleModule, "warn") as warn:
            result = self.execute_module(changed=False)
        # the delay of object 4 must not end up on object 6, nor the member of object 5 anywhere
        self.assertEqual(
            result["gathered"],
            [
                {
                    "object_id": 6,
                    "ip_sla": {"operation_id": 6, "parameter": "state"},
                    "delay": {"up": 15},
                },
            ],
        )
        warn.assert_called_once()
        self.assertIn("4, 5", warn.call_args[0][0])

    def test_ios_track_objects_unsupported_object_is_not_overridden(self):
        result = self._run(
            "track 4 ip route 192.0.2.0 255.255.255.0 metric threshold\n",
            {
                "config": [{"object_id": 1, "ip_sla": {"operation_id": 1, "parameter": "state"}}],
                "state": "overridden",
            },
        )
        self.assertEqual(result["commands"], ["track 1 ip sla 1 state"])
