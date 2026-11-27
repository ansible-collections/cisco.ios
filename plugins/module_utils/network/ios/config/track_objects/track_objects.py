# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_track_objects config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.track_objects import (
    Track_objectsTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


TYPES = ("interface", "ip_sla", "ip_route", "boolean_list")


def _type(obj):
    """The tracked object type (interface, ip_sla, ...) set in an object, if any."""
    for key in TYPES:
        if obj.get(key):
            return key
    return None


class Track_objects(ResourceModule):
    """
    The ios_track_objects config class
    """

    def __init__(self, module):
        super(Track_objects, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="track_objects",
            tmplt=Track_objectsTemplate(),
        )

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self._by_id(self.want)
        haved = self._by_id(self.have)

        if self.state == "deleted":
            for obj_id in wantd or haved:
                if obj_id in haved:
                    self._remove(obj_id)
            return

        if self.state == "overridden":
            for obj_id in haved:
                if obj_id not in wantd:
                    self._remove(obj_id)

        # keep the order of the task, it makes the commands deterministic
        for obj_id, want in wantd.items():
            self._compare_object(want, haved.get(obj_id, {}))

    @staticmethod
    def _by_id(objects):
        result = {}
        for obj in deepcopy(objects) or []:
            # "Gi1" in the task and "GigabitEthernet1" on the device are the same interface
            if obj.get("interface"):
                obj["interface"]["name"] = normalize_interface(obj["interface"]["name"])
            result[obj["object_id"]] = obj
        return result

    def _remove(self, obj_id):
        self.commands.append(self._tmplt.render({"object_id": obj_id}, "object_id", True))

    def _header(self, obj):
        kind = _type(obj)
        return self._tmplt.render(obj, kind, False)

    def _compare_object(self, want, have):
        obj_id = want["object_id"]
        want_type = _type(want)

        if self.state == "merged" and not want_type:
            # nothing says what to track, keep what is on the device
            want = {**have, **{k: v for k, v in want.items() if v}} if have else want
            want_type = _type(want)
        if not want_type:
            reason = "it does not exist on the device" if not have else "with state %s" % self.state
            self._module.fail_json(
                msg="The type of tracked object %s (interface, ip_sla, ip_route or boolean_list) is required, %s."
                % (obj_id, reason),
            )

        begin = len(self.commands)
        if have and _type(have) != want_type:
            # IOS: "Cannot change tracked object - delete old config first"
            self._remove(obj_id)
            have = {}
            begin = len(self.commands)

        if self.state == "merged" and have:
            want = self._merge(want, have)

        # what is tracked is changed in place as long as the kind stays the same
        header_changed = not have or self._header(have) != self._header(want)

        self._compare_route_vrf(want, have)
        self._compare_objects(want, have)
        self._compare_delay(want, have)

        if header_changed:
            self.commands.insert(begin, self._header(want))
        elif len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want, "object_id", False))

    @staticmethod
    def _merge(want, have):
        merged = dict_merge(have, {k: v for k, v in want.items() if k != "boolean_list"})
        if want.get("boolean_list"):
            members = {
                o["object_id"]: o for o in (have.get("boolean_list") or {}).get("objects", [])
            }
            members.update({o["object_id"]: o for o in want["boolean_list"].get("objects", [])})
            merged["boolean_list"] = {
                "operator": want["boolean_list"]["operator"],
                "objects": list(members.values()),
            }
        return merged

    def _compare_route_vrf(self, want, have):
        if want.get("ip_route") or have.get("ip_route"):
            want_vrf = (want.get("ip_route") or {}).get("vrf")
            have_vrf = (have.get("ip_route") or {}).get("vrf")
            if want_vrf != have_vrf:
                if have_vrf:
                    self.addcmd(have, "vrf", True)
                if want_vrf:
                    self.addcmd(want, "vrf", False)

    def _compare_delay(self, want, have):
        want_delay = want.get("delay") or {}
        have_delay = have.get("delay") or {}
        if self.state == "merged":
            want_delay = {**have_delay, **want_delay}
        if want_delay == have_delay:
            return
        if have_delay and any(k not in want_delay for k in have_delay):
            # "delay up 30" does not clear a configured "down", so start from scratch
            self.commands.append(self._tmplt.render(have, "delay", True))
        if want_delay:
            self.commands.append(self._tmplt.render({"delay": want_delay}, "delay", False))

    def _compare_objects(self, want, have):
        want_list = want.get("boolean_list")
        if not want_list:
            return
        want_members = {o["object_id"]: bool(o.get("negate")) for o in want_list.get("objects", [])}
        have_members = {
            o["object_id"]: bool(o.get("negate"))
            for o in (have.get("boolean_list") or {}).get("objects", [])
        }
        for member, negate in have_members.items():
            # a member that stays in the list is changed by adding it again, "object N" replaces "object N not"
            if member not in want_members and self.state != "merged":
                self.commands.append("no object %s" % member)
        for member, negate in want_members.items():
            if have_members.get(member) != negate or member not in have_members:
                self.commands.append(
                    self._tmplt.render(
                        {"member": member, "negate": negate},
                        "boolean_object",
                        False,
                    ),
                )
