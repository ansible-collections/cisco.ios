#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The pop_ace filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: pop_ace
    author: Sagar Paul (@KB-perByte)
    version_added: "4.4.0"
    short_description: Remove ace entries from a acl source of truth.
    description:
        - This plugin removes specific keys from a provided acl data.
        - Using the parameters below - C(acls_data | cisco.ios.pop_ace(filter_options=filter_options, match_criteria=match_criteria))
    options:
      data:
        description:
        - This option represents a list of dictionaries of acls facts.
        - For example C(acls_data | cisco.ios.pop_ace(filter_options=filter_options, match_criteria=match_criteria)),
          in this case C(acls_data) represents this option.
        type: raw
        required: True
      filter_options:
        description: Specify filtering options which drives the filter plugin.
        type: dict
        suboptions:
          remove:
            description:
              - Remove first removes one ace from each ACL entry on match
              - Remove all is more aggressive and removes more than one on match
            type: str
            choices: ['first', 'all']
            default: all
          failed_when:
            description:
              - On missing it fails when there is no match with the ACL data supplied
              - On never it would never fail
            type: str
            choices: ['missing', 'never']
            default: missing
          match_all:
            description: When true ensures ace removed only when it matches all match criteria
            type: bool
            default: False
      match_criteria:
        description: Specify the matching configuration of the ACEs to remove.
        type: dict
        required: True
        suboptions:
          afi:
            description: Specify afi to match
            type: str
            required: True
          acl_name:
            description: ACL name to match
            type: str
          source:
            description: Source address/ host/ any of the ACE to match
            type: str
          destination:
            description: Destination address/ host/ any of the ACE to natch
            type: str
          sequence:
            description: Sequence number of the ACE to match
            type: str
          protocol:
            description: Protocol name of the ACE to match
            type: str
          grant:
            description: Grant type permit or deny to match
            type: str
"""

EXAMPLES = r"""
##Playbook with filter plugin example
vars:
  filter_options:
    match_all: true
  match_criteria:
    afi: "ipv4"
    source: "192.0.2.0"
    destination: "192.0.3.0"
  acls_data:
    - acls:
        - aces:
            - destination:
                address: 192.0.3.0
                wildcard_bits: 0.0.0.255
              dscp: ef
              grant: deny
              protocol: icmp
              protocol_options:
                icmp:
                  traceroute: true
              sequence: 10
              source:
                address: 192.0.2.0
                wildcard_bits: 0.0.0.255
              ttl:
                eq: 10
            - destination:
                host: 198.51.110.0
                port_protocol:
                  eq: telnet
              grant: deny
              protocol: tcp
              protocol_options:
                tcp:
                  ack: true
              sequence: 20
              source:
                host: 198.51.100.0
          acl_type: extended
          name: "110"
        - aces:
            - destination:
                address: 198.51.101.0
                port_protocol:
                  eq: telnet
                wildcard_bits: 0.0.0.255
              grant: deny
              protocol: tcp
              protocol_options:
                tcp:
                  ack: true
              sequence: 10
              source:
                address: 198.51.100.0
                wildcard_bits: 0.0.0.255
              tos:
                service_value: 12
            - destination:
                address: 192.0.4.0
                port_protocol:
                  eq: www
                wildcard_bits: 0.0.0.255
              dscp: ef
              grant: deny
              protocol: tcp
              protocol_options:
                tcp:
                  ack: true
              sequence: 20
              source:
                address: 192.0.3.0
                wildcard_bits: 0.0.0.255
              ttl:
                lt: 20
          acl_type: extended
          name: "123"
        - aces:
            - grant: deny
              sequence: 10
              source:
                host: 192.168.1.200
            - grant: deny
              sequence: 20
              source:
                address: 192.168.2.0
                wildcard_bits: 0.0.0.255
          acl_type: standard
          name: std_acl
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
          name: test
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

tasks:
  - name: Remove ace entries from a provided data
    ansible.builtin.debug:
      msg: "{{ acls_data | cisco.ios.pop_ace(filter_options=filter_options, match_criteria=match_criteria) }}"

##Output
# PLAY [Filter plugin example pop_ace] ******************************************************************************************************************

