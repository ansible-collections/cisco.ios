.. _cisco.ios.ios_evpn_global_module:


***************************
cisco.ios.ios_evpn_global
***************************

**Resource module to configure EVPN global.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of EVPN global on Cisco IOS devices.




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
                        <div>A dictionary of EVPN global options</div>
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
                    <b>router_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>EVPN router ID</div>
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
                        <span style="color: purple">bool</span>
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
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>flooding_suppression</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Suppress flooding of broadcast, multicast, and/or unknown unicast packets</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_resolution</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Suppress flooding of Address Resolution and Neighbor Discovery Protocol packets</div>
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
                        <div>Disable flooding suppression</div>
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
                    <b>disable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Disable IP local learning</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route Target VPN Extended Communities</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auto</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Automatically set a route-target</div>
                </td>
            </tr>
                            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set vni-based route-target</div>
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
    # l2vpn evpn
    #  replication-type static
    #  router-id Loopback1
    #  default-gateway advertise

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_evpn_global:
        config:
            replication_type: ingress
            route_target:
              auto:
                vni: true
            default_gateway:
              advertise: false
            ip:
              local_learning: 
                disable: true
            flooding_suppression:
              address_resolution: 
                disable: false
        state: merged

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "l2vpn evpn",
    #       "no default-gateway advertise",
    #       "replication-type ingress",
    #       "route-target auto vni",
    #       "ip local-learning disable",
    #   ]

    # After state:
    # ------------
    # l2vpn evpn
    #  replication-type ingress
    #  router-id Loopback1
    #  ip local-learning disable
    #  route-target auto vni

    # Using state replaced

    # Before state:
    # -------------
    # l2vpn evpn
    #  replication-type ingress
    #  router-id Loopback1
    #  ip local-learning disable
    #  route-target auto vni

    - name: Replaces device configuration for EVPN global with provided configuration
      cisco.ios.ios_evpn_global:
        config:
            replication_type: static
            router_id: loopback2
            default_gateway:
              advertise: true
            flooding_suppression:
              address_resolution: 
                disable: true
        state: replaced

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "l2vpn evpn",
    #       "default-gateway advertise",
    #       "flooding-suppression address-resolution disable",
    #       "no ip local-learning disable",
    #       "replication-type static",
    #       "no route-target auto vni",
    #       "router-id loopback2"
    #   ],

    # After state:
    # ------------
    # l2vpn evpn
    #  replication-type static
    #  flooding-suppression address-resolution disable
    #  router-id Loopback2
    #  default-gateway advertise

    # Using state Deleted

    # Before state:
    # -------------
    # l2vpn evpn
    #  replication-type static
    #  flooding-suppression address-resolution disable
    #  router-id Loopback2
    #  default-gateway advertise

    - name: Delete EVPN global
      cisco.ios.ios_evpn_global:
        config:
        state: deleted

    # Commands Fired:
    # ---------------
    #  "commands": [
    #      "no l2vpn evpn"
    #      ]

    # After state:
    # -------------
    # 

    # Using gathered

    # Before state:
    # -------------
    #
    # l2vpn evpn
    #  replication-type ingress
    #  router-id Loopback1
    #  ip local-learning disable
    #  route-target auto vni

    - name: Gather facts for evpn_global
      cisco.ios.ios_evpn_global:
        config:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #   replication_type: ingress
    #   route_target:
    #     auto:
    #       vni: true
    #   router_id: Loopback1
    #   ip:
    #     local_learning: 
    #       disable: true

    # Using Rendered

    - name: Rendered the provided configuration with the existing running configuration
      cisco.ios.ios_evpn_global:
        config:
            replication_type: static
            route_target:
              auto:
                vni: true
        state: rendered

    # Task Output:
    # ------------
    #
    # rendered:
    # - l2vpn evpn
    # - replication-type static
    # - route-target auto vni

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # l2vpn evpn
    #  replication-type ingress
    #  router-id Loopback1
    #  default-gateway advertise
    #  route-target auto vni

    - name: Parse the commands for provided configuration
      cisco.ios.ios_evpn_global:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    #
    # parsed:
    #     replication_type: ingress
    #     route_target:
    #       auto:
    #         vni: true
    #     router_id: Loopback1
    #     default_gateway:
    #       advertise: true


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
