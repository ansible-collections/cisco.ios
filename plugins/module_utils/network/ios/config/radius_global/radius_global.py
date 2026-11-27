# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_radius_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy
from ipaddress import ip_address

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.radius_global import (
    Radius_globalTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


# IOS does not print what is set to its default, a missing line is the default
SCALAR_DEFAULTS = {"timeout": 5, "retransmit": 3, "deadtime": 0}
DEAD_CRITERIA_DEFAULT = {"time": 10, "tries": 10}
PORT_DEFAULTS = {"auth_port": 1812, "acct_port": 1813}
ATTRIBUTE_OPTIONS = (
    "on_for_login_auth",
    "access_request_include",
    "include_in_access_req",
    "include_in_acct_req",
)
# attributes that IOS sends by default, "no radius-server attribute 77 ..." is printed when they are off
ON_BY_DEFAULT = {77: ("include_in_access_req", "include_in_acct_req")}
GLOBAL_KEYS = (
    "timeout",
    "retransmit",
    "deadtime",
    "dead_criteria",
    "load_balance",
    "source_interface",
)


class Radius_global(ResourceModule):
    """
    The ios_radius_global config class
    """

    def __init__(self, module):
        super(Radius_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="radius_global",
            tmplt=Radius_globalTemplate(),
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
        want = self._prepare(self.want)
        have = self._prepare(self.have)
        wservers, hservers = want.pop("servers"), have.pop("servers")
        wattrs, hattrs = want.pop("attributes"), have.pop("attributes")

        if self.state == "deleted":
            self._deleted(want, have, wservers, hservers, wattrs, hattrs)
            return

        self._globals(want, have)
        self._attributes(wattrs, hattrs)

        if self.state == "overridden":
            for name in hservers:
                if name not in wservers:
                    self.addcmd({"name": name}, "server", True)
        # keep the order of the task, it makes the commands deterministic
        for name, server in wservers.items():
            self._server(server, hservers.get(name, {}))

    def _prepare(self, config):
        """Servers and attributes as dicts, interface names in their full form."""
        config = deepcopy(config) or {}
        config["servers"] = {server["name"]: server for server in config.get("servers", [])}
        config["attributes"] = {attr["number"]: attr for attr in config.get("attributes", [])}
        source = config.get("source_interface")
        if source:
            source["name"] = normalize_interface(source["name"])
        for number, attr in config["attributes"].items():
            for option in ON_BY_DEFAULT.get(number, ()):
                if attr.get(option) is False:
                    self._module.fail_json(
                        msg="attribute %s is sent by default, %s cannot be switched off with this module."
                        % (number, option),
                    )
        return config

    # ------------------------------------------------------------------ global options
    def _globals(self, want, have):
        wanted = {key: want.get(key) for key in GLOBAL_KEYS}
        if self.state == "merged":
            # an option that is not in the task is not touched
            wanted = {
                key: (value if value is not None else have.get(key))
                for key, value in wanted.items()
            }
        for key in SCALAR_DEFAULTS:
            self._compare_scalar(key, wanted, have)
        self._compare_dead_criteria(wanted.get("dead_criteria"), have.get("dead_criteria"))
        self.compare(parsers=["load_balance", "source_interface"], want=wanted, have=have)

    def _compare_scalar(self, key, want, have):
        default = SCALAR_DEFAULTS[key]
        want_value, have_value = want.get(key), have.get(key)
        if want_value is None:
            # not wanted: back to the default
            if have_value is not None and have_value != default:
                self.addcmd(have, key, True)
        elif want_value != (have_value if have_value is not None else default):
            if want_value == default:
                # "radius-server deadtime 0" is invalid input, the bare "no" form is the way back to the default
                self.addcmd(have, key, True)
            else:
                self.addcmd(want, key, False)

    def _compare_dead_criteria(self, want, have):
        effective_have = dict(DEAD_CRITERIA_DEFAULT, **(have or {}))
        if want is None:
            if effective_have != DEAD_CRITERIA_DEFAULT:
                self.addcmd({"dead_criteria": effective_have}, "dead_criteria", True)
            return
        effective_want = dict(
            DEAD_CRITERIA_DEFAULT,
            **{k: v for k, v in want.items() if v is not None},
        )
        if self.state == "merged":
            effective_want = dict(
                effective_have,
                **{k: v for k, v in want.items() if v is not None},
            )
        if effective_want == effective_have:
            return
        if effective_want == DEAD_CRITERIA_DEFAULT:
            self.addcmd({"dead_criteria": effective_have}, "dead_criteria", True)
        else:
            self.addcmd({"dead_criteria": effective_want}, "dead_criteria", False)

    # ------------------------------------------------------------------ attributes
    def _attributes(self, wattrs, hattrs):
        numbers = list(wattrs)
        if self.state in ("replaced", "overridden"):
            numbers += [number for number in hattrs if number not in wattrs]
        for number in numbers:
            have = dict(hattrs.get(number, {}), number=number)
            want = dict(wattrs.get(number, {}), number=number)
            if self.state == "merged":
                # an option that is not in the task is not touched
                want = dict(
                    have,
                    **{key: value for key, value in want.items() if value is not None},
                )
            for option in ATTRIBUTE_OPTIONS:
                self.compare(parsers=["attribute_" + option], want=want, have=have)

    # ------------------------------------------------------------------ servers
    def _server(self, want, have):
        name = want["name"]
        begin = len(self.commands)
        want_address = want.get("address")
        if not have and not (
            want_address and (want_address.get("ipv4") or want_address.get("ipv6"))
        ):
            self._module.fail_json(
                msg="The address (ipv4 or ipv6) of the new radius server %s is required." % name,
            )

        self._compare_address(name, want_address, have.get("address"))
        self._compare_key(name, want.get("key"), have.get("key"))

        wanted = dict(want, name=name)
        if self.state == "merged":
            wanted = {
                key: (want.get(key) if want.get(key) is not None else have.get(key))
                for key in ("timeout", "retransmit")
            }
            wanted["name"] = name
        self.compare(parsers=["server_timeout", "server_retransmit"], want=wanted, have=have)

        if len(self.commands) != begin or not have:
            self.commands.insert(begin, self._tmplt.render({"name": name}, "server", False))

    def _compare_address(self, name, want, have):
        if not want:
            return
        have = have or {}
        want = dict(want)
        if self.state == "merged" and have:
            # what the task does not say stays as on the device, a family of the task replaces the other one
            families = [family for family in ("ipv4", "ipv6") if want.get(family)]
            family = families[0] if families else ("ipv4" if have.get("ipv4") else "ipv6")
            merged = {key: value for key, value in have.items() if key in PORT_DEFAULTS}
            merged[family] = want.get(family) or have.get(family)
            merged.update(
                {
                    key: value
                    for key, value in want.items()
                    if key in PORT_DEFAULTS and value is not None
                },
            )
            want = merged

        def effective(address):
            return {
                "ipv4": self._host((address or {}).get("ipv4")),
                "ipv6": self._host((address or {}).get("ipv6")),
                "auth_port": (address or {}).get("auth_port", PORT_DEFAULTS["auth_port"]),
                "acct_port": (address or {}).get("acct_port", PORT_DEFAULTS["acct_port"]),
            }

        if effective(want) != effective(have):
            self.addcmd({"address": want}, "server_address", False)

    @staticmethod
    def _host(host):
        """An IP address as an address, IOS prints 2001:DB8::10 for 2001:db8::10, a host name in lower case."""
        if not host:
            return host
        try:
            return ip_address(host).compressed
        except ValueError:
            return host.lower()

    def _compare_key(self, name, want, have):
        """IOS prints the key encrypted: a clear text key cannot be compared, it is only sent when there is none."""
        if want:
            if have is None:
                self.addcmd({"key": want}, "server_key", False)
            elif want.get("type", 0) != 0 and (want["type"], want["value"]) != (
                have["type"],
                have["value"],
            ):
                self.addcmd({"key": want}, "server_key", False)
        elif have is not None and self.state in ("replaced", "overridden"):
            self.addcmd({"key": have}, "server_key", True)

    # ------------------------------------------------------------------ deleted
    def _deleted(self, want, have, wservers, hservers, wattrs, hattrs):
        everything = not (
            wservers or wattrs or any(want.get(key) is not None for key in GLOBAL_KEYS)
        )
        if everything:
            for name in hservers:
                self.addcmd({"name": name}, "server", True)
        else:
            for name in wservers:
                if name in hservers:
                    self.addcmd({"name": name}, "server", True)
        named = {key: None for key in GLOBAL_KEYS}
        if everything:
            reset_keys = GLOBAL_KEYS
        else:
            reset_keys = [key for key in GLOBAL_KEYS if want.get(key) is not None]
        for key in SCALAR_DEFAULTS:
            if key in reset_keys:
                self._compare_scalar(key, named, have)
        if "dead_criteria" in reset_keys:
            self._compare_dead_criteria(None, have.get("dead_criteria"))
        for key in ("load_balance", "source_interface"):
            if key in reset_keys and have.get(key):
                self.addcmd(have, key, True)
        for number in (hattrs if everything else wattrs):
            if number in hattrs:
                for option in ATTRIBUTE_OPTIONS:
                    if hattrs[number].get(option):
                        self.addcmd(
                            dict(hattrs[number], number=number),
                            "attribute_" + option,
                            True,
                        )
