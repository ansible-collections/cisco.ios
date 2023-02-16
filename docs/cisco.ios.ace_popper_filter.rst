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
- Using the parameters below - ``acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria``)




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
                        <div>Specify filtering options which drives the filter plugin.</div>
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
                        <div>On missing it fails when there is no match with the ACL data supplied</div>
                        <div>On never it would never fail</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match_all</b>
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
                        <div>When true ensures ace removed only when it matches all match criteria</div>
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
                        <div>Remove first removes one ace from each ACL entry on match</div>
                        <div>Remove all is more aggressive and removes more than one on match</div>
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
                        <div>Specify the matching configuration of the ACEs to remove.</div>
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
                        <div>ACL name to match</div>
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
                        <div>Specify afi to match</div>
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
                        <div>Destination address of the ACE to natch</div>
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
                        <div>Grant type permit or deny to match</div>
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
                        <div>Protocol name of the ACE to match</div>
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
                        <div>Sequence number of the ACE to match</div>
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
                        <div>Source address of the ACE to match</div>
                </td>
            </tr>

    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    ##Playbook with filter plugin example
      vars:
        filter_options:
          match_all: true
        match_criteria:
          afi: "ipv4"
          source_address: "192.0.2.0"
          destination_address: "192.0.3.0"
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
            msg: "{{ acls_data | cisco.ios.ace_popper(filter_options=filter_options, match_criteria=match_criteria) }}"

    ##Output
    # PLAY [Filter plugin example ace_popper] ******************************************************************************************************************

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
    - name: Gather ACLs config from device existing ACLs config
      cisco.ios.ios_acls:
        state: gathered
      register: result_gathered

    - name: Setting host facts for ace_popper filter plugin
      ansible.builtin.set_fact:
        acls_facts: "{{ result_gathered.gathered }}"
        filter_options:
          match_all: true
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


    ##Output

    # PLAYBOOK: acl_popper_example.yml ***********************************************

    # PLAY [Filter plugin example ace_popper] ****************************************

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

    # TASK [Setting host facts for ace_popper filter plugin] *************************
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
    #       destination_address: 192.0.3.0
    #       source_address: 192.0.2.0

    # TASK [Invoke ace_popper filter plugin] *****************************************
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




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
