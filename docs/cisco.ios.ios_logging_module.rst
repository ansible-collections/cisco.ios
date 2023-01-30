.. _cisco.ios.ios_logging_module:


*********************
cisco.ios.ios_logging
*********************

**(deprecated, removed after 2023-06-01) Manage logging on network devices**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2023-06-01
:Why: Newer and updated modules released with more functionality.
:Alternative: ios_logging_global



Synopsis
--------
- This module provides declarative management of logging on Cisco Ios devices.




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
                    <b>aggregate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of logging definitions.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>on</li>
                                    <li>host</li>
                                    <li>console</li>
                                    <li>monitor</li>
                                    <li>buffered</li>
                                    <li>trap</li>
                        </ul>
                </td>
                <td>
                        <div>Destination of the logs.</div>
                        <div>On dest has to be quoted as &#x27;on&#x27; or else pyyaml will convert to True before it gets to Ansible.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set logging facility.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>emergencies</li>
                                    <li>alerts</li>
                                    <li>critical</li>
                                    <li>errors</li>
                                    <li>warnings</li>
                                    <li>notifications</li>
                                    <li>informational</li>
                                    <li>debugging</li>
                        </ul>
                </td>
                <td>
                        <div>Set logging severity levels.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The hostname or IP address of the destination.</div>
                        <div>Required when <em>dest=host</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>size</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Size of buffer. The acceptable value is in range from 4096 to 4294967295 bytes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>present</li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>State of the logging configuration.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>on</li>
                                    <li>host</li>
                                    <li>console</li>
                                    <li>monitor</li>
                                    <li>buffered</li>
                                    <li>trap</li>
                        </ul>
                </td>
                <td>
                        <div>Destination of the logs.</div>
                        <div>On dest has to be quoted as &#x27;on&#x27; or else pyyaml will convert to True before it gets to Ansible.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set logging facility.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>emergencies</li>
                                    <li>alerts</li>
                                    <li>critical</li>
                                    <li>errors</li>
                                    <li>warnings</li>
                                    <li>notifications</li>
                                    <li>informational</li>
                                    <li><div style="color: blue"><b>debugging</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Set logging severity levels.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
                        <div>The hostname or IP address of the destination.</div>
                        <div>Required when <em>dest=host</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>size</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Size of buffer. The acceptable value is in range from 4096 to 4294967295 bytes.</div>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>State of the logging configuration.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against IOS 15.6
   - The 'Default System Message Logging Configuration' of the ios device like facility Local7 or logging on is not subjected to idempotency causes
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    - name: Configure host logging
      cisco.ios.ios_logging:
        dest: host
        name: 172.16.0.1
        state: present

    - name: Remove host logging configuration
      cisco.ios.ios_logging:
        dest: host
        name: 172.16.0.1
        state: absent

    - name: Configure console logging level and facility
      cisco.ios.ios_logging:
        dest: console
        facility: local7
        level: debugging
        state: present

    - name: Enable logging to all
      cisco.ios.ios_logging:
        dest: on

    - name: Configure buffer size
      cisco.ios.ios_logging:
        dest: buffered
        size: 5000

    - name: Configure logging using aggregate
      cisco.ios.ios_logging:
        aggregate:
        - {dest: console, level: notifications}
        - {dest: buffered, size: 9000}

    - name: Remove logging using aggregate
      cisco.ios.ios_logging:
        aggregate:
        - {dest: console, level: notifications}
        - {dest: buffered, size: 9000}
        state: absent



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
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The list of configuration mode commands to send to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;logging facility local7&#x27;, &#x27;logging host 172.16.0.1&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in a release after 2023-06-01. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
