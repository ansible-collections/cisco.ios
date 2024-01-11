.. _cisco.ios.ios_vxlan_vtep_module:


************************
cisco.ios.ios_vxlan_vtep
************************

**Resource module to configure VXLAN VTEP interface.**


Version added: 5.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VXLAN VTEP interface on Cisco IOS network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="7">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="7">
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
                        <div>A dictionary of VXLAN VTEP interface option</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_reachability_bgp</b>
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
                        <div>Host reachability using EVPN protocol</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VXLAN VTEP interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
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
                        <div>Configure VNI member</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure VNI information</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>l2vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Associates L2VNI with the VXLAN VTEP interface</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>replication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Replication type for the L2VNI</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mcast_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure multicast group for VN<em>s</em></div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 multicast group</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 multicast group</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
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
                        <div>Replication type</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VNI number</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>l3vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Associates L3VNI with the VXLAN VTEP interface</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VNI number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF name of the L3VNI</div>
                </td>
            </tr>



            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source interface for the VXLAN VTEP interface</div>
                </td>
            </tr>

            <tr>
                <td colspan="7">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^interface nve</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="7">
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
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS-XE device with Version 17.13.01 on Cat9k on CML.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html



Examples
--------

.. code-block:: yaml

    # Using state merged

    # Before state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback1
    #  host-reachability protocol bgp
    #  member vni 10101 mcast-group 225.0.0.101
    #  member vni 10102 ingress-replication
    #  member vni 50901 vrf green
    #  member vni 10201 mcast-group 225.0.0.101
    #  member vni 10202 ingress-replication
    #  member vni 50902 vrf blue

    # - name: Merge the provided configuration with the device configuration
    #   cisco.ios.ios_vxlan_vtep:
    #     config:
    #     - interface: nve1
    #       source_interface: loopback2
    #       member:
    #         vni:
    #           l2vni:
    #             - vni: 10101
    #               replication:
    #                 type: ingress
    #             - vni: 10201
    #               replication:
    #                 type: static
    #                 mcast_group:
    #                   ipv4: 225.0.0.101
    #                   ipv6: FF0E:225::101
    #           l3vni:
    #             - vni: 50901
    #               vrf: blue
    #     state: merged

    # Commands Fired:
    # ---------------
    #   "commands": [
    #         "interface nve1",
    #         "source-interface loopback2",
    #         "no member vni 10101 mcast-group 225.0.0.101",
    #         "member vni 10101 ingress-replication",
    #         "no member vni 10201 mcast-group 225.0.0.101",
    #         "member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
    #         "no member vni 50901 vrf green",
    #         "no member vni 50902 vrf blue",
    #         "member vni 50901 vrf blue"
    #   ],

    # After state:
    # ------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10102 ingress-replication
    #  member vni 10202 ingress-replication
    #  member vni 10101 ingress-replication
    #  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
    #  member vni 50901 vrf blue

    # Using state replaced

    # Before state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10102 ingress-replication
    #  member vni 10202 ingress-replication
    #  member vni 10101 ingress-replication
    #  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101
    #  member vni 50901 vrf blue

    # - name: Replaces the device configuration with the provided configuration
    #   cisco.ios.ios_vxlan_vtep:
    #     config:
    #     - interface: nve1
    #       source_interface: Loopback2
    #       member:
    #         vni:
    #           l2vni:
    #             - vni: 10101
    #               replication:
    #                 type: static
    #                 mcast_group:
    #                   ipv6: FF0E:225::101
    #             - vni: 10201
    #               replication:
    #                 type: static
    #                 mcast_group:
    #                   ipv6: FF0E:225::102
    #     state: replaced

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "interface nve1",
    #       "no member vni 10101 ingress-replication",
    #       "member vni 10101 mcast-group FF0E:225::101",
    #       "no member vni 10201 mcast-group 225.0.0.101 FF0E:225::101",
    #       "member vni 10201 mcast-group FF0E:225::102",
    #       "no member vni 10102 ingress-replication",
    #       "no member vni 10202 ingress-replication",
    #       "no member vni 50901 vrf blue"
    #   ],

    # After state:
    # ------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10101 mcast-group FF0E:225::101
    #  member vni 10201 mcast-group FF0E:225::102

    # Using state Deleted

    # Before state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10101 mcast-group FF0E:225::101
    #  member vni 10201 mcast-group FF0E:225::102

    # - name: "Delete VXLAN VTEP interface"
    #   cisco.ios.ios_vxlan_vtep:
    #     config:
    #     - interface: nve1
    #     state: deleted

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "interface nve1",
    #       "no source-interface Loopback2",
    #       "no host-reachability protocol bgp",
    #       "no member vni 10101 mcast-group FF0E:225::101",
    #       "no member vni 10201 mcast-group FF0E:225::102"
    #   ],

    # After state:
    # -------------
    # interface nve1
    #  no ip address

    # Using state Deleted with member VNIs

    # Before state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10101 mcast-group FF0E:225::101
    #  member vni 10102 mcast-group 225.0.0.101
    #  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101

    # - name: "Delete VXLAN VTEP interface with member VNIs"
    #   cisco.ios.ios_vxlan_vtep:
    #     config:
    #     - interface: nve1
    #       source_interface: Loopback2
    #       member:
    #         vni:
    #           l2vni:
    #             - vni: 10101
    #             - vni: 10102
    #     state: deleted

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "interface nve1",
    #       "no member vni 10101 mcast-group FF0E:225::101",
    #       "no member vni 10102 mcast-group 225.0.0.101"
    #   ],

    # After state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10201 mcast-group 225.0.0.101 FF0E:225::101

    # Using state Deleted with no config

    # Before state:
    # -------------
    # interface nve1
    #  no ip address
    #  source-interface Loopback2
    #  host-reachability protocol bgp
    #  member vni 10101 mcast-group FF0E:225::101
    #  member vni 10201 mcast-group FF0E:225::102

    # - name: "Delete VXLAN VTEP interface with no config"
    #   cisco.ios.ios_vxlan_vtep:
    #     state: deleted

    # Commands Fired:
    # ---------------
    #   "commands": [
    #       "interface nve1",
    #       "no source-interface Loopback2",
    #       "no host-reachability protocol bgp",
    #       "no member vni 10101 mcast-group FF0E:225::101",
    #       "no member vni 10201 mcast-group FF0E:225::102"
    #   ],

    # After state:
    # -------------
    # interface nve1
    #  no ip address



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface nve1&#x27;, &#x27;source-interface Loopback1&#x27;, &#x27;host-reachability protocol bgp&#x27;, &#x27;member vni 10101 ingress-replication&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Padmini Priyadarshini Sivaraj (@PadminiSivaraj)
