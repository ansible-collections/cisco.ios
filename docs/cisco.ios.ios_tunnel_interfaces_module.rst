.. _cisco.ios.ios_tunnel_interfaces_module:


*******************************
cisco.ios.ios_tunnel_interfaces
*******************************

**Resource module to configure tunnel interface parameters.**


Version added: 11.8.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the tunnel specific parameters (``tunnel source``, ``tunnel destination``, ``tunnel key``, ``tunnel vrf`` and so on) of tunnel interfaces on Cisco IOS devices.
- The other settings of a tunnel interface are managed by the modules that already own them, ``ios_interfaces`` for the description, ``ios_vrf_interfaces`` for ``vrf forwarding`` and ``ios_l3_interfaces`` for the IP address, MTU, TCP MSS and redirects.
- Supported parameters are *source*, *destination*, *mode* (``gre ip``, ``gre ipv6`` and ``gre multipoint``), *key*, *vrf*, *ttl*, *checksum* and *path_mtu_discovery*. Others, for example ``tunnel keepalive`` and ``tunnel protection``, are not covered yet.




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
                        <div>A list of tunnel interface configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>checksum</b>
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
                        <div>Enable GRE checksums (<code>tunnel checksum</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>destination</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination of the tunnel, an IPv4 or IPv6 address (<code>tunnel destination</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>GRE key of the tunnel (<code>tunnel key</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>gre_ip</li>
                                    <li>gre_ipv6</li>
                                    <li>gre_multipoint</li>
                        </ul>
                </td>
                <td>
                        <div>Encapsulation of the tunnel (<code>tunnel mode</code>).</div>
                        <div><code>gre_ip</code> is the default of IOS and is not printed in the running configuration.</div>
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
                        <div>Full name of the tunnel interface, for example <code>Tunnel1501</code>. <code>Tu1501</code> is accepted too.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path_mtu_discovery</b>
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
                        <div>Enable path MTU discovery on the tunnel (<code>tunnel path-mtu-discovery</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source of the tunnel, an interface name or an IP address (<code>tunnel source</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ttl</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>TTL of the tunnel packets (<code>tunnel ttl</code>). 255 is the default of IOS and is not printed.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>VRF used to look up the tunnel destination (<code>tunnel vrf</code>).</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^interface Tunnel</b>.</div>
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
                        <div>With state <em>merged</em>, the provided parameters are added to the existing ones. Nothing is removed.</div>
                        <div>With state <em>replaced</em>, the tunnel interfaces named in the task are made to match exactly, parameters not in the task are removed. Tunnel interfaces not named are left alone.</div>
                        <div>With state <em>overridden</em>, the device is made to match the task exactly, the parameters of tunnel interfaces not named in the task are removed.</div>
                        <div>With state <em>deleted</em>, the tunnel parameters of the interfaces named in the task are removed. Without <em>config</em> the parameters of all tunnel interfaces are removed.</div>
                        <div>With state <em>gathered</em>, the configuration is read from the device and returned in <em>gathered</em>.</div>
                        <div>With state <em>rendered</em>, the task configuration is returned as device commands in <em>rendered</em> without connecting to the device.</div>
                        <div>With state <em>parsed</em>, <em>running_config</em> is returned as structured data in <em>parsed</em>.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS XE Software, Version 17.12.4 on a Catalyst 9300.
   - This module works with connection ``network_cli``.
   - IOS does not print the defaults ``tunnel mode gre ip`` and ``tunnel ttl 255``. The module treats a tunnel without them as *mode=gre_ip* and *ttl=255*, so setting the defaults explicitly is idempotent.
   - IOS refuses ``tunnel mode gre multipoint`` while a ``tunnel destination`` is configured, and the error is not seen by the connection plugin. The module removes the destination before switching to *gre_multipoint*, sets the mode before the destination when leaving it, and fails when a task sets *destination* together with *mode=gre_multipoint*.
   - The tunnel interface itself is not removed by this module. State *deleted* removes the tunnel parameters only, use ``ios_interfaces`` with state *purged* to remove the interface.
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # router#show running-config | section ^interface Tunnel
    # router#

    - name: Configure the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1501
            source: Loopback499
            destination: 198.51.100.101
            key: 1501
            vrf: MGMT
        state: merged

    # Task Output
    # -----------
    #
    # commands:
    #   - interface Tunnel1501
    #   - tunnel source Loopback499
    #   - tunnel destination 198.51.100.101
    #   - tunnel key 1501
    #   - tunnel vrf MGMT

    # After state:
    # ------------
    #
    # router#show running-config | section ^interface Tunnel
    # interface Tunnel1501
    #  tunnel source Loopback499
    #  tunnel destination 198.51.100.101
    #  tunnel key 1501
    #  tunnel vrf MGMT

    # A complete tunnel interface is built by the modules that own each part

    - name: Create the tunnel interface, its description and VRF
      cisco.ios.ios_interfaces:
        config:
          - name: Tunnel1501
            description: "Tunnel to the remote site"
        state: merged

    - name: Put the tunnel interface in a VRF
      cisco.ios.ios_vrf_interfaces:
        config:
          - name: Tunnel1501
            vrf_name: CUSTOMER
        state: merged

    - name: Address and tune the tunnel interface
      cisco.ios.ios_l3_interfaces:
        config:
          - name: Tunnel1501
            ipv4:
              - address: 192.0.2.82/30
                mtu: 1400
            redirects: false
            tcp_adjust_mss: 1360
            ipv6_redirects: false
            ipv6_unreachables: false
        state: merged

    - name: Configure the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1501
            source: Loopback499
            destination: 198.51.100.101
            key: 1501
            vrf: MGMT
        state: merged

    # router#show running-config interface Tunnel1501
    # interface Tunnel1501
    #  description Tunnel to the remote site
    #  vrf forwarding CUSTOMER
    #  ip address 192.0.2.82 255.255.255.252
    #  no ip redirects
    #  ip mtu 1400
    #  ip tcp adjust-mss 1360
    #  no ipv6 redirects
    #  no ipv6 unreachables
    #  tunnel source Loopback499
    #  tunnel destination 198.51.100.101
    #  tunnel key 1501
    #  tunnel vrf MGMT

    # Using replaced

    # Before state:
    # -------------
    #
    # interface Tunnel1501
    #  tunnel source Loopback499
    #  tunnel destination 198.51.100.101
    #  tunnel key 1501
    #  tunnel vrf MGMT

    - name: Replace the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1501
            source: Loopback499
            destination: 198.51.100.102
            ttl: 64
        state: replaced

    # Task Output
    # -----------
    #
    # commands:
    #   - interface Tunnel1501
    #   - tunnel destination 198.51.100.102
    #   - no tunnel key
    #   - no tunnel vrf MGMT
    #   - tunnel ttl 64

    # Using overridden

    # Before state:
    # -------------
    #
    # interface Tunnel1501
    #  tunnel source Loopback499
    #  tunnel destination 198.51.100.101
    # interface Tunnel1502
    #  tunnel source Loopback499
    #  tunnel destination 198.51.100.102

    - name: Override the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1501
            source: Loopback499
            destination: 198.51.100.101
        state: overridden

    # Task Output
    # -----------
    #
    # commands:
    #   - interface Tunnel1502
    #   - no tunnel source
    #   - no tunnel destination

    # Using deleted

    - name: Remove the tunnel parameters of one interface
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1501
        state: deleted

    - name: Remove the tunnel parameters of all tunnel interfaces
      cisco.ios.ios_tunnel_interfaces:
        state: deleted

    # Using gathered

    - name: Gather the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    #   - name: Tunnel1501
    #     source: Loopback499
    #     destination: 198.51.100.101
    #     key: 1501
    #     vrf: MGMT

    # Using rendered

    - name: Render the tunnel commands
      cisco.ios.ios_tunnel_interfaces:
        config:
          - name: Tunnel1502
            mode: gre_multipoint
            source: Loopback499
            key: 7
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    #   - interface Tunnel1502
    #   - tunnel mode gre multipoint
    #   - tunnel source Loopback499
    #   - tunnel key 7

    # Using parsed

    - name: Parse the tunnel parameters
      cisco.ios.ios_tunnel_interfaces:
        running_config: |
          interface Tunnel1501
           tunnel source Loopback499
           tunnel destination 198.51.100.101
           tunnel key 1501
        state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    #   - name: Tunnel1501
    #     source: Loopback499
    #     destination: 198.51.100.101
    #     key: 1501



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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Tunnel1501&#x27;, &#x27;tunnel source Loopback499&#x27;, &#x27;tunnel destination 198.51.100.101&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Tunnel1501&#x27;, &#x27;tunnel source Loopback499&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørgen Spange (@jorgenspange)
