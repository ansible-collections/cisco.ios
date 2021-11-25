.. _cisco.ios.ios_l3_interfaces_module:


***************************
cisco.ios.ios_l3_interfaces
***************************

**L3 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of Layer-3 interface on Cisco IOS devices.




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
                        <div>A dictionary of Layer-3 interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 address to be set for the Layer-3 interface mentioned in <em>name</em> option. The address format is &lt;ipv4 address&gt;/&lt;mask&gt;, the mask is number in range 0-32 eg. 192.168.0.1/24.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures the IPv4 address for Interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dhcp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP Address negotiated via DHCP.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>client_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify client-id to use.</div>
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
                        <div>Enable dhcp.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify value for hostname option.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dhcp_client</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures and specifies client-id to use over DHCP ip. Note, This option shall work only when dhcp is configured as IP.</div>
                        <div>GigabitEthernet interface number</div>
                        <div>This option is DEPRECATED and is replaced with dhcp which accepts dict as input this attribute will be removed after 2023-08-01.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dhcp_hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures and specifies value for hostname option over DHCP ip. Note, This option shall work only when dhcp is configured as IP.</div>
                        <div>This option is DEPRECATED and is replaced with dhcp which accepts dict as input this attribute will be removed after 2023-08-01.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pool</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP Address auto-configured from a local DHCP pool.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secondary</b>
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
                        <div>Configures the IP address as a secondary address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 address to be set for the Layer-3 interface mentioned in <em>name</em> option.</div>
                        <div>The address format is &lt;ipv6 address&gt;/&lt;mask&gt;, the mask is number in range 0-128 eg. fd5d:12c9:2201:1::1/64</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures the IPv6 address for Interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>anycast</b>
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
                        <div>Configure as an anycast</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>autoconfig</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Obtain address using auto-configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Insert default route.</div>
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
                        <div>enable auto-configuration.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cga</b>
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
                        <div>Use CGA interface identifier</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dhcp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Obtain a ipv6 address using DHCP.</div>
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
                        <div>Enable dhcp.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rapid_commit</b>
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
                        <div>Enable Rapid-Commit.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eui</b>
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
                        <div>Use eui-64 interface identifier</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link_local</b>
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
                        <div>Use link-local address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>segment_routing</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Segment Routing submode</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Set a command to its defaults.</div>
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
                        <div>Enable segmented routing.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6_sr</b>
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
                        <div>Set ipv6_sr.</div>
                </td>
            </tr>


            <tr>
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
                        <div>Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.</div>
                </td>
            </tr>

            <tr>
                <td colspan="4">
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^interface</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSv Version 15.6.
   - Using deleted state without config will delete all l3 attributes from all the interfaces.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html



Examples
--------