# TASK [Remove ace entries from a provided data] ***********************************************************************************************************
# ok: [xe_machine] =>
#   msg:
#     clean_acls:
#       acls:
#       - acls:
#         - aces:
#           - destination:
#               host: 198.51.110.0
#               port_protocol:
#                 eq: telnet
#             grant: deny
#             protocol: tcp
#             protocol_options:
#               tcp:
#                 ack: true
#             sequence: 20
#             source:
#               host: 198.51.100.0
#           name: '110'
#         - aces:
#           - destination:
#               address: 198.51.101.0
#               port_protocol:
#                 eq: telnet
#               wildcard_bits: 0.0.0.255
#             grant: deny
#             protocol: tcp
#             protocol_options:
#               tcp:
#                 ack: true
#             sequence: 10
#             source:
#               address: 198.51.100.0
#               wildcard_bits: 0.0.0.255
#             tos:
#               service_value: 12
#           - destination:
#               address: 192.0.4.0
#               port_protocol:
#                 eq: www
#               wildcard_bits: 0.0.0.255
#             dscp: ef
#             grant: deny
#             protocol: tcp
#             protocol_options:
#               tcp:
#                 ack: true
#             sequence: 20
#             source:
#               address: 192.0.3.0
#               wildcard_bits: 0.0.0.255
#             ttl:
#               lt: 20
#           name: '123'
#         - aces:
#           - grant: deny
#             sequence: 10
#             source:
#               host: 192.168.1.200
#           - grant: deny
#             sequence: 20
#             source:
#               address: 192.168.2.0
#               wildcard_bits: 0.0.0.255
#           name: std_acl
#         afi: ipv4
#       - acls:
#         - aces:
#           - destination:
#               any: true
#               port_protocol:
#                 eq: telnet
#             dscp: af11
#             grant: deny
#             protocol: tcp
#             protocol_options:
#               tcp:
#                 ack: true
#             sequence: 10
#             source:
#               any: true
#               port_protocol:
#                 eq: www
#           name: R1_TRAFFIC
#         afi: ipv6
#     removed_aces:
#       acls:
#       - acls:
#         - aces:
#           - destination:
#               address: 192.0.3.0
#               wildcard_bits: 0.0.0.255
#             dscp: ef
#             grant: deny
#             protocol: icmp
#             protocol_options:
#               icmp:
#                 traceroute: true
#             sequence: 10
#             source:
#               address: 192.0.2.0
#               wildcard_bits: 0.0.0.255
#             ttl:
#               eq: 10
#           name: '110'
#         - aces:
#           - destination:
#               address: 192.0.3.0
#               port_protocol:
#                 eq: www
#               wildcard_bits: 0.0.0.255
#             grant: deny
#             option:
#               traceroute: true
#             protocol: tcp
#             protocol_options:
#               tcp:
#                 fin: true
#             sequence: 10
#             source:
#               address: 192.0.2.0
#               wildcard_bits: 0.0.0.255
#             ttl:
#               eq: 10
#           name: test
#         afi: ipv4
#       - acls: []
#         afi: ipv6


##Playbook with workflow example
tasks:
  - name: Gather ACLs config from device existing ACLs config
    cisco.ios.ios_acls:
      state: gathered
    register: result_gathered

  - name: Setting host facts for pop_ace filter plugin
    ansible.builtin.set_fact:
      acls_facts: "{{ result_gathered.gathered }}"
      filter_options:
        match_all: true
      match_criteria:
        afi: "ipv4"
        source: "192.0.2.0"
        destination: "192.0.3.0"

  - name: Invoke pop_ace filter plugin
    ansible.builtin.set_fact:
      clean_acls: "{{ acls_facts | cisco.ios.pop_ace(filter_options=filter_options, match_criteria=match_criteria) }}"

  - name: Override ACLs config with device existing ACLs config
    cisco.ios.ios_acls:
      state: overridden
      config: "{{ clean_acls['clean_acls']['acls'] | from_yaml }}"


##Output

# PLAYBOOK: pop_ace_example.yml ***********************************************

# PLAY [Filter plugin example pop_ace] ****************************************

