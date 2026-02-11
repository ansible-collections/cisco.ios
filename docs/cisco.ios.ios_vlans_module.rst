.. _cisco.ios.ios_vlans_module:


*******************
cisco.ios.ios_vlans
*******************

**Resource module to configure VLANs.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VLANs on Cisco IOS network devices.




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
                        <div>A dictionary of VLANs options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>member</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Members of VLAN</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Ethernet Virtual Private Network (EVPN)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VXLAN vni</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VLAN Maximum Transmission Unit.</div>
                        <div>Refer to vendor documentation for valid values.</div>
                        <div>This option is DEPRECATED use ios_interfaces to configure mtu, this attribute will be removed after 2027-01-01.</div>
                        <div>mtu is collected as part of facts, but a mtu command wont be fired if the configuration is present in the playbook.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Ascii name of the VLAN.</div>
                        <div>NOTE, <em>name</em> should not be named/appended with <em>default</em> as it is reserved for device default vlans.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private_vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Options for private vlan configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>associated</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of private VLANs associated with the primary . Only works with `type: primary`.</div>
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
                                    <li>primary</li>
                                    <li>isolated</li>
                                    <li>community</li>
                        </ul>
                </td>
                <td>
                        <div>Private VLAN type</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_span</b>
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
                        <div>Configure as Remote SPAN VLAN</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>shutdown</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enabled</li>
                                    <li>disabled</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies whether VLAN switching should be administratively enabled or disabled.</div>
                        <div>When set to <code>enabled</code>, the VLAN interface is administratively shut down, which prevents it from forwarding traffic.</div>
                        <div>When set to <code>disabled</code>, the VLAN interface is administratively enabled by issuing the internal <code>no shutdown</code> command, allowing it to forward traffic.</div>
                        <div>The operational state of the VLAN depends on both the administrative state (<code>shutdown</code> or <code>no shutdown</code>) and the physical link status.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>active</li>
                                    <li>suspend</li>
                        </ul>
                </td>
                <td>
                        <div>Operational state of the VLAN</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ID of the VLAN. Range 1-4094</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show vlan</b>.</div>
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
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of commands <em>show vlan</em> and <em>show running-config | sec ^vlan configuration .+</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS-XE device with Version 17.13.01 on Cat9k on CML.
   - Starting from v2.5.0, this module will fail when run against Cisco IOS devices that do not support VLANs. The offline states (``rendered`` and ``parsed``) will work as expected.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_vlans:
        config:
          - name: Vlan_10
            vlan_id: 10
            state: active
            shutdown: disabled
            remote_span: true
          - name: Vlan_20
            vlan_id: 20
            mtu: 610
            state: active
            shutdown: enabled
          - name: Vlan_30
            vlan_id: 30
            state: suspend
            shutdown: enabled
        state: merged

    # After state:
    # ------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 10   vlan_10                          active
    # 20   vlan_20                          act/lshut
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     610   -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    # 10

    # Using merged

    # Before state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201


    - name: Merge provided configuration with device configuration
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 102
            member:
              vni: 10102
              evi: 102
          - vlan_id: 901
            member:
              vni: 50901
        state: merged

    # After state:
    # ------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201
    # vlan configuration 901
    #  member vni 50901

    # Using overridden

    # Before state:
    # -------------
    #
    # S1#show vlan

    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
    # 10   Vlan_10                          active
    # 20   Vlan_20                          active
    # 30   Vlan_30                          suspended
    # 44   Vlan_44                          suspended
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup

    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     610   -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 44   enet  100044     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------


    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------
    # S1#


    - name: Override device configuration of all VLANs with provided configuration
      cisco.ios.ios_vlans:
        config:
          - name: Vlan_2020
            state: active
            vlan_id: 20
            shutdown: disabled
        state: overridden

    # Task output:
    # ------------

    # after:
    # - mtu: 1500
    #   name: default
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 1
    # - mtu: 1500
    #   name: Vlan_2020
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 20
    # - mtu: 1500
    #   name: fddi-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1002
    # - mtu: 1500
    #   name: token-ring-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1003
    # - mtu: 1500
    #   name: fddinet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1004
    # - mtu: 1500
    #   name: trnet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1005

    # before:
    # - mtu: 1500
    #   name: default
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 1
    # - mtu: 1500
    #   name: Vlan_10
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 10
    # - mtu: 610
    #   name: Vlan_20
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 20
    # - mtu: 1500
    #   name: Vlan_30
    #   shutdown: disabled
    #   state: suspend
    #   vlan_id: 30
    # - mtu: 1500
    #   name: Vlan_44
    #   shutdown: disabled
    #   state: suspend
    #   vlan_id: 44
    # - mtu: 1500
    #   name: fddi-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1002
    # - mtu: 1500
    #   name: token-ring-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1003
    # - mtu: 1500
    #   name: fddinet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1004
    # - mtu: 1500
    #   name: trnet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1005

    # commands:
    # - no vlan 1
    # - no vlan 10
    # - no vlan 30
    # - no vlan 44
    # - no vlan 1002
    # - no vlan 1003
    # - no vlan 1004
    # - no vlan 1005
    # - vlan 20
    # - name Vlan_2020
    # - no mtu 610
    # - no vlan configuration 1
    # - no vlan configuration 10
    # - no vlan configuration 30
    # - no vlan configuration 44
    # - no vlan configuration 1002
    # - no vlan configuration 1003
    # - no vlan configuration 1004
    # - no vlan configuration 1005

    # After state:
    # ------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
    # 20   Vlan_2020                        active
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup

    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 20   enet  100020     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------


    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------

    # Using purged

    # Before state:
    # -------------
    #
    # S1#show vlan

    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
    # 20   Vlan_2020                        active
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup

    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 20   enet  100020     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------


    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------

    # S1#show running-config | section ^vlan configuration .+
    # vlan configuration 20


    - name: Purge all vlans configuration
      cisco.ios.ios_vlans:
        config:
        state: purged

    # Task output:
    # ------------

    # after:
    # - mtu: 1500
    #   name: default
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 1
    # - mtu: 1500
    #   name: fddi-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1002
    # - mtu: 1500
    #   name: token-ring-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1003
    # - mtu: 1500
    #   name: fddinet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1004
    # - mtu: 1500
    #   name: trnet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1005

    # before:
    # - mtu: 1500
    #   name: default
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 1
    # - mtu: 1500
    #   name: Vlan_2020
    #   shutdown: disabled
    #   state: active
    #   vlan_id: 20
    # - mtu: 1500
    #   name: fddi-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1002
    # - mtu: 1500
    #   name: token-ring-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1003
    # - mtu: 1500
    #   name: fddinet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1004
    # - mtu: 1500
    #   name: trnet-default
    #   shutdown: enabled
    #   state: active
    #   vlan_id: 1005

    # commands:
    # - no vlan 1
    # - no vlan 20
    # - no vlan 1002
    # - no vlan 1003
    # - no vlan 1004
    # - no vlan 1005
    # - no vlan configuration 1
    # - no vlan configuration 20
    # - no vlan configuration 1002
    # - no vlan configuration 1003
    # - no vlan configuration 1004
    # - no vlan configuration 1005

    # After state:
    # ------------
    #
    # S1#show vlan

    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup

    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------


    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------

    # S1#show running-config | section ^vlan configuration .+
    # S1#


    # Using replaced

    # Before state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 10   vlan_10                          active
    # 20   vlan_20                          act/lshut
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     610   -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    # 10

    - name: Replaces device configuration of listed VLANs with provided configuration
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 20
            name: Test_VLAN20
            mtu: 700
            shutdown: disabled
          - vlan_id: 50
            name: pvlan-isolated
            private_vlan:
              type: isolated
          - vlan_id: 60
            name: pvlan-community
            private_vlan:
              type: community
          - vlan_id: 70
            name: pvlan-primary
            private_vlan:
              type: primary
              associated:
                - 50
                - 60

        state: replaced

    # After state:
    # ------------
    #
    # vios_l2#sh vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
    # 10   Vlan_10                          active
    # 20   Test_VLAN20                      active
    # 50   pvlan-isolated                   active
    # 60   pvlan-community                  active
    # 70   pvlan-primary                    active
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1000  -      -      -        -    -        0      0
    # 20   enet  100020     700   -      -      -        -    -        0      0
    # 50   enet  100050     1500  -      -      -        -    -        0      0
    # 60   enet  100051     1500  -      -      -        -    -        0      0
    # 70   enet  100059     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    #
    #
    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------
    # 70      50        isolated
    # 70      60        community

    # Using deleted

    # Before state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 10   vlan_10                          active
    # 20   vlan_20                          act/lshut
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     610   -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    # 10

    - name: Delete attributes of given VLANs
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 10
          - vlan_id: 20
        state: deleted

    # After state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Using deleted

    # Before state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201
    # vlan configuration 901
    #  member vni 50901

    - name: Delete attributes of given VLANs
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 101
        state: deleted

    # After state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201
    # vlan configuration 901
    #  member vni 50901

    # Using Deleted without any config passed
    # "(NOTE: This will delete all of configured vlans attributes)"

    # Before state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 10   vlan_10                          active
    # 20   vlan_20                          act/lshut
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     610   -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    # 10

    - name: Delete attributes of ALL VLANs
      cisco.ios.ios_vlans:
        state: deleted

    # After state:
    # -------------
    #
    # vios_l2#show vlan
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    # Using Deleted without any config passed
    # "(NOTE: This will delete all of configured vlans attributes)"

    # Before state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201
    # vlan configuration 202
    #  member evpn-instance 202 vni 10202
    # vlan configuration 901
    #  member vni 50901

    - name: Delete attributes of ALL VLANs
      cisco.ios.ios_vlans:
        state: deleted

    # After state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # no vlan configuration 101
    # no vlan configuration 102
    # no vlan configuration 201
    # no vlan configuration 202
    # no vlan configuration 901
    # no vlan configuration 902

    # Using gathered, vlan configuration only

    # Before state:
    # -------------
    #
    # Leaf-01#show run nve | sec ^vlan configuration
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 201
    #  member evpn-instance 201 vni 10201
    # vlan configuration 202
    #  member evpn-instance 202 vni 10202
    # vlan configuration 901
    #  member vni 50901

    - name: Gather listed vlans with provided configurations
      cisco.ios.ios_vlans:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # gathered = [
    #     {
    #         "member": {
    #             "evi": 101,
    #             "vni": 10101
    #         },
    #         "vlan_id": 101
    #     },
    #     {
    #         "member": {
    #             "evi": 102,
    #             "vni": 10102
    #         },
    #         "vlan_id": 102
    #     },
    #     {
    #         "member": {
    #             "evi": 201,
    #             "vni": 10201
    #         },
    #         "vlan_id": 201
    #     },
    #     {
    #         "member": {
    #             "evi": 202,
    #             "vni": 10202
    #         },
    #         "vlan_id": 202
    #     },
    #     {
    #         "member": {
    #             "vni": 50901
    #         },
    #         "vlan_id": 901
    #     },
    #     {
    #         "member": {
    #             "vni": 50902
    #         },
    #         "vlan_id": 902
    #     }
    # ]

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_vlans:
        config:
          - name: Vlan_10
            vlan_id: 10
            state: active
            shutdown: disabled
            remote_span: true
          - name: Vlan_20
            vlan_id: 20
            mtu: 610
            state: active
            shutdown: enabled
          - name: Vlan_30
            vlan_id: 30
            state: suspend
            shutdown: enabled
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "vlan 10",
    #         "name Vlan_10",
    #         "state active",
    #         "remote-span",
    #         "no shutdown",
    #         "vlan 20",
    #         "name Vlan_20",
    #         "state active",
    #         "mtu 610",
    #         "shutdown",
    #         "vlan 30",
    #         "name Vlan_30",
    #         "state suspend",
    #         "shutdown"
    #     ]

    # Using Rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 101
            member:
              vni: 10101
              evi: 101
          - vlan_id: 102
            member:
              vni: 10102
              evi: 102
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #     "vlan configuration 101",
    #     "member evpn-instance 101 vni 10101",
    #     "vlan configuration 102",
    #     "member evpn-instance 102 vni 10102"
    # ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 10   vlan_10                          active
    # 20   vlan_20                          act/lshut
    # 30   vlan_30                          sus/lshut
    # 1002 fddi-default                     act/unsup
    # 1003 token-ring-default               act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trnet-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 20   enet  100020     1500  -      -      -        -    -        0      0
    # 30   enet  100030     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 tr    101003     1500  -      -      -        -    -        0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

    - name: Parse the commands for provided configuration
      cisco.ios.ios_vlans:
        running_config: "{{ lookup('file', './parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "mtu": 1500,
    #             "name": "default",
    #             "shutdown": "disabled",
    #             "state": "active",
    #             "vlan_id": 1
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "vlan_10",
    #             "shutdown": "disabled",
    #             "state": "active",
    #             "vlan_id": 10
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "vlan_20",
    #             "shutdown": "enabled",
    #             "state": "active",
    #             "vlan_id": 20
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "vlan_30",
    #             "shutdown": "enabled",
    #             "state": "suspend",
    #             "vlan_id": 30
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "fddi-default",
    #             "shutdown": "enabled",
    #             "state": "active",
    #             "vlan_id": 1002
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "token-ring-default",
    #             "shutdown": "enabled",
    #             "state": "active",
    #             "vlan_id": 1003
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "fddinet-default",
    #             "shutdown": "enabled",
    #             "state": "active",
    #             "vlan_id": 1004
    #         },
    #         {
    #             "mtu": 1500,
    #             "name": "trnet-default",
    #             "shutdown": "enabled",
    #             "state": "active",
    #             "vlan_id": 1005
    #         }
    #     ]

    # Using Parsed Vlan configuration only

    # File: parsed.cfg
    # ----------------
    #
    # vlan configuration 101
    #  member evpn-instance 101 vni 10101
    # vlan configuration 102
    #  member evpn-instance 102 vni 10102
    # vlan configuration 901
    #  member vni 50901

    - name: Parse the commands for provided configuration
      cisco.ios.ios_vlans:
        running_config: "{{ lookup('file', './parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #     {
    #         "member": {
    #             "evi": 101,
    #             "vni": 10101
    #         },
    #         "vlan_id": 101
    #     },
    #     {
    #         "member": {
    #             "evi": 102,
    #             "vni": 10102
    #         },
    #         "vlan_id": 102
    #     },
    #     {
    #         "member": {
    #             "vni": 50901
    #         },
    #         "vlan_id": 901
    #     }
    # ]

    # Using Parsed, Vlan and vlan configuration

    # File: parsed.cfg
    # ----------------
    #
    # VLAN Name                             Status    Ports
    # ---- -------------------------------- --------- -------------------------------
    # 1    default                          active    Gi0/1, Gi0/2
    # 101  RemoteIsInMyName                 act/unsup Fa0/1, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8, Fa0/9, Fa0/10, Fa0/11, Fa0/12
    #                                                 Fa0/13, Fa0/14, Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20, Fa0/21
    #                                                 Fa0/22, Fa0/23, Fa0/24, Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
    #                                                 Fa0/31, Fa0/32, Fa0/33, Fa0/34, Fa0/35, Fa0/36, Fa0/37, Fa0/38, Fa0/39
    #                                                 Fa0/40, Fa0/41, Fa0/42, Fa0/43, Fa0/44, Fa0/45, Fa0/46, Fa0/47, Fa0/48
    # 150  VLAN0150                         active
    # 888  a_very_long_vlan_name_a_very_long_vlan_name
    #                                     active
    # 1002 fddi-default                     act/unsup
    # 1003 trcrf-default                    act/unsup
    # 1004 fddinet-default                  act/unsup
    # 1005 trbrf-default                    act/unsup
    #
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 101  enet  100101     610   -      -      -        -    -        0      0
    # 150  enet  100150     1500  -      -      -        -    -        0      0
    # 888  enet  100888     1500  -      -      -        -    -        0      0
    # 1002 fddi  101002     1500  -      -      -        -    -        0      0
    # 1003 trcrf 101003     4472  1005   3276   -        -    srb      0      0
    # 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
    # 1005 trbrf 101005     4472  -      -      15       ibm  -        0      0
    #
    #
    # VLAN AREHops STEHops Backup CRF
    # ---- ------- ------- ----------
    # 1003 7       7       off
    #
    # Remote SPAN VLANs
    # ------------------------------------------------------------------------------
    # 150
    #
    # Primary Secondary Type              Ports
    # ------- --------- ----------------- ------------------------------------------
    #
    # vlan configuration 101
    #   member evpn-instance 101 vni 10101
    # vlan configuration 102
    #   member evpn-instance 102 vni 10102
    # vlan configuration 901
    #   member vni 50901

    - name: Parse the commands for provided configuration
      cisco.ios.ios_vlans:
        running_config: "{{ lookup('file', './parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #     {
    #         "name": "default",
    #         "vlan_id": 1,
    #         "state": "active",
    #         "shutdown": "disabled",
    #         "mtu": 1500,
    #     },
    #     {
    #         "name": "RemoteIsInMyName",
    #         "vlan_id": 101,
    #         "state": "active",
    #         "shutdown": "enabled",
    #         "mtu": 610,
    #         "member": {"evi": 101, "vni": 10101},
    #     },
    #     {
    #         "name": "VLAN0150",
    #         "vlan_id": 150,
    #         "state": "active",
    #         "shutdown": "disabled",
    #         "mtu": 1500,
    #         "remote_span": True,
    #     },
    #     {
    #         "name": "a_very_long_vlan_name_a_very_long_vlan_name",
    #         "vlan_id": 888,
    #         "state": "active",
    #         "shutdown": "disabled",
    #         "mtu": 1500,
    #     },
    #     {
    #         "name": "fddi-default",
    #         "vlan_id": 1002,
    #         "state": "active",
    #         "shutdown": "enabled",
    #         "mtu": 1500,
    #     },
    #     {
    #         "name": "trcrf-default",
    #         "vlan_id": 1003,
    #         "state": "active",
    #         "shutdown": "enabled",
    #         "mtu": 4472,
    #     },
    #     {
    #         "name": "fddinet-default",
    #         "vlan_id": 1004,
    #         "state": "active",
    #         "shutdown": "enabled",
    #         "mtu": 1500,
    #     },
    #     {
    #         "name": "trbrf-default",
    #         "vlan_id": 1005,
    #         "state": "active",
    #         "shutdown": "enabled",
    #         "mtu": 4472,
    #     },
    #     {"vlan_id": 102, "member": {"evi": 102, "vni": 10102}},
    #     {"vlan_id": 901, "member": {"vni": 50901}},
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vlan configuration 202&#x27;, &#x27;state active&#x27;, &#x27;remote-span&#x27;]</div>
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
                            <div>The provided configuration in the task rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vlan configuration 202&#x27;, &#x27;member evpn-instance 202 vni 10202&#x27;, &#x27;vlan 200&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
- Sagar Paul (@KB-perByte)
- Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
