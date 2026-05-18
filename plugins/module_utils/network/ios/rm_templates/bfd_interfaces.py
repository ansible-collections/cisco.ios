# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bfd_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Bfd_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bfd_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                (\s+(?P<no>no))
                \s+bfd\senable
                $""", re.VERBOSE,
            ),
            "setval": "bfd enable",
            "result": {
                "{{ name }}": {
                    "bfd": "{{ False if no is defined else True }}",
                },
            },
        },
        {
            "name": "echo",
            "getval": re.compile(
                r"""
                (\s+(?P<no>no))
                \s+bfd\secho
                $""", re.VERBOSE,
            ),
            "setval": "bfd echo",
            "result": {
                "{{ name }}": {
                    "echo": "{{ False if no is defined else True }}",
                },
            },
        },
        {
            "name": "jitter",
            "getval": re.compile(
                r"""
                (\s+(?P<no>no))
                \s+bfd\sjitter
                $""", re.VERBOSE,
            ),
            "setval": "bfd jitter",
            "result": {
                "{{ name }}": {
                    "jitter": "{{ False if no is defined else True }}",
                },
            },
        },
        {
            "name": "local_address",
            "getval": re.compile(
                r"""\s+bfd\slocal-address
                    (\s(?P<local_address>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "bfd local-address {{ local_address }}",
            "result": {"{{ name }}": {"local_address": "{{ local_address }}"}},
        },
        {
            "name": "template",
            "getval": re.compile(
                r"""\s+bfd\stemplate
                    (\s(?P<template>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "bfd template {{ template }}",
            "result": {"{{ name }}": {"template": "{{ template }}"}},
        },
        {
            "name": "interval",
            "getval": re.compile(
                r"""
                \s+bfd\sinterval
                \s+(?P<input>\d+)
                \s+min_rx\s(?P<min_rx>\d+)
                \s+multiplier\s(?P<multiplier>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "bfd interval {{ interval.input }} "
                      "min_rx {{ interval.min_rx }} "
                      "multiplier {{ interval.multiplier }}",
            "result": {
                "{{ name }}": {
                    "interval": {
                        "input": "{{ input }}",
                        "min_rx": "{{ min_rx | int }}",
                        "multiplier": "{{ multiplier }}",
                    },
                },
            },
        },
    ]
    # fmt: on
