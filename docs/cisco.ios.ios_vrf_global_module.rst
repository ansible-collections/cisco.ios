.. _cisco.ios.ios_vrf_global_module:


************************
cisco.ios.ios_vrf_global
************************

**Resource module to configure global VRF definitions.**


Version added: 8.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VRF definitions on Cisco IOS.




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
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary containing device configurations for VRF, including a list of VRF definitions.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrfs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of VRF definitions.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF specific description</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF IPv4 configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multicast</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 multicast configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multitopology</b>
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
                        <div>Enable multicast-specific topology</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF IPv6 configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multicast</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 multicast configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multitopology</b>
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
                        <div>Enable multicast-specific topology</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Name of the VRF.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rd</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify route distinguisher (RD).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Specify target VPN extended configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>both</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Both export and import target-VPN configuration.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>export</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Export target-VPN configuration.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>import_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Import target-VPN configuration.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vnet</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual networking configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Identifier used to tag packets associated with this VNET.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vpn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure vpn-id for the VRF as specified in RFC 2685.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure vpn-id in RFC 2685 format.</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^vrf</b>.</div>
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
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>deleted</li>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>rendered</li>
                                    <li>overridden</li>
                                    <li>purged</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section vrf</em>. connection to remote host is not required.</div>
                        <div>The state <em>deleted</em> only removes the VRF attributes that this module manages and does not negate the VRF completely. Thereby, preserving address-family related configurations under VRF context.</div>
                        <div>The state <em>purged</em> removes all the VRF definitions from the target device. Use caution with this state.</div>
                        <div>Refer to examples for more details.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS-XE version 17.3 on CML.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - The module examples uses callback plugin (stdout_callback = yaml) to generate task output in yaml format.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF2
              description: This is a test VRF for merged state
              ipv4:
                multicast:
                  multitopology: true
              ipv6:
                multicast:
                  multitopology: true
              rd: "2:3"
              route_target:
                export: "192.0.2.0:100"
                import_config: "192.0.2.3:200"
              vpn:
                id: "2:45"
              vnet:
                tag: 200
        state: merged

    # Task output
    # -------------
    #
    # before: {}
    #
    # commands:
    #   - vrf definition VRF2
    #   - description This is a test VRF for merged state
    #   - ipv4 multicast multitopology
    #   - ipv6 multicast multitopology
    #   - rd 2:3
    #   - route-target export 192.0.2.0:100
    #   - route-target import 192.0.2.3:200
    #   - vnet tag 200
    #   - vpn id 2:45
    #
    # after:
    #   - name: VRF2
    #     description: This is a test VRF for merged state
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "2:3"
    #     route_target:
    #       export: "192.0.2.0:100"
    #       import_config: "192.0.2.3:200"
    #     vnet:
    #       tag: 200
    #     vpn:
    #       id: "2:45"

    # After state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    #  vnet tag 200
    #  description This is a test VRF for merged state
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 2:3
    #  vpn id 2:45
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.3:200

    # Using replaced

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    #  vnet tag 200
    #  description This is a test VRF for merged state
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 2:3
    #  vpn id 2:45
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.3:200

    - name: Replace the provided configuration with the existing running configuration
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF7
              description: VRF7 description
              ipv4:
                multicast:
                  multitopology: true
              ipv6:
                multicast:
                  multitopology: true
              rd: "7:8"
              route_target:
                export: "198.51.100.112:500"
                import_config: "192.0.2.4:400"
              vpn:
                id: "5:45"
              vnet:
                tag: 300
        state: replaced

    # Task Output:
    # ------------
    #
    # before:
    #   - name: VRF2
    #     description: This is a test VRF for merged state
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "2:3"
    #     route_target:
    #       export: "192.0.2.0:100"
    #       import_config: "192.0.2.3:200"
    #     vnet:
    #       tag: 200
    #     vpn:
    #       id: "2:45"
    #
    # commands:
    # - vrf definition VRF7
    # - description VRF7 description
    # - ipv4 multicast multitopology
    # - ipv6 multicast multitopology
    # - rd 7:8
    # - route-target export 198.51.100.112:500
    # - route-target import 192.0.2.4:400
    # - vnet tag 300
    # - vpn id 5:45
    #
    # after:
    #   - name: VRF2
    #     description: This is a test VRF for merged state
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "2:3"
    #     route_target:
    #       export: "192.0.2.0:100"
    #       import_config: "192.0.2.3:200"
    #     vnet:
    #       tag: 200
    #     vpn:
    #       id: "2:45
    #   - name: VRF7
    #     description: VRF7 description
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "7:8"
    #     route_target:
    #       export: "198.51.100.112:500"
    #       import_config: "192.0.2.4:400"
    #     vnet:
    #       tag: 300
    #     vpn:
    #       id: "5:45"
    #
    # After state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    #  vnet tag 200
    #  description This is a test VRF for merged state
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 2:3
    #  vpn id 2:45
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.3:200
    # vrf definition VRF7
    #  vnet tag 300
    #  description VRF7 description
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 7:8
    #  route-target export 198.51.100.112:500
    #  route-target import 192.0.2.4:400
    #  vpn id 5:45

    # Using Overridden

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    #  vnet tag 200
    #  description This is a test VRF for merged state
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 2:3
    #  vpn id 2:45
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.3:200
    # vrf definition VRF7
    #  vnet tag 300
    #  description VRF7 description
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 7:8
    #  route-target export 198.51.100.112:500
    #  route-target import 192.0.2.4:400
    #  vpn id 5:45

    - name: Override the provided configuration with the existing running configuration
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF6
              description: VRF6 description
              ipv4:
                multicast:
                  multitopology: true
              ipv6:
                multicast:
                  multitopology: true
              rd: "6:7"
              route_target:
                export: "198.51.0.2:400"
                import_config: "198.51.0.5:200"
              vpn:
                id: "4:5"
              vnet:
                tag: 500
        state: overridden

    # Task Output:
    # ------------
    #
    # before:
    #   - name: VRF2
    #     description: This is a test VRF for merged state
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "2:3"
    #     route_target:
    #       export: "192.0.2.0:100"
    #       import_config: "192.0.2.3:200"
    #     vnet:
    #       tag: 200
    #     vpn:
    #       id: "2:45
    #   - name: VRF7
    #     description: VRF7 description
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "7:8"
    #     route_target:
    #       export: "198.51.100.112:500"
    #       import_config: "192.0.2.4:400"
    #     vnet:
    #       tag: 300
    #     vpn:
    #       id: "5:45"
    #
    # commands:
    # - vrf definition VRF2
    # - no description This is a test VRF for merged state
    # - no ipv4 multicast multitopology
    # - no ipv6 multicast multitopology
    # - no rd 2:3
    # - no route-target export 192.0.2.0:100
    # - no route-target import 192.0.2.3:200
    # - no vnet tag 200
    # - no vpn id 2:45
    # - vrf definition VRF7
    # - no description VRF7 description
    # - no ipv4 multicast multitopology
    # - no ipv6 multicast multitopology
    # - no rd 7:8
    # - no route-target export 198.51.100.112:500
    # - no route-target import 192.0.2.4:400
    # - no vnet tag 300
    # - no vpn id 5:45
    # - vrf definition VRF6
    # - description VRF6 description
    # - ipv4 multicast multitopology
    # - ipv6 multicast multitopology
    # - rd 6:7
    # - route-target export 198.51.0.2:400
    # - route-target import 198.51.0.5:200
    # - vnet tag 500
    # - vpn id 4:5
    #
    # after:
    #   - name: VRF2
    #   - name: VRF6
    #     description: VRF6 description
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "6:7"
    #     route_target:
    #       export: "198.51.0.2:400"
    #       import_config: "198.51.0.5:200"
    #     vnet:
    #       tag: 500
    #     vpn:
    #       id: "4:5
    #   - name: VRF7

    # After state:
    # ------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    #  vnet tag 500
    #  description VRF6 description
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 6:7
    #  vpn id 4:5
    #  route-target export 198.51.0.2:400
    #  route-target import 198.51.0.5:200
    # vrf definition VRF7

    # Using Deleted

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    #  vnet tag 500
    #  description VRF6 description
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 6:7
    #  vpn id 4:5
    #  route-target export 198.51.0.2:400
    #  route-target import 198.51.0.5:200
    # vrf definition VRF7

    - name: Delete the provided configuration when config is given
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF2
            - name: VRF6
            - name: VRF7
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    #   - name: VRF2
    #   - name: VRF6
    #     description: VRF6 description
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "6:7"
    #     route_target:
    #       export: "198.51.0.2:400"
    #       import_config: "198.51.0.5:200"
    #     vnet:
    #       tag: 500
    #     vpn:
    #       id: "4:5"
    #   - name: VRF7
    #
    # commands:
    # - vrf definition VRF2
    # - vrf definition VRF6
    # - no description VRF6 description
    # - no ipv4 multicast multitopology
    # - no ipv6 multicast multitopology
    # - no rd 6:7
    # - no route-target export 198.51.0.2:400
    # - no route-target import 198.51.0.5:200
    # - no vnet tag 500
    # - no vpn id 4:5
    # - vrf definition VRF7
    #
    # after:
    #   - name: VRF2
    #   - name: VRF6
    #   - name: VRF7

    # After state:
    # -------------
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    # vrf definition VRF7

    # Using Deleted with empty config

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    #  vnet tag 500
    #  description VRF6 description
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 6:7
    #  vpn id 4:5
    #  route-target export 198.51.0.2:400
    #  route-target import 198.51.0.5:200
    # vrf definition VRF7

    - name: Delete the provided configuration when config is empty
      cisco.ios.ios_vrf_global:
        config:
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    #   - name: VRF2
    #   - name: VRF6
    #     description: VRF6 description
    #     ipv4:
    #       multicast:
    #         multitopology: true
    #     ipv6:
    #       multicast:
    #         multitopology: true
    #     rd: "6:7"
    #     route_target:
    #       export: "198.51.0.2:400"
    #       import_config: "198.51.0.5:200"
    #     vnet:
    #       tag: 500
    #     vpn:
    #       id: "4:5"
    #   - name: VRF7

    # commands:
    # - vrf definition VRF2
    # - vrf definition VRF6
    # - no description VRF6 description
    # - no ipv4 multicast multitopology
    # - no ipv6 multicast multitopology
    # - no rd 6:7
    # - no route-target export 198.51.0.2:400
    # - no route-target import 198.51.0.5:200
    # - no vnet tag 500
    # - no vpn id 4:5
    # - vrf definition VRF7
    #
    # after:
    #   - name: VRF2
    #   - name: VRF6
    #   - name: VRF7

    # After state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    # vrf definition VRF7

    # Using purged - would delete all the VRF definitions

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    # vrf definition VRF6
    # vrf definition VRF7

    - name: Purge all the configuration from the device
      cisco.ios.ios_vrf_global:
        state: purged

    # Task Output:
    # ------------
    #
    # before:
    #   - name: VRF2
    #   - name: VRF6
    #   - name: VRF7
    # commands:
    # - no vrf definition VRF2
    # - no vrf definition VRF6
    # - no vrf definition VRF7
    # after: {}

    # After state:
    # -------------
    #
    # admin#show running-config | section ^vrf

    # Using Rendered

    - name: Render provided configuration with device configuration
      cisco.ios.ios_vrf_global:
        config:
          vrfs:
            - name: VRF2
              description: This is a test VRF for merged state
              ipv4:
                multicast:
                  multitopology: true
              ipv6:
                multicast:
                  multitopology: true
              rd: "2:3"
              route_target:
                export: "192.0.2.0:100"
                import_config: "192.0.2.3:200"
              vpn:
                id: "2:45"
              vnet:
                tag: 200
        state: rendered

    # Task Output:
    # ------------
    #
    # rendered:
    # - vrf definition VRF2
    # - description This is a test VRF for merged state
    # - ipv4 multicast multitopology
    # - ipv6 multicast multitopology
    # - rd 2:3
    # - route-target export 192.0.2.0:100
    # - route-target import 192.0.2.3:200
    # - vnet tag 200
    # - vpn id 2:45

    # Using Gathered

    # Before state:
    # -------------
    #
    # admin#show running-config | section ^vrf
    # vrf definition VRF2
    #  vnet tag 200
    #  description This is a test VRF for merged state
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 2:3
    #  vpn id 2:45
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.3:200

    - name: Gather existing running configuration
      cisco.ios.ios_vrf_global:
        config:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #   vrfs:
    #     - name: VRF2
    #       description: This is a test VRF for merged state
    #       ipv4:
    #         multicast:
    #           multitopology: true
    #       ipv6:
    #         multicast:
    #           multitopology: true
    #       rd: "2:3"
    #       route_target:
    #         export: "192.0.2.0:100"
    #         import_config: "192.0.2.3:200"
    #       vnet:
    #         tag: 200
    #       vpn:
    #         id: "2:45"

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # vrf definition test
    #  vnet tag 34
    #  description This is test VRF
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 192.0.2.0:300
    #  vpn id 3:4
    #  route-target export 192.0.2.0:100
    #  route-target import 192.0.2.2:300
    # vrf definition test2
    #  vnet tag 35
    #  description This is test VRF
    #  ipv4 multicast multitopology
    #  ipv6 multicast multitopology
    #  rd 192.0.2.3:300

    - name: Parse the provided configuration
      cisco.ios.ios_vrf_global:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    #
    # parsed:
    #   vrfs:
    #     - name: test
    #       description: This is test VRF
    #       ipv4:
    #         multicast:
    #           multitopology: true
    #       ipv6:
    #         multicast:
    #           multitopology: true
    #       rd: "192.0.2.0:300"
    #       route_target:
    #         export: "192.0.2.0:100"
    #         import_config: "192.0.2.2:300"
    #       vnet:
    #         tag: 34
    #       vpn:
    #         id: "3:4"
    #     - name: test2
    #       description: This is test VRF
    #       ipv4:
    #         multicast:
    #           multitopology: true
    #       ipv6:
    #         multicast:
    #           multitopology: true
    #       rd: "192.0.2.3:300"
    #       vnet:
    #         tag: 35



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf definition test&#x27;, &#x27;description This is a test VRF&#x27;, &#x27;rd: 2:3&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf definition management&#x27;, &#x27;description This is a test VRF&#x27;, &#x27;rd: 2:3&#x27;, &#x27;route-target export 190.0.2.3:400&#x27;, &#x27;route-target import 190.0.2.1:300&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ruchi Pakhle (@Ruchip16)
