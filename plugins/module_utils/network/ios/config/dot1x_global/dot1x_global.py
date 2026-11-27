# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_dot1x_global config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.dot1x_global import (
    Dot1x_globalTemplate,
)


# what a device has when nothing is configured, "show running-config all" prints the values
DEFAULTS = {
    "system_auth_control": False,
    "critical_eapol": False,
    "auth_fail_eapol": False,
    "authentication": {
        "mac_move": {"permit": False, "deny_uncontrolled": False},
        "critical_recovery_delay": 100,
    },
}


class Dot1x_global(ResourceModule):
    """
    The ios_dot1x_global config class
    """

    def __init__(self, module):
        super(Dot1x_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="dot1x_global",
            tmplt=Dot1x_globalTemplate(),
        )
        # 802.1X is switched on last, once the options it uses are in place
        self.parsers = [
            "auth_fail_eapol",
            "critical_eapol",
            "mac_move_permit",
            "mac_move_deny_uncontrolled",
            "critical_recovery_delay",
            "system_auth_control",
        ]

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

        if self.state == "merged":
            want = dict_merge(have, want)
        elif self.state in ["replaced", "overridden"]:
            # what the task does not say goes back to its default
            want = dict_merge(deepcopy(DEFAULTS), want)
        elif self.state == "deleted":
            want = deepcopy(DEFAULTS)

        self.compare(parsers=self.parsers, want=want, have=have)