# TASK [Gather ACLs config with device existing ACLs config] *********************
# ok: [xe_machine] => changed=false
#   gathered:
#   - acls:
#     - aces:
#       - destination:
#           address: 192.0.3.0
#           wildcard_bits: 0.0.0.255
#         dscp: ef
#         grant: deny
#         protocol: icmp
#         protocol_options:
#           icmp:
#             traceroute: true
#         sequence: 10
#         source:
#           address: 192.0.2.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           eq: 10
#       - destination:
#           host: 198.51.110.0
#           port_protocol:
#             eq: telnet
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           host: 198.51.100.0
#       acl_type: extended
#       name: '110'
#     - aces:
#       - destination:
#           address: 198.51.101.0
#           port_protocol:
#             eq: telnet
#           wildcard_bits: 0.0.0.255
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           address: 198.51.100.0
#           wildcard_bits: 0.0.0.255
#         tos:
#           service_value: 12
#       - destination:
#           address: 192.0.4.0
#           port_protocol:
#             eq: www
#           wildcard_bits: 0.0.0.255
#         dscp: ef
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           address: 192.0.3.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           lt: 20
#       acl_type: extended
#       name: '123'
#     - aces:
#       - grant: deny
#         sequence: 10
#         source:
#           host: 192.168.1.200
#       - grant: deny
#         sequence: 20
#         source:
#           address: 192.168.2.0
#           wildcard_bits: 0.0.0.255
#       acl_type: standard
#       name: std_acl
#     - aces:
#       - destination:
#           address: 192.0.3.0
#           port_protocol:
#             eq: www
#           wildcard_bits: 0.0.0.255
#         grant: deny
#         option:
#           traceroute: true
#         protocol: tcp
#         protocol_options:
#           tcp:
#             fin: true
#         sequence: 10
#         source:
#           address: 192.0.2.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           eq: 10
#       acl_type: extended
#       name: test
#     afi: ipv4
#   - acls:
#     - aces:
#       - destination:
#           any: true
#           port_protocol:
#             eq: telnet
#         dscp: af11
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           any: true
#           port_protocol:
#             eq: www
#       name: R1_TRAFFIC
#     afi: ipv6
#   invocation:
#     module_args:
#       config: null
#       running_config: null
#       state: gathered

# TASK [Setting host facts for pop_ace filter plugin] *************************
# ok: [xe_machine] => changed=false
#   ansible_facts:
#     acls_facts:
#     - acls:
#       - aces:
#         - destination:
#             address: 192.0.3.0
#             wildcard_bits: 0.0.0.255
#           dscp: ef
#           grant: deny
#           protocol: icmp
#           protocol_options:
#             icmp:
#               traceroute: true
#           sequence: 10
#           source:
#             address: 192.0.2.0
#             wildcard_bits: 0.0.0.255
#           ttl:
#             eq: 10
#         - destination:
#             host: 198.51.110.0
#             port_protocol:
#               eq: telnet
#           grant: deny
#           protocol: tcp
#           protocol_options:
#             tcp:
#               ack: true
#           sequence: 20
#           source:
#             host: 198.51.100.0
#         acl_type: extended
#         name: '110'
#       - aces:
#         - destination:
#             address: 198.51.101.0
#             port_protocol:
#               eq: telnet
#             wildcard_bits: 0.0.0.255
#           grant: deny
#           protocol: tcp
#           protocol_options:
#             tcp:
#               ack: true
#           sequence: 10
#           source:
#             address: 198.51.100.0
#             wildcard_bits: 0.0.0.255
#           tos:
#             service_value: 12
#         - destination:
#             address: 192.0.4.0
#             port_protocol:
#               eq: www
#             wildcard_bits: 0.0.0.255
#           dscp: ef
#           grant: deny
#           protocol: tcp
#           protocol_options:
#             tcp:
#               ack: true
#           sequence: 20
#           source:
#             address: 192.0.3.0
#             wildcard_bits: 0.0.0.255
#           ttl:
#             lt: 20
#         acl_type: extended
#         name: '123'
#       - aces:
#         - grant: deny
#           sequence: 10
#           source:
#             host: 192.168.1.200
#         - grant: deny
#           sequence: 20
#           source:
#             address: 192.168.2.0
#             wildcard_bits: 0.0.0.255
#         acl_type: standard
#         name: std_acl
#       - aces:
#         - destination:
#             address: 192.0.3.0
#             port_protocol:
#               eq: www
#             wildcard_bits: 0.0.0.255
#           grant: deny
#           option:
#             traceroute: true
#           protocol: tcp
#           protocol_options:
#             tcp:
#               fin: true
#           sequence: 10
#           source:
#             address: 192.0.2.0
#             wildcard_bits: 0.0.0.255
#           ttl:
#             eq: 10
#         acl_type: extended
#         name: test
#       afi: ipv4
#     - acls:
#       - aces:
#         - destination:
#             any: true
#             port_protocol:
#               eq: telnet
#           dscp: af11
#           grant: deny
#           protocol: tcp
#           protocol_options:
#             tcp:
#               ack: true
#           sequence: 10
#           source:
#             any: true
#             port_protocol:
#               eq: www
#         name: R1_TRAFFIC
#       afi: ipv6
#     filter_options:
#       match_all: true
#     match_criteria:
#       afi: ipv4
#       destination: 192.0.3.0
#       source: 192.0.2.0

