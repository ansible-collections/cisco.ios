.. _cisco.ios.ace_popper_filter:


********************
cisco.ios.ace_popper
********************

**Remove ace entries from a acl source of truth.**


Version added: 4.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin removes specific keys from a provided acl data.
- Using the parameters below- ``acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria``)




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This option represents a list of dictionaries of acls facts.</div>
                        <div>For example <code>acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria</code>), in this case <code>acls_data</code> represents this option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the target keys to remove in list format.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>failed_when</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>missing</b>&nbsp;&larr;</div></li>
                                    <li>never</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify aggregate mask</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remove</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>first</li>
                                    <li><div style="color: blue"><b>all</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify aggregate address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sticky</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify aggregate mask</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match_criteria</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the matching configuration of target keys and data attributes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>acl_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>ACL name</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify afi</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>destination_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Destination address of the ACE</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>grant</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Grant type permit or deny</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Protocol name</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Sequence number of the ACE</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Source address of the ACE</div>
                </td>
            </tr>

    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
