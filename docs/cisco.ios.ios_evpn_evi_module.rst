.. _cisco.ios.ios_evpn_evi_module:


***************************
cisco.ios.ios_evpn_evi
***************************

**Resource module to configure EVPN EVI.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of EVPN EVI on Cisco IOS devices.




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
                        <div>A dictionary of EVPN EVI options</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">int</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>EVPN instance value</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encapsulation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Default:</b>
                                    <li>vxlan</li>
                        </ul>
                </td>
                <td>
                        <div>EVPN encapsulation type</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>replication_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ingress</li>
                                    <li>static</li>
                        </ul>
                </td>
                <td>
                        <div>Method for replicating BUM traffic</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_distinguisher</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>EVPN Route Distinguisher</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_gateway</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Default gateway parameters</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Advertise Default Gateway MAC/IP routes</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable advertisement of Default Gateway MAC/IP routes</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Disable advertisement of Default Gateway MAC/IP routes</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP parameters</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>local_learning</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP local learning</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable IP local learning</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable IP local learning</div>
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
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in .</div>
                        <div>The module have declaratively similar behavior for replaced and overridden state.</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^router bgp</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>

                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.3 on CML.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html



Examples
--------

.. code-block:: yaml

    # Using state merged

    # Before state:
    # -------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_evpn_evi:
        config:
          - evi: 101
            replication_type: ingress
            route_distinguisher: '1:1'
            default_gateway:
              advertise:
                enable: False
            ip:
              local_learning:
                enable: True      
      
          - evi: 202
            replication_type: static
            default_gateway:
              advertise:
                enable: True
            ip:
              local_learning:
                disable: True 
        state: merged 

    # Commands Fired:
    # ---------------
    # "commands": [
    #     "l2vpn evpn instance 101 vlan-based",
    #     "ip local-learning enable",
    #     "replication-type ingress",
    #     "rd 1:1",
    #     "l2vpn evpn instance 202 vlan-based",
    #     "default-gateway advertise enable",
    #     "ip local-learning disable",
    #     "replication-type static"
    #     ],

    # After state:
    # ------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  rd 1:1
    #  replication-type ingress
    #  ip local-learning enable
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  ip local-learning disable
    #  default-gateway advertise enable

    # Using state replaced

    # Before state:
    # -------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  rd 1:1
    #  replication-type ingress
    #  ip local-learning enable
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  ip local-learning disable
    #  default-gateway advertise enable

    - name: Replaces the device configuration with the provided configuration
      cisco.ios.ios_evpn_evi:
        config:
          - evi: 101
            replication_type: ingress
            default_gateway:
              advertise:
                enable: True 
          - evi: 202
            replication_type: ingress
        state: replaced

    # Commands Fired:
    # ---------------
    # "commands": [
    #     "l2vpn evpn instance 101 vlan-based",
    #     "default-gateway advertise enable",
    #     "no ip local-learning enable",
    #     "no rd 1:1",
    #     "l2vpn evpn instance 202 vlan-based",
    #     "no default-gateway advertise enable",
    #     "no ip local-learning disable",
    #     "replication-type ingress"
    #     ],

    # After state:
    # ------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    #  default-gateway advertise enable
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress

    #  Using state overridden

    # Before state:
    # -------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    #  default-gateway advertise enable
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress

    - name: Override the device configuration with provided configuration
      cisco.ios.ios_evpn_evi:
        config:
          - evi: 101
            replication_type: ingress
            default_gateway:
              advertise:
                enable: True 
          - evi: 202
            replication_type: static
            default_gateway:
              advertise:
                enable: True 
        state: overridden

    # Commands Fired:
    # ---------------
    # "commands": [
    #     "no l2vpn evpn instance 102 vlan-based",
    #     "no l2vpn evpn instance 201 vlan-based",
    #     "l2vpn evpn instance 202 vlan-based",
    #     "default-gateway advertise enable",
    #     "replication-type static"
    #     ],

    # After state:
    # ------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    #  default-gateway advertise enable
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  default-gateway advertise enable
    # Using state Deleted
    
    # Before state:
    # -------------
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    #  default-gateway advertise enable
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  default-gateway advertise enable
    
    - name: "Delete the given EVI(s)"
      cisco.ios.ios_evpn_evi:
        config:
          - evi: 101
        state: deleted

    # Commands Fired:
    # ---------------      
    # "commands": [
    #       "no l2vpn evpn instance 101 vlan-based"
    #       ],
    
    # After state:
    # -------------
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  default-gateway advertise enable

    # Using state Deleted without any config passed

    # Before state:
    # -------------
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    #  default-gateway advertise enable

    - name: "Delete ALL EVIs"
      cisco.ios.ios_evpn_evi:
        state: deleted

    # Commands Fired:
    # ---------------
    # "commands": [
    #     "no l2vpn evpn instance 102 vlan-based",
    #     "no l2vpn evpn instance 202 vlan-based"
    #     ],

    # After state:
    # -------------
    # !

    # Using gathered

    # Before state:
    # -------------
    #
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !
    # l2vpn evpn instance 201 vlan-based
    #  encapsulation vxlan
    #  replication-type static
    # !
    # l2vpn evpn instance 202 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress

    - name: Gather facts for evpn_evi
      cisco.ios.ios_evpn_evi:
        config:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #   - evi: 101
    #     encapsulation: vxlan
    #     replication_type: static
    #   - evi: 102
    #     encapsulation: vxlan
    #     replication_type: ingress
    #   - evi: 201
    #     encapsulation: vxlan
    #     replication_type: static
    #   - evi: 202
    #     encapsulation: vxlan
    #     replication_type: ingress
    
    # Using Rendered
    
    - name: Rendered the provided configuration with the existing running configuration
      cisco.ios.ios_evpn_evi:
        config:
          - evi: 101
            replication_type: ingress
            default_gateway:
              advertise:
                enable: True 
          - evi: 202
            replication_type: ingress
        state: rendered

    # Task Output:
    # ------------
    #
    # rendered:
    # - l2vpn evpn instance 101 vlan-based
    # - default-gateway advertise enable
    # - replication-type ingress
    # - l2vpn evpn instance 202 vlan-based
    # - replication-type ingress


    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # l2vpn evpn instance 101 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    #  default-gateway advertise enable
    # !
    # l2vpn evpn instance 102 vlan-based
    #  encapsulation vxlan
    #  replication-type ingress
    # !

    - name: Parse the commands for provided configuration
      cisco.ios.ios_evpn_evi:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    #
    # parsed:
    #   - evi: 101
    #     encapsulation: vxlan
    #     replication_type: ingress
    #     default_gateway:
    #       advertise:
    #         enable: true
    #   - evi: 102
    #     encapsulation: vxlan
    #     replication_type: ingress



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
                      <span style="color: purple">dictionary</span>
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
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when state is <em>merged</em>, <em>replaced</em>,  <em>overridden</em>, or <em>deleted</em></td>
                <td>
                            <div>The configuration prior to the module execution.</div>
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
                <td>when state is <em>merged</em>, <em>replaced</em>, <em>overridden</em>, or <em>deleted</em></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;l2vpn evpn&#x27;, &#x27;replication-type ingress&#x27;, &#x27;router-id Loopback1&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