# TASK [Invoke pop_ace filter plugin] *****************************************
# ok: [xe_machine] => changed=false
#   ansible_facts:
#     clean_acls:
#       clean_acls:
#         acls:
#         - acls:
#           - aces:
#             - destination:
#                 host: 198.51.110.0
#                 port_protocol:
#                   eq: telnet
#               grant: deny
#               protocol: tcp
#               protocol_options:
#                 tcp:
#                   ack: true
#               sequence: 20
#               source:
#                 host: 198.51.100.0
#             name: '110'
#           - aces:
#             - destination:
#                 address: 198.51.101.0
#                 port_protocol:
#                   eq: telnet
#                 wildcard_bits: 0.0.0.255
#               grant: deny
#               protocol: tcp
#               protocol_options:
#                 tcp:
#                   ack: true
#               sequence: 10
#               source:
#                 address: 198.51.100.0
#                 wildcard_bits: 0.0.0.255
#               tos:
#                 service_value: 12
#             - destination:
#                 address: 192.0.4.0
#                 port_protocol:
#                   eq: www
#                 wildcard_bits: 0.0.0.255
#               dscp: ef
#               grant: deny
#               protocol: tcp
#               protocol_options:
#                 tcp:
#                   ack: true
#               sequence: 20
#               source:
#                 address: 192.0.3.0
#                 wildcard_bits: 0.0.0.255
#               ttl:
#                 lt: 20
#             name: '123'
#           - aces:
#             - grant: deny
#               sequence: 10
#               source:
#                 host: 192.168.1.200
#             - grant: deny
#               sequence: 20
#               source:
#                 address: 192.168.2.0
#                 wildcard_bits: 0.0.0.255
#             name: std_acl
#           afi: ipv4
#         - acls:
#           - aces:
#             - destination:
#                 any: true
#                 port_protocol:
#                   eq: telnet
#               dscp: af11
#               grant: deny
#               protocol: tcp
#               protocol_options:
#                 tcp:
#                   ack: true
#               sequence: 10
#               source:
#                 any: true
#                 port_protocol:
#                   eq: www
#             name: R1_TRAFFIC
#           afi: ipv6
#       removed_aces:
#         acls:
#         - acls:
#           - aces:
#             - destination:
#                 address: 192.0.3.0
#                 wildcard_bits: 0.0.0.255
#               dscp: ef
#               grant: deny
#               protocol: icmp
#               protocol_options:
#                 icmp:
#                   traceroute: true
#               sequence: 10
#               source:
#                 address: 192.0.2.0
#                 wildcard_bits: 0.0.0.255
#               ttl:
#                 eq: 10
#             name: '110'
#           - aces:
#             - destination:
#                 address: 192.0.3.0
#                 port_protocol:
#                   eq: www
#                 wildcard_bits: 0.0.0.255
#               grant: deny
#               option:
#                 traceroute: true
#               protocol: tcp
#               protocol_options:
#                 tcp:
#                   fin: true
#               sequence: 10
#               source:
#                 address: 192.0.2.0
#                 wildcard_bits: 0.0.0.255
#               ttl:
#                 eq: 10
#             name: test
#           afi: ipv4
#         - acls: []
#           afi: ipv6

