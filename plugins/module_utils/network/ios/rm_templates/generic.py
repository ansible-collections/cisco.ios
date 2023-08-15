# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The User_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class IosNetworkTemplate(NetworkTemplate):
    def __init__(self, lines=None, tmplt=None, prefix=None, module=None):
        super(IosNetworkTemplate, self).__init__(
            lines=lines,
            tmplt=tmplt,
            prefix=prefix,
            module=module,
        )

    def _render(self, tmplt, data, negate):
        if isinstance(tmplt, dict) and "command" in tmplt:
            res = deepcopy(tmplt)
            try:
                if callable(res["command"]):
                    res["command"] = res["command"](data)
                else:
                    res["command"] = self._template(
                        value=res["command"],
                        variables=data,
                        fail_on_undefined=False,
                    )
            except KeyError:
                return None

            if res:
                if negate:
                    rem = "{0} ".format(self._prefix.get("remove", "no"))
                    if isinstance(res["command"], list):
                        res["command"] = list(map(rem, res["command"]))
                    else:
                        res["command"] = rem + res["command"]
                    return res
                else:
                    set_cmd = "{0} ".format(self._prefix.get("set", ""))
                    if isinstance(res["command"], list):
                        res["command"] = list(map(set_cmd, res["command"]))
                    else:
                        res["command"] = set_cmd + res["command"]
            return res
        return super(IosNetworkTemplate, self)._render(tmplt, data, negate)
