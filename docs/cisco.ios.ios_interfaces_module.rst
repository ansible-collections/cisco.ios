.. _cisco.ios.ios_interfaces_module:


************************
cisco.ios.ios_interfaces
************************

**Resource module to configure interfaces.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes of Cisco IOS network devices.




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
                        <div>A dictionary of interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Interface description.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>duplex</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>full</li>
                                    <li>half</li>
                                    <li>auto</li>
                        </ul>
                </td>
                <td>
                        <div>Interface link status. Applicable for Ethernet interfaces only, either in half duplex, full duplex or in automatic state which negotiates the duplex automatically.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enabled</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Administrative state of the interface.</div>
                        <div>Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it.</div>
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
                                    <li>layer2</li>
                                    <li>layer3</li>
                        </ul>
                </td>
                <td>
                        <div>Manage Layer2 or Layer3 state of the interface.</div>
                        <div>For a Layer 2 appliance mode Layer2 adds switchport command ( default impacts idempotency).</div>
                        <div>For a Layer 2 appliance mode Layer3 adds no switchport command.</div>
                        <div>For a Layer 3 appliance mode Layer3/2 has no impact rather command fails on apply.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>MTU for a specific interface. Applicable for Ethernet interfaces only.</div>
                        <div>Refer to vendor documentation for valid values.</div>
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
                        <div>Full name of interface, e.g. GigabitEthernet0/2, loopback999.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>speed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface link speed. Applicable for Ethernet interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IOS template name.</div>
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
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | include ip route|ipv6 route</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                        <div>The state <em>purged</em> negates virtual/logical interfaces that are specified in task from running-config.</div>
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
    # Router#sh running-config | section interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  description Configured and Merged by Ansible Network
    #  ip address dhcp
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Merged by Ansible Network
            enabled: true
          - name: GigabitEthernet3
            description: Configured and Merged by Ansible Network
            mtu: 3800
            enabled: false
            speed: 100
            duplex: full
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Merged by Ansible Network
    #   enabled: true
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Merged by Ansible Network
    #   enabled: false
    #   mtu: 3800
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: true
    #   name: Loopback888
    # - enabled: true
    #   name: Loopback999
    # commands:
    # - interface GigabitEthernet3
    # - description Configured and Merged by Ansible Network
    # - speed 100
    # - mtu 3800
    # - duplex full
    # - shutdown
    # after:
    # - enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Merged by Ansible Network
    #   enabled: true
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Merged by Ansible Network
    #   enabled: true
    #   mtu: 2800
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: true
    #   name: Loopback888
    # - enabled: true
    #   name: Loopback999

    # After state:
    # ------------
    #
    # Router#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  description Configured and Merged by Ansible Network
    #  ip address dhcp
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Merged by Ansible Network
    #  mtu 3800
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using merged - with mode attribute

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Configured by Ansible
    # interface GigabitEthernet2
    #  description This is test
    # interface GigabitEthernet3
    #  description This is test
    #  no switchport

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Merged by Ansible Network
            enabled: true
            mode: layer2
          - name: GigabitEthernet3
            description: Configured and Merged by Ansible Network
            mode: layer3
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Merged by Ansible Network
    #   name: GigabitEthernet2
    # - description: Configured and Merged by Ansible Network
    #   name: GigabitEthernet3
    # commands:
    # - interface GigabitEthernet2
    # - description Configured and Merged by Ansible Network
    # - switchport
    # - interface GigabitEthernet3
    # - description Configured and Merged by Ansible Network
    # after:
    # - enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Merged by Ansible Network
    #   enabled: true
    #   name: GigabitEthernet2
    # - description: Configured and Merged by Ansible Network
    #   name: GigabitEthernet3
    #   mode: layer3

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Configured by Ansible
    # interface GigabitEthernet2
    #  description Configured and Merged by Ansible Network
    # interface GigabitEthernet3
    #  description Configured and Merged by Ansible Network
    #  no switchport

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet3
            description: Configured and Replaced by Ansible Network
            enabled: false
            speed: 1000
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: true
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - enabled: true
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: true
    #   name: Loopback888
    # - enabled: true
    #   name: Loopback999
    # - enabled: true
    #   name: Vlan50
    # commands:
    # - interface GigabitEthernet3
    # - description Configured and Replaced by Ansible Network
    # - shutdown
    # after:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: true
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Replaced by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: true
    #   name: Loopback888
    # - enabled: true
    #   name: Loopback999
    # - enabled: true
    #   name: Vlan50

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Replaced by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Replaced by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname

    - name: Override device configuration of all interfaces with provided configuration
      cisco.ios.ios_interfaces:
        config:
          - description: Management interface do not change
            enabled: true
            name: GigabitEthernet1
          - name: GigabitEthernet2
            description: Configured and Overridden by Ansible Network
            speed: 10000
          - name: GigabitEthernet3
            description: Configured and Overridden by Ansible Network
            enabled: false
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: true
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Replaced by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: true
    #   name: Loopback888
    # - enabled: true
    #   name: Loopback999
    # - enabled: true
    #   name: Vlan50
    # commands:
    # - interface loopback888
    # - shutdown
    # - interface loopback999
    # - shutdown
    # - interface Vlan50
    # - shutdown
    # - interface GigabitEthernet2
    # - description Configured and Overridden by Ansible Network
    # - speed 10000
    # - interface GigabitEthernet3
    # - description Configured and Overridden by Ansible Network
    # - no speed 1000
    # after:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Overridden by Ansible Network
    #   enabled: true
    #   name: GigabitEthernet2
    #   speed: '10000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback888
    # - enabled: false
    #   name: Loopback999
    # - enabled: false
    #   name: Vlan50

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    #  shutdown
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  description Configured and Overridden by Ansible Network
    #  ip address dhcp
    #  speed 10000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname
    #  shutdown

    # Using Deleted

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    #  shutdown
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  description Configured and Overridden by Ansible Network
    #  ip address dhcp
    #  speed 10000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname
    #  shutdown

    - name: "Delete interface attributes (Note: This won't delete the interface itself)"
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - description: Configured and Overridden by Ansible Network
    #   enabled: true
    #   name: GigabitEthernet2
    #   speed: '10000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback888
    # - enabled: false
    #   name: Loopback999
    # - enabled: false
    #   name: Vlan50
    # commands:
    # - interface GigabitEthernet2
    # - no description Configured and Overridden by Ansible Network
    # - no speed 10000
    # - shutdown
    # after:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: false
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback888
    # - enabled: false
    #   name: Loopback999
    # - enabled: false
    #   name: Vlan50

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    #  shutdown
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname
    #  shutdown

    # Using Purged

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    #  shutdown
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Vlan50
    #  ip address dhcp hostname testHostname
    #  shutdown

    - name: "Purge given interfaces (Note: This will delete the interface itself)"
      cisco.ios.ios_interfaces:
        config:
          - name: Loopback888
          - name: Vlan50
        state: purged

    # Task Output
    # -----------
    #
    # before:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: false
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback888
    # - enabled: false
    #   name: Loopback999
    # - enabled: false
    #   name: Vlan50
    # commands:
    # - no interface loopback888
    # - no interface Vlan50
    # after:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: false
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback999

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^interface
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Gather facts of interfaces
      cisco.ios.ios_interfaces:
        config:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: false
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback999

    # Using rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet1
            description: Configured by Ansible-Network
            mtu: 110
            enabled: true
            duplex: half
          - name: GigabitEthernet2
            description: Configured by Ansible-Network
            mtu: 2800
            enabled: false
            speed: 100
            duplex: full
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    # - interface GigabitEthernet1
    # - description Configured by Ansible-Network
    # - mtu 110
    # - duplex half
    # - no shutdown
    # - interface GigabitEthernet2
    # - description Configured by Ansible-Network
    # - speed 100
    # - mtu 2800
    # - duplex full
    # - shutdown

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface Loopback999
    #  no ip address
    #  shutdown
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  ip address dhcp
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  shutdown
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Parse the provided configuration
      cisco.ios.ios_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    # - description: Management interface do not change
    #   enabled: true
    #   name: GigabitEthernet1
    # - enabled: false
    #   name: GigabitEthernet2
    #   speed: '1000'
    # - description: Configured and Overridden by Ansible Network
    #   enabled: false
    #   name: GigabitEthernet3
    #   speed: '1000'
    # - enabled: false
    #   name: GigabitEthernet4
    # - enabled: false
    #   name: Loopback999



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet2&#x27;, &#x27;speed 1200&#x27;, &#x27;mtu 1800&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet1&#x27;, &#x27;description Interface description&#x27;, &#x27;shutdown&#x27;]</div>
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
