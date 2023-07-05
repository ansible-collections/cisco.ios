.. _cisco.ios.ios_static_routes_module:


***************************
cisco.ios.ios_static_routes
***************************

**Resource module to configure static routes.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the static routes on IOS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="5">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="5">
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
                        <div>A dictionary of static route options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_families</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address family to use for the static routes</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>Top level address family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configuring static route</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination prefix with its subnet mask</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hops</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>next hop address or interface</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dhcp</b>
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
                        <div>Default gateway obtained from DHCP</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>distance_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance metric for this route</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>forward_router_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Forwarding router&#x27;s address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global</b>
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
                        <div>Next hop address is global</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface for directly connected static routes</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multicast</b>
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
                        <div>multicast route</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Specify name of the next hop</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>permanent</b>
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
                        <div>permanent route</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set tag for this route</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Install route depending on tracked item with tracked object number.</div>
                        <div>Tracking does not support multicast</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unicast</b>
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
                        <div>unicast route (ipv6 specific)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>topology</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure static route for a Topology Routing/Forwarding instance</div>
                        <div>NOTE, VRF and Topology can be used together only with Multicast and Topology should pre-exist before it can be used</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>IP VPN Routing/Forwarding instance name.</div>
                        <div>NOTE, In case of IPV4/IPV6 VRF routing table should pre-exist before configuring.</div>
                        <div>NOTE, if the vrf information is not provided then the routes shall be configured under global vrf.</div>
                </td>
            </tr>

            <tr>
                <td colspan="5">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | include ip route|ipv6 route</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="5">
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
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | include ip route|ipv6 route</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.3 on CML.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - The module examples uses callback plugin (stdout_callback = yaml) to generate task output in yaml format.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_static_routes:
        config:
          - vrf: blue
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.0/24
                    next_hops:
                      - forward_router_address: 192.0.2.1
                        name: merged_blue
                        tag: 50
                        track: 150
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 198.51.100.0/24
                    next_hops:
                      - forward_router_address: 198.51.101.1
                        name: merged_route_1
                        distance_metric: 110
                        tag: 40
                        multicast: true
                      - forward_router_address: 198.51.101.2
                        name: merged_route_2
                        distance_metric: 30
                      - forward_router_address: 198.51.101.3
                        name: merged_route_3
              - afi: ipv6
                routes:
                  - dest: 2001:DB8:0:3::/64
                    next_hops:
                      - forward_router_address: 2001:DB8:0:3::2
                        name: merged_v6
                        tag: 105
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - {}
    # commands:
    # - ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name merged_route_1 multicast
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name merged_route_2
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
    # - ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name merged_blue track 150
    # after:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: merged_route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: merged_route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: merged_route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: merged_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: merged_blue
    #         tag: 50
    #         track: 150
    #   vrf: blue

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name merged_blue track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name merged_route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name merged_route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name merged_blue track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name merged_route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name merged_route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6

    - name: Replace provided configuration with device configuration
      cisco.ios.ios_static_routes:
        config:
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 198.51.100.0/24
                    next_hops:
                      - forward_router_address: 198.51.101.1
                        name: replaced_route
                        distance_metric: 175
                        tag: 70
                        multicast: true
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: merged_route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: merged_route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: merged_route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: merged_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: merged_blue
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name merged_route_3
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name merged_route_2
    # after:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - distance_metric: 175
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: replaced_route
    #         tag: 70
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: merged_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: merged_blue
    #         tag: 50
    #         track: 150
    #   vrf: blue

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name merged_blue track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name merged_blue track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6

    - name: Override provided configuration with device configuration
      cisco.ios.ios_static_routes:
        config:
          - vrf: blue
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.0/24
                    next_hops:
                      - forward_router_address: 192.0.2.1
                        name: override_vrf
                        tag: 50
                        track: 150
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - distance_metric: 175
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: replaced_route
    #         tag: 70
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: merged_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: merged_blue
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name override_vrf track 150
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.1 175 tag 70 name replaced_route multicast
    # - no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name merged_v6
    # after:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: override_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name override_vrf track 150

    # Using deleted

    # Before state:
    # -------------
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Delete the exact static routes, with all the static routes explicitly mentioned in want
      cisco.ios.ios_static_routes:
        config:
          - vrf: blue
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.0/24
                    next_hops:
                      - forward_router_address: 192.0.2.1
                        name: test_vrf
                        tag: 50
                        track: 150
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 198.51.100.0/24
                    next_hops:
                      - forward_router_address: 198.51.101.1
                        name: route_1
                        distance_metric: 110
                        tag: 40
                        multicast: true
                      - forward_router_address: 198.51.101.2
                        name: route_2
                        distance_metric: 30
                      - forward_router_address: 198.51.101.3
                        name: route_3
              - afi: ipv6
                routes:
                  - dest: 2001:DB8:0:3::/64
                    next_hops:
                      - forward_router_address: 2001:DB8:0:3::2
                        name: test_v6
                        tag: 105
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - no ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # - no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6
    # after: {}

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route

    # Using deleted - delete based on specific routes

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Delete destination specific static routes
      cisco.ios.ios_static_routes:
        config:
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 198.51.100.0/24
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # after:
    # - address_families:
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    # Using deleted - delete based on vrfs

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Delete vrf specific static routes
      cisco.ios.ios_static_routes:
        config:
          - vrf: blue
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - no ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # after:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105

    # After state:
    # ------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    # Using deleted - delete all

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Delete ALL configured static routes
      cisco.ios.ios_static_routes:
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue
    # commands:
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # - no ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # - no ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6
    # - no ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # after: {}

    # After state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route

    # Using gathered

    # Before state:
    # -------------
    #
    # vios#show running-config | include ip route|ipv6 route
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Gather facts of static routes
      cisco.ios.ios_static_routes:
        config:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue

    # Using rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_static_routes:
        config:
          - vrf: blue
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.0/24
                    next_hops:
                      - forward_router_address: 192.0.2.1
                        name: test_vrf
                        tag: 50
                        track: 150
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 198.51.100.0/24
                    next_hops:
                      - forward_router_address: 198.51.101.1
                        name: route_1
                        distance_metric: 110
                        tag: 40
                        multicast: true
                      - forward_router_address: 198.51.101.2
                        name: route_2
                        distance_metric: 30
                      - forward_router_address: 198.51.101.3
                        name: route_3
              - afi: ipv6
                routes:
                  - dest: 2001:DB8:0:3::/64
                    next_hops:
                      - forward_router_address: 2001:DB8:0:3::2
                        name: test_v6
                        tag: 105
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    # - ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # - ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # - ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # ip route vrf blue 192.0.2.0 255.255.255.0 192.0.2.1 tag 50 name test_vrf track 150
    # ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3
    # ip route 198.51.100.0 255.255.255.0 198.51.101.2 30 name route_2
    # ip route 198.51.100.0 255.255.255.0 198.51.101.1 110 tag 40 name route_1 multicast
    # ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6

    - name: Parse the provided configuration
      cisco.ios.ios_static_routes:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 198.51.100.0/24
    #       next_hops:
    #       - forward_router_address: 198.51.101.3
    #         name: route_3
    #       - distance_metric: 30
    #         forward_router_address: 198.51.101.2
    #         name: route_2
    #       - distance_metric: 110
    #         forward_router_address: 198.51.101.1
    #         multicast: true
    #         name: route_1
    #         tag: 40
    #   - afi: ipv6
    #     routes:
    #     - dest: 2001:DB8:0:3::/64
    #       next_hops:
    #       - forward_router_address: 2001:DB8:0:3::2
    #         name: test_v6
    #         tag: 105
    # - address_families:
    #   - afi: ipv4
    #     routes:
    #     - dest: 192.0.2.0/24
    #       next_hops:
    #       - forward_router_address: 192.0.2.1
    #         name: test_vrf
    #         tag: 50
    #         track: 150
    #   vrf: blue



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
                            <div>The configuration as structured data after module completion.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                            <div>The configuration as structured data prior to module invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                            <div>The set of commands pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip route vrf test 172.31.10.0 255.255.255.0 10.10.10.2 name new_test multicast&#x27;]</div>
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
                <td>When <code>state</code> is <em>gathered</em></td>
                <td>
                            <div>The configuration as structured data transformed for the running configuration fetched from remote host</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                <td>When <code>state</code> is <em>parsed</em></td>
                <td>
                            <div>The configuration as structured data transformed for the value of <code>running_config</code> option</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                <td>When <code>state</code> is <em>rendered</em></td>
                <td>
                            <div>The set of CLI commands generated from the value in <code>config</code> option</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip route 198.51.100.0 255.255.255.0 198.51.101.3 name route_3&#x27;, &#x27;ipv6 route 2001:DB8:0:3::/64 2001:DB8:0:3::2 tag 105 name test_v6&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
- Sumit Jaiswal (@justjais)
