# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vlan_configurations parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Vlan_configurationsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vlan_configurationsTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )

    # fmt: off
    PARSERS = [
        {
            "name": "vlan_id",
            "getval": re.compile(
                r"""
                ^vlan\sconfiguration\s(?P<vlan_id>\d+)
<<<<<<< Updated upstream:plugins/module_utils/network/ios/rm_templates/vlan_configuration.py
                $""", re.VERBOSE,
            ),
            "setval": "",
=======
                $""", re.VERBOSE),
            "setval": "vlan configuration {{ vlan_id|string }}",
>>>>>>> Stashed changes:plugins/module_utils/network/ios/rm_templates/vlan_configurations.py
            "result": {
                "{{ vlan_id }}": {
                    "vlan_id": "{{ vlan_id }}",
                },
            },
            "shared": True,
        },
        {
            "name": "member",
            "getval": re.compile(
                r"""
                \s+member
                (\sevpn-instance\s(?P<inst_vlan_id>\d+))?
                (\svni\s(?P<vni>\d+))?
<<<<<<< Updated upstream:plugins/module_utils/network/ios/rm_templates/vlan_configuration.py
                $""", re.VERBOSE,
            ),
            "setval": "",
=======
                $""", re.VERBOSE),
            "setval": "member"
            "{{ (' evpn-instance ' + member.evi|string) if member.evi is defined else '' }}"
            "{{ (' vni ' + member.vni|string) if member.vni is defined else '' }}",
>>>>>>> Stashed changes:plugins/module_utils/network/ios/rm_templates/vlan_configurations.py
            "result": {
                "{{ vlan_id }}": {
                    "member": {
                        "evi": "{{ inst_vlan_id }}",
                        "vni": "{{ vni }}",
                    },
                },
            },
        },
    ]
    # fmt: on
