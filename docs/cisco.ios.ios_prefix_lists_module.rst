.. _cisco.ios.ios_prefix_lists_module:


**************************
cisco.ios.ios_prefix_lists
**************************

**Prefix Lists resource module**


Version added: 2.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the attributes of prefix list on Cisco IOS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of configurations for Prefix lists.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>The Address Family Indicator (AFI) for the  prefix list.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of Prefix-lists.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Prefix-list specific description</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>entries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Prefix-lists supported params.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>deny</li>
                                    <li>permit</li>
                        </ul>
                </td>
                <td>
                        <div>Specify packets to be rejected or forwarded</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Prefix-list specific description</div>
                        <div>Description param at entries level is DEPRECATED</div>
                        <div>New Description is introduced at prefix_lists level, please use the Description param defined at prefix_lists level instead of Description param at entries level, as at this level description option will get removed in a future release.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ge</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum prefix length to be matched</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>le</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix length to be matched</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 prefix &lt;network&gt;/&lt;length&gt;, e.g., A.B.C.D/nn</div>
                        <div>IPv6 prefix &lt;network&gt;/&lt;length&gt;, e.g., X:X:X:X::X/&lt;0-128&gt;</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>sequence number of an entry</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of a prefix-list</div>
                </td>
            </tr>


            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>sh bgp</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>merged</em> is the default state which merges the want and have config, but for Prefix-List module as the IOS platform doesn&#x27;t allow update of Prefix-List over an pre-existing Prefix-List, same way Prefix-Lists resource module will error out for respective scenario and only addition of new Prefix-List over new sequence will be allowed with merge state.</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>sh running-config | section ^ip prefix-list|^ipv6 prefix-list</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSv Version 15.2 on VIRL
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html



Examples
--------

