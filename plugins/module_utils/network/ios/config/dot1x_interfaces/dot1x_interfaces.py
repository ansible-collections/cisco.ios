# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_dot1x_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.dot1x_interfaces import (
    Dot1x_interfacesTemplate,
    server_dead_lines,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


# in the order the device prints them, "event_server_dead" is compared line by line
PARSERS = (
    "port_control",
    "periodic",
    "reauthenticate",
    "violation",
    "control_direction",
    "host_mode",
    "order",
    "priority",
    "event_fail",
    "event_no_response",
    "event_server_dead",
    "event_server_alive",
    "mab",
    "dot1x_pae",
    "dot1x_tx_period",
    "dot1x_max_reauth_req",
)

# IOS does not print what is the default: a port without the line has the default, and the default in a
# task is not a change. parser: (where it is in the config, the default)
DEFAULTS = {
    "port_control": (("authentication", "port_control"), "force_authorized"),
    "reauthenticate": (("authentication", "timer", "reauthenticate"), {"seconds": 3600}),
    "violation": (("authentication", "violation"), "shutdown"),
    "control_direction": (("authentication", "control_direction"), "both"),
    "host_mode": (("authentication", "host_mode"), "single_host"),
    "dot1x_tx_period": (("dot1x", "timeout", "tx_period"), 30),
    "dot1x_max_reauth_req": (("dot1x", "max_reauth_req"), 2),
}
SERVER_DEAD = ("authentication", "event", "server_dead")
FAIL = ("authentication", "event", "fail")
DEFAULT_RETRY = 2

# One command line each: a new value replaces the line, it is not merged with the old one
ATOMIC = (
    ("authentication", "timer", "reauthenticate"),
    ("authentication", "order"),
    ("authentication", "priority"),
    FAIL,
    ("authentication", "event", "no_response"),
    ("authentication", "event", "server_alive"),
)


def _get(data, path):
    for key in path:
        if not isinstance(data, dict) or data.get(key) is None:
            return None
        data = data[key]
    return data


def _set(data, path, value):
    for key in path[:-1]:
        data = data.setdefault(key, {})
    data[path[-1]] = value


class Dot1x_interfaces(ResourceModule):
    """
    The ios_dot1x_interfaces config class
    """

    def __init__(self, module):
        super(Dot1x_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="dot1x_interfaces",
            tmplt=Dot1x_interfacesTemplate(),
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
        wantd = self._by_name(self.want, validate=True)
        haved = self._by_name(self.have)

        if self.state == "deleted":
            # without config: every interface that has options
            for name in wantd or haved:
                if name in haved:
                    self._compare({"name": name}, haved[name])
            return

        if self.state == "overridden":
            for name, have in haved.items():
                if name not in wantd:
                    self._compare({"name": name}, have)

        # keep the order of the task, it makes the commands deterministic
        for name, want in wantd.items():
            have = haved.get(name, {})
            if self.state == "merged" and have:
                want = self._merge(want, have)
            self._compare(want, have)

    def _by_name(self, interfaces, validate=False):
        result = {}
        for item in deepcopy(interfaces) or []:
            # "Gi1/0/1" in the task and "GigabitEthernet1/0/1" on the device are the same interface
            item["name"] = normalize_interface(item["name"])
            if validate:
                self._validate(item)
            fail = _get(item, FAIL)
            if fail and fail.get("retry") == DEFAULT_RETRY:
                # IOS does not print "retry 2"
                del fail["retry"]
            result[item["name"]] = item
        return result

    @staticmethod
    def _merge(want, have):
        """Merge want onto have, a command line that is in want replaces the one of have."""
        merged = dict_merge(have, want)
        for path in ATOMIC:
            value = _get(want, path)
            if value is not None:
                _set(merged, path, value)
        return merged

    def _validate(self, item):
        """The combinations IOS refuses."""
        name = item["name"]
        event = (item.get("authentication") or {}).get("event") or {}
        timer = ((item.get("authentication") or {}).get("timer") or {}).get("reauthenticate")
        problem = None
        fail = event.get("fail")
        dead = event.get("server_dead")
        if timer is not None and bool(timer.get("server")) == (timer.get("seconds") is not None):
            problem = "authentication.timer.reauthenticate needs either server or seconds"
        elif fail and fail.get("action") == "authorize" and fail.get("vlan") is None:
            problem = "authentication.event.fail with action authorize needs a vlan"
        elif fail and fail.get("action") == "next_method" and fail.get("vlan") is not None:
            problem = "authentication.event.fail with action next_method does not take a vlan"
        elif fail and fail.get("action") is None:
            problem = "authentication.event.fail needs an action"
        elif (
            dead
            and dead.get("action") == "reinitialize"
            and (dead.get("vlan") is None or dead.get("voice"))
        ):
            problem = "authentication.event.server_dead with action reinitialize needs a vlan and takes no voice"
        elif (
            dead
            and dead.get("action") == "authorize"
            and dead.get("vlan") is None
            and not dead.get("voice")
        ):
            problem = "authentication.event.server_dead with action authorize needs a vlan or voice"
        elif dead and dead.get("action") is None:
            problem = "authentication.event.server_dead needs an action"
        elif event.get("no_response") and event["no_response"].get("vlan") is None:
            problem = "authentication.event.no_response needs a vlan"
        if problem:
            self._module.fail_json(msg="%s: %s." % (name, problem))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Dot1x_interfaces network resource.
        """
        begin = len(self.commands)

        want_fail, have_fail = _get(want, FAIL), _get(have, FAIL)
        if (
            want_fail
            and have_fail
            and "retry" not in want_fail
            and have_fail.get("retry") not in (None, DEFAULT_RETRY)
        ):
            # the retry that is on the port has to be set back, not printed means 2
            want = deepcopy(want)
            _get(want, FAIL)["retry"] = DEFAULT_RETRY

        for parser in PARSERS:
            if parser == "event_server_dead":
                self._compare_server_dead(want, have)
            elif parser in DEFAULTS:
                self._compare_default(parser, want, have)
            else:
                self.compare(parsers=[parser], want=want, have=have)

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want, "name", False))

    def _compare_default(self, parser, want, have):
        """An option with a default: the port without the line has the default."""
        path, default = DEFAULTS[parser]
        want_value, have_value = _get(want, path), _get(have, path)
        if want_value is None:
            # not wanted: back to the default
            if have_value is not None and have_value != default:
                self.addcmd(have, parser, True)
        elif want_value != (have_value if have_value is not None else default):
            self.addcmd(want, parser, False)

    def _compare_server_dead(self, want, have):
        """The vlan and the voice domain of "server dead" are lines of their own, each one is added or removed.

        The device prints the voice line next to the vlan line without being asked for it. A voice line that
        the task does not mention is therefore left alone as long as the task has the vlan, and it goes with
        the vlan when the task has no "server dead" at all or says voice: false.
        """
        want_dead = _get(want, SERVER_DEAD)
        have_dead = _get(have, SERVER_DEAD)
        want_lines = server_dead_lines(want_dead or {})
        have_lines = server_dead_lines(have_dead or {})
        voice_line = "authentication event server dead action authorize voice"
        keep_voice = (
            bool(want_dead) and want_dead.get("vlan") is not None and want_dead.get("voice") is None
        )
        for line in have_lines:
            if line not in want_lines and not (line == voice_line and keep_voice):
                self.commands.append("no " + line)
        for line in want_lines:
            if line not in have_lines:
                self.commands.append(line)
