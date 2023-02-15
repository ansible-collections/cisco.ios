#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The ace_popper filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: ace_popper
    author: Sagar Paul (@KB-perByte)
    version_added: "4.4.0"
    short_description: Remove ace entries from a acl source of truth.
    description:
        - This plugin removes specific keys from a provided acl data.
        - Using the parameters below- C(acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria))
    options:
      data:
        description:
        - This option represents a list of dictionaries of acls facts.
        - For example C(acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria)),
          in this case C(acls_data) represents this option.
        type: raw
        required: True
      filter_options:
        description: Specify the target keys to remove in list format.
        type: dict
        suboptions:
          remove:
            description: Specify aggregate address
            type: str
            choices: ['first', 'all']
            default: all
          failed_when:
            description: Specify aggregate mask
            type: str
            choices: ['missing', 'never']
            default: missing
          sticky:
            description: Specify aggregate mask
            type: bool
            default: False
      match_criteria:
        description: Specify the matching configuration of target keys and data attributes.
        type: dict
        required: True
        suboptions:
          afi:
            description: Specify afi
            type: str
            required: True
          acl_name:
            description: ACL name
            type: str
          source_address:
            description: Source address of the ACE
            type: str
          destination_address:
            description: Destination address of the ACE
            type: str
          sequence:
            description: Sequence number of the ACE
            type: str
          protocol:
            description: Protocol name
            type: str
          grant:
            description: Grant type permit or deny
            type: str
"""

EXAMPLES = r"""

##Playbook
- name: Gather ACLs config from device existing ACLs config
  cisco.ios.ios_acls:
    state: gathered
  register: result_gathered

- name: Setting host facts for ace_popper filter plugin
  ansible.builtin.set_fact:
    acls_facts: "{{ result_gathered.gathered }}"
    filter_options:
      sticky: true
    match_criteria:
      afi: "ipv4"
      source_address: "192.0.2.0"
      destination_address: "192.0.3.0"

- name: Invoke ace_popper filter plugin
  ansible.builtin.set_fact:
    clean_acls: "{{ acls_facts | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria) }}"

- name: Override ACLs config with device existing ACLs config
  cisco.ios.ios_acls:
    state: overridden
    config: "{{ clean_acls['clean_acls']['acls'] | from_yaml }}"
  check_mode: true


##Output
# PLAYBOOK: ace_popper_example.yml ***********************************************
# 1 plays in ace_popper_example.yml

# PLAY [Filter plugin example ace_popper] ****************************************
# ....

# TASK [Gather ACLs config with device existing ACLs config] *********************
# task path: /home/...ace_popper_example.yml:214
# ok: [xe_machine] => {
#     "changed": false,
#     "gathered": [
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "icmp",
#                             "protocol_options": {
#                                 "icmp": {
#                                     "traceroute": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "host": "198.51.110.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "host": "198.51.100.0"
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "110"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "198.51.101.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "198.51.100.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "tos": {
#                                 "service_value": 12
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "address": "192.0.4.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "lt": 20
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "123"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "grant": "deny",
#                             "sequence": 10,
#                             "source": {
#                                 "host": "192.168.1.200"
#                             }
#                         },
#                         {
#                             "grant": "deny",
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.168.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             }
#                         }
#                     ],
#                     "acl_type": "standard",
#                     "name": "std_acl"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "option": {
#                                 "traceroute": true
#                             },
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "fin": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "test"
#                 }
#             ],
#             "afi": "ipv4"
#         },
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "dscp": "af11",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 }
#                             }
#                         }
#                     ],
#                     "name": "R1_TRAFFIC"
#                 }
#             ],
#             "afi": "ipv6"
#         }
#     ],
#     "invocation": {
#         "module_args": {
#             "config": null,
#             "running_config": null,
#             "state": "gathered"
#         }
#     }
# }

