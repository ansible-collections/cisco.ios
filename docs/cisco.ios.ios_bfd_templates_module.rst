.. _cisco.ios.ios_bfd_templates_module:


***************************
cisco.ios.ios_bfd_templates
***************************

**Bidirectional Forwarding Detection (BFD) templates configurations**


Version added: 11.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manages Bidirectional Forwarding Detection (BFD) templates configurations




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="3">
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
                        <div>A dictionary of bfd template options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure authentication for the BFD template</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keychain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the key chain to use for authentication</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>sha_1</li>
                                    <li>md5</li>
                                    <li>meticulous_md5</li>
                                    <li>meticulous_sha_1</li>
                        </ul>
                </td>
                <td>
                        <div>Authentication type to use for BFD sessions</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dampening</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>enables session dampening</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>half_life_period</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>half-life period for the exponential decay algorithm, in minutes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_suppress_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The maximum amount of time a session can be suppressed, in minutes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reuse_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The threshold at which a dampened session is allowed to be reused (taken out of dampening), in milliseconds.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suppress_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The threshold at which a session is suppressed (put into dampening), in milliseconds.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>echo</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>enables the BFD echo function for all interfaces which uses this specific template.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hop</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>single_hop</li>
                                    <li>multi_hop</li>
                        </ul>
                </td>
                <td>
                        <div>type of template to be used</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>defines transmit interval between BFD packets</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_rx</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The minimum interval in milliseconds that the local system is capable of supporting between received BFD control packets</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_tx</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The minimum interval in milliseconds that the local system desires for transmitting BFD control packets</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multiplier</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the number of consecutive BFD control packets that must be missed from a BFD peer before BFD declares                         that the peer is unavailable and the Layer 3 BFD peer is informed of the failure.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name of the BFD template to be used</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^bfd-template</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>purged</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^bfd-template</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                        <div>The state <code>deleted</code> does not support or guarantee granular deletion of configuration the playbook should act as source of truth, and the desired state of the resouce is what the playbook should reflect. Use <code>overridden</code> or <code>replaced</code> to get extra configuration removed.</div>
                        <div>The state <em>purged</em> removes BFD templates completely using a single top-level <code>no bfd-template</code> command, which removes the entire template definition at once.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS XE Software, Version 17.13.01a on CML
   - This module works with connection ``network_cli``
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Using merged
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # (no BFD templates configured)

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
            interval:
              min_tx: 200
              min_rx: 200
              multiplier: 3
            authentication:
              type: sha_1
              keychain: bfd_keychain
            echo: true
          - name: template2
            hop: multi_hop
            interval:
              min_tx: 500
              min_rx: 500
              multiplier: 5
            dampening:
              half_life_period: 30
              reuse_threshold: 2000
              suppress_threshold: 5000
              max_suppress_time: 120
        state: merged

    # Commands Fired:
    # ---------------
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    #  authentication sha-1 keychain bfd_keychain
    #  echo
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5
    #  dampening 30 2000 5000 120

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    #  authentication sha-1 keychain bfd_keychain
    #  echo
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5
    #  dampening 30 2000 5000 120

    # Using replaced
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    #  authentication sha-1 keychain bfd_keychain
    #  echo
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    - name: Replace device configuration of specified BFD templates with provided configuration
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
            interval:
              min_tx: 300
              min_rx: 300
              multiplier: 4
            authentication:
              type: sha_1
              keychain: new_keychain
        state: replaced

    # Commands Fired:
    # ---------------
    # bfd-template single-hop template1
    #  no echo
    #  interval min-tx 300 min-rx 300 multiplier 4
    #  no authentication sha-1 keychain bfd_keychain
    #  authentication sha-1 keychain new_keychain

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 300 min-rx 300 multiplier 4
    #  authentication sha-1 keychain new_keychain
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    # Using overridden
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5
    # bfd-template single-hop template3
    #  echo

    - name: Override device configuration with provided configuration
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
            interval:
              min_tx: 300
              min_rx: 300
              multiplier: 5
            authentication:
              type: md5
              keychain: secure_key
        state: overridden

    # Commands Fired:
    # ---------------
    # no bfd-template multi-hop template2
    # no bfd-template single-hop template3
    # bfd-template single-hop template1
    #  interval min-tx 300 min-rx 300 multiplier 5
    #  authentication md5 keychain secure_key

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 300 min-rx 300 multiplier 5
    #  authentication md5 keychain secure_key

    # Using deleted
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    #  authentication sha-1 keychain bfd_keychain
    #  echo
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    - name: Delete specified BFD template
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
        state: deleted

    # Commands Fired:
    # ---------------
    # bfd-template single-hop template1
    #  no echo
    #  no interval min-tx 200 min-rx 200 multiplier 3
    #  no authentication sha-1 keychain bfd_keychain

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    # Using deleted (to delete all BFD templates )
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    - name: Delete all BFD template configurations
      cisco.ios.ios_bfd_templates:
        state: deleted

    # Commands Fired:
    # ---------------
    # bfd-template single-hop template1
    #  no interval min-tx 200 min-rx 200 multiplier 3
    # bfd-template multi-hop template2
    #  no interval min-tx 500 min-rx 500 multiplier 5

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    # bfd-template multi-hop template2

    # Using purged
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    - name: Purge specified BFD template configurations (complete removal)
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
        state: purged

    # Commands Fired:
    # ---------------
    # no bfd-template single-hop template1

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5

    # Using purged (to remove all BFD templates)
    # Before state:
    # -------------
    # router-ios#show running-config | section ^bfd-template
    # bfd-template single-hop template1
    #  interval min-tx 200 min-rx 200 multiplier 3
    #  authentication sha-1 keychain bfd_keychain
    # bfd-template multi-hop template2
    #  interval min-tx 500 min-rx 500 multiplier 5
    # bfd-template single-hop template3
    #  echo

    - name: Purge all BFD template configurations (complete removal)
      cisco.ios.ios_bfd_templates:
        config: []
        state: purged

    # Commands Fired:
    # ---------------
    # no bfd-template single-hop template1
    # no bfd-template multi-hop template2
    # no bfd-template single-hop template3

    # After state:
    # ------------
    # router-ios#show running-config | section ^bfd-template
    # (no BFD templates configured)

    # Using rendered
    - name: Render platform specific commands from task input using rendered state
      cisco.ios.ios_bfd_templates:
        config:
          - name: template1
            hop: single_hop
            interval:
              min_tx: 200
              min_rx: 200
              multiplier: 3
            authentication:
              type: meticulous_sha_1
              keychain: secure_chain
            echo: true
        state: rendered

    # Module Execution Result:
    # ------------------------
    # "rendered": [
    #     "bfd-template single-hop template1",
    #     "interval min-tx 200 min-rx 200 multiplier 3",
    #     "authentication meticulous-sha-1 keychain secure_chain",
    #     "echo"
    # ]

    # Using gathered
    - name: Gather BFD template configuration from the device
      cisco.ios.ios_bfd_templates:
        state: gathered

    # Module Execution Result:
    # ------------------------
    # "gathered": [
    #     {
    #         "name": "template1",
    #         "hop": "single_hop",
    #         "interval": {
    #             "min_tx": 200,
    #             "min_rx": 200,
    #             "multiplier": 3
    #         },
    #         "authentication": {
    #             "type": "sha_1",
    #             "keychain": "bfd_keychain"
    #         },
    #         "echo": true
    #     }
    # ]

    # Using parsed
    - name: Parse the provided configuration to structured format
      cisco.ios.ios_bfd_templates:
        running_config: |
          bfd-template single-hop template1
           interval min-tx 200 min-rx 200 multiplier 3
           authentication sha-1 keychain bfd_keychain
           echo
          bfd-template multi-hop template2
           dampening 30 2000 5000 120
        state: parsed

    # Module Execution Result:
    # ------------------------
    # "parsed": [
    #     {
    #         "name": "template1",
    #         "hop": "single_hop",
    #         "interval": {
    #             "min_tx": 200,
    #             "min_rx": 200,
    #             "multiplier": 3
    #         },
    #         "authentication": {
    #             "type": "sha_1",
    #             "keychain": "bfd_keychain"
    #         },
    #         "echo": true
    #     },
    #     {
    #         "name": "template2",
    #         "hop": "multi_hop",
    #         "dampening": {
    #             "half_life_period": 30,
    #             "reuse_threshold": 2000,
    #             "suppress_threshold": 5000,
    #             "max_suppress_time": 120
    #         }
    #     }
    # ]



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
                            <div>The resulting configuration after module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
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
                            <div>The configuration prior to the module invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;bfd-template single-hop template1&#x27;, &#x27;interval min-tx 200 min-rx 200 multiplier 3&#x27;, &#x27;authentication sha-1 keychain bfd_keychain&#x27;, &#x27;echo&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>gathered</code></td>
                <td>
                            <div>Facts about the network resource gathered from the remote device as structured data.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>parsed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>parsed</code></td>
                <td>
                            <div>The device native config provided in <em>running_config</em> option parsed into structured data as per module argspec.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>rendered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>rendered</code></td>
                <td>
                            <div>The provided configuration in the task rendered in device native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;bfd-template single-hop template1&#x27;, &#x27;interval min-tx 200 min-rx 200 multiplier 3&#x27;, &#x27;authentication sha-1 keychain bfd_keychain&#x27;, &#x27;echo&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Komal Desai (@komaldesai13)
