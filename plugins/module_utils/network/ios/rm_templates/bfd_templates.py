# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bfd_templates parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Bfd_templatesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bfd_templatesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^bfd-template
                    \s(?P<hop>single-hop|multi-hop)
                    \s(?P<name>\S+)
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "bfd-template {% if hop == 'single_hop' %}single-hop{% elif hop == 'multi_hop' %}multi-hop{% endif %} {{ name }}",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "hop": "{% if hop == 'single-hop' %}single_hop{% elif hop == 'multi-hop' %}multi_hop{% endif %}",
                },
            },
            "shared": True,
        },
        {
            "name": "interval",
            "getval": re.compile(
                r"""
                \s+interval\smin-tx\s(?P<min_tx>\d+)
                \smin-rx\s(?P<min_rx>\d+)
                \smultiplier\s(?P<multiplier>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "interval min-tx {{ interval.min_tx }} "
                      "min-rx {{ interval.min_rx }} "
                      "multiplier {{ interval.multiplier }}",
            "result": {
                "{{ name }}": {
                    "interval": {
                        "min_tx": "{{ min_tx | int }}",
                        "min_rx": "{{ min_rx | int }}",
                        "multiplier": "{{ multiplier | int }}",
                    },
                },
            },
        },
        {
            "name": "dampening",
            "getval": re.compile(
                r"""
                \s+dampening\s(?P<half_life_period>\d+)
                \s(?P<reuse_threshold>\d+)
                \s(?P<suppress_threshold>\d+)
                \s(?P<max_suppress_time>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "dampening {{ dampening.half_life_period }} "
                      "{{ dampening.reuse_threshold }} "
                      "{{ dampening.suppress_threshold }} "
                      "{{ dampening.max_suppress_time }}",
            "result": {
                "{{ name }}": {
                    "dampening": {
                        "half_life_period": "{{ half_life_period | int }}",
                        "reuse_threshold": "{{ reuse_threshold | int }}",
                        "suppress_threshold": "{{ suppress_threshold | int }}",
                        "max_suppress_time": "{{ max_suppress_time | int }}",
                    },
                },
            },
        },
        {
            "name": "echo",
            "getval": re.compile(
                r"""
                \s+(?P<no>no\s)?echo
                $""",
                re.VERBOSE,
            ),
            "setval": "echo",
            "result": {
                "{{ name }}": {
                    "echo": "{{ False if no is defined else True }}",
                },
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s+authentication\s(?P<auth_type>sha-1|md5|meticulous-md5|meticulous-sha-1)
                \skeychain\s(?P<keychain>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": (
                "authentication "
                "{% if authentication.type == 'sha_1' %}sha-1"
                "{% elif authentication.type == 'md5' %}md5"
                "{% elif authentication.type == 'meticulous_md5' %}meticulous-md5"
                "{% elif authentication.type == 'meticulous_sha_1' %}meticulous-sha-1"
                "{% endif %} "
                "keychain {{ authentication.keychain }}"
            ),
            "result": {
                "{{ name }}": {
                    "authentication": {
                        "type": (
                            "{% if auth_type == 'sha-1' %}sha_1"
                            "{% elif auth_type == 'md5' %}md5"
                            "{% elif auth_type == 'meticulous-md5' %}meticulous_md5"
                            "{% elif auth_type == 'meticulous-sha-1' %}meticulous_sha_1"
                            "{% endif %}"
                        ),
                        "keychain": "{{ keychain }}",
                    },
                },
            },
        },
    ]
    # fmt: on