# TASK [Setting host facts for ace_popper filter plugin] *************************
# task path: /home/...ace_popper_example.yml:219
# ok: [xe_machine] => {
#     "ansible_facts": {
#         "acls_facts": [
#             {
#                 "acls": [
#                     {
#                         "aces": [
#                             {
#                                 "destination": {
#                                     "address": "192.0.3.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "dscp": "ef",
#                                 "grant": "deny",
#                                 "protocol": "icmp",
#                                 "protocol_options": {
#                                     "icmp": {
#                                         "traceroute": true
#                                     }
#                                 },
#                                 "sequence": 10,
#                                 "source": {
#                                     "address": "192.0.2.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "ttl": {
#                                     "eq": 10
#                                 }
#                             },
#                             {
#                                 "destination": {
#                                     "host": "198.51.110.0",
#                                     "port_protocol": {
#                                         "eq": "telnet"
#                                     }
#                                 },
#                                 "grant": "deny",
#                                 "protocol": "tcp",
#                                 "protocol_options": {
#                                     "tcp": {
#                                         "ack": true
#                                     }
#                                 },
#                                 "sequence": 20,
#                                 "source": {
#                                     "host": "198.51.100.0"
#                                 }
#                             }
#                         ],
#                         "acl_type": "extended",
#                         "name": "110"
#                     },
#                     {
#                         "aces": [
#                             {
#                                 "destination": {
#                                     "address": "198.51.101.0",
#                                     "port_protocol": {
#                                         "eq": "telnet"
#                                     },
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "grant": "deny",
#                                 "protocol": "tcp",
#                                 "protocol_options": {
#                                     "tcp": {
#                                         "ack": true
#                                     }
#                                 },
#                                 "sequence": 10,
#                                 "source": {
#                                     "address": "198.51.100.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "tos": {
#                                     "service_value": 12
#                                 }
#                             },
#                             {
#                                 "destination": {
#                                     "address": "192.0.4.0",
#                                     "port_protocol": {
#                                         "eq": "www"
#                                     },
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "dscp": "ef",
#                                 "grant": "deny",
#                                 "protocol": "tcp",
#                                 "protocol_options": {
#                                     "tcp": {
#                                         "ack": true
#                                     }
#                                 },
#                                 "sequence": 20,
#                                 "source": {
#                                     "address": "192.0.3.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "ttl": {
#                                     "lt": 20
#                                 }
#                             }
#                         ],
#                         "acl_type": "extended",
#                         "name": "123"
#                     },
#                     {
#                         "aces": [
#                             {
#                                 "grant": "deny",
#                                 "sequence": 10,
#                                 "source": {
#                                     "host": "192.168.1.200"
#                                 }
#                             },
#                             {
#                                 "grant": "deny",
#                                 "sequence": 20,
#                                 "source": {
#                                     "address": "192.168.2.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 }
#                             }
#                         ],
#                         "acl_type": "standard",
#                         "name": "std_acl"
#                     },
#                     {
#                         "aces": [
#                             {
#                                 "destination": {
#                                     "address": "192.0.3.0",
#                                     "port_protocol": {
#                                         "eq": "www"
#                                     },
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "grant": "deny",
#                                 "option": {
#                                     "traceroute": true
#                                 },
#                                 "protocol": "tcp",
#                                 "protocol_options": {
#                                     "tcp": {
#                                         "fin": true
#                                     }
#                                 },
#                                 "sequence": 10,
#                                 "source": {
#                                     "address": "192.0.2.0",
#                                     "wildcard_bits": "0.0.0.255"
#                                 },
#                                 "ttl": {
#                                     "eq": 10
#                                 }
#                             }
#                         ],
#                         "acl_type": "extended",
#                         "name": "test"
#                     }
#                 ],
#                 "afi": "ipv4"
#             },
#             {
#                 "acls": [
#                     {
#                         "aces": [
#                             {
#                                 "destination": {
#                                     "any": true,
#                                     "port_protocol": {
#                                         "eq": "telnet"
#                                     }
#                                 },
#                                 "dscp": "af11",
#                                 "grant": "deny",
#                                 "protocol": "tcp",
#                                 "protocol_options": {
#                                     "tcp": {
#                                         "ack": true
#                                     }
#                                 },
#                                 "sequence": 10,
#                                 "source": {
#                                     "any": true,
#                                     "port_protocol": {
#                                         "eq": "www"
#                                     }
#                                 }
#                             }
#                         ],
#                         "name": "R1_TRAFFIC"
#                     }
#                 ],
#                 "afi": "ipv6"
#             }
#         ],
#         "filter_options": {
#             "sticky": true
#         },
#         "match_criteria": {
#             "afi": "ipv4",
#             "destination_address": "192.0.3.0",
#             "source_address": "192.0.2.0"
#         }
#     },
#     "changed": false
# }