# TASK [Override ACLs config with device existing ACLs config] *******************
# changed: [xe_machine] => changed=true
#   after:
#   - acls:
#     - aces:
#       - destination:
#           host: 198.51.110.0
#           port_protocol:
#             eq: telnet
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           host: 198.51.100.0
#       acl_type: extended
#       name: '110'
#     - aces:
#       - destination:
#           address: 198.51.101.0
#           port_protocol:
#             eq: telnet
#           wildcard_bits: 0.0.0.255
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           address: 198.51.100.0
#           wildcard_bits: 0.0.0.255
#         tos:
#           service_value: 12
#       - destination:
#           address: 192.0.4.0
#           port_protocol:
#             eq: www
#           wildcard_bits: 0.0.0.255
#         dscp: ef
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           address: 192.0.3.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           lt: 20
#       acl_type: extended
#       name: '123'
#     - aces:
#       - grant: deny
#         sequence: 10
#         source:
#           host: 192.168.1.200
#       - grant: deny
#         sequence: 20
#         source:
#           address: 192.168.2.0
#           wildcard_bits: 0.0.0.255
#       acl_type: standard
#       name: std_acl
#     afi: ipv4
#   - acls:
#     - aces:
#       - destination:
#           any: true
#           port_protocol:
#             eq: telnet
#         dscp: af11
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           any: true
#           port_protocol:
#             eq: www
#       name: R1_TRAFFIC
#     afi: ipv6
#   before:
#   - acls:
#     - aces:
#       - destination:
#           address: 192.0.3.0
#           wildcard_bits: 0.0.0.255
#         dscp: ef
#         grant: deny
#         protocol: icmp
#         protocol_options:
#           icmp:
#             traceroute: true
#         sequence: 10
#         source:
#           address: 192.0.2.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           eq: 10
#       - destination:
#           host: 198.51.110.0
#           port_protocol:
#             eq: telnet
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           host: 198.51.100.0
#       acl_type: extended
#       name: '110'
#     - aces:
#       - destination:
#           address: 198.51.101.0
#           port_protocol:
#             eq: telnet
#           wildcard_bits: 0.0.0.255
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           address: 198.51.100.0
#           wildcard_bits: 0.0.0.255
#         tos:
#           service_value: 12
#       - destination:
#           address: 192.0.4.0
#           port_protocol:
#             eq: www
#           wildcard_bits: 0.0.0.255
#         dscp: ef
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 20
#         source:
#           address: 192.0.3.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           lt: 20
#       acl_type: extended
#       name: '123'
#     - aces:
#       - grant: deny
#         sequence: 10
#         source:
#           host: 192.168.1.200
#       - grant: deny
#         sequence: 20
#         source:
#           address: 192.168.2.0
#           wildcard_bits: 0.0.0.255
#       acl_type: standard
#       name: std_acl
#     - aces:
#       - destination:
#           address: 192.0.3.0
#           port_protocol:
#             eq: www
#           wildcard_bits: 0.0.0.255
#         grant: deny
#         option:
#           traceroute: true
#         protocol: tcp
#         protocol_options:
#           tcp:
#             fin: true
#         sequence: 10
#         source:
#           address: 192.0.2.0
#           wildcard_bits: 0.0.0.255
#         ttl:
#           eq: 10
#       acl_type: extended
#       name: test
#     afi: ipv4
#   - acls:
#     - aces:
#       - destination:
#           any: true
#           port_protocol:
#             eq: telnet
#         dscp: af11
#         grant: deny
#         protocol: tcp
#         protocol_options:
#           tcp:
#             ack: true
#         sequence: 10
#         source:
#           any: true
#           port_protocol:
#             eq: www
#       name: R1_TRAFFIC
#     afi: ipv6
#   commands:
#   - ip access-list extended 110
#   - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#   - no ip access-list extended test

"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.cisco.ios.plugins.plugin_utils.pop_ace import pop_ace


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _pop_ace(*args, **kwargs):
    """remove ace entries from a acl data"""

    keys = ["data", "filter_options", "match_criteria"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="pop_ace")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return pop_ace(**updated_data)


class FilterModule(object):
    """pop_ace"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"pop_ace": _pop_ace}
