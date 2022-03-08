.. _cisco.ios.ios_cliconf:


*************
cisco.ios.ios
*************

**Use ios cliconf to run command on Cisco IOS platform**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This ios plugin provides low level abstraction apis for sending and receiving CLI commands from Cisco IOS network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config_commands</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.0.0</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                                <div>var: ansible_ios_config_commands</div>
                    </td>
                <td>
                        <div>Specifies a list of commands that can make configuration changes to the target device.</div>
                        <div>When `ansible_network_single_user_mode` is enabled, if a command sent to the device is present in this list, the existing cache is invalidated.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Networking Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
