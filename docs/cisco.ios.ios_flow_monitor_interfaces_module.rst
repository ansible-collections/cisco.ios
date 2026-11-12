.. _cisco.ios.ios_flow_monitor_interfaces_module:


*************************************
cisco.ios.ios_flow_monitor_interfaces
*************************************

**Resource module to configure per-interface flow monitor assignments on Cisco IOS XE.**


Version added: 11.7.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the per-interface ``ip flow monitor`` configuration on Cisco IOS XE devices.
- It assigns flow monitors (with a sampler and direction) to interfaces.
- Flow monitor and sampler names referenced here must already exist on the device; use :ref:`cisco.ios.ios_flow_monitor_global <cisco.ios.ios_flow_monitor_global_module>` to create them.




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
                        <div>A list of interfaces with flow monitor assignments.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>flow_monitors</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of flow monitor assignments on this interface.</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>input</li>
                                    <li>output</li>
                        </ul>
                </td>
                <td>
                        <div>Traffic direction to monitor.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>monitor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the flow monitor to apply.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>ip</b>&nbsp;&larr;</div></li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>IP protocol family for the flow monitor assignment.</div>
                        <div>Use <code>ipv6</code> to assign the monitor to IPv6 traffic (<code>ipv6 flow monitor ...</code>).</div>
                        <div>Defaults to <code>ip</code> for standard IPv4 monitoring.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sampler</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the sampler to use with this monitor.</div>
                        <div>Optional, an unsampled monitor can be assigned without a sampler.</div>
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
                        <div>Name of the interface, e.g. GigabitEthernet0/1, Port-channel21.800.</div>
                        <div>Short interface names like Gi0/1 are normalized to the full name.</div>
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
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec.</div>
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
                        <div>State <em>merged</em> merges the provided flow monitor assignments into existing interface config.</div>
                        <div>State <em>replaced</em> replaces the flow monitor assignments for specified interfaces only.</div>
                        <div>State <em>overridden</em> replaces flow monitor assignments across all interfaces.</div>
                        <div>State <em>deleted</em> removes the specified (or all) flow monitor assignments.</div>
                        <div>State <em>rendered</em>, <em>gathered</em> and <em>parsed</em> do not perform any change on the device.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS XE.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - Short interface names (e.g. Gi1/0/1) are normalized and are compared with the full names on the device.
   - A ``protocol=ipv6`` assignment needs IPv6 routing enabled (``ipv6 unicast-routing``) and a flow monitor whose record matches IPv6 fields. Otherwise IOS XE drops the ``ipv6 flow monitor`` line without an error and the module reports the assignment as changed on every run.
   - A flow record that matches both IPv4 and IPv6 fields cannot be attached to an interface, IOS XE refuses it with ``Unsupported key field``. Use one flow monitor for ``ip`` and another for ``ipv6`` on the same interface.
   - The module examples use callback plugin (stdout_callback = yaml) to generate task output in yaml format.



Examples
--------

.. code-block:: yaml

    # Using state: merged

    # Before state:
    # router# show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address 192.0.2.10 255.255.255.0

    - name: Assign flow monitors to interfaces
      cisco.ios.ios_flow_monitor_interfaces:
        config:
          - name: GigabitEthernet1
            flow_monitors:
              - monitor: FLOW_MONITOR_IN
                sampler: FLOW_SAMPLER
                direction: input
              - monitor: FLOW_MONITOR_OUT
                sampler: FLOW_SAMPLER
                direction: output
        state: merged

    # Commands fired:
    # interface GigabitEthernet1
    #  ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
    #  ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output

    # Using state: deleted

    - name: Remove flow monitors from specific interfaces
      cisco.ios.ios_flow_monitor_interfaces:
        config:
          - name: GigabitEthernet1
        state: deleted

    # Using state: deleted — remove all

    - name: Remove all interface flow monitor assignments
      cisco.ios.ios_flow_monitor_interfaces:
        state: deleted

    # Using state: replaced

    # Before state:
    # interface GigabitEthernet1
    #  ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input
    #  ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output

    - name: Replace flow monitors on GigabitEthernet1
      cisco.ios.ios_flow_monitor_interfaces:
        config:
          - name: GigabitEthernet1
            flow_monitors:
              - monitor: FLOW_MONITOR_IN
                sampler: FLOW_SAMPLER
                direction: input
              - monitor: FLOW_MONITOR_OUT
                sampler: FLOW_SAMPLER
                direction: output
        state: replaced

    # Commands fired:
    # interface GigabitEthernet1
    #  no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER input
    #  no ip flow monitor OLD_MONITOR sampler FLOW_SAMPLER output
    #  ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
    #  ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output

    # Using state: parsed

    - name: Parse interface config into structured data
      cisco.ios.ios_flow_monitor_interfaces:
        running_config: |
          interface GigabitEthernet1
           ip address 192.0.2.10 255.255.255.0
           ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input
           ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output
        state: parsed

    # Using state: merged — with IPv6 monitor

    - name: Assign IPv6 flow monitor to interface
      cisco.ios.ios_flow_monitor_interfaces:
        config:
          - name: GigabitEthernet1
            flow_monitors:
              - monitor: FLOW_MONITOR_V6
                sampler: FLOW_SAMPLER
                direction: input
                protocol: ipv6
        state: merged

    # Commands fired:
    # interface GigabitEthernet1
    #  ipv6 flow monitor FLOW_MONITOR_V6 sampler FLOW_SAMPLER input

    # Using state: gathered

    - name: Gather flow monitor interface assignments
      cisco.ios.ios_flow_monitor_interfaces:
        state: gathered



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
                <td>always</td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet1&#x27;, &#x27;ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input&#x27;, &#x27;ip flow monitor FLOW_MONITOR_OUT sampler FLOW_SAMPLER output&#x27;]</div>
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
                            <div>The device native config provided in <em>running_config</em> option, parsed into structured data.</div>
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
                            <div>The set of CLI commands generated from the value of <em>state=rendered</em> option.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet1&#x27;, &#x27;ip flow monitor FLOW_MONITOR_IN sampler FLOW_SAMPLER input&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jorgen Spange (@jorgenspange)