.. code-block:: yaml

    # Using deleted by Name

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Delete provided Prefix lists config by Prefix name
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: 10
              - name: test_prefix
        state: deleted

    #  Commands Fired:
    #  ---------------
    #
    #  "commands": [
    #         "no ip prefix-list 10",
    #         "no ip prefix-list test_prefix"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    # Using deleted by AFI

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Delete provided Prefix lists config by AFI
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
        state: deleted

    #  Commands Fired:
    #  ---------------
    #
    #  "commands": [
    #         "no ip prefix-list test",
    #         "no ip prefix-list 10",
    #         "no ip prefix-list test_prefix"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    # Using deleted without any config passed (NOTE: This will delete all Prefix lists configuration from device)

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Delete all Prefix lists config
      cisco.ios.ios_prefix_lists:
        state: deleted

    # Commands Fired:
    # ---------------
    #
    #  "commands": [
    #         "no ip prefix-list test",
    #         "no ip prefix-list 10",
    #         "no ip prefix-list test_prefix",
    #         "no ipv6 prefix-list test_ipv6"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # router-ios#

    # Using merged

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 description this is ipv6
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Merge provided Prefix lists configuration
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv6
            prefix_lists:
              - name: test_ipv6
                description: this is ipv6 merge test
                entries:
                  - action: deny
                    prefix: 2001:DB8:0:4::/64
                    ge: 80
                    le: 100
                    sequence: 10
        state: merged

    # After state:
    # -------------
    #
    # Play Execution fails, with error:
    # Cannot update existing sequence 10 of Prefix Lists test_ipv6 with state merged.
    # Please use state replaced or overridden.

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 description this is ipv6
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Merge provided Prefix lists configuration
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: 10
                description: this is new merge test
                entries:
                  - action: deny
                    prefix: 1.0.0.0/8
                    le: 15
                    sequence: 5
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 10
                    sequence: 10
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 15
                  - action: deny
                    prefix: 14.0.0.0/8
                    ge: 20
                    le: 21
                    sequence: 20
              - name: test
                description: this is merge test
                entries:
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 50
              - name: test_prefix
                description: this is for prefix-list
                entries:
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 10
                    le: 15
                    sequence: 5
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 20
                    sequence: 10
          - afi: ipv6
            prefix_lists:
              - name: test_ipv6
                description: this is ipv6 merge test
                entries:
                  - action: deny
                    prefix: 2001:DB8:0:4::/64
                    ge: 80
                    le: 100
                    sequence: 20
        state: merged

    #  Commands Fired:
    #  ---------------
    #
    #   "commands": [
    #         "ip prefix-list test description this is merge test",
    #         "ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15",
    #         "ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15",
    #         "ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
    #         "ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
    #         "ip prefix-list 10 description this is new merge test",
    #         "ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21",
    #         "ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20",
    #         "ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15",
    #         "ip prefix-list test_prefix description this is for prefix-list",
    #         "ipv6 prefix-list test_ipv6 seq 20 deny 2001:DB8:0:4::/64 ge 80 le 100",
    #         "ipv6 prefix-list test_ipv6 description this is ipv6 merge test"
    #     ]

    # After state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is new merge test
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is merge test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 merge test
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

    # Using overridden

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Override provided Prefix lists configuration
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: 10
                description: this is override test
                entries:
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 15
                  - action: deny
                    prefix: 14.0.0.0/8
                    ge: 20
                    le: 21
                    sequence: 20
              - name: test_override
                description: this is override test
                entries:
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 20
                    sequence: 10
          - afi: ipv6
            prefix_lists:
              - name: test_ipv6
                description: this is ipv6 override test
                entries:
                  - action: deny
                    prefix: 2001:DB8:0:4::/64
                    ge: 80
                    le: 100
                    sequence: 10
        state: overridden

    # Commands Fired:
    # ---------------
    #
    #  "commands": [
    #         "no ip prefix-list test",
    #         "no ip prefix-list test_prefix",
    #         "ip prefix-list 10 description this is override test",
    #         "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
    #         "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
    #         "ip prefix-list test_override seq 10 deny 35.0.0.0/8 ge 20",
    #         "ip prefix-list test_override description this is override test",
    #         "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
    #         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
    #         "ipv6 prefix-list test_ipv6 description this is ipv6 override test"
    #     ]

    # After state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is override test
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test_override description this is override test
    # ip prefix-list test_override seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 override test
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

    # Using replaced

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Replaced provided Prefix lists configuration
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: 10
                description: this is replace test
                entries:
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 15
                  - action: deny
                    prefix: 14.0.0.0/8
                    ge: 20
                    le: 21
                    sequence: 20
              - name: test_replace
                description: this is replace test
                entries:
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 20
                    sequence: 10
          - afi: ipv6
            prefix_lists:
              - name: test_ipv6
                description: this is ipv6 replace test
                entries:
                  - action: deny
                    prefix: 2001:DB8:0:4::/64
                    ge: 80
                    le: 100
                    sequence: 10
        state: replaced

    # Commands Fired:
    # ---------------
    #  "commands": [
    #         "ip prefix-list 10 description this is replace test",
    #         "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
    #         "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
    #         "ip prefix-list test_replace seq 10 deny 35.0.0.0/8 ge 20",
    #         "ip prefix-list test_replace description this is replace test",
    #         "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
    #         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
    #         "ipv6 prefix-list test_ipv6 description this is ipv6 replace test"
    #     ]

    # After state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is replace test
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ip prefix-list test_replace description this is replace test
    # ip prefix-list test_replace seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 replace test
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

    # Using Gathered

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Gather Prefix lists provided configurations
      cisco.ios.ios_prefix_lists:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #         {
    #             "afi": "ipv4",
    #             "prefix_lists": [
    #                 {
    #                     "description": "this is test description"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "le": 15,
    #                             "prefix": "1.0.0.0/8",
    #                             "sequence": 5
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 10,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 10
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 15,
    #                             "prefix": "12.0.0.0/8",
    #                             "sequence": 15
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 20,
    #                             "le": 21,
    #                             "prefix": "14.0.0.0/8",
    #                             "sequence": 20
    #                         }
    #                     ],
    #                     "name": "10"
    #                 },
    #                 {
    #                     "description": "this is test"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 15,
    #                             "prefix": "12.0.0.0/8",
    #                             "sequence": 50
    #                         }
    #                     ],
    #                     "name": "test"
    #                 },
    #                 {
    #                     "description": "this is for prefix-list"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 10,
    #                             "le": 15,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 5
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 20,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 10
    #                         }
    #                     ],
    #                     "name": "test_prefix"
    #                 }
    #             ]
    #         },
    #         {
    #             "afi": "ipv6",
    #             "prefix_lists": [
    #                 {
    #                     "description": "this is ipv6 prefix-list"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 80,
    #                             "prefix": "2001:DB8:0:4::/64",
    #                             "sequence": 10
    #                         }
    #                     ],
    #                     "name": "test_ipv6"
    #                 }
    #             ]
    #         }
    #     ]

    # After state:
    # ------------
    #
    # router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: 10
                description: this is new merge test
                entries:
                  - action: deny
                    prefix: 1.0.0.0/8
                    le: 15
                    sequence: 5
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 10
                    sequence: 10
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 15
                  - action: deny
                    prefix: 14.0.0.0/8
                    ge: 20
                    le: 21
                    sequence: 20
              - name: test
                description: this is merge test
                entries:
                  - action: deny
                    prefix: 12.0.0.0/8
                    ge: 15
                    sequence: 50
              - name: test_prefix
                description: this is for prefix-list
                entries:
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 10
                    le: 15
                    sequence: 5
                  - action: deny
                    prefix: 35.0.0.0/8
                    ge: 20
                    sequence: 10
          - afi: ipv6
            prefix_lists:
              - name: test_ipv6
                description: this is ipv6 merge test
                entries:
                  - action: deny
                    prefix: 2001:DB8:0:4::/64
                    ge: 80
                    le: 100
                    sequence: 10
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    #  "rendered": [
    #         "ip prefix-list test description this is test",
    #         "ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15",
    #         "ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15",
    #         "ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
    #         "ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
    #         "ip prefix-list 10 description this is test description",
    #         "ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21",
    #         "ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20",
    #         "ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15",
    #         "ip prefix-list test_prefix description this is for prefix-list",
    #         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 l2 100",
    #         "ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list"
    #     ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # ip prefix-list 10 description this is test description
    # ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
    # ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
    # ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
    # ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
    # ip prefix-list test description this is test
    # ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
    # ip prefix-list test_prefix description this is for prefix-list
    # ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
    # ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
    # ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
    # ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

    - name: Parse the provided configuration with the existing running configuration
      cisco.ios.ios_prefix_lists:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "afi": "ipv4",
    #             "prefix_lists": [
    #                 {
    #                     "description": "this is test description"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "le": 15,
    #                             "prefix": "1.0.0.0/8",
    #                             "sequence": 5
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 10,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 10
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 15,
    #                             "prefix": "12.0.0.0/8",
    #                             "sequence": 15
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 20,
    #                             "le": 21,
    #                             "prefix": "14.0.0.0/8",
    #                             "sequence": 20
    #                         }
    #                     ],
    #                     "name": "10"
    #                 },
    #                 {
    #                     "description": "this is test"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 15,
    #                             "prefix": "12.0.0.0/8",
    #                             "sequence": 50
    #                         }
    #                     ],
    #                     "name": "test"
    #                 },
    #                 {
    #                     "description": "this is for prefix-list"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 10,
    #                             "le": 15,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 5
    #                         },
    #                         {
    #                             "action": "deny",
    #                             "ge": 20,
    #                             "prefix": "35.0.0.0/8",
    #                             "sequence": 10
    #                         }
    #                     ],
    #                     "name": "test_prefix"
    #                 }
    #             ]
    #         },
    #         {
    #             "afi": "ipv6",
    #             "prefix_lists": [
    #                 {
    #                     "description": "this is ipv6 prefix-list"
    #                     "entries": [
    #                         {
    #                             "action": "deny",
    #                             "ge": 80,
    #                             "prefix": "2001:DB8:0:4::/64",
    #                             "sequence": 10
    #                         }
    #                     ],
    #                     "name": "test_ipv6"
    #                 }
    #             ]
    #         }
    #     ]



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when changed</td>
                <td>
                            <div>The resulting configuration model invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The configuration prior to the model invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip prefix-list 10 description this is test description&#x27;, &#x27;ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
