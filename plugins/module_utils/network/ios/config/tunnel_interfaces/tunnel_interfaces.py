# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_tunnel_interfaces config file.
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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.tunnel_interfaces import (
    Tunnel_interfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
)


DEFAULTS = {"mode": "gre_ip", "ttl": 255}


def _address_or(value, fallback):
    """An IP address in its canonical form (the device prints 2001:DB8::1), or what fallback makes of the value."""
    try:
        return ip_address(value).compressed
    except ValueError:
        return fallback(value)


class Tunnel_interfaces(ResourceModule):
    """
    The ios_tunnel_interfaces config class
    """

    def __init__(self, module):
        super(Tunnel_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="tunnel_interfaces",
            tmplt=Tunnel_interfacesTemplate(),
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
        wantd = self._by_name(self.want, check=True)
        haved = self._by_name(self.have)

        if self.state == "deleted":
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
            self._compare(want, haved.get(name, {}))

    def _by_name(self, interfaces, check=False):
        result = {}
        for item in deepcopy(interfaces) or []:
            # "Tu1501" in the task and "Tunnel1501" on the device are the same interface
            item["name"] = normalize_interface(item["name"])
            if check and not item["name"].startswith("Tunnel"):
                self._module.fail_json(msg="%s is not a tunnel interface." % item["name"])
            # "Gi1" and "GigabitEthernet1", "2001:DB8::1" and "2001:db8::1" are the same
            if item.get("source"):
                item["source"] = _address_or(item["source"], normalize_interface)
            if item.get("destination"):
                item["destination"] = _address_or(item["destination"], str)
            result[item["name"]] = item
        return result

    def _compare(self, want, have):
        begin = len(self.commands)

        given_destination = want.get("destination")
        if self.state == "merged" and have:
            want = dict_merge(have, {k: v for k, v in want.items() if v is not None})
        if want.get("mode") == "gre_multipoint":
            if given_destination:
                self._module.fail_json(
                    msg="%s: a destination cannot be set with mode gre_multipoint, IOS refuses it."
                    % want["name"],
                )
            # IOS refuses the mode while a destination is set, the one on the device is removed
            want.pop("destination", None)

        if want.get("mode") == "gre_multipoint":
            # the destination has to go before the mode is switched
            self.compare(parsers=["destination"], want=want, have=have)
            self._compare_default("mode", want, have)
            self.compare(parsers=["source"], want=want, have=have)
        else:
            self._compare_default("mode", want, have)
            self.compare(parsers=["source", "destination"], want=want, have=have)
        self.compare(parsers=["key", "tunnel_vrf"], want=want, have=have)
        self._compare_default("ttl", want, have)
        self.compare(parsers=["checksum", "path_mtu_discovery"], want=want, have=have)

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def _compare_default(self, key, want, have):
        """mode and ttl: IOS does not print the default, so a tunnel without the line has the default."""
        default = DEFAULTS[key]
        want_value, have_value = want.get(key), have.get(key)
        if want_value is None:
            # not wanted: back to the default
            if have_value is not None and have_value != default:
                self.addcmd(have, key, True)
        elif want_value != (have_value if have_value is not None else default):
            self.addcmd(want, key, False)
