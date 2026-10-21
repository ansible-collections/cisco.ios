.. _cisco.ios.ios_monitor_sessions_module:


******************************
cisco.ios.ios_monitor_sessions
******************************

**Resource module to configure SPAN monitor sessions.**


Version added: 11.7.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of SPAN (Switched Port Analyzer) monitor sessions on Cisco IOS-XE devices.
- Each monitor session defines one or more source interfaces whose traffic is mirrored to a destination interface.
- Only local SPAN (source interface to destination interface) is supported. VLAN-based sources, RSPAN (remote SPAN), and ERSPAN are not covered by this module.




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
                        <div>List of monitor session configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>destination</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination interface configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encapsulation_replicate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Replicate the encapsulation of the monitored traffic.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Destination interface name.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>session</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Monitor session number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sources</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of source interface specifications.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>direction</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>rx</li>
                                    <li>tx</li>
                                    <li><div style="color: blue"><b>both</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Traffic direction to monitor on the source interface.</div>
                        <div><code>both</code> is the default when no direction is specified.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interfaces</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of source interface names for this source entry.</div>
                        <div>Each element is a single interface name (e.g. <code>Gi1/0/1</code>, <code>Po2</code>) or a range string exactly as it appears in the running configuration (e.g. <code>Gi1/0/1 - 3</code>).</div>
                        <div>All interfaces in the list share the same <code>direction</code>.</div>
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
                        <div>The value of this option should be the output of <b>show running-config | section ^monitor session</b> executed on the device.</div>
                        <div>The state <em>parsed</em> reads the configuration from this option and transforms it into Ansible structured data as per the resource module&#x27;s argspec.</div>
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
                        <div>The state the configuration should be left in.</div>
                        <div><em>merged</em> adds or updates monitor sessions without removing existing ones.</div>
                        <div><em>replaced</em> replaces source and destination configuration for the specified sessions, leaving unspecified sessions intact.</div>
                        <div><em>overridden</em> replaces the entire monitor session configuration; sessions not present in <code>config</code> are removed.</div>
                        <div><em>deleted</em> removes the specified sessions, or all sessions when <code>config</code> is omitted.</div>
                        <div><em>rendered</em> generates CLI commands from <code>config</code> without connecting to the device.</div>
                        <div><em>gathered</em> retrieves and returns the running configuration as structured data without modifying the device.</div>
                        <div><em>parsed</em> parses the configuration provided in <code>running_config</code> and returns structured data.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS-XE on Cat9k switches.
   - This module works with connection ``network_cli``.
   - Interface names in ``config`` must match the abbreviated form used in the running configuration (e.g. ``Gi1/0/1``, ``Po2``, ``Twe1/0/2``).



Examples
--------

