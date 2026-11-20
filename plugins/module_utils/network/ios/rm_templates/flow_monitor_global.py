# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Flow_monitor_global parser template file.

Facts are gathered with a custom block parser (see facts/flow_monitor_global) and
commands are generated in config/flow_monitor_global, so this template defines no
parsers. It exists only to provide ``validate_config`` to the facts and config classes.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Flow_monitor_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Flow_monitor_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    PARSERS = []
