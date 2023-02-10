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
    version_added: "2.5.0"
    short_description: Remove ace entries from a acl source of truth.
    description:
        - This plugin removes specific keys from a provided data recursively.
        - Matching parameter defaults to equals unless C(matching_parameter) is explicitly mentioned.
        - Using the parameters below- C(data|ansible.utils.acl_popper(target([....])))
    options:
      data:
        description:
        - This option represents a list of dictionaries or a dictionary with any level of nesting data.
        - For example C(config_data|ansible.utils.acl_popper(target([....]))), in this case C(config_data) represents this option.
        type: raw
        required: True
      filter_options:
        description: Specify the target keys to remove in list format.
        type: dict
        suboptions:
          remove:
            description: Specify aggregate address
            type: str
          failed_when:
            description: Specify aggregate mask
            type: str
      match_criteria:
        description: Specify the matching configuration of target keys and data attributes.
        type: dict
        suboptions:
          afi:
            description: Specify afi
            type: str
          acl_name:
            description: Specify acl_name
            type: str
          source_address:
            description: Set source_address
            type: str
          destination_address:
            description: Set destination_address
            type: str
          sequence:
            description: sequence
            type: str
          protocol:
            description: Set protocol
            type: str
          grant:
            description: grant
            type: str
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
                  any: true
                  port_protocol:
                    eq: "22"
                grant: permit
                protocol: tcp
                sequence: 10
                source:
                  any: true
              - destination:
                  host: 192.168.20.5
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
    - filter_options:
        remove: "first"
        # filed_when: "missing"
    - match_criteria:
        afi: "ipv4"
        acl_name: "test_acl"
        source_address: "198.51.100.0"

  tasks:
    - name: Remove ace entries from a provided data
      ansible.builtin.debug:
        msg: "{{ acls_data | cisco.ios.acl_popper(filter_options=filter_options, match_criteria=match_criteria) }}"
      register: result

##Output
# TASK [Remove ace entries from a provided data] ***********************
# ok: [localhost] => {
#     "msg": {
#         "acls": {
#             "acls": [
#                 {
#                     "acls": [],
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
#                                 },
#                                 {
#                                     "destination": {
#                                         "host": "192.168.20.5",
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

import debugpy


debugpy.listen(3000)
debugpy.wait_for_client()


@pass_environment
def _acl_popper(*args, **kwargs):
    """remove ace entries from a acl data"""

    keys = ["data", "filter_options", "match_criteria"]
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