.. code-block:: yaml

    # Using state: merged

    # Before state:
    # -------------
    # (no monitor session configuration)

    - name: Configure SPAN session 1 with multiple sources and replicate encapsulation
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 1
            sources:
              - interfaces:
                  - Twe1/0/2
                  - Twe1/0/12
                  - Twe1/0/45
              - interfaces:
                  - Po2
            destination:
              interface: Po3
              encapsulation_replicate: true
        state: merged

    # Commands fired:
    # ---------------
    # monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45 , Po2
    # monitor session 1 destination interface Po3 encapsulation replicate

    # After state:
    # ------------
    # monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
    # monitor session 1 source interface Po2
    # monitor session 1 destination interface Po3 encapsulation replicate

    # Using state: merged with direction

    # Before state:
    # -------------
    # (no monitor session configuration)

    - name: Configure SPAN session with rx-only sources
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 2
            sources:
              - interfaces:
                  - "Gi1/0/1 - 3"
                direction: rx
              - interfaces:
                  - Gi1/0/5
            destination:
              interface: Gi1/0/48
        state: merged

    # Commands fired:
    # ---------------
    # monitor session 2 source interface Gi1/0/1 , Gi1/0/2 , Gi1/0/3 rx
    # monitor session 2 source interface Gi1/0/5
    # monitor session 2 destination interface Gi1/0/48

    # Using state: replaced

    # Before state:
    # -------------
    # monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
    # monitor session 1 source interface Po2
    # monitor session 1 destination interface Po3 encapsulation replicate

    - name: Replace session 1 with updated source list
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 1
            sources:
              - interfaces:
                  - Po2
              - interfaces:
                  - Po4
            destination:
              interface: Po3
              encapsulation_replicate: true
        state: replaced

    # Commands fired:
    # ---------------
    # no monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
    # monitor session 1 source interface Po4

    # After state:
    # ------------
    # monitor session 1 source interface Po2
    # monitor session 1 source interface Po4
    # monitor session 1 destination interface Po3 encapsulation replicate

    # Using state: overridden

    # Before state:
    # -------------
    # monitor session 1 source interface Po2
    # monitor session 1 destination interface Po3 encapsulation replicate
    # monitor session 2 source interface Gi1/0/1
    # monitor session 2 destination interface Gi1/0/48

    - name: Override all sessions - remove session 2 and update session 1
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 1
            sources:
              - interfaces:
                  - Po2
            destination:
              interface: Po3
              encapsulation_replicate: true
        state: overridden

    # Commands fired:
    # ---------------
    # no monitor session 2

    # Using state: deleted - specific session

    - name: Delete monitor session 1
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 1
        state: deleted

    # Commands fired:
    # ---------------
    # no monitor session 1

    # Using state: deleted - all sessions

    - name: Delete all monitor sessions
      cisco.ios.ios_monitor_sessions:
        state: deleted

    # Commands fired:
    # ---------------
    # no monitor session 1
    # no monitor session 2

    # Using state: gathered

    - name: Gather monitor session facts
      cisco.ios.ios_monitor_sessions:
        state: gathered

    # Returns:
    # gathered:
    #   - session: 1
    #     sources:
    #       - interfaces:
    #           - Twe1/0/2
    #           - Twe1/0/12
    #           - Twe1/0/45
    #         direction: both
    #       - interfaces:
    #           - Po2
    #         direction: both
    #     destination:
    #       interface: Po3
    #       encapsulation_replicate: true

    # Using state: rendered

    - name: Render monitor session commands without connecting to the device
      cisco.ios.ios_monitor_sessions:
        config:
          - session: 1
            sources:
              - interfaces:
                  - Po2
            destination:
              interface: Po3
              encapsulation_replicate: true
        state: rendered

    # Returns:
    # rendered:
    #   - monitor session 1 source interface Po2
    #   - monitor session 1 destination interface Po3 encapsulation replicate

    # Using state: parsed

    - name: Parse monitor session configuration
      cisco.ios.ios_monitor_sessions:
        running_config: |
          monitor session 1 source interface Twe1/0/2 , Twe1/0/12 , Twe1/0/45
          monitor session 1 source interface Po2
          monitor session 1 destination interface Po3 encapsulation replicate
        state: parsed

    # Returns:
    # parsed:
    #   - session: 1
    #     sources:
    #       - interfaces:
    #           - Twe1/0/2
    #           - Twe1/0/12
    #           - Twe1/0/45
    #         direction: both
    #       - interfaces:
    #           - Po2
    #         direction: both
    #     destination:
    #       interface: Po3
    #       encapsulation_replicate: true



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
                            <div>The resulting configuration module invocation.</div>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;monitor session 1 source interface Po2&#x27;, &#x27;monitor session 1 destination interface Po3 encapsulation replicate&#x27;]</div>
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
                            <div>The device native config provided in <em>running_config</em> option, parsed into structured data as per module argspec.</div>
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
                            <div>The set of CLI commands generated from the value of <em>config</em> option.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;monitor session 1 source interface Po2&#x27;, &#x27;monitor session 1 destination interface Po3 encapsulation replicate&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jorgen Spange (@jorgenspange)
