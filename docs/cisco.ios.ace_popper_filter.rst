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
            msg: "{{ acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria) }}"
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




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
