.. _cisco.ios.ios_user_module:


******************
cisco.ios.ios_user
******************

**Module to manage the aggregates of local users.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of the local usernames configured on network devices. It allows playbooks to manage either individual usernames or the aggregate of usernames in the current running config. It also supports purging usernames from the configuration that are not explicitly defined.




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
                        <div>The set of username objects to be configured on the remote Cisco IOS device. The list entries can either be the username or a hash of username and properties. This argument is mutually exclusive with the <code>name</code> argument.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: users, collection</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>configured_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The password to be configured on the Cisco IOS device. The password needs to be provided in clear and it will be encrypted on the device. Please note that this option is not same as <code>provider password</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hashed_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option allows configuring hashed passwords on Cisco IOS devices.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the type of hash (e.g., 5 for MD5, 8 for PBKDF2, etc.)</div>
                        <div>For this to work, the device needs to support the desired hash type</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The actual hashed password to be configured on the device</div>
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
                        <div>The username to be configured on the Cisco IOS device. This argument accepts a string value and is mutually exclusive with the <code>aggregate</code> argument. Please note that this option is not same as <code>provider username</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nopassword</b>
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
                        <div>Defines the username without assigning a password. This will allow the user to login to the system without being authenticated by a password.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>secret</li>
                                    <li>password</li>
                        </ul>
                </td>
                <td>
                        <div>This argument determines whether a &#x27;password&#x27; or &#x27;secret&#x27; will be configured.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>privilege</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <code>privilege</code> argument configures the privilege level of the user when logged into the system. This argument accepts integer values in the range of 1 to 15.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sshkey</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies one or more SSH public key(s) to configure for the given username.</div>
                        <div>This argument accepts a valid SSH key value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                                    <li>present</li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Configures the state of the username definition as it relates to the device operational configuration. When set to <em>present</em>, the username(s) should be configured in the device active configuration and when set to <em>absent</em> the username(s) should not be in the device active configuration</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>update_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>on_create</li>
                                    <li>always</li>
                        </ul>
                </td>
                <td>
                        <div>Since passwords are encrypted in the device running config, this argument will instruct the module when to change the password.  When set to <code>always</code>, the password will always be updated in the device and when set to <code>on_create</code> the password will be updated only if the username is created.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>view</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures the view for the username in the device running configuration. The argument accepts a string value defining the view name. This argument does not check if the view has been configured on the device.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: role</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>configured_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The password to be configured on the Cisco IOS device. The password needs to be provided in clear and it will be encrypted on the device. Please note that this option is not same as <code>provider password</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hashed_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option allows configuring hashed passwords on Cisco IOS devices.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the type of hash (e.g., 5 for MD5, 8 for PBKDF2, etc.)</div>
                        <div>For this to work, the device needs to support the desired hash type</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The actual hashed password to be configured on the device</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
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
                        <div>The username to be configured on the Cisco IOS device. This argument accepts a string value and is mutually exclusive with the <code>aggregate</code> argument. Please note that this option is not same as <code>provider username</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nopassword</b>
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
                        <div>Defines the username without assigning a password. This will allow the user to login to the system without being authenticated by a password.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>secret</b>&nbsp;&larr;</div></li>
                                    <li>password</li>
                        </ul>
                </td>
                <td>
                        <div>This argument determines whether a &#x27;password&#x27; or &#x27;secret&#x27; will be configured.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>privilege</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <code>privilege</code> argument configures the privilege level of the user when logged into the system. This argument accepts integer values in the range of 1 to 15.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>purge</b>
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
                        <div>Instructs the module to consider the resource definition absolute. It will remove any previously configured usernames on the device with the exception of the `admin` user (the current defined set of users).</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sshkey</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies one or more SSH public key(s) to configure for the given username.</div>
                        <div>This argument accepts a valid SSH key value.</div>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Configures the state of the username definition as it relates to the device operational configuration. When set to <em>present</em>, the username(s) should be configured in the device active configuration and when set to <em>absent</em> the username(s) should not be in the device active configuration</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>update_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>on_create</li>
                                    <li><div style="color: blue"><b>always</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Since passwords are encrypted in the device running config, this argument will instruct the module when to change the password.  When set to <code>always</code>, the password will always be updated in the device and when set to <code>on_create</code> the password will be updated only if the username is created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>view</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures the view for the username in the device running configuration. The argument accepts a string value defining the view name. This argument does not check if the view has been configured on the device.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: role</div>
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

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username testuser privilege 15 password 0 password

    # Present state create a new user play:
    # -------------------------------------

    - name: Create a new user
      cisco.ios.ios_user:
        name: ansible
        nopassword: true
        sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        state: present

    # Task Output
    # -----------

    # commands:
    # - ip ssh pubkey-chain
    # - username ansible
    # - key-hash ssh-rsa 2ABB27BBC33ED53EF7D55037952ABB27 test@fedora
    # - exit
    # - exit
    # - username ansible nopassword

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username testuser privilege 15 password 0 password
    # username ansible nopassword
    #   username ansible
    #    key-hash ssh-rsa 2ABB27BBC33ED53EF7D55037952ABB27 test@fedora

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username testuser privilege 15 password 0 password

    # Present state create a new user with multiple keys play:
    # --------------------------------------------------------

    - name: Create a new user with multiple keys
      cisco.ios.ios_user:
        name: ansible
        sshkey:
          - "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
          - "{{ lookup('file', '~/path/to/public_key') }}"
        state: present

    # Task Output
    # -----------

    # commands:
    # - ip ssh pubkey-chain
    # - username ansible
    # - key-hash ssh-rsa 2ABB27BBC33ED53EF7D55037952ABB27 test@fedora
    # - key-hash ssh-rsa 1985673DCF7FA9A0F374BB97DC2ABB27 test@fedora
    # - exit
    # - exit

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username testuser privilege 15 password 0 password
    #   username ansible
    #    key-hash ssh-rsa 2ABB27BBC33ED53EF7D55037952ABB27 test@fedora
    #    key-hash ssh-rsa 1985673DCF7FA9A0F374BB97DC2ABB27 test@fedora

    # Using Purge: true

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username testuser privilege 15 password 0 password
    # username ansible nopassword
    #   username ansible
    #    key-hash ssh-rsa 2ABB27BBC33ED53EF7D55037952ABB27 test@fedora

    # Purge all users except admin play:
    # ----------------------------------

    - name: Remove all users except admin
      cisco.ios.ios_user:
        purge: true

    # Task Output
    # -----------

    # commands:
    # - no username testuser
    # - no username ansible
    # - ip ssh pubkey-chain
    # - no username ansible
    # - exit

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password

    # Using Purge: true

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username testuser privilege 15 password 0 password1
    # username testuser1 privilege 15 password 0 password2
    # username ansible nopassword

    # Purge all users except admin and these listed users play:
    # ---------------------------------------------------------

    - name: Remove all users except admin and these listed users
      cisco.ios.ios_user:
        aggregate:
          - name: testuser
          - name: testuser1
        purge: true

    # Task Output
    # -----------

    # commands:
    # - no username ansible

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password
    # username testuser privilege 15 password 0 password1
    # username testuser1 privilege 15 password 0 password2

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username netop password 0 password1
    # username netend password 0 password2

    # Present state set multiple users to privilege level 15 play:
    # ------------------------------------------------------------

    - name: Set multiple users to privilege level 15
      cisco.ios.ios_user:
        aggregate:
          - name: netop
          - name: netend
        privilege: 15
        state: present

    # Task Output
    # -----------

    # commands:
    # - username netop privilege 15
    # - username netend privilege 15

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password
    # username netop privilege 15 password 0 password1
    # username netend privilege 15 password 0 password2

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username netop privilege 15 password 0 oldpassword

    # Present state Change Password for User netop play:
    # --------------------------------------------

    - name: Change Password for User netop
      cisco.ios.ios_user:
        name: netop
        configured_password: "newpassword"
        password_type: password
        update_password: always
        state: present

    # Task Output
    # -----------

    # commands:
    # - username netop password newpassword

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password
    # username netop privilege 15 password 0 newpassword

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username netop privilege 15 password 0 password
    # username netend privilege 15 password 0 password

    # Present state set user view/role for users play:
    # --------------------------------------------

    - name: Set user view/role for users
      cisco.ios.ios_user:
        aggregate:
          - name: netop
          - name: netend
        view: network-admin
        state: present

    # Task Output
    # -----------

    # commands:
    # - username netop view network-admin
    # - username netend view network-admin

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password
    # username netop privilege 15 view network-admin password 0 password
    # username netend privilege 15 view network-admin password 0 password

    # Using state: present

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password

    # Present state create a new user with hashed password play:
    # --------------------------------------------------------------

    - name: Create a new user with hashed password
      cisco.ios.ios_user:
        name: ansibletest5
        hashed_password:
          type: 9
          value: "thiswillbereplacedwithhashedpassword"
        state: present

    # Task Output
    # -----------

    # commands:
    # - username ansibletest5 secret 9 thiswillbereplacedwithhashedpassword

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password
    # username ansibletest5 secret 9 thiswillbereplacedwithhashedpassword

    # Using state: absent

    # Before state:
    # -------------

    # router-ios#show running-config | section ^username
    # username admin privilege 15 password 0 password
    # username ansibletest1 password 0 password
    # username ansibletest2 secret 9 thiswillbereplacedwithhashedpassword
    # username ansibletest3 password 5 thistoowillbereplacedwithhashedpassword

    # Absent state remove multiple users play:
    # ----------------------------------------

    - name: Delete users with aggregate
      cisco.ios.ios_user:
        aggregate:
          - name: ansibletest1
          - name: ansibletest2
          - name: ansibletest3
        state: absent

    # Task Output
    # -----------

    # commands:
    # - no username ansibletest1
    # - no username ansibletest2
    # - no username ansibletest3

    # After state:
    # ------------

    # router-ios#show running-config | section username
    # username admin privilege 15 password 0 password



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;username ansible secret password&#x27;, &#x27;username admin secret admin&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