.. code-block:: yaml

    # Using state merged

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  ip address 10.1.1.1 255.255.255.0
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  no ip address
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_l3_interfaces:
        config:
        - name: GigabitEthernet0/1
          ipv4:
          - address: 192.168.0.1/24
            secondary: true
        - name: GigabitEthernet0/2
          ipv4:
          - address: 192.168.0.2/24
        - name: GigabitEthernet0/3
          ipv6:
          - address: fd5d:12c9:2201:1::1/64
        - name: GigabitEthernet0/3.100
          ipv4:
          - address: 192.168.0.3/24
        state: merged

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet0/1",
    #       "ip address 192.168.0.1 255.255.255.0 secondary",
    #       "interface GigabitEthernet0/2",
    #       "ip address 192.168.0.2 255.255.255.0",
    #       "interface GigabitEthernet0/3",
    #       "ipv6 address fd5d:12c9:2201:1::1/64",
    #       "GigabitEthernet0/3.100",
    #       "ip address 192.168.0.3 255.255.255.0",
    #     ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  ip address 10.1.1.1 255.255.255.0
    #  ip address 192.168.0.1 255.255.255.0 secondary
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  ip address 192.168.0.2 255.255.255.0
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ipv6 address FD5D:12C9:2201:1::1/64
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.3 255.255.255.0

    # Using state replaced

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  ip address 10.1.1.1 255.255.255.0
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ip address 192.168.2.0 255.255.255.0
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.2 255.255.255.0

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.ios.ios_l3_interfaces:
        config:
        - name: GigabitEthernet0/2
          ipv4:
          - address: 192.168.2.0/24
        - name: GigabitEthernet0/3
          ipv4:
          - dhcp:
              client_id: GigabitEthernet0/2
              hostname: test.com
        - name: GigabitEthernet0/3.100
          ipv4:
          - address: 192.168.0.3/24
            secondary: true
        state: replaced

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet0/1",
    #       "ip address 192.168.0.1 255.255.255.0 secondary",
    #       "interface GigabitEthernet0/2",
    #       "ip address 192.168.0.2 255.255.255.0",
    #       "interface GigabitEthernet0/3",
    #       "no ip address 192.168.2.0 255.255.255.0",
    #       "ip address dhcp client-id GigabitEthernet0/2 hostname test.com",
    #       "GigabitEthernet0/3.100",
    #       "no ip address 192.168.0.2 255.255.255.0",
    #       "ip address 192.168.0.3 255.255.255.0 secondary",
    #     ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  ip address 10.1.1.1 255.255.255.0
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  ip address 192.168.2.1 255.255.255.0
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ip address dhcp client-id GigabitEthernet0/2 hostname test.com
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.3 255.255.255.0 secondary

    # Using state overridden

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  ip address 10.1.1.1 255.255.255.0
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  ip address 192.168.2.1 255.255.255.0
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ipv6 address FD5D:12C9:2201:1::1/64
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.2 255.255.255.0

    - name: Override device configuration of all interfaces with provided configuration
      cisco.ios.ios_l3_interfaces:
        config:
        - name: GigabitEthernet0/2
          ipv4:
          - address: 192.168.0.1/24
        - name: GigabitEthernet0/3.100
          ipv6:
          - autoconfig: true
        state: overridden

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet0/1",
    #       "no ip address 10.1.1.1 255.255.255.0",
    #       "interface GigabitEthernet0/2",
    #       "no ip address 192.168.2.1 255.255.255.0",
    #       "ip address 192.168.0.1 255.255.255.0",
    #       "interface GigabitEthernet0/3",
    #       "no ipv6 address FD5D:12C9:2201:1::1/64",
    #       "GigabitEthernet0/3.100",
    #       "no ip address 192.168.0.2 255.255.255.0",
    #       "ipv6 address autoconfig",
    #     ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  ip address 192.168.0.1 255.255.255.0
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ipv6 address autoconfig

    # Using state Deleted

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  ip address 192.0.2.10 255.255.255.0
    #  shutdown
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  ip address 192.168.1.0 255.255.255.0
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ip address 192.168.0.1 255.255.255.0
    #  shutdown
    #  duplex full
    #  speed 10
    #  ipv6 address FD5D:12C9:2201:1::1/64
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.2 255.255.255.0

    - name: "Delete attributes of given interfaces (NOTE: This won't delete the interfaces itself)"
      cisco.ios.ios_l3_interfaces:
        config:
        - name: GigabitEthernet0/2
        - name: GigabitEthernet0/3.100
        state: deleted

    # "commands": [
    #       "interface GigabitEthernet0/2",
    #       "no ip address 192.168.1.0 255.255.255.0",
    #       "GigabitEthernet0/3.100",
    #       "no ip address 192.168.0.2 255.255.255.0",
    #     ],

    # After state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  ip address 192.0.2.10 255.255.255.0
    #  shutdown
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ip address 192.168.0.1 255.255.255.0
    #  shutdown
    #  duplex full
    #  speed 10
    #  ipv6 address FD5D:12C9:2201:1::1/64
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20

    # Using state Deleted without any config passed
    #"(NOTE: This will delete all of configured L3 resource module attributes from each configured interface)"

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  ip address 192.0.2.10 255.255.255.0
    #  shutdown
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  ip address 192.168.1.0 255.255.255.0
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  ip address 192.168.0.1 255.255.255.0
    #  shutdown
    #  duplex full
    #  speed 10
    #  ipv6 address FD5D:12C9:2201:1::1/64
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20
    #  ip address 192.168.0.2 255.255.255.0

    - name: "Delete L3 attributes of ALL interfaces together (NOTE: This won't delete the interface itself)"
      cisco.ios.ios_l3_interfaces:
        state: deleted

    # "commands": [
    #       "interface GigabitEthernet0/1",
    #       "no ip address 192.0.2.10 255.255.255.0",
    #       "interface GigabitEthernet0/2",
    #       "no ip address 192.168.1.0 255.255.255.0",
    #       "interface GigabitEthernet0/3",
    #       "no ip address 192.168.0.1 255.255.255.0",
    #       "no ipv6 address FD5D:12C9:2201:1::1/64",
    #       "GigabitEthernet0/3.100",
    #       "no ip address 192.168.0.2 255.255.255.0",
    #     ],

    # After state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  shutdown
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  shutdown
    #  duplex full
    #  speed 10
    # interface GigabitEthernet0/3.100
    #  encapsulation dot1Q 20

    # Using state Gathered

    # Before state:
    # -------------

    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  ip address 203.0.113.27 255.255.255.0
    # interface GigabitEthernet0/2
    #  ip address 192.0.2.1 255.255.255.0 secondary
    #  ip address 192.0.2.2 255.255.255.0
    #  ipv6 address 2001:DB8:0:3::/64

    - name: Gather listed l3 interfaces with provided configurations
      cisco.ios.ios_l3_interfaces:
        state: gathered

    # Module Execution Result:
    # ------------------------

    # "gathered": [
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "203.0.113.27 255.255.255.0"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "192.0.2.1 255.255.255.0",
    #                     "secondary": true
    #                 },
    #                 {
    #                     "address": "192.0.2.2 255.255.255.0"
    #                 }
    #             ],
    #             "ipv6": [
    #                 {
    #                     "address": "2001:db8:0:3::/64"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/2"
    #         }
    #     ]

    # After state:
    # ------------

    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  ip address 203.0.113.27 255.255.255.0
    # interface GigabitEthernet0/2
    #  ip address 192.0.2.1 255.255.255.0 secondary
    #  ip address 192.0.2.2 255.255.255.0
    #  ipv6 address 2001:DB8:0:3::/64

    # Using state Rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_l3_interfaces:
        config:
        - name: GigabitEthernet0/1
          ipv4:
          - dhcp:
              client_id: GigabitEthernet0/0
              hostname: test.com
        - name: GigabitEthernet0/2
          ipv4:
          - address: 198.51.100.1/24
            secondary: true
          - address: 198.51.100.2/24
          ipv6:
          - address: 2001:db8:0:3::/64
        state: rendered

    # Module Execution Result:
    # ------------------------

    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "ip address dhcp client-id GigabitEthernet 0/0 hostname test.com",
    #         "interface GigabitEthernet0/2",
    #         "ip address 198.51.100.1 255.255.255.0 secondary",
    #         "ip address 198.51.100.2 255.255.255.0",
    #         "ipv6 address 2001:db8:0:3::/64"
    #     ]

    # Using state Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    #  ip address dhcp client-id GigabitEthernet 0/0 hostname test.com
    # interface GigabitEthernet0/2
    #  ip address 198.51.100.1 255.255.255.0
    #  ip address 198.51.100.2 255.255.255.0 secondary
    #  ipv6 address 2001:db8:0:3::/64

    - name: Parse the commands for provided configuration
      cisco.ios.ios_l3_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------

    # "parsed": [
    #         {
    #             "ipv4": [
    #                 {
    #                     "dhcp": {
    #                         "client_id": GigabitEthernet0/0,
    #                         "hostname": "test.com"
    #                     }
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "198.51.100.1/24",
    #                     "secondary": true
    #                 },
    #                 {
    #                     "address": "198.51.100.2/24"
    #                 }
    #             ],
    #             "ipv6": [
    #                 {
    #                     "address": "2001:db8:0:3::/64"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/2"
    #         }
    #     ]



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
                <td>when state is <em>merged</em>, <em>replaced</em>, <em>overridden</em>, <em>deleted</em> or <em>purged</em></td>
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
                <td>when state is <em>merged</em>, <em>replaced</em>, <em>overridden</em>, <em>deleted</em> or <em>purged</em></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip address 192.168.0.3 255.255.255.0&#x27;, &#x27;ipv6 address dhcp rapid-commit&#x27;, &#x27;ipv6 address fd5d:12c9:2201:1::1/64 anycast&#x27;]</div>
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
                <td>when state is <em>gathered</em></td>
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
                <td>when state is <em>parsed</em></td>
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
                <td>when state is <em>rendered</em></td>
                <td>
                            <div>The provided configuration in the task rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ipv6 address FD5D:12C9:2201:1::1/64&#x27;, &#x27;ip address 192.168.0.3 255.255.255.0&#x27;, &#x27;ip address autoconfig&#x27;]</div>
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
