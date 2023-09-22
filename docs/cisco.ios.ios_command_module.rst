.. _cisco.ios.ios_command_module:


*********************
cisco.ios.ios_command
*********************

**Module to run commands on remote devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Sends arbitrary commands to an ios node and returns the results read from the device. This module includes an argument that will cause the module to wait for a specific condition before returning or timing out if the condition is not met.
- This module does not support running commands in configuration mode. Please use `ios_config <https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_config_module.html#ansible-collections-cisco-ios-ios-config-module>`_ to configure IOS devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of commands to send to the remote ios device over the configured provider. The resulting output from the command is returned. If the <em>wait_for</em> argument is provided, the module is not returned until the condition is satisfied or the number of retries has expired. If a command sent to the device requires answering a prompt, it is possible to pass a dict containing <em>command</em>, <em>answer</em> and <em>prompt</em>. Common answers are &#x27;y&#x27; or &quot;\r&quot; (carriage return, must be double quotes). See examples.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                <td>
                        <div>Configures the interval in seconds to wait between retries of the command. If the command does not pass the specified conditions, the interval indicates how long to wait before trying the command again.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>any</li>
                                    <li><div style="color: blue"><b>all</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>The <em>match</em> argument is used in conjunction with the <em>wait_for</em> argument to specify the match policy.  Valid values are <code>all</code> or <code>any</code>.  If the value is set to <code>all</code> then all conditionals in the wait_for must be satisfied.  If the value is set to <code>any</code> then only one of the values must be satisfied.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">9</div>
                </td>
                <td>
                        <div>Specifies the number of retries a command should by tried before it is considered failed. The command is run on the target device every retry and evaluated against the <em>wait_for</em> conditions.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wait_for</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of conditions to evaluate against the output of the command. The task will wait for each condition to be true before moving forward. If the conditional is not true within the configured number of retries, the task fails. See examples.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: waitfor</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.3 on CML.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    - name: Run show version on remote devices
      cisco.ios.ios_command:
        commands: show version

    # output-

    # ok: [iosxeappliance] => {
    #     "changed": false,
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 "show version"
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": null
    #         }
    #     },
    #     "stdout": [
    #         "Cisco IOS XE Software, Version 17.03.04a\nCisco IOS Software [Amsterdam], Virtual XE Software ... register is 0x2102"
    #     ],
    #     "stdout_lines": [
    #         [
    #             "Cisco IOS XE Software, Version 17.03.04a",
    #             "Cisco IOS Software [Amsterdam], Virtual XE Software",
    #             "..."
    #             "Configuration register is 0x2102"
    #         ]
    #     ]
    # }

    - name: Run show version and check to see if output contains IOS
      cisco.ios.ios_command:
        commands: show version
        wait_for: result[0] contains IOS

    # output-

    # ok: [iosxeappliance] => {
    #     "changed": false,
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 "show version"
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": [
    #                 "result[0] contains IOS"
    #             ]
    #         }
    #     },
    #     "stdout": [
    #         "Cisco IOS XE Software, Version 17.03.04a\nCisco IOS Software [Amsterdam], Virtual XE Software ... register is 0x2102"
    #     ],
    #     "stdout_lines": [
    #         [
    #             "Cisco IOS XE Software, Version 17.03.04a",
    #             "Cisco IOS Software [Amsterdam], Virtual XE Software",
    #             "..."
    #             "Configuration register is 0x2102"
    #         ]
    #     ]
    # }

    - name: Run multiple commands on remote nodes
      cisco.ios.ios_command:
        commands:
          - show version
          - show interfaces

    # output-

    # ok: [iosxeappliance] => {
    #     "changed": false,
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 "show version",
    #                 "show interfaces"
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": null
    #         }
    #     },
    #     "stdout": [
    #         "Cisco IOS XE Software, Version 17.03.04a\nCisco IOS Software [Amsterdam], Virtual XE Software Configuration register is 0x2102",
    #         "Loopback999 is up, line protocol is up ...failures, 0 output buffers swapped out"
    #     ],
    #     "stdout_lines": [
    #         [
    #             "Cisco IOS XE Software, Version 17.03.04a",
    #             "Cisco IOS Software [Amsterdam], Virtual XE Software",
    #             "..."
    #             "Configuration register is 0x2102"
    #         ],
    #         [
    #             "Loopback999 is up, line protocol is up ",
    #             "  Hardware is Loopback",
    #             "  Description: this is a test",
    #             "  MTU 1514 bytes, BW 8000000 Kbit/sec, DLY 5000 usec, ",
    #             "     reliability 255/255, txload 1/255, rxload 1/255",
    #             "  Encapsulation LOOPBACK, loopback not set",
    #             "  Keepalive set (10 sec)",
    #             "  Last input never, output never, output hang never",
    #             "  Last clearing of \"show interface\" counters never",
    #             "  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0",
    #             "  Queueing strategy: fifo",
    #             "  Output queue: 0/0 (size/max)",
    #             "  5 minute input rate 0 bits/sec, 0 packets/sec",
    #             "  5 minute output rate 0 bits/sec, 0 packets/sec",
    #             "     0 packets input, 0 bytes, 0 no buffer",
    #             "     Received 0 broadcasts (0 IP multicasts)",
    #             "     0 runts, 0 giants, 0 throttles ",
    #             "     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort",
    #             "     0 packets output, 0 bytes, 0 underruns",
    #             "     Output 0 broadcasts (0 IP multicasts)",
    #             "     0 output errors, 0 collisions, 0 interface resets",
    #             "     0 unknown protocol drops",
    #             "     0 output buffer failures, 0 output buffers swapped out"
    #         ]
    #     ]
    # }

    - name: Run multiple commands and evaluate the output
      cisco.ios.ios_command:
        commands:
          - show version
          - show interfaces
        wait_for:
          - result[0] contains IOS
          - result[1] contains Loopback0

    # output-
    # failed play as result[1] contains Loopback0 is false

    # fatal: [iosxeappliance]: FAILED! => {
    #     "changed": false,
    #     "failed_conditions": [
    #         "result[1] contains Loopback0"
    #     ],
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 "show version",
    #                 "show interfaces"
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": [
    #                 "result[0] contains IOS",
    #                 "result[1] contains Loopback0"
    #             ]
    #         }
    #     },
    #     "msg": "One or more conditional statements have not been satisfied"
    # }

    - name: Run commands that require answering a prompt
      cisco.ios.ios_command:
        commands:
          - command: "clear counters GigabitEthernet2"
            prompt: 'Clear "show interface" counters on this interface \[confirm\]'
            answer: "y"
          - command: "clear counters GigabitEthernet3"
            prompt: "[confirm]"
            answer: "\r"

    # output-

    # ok: [iosxeappliance] => {
    #     "changed": false,
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 {
    #                     "answer": "y",
    #                     "check_all": false,
    #                     "command": "clear counters GigabitEthernet2",
    #                     "newline": true,
    #                     "output": null,
    #                     "prompt": "Clear \"show interface\" counters on this interface \\[confirm\\]",
    #                     "sendonly": false
    #                 },
    #                 {
    #                     "answer": "\r",
    #                     "check_all": false,
    #                     "command": "clear counters GigabitEthernet3",
    #                     "newline": true,
    #                     "output": null,
    #                     "prompt": "[confirm]",
    #                     "sendonly": false
    #                 }
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": null
    #         }
    #     },
    #     "stdout": [
    #         "Clear \"show interface\" counters on this interface [confirm]y",
    #         "Clear \"show interface\" counters on this interface [confirm]"
    #     ],
    #     "stdout_lines": [
    #         [
    #             "Clear \"show interface\" counters on this interface [confirm]y"
    #         ],
    #         [
    #             "Clear \"show interface\" counters on this interface [confirm]"
    #         ]
    #     ]
    # }

    - name: Run commands with complex values like special characters in variables
      cisco.ios.ios_command:
        commands:
          ["{{ 'test aaa group TEST ' ~ user ~ ' ' ~ password ~ ' new-code' }}"]
      vars:
        user: "dummy"
        password: "!dummy"

    # ok: [iosxeappliance] => {
    #     "changed": false,
    #     "invocation": {
    #         "module_args": {
    #             "commands": [
    #                 "test aaa group group test !dummy new-code"
    #             ],
    #             "interval": 1,
    #             "match": "all",
    #             "retries": 10,
    #             "wait_for": null
    #         }
    #     },
    #     "stdout": [
    #         "User was successfully authenticated."
    #     ],
    #     "stdout_lines": [
    #         [
    #             "User was successfully authenticated."
    #         ]
    #     ]
    # }



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
                    <b>failed_conditions</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>failed</td>
                <td>
                            <div>The list of conditionals that have failed</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;...&#x27;, &#x27;...&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always apart from low level errors (such as action plugin)</td>
                <td>
                            <div>The set of responses from the commands</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;...&#x27;, &#x27;...&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout_lines</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always apart from low level errors (such as action plugin)</td>
                <td>
                            <div>The value of stdout split into a list</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[[&#x27;...&#x27;, &#x27;...&#x27;], [&#x27;...&#x27;], [&#x27;...&#x27;]]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Peter Sprygada (@privateip)
