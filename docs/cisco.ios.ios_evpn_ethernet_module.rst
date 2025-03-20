.. _cisco.ios.ios_evpn_ethernet_module:


***************************
cisco.ios.ios_evpn_ethernet
***************************

**Resource module to configure L2VPN EVPN Ethernet Segment.**


Version added: 9.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the L2VPN EVPN Ethernet Segment attributes of Cisco IOS network devices.




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
                        <div>A dictionary of L2VPN EVPN Ethernet Segment options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default</b>
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
                        <div>Set a command to its defaults</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>df_election</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Designated forwarder election parameters</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>preempt_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Preempt time before advertising routes</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wait_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Designated forwarder election wait time</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>identifier</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Ethernet Segment Identifiers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>esi_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>system mac or 9-octet ESI value in hex</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>identifier_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>0</li>
                                    <li>3</li>
                        </ul>
                </td>
                <td>
                        <div>Type 0 (arbitrary 9-octet ESI value)</div>
                        <div>Type 3 (MAC-based ESI value)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redundancy</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multi-homing redundancy parameters</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>all_active</b>
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
                        <div>Per-flow load-balancing between PEs on same Ethernet Segment</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>single_active</b>
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
                        <div>Per-vlan load-balancing between PEs on same Ethernet Segment</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>segment</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>L2VPN EVPN Ethernet Segment, l2vpn evpn ethernet-segment 1</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^l2vpn</b>.</div>
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
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^l2vpn</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                        <div>The state <em>purged</em> negates virtual/logical interfaces that are specified in task from running-config.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.16.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - The module examples uses callback plugin (callback_result_format=yaml) to generate task output in yaml format.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
          - identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.01
            redundancy:
              single_active: true
            segment: '1'
          - df_election:
              preempt_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.02
            redundancy:
              single_active: true
            segment: '2'
          - identifier:
              identifier_type: '3'
              esi_value: 00.00.00.00.00.00.00.00.03
            redundancy:
              single_active: true
            segment: '3'
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.04
            redundancy:
              all_active: true
            segment: '4'
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.05
            redundancy:
              all_active: true
            segment: '5'
        state: merged

    # Task Output
    # -----------
    #
    # before:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    # commands:
    # - l2vpn evpn ethernet-segment 5
    # - identifier type 0 00.00.00.00.00.00.00.00.05
    # - redundancy all-active
    # - df-election wait-time 1
    # after:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.05
    #    redundancy:
    #        all_active: true
    #    segment: '5'

    # After state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !
    # l2vpn evpn ethernet-segment 5
    #  identifier type 0 00.00.00.00.00.00.00.00.05
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.04
            redundancy:
              single_active: true
            segment: '4'
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.05
            redundancy:
              all_active: true
            segment: '5'
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    # commands:
    # - l2vpn evpn ethernet-segment 4
    # - redundancy single-active
    # - l2vpn evpn ethernet-segment 5
    # - identifier type 0 00.00.00.00.00.00.00.00.05
    # - redundancy all-active
    # - df-election wait-time 1
    # after:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        single_active: true
    #    segment: '4'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.05
    #    redundancy:
    #        all_active: true
    #    segment: '5'

    # After state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy single-active
    #  df-election wait-time 1
    # !
    # l2vpn evpn ethernet-segment 5
    #  identifier type 0 00.00.00.00.00.00.00.00.05
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.04
            redundancy:
              single_active: true
            segment: '4'
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.05
            redundancy:
              all_active: true
            segment: '5'
        state: overridden

    # After state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy single-active
    #  df-election wait-time 1
    # !
    # l2vpn evpn ethernet-segment 5
    #  identifier type 0 00.00.00.00.00.00.00.00.05
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    # Using deleted

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
          - identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.01
            redundancy:
              single_active: true
            segment: '1'
          - df_election:
              preempt_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.02
            redundancy:
              single_active: true
            segment: '2'
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #  - identifier:
    #      identifier_type: '0'
    #      esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #      single_active: true
    #    segment: '1'
    #  - df_election:
    #      preempt_time: 1
    #    identifier:
    #      identifier_type: '0'
    #      esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #      single_active: true
    #    segment: '2'
    #  - identifier:
    #      identifier_type: '3'
    #      esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #      single_active: true
    #    segment: '3'
    #  - df_election:
    #      wait_time: 1
    #    identifier:
    #      identifier_type: '0'
    #      esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #      all_active: true
    #    segment: '4'
    # commands:
    # - l2vpn evpn ethernet-segment 1
    # - no identifier type 0 00.00.00.00.00.00.00.00.01
    # - no redundancy single-active
    # - l2vpn evpn ethernet-segment 2
    # - no identifier type 0 00.00.00.00.00.00.00.00.02
    # - no redundancy single-active
    # - no df-election wait-time 1
    # after:
    #  - segment: '1'
    #  - segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.05
    #    redundancy:
    #        all_active: true
    #    segment: '5'

    # After state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    # !
    # l2vpn evpn ethernet-segment 2
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !
    # l2vpn evpn ethernet-segment 5
    #  identifier type 0 00.00.00.00.00.00.00.00.05
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    # Using purged

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
          - segment: '1'
          - segment: '2'
        state: purged

    # Task Output
    # -----------
    #
    # before:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    # commands:
    # - no l2vpn evpn ethernet-segment 1
    # - no l2vpn evpn ethernet-segment 2
    # after:
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.05
    #    redundancy:
    #        all_active: true
    #    segment: '5'

    # After state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !
    # l2vpn evpn ethernet-segment 5
    #  identifier type 0 00.00.00.00.00.00.00.00.05
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    # Using gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^l2vpn evpn ethernet-segment
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Gather facts of evpn ethernet segment
      cisco.ios.ios_evpn_ethernet:
        config:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'

    # Using rendered

    - name: Render commands with provided configuration
      cisco.ios.ios_evpn_ethernet:
        config:
          - identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.01
            redundancy:
              single_active: true
            segment: '1'
          - df_election:
              preempt_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.02
            redundancy:
              single_active: true
            segment: '2'
          - identifier:
              identifier_type: '3'
              esi_value: 00.00.00.00.00.00.00.00.03
            redundancy:
              single_active: true
            segment: '3'
          - df_election:
              wait_time: 1
            identifier:
              identifier_type: '0'
              esi_value: 00.00.00.00.00.00.00.00.04
            redundancy:
              all_active: true
            segment: '4'
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    # - l2vpn evpn ethernet-segment 1
    # - redundancy single-active
    # - identifier type 0 00.00.00.00.00.00.00.00.01
    # - l2vpn evpn ethernet-segment 2
    # - df-election preempt-time 1
    # - redundancy single-active
    # - identifier type 0 00.00.00.00.00.00.00.00.02
    # - l2vpn evpn ethernet-segment 3
    # - redundancy single-active
    # - identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    # - l2vpn evpn ethernet-segment 4
    # - df-election wait-time 1
    # - redundancy all-active
    # - identifier type 0 00.00.00.00.00.00.00.00.04

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # l2vpn evpn ethernet-segment 1
    #  identifier type 0 00.00.00.00.00.00.00.00.01
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 2
    #  identifier type 0 00.00.00.00.00.00.00.00.02
    #  redundancy single-active
    #  df-election preempt-time 1
    # !
    # l2vpn evpn ethernet-segment 3
    #  identifier type 3 system-mac 00.00.00.00.00.00.00.00.03
    #  redundancy single-active
    # !
    # l2vpn evpn ethernet-segment 4
    #  identifier type 0 00.00.00.00.00.00.00.00.04
    #  redundancy all-active
    #  df-election wait-time 1
    # !

    - name: Parse the provided configuration
      cisco.ios.ios_evpn_ethernet:
        running_config: "{{ lookup('file', 'ios_ethernet_segment_parsed.cfg') }}"
        state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    #  - identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.01
    #    redundancy:
    #        single_active: true
    #    segment: '1'
    #  - df_election:
    #        preempt_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.02
    #    redundancy:
    #        single_active: true
    #    segment: '2'
    #  - identifier:
    #        identifier_type: '3'
    #        esi_value: 00.00.00.00.00.00.00.00.03
    #    redundancy:
    #        single_active: true
    #    segment: '3'
    #  - df_election:
    #        wait_time: 1
    #    identifier:
    #        identifier_type: '0'
    #        esi_value: 00.00.00.00.00.00.00.00.04
    #    redundancy:
    #        all_active: true
    #    segment: '4'



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;l2vpn evpn ethernet-segment 1&#x27;, &#x27;identifier type 0 00.00.00.00.00.00.00.00.01&#x27;, &#x27;redundancy single-active&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;l2vpn evpn ethernet-segment 1&#x27;, &#x27;identifier type 3 system-mac 0000.0000.0000.0001&#x27;, &#x27;redundancy all-active&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
- Jorgen Spange (@jorgenspange)
