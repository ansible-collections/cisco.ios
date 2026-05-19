.. _cisco.ios.ios_bfd_interfaces_module:


****************************
cisco.ios.ios_bfd_interfaces
****************************

**Resource module to configure bfd in interfaces.**


Version added: 11.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the bfd configuration in interface of Cisco IOS network devices.




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
                        <div>A list of interface options, to configure bfd.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable or disable bfd for the interface.</div>
                        <div>Default value for appliance might impact idempotency.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>echo</b>
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
                        <div>Use echo adjunct as bfd detection mechanism.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Transmit interval between BFD packets</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>input</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interval between transmitted BFD control packets 50 - 9999 Milliseconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_rx</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum receive interval capability 50 - 9999 Milliseconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multiplier</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Detection multiplier 3 - 50</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>jitter</b>
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
                        <div>Enable BFD interval transmit jittering.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>local_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>BFD local address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Short interface names like Gi0/2, Lo999 may impact idempotency.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>BFD template (might impact other BFD configuration),</div>
                        <div>Ansible won&#x27;t guarantee state operations.</div>
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
                        <div>The value of this option should be the output received from the IOS XE device by executing the command <b>show running-config | section ^interface</b>.</div>
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
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section interface</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
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

    # Using state: merged

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto


    - name: Apply the provided BFD configuration to interfaces
      cisco.ios.ios_bfd_interfaces:
        config:
          - name: GigabitEthernet1
            bfd: true
            jitter: false
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
            local_address: 10.0.1.2
            template: ANSIBLE
          - name: GigabitEthernet2
            bfd: true
            jitter: true
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
          - name: GigabitEthernet4
            template: ANSIBLE_Tempalte
        state: merged

    # Commands Fired:
    # ---------------

    # after:
    # -   interval:
    #         input: 100
    #         min_rx: 100
    #         multiplier: 3
    #     jitter: false
    #     local_address: 10.0.1.2
    #     name: GigabitEthernet1
    # -   interval:
    #         input: 100
    #         min_rx: 100
    #         multiplier: 3
    #     name: GigabitEthernet2
    # -   name: GigabitEthernet3
    # -   name: GigabitEthernet4
    #     template: ANSIBLE_Tempalte
    # before:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    # -   name: GigabitEthernet3
    # -   name: GigabitEthernet4
    # changed: true
    # commands:
    # - interface GigabitEthernet1
    # - bfd enable
    # - bfd local-address 10.0.1.2
    # - bfd interval 100 min_rx 100 multiplier 3
    # - bfd template ANSIBLE
    # - no bfd jitter
    # - interface GigabitEthernet2
    # - bfd enable
    # - bfd jitter
    # - bfd interval 100 min_rx 100 multiplier 3
    # - interface GigabitEthernet4
    # - bfd template ANSIBLE_Tempalte

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    #  bfd local-address 10.0.1.2
    #  bfd interval 100 min_rx 100 multiplier 3
    #  no bfd jitter
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    #  bfd interval 100 min_rx 100 multiplier 3
    # interface GigabitEthernet3
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    #  bfd template ANSIBLE_Tempalte

    # Using state: replaced

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    #  bfd local-address 10.0.1.2
    #  bfd interval 100 min_rx 100 multiplier 3
    #  no bfd jitter
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    #  bfd interval 100 min_rx 100 multiplier 3
    # interface GigabitEthernet3
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    #  bfd template ANSIBLE_Tempalte


    - name: Replace BFD configuration for specified interfaces
      cisco.ios.ios_bfd_interfaces:
        config:
          - name: GigabitEthernet1
            bfd: true
            echo: true
            jitter: true
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
            local_address: 10.0.1.2
            template: ANSIBLE
          - name: GigabitEthernet2
            bfd: true
            echo: true
            jitter: true
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
          - name: GigabitEthernet6
            template: ANSIBLE_3Tempalte
        state: replaced

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet1",
    #       "bfd enable",
    #       "bfd echo",
    #       "bfd jitter",
    #       "bfd local-address 10.0.1.2",
    #       "bfd interval 100 min_rx 100 multiplier 3",
    #       "bfd template ANSIBLE",
    #       "interface GigabitEthernet2",
    #       "bfd enable",
    #       "bfd echo",
    #       "bfd jitter",
    #       "bfd interval 100 min_rx 100 multiplier 3",
    #       "no bfd template OLD_TEMPLATE",
    #       "interface GigabitEthernet6",
    #       "bfd template ANSIBLE_3Tempalte"
    #     ]

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd enable
    #  bfd echo
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 100 min_rx 100 multiplier 3
    #  bfd template ANSIBLE
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd enable
    #  bfd echo
    #  bfd jitter
    #  bfd interval 100 min_rx 100 multiplier 3
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3
    # interface GigabitEthernet6
    #  bfd template ANSIBLE_3Tempalte

    # Using state: overridden

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd local-address 10.0.0.1
    #  bfd interval 57 min_rx 66 multiplier 45
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd template OLD_TEMPLATE
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    - name: Override all BFD configuration with provided configuration
      cisco.ios.ios_bfd_interfaces:
        config:
          - name: GigabitEthernet1
            bfd: true
            echo: true
            jitter: true
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
            local_address: 10.0.1.2
            template: ANSIBLE
          - name: GigabitEthernet2
            bfd: true
            echo: true
            jitter: true
            interval:
              input: 100
              min_rx: 100
              multiplier: 3
          - name: GigabitEthernet6
            template: ANSIBLE_3Tempalte
        state: overridden

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet3",
    #       "no bfd jitter",
    #       "no bfd local-address 10.0.1.2",
    #       "no bfd interval 50 min_rx 50 multiplier 3",
    #       "interface GigabitEthernet1",
    #       "bfd enable",
    #       "bfd echo",
    #       "bfd jitter",
    #       "bfd local-address 10.0.1.2",
    #       "bfd interval 100 min_rx 100 multiplier 3",
    #       "bfd template ANSIBLE",
    #       "interface GigabitEthernet2",
    #       "bfd enable",
    #       "bfd echo",
    #       "bfd jitter",
    #       "bfd interval 100 min_rx 100 multiplier 3",
    #       "no bfd template OLD_TEMPLATE",
    #       "interface GigabitEthernet6",
    #       "bfd template ANSIBLE_3Tempalte"
    #     ]

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd enable
    #  bfd echo
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 100 min_rx 100 multiplier 3
    #  bfd template ANSIBLE
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd enable
    #  bfd echo
    #  bfd jitter
    #  bfd interval 100 min_rx 100 multiplier 3
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    # interface GigabitEthernet6
    #  bfd template ANSIBLE_3Tempalte

    # Using state: deleted

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd local-address 10.0.0.1
    #  bfd interval 57 min_rx 66 multiplier 45
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd template OLD_TEMPLATE
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    - name: Delete BFD configuration for specified interfaces
      cisco.ios.ios_bfd_interfaces:
        config:
          - name: GigabitEthernet1
          - name: GigabitEthernet2
        state: deleted

    # Commands Fired:
    # ---------------

    # "commands": [
    #       "interface GigabitEthernet1",
    #       "no bfd local-address 10.0.0.1",
    #       "no bfd interval 57 min_rx 66 multiplier 45",
    #       "interface GigabitEthernet2",
    #       "no bfd template OLD_TEMPLATE"
    #     ]

    # After state:
    # ------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    # Using state: gathered

    # Before state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd local-address 10.0.0.1
    #  bfd interval 57 min_rx 66 multiplier 45
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd template OLD_TEMPLATE
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    - name: Gather listed BFD interfaces config
      cisco.ios.ios_bfd_interfaces:
        state: gathered

    # Module Execution Result:
    # ------------------------

    # "gathered": [
    #     {
    #         "name": "GigabitEthernet1",
    #         "local_address": "10.0.0.1",
    #         "interval": {
    #             "input": 57,
    #             "min_rx": 66,
    #             "multiplier": 45
    #         }
    #     },
    #     {
    #         "name": "GigabitEthernet2",
    #         "template": "OLD_TEMPLATE"
    #     },
    #     {
    #         "name": "GigabitEthernet3",
    #         "jitter": true,
    #         "local_address": "10.0.1.2",
    #         "interval": {
    #             "input": 50,
    #             "min_rx": 50,
    #             "multiplier": 3
    #         }
    #     }
    # ]

    # After state:
    # -------------

    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd local-address 10.0.0.1
    #  bfd interval 57 min_rx 66 multiplier 45
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd template OLD_TEMPLATE
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    # Using state: rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_bfd_interfaces:
        config:
          - name: GigabitEthernet1
            local_address: 10.0.0.1
            interval:
              input: 57
              min_rx: 66
              multiplier: 45
          - name: GigabitEthernet2
            template: OLD_TEMPLATE
          - name: GigabitEthernet3
            jitter: true
            local_address: 10.0.1.2
            interval:
              input: 50
              min_rx: 50
              multiplier: 3
        state: rendered

    # Module Execution Result:
    # ------------------------

    # "rendered": [
    #     "interface GigabitEthernet1",
    #     "bfd local-address 10.0.0.1",
    #     "bfd interval 57 min_rx 66 multiplier 45",
    #     "interface GigabitEthernet2",
    #     "bfd template OLD_TEMPLATE",
    #     "interface GigabitEthernet3",
    #     "bfd jitter",
    #     "bfd local-address 10.0.1.2",
    #     "bfd interval 50 min_rx 50 multiplier 3"
    # ]

    # Using state: parsed

    # File: parsed.cfg
    # ----------------

    # interface GigabitEthernet1
    #  description Ansible UT interface 1
    #  no shutdown
    #  bfd local-address 10.0.0.1
    #  bfd interval 57 min_rx 66 multiplier 45
    # interface GigabitEthernet2
    #  description Ansible UT interface 2
    #  ip address dhcp
    #  bfd template OLD_TEMPLATE
    # interface GigabitEthernet3
    #  description Ansible UT interface 3
    #  no ip address
    #  shutdown
    #  no bfd jitter
    #  bfd local-address 10.0.1.2
    #  bfd interval 50 min_rx 50 multiplier 3

    - name: Parse the provided configuration with the existing running configuration
      cisco.ios.ios_bfd_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------

    # "parsed": [
    #     {
    #         "name": "GigabitEthernet1",
    #         "local_address": "10.0.0.1",
    #         "interval": {
    #             "input": 57,
    #             "min_rx": 66,
    #             "multiplier": 45
    #         }
    #     },
    #     {
    #         "name": "GigabitEthernet2",
    #         "template": "OLD_TEMPLATE"
    #     },
    #     {
    #         "name": "GigabitEthernet3",
    #         "jitter": false,
    #         "local_address": "10.0.1.2",
    #         "interval": {
    #             "input": 50,
    #             "min_rx": 50,
    #             "multiplier": 3
    #         }
    #     }
    # ]



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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/2&#x27;, &#x27;no bfd jitter&#x27;, &#x27;bfd interval 100 min_rx 100 multiplier 3&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/2&#x27;, &#x27;bfd echo&#x27;, &#x27;bfd jitter&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
