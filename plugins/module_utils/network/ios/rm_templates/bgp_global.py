# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Bgp_global parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_bgp_bestpath(config_data):
    pass


def _tmplt_neighbor(config_data):
    pass


class Bgp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Bgp_globalTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "asn",
            "getval": re.compile(
                r"""^router*
                    \s*bgp*
                    \s*(?P<asn>\d+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "asn",
            "setval": "router bgp {{ asn }}",
            "result": {"asn": "{{ asn }}"},
            "shared": True,
        },
        {
            "name": "bgp",
            "getval": re.compile(
                r"""\s*bgp*
                        \s*(?P<always_compare_med>always-compare-med)*
                        \s*(?P<log_neighbor_changes>log-neighbor-changes)*
                        $""",
                re.VERBOSE,
            ),
            "setval": "bgp always-compare-med",
            # "compval": "always_compare_med",
            "result": {
                # "{{ asn }}": {
                "bgp": {
                    "always_compare_med": "{{ True if always_compare_med is defined }}",
                    "log_neighbor_changes": "{{ True if log_neighbor_changes is defined }}",
                },
                # },
            },
        },
        # {
        #     "name": "bgp.log_neighbor_changes",
        #     "getval": re.compile(
        #         r"""\s*bgp*
        #             $""",
        #         re.VERBOSE,
        #     ),
        #     "setval": "bgp log-neighbor-changes",
        #     "compval": "log_neighbor_changes",
        #     "result": {
        #         #"{{ asn }}": {
        #             "bgp": {
        #             },
        #         #},
        #     },
        # },
        {
            "name": "bgp.bestpath",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*bestpath*
                    \s*(?P<aigp>aigp\signore)*
                    \s*(?P<compare_routerid>compare-routerid)*
                    \s*(?P<cost_community>cost-community\signore)*
                    \s*(?P<med>med\s(confed|missing-as-worst|confed\smissing-as-worst))*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_bestpath,
            "compval": "bestpath",
            "result": {
                # "{{ asn }}": {
                "bgp": {
                    "bestpath": {
                        "aigp": "{{ True if aigp is defined }}",
                        "compare_routerid": "{{ True if compare_routerid is defined }}",
                        "cost_community": "{{ True if cost_community is defined }}",
                        "med": {
                            "confed": "{{ True if med is defined and 'confed' in med }}",
                            "missing_as_worst": "{{ True if med is defined and 'missing-as-worst' in med }}",
                        },
                    }
                },
                # },
            },
        },
        {
            "name": "bgp.nopeerup_delay",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*nopeerup-delay*
                    \s*(?P<cold_boot>cold-boot\s\d+)*
                    \s*(?P<nsf_switchover>nsf-switchover\s\d+)*
                    \s*(?P<post_boot>post-boot\s\d+)*
                    \s*(?P<user_initiated>user-initiated\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "bgp log-neighbor-changes",
            "compval": "log_neighbor_changes",
            "result": {
                # "{{ asn }}": {
                "bgp": {
                    "nopeerup_delay": {
                        "cold_boot": "{{ cold_boot.split('cold-boot ')[1] }}",
                        "nsf_switchover": "{{ nsf_switchover.split('nsf-switchover ')[1] }}",
                        "post_boot": "{{ post_boot.split('post-boot ')[1] }}",
                        "user_initiated": "{{ user_initiated.split('user-initiated ')[1] }}",
                    }
                },
                # },
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""\s*neighbor*
                    \s*(?P<neighbor>(?:[0-9]{1,3}\.){3}[0-9]{1,3}|host\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+|\S+)*
                    \s*(?P<remote_as>remote-as\s\d+)*
                    \s*(?P<description>description\s\S.+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor,
            "compval": "neighbor",
            "result": {
                # "{{ asn }}": {
                "neighbor": {
                    "address": "{{ neighbor if ':' not in neighbor and '.' in neighbor }}",
                    "ipv6_address": "{{ neighbor if ':' in neighbor and '.' in neighbor }}",
                    "tag": "{{ neighbor if ':' not in neighbor and '.' not in neighbor }}",
                    "remote_as": "{{ remote_as.split('remote-as ')[1] if remote_as is defined }}",
                    "description": "{{ description.split('description ')[1] if description is defined }}",
                },
                # },
            },
        },
    ]