# TASK [Invoke ace_popper filter plugin] *****************************************
# task path: /home/...ace_popper_example.yml:229
# ok: [xe_machine] => {
#     "ansible_facts": {
#         "clean_acls": {
#             "clean_acls": {
#                 "acls": [
#                     {
#                         "acls": [
#                             {
#                                 "aces": [
#                                     {
#                                         "destination": {
#                                             "host": "198.51.110.0",
#                                             "port_protocol": {
#                                                 "eq": "telnet"
#                                             }
#                                         },
#                                         "grant": "deny",
#                                         "protocol": "tcp",
#                                         "protocol_options": {
#                                             "tcp": {
#                                                 "ack": true
#                                             }
#                                         },
#                                         "sequence": 20,
#                                         "source": {
#                                             "host": "198.51.100.0"
#                                         }
#                                     }
#                                 ],
#                                 "name": "110"
#                             },
#                             {
#                                 "aces": [
#                                     {
#                                         "destination": {
#                                             "address": "198.51.101.0",
#                                             "port_protocol": {
#                                                 "eq": "telnet"
#                                             },
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "grant": "deny",
#                                         "protocol": "tcp",
#                                         "protocol_options": {
#                                             "tcp": {
#                                                 "ack": true
#                                             }
#                                         },
#                                         "sequence": 10,
#                                         "source": {
#                                             "address": "198.51.100.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "tos": {
#                                             "service_value": 12
#                                         }
#                                     },
#                                     {
#                                         "destination": {
#                                             "address": "192.0.4.0",
#                                             "port_protocol": {
#                                                 "eq": "www"
#                                             },
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "dscp": "ef",
#                                         "grant": "deny",
#                                         "protocol": "tcp",
#                                         "protocol_options": {
#                                             "tcp": {
#                                                 "ack": true
#                                             }
#                                         },
#                                         "sequence": 20,
#                                         "source": {
#                                             "address": "192.0.3.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "ttl": {
#                                             "lt": 20
#                                         }
#                                     }
#                                 ],
#                                 "name": "123"
#                             },
#                             {
#                                 "aces": [
#                                     {
#                                         "grant": "deny",
#                                         "sequence": 10,
#                                         "source": {
#                                             "host": "192.168.1.200"
#                                         }
#                                     },
#                                     {
#                                         "grant": "deny",
#                                         "sequence": 20,
#                                         "source": {
#                                             "address": "192.168.2.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         }
#                                     }
#                                 ],
#                                 "name": "std_acl"
#                             }
#                         ],
#                         "afi": "ipv4"
#                     },
#                     {
#                         "acls": [
#                             {
#                                 "aces": [
#                                     {
#                                         "destination": {
#                                             "any": true,
#                                             "port_protocol": {
#                                                 "eq": "telnet"
#                                             }
#                                         },
#                                         "dscp": "af11",
#                                         "grant": "deny",
#                                         "protocol": "tcp",
#                                         "protocol_options": {
#                                             "tcp": {
#                                                 "ack": true
#                                             }
#                                         },
#                                         "sequence": 10,
#                                         "source": {
#                                             "any": true,
#                                             "port_protocol": {
#                                                 "eq": "www"
#                                             }
#                                         }
#                                     }
#                                 ],
#                                 "name": "R1_TRAFFIC"
#                             }
#                         ],
#                         "afi": "ipv6"
#                     }
#                 ]
#             },
#             "removed_aces": {
#                 "acls": [
#                     {
#                         "acls": [
#                             {
#                                 "aces": [
#                                     {
#                                         "destination": {
#                                             "address": "192.0.3.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "dscp": "ef",
#                                         "grant": "deny",
#                                         "protocol": "icmp",
#                                         "protocol_options": {
#                                             "icmp": {
#                                                 "traceroute": true
#                                             }
#                                         },
#                                         "sequence": 10,
#                                         "source": {
#                                             "address": "192.0.2.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "ttl": {
#                                             "eq": 10
#                                         }
#                                     }
#                                 ],
#                                 "name": "110"
#                             },
#                             {
#                                 "aces": [
#                                     {
#                                         "destination": {
#                                             "address": "192.0.3.0",
#                                             "port_protocol": {
#                                                 "eq": "www"
#                                             },
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "grant": "deny",
#                                         "option": {
#                                             "traceroute": true
#                                         },
#                                         "protocol": "tcp",
#                                         "protocol_options": {
#                                             "tcp": {
#                                                 "fin": true
#                                             }
#                                         },
#                                         "sequence": 10,
#                                         "source": {
#                                             "address": "192.0.2.0",
#                                             "wildcard_bits": "0.0.0.255"
#                                         },
#                                         "ttl": {
#                                             "eq": 10
#                                         }
#                                     }
#                                 ],
#                                 "name": "test"
#                             }
#                         ],
#                         "afi": "ipv4"
#                     },
#                     {
#                         "acls": [],
#                         "afi": "ipv6"
#                     }
#                 ]
#             }
#         }
#     },
#     "changed": false
# }

