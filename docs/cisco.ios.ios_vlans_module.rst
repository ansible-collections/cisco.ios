.. Created with antsibull-docs 2.21.0

cisco.ios.ios_vlans module -- Resource module to configure VLANs.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `cisco.ios collection <https://galaxy.ansible.com/ui/repo/published/cisco/ios/>`_ (version 11.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible\-galaxy collection install cisco.ios`.

To use it in a playbook, specify: ``cisco.ios.ios_vlans``.

New in cisco.ios 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides declarative management of VLANs on Cisco IOS network devices.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="3"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config"></div>
      <p style="display: inline;"><strong>config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>A dictionary of VLANs options</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/member"></div>
      <p style="display: inline;"><strong>member</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/member" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Members of VLAN</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/member/evi"></div>
      <p style="display: inline;"><strong>evi</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/member/evi" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Ethernet Virtual Private Network (EVPN)</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/member/vni"></div>
      <p style="display: inline;"><strong>vni</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/member/vni" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>VXLAN vni</p>
    </td>
  </tr>

  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/mtu"></div>
      <p style="display: inline;"><strong>mtu</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/mtu" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>VLAN Maximum Transmission Unit.</p>
      <p>Refer to vendor documentation for valid values.</p>
      <p>This option is DEPRECATED use ios_interfaces to configure mtu, this attribute will be removed after 2027-01-01.</p>
      <p>mtu is collected as part of facts, but a mtu command wont be fired if the configuration is present in the playbook.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Ascii name of the VLAN.</p>
      <p>NOTE, <em>name</em> should not be named/appended with <em>default</em> as it is reserved for device default vlans.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/private_vlan"></div>
      <p style="display: inline;"><strong>private_vlan</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/private_vlan" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Options for private vlan configuration.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/private_vlan/associated"></div>
      <p style="display: inline;"><strong>associated</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/private_vlan/associated" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=integer</span>
      </p>
    </td>
    <td valign="top">
      <p>List of private VLANs associated with the primary . Only works with `type: primary`.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/private_vlan/type"></div>
      <p style="display: inline;"><strong>type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/private_vlan/type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Private VLAN type</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;primary&#34;</code></p></li>
        <li><p><code>&#34;isolated&#34;</code></p></li>
        <li><p><code>&#34;community&#34;</code></p></li>
      </ul>

    </td>
  </tr>

  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/remote_span"></div>
      <p style="display: inline;"><strong>remote_span</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/remote_span" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Configure as Remote SPAN VLAN</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/shutdown"></div>
      <p style="display: inline;"><strong>shutdown</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/shutdown" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Specifies whether VLAN switching should be administratively enabled or disabled.</p>
      <p>When set to <code class='docutils literal notranslate'>enabled</code>, the VLAN interface is administratively shut down, which prevents it from forwarding traffic.</p>
      <p>When set to <code class='docutils literal notranslate'>disabled</code>, the VLAN interface is administratively enabled by issuing the internal <code class='docutils literal notranslate'>no shutdown</code> command, allowing it to forward traffic.</p>
      <p>The operational state of the VLAN depends on both the administrative state (<code class='docutils literal notranslate'>shutdown</code> or <code class='docutils literal notranslate'>no shutdown</code>) and the physical link status.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;enabled&#34;</code></p></li>
        <li><p><code>&#34;disabled&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Operational state of the VLAN</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;active&#34;</code></p></li>
        <li><p><code>&#34;suspend&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vlan_id"></div>
      <p style="display: inline;"><strong>vlan_id</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vlan_id" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>ID of the VLAN. Range 1-4094</p>
    </td>
  </tr>

  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-running_config"></div>
      <p style="display: inline;"><strong>running_config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-running_config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option is used only with state <em>parsed</em>.</p>
      <p>The value of this option should be the output received from the IOS device by executing the command <b>show vlan</b>.</p>
      <p>The state <em>parsed</em> reads the configuration from <code class='docutils literal notranslate'>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</p>
    </td>
  </tr>
  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The state the configuration should be left in</p>
      <p>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</p>
      <p>The state <em>rendered</em> will transform the configuration in <code class='docutils literal notranslate'>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</p>
      <p>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</p>
      <p>The state <em>parsed</em> reads the configuration from <code class='docutils literal notranslate'>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code class='docutils literal notranslate'>running_config</code> option should be the same format as the output of commands <em>show vlan</em> and <em>show running-config | sec ^vlan configuration .+</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;merged&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;replaced&#34;</code></p></li>
        <li><p><code>&#34;overridden&#34;</code></p></li>
        <li><p><code>&#34;deleted&#34;</code></p></li>
        <li><p><code>&#34;rendered&#34;</code></p></li>
        <li><p><code>&#34;gathered&#34;</code></p></li>
        <li><p><code>&#34;purged&#34;</code></p></li>
        <li><p><code>&#34;parsed&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- Tested against Cisco IOS\-XE device with Version 17.13.01 on Cat9k on CML.
- Starting from v2.5.0, this module will fail when run against Cisco IOS devices that do not support VLANs. The offline states (\ :literal:`rendered` and :literal:`parsed`\ ) will work as expected.
- This module works with connection :literal:`network\_cli`. See \ `https://docs.ansible.com/ansible/latest/network/user\_guide/platform\_ios.html <https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html>`__


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
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-after"></div>
      <p style="display: inline;"><strong>after</strong></p>
      <a class="ansibleOptionLink" href="#return-after" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The resulting configuration after module execution.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when changed</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;This output will always be in the same format as the module argspec.\n&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-before"></div>
      <p style="display: inline;"><strong>before</strong></p>
      <a class="ansibleOptionLink" href="#return-before" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration prior to the module execution.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when <em>state</em> is <code class='docutils literal notranslate'>merged</code>, <code class='docutils literal notranslate'>replaced</code>, <code class='docutils literal notranslate'>overridden</code>, <code class='docutils literal notranslate'>deleted</code> or <code class='docutils literal notranslate'>purged</code></p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;This output will always be in the same format as the module argspec.\n&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-commands"></div>
      <p style="display: inline;"><strong>commands</strong></p>
      <a class="ansibleOptionLink" href="#return-commands" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The set of commands pushed to the remote device.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when <em>state</em> is <code class='docutils literal notranslate'>merged</code>, <code class='docutils literal notranslate'>replaced</code>, <code class='docutils literal notranslate'>overridden</code>, <code class='docutils literal notranslate'>deleted</code> or <code class='docutils literal notranslate'>purged</code></p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;vlan configuration 202&#34;, &#34;state active&#34;, &#34;remote-span&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-gathered"></div>
      <p style="display: inline;"><strong>gathered</strong></p>
      <a class="ansibleOptionLink" href="#return-gathered" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>Facts about the network resource gathered from the remote device as structured data.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when <em>state</em> is <code class='docutils literal notranslate'>gathered</code></p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;This output will always be in the same format as the module argspec.\n&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-parsed"></div>
      <p style="display: inline;"><strong>parsed</strong></p>
      <a class="ansibleOptionLink" href="#return-parsed" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The device native config provided in <em>running_config</em> option parsed into structured data as per module argspec.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when <em>state</em> is <code class='docutils literal notranslate'>parsed</code></p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;This output will always be in the same format as the module argspec.\n&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-rendered"></div>
      <p style="display: inline;"><strong>rendered</strong></p>
      <a class="ansibleOptionLink" href="#return-rendered" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The provided configuration in the task rendered in device-native format (offline).</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when <em>state</em> is <code class='docutils literal notranslate'>rendered</code></p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;vlan configuration 202&#34;, &#34;member evpn-instance 202 vni 10202&#34;, &#34;vlan 200&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
- Sagar Paul (@KB-perByte)
- Padmini Priyadarshini Sivaraj (@PadminiSivaraj)


Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible\-collections/cisco.ios/issues>`__
* `Repository (Sources) <https://github.com/ansible\-collections/cisco.ios>`__
