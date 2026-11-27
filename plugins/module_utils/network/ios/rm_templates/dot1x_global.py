# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Dot1x_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Dot1x_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Dot1x_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "system_auth_control",
            "getval": re.compile(r"^dot1x\ssystem-auth-control$"),
            "setval": "dot1x system-auth-control",
            "result": {"system_auth_control": True},
        },
        {
            # "dot1x critical eapol block" is another command
            "name": "critical_eapol",
            "getval": re.compile(r"^dot1x\scritical\seapol$"),
            "setval": "dot1x critical eapol",
            "result": {"critical_eapol": True},
        },
        {
            "name": "auth_fail_eapol",
            "getval": re.compile(r"^dot1x\sauth-fail\seapol$"),
            "setval": "dot1x auth-fail eapol",
            "result": {"auth_fail_eapol": True},
        },
        {
            # IOS prints "authentication mac-move deny" when neither of the two is set, that line is not an option
            "name": "mac_move_permit",
            "getval": re.compile(r"^authentication\smac-move\spermit$"),
            "setval": "authentication mac-move permit",
            "compval": "authentication.mac_move.permit",
            "result": {"authentication": {"mac_move": {"permit": True}}},
        },
        {
            "name": "mac_move_deny_uncontrolled",
            "getval": re.compile(r"^authentication\smac-move\sdeny-uncontrolled$"),
            "setval": "authentication mac-move deny-uncontrolled",
            "compval": "authentication.mac_move.deny_uncontrolled",
            "result": {"authentication": {"mac_move": {"deny_uncontrolled": True}}},
        },
        {
            "name": "critical_recovery_delay",
            "getval": re.compile(r"^authentication\scritical\srecovery\sdelay\s(?P<delay>\d+)$"),
            "setval": "authentication critical recovery delay {{ authentication.critical_recovery_delay }}",
            "compval": "authentication.critical_recovery_delay",
            "result": {"authentication": {"critical_recovery_delay": "{{ delay | int }}"}},
        },
    ]
    # fmt: on
