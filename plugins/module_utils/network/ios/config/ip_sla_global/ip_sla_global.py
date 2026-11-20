# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_ip_sla_global config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ip_sla_global import (
    Ip_sla_globalTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


OP_TYPES = ("icmp_echo", "tcp_connect", "http")
OPTIONS = (
    "vrf",
    "frequency",
    "threshold",
    "timeout",
    "tag",
    "owner",
    "request_data_size",
    "tos",
)
GLOBAL_PARSERS = ("logging_traps", "enable_reaction_alerts")
DEFAULT_THRESHOLD = 5000
DEFAULT_TIMEOUT = 5000
DEFAULT_FREQUENCY = 60


def _op_type(op):
    """The operation type key (icmp_echo, tcp_connect, http) set in an operation, if any."""
    for key in OP_TYPES:
        if op.get(key):
            return key
    return None


class Ip_sla_global(ResourceModule):
    """
    The ios_ip_sla_global config class
    """

    def __init__(self, module):
        super(Ip_sla_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ip_sla_global",
            tmplt=Ip_sla_globalTemplate(),
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
        want = deepcopy(self.want) or {}
        have = deepcopy(self.have) or {}
        # "Gi1" in the task and "GigabitEthernet1" on the device are the same interface
        for ops in (want.get("operations", []), have.get("operations", [])):
            for op in ops:
                icmp = op.get("icmp_echo")
                if icmp and icmp.get("source_interface"):
                    icmp["source_interface"] = normalize_interface(icmp["source_interface"])
                # IOS does not print the default life of 3600 seconds
                if op.get("schedule") and not op["schedule"].get("life"):
                    op["schedule"]["life"] = "3600"
        wanted_ops = {op["operation_id"]: op for op in want.get("operations", [])}
        haved_ops = {op["operation_id"]: op for op in have.get("operations", [])}

        if self.state == "deleted":
            self._deleted(want, have, wanted_ops, haved_ops)
            return

        self._compare_globals(want, have)

        if self.state == "overridden":
            for op_id in haved_ops:
                if op_id not in wanted_ops:
                    self.commands.append(
                        self._tmplt.render({"operation_id": op_id}, "operation_id", True),
                    )

        # keep the order of the task, it makes the commands deterministic
        for op_id, wop in wanted_ops.items():
            self._compare_operation(wop, haved_ops.get(op_id, {}))

    def _deleted(self, want, have, wanted_ops, haved_ops):
        if wanted_ops:
            for op_id in wanted_ops:
                if op_id in haved_ops:
                    self.commands.append(
                        self._tmplt.render({"operation_id": op_id}, "operation_id", True),
                    )
            for parser in GLOBAL_PARSERS:
                if want.get(parser) and have.get(parser):
                    self.addcmd(have, parser, True)
            return
        for parser in GLOBAL_PARSERS:
            if have.get(parser):
                self.addcmd(have, parser, True)
        for op_id in haved_ops:
            self.commands.append(self._tmplt.render({"operation_id": op_id}, "operation_id", True))

    def _compare_globals(self, want, have):
        wanted = {k: want.get(k) for k in GLOBAL_PARSERS}
        if self.state == "merged":
            # an option that is not in the task is not touched
            wanted = {k: (v if v is not None else have.get(k)) for k, v in wanted.items()}
        self.compare(parsers=list(GLOBAL_PARSERS), want=wanted, have=have)

    def _compare_operation(self, want, have):
        """Generate the commands of one operation.

        IOS does not allow to edit an operation that is scheduled, and it does not allow to change
        what the type line (destination, URL, source) or to drop the raw request: the operation is
        removed and created again in those cases. Other changes to a scheduled operation are made by
        removing the schedule first and adding it back afterwards.
        """
        op_id = want["operation_id"]
        if self.state == "merged":
            want = self._merge_operation(want, have)
        want_type, have_type = _op_type(want), _op_type(have)
        self._validate_schedule(want)

        begin = len(self.commands)
        recreate = False
        if have and have_type and (want_type or self.state != "merged"):
            recreate = (
                want_type != have_type
                or self._type_line(want) != self._type_line(have)
                or (self._raw_request(have) and not self._raw_request(want))
            )
        if recreate:
            self.commands.append(self._tmplt.render(have, "operation_id", True))
            have = {"operation_id": op_id}
            begin = len(self.commands)

        # operation type line, then the options below it; the raw request is a block of its own
        for key in OP_TYPES:
            self.compare(
                parsers=[key],
                want=self._without_raw_request(want),
                have=self._without_raw_request(have),
            )
        self._compare_raw_request(want, have)
        self.compare(parsers=list(OPTIONS), want=want, have=have)

        changed = len(self.commands) != begin
        if changed or not have:
            self.commands.insert(begin, self._tmplt.render(want, "operation_id", False))

        have_sched = have.get("schedule")
        if changed and have_sched:
            # the operation is running, it has to be stopped for the changes above
            self.commands.insert(
                begin,
                self._tmplt.render({"operation_id": op_id}, "schedule", True),
            )
            have_sched = None
        self._compare_schedule(want, have_sched)

    def _validate_schedule(self, op):
        """IOS refuses to schedule an operation unless threshold <= timeout <= frequency.

        The message starts with "%" and no space, which the terminal plugin does not treat as an error:
        without this check the schedule would silently be missing and every run would try again.
        """
        if not op.get("schedule"):
            return
        threshold = op.get("threshold", DEFAULT_THRESHOLD)
        timeout = op.get("timeout", DEFAULT_TIMEOUT)
        frequency = op.get("frequency", DEFAULT_FREQUENCY)
        problem = None
        if threshold > timeout:
            problem = "the threshold of %s ms is greater than the timeout of %s ms" % (
                threshold,
                timeout,
            )
        elif timeout > frequency * 1000:
            problem = "the timeout of %s ms is greater than the frequency of %s s" % (
                timeout,
                frequency,
            )
        if problem:
            self._module.fail_json(
                msg="ip sla %s cannot be scheduled, %s (IOS defaults: threshold %s ms, timeout %s ms, frequency %s s)."
                % (
                    op["operation_id"],
                    problem,
                    DEFAULT_THRESHOLD,
                    DEFAULT_TIMEOUT,
                    DEFAULT_FREQUENCY,
                ),
            )

    @staticmethod
    def _type_line(op):
        """What the type line holds, it cannot be changed on a device."""
        key = _op_type(op)
        value = dict(op.get(key) or {})
        value.pop("raw_request", None)
        return key, value

    @staticmethod
    def _raw_request(op):
        return (op.get("http") or {}).get("raw_request")

    @staticmethod
    def _without_raw_request(op):
        http = op.get("http")
        if not http or "raw_request" not in http:
            return op
        return {**op, "http": {k: v for k, v in http.items() if k != "raw_request"}}

    def _merge_operation(self, want, have):
        """Merge want onto have. A new operation type in want replaces the one of have."""
        base = {
            k: v
            for k, v in have.items()
            if not (_op_type(want) and k in OP_TYPES and k != _op_type(want))
        }
        return dict_merge(base, want)

    def _compare_raw_request(self, want, have):
        """The http raw request lives in its own submode: http-raw-request / <payload> / exit.

        A request that differs is replaced in place. Dropping it is a recreate of the operation.
        """
        want_req = self._raw_request(want)
        if want_req and want_req != self._raw_request(have):
            self.commands.extend(["http-raw-request", want_req, "exit"])

    def _compare_schedule(self, want, have_sched):
        op_id = want["operation_id"]
        want_sched = want.get("schedule")
        if self.state == "merged" and want_sched and have_sched:
            want_sched = dict_merge(have_sched, want_sched)
        if want_sched == have_sched:
            return
        data = {"operation_id": op_id}
        if have_sched:
            # a scheduled operation cannot be rescheduled in place
            self.commands.append(self._tmplt.render(data, "schedule", True))
        if want_sched:
            data["schedule"] = want_sched
            self.commands.append(self._tmplt.render(data, "schedule", False))
