.. _cisco.ios.ios_pki_trustpoints_module:


*****************************
cisco.ios.ios_pki_trustpoints
*****************************

**Resource module to configure PKI trustpoints.**


Version added: 11.8.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the attributes of PKI trustpoints on Cisco IOS.




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
                        <div>A list of trustpoints.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_certificate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The certificate of the CA, PEM. It is installed with <code>crypto pki authenticate</code> when the trustpoint does not hold it yet.</div>
                        <div>Needs <em>enrollment.type=terminal</em> and a <em>fingerprint</em> that matches the certificate, SHA-1 or MD5.</div>
                        <div>It is never removed or replaced by this module, a trustpoint that holds another certificate of a CA is an error, remove the trustpoint first with state <em>deleted</em>.</div>
                        <div>It is returned by the state <em>gathered</em> as it is in the configuration of the device.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delete_certificates</b>
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
                        <div>Allow state <em>deleted</em> to remove the trustpoint although it holds a CA certificate, it is refused otherwise. Default <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enrollment</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>How the certificate of the CA is obtained (<code>enrollment</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pem</b>
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
                        <div>Use PEM boundaries in the certificate requests (<code>enrollment terminal pem</code>).</div>
                        <div>Only with <em>type=terminal</em>, IOS XE 17.12 and 17.18 refuse <code>pem</code> after a url.</div>
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
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>terminal</li>
                                    <li>selfsigned</li>
                                    <li>pkcs12</li>
                                    <li>url</li>
                        </ul>
                </td>
                <td>
                        <div>The method, <code>terminal</code> for a certificate that is pasted, as with <em>ca_certificate</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URL of the CA, required when <em>type=url</em>.</div>
                        <div>IOS resolves a host name when the command is entered, it must resolve on the device. An IP address always works.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fingerprint</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Fingerprint of the certificate of the CA, hexadecimal. Colons and spaces are ignored (<code>fingerprint</code>).</div>
                        <div>IOS refuses to authenticate a CA certificate unless the trustpoint pins its fingerprint, it is required with <em>ca_certificate</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hash</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>sha1</li>
                                    <li>sha256</li>
                                    <li>sha384</li>
                                    <li>sha512</li>
                        </ul>
                </td>
                <td>
                        <div>Hash algorithm of the certificate requests and of the self-signed certificate (<code>hash</code>).</div>
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
                        <div>Name of the trustpoint.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>revocation_check</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>crl</li>
                                    <li>ocsp</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>Methods used to check the revocation of a certificate, in the order they are tried (<code>revocation-check</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rsakeypair</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The RSA key pair of the trustpoint (<code>rsakeypair</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_label</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the key pair.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Size of the key pair, when the key pair is generated.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>subject_alt_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Subject alternative name of the certificate of the device (<code>subject-alt-name</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>subject_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Subject name of the certificate of the device (<code>subject-name</code>).</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain</b>.</div>
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
                                    <li>deleted</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>With state <em>merged</em>, the provided options are added to the trustpoints named in the task. Nothing is removed.</div>
                        <div>With state <em>replaced</em>, the trustpoints named in the task are made to match, the options that can be removed and that are not in the task are removed.</div>
                        <div>With state <em>deleted</em>, the trustpoints named in the task are removed. A trustpoint that holds a CA certificate is only removed with <em>delete_certificates</em>, nothing is removed when one of them is refused. <em>config</em> is required.</div>
                        <div>With state <em>gathered</em>, the configuration is read from the device and returned in <em>gathered</em>.</div>
                        <div>With state <em>rendered</em>, the task configuration is returned as device commands in <em>rendered</em> without connecting to the device.</div>
                        <div>With state <em>parsed</em>, <em>running_config</em> is returned as structured data in <em>parsed</em>.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - Only the trustpoints named in the task are touched, the others (for example ``SLA-TrustPoint`` and the self-signed trustpoint of the web server) are left alone in every state.
   - Options of a trustpoint that are not listed here are not changed. ``enrollment``, ``revocation_check`` and ``hash`` always have a value on IOS, they are changed when they are in the task and never removed.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # router#show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain
    # router#

    - name: Add the root CA of the company to the trust store
      cisco.ios.ios_pki_trustpoints:
        config:
          - name: COMPANY-ROOT-CA
            enrollment:
              type: terminal
            revocation_check:
              - none
            fingerprint: 68028C590C6CC086A62DE7D04032477D2AA6CBC2
            ca_certificate: "{{ lookup('ansible.builtin.file', 'company-root-ca.pem') }}"
        state: merged

    # Task Output
    # -----------
    #
    # commands:
    #   - crypto pki trustpoint COMPANY-ROOT-CA
    #   - enrollment terminal
    #   - revocation-check none
    #   - fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2
    #   - crypto pki authenticate COMPANY-ROOT-CA

    # After state:
    # ------------
    #
    # router#show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain
    # crypto pki trustpoint COMPANY-ROOT-CA
    #  enrollment terminal
    #  fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2
    #  revocation-check none
    # crypto pki certificate chain COMPANY-ROOT-CA
    #  certificate ca 266FFBF2E589795D91003E4AD0B100DFF4C78563
    #   30820306 308201EE A0030201 02021426 6FFBF2E5 89795D91 003E4AD0 B100DFF4
    #   ...
    #         quit

    # Using replaced

    # Before state:
    # -------------
    #
    # crypto pki trustpoint WEB-CERT
    #  enrollment terminal
    #  subject-name CN=router.example.com
    #  revocation-check none
    #  rsakeypair web-key

    - name: Replace the options of a trustpoint
      cisco.ios.ios_pki_trustpoints:
        config:
          - name: WEB-CERT
            enrollment:
              type: terminal
            revocation_check:
              - crl
              - none
            rsakeypair:
              key_label: web-key
        state: replaced

    # Task Output
    # -----------
    #
    # commands:
    #   - crypto pki trustpoint WEB-CERT
    #   - revocation-check crl none
    #   - no subject-name CN=router.example.com

    # Using deleted

    - name: Remove a trustpoint and the CA certificate it holds
      cisco.ios.ios_pki_trustpoints:
        config:
          - name: COMPANY-ROOT-CA
            delete_certificates: true
        state: deleted

    # Task Output
    # -----------
    #
    # commands:
    #   - no crypto pki trustpoint COMPANY-ROOT-CA

    # Using gathered

    - name: Gather the trustpoints
      cisco.ios.ios_pki_trustpoints:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    #   - name: COMPANY-ROOT-CA
    #     enrollment:
    #       type: terminal
    #     revocation_check:
    #       - none
    #     fingerprint: 68028C590C6CC086A62DE7D04032477D2AA6CBC2
    #     ca_certificate: |
    #       -----BEGIN CERTIFICATE-----
    #       MIIDCjCCAfKgAwIBAgIU...
    #       -----END CERTIFICATE-----

    # Using rendered

    - name: Render the commands of a trustpoint
      cisco.ios.ios_pki_trustpoints:
        config:
          - name: WEB-CERT
            enrollment:
              type: selfsigned
            hash: sha256
            subject_name: CN=router.example.com
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    #   - crypto pki trustpoint WEB-CERT
    #   - enrollment selfsigned
    #   - hash sha256
    #   - subject-name CN=router.example.com

    # Using parsed

    - name: Parse the trustpoints
      cisco.ios.ios_pki_trustpoints:
        running_config: |
          crypto pki trustpoint WEB-CERT
           enrollment terminal
           revocation-check crl none
           hash sha256
        state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    #   - name: WEB-CERT
    #     enrollment:
    #       type: terminal
    #     revocation_check:
    #       - crl
    #       - none
    #     hash: sha256



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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code> or <code>deleted</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code> or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                            <div><code>crypto pki authenticate</code> is not a configuration command, it is run after the configuration is applied.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;crypto pki trustpoint COMPANY-ROOT-CA&#x27;, &#x27;enrollment terminal&#x27;, &#x27;fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2&#x27;, &#x27;crypto pki authenticate COMPANY-ROOT-CA&#x27;]</div>
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
                            <div>The provided configuration in the task rendered in device native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;crypto pki trustpoint WEB-CERT&#x27;, &#x27;enrollment selfsigned&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørgen Spange (@jorgenspange)
