.. _cisco.ios.ios_vrf_interfaces_module:


****************************
cisco.ios.ios_vrf_interfaces
****************************

**Manages VRF configuration on interfaces.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manages Virtual Routing and Forwarding (VRF) configuration on interfaces of Cisco IOS devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
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
                        <div>A list of interface VRF configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Full name of the interface to be configured.</div>
                        <div>Example - GigabitEthernet1, Loopback24</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the VRF to be configured on the interface.</div>
                        <div>When configured, applies &#x27;vrf forwarding &lt;vrf_name&gt;&#x27; under the interface.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^interface</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
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
                        <div>The state the configuration should be left in.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS XE Version 17.13.01a
   - VRF must exist before assigning to an interface
   - When removing VRF from interface, associated IP addresses will be removed
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: GigabitEthernet1
          - name: GigabitEthernet2
            vrf_name: vrf_D
          - name: GigabitEthernet3
          - name: GigabitEthernet4
        state: merged

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #
    # commands:
    #   - interface GigabitEthernet2
    #   - vrf forwarding vrf_D
    #
    # after:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_D"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  vrf forwarding vrf_D
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  vrf forwarding vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Override device configuration with provided configuration
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: GigabitEthernet1
          - name: GigabitEthernet2
          - name: GigabitEthernet3
          - name: GigabitEthernet4
        state: overridden

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_B"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #
    # commands:
    #   - interface GigabitEthernet2
    #   - no vrf forwarding vrf_B
    #
    # after:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using gathered

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  vrf forwarding vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Gather listed VRF interfaces
      cisco.ios.ios_vrf_interfaces:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_B"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"

    # Using rendered

    - name: Render VRF configuration
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: GigabitEthernet1
          - name: GigabitEthernet2
            vrf_name: vrf_D
          - name: GigabitEthernet3
          - name: GigabitEthernet4
        state: rendered

    # Task Output:
    # ------------
    #
    # rendered:
    #   - interface GigabitEthernet2
    #   - vrf forwarding vrf_D

    # Using parsed

    # File: parsed.cfg
    # ---------------
    #
    # interface GigabitEthernet1
    #  vrf vrf_C
    #  shutdown
    # !
    # interface GigabitEthernet2
    #  vrf vrf_D
    #  shutdown
    # !
    # interface GigabitEthernet3
    #  shutdown
    # !
    # interface GigabitEthernet4
    #  shutdown
    # !

    - name: Parse configuration from device running config
      cisco.ios.ios_vrf_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    #
    # parsed:
    #   - name: "GigabitEthernet1"
    #     vrf_name: "vrf_C"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_D"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  vrf forwarding vrf_A
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  vrf forwarding vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  vrf forwarding vrf_C
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Replace device configuration of listed VRF interfaces with provided configuration
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: GigabitEthernet1
            vrf_name: vrf_D
          - name: GigabitEthernet2
            vrf_name: vrf_E
        state: replaced

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #     vrf_name: "vrf_A"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_B"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #     vrf_name: "vrf_C"
    #
    # commands:
    #   - interface GigabitEthernet1
    #   - no vrf forwarding vrf_A
    #   - vrf forwarding vrf_D
    #   - interface GigabitEthernet2
    #   - no vrf forwarding vrf_B
    #   - vrf forwarding vrf_E
    #
    # after:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #     vrf_name: "vrf_D"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_E"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #     vrf_name: "vrf_C"

    # Using deleted

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  vrf forwarding vrf_A
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  vrf forwarding vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  vrf forwarding vrf_C
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Delete VRF configuration of specified interfaces
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: GigabitEthernet1
          - name: GigabitEthernet2
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #     vrf_name: "vrf_A"
    #   - name: "GigabitEthernet2"
    #     vrf_name: "vrf_B"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #     vrf_name: "vrf_C"
    #
    # commands:
    #   - interface GigabitEthernet1
    #   - no vrf forwarding vrf_A
    #   - interface GigabitEthernet2
    #   - no vrf forwarding vrf_B
    #
    # after:
    #   - name: "Loopback24"
    #   - name: "GigabitEthernet1"
    #   - name: "GigabitEthernet2"
    #   - name: "GigabitEthernet3"
    #   - name: "GigabitEthernet4"
    #     vrf_name: "vrf_C"

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback24
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  negotiation auto
    # interface GigabitEthernet4
    #  vrf forwarding vrf_C
    #  no ip address
    #  shutdown
    #  negotiation auto



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Loopback24&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet1&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet2&quot;,
            &quot;vrf_name&quot;: &quot;vrf_D&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet3&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet4&quot;
        }
    ]</div>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code></td>
                <td>
                            <div>The configuration prior to the module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Loopback24&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet1&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet2&quot;,
            &quot;vrf_name&quot;: &quot;vrf_B&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet3&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet4&quot;
        }
    ]</div>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet2&#x27;, &#x27;vrf forwarding vrf_D&#x27;, &#x27;no vrf forwarding vrf_B&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Loopback24&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet1&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet2&quot;,
            &quot;vrf_name&quot;: &quot;vrf_B&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet3&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet4&quot;
        }
    ]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;GigabitEthernet1&quot;,
            &quot;vrf_name&quot;: &quot;vrf_C&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet2&quot;,
            &quot;vrf_name&quot;: &quot;vrf_D&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet3&quot;
        },
        {
            &quot;name&quot;: &quot;GigabitEthernet4&quot;
        }
    ]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet1&#x27;, &#x27;vrf forwarding vrf_C&#x27;, &#x27;interface GigabitEthernet2&#x27;, &#x27;vrf forwarding vrf_D&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- AAYUSH ANAND (@AAYUSH2091)
