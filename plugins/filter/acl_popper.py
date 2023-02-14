#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The acl_popper filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: acl_popper
    author: Sagar Paul (@KB-perByte)
    version_added: "4.4.0"
    short_description: Remove ace entries from a acl source of truth.
    description:
        - This plugin removes specific keys from a provided acl data.
        - Using the parameters below- C(acls_data | cisco.ios.acl_popper(filter_options=filter_options, match_criteria=match_criteria))
    options:
      data:
        description:
        - This option represents a list of dictionaries of acls facts.
        - For example C(acls_data | cisco.ios.acl_popper(filter_options=filter_options, match_criteria=match_criteria)),
          in this case C(acls_data) represents this option.
        type: raw
        required: True
      failed_when:
        description: Specify aggregate mask
        type: str
        choices: ['missing', 'never']
        default: missing
      match_criteria:
        description: Specify the matching configuration of target keys and data attributes.
        type: dict
        required: True
        suboptions:
          ipv4:
            description: Specify ipv4 acl names with sequence number list
            type: raw
          ipv6:
            description: Specify ipv6 acl names with sequence number list
            type: raw
"""

EXAMPLES = r"""

##Playbook
vars:
  - acls_data:
    - acls:
        - aces:
            - grant: permit
              sequence: 10
              source:
                address: 192.168.12.0
                wildcard_bits: 0.0.0.255
          acl_type: standard
          name: "1"
        - aces:
            - destination:
                address: 192.168.20.5
                any: true
                port_protocol:
                  eq: "22"
              grant: permit
              protocol: tcp
              sequence: 10
              source:
                any: true
            - destination:
                address: 192.168.20.5
                port_protocol:
                  eq: "22"
              grant: permit
              protocol: tcp
              sequence: 21
              source:
                host: 192.168.11.8
          acl_type: extended
          name: acl_123
        - aces:
            - destination:
                address: 192.0.3.0
                port_protocol:
                  eq: www
                wildcard_bits: 0.0.0.255
              grant: deny
              option:
                traceroute: true
              protocol: tcp
              protocol_options:
                tcp:
                  fin: true
              sequence: 10
              source:
                address: 192.0.2.0
                wildcard_bits: 0.0.0.255
              ttl:
                eq: 10
          acl_type: extended
          name: test_acl
      afi: ipv4
    - acls:
        - aces:
            - destination:
                any: true
                port_protocol:
                  eq: telnet
              dscp: af11
              grant: deny
              protocol: tcp
              protocol_options:
                tcp:
                  ack: true
              sequence: 10
              source:
                any: true
                port_protocol:
                  eq: www
          name: R1_TRAFFIC
      afi: ipv6
  - failed_when: "missing"
  - match_criteria:
      ipv4:
        '1':
        - 10
        acl_123:
        - 21
      ipv6:
        R1_TRAFFIC:
        - 10

tasks:
  - name: Build source of truth based and keep backup
    ansible.builtin.debug:
      msg: "{{ acls_data | cisco.ios.acl_popper(failed_when=failed_when, match_criteria=match_criteria) }}"
    register: result


##Output
# ok: [localhost] => {
#     "msg": {
#         "acls": {
#             "acls": [
#                 {
#                     "acls": [
#                         {
#                             "ace": [
#                                 {
#                                     "destination": {
#                                         "address": "192.168.20.5",
#                                         "any": true,
#                                         "port_protocol": {
#                                             "eq": "22"
#                                         }
#                                     },
#                                     "grant": "permit",
#                                     "protocol": "tcp",
#                                     "sequence": 10,
#                                     "source": {
#                                         "any": true
#                                     }
#                                 }
#                             ],
#                             "name": "acl_123"
#                         },
#                         {
#                             "ace": [
#                                 {
#                                     "destination": {
#                                         "address": "192.0.3.0",
#                                         "port_protocol": {
#                                             "eq": "www"
#                                         },
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "grant": "deny",
#                                     "option": {
#                                         "traceroute": true
#                                     },
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "tcp": {
#                                             "fin": true
#                                         }
#                                     },
#                                     "sequence": 10,
#                                     "source": {
#                                         "address": "192.0.2.0",
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "ttl": {
#                                         "eq": 10
#                                     }
#                                 }
#                             ],
#                             "name": "test_acl"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 },
#                 {
#                     "acls": [],
#                     "afi": "ipv6"
#                 }
#             ]
#         },
#         "removed_acls": {
#             "acls": [
#                 {
#                     "acls": [
#                         {
#                             "ace": [
#                                 {
#                                     "grant": "permit",
#                                     "sequence": 10,
#                                     "source": {
#                                         "address": "192.168.12.0",
#                                         "wildcard_bits": "0.0.0.255"
#                                     }
#                                 }
#                             ],
#                             "name": "1"
#                         },
#                         {
#                             "ace": [
#                                 {
#                                     "destination": {
#                                         "address": "192.168.20.5",
#                                         "port_protocol": {
#                                             "eq": "22"
#                                         }
#                                     },
#                                     "grant": "permit",
#                                     "protocol": "tcp",
#                                     "sequence": 21,
#                                     "source": {
#                                         "host": "192.168.11.8"
#                                     }
#                                 }
#                             ],
#                             "name": "acl_123"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 },
#                 {
#                     "acls": [
#                         {
#                             "ace": [
#                                 {
#                                     "destination": {
#                                         "any": true,
#                                         "port_protocol": {
#                                             "eq": "telnet"
#                                         }
#                                     },
#                                     "dscp": "af11",
#                                     "grant": "deny",
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "tcp": {
#                                             "ack": true
#                                         }
#                                     },
#                                     "sequence": 10,
#                                     "source": {
#                                         "any": true,
#                                         "port_protocol": {
#                                             "eq": "www"
#                                         }
#                                     }
#                                 }
#                             ],
#                             "name": "R1_TRAFFIC"
#                         }
#                     ],
#                     "afi": "ipv6"
#                 }
#             ]
#         }
#     }
# }
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.cisco.ios.plugins.plugin_utils.acl_popper import acl_popper


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _acl_popper(*args, **kwargs):
    """remove ace entries from a acl data"""

    keys = ["data", "failed_when", "match_criteria"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="acl_popper")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return acl_popper(**updated_data)


class FilterModule(object):
    """acl_popper"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"acl_popper": _acl_popper}
