.. _cisco.ios.ios_banner_module:


********************
cisco.ios.ios_banner
********************

**Module to configure multiline banners.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This will configure both login and motd banners on remote devices running Cisco IOS. It allows playbooks to add or remote banner text from the active running configuration.




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
                    <b>banner</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>login</li>
                                    <li>motd</li>
                                    <li>exec</li>
                                    <li>incoming</li>
                                    <li>slip-ppp</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies which banner should be configured on the remote device. In Ansible 2.4 and earlier only <em>login</em> and <em>motd</em> were supported.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multiline_delimiter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"@"</div>
                </td>
                <td>
                        <div>Specify the delimiting character than will be used for configuration.</div>
                </td>
            </tr>
            <tr>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies whether or not the configuration is present in the current devices active running configuration.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The banner text that should be present in the remote device running configuration.  This argument accepts a multiline string, with no empty lines. Requires <em>state=present</em>.</div>
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

    - name: Configure the login banner
      cisco.ios.ios_banner:
        banner: login
        text: |
          this is my login banner
          that contains a multiline
          string
        state: present

    - name: Remove the motd banner
      cisco.ios.ios_banner:
        banner: motd
        state: absent

    - name: Configure banner from file
      cisco.ios.ios_banner:
        banner: motd
        text: "{{ lookup('file', './config_partial/raw_banner.cfg') }}"  # Use unix formatted text files (LF not CRLF) to avoid idempotency issues.
        state: present

    - name: Configure the login banner using delimiter
      cisco.ios.ios_banner:
        banner: login
        multiline_delimiter: x
        text: this is my login banner
        state: present



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;banner login&#x27;, &#x27;this is my login banner&#x27;, &#x27;that contains a multiline&#x27;, &#x27;string&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ricardo Carrillo Cruz (@rcarrillocruz)