# TASK [Override ACLs config with device existing ACLs config] *******************
# task path: /home/...ace_popper_example.yml:233
# changed: [xe_machine] => {
#     "after": [
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "icmp",
#                             "protocol_options": {
#                                 "icmp": {
#                                     "traceroute": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "host": "198.51.110.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "host": "198.51.100.0"
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "110"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "198.51.101.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "198.51.100.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "tos": {
#                                 "service_value": 12
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "address": "192.0.4.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "lt": 20
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "123"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "grant": "deny",
#                             "sequence": 10,
#                             "source": {
#                                 "host": "192.168.1.200"
#                             }
#                         },
#                         {
#                             "grant": "deny",
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.168.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             }
#                         }
#                     ],
#                     "acl_type": "standard",
#                     "name": "std_acl"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "option": {
#                                 "traceroute": true
#                             },
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "fin": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "test"
#                 }
#             ],
#             "afi": "ipv4"
#         },
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "dscp": "af11",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 }
#                             }
#                         }
#                     ],
#                     "name": "R1_TRAFFIC"
#                 }
#             ],
#             "afi": "ipv6"
#         }
#     ],
#     "before": [
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "icmp",
#                             "protocol_options": {
#                                 "icmp": {
#                                     "traceroute": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "host": "198.51.110.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "host": "198.51.100.0"
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "110"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "198.51.101.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "198.51.100.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "tos": {
#                                 "service_value": 12
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "address": "192.0.4.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "lt": 20
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "123"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "grant": "deny",
#                             "sequence": 10,
#                             "source": {
#                                 "host": "192.168.1.200"
#                             }
#                         },
#                         {
#                             "grant": "deny",
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.168.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             }
#                         }
#                     ],
#                     "acl_type": "standard",
#                     "name": "std_acl"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "option": {
#                                 "traceroute": true
#                             },
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "fin": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "test"
#                 }
#             ],
#             "afi": "ipv4"
#         },
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "dscp": "af11",
#                             "grant": "deny",
#                             "protocol": "tcp",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 }
#                             }
#                         }
#                     ],
#                     "name": "R1_TRAFFIC"
#                 }
#             ],
#             "afi": "ipv6"
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "ip access-list extended 110",
#         "no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10",
#         "no ip access-list extended test"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                     "acls": [
#                         {
#                             "aces": [
#                                 {
#                                     "destination": {
#                                         "address": null,
#                                         "any": null,
#                                         "host": "198.51.110.0",
#                                         "object_group": null,
#                                         "port_protocol": {
#                                             "eq": "telnet",
#                                             "gt": null,
#                                             "lt": null,
#                                             "neq": null,
#                                             "range": null
#                                         },
#                                         "wildcard_bits": null
#                                     },
#                                     "dscp": null,
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "ahp": null,
#                                         "eigrp": null,
#                                         "esp": null,
#                                         "gre": null,
#                                         "hbh": null,
#                                         "icmp": null,
#                                         "igmp": null,
#                                         "ip": null,
#                                         "ipinip": null,
#                                         "ipv6": null,
#                                         "nos": null,
#                                         "ospf": null,
#                                         "pcp": null,
#                                         "pim": null,
#                                         "protocol_number": null,
#                                         "sctp": null,
#                                         "tcp": {
#                                             "ack": true,
#                                             "established": null,
#                                             "fin": null,
#                                             "psh": null,
#                                             "rst": null,
#                                             "syn": null,
#                                             "urg": null
#                                         },
#                                         "udp": null
#                                     },
#                                     "remarks": null,
#                                     "sequence": 20,
#                                     "source": {
#                                         "address": null,
#                                         "any": null,
#                                         "host": "198.51.100.0",
#                                         "object_group": null,
#                                         "port_protocol": null,
#                                         "wildcard_bits": null
#                                     },
#                                     "time_range": null,
#                                     "tos": null,
#                                     "ttl": null
#                                 }
#                             ],
#                             "acl_type": null,
#                             "name": "110"
#                         },
#                         {
#                             "aces": [
#                                 {
#                                     "destination": {
#                                         "address": "198.51.101.0",
#                                         "any": null,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": {
#                                             "eq": "telnet",
#                                             "gt": null,
#                                             "lt": null,
#                                             "neq": null,
#                                             "range": null
#                                         },
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "dscp": null,
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "ahp": null,
#                                         "eigrp": null,
#                                         "esp": null,
#                                         "gre": null,
#                                         "hbh": null,
#                                         "icmp": null,
#                                         "igmp": null,
#                                         "ip": null,
#                                         "ipinip": null,
#                                         "ipv6": null,
#                                         "nos": null,
#                                         "ospf": null,
#                                         "pcp": null,
#                                         "pim": null,
#                                         "protocol_number": null,
#                                         "sctp": null,
#                                         "tcp": {
#                                             "ack": true,
#                                             "established": null,
#                                             "fin": null,
#                                             "psh": null,
#                                             "rst": null,
#                                             "syn": null,
#                                             "urg": null
#                                         },
#                                         "udp": null
#                                     },
#                                     "remarks": null,
#                                     "sequence": 10,
#                                     "source": {
#                                         "address": "198.51.100.0",
#                                         "any": null,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": null,
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "time_range": null,
#                                     "tos": {
#                                         "max_reliability": null,
#                                         "max_throughput": null,
#                                         "min_delay": null,
#                                         "min_monetary_cost": null,
#                                         "normal": null,
#                                         "service_value": 12
#                                     },
#                                     "ttl": null
#                                 },
#                                 {
#                                     "destination": {
#                                         "address": "192.0.4.0",
#                                         "any": null,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": {
#                                             "eq": "www",
#                                             "gt": null,
#                                             "lt": null,
#                                             "neq": null,
#                                             "range": null
#                                         },
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "dscp": "ef",
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "ahp": null,
#                                         "eigrp": null,
#                                         "esp": null,
#                                         "gre": null,
#                                         "hbh": null,
#                                         "icmp": null,
#                                         "igmp": null,
#                                         "ip": null,
#                                         "ipinip": null,
#                                         "ipv6": null,
#                                         "nos": null,
#                                         "ospf": null,
#                                         "pcp": null,
#                                         "pim": null,
#                                         "protocol_number": null,
#                                         "sctp": null,
#                                         "tcp": {
#                                             "ack": true,
#                                             "established": null,
#                                             "fin": null,
#                                             "psh": null,
#                                             "rst": null,
#                                             "syn": null,
#                                             "urg": null
#                                         },
#                                         "udp": null
#                                     },
#                                     "remarks": null,
#                                     "sequence": 20,
#                                     "source": {
#                                         "address": "192.0.3.0",
#                                         "any": null,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": null,
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "time_range": null,
#                                     "tos": null,
#                                     "ttl": {
#                                         "eq": null,
#                                         "gt": null,
#                                         "lt": 20,
#                                         "neq": null,
#                                         "range": null
#                                     }
#                                 }
#                             ],
#                             "acl_type": null,
#                             "name": "123"
#                         },
#                         {
#                             "aces": [
#                                 {
#                                     "destination": null,
#                                     "dscp": null,
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": null,
#                                     "protocol_options": null,
#                                     "remarks": null,
#                                     "sequence": 10,
#                                     "source": {
#                                         "address": null,
#                                         "any": null,
#                                         "host": "192.168.1.200",
#                                         "object_group": null,
#                                         "port_protocol": null,
#                                         "wildcard_bits": null
#                                     },
#                                     "time_range": null,
#                                     "tos": null,
#                                     "ttl": null
#                                 },
#                                 {
#                                     "destination": null,
#                                     "dscp": null,
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": null,
#                                     "protocol_options": null,
#                                     "remarks": null,
#                                     "sequence": 20,
#                                     "source": {
#                                         "address": "192.168.2.0",
#                                         "any": null,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": null,
#                                         "wildcard_bits": "0.0.0.255"
#                                     },
#                                     "time_range": null,
#                                     "tos": null,
#                                     "ttl": null
#                                 }
#                             ],
#                             "acl_type": null,
#                             "name": "std_acl"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 },
#                 {
#                     "acls": [
#                         {
#                             "aces": [
#                                 {
#                                     "destination": {
#                                         "address": null,
#                                         "any": true,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": {
#                                             "eq": "telnet",
#                                             "gt": null,
#                                             "lt": null,
#                                             "neq": null,
#                                             "range": null
#                                         },
#                                         "wildcard_bits": null
#                                     },
#                                     "dscp": "af11",
#                                     "enable_fragments": null,
#                                     "evaluate": null,
#                                     "fragments": null,
#                                     "grant": "deny",
#                                     "log": null,
#                                     "log_input": null,
#                                     "option": null,
#                                     "precedence": null,
#                                     "protocol": "tcp",
#                                     "protocol_options": {
#                                         "ahp": null,
#                                         "eigrp": null,
#                                         "esp": null,
#                                         "gre": null,
#                                         "hbh": null,
#                                         "icmp": null,
#                                         "igmp": null,
#                                         "ip": null,
#                                         "ipinip": null,
#                                         "ipv6": null,
#                                         "nos": null,
#                                         "ospf": null,
#                                         "pcp": null,
#                                         "pim": null,
#                                         "protocol_number": null,
#                                         "sctp": null,
#                                         "tcp": {
#                                             "ack": true,
#                                             "established": null,
#                                             "fin": null,
#                                             "psh": null,
#                                             "rst": null,
#                                             "syn": null,
#                                             "urg": null
#                                         },
#                                         "udp": null
#                                     },
#                                     "remarks": null,
#                                     "sequence": 10,
#                                     "source": {
#                                         "address": null,
#                                         "any": true,
#                                         "host": null,
#                                         "object_group": null,
#                                         "port_protocol": {
#                                             "eq": "www",
#                                             "gt": null,
#                                             "lt": null,
#                                             "neq": null,
#                                             "range": null
#                                         },
#                                         "wildcard_bits": null
#                                     },
#                                     "time_range": null,
#                                     "tos": null,
#                                     "ttl": null
#                                 }
#                             ],
#                             "acl_type": null,
#                             "name": "R1_TRAFFIC"
#                         }
#                     ],
#                     "afi": "ipv6"
#                 }
#             ],
#             "running_config": null,
#             "state": "overridden"
#         }
#     }
# }

# PLAY RECAP *********************************************************************
# xe_machine               : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0



"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.cisco.ios.plugins.plugin_utils.ace_popper import ace_popper


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _ace_popper(*args, **kwargs):
    """remove ace entries from a acl data"""

    keys = ["data", "filter_options", "match_criteria"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="ace_popper")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return ace_popper(**updated_data)


class FilterModule(object):
    """ace_popper"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"ace_popper": _ace_popper}
