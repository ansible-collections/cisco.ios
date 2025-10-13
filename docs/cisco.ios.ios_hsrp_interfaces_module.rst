.. _cisco.ios.ios_hsrp_interfaces_module:


*****************************
cisco.ios.ios_hsrp_interfaces
*****************************

**Resource module to configure HSRP on interfaces.**


Version added: 10.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of HSRP configuration on interface for Cisco IOS devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="5">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="5">
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
                        <div>A list of HSP configuration options to add to interface</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Enable HSRP BFD</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>HSRP initialization delay</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minimum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay at least this long</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reload</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay after reload</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_refresh</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Refresh MAC cache on switch by periodically sending packet from virtual mac address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redirect</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redirect configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertisement</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redirect advertisement messages (standby redirect advertisement authentication md5)</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set encryption 0 (unencrypted/default) or 7 (hidden)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_chain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key chain</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_string</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password_text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password text valid for plain text and and key-string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>time_out</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set timeout</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Adjust redirect timers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>adv_timer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Passive router advertisement interval in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>holddown_timer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Passive router holddown interval in seconds</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>standby_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group number and group options for standby (HSRP)</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: standby_groups</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set encryption 0 (unencrypted/default) or 7 (hidden)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_chain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key chain</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_string</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password_text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password text valid for plain text and and key-string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>time_out</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set timeout</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>follow</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable HSRP BFD</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redundancy name string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_no</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable HSRP IPv4 and set the virtual IP address</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secondary</b>
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
                        <div>Make this IP address a secondary virtual IP address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>virtual_ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual IP address</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable HSRP IPv6 and set the IP address</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>addresses</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 link-local address or IPv6 prefix</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>autoconfig</b>
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
                        <div>Obtain address using autoconfiguration</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual MAC address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>preempt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Overthrow lower priority Active routers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delay</b>
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
                        <div>Wait before preempting</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enables preempt, drives the lone `standby &lt;grp_no&gt; preempt` command</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minimum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay at least this long</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reload</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay after reload</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sync</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Wait for IP redundancy clients</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>priority</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">100</div>
                </td>
                <td>
                        <div>Priority level</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Overthrow lower priority Active routers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hello_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hello interval in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hold_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hold time in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>msec</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify hello interval in milliseconds</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hello_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>&lt;15-999&gt;  Hello interval in milliseconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hold_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>&lt;60-3000&gt;  Hold time in milliseconds</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority tracking</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>decrement</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority decrement</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>shutdown</b>
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
                        <div>Shutdown Group</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track_no</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Track object number</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_bia</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>HSRP uses interface&#x27;s burned in address (does not work with mac address)</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scope</b>
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
                        <div>Use-bia applies to all groups on this interface or sub-interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
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
                        <div>Set use-bia</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>1</li>
                                    <li>2</li>
                        </ul>
                </td>
                <td>
                        <div>HSRP version</div>
                </td>
            </tr>

            <tr>
                <td colspan="5">
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
                <td colspan="5">
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
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^interface</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.16.
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - The module examples uses callback plugin (callback_result_format=yaml) to generate task output in yaml format.
   - For idempotency, the module consieders that version defaults to 1 as it is implied by the applaince and not available in the running-config. Priority defaults to 100 if not specified in the configuration.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # Router#show running-config | section ^interface
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address


    - name: Populate the device with HSRP interface configuration
      cisco.ios.hsrp_interfaces:
        state: merged
        config:
          - delay:
              minimum: 5555
              reload: 556
            mac_refresh: 45
            name: Vlan70
            redirect:
              advertisement:
                authentication:
                  key_chain: HSRP_CHAIN
              timers:
                adv_timer: 10
                holddown_timer: 55
            standby_options:
              - authentication:
                  encryption: 7
                  key_string: 0123456789ABCDEF
                follow: MASTER_GROUP
                group_name: PRIMARY_GROUP
                group_no: 10
                ip:
                  - secondary: true
                    virtual_ip: 10.0.10.2
                preempt:
                  delay: true
                  enabled: true
                  minimum: 100
                  reload: 50
                  sync: 30
                priority: 110
                timers:
                  hold_time: 250
                  msec:
                    hello_interval: 200
                track:
                  - decrement: 20
                    track_no: 1
              - follow: MASTER_GROUP
                group_name: IPV6_GROUP
                group_no: 20
                ipv6:
                  addresses:
                    - '2001:db8:20::1/64'
                  autoconfig: true
                mac_address: 0000.0000.0014
                priority: 120
            version: 2
          - delay:
              minimum: 100
              reload: 200
            name: Vlan100
            standby_options:
              - authentication:
                  password_text: hello_secret
                group_name: BACKUP_GROUP
                group_no: 5
                ip:
                  - virtual_ip: 192.168.1.1
                preempt:
                  enabled: true
                priority: 150
                timers:
                  hello_interval: 5
                  hold_time: 15
                track:
                  - decrement: 30
                    track_no: 10
            version: 2
          - name: GigabitEthernet3
            standby_options:
              - group_no: 1
                ip:
                  - virtual_ip: 172.16.1.1
                priority: 100
            version: 1
          - name: GigabitEthernet2
            standby_options:
              - authentication:
                  key_chain: AUTH_CHAIN
                group_no: 2
                ip:
                  - secondary: true
                    virtual_ip: 172.16.2.1
                priority: 100
            version: 1


    # Task Output
    # -----------
    #
    # before:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    # -   name: GigabitEthernet3
    # -   name: GigabitEthernet4
    # -   name: Vlan70
    # -   name: Vlan100
    # commands:
    # - interface Vlan70
    # - standby version 2
    # - standby delay minimum 5555 reload 556
    # - standby mac-refresh 45
    # - standby redirect timers 10 55
    # - standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    # - standby 10 follow MASTER_GROUP
    # - standby 10 name PRIMARY_GROUP
    # - standby 10 preempt delay minimum 100 reload 50 sync 30
    # - standby 10 priority 110
    # - standby 10 authentication md5 key-string 7 0123456789ABCDEF
    # - standby 10 ip 10.0.10.2 secondary
    # - standby 10 track 1 decrement 20
    # - standby 20 follow MASTER_GROUP
    # - standby 20 mac-address 0000.0000.0014
    # - standby 20 name IPV6_GROUP
    # - standby 20 priority 120
    # - standby 20 ipv6 autoconfig
    # - standby 20 ipv6 2001:db8:20::1/64
    # - interface Vlan100
    # - standby version 2
    # - standby delay minimum 100 reload 200
    # - standby 5 name BACKUP_GROUP
    # - standby 5 preempt
    # - standby 5 priority 150
    # - standby 5 authentication ********
    # - standby 5 ip 192.168.1.1
    # - standby 5 track 10 decrement 30
    # - interface GigabitEthernet3
    # - standby version 1
    # - standby 1 priority 100
    # - standby 1 ip 172.16.1.1
    # - interface GigabitEthernet2
    # - standby version 1
    # - standby 2 priority 100
    # - standby 2 authentication md5 key-chain AUTH_CHAIN
    # - standby 2 ip 172.16.2.1 secondary
    # after:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    #     standby_options:
    #     -   authentication:
    #             key_chain: AUTH_CHAIN
    #         group_no: 2
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 172.16.2.1
    #         priority: 100
    # -   name: GigabitEthernet3
    #     standby_options:
    #     -   group_no: 1
    #         ip:
    #         -   virtual_ip: 172.16.1.1
    #         priority: 100
    # -   name: GigabitEthernet4
    # -   delay:
    #         minimum: 5555
    #         reload: 556
    #     mac_refresh: 45
    #     name: Vlan70
    #     redirect:
    #         advertisement:
    #             authentication:
    #                 key_chain: HSRP_CHAIN
    #         timers:
    #             adv_timer: 10
    #             holddown_timer: 55
    #     standby_options:
    #     -   authentication:
    #             encryption: 7
    #             key_string: 0123456789ABCDEF
    #         follow: MASTER_GROUP
    #         group_name: PRIMARY_GROUP
    #         group_no: 10
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 10.0.10.2
    #         preempt:
    #             delay: true
    #             enabled: true
    #             minimum: 100
    #             reload: 50
    #             sync: 30
    #         priority: 110
    #         track:
    #         -   decrement: 20
    #             track_no: 1
    #     -   follow: MASTER_GROUP
    #         group_name: IPV6_GROUP
    #         group_no: 20
    #         ipv6:
    #             addresses:
    #             - 2001:DB8:20::1/64
    #             autoconfig: true
    #         mac_address: 0000.0000.0014
    #         priority: 120
    #     version: 2
    # -   delay:
    #         minimum: 100
    #         reload: 200
    #     name: Vlan100
    #     standby_options:
    #     -   group_name: BACKUP_GROUP
    #         group_no: 5
    #         ip:
    #         -   virtual_ip: 192.168.1.1
    #         preempt:
    #             enabled: true
    #         priority: 150
    #         track:
    #         -   decrement: 30
    #             track_no: 10
    #     version: 2

    # After state:
    # ------------
    #
    # Router#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # !
    # interface GigabitEthernet2
    #  no ip address
    #  standby 2 ip 172.16.2.1 secondary
    #  standby 2 authentication md5 key-chain AUTH_CHAIN
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet3
    #  no ip address
    #  standby 1 ip 172.16.1.1
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface Vlan70
    #  description for test
    #  no ip address
    #  standby mac-refresh 45
    #  standby redirect timers 10 55
    #  standby delay minimum 5555 reload 556
    #  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    #  standby version 2
    #  standby 10 ip 10.0.10.2 secondary
    #  standby 10 follow MASTER_GROUP
    #  standby 10 priority 110
    #  standby 10 preempt delay minimum 100 reload 50 sync 30
    #  standby 10 authentication md5 key-string 7 0123456789ABCDEF
    #  standby 10 name PRIMARY_GROUP
    #  standby 10 track 1 decrement 20
    #  standby 20 ipv6 autoconfig
    #  standby 20 ipv6 2001:DB8:20::1/64
    #  standby 20 follow MASTER_GROUP
    #  standby 20 priority 120
    #  standby 20 name IPV6_GROUP
    #  standby 20 mac-address 0000.0000.0014
    # !
    # interface Vlan100
    #  description for test
    #  no ip address
    #  standby delay minimum 100 reload 200
    #  standby version 2
    #  standby 5 ip 192.168.1.1
    #  standby 5 priority 150
    #  standby 5 preempt
    #  standby 5 name BACKUP_GROUP
    #  standby 5 track 10 decrement 30
    # !


    # Using replaced

    # Before state:
    # -------------
    #
    # Router#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  speed 1000
    #  standby 22 ip 10.0.0.1 secondary
    #  no negotiation auto
    # interface GigabitEthernet4
    #  no ip address
    #  standby 0 priority 5
    #  shutdown
    #  negotiation auto

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.ios.ios_hsrp_interfaces:
        config:
          - name: GigabitEthernet3
            standby_groups:
              - group_no: 22
                ip:
                  - virtual_ip: 10.0.0.1
                    secondary: true
          - name: GigabitEthernet4
            standby_groups:
              - group_no: 0
                priority: 6
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    # - name: GigabitEthernet1
    # - name: GigabitEthernet2
    # - name: GigabitEthernet3
    #     standby_groups:
    #       - group_no: 22
    #         ip:
    #           - virtual_ip: 192.168.0.2
    #             secondary: True
    # - name: GigabitEthernet4
    #     standby_groups:
    #       - group_no: 0
    #         priority: 6
    # - name: Loopback999
    # - name: Loopback888
    # commands:
    # - interface GigabitEthernet3
    # - standby 22 ip 10.0.0.1 secondary
    # - interface GigabitEthernet4
    # - standby 0 priority 5
    # after:
    #   name: GigabitEthernet1
    #   name: GigabitEthernet2
    #   name: GigabitEthernet3
    #     standby_groups:
    #       - group_no: 22
    #         ip:
    #           - virtual_ip: 192.168.0.2
    #             secondary: True
    # - name: GigabitEthernet4
    #     standby_groups:
    #       - group_no: 0
    #         priority: 6
    # - name: Loopback999
    # - name: Loopback888

    # After state:
    # ------------
    #
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  standby 22 ip 10.0.0.1 secondary
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  description Auto_Cable_Testing_Ansible
    #  no ip address
    #  standby 0 priority 6
    #  shutdown
    #  negotiation auto

    # Using overridden

    # Before state:
    # -------------
    #
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  standby 22 ip 10.0.0.1 secondary
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  description Auto_Cable_Testing_Ansible
    #  no ip address
    #  standby 0 priority 6
    #  shutdown
    #  negotiation auto

    - name: Override device configuration of all interfaces with provided configuration
      cisco.ios.ios_hsrp_interfaces:
        config:
          - name: GigabitEthernet4
            standby_groups:
              - group_no: 0
                priority: 10
        state: overridden

    # Task Output
    # -----------
    # before:
    # - name: GigabitEthernet1
    # - name: GigabitEthernet2
    # - name: GigabitEthernet3
    #     standby_groups:
    #       - group_no: 22
    #         ip:
    #           - virtual_ip: 192.168.0.2
    #             secondary: True
    # - name: GigabitEthernet4
    #     standby_groups:
    #       - group_no: 0
    #         priority: 6
    # - name: Loopback999
    # - name: Loopback888
    # commands:
    # - interface GigabitEthernet3
    # - no standby 22 ip 10.0.0.1 secondary
    # - interface GigabitEthernet4
    # - no standby 0 priority 6
    # - standby 0 priority 10
    # after:
    # - name: GigabitEthernet1
    # - name: GigabitEthernet2
    # - name: GigabitEthernet3
    # - name: GigabitEthernet4
    #     standby_groups:
    #       - group_no: 0
    #         priority: 10
    # - name: Loopback999
    # - name: Loopback888

    # After state:
    # ------------
    #
    # router-ios#show running-config | section ^interface
    # interface Loopback888
    #  no ip address
    # interface Loopback999
    #  no ip address
    # interface GigabitEthernet1
    #  description Management interface do not change
    #  ip address dhcp
    #  negotiation auto
    # interface GigabitEthernet2
    #  no ip address
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet3
    #  no ip address
    #  speed 1000
    #  no negotiation auto
    # interface GigabitEthernet4
    #  description Auto_Cable_Testing_Ansible
    #  no ip address
    #  standby 0 priority 10
    #  shutdown
    #  negotiation auto

    # Using deleted

    # Before state:
    # -------------
    #
    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # !
    # interface GigabitEthernet2
    #  no ip address
    #  standby 2 ip 172.16.2.1 secondary
    #  standby 2 authentication md5 key-chain AUTH_CHAIN
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet3
    #  no ip address
    #  standby 1 ip 172.16.1.1
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface Vlan70
    #  description for test
    #  no ip address
    #  standby mac-refresh 45
    #  standby redirect timers 10 55
    #  standby delay minimum 5555 reload 556
    #  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    #  standby version 2
    #  standby 10 ip 10.0.10.2 secondary
    #  standby 10 follow MASTER_GROUP
    #  standby 10 priority 110
    #  standby 10 preempt delay minimum 100 reload 50 sync 30
    #  standby 10 authentication md5 key-string 7 0123456789ABCDEF
    #  standby 10 name PRIMARY_GROUP
    #  standby 10 track 1 decrement 20
    #  standby 20 ipv6 autoconfig
    #  standby 20 ipv6 2001:DB8:20::1/64
    #  standby 20 follow MASTER_GROUP
    #  standby 20 priority 120
    #  standby 20 name IPV6_GROUP
    #  standby 20 mac-address 0000.0000.0014
    # !
    # interface Vlan100
    #  description for test
    #  no ip address
    #  standby delay minimum 100 reload 200
    #  standby version 2
    #  standby 5 ip 192.168.1.1
    #  standby 5 priority 150
    #  standby 5 preempt
    #  standby 5 name BACKUP_GROUP
    #  standby 5 track 10 decrement 30


    - name: "Delete attributes of given interfaces (NOTE: This won't delete the interfaces)"
      cisco.ios.ios_hsrp_interfaces:
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    #     standby_options:
    #     -   authentication:
    #             key_chain: AUTH_CHAIN
    #         group_no: 2
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 172.16.2.1
    #         priority: 100
    # -   name: GigabitEthernet3
    #     standby_options:
    #     -   group_no: 1
    #         ip:
    #         -   virtual_ip: 172.16.1.1
    #         priority: 100
    # -   name: GigabitEthernet4
    # -   delay:
    #         minimum: 5555
    #         reload: 556
    #     mac_refresh: 45
    #     name: Vlan70
    #     redirect:
    #         advertisement:
    #             authentication:
    #                 key_chain: HSRP_CHAIN
    #         timers:
    #             adv_timer: 10
    #             holddown_timer: 55
    #     standby_options:
    #     -   authentication:
    #             encryption: 7
    #             key_string: 0123456789ABCDEF
    #         follow: MASTER_GROUP
    #         group_name: PRIMARY_GROUP
    #         group_no: 10
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 10.0.10.2
    #         preempt:
    #             delay: true
    #             enabled: true
    #             minimum: 100
    #             reload: 50
    #             sync: 30
    #         priority: 110
    #         track:
    #         -   decrement: 20
    #             track_no: 1
    #     -   follow: MASTER_GROUP
    #         group_name: IPV6_GROUP
    #         group_no: 20
    #         ipv6:
    #             addresses:
    #             - 2001:DB8:20::1/64
    #             autoconfig: true
    #         mac_address: 0000.0000.0014
    #         priority: 120
    #     version: 2
    # -   delay:
    #         minimum: 100
    #         reload: 200
    #     name: Vlan100
    #     standby_options:
    #     -   group_name: BACKUP_GROUP
    #         group_no: 5
    #         ip:
    #         -   virtual_ip: 192.168.1.1
    #         preempt:
    #             enabled: true
    #         priority: 150
    #         track:
    #         -   decrement: 30
    #             track_no: 10
    #     version: 2
    # commands:
    # - interface GigabitEthernet2
    # - no standby version 1
    # - no standby 2
    # - interface GigabitEthernet3
    # - no standby version 1
    # - no standby 1
    # - interface Vlan70
    # - no standby version 2
    # - no standby delay minimum 5555 reload 556
    # - no standby mac-refresh 45
    # - no standby redirect timers 10 55
    # - no standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    # - no standby 10
    # - no standby 20
    # - no standby version 2
    # - interface Vlan100
    # - no standby version 2
    # - no standby delay minimum 100 reload 200
    # - no standby 5
    # - no standby version 2
    # after:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    # -   name: GigabitEthernet3
    # -   name: GigabitEthernet4
    # -   name: Vlan70
    # -   name: Vlan100

    # After state:
    # -------------
    #
    # router-ios#show running-config | section ^interface
    # !
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # !
    # interface GigabitEthernet2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet3
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface Vlan70
    #  description for test
    #  no ip address
    # !
    # interface Vlan100
    #  description for test
    #  no ip address
    # !

    # Using gathered

    # Before state:
    # -------------
    # router-ios#show running-config | section ^interface
    # interface GigabitEthernet1
    #  ip address dhcp
    #  negotiation auto
    # !
    # interface GigabitEthernet2
    #  no ip address
    #  standby 2 ip 172.16.2.1 secondary
    #  standby 2 authentication md5 key-chain AUTH_CHAIN
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet3
    #  no ip address
    #  standby 1 ip 172.16.1.1
    #  shutdown
    #  negotiation auto
    # !
    # interface GigabitEthernet4
    #  no ip address
    #  shutdown
    #  negotiation auto
    # !
    # interface Vlan70
    #  description for test
    #  no ip address
    #  standby mac-refresh 45
    #  standby redirect timers 10 55
    #  standby delay minimum 5555 reload 556
    #  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    #  standby version 2
    #  standby 10 ip 10.0.10.2 secondary
    #  standby 10 follow MASTER_GROUP
    #  standby 10 priority 110
    #  standby 10 preempt delay minimum 100 reload 50 sync 30
    #  standby 10 authentication md5 key-string 7 0123456789ABCDEF
    #  standby 10 name PRIMARY_GROUP
    #  standby 10 track 1 decrement 20
    #  standby 20 ipv6 autoconfig
    #  standby 20 ipv6 2001:DB8:20::1/64
    #  standby 20 follow MASTER_GROUP
    #  standby 20 priority 120
    #  standby 20 name IPV6_GROUP
    #  standby 20 mac-address 0000.0000.0014
    # !
    # interface Vlan100
    #  description for test
    #  no ip address
    #  standby delay minimum 100 reload 200
    #  standby version 2
    #  standby 5 ip 192.168.1.1
    #  standby 5 priority 150
    #  standby 5 preempt
    #  standby 5 name BACKUP_GROUP
    #  standby 5 track 10 decrement 30

    - name: Gather facts for hsrp interfaces
      cisco.ios.ios_hsrp_interfaces:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    # -   name: GigabitEthernet1
    # -   name: GigabitEthernet2
    #     standby_options:
    #     -   authentication:
    #             key_chain: AUTH_CHAIN
    #         group_no: 2
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 172.16.2.1
    #         priority: 100
    # -   name: GigabitEthernet3
    #     standby_options:
    #     -   group_no: 1
    #         ip:
    #         -   virtual_ip: 172.16.1.1
    #         priority: 100
    # -   name: GigabitEthernet4
    # -   delay:
    #         minimum: 5555
    #         reload: 556
    #     mac_refresh: 45
    #     name: Vlan70
    #     redirect:
    #         advertisement:
    #             authentication:
    #                 key_chain: HSRP_CHAIN
    #         timers:
    #             adv_timer: 10
    #             holddown_timer: 55
    #     standby_options:
    #     -   authentication:
    #             encryption: 7
    #             key_string: 0123456789ABCDEF
    #         follow: MASTER_GROUP
    #         group_name: PRIMARY_GROUP
    #         group_no: 10
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 10.0.10.2
    #         preempt:
    #             delay: true
    #             enabled: true
    #             minimum: 100
    #             reload: 50
    #             sync: 30
    #         priority: 110
    #         track:
    #         -   decrement: 20
    #             track_no: 1
    #     -   follow: MASTER_GROUP
    #         group_name: IPV6_GROUP
    #         group_no: 20
    #         ipv6:
    #             addresses:
    #             - 2001:DB8:20::1/64
    #             autoconfig: true
    #         mac_address: 0000.0000.0014
    #         priority: 120
    #     version: 2
    # -   delay:
    #         minimum: 100
    #         reload: 200
    #     name: Vlan100
    #     standby_options:
    #     -   group_name: BACKUP_GROUP
    #         group_no: 5
    #         ip:
    #         -   virtual_ip: 192.168.1.1
    #         preempt:
    #             enabled: true
    #         priority: 150
    #         track:
    #         -   decrement: 30
    #             track_no: 10
    #     version: 2

    # Using rendered

    - name: Render the commands for provided configuration
      cisco.ios.ios_hsrp_interfaces:
        config:
          - delay:
              minimum: 5555
              reload: 556
            mac_refresh: 45
            name: Vlan70
            redirect:
              advertisement:
                authentication:
                  key_chain: HSRP_CHAIN
              timers:
                adv_timer: 10
                holddown_timer: 55
            standby_options:
              - authentication:
                  encryption: 7
                  key_string: 0123456789ABCDEF
                follow: MASTER_GROUP
                group_name: PRIMARY_GROUP
                group_no: 10
                ip:
                  - virtual_ip: 10.0.10.1
                  - secondary: true
                    virtual_ip: 10.0.10.2
                  - secondary: true
                    virtual_ip: 10.0.10.3
                mac_address: 0000.0c07.ac0a
                preempt:
                  delay: true
                  enabled: true
                  minimum: 100
                  reload: 50
                  sync: 30
                priority: 110
                timers:
                  hold_time: 250
                  msec:
                    hello_interval: 200
                track:
                  - decrement: 20
                    track_no: 1
                  - shutdown: true
                    track_no: 2
              - follow: MASTER_GROUP
                group_name: IPV6_GROUP
                group_no: 20
                ipv6:
                  addresses:
                    - 2001:db8:10::1/64
                    - 2001:db8:20::1/64
                  autoconfig: true
                mac_address: 0000.0c07.ac14
                priority: 120
            version: 2
          - delay:
              minimum: 100
              reload: 200
            name: Vlan100
            standby_options:
              - authentication:
                  password_text: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
                group_name: BACKUP_GROUP
                group_no: 5
                ip:
                  - virtual_ip: 192.168.1.1
                preempt:
                  enabled: true
                priority: 150
                timers:
                  hello_interval: 5
                  hold_time: 15
                track:
                  - decrement: 30
                    track_no: 10
            version: 2
          - name: GigabitEthernet3
            standby_options:
              - group_no: 1
                ip:
                  - virtual_ip: 172.16.1.1
                priority: 100
            use_bia:
              set: true
          - name: GigabitEthernet2
            standby_options:
              - authentication:
                  key_chain: AUTH_CHAIN
                group_no: 2
                ip:
                  - secondary: true
                    virtual_ip: 172.16.2.1
                priority: 100
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    # - interface Vlan70
    # - standby version 2
    # - standby delay minimum 5555 reload 556
    # - standby mac-refresh 45
    # - standby redirect timers 10 55
    # - standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    # - standby 10 follow MASTER_GROUP
    # - standby 10 mac-address 0000.0c07.ac0a
    # - standby 10 name PRIMARY_GROUP
    # - standby 10 preempt delay minimum 100 reload 50 sync 30
    # - standby 10 priority 110
    # - standby 10 authentication md5 key-string 7 0123456789ABCDEF
    # - standby 10 ip 10.0.10.1
    # - standby 10 ip 10.0.10.2 secondary
    # - standby 10 ip 10.0.10.3 secondary
    # - standby 10 track 1 decrement 20
    # - standby 10 track 2 shutdown
    # - standby 20 follow MASTER_GROUP
    # - standby 20 mac-address 0000.0c07.ac14
    # - standby 20 name IPV6_GROUP
    # - standby 20 priority 120
    # - standby 20 ipv6 autoconfig
    # - standby 20 ipv6 2001:db8:10::1/64
    # - standby 20 ipv6 2001:db8:20::1/64
    # - interface Vlan100
    # - standby version 2
    # - standby delay minimum 100 reload 200
    # - standby 5 name BACKUP_GROUP
    # - standby 5 preempt
    # - standby 5 priority 150
    # - standby 5 authentication ********
    # - standby 5 ip 192.168.1.1
    # - standby 5 track 10 decrement 30
    # - interface GigabitEthernet3
    # - standby version 1
    # - standby use-bia scope interface
    # - standby 1 priority 100
    # - standby 1 ip 172.16.1.1
    # - interface GigabitEthernet2
    # - standby version 1
    # - standby 2 priority 100
    # - standby 2 authentication md5 key-chain AUTH_CHAIN
    # - standby 2 ip 172.16.2.1 secondary

    # Using parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface Vlan70
    #  no ip address
    #  standby mac-refresh 45
    #  standby redirect timers 10 55
    #  standby delay minimum 5555 reload 556
    #  standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
    #  standby version 2
    #  standby 10 ip 10.0.10.1
    #  standby 10 ip 10.0.10.2 secondary
    #  standby 10 ip 10.0.10.3 secondary
    #  standby 10 follow MASTER_GROUP
    #  standby 10 timers msec 200 250
    #  standby 10 priority 110
    #  standby 10 preempt delay minimum 100 reload 50 sync 30
    #  standby 10 authentication md5 key-string 7 0123456789ABCDEF
    #  standby 10 name PRIMARY_GROUP
    #  standby 10 mac-address 0000.0c07.ac0a
    #  standby 10 track 1 decrement 20
    #  standby 10 track 2 shutdown
    #  standby 20 ipv6 2001:db8:10::1/64
    #  standby 20 ipv6 2001:db8:20::1/64
    #  standby 20 ipv6 autoconfig
    #  standby 20 follow MASTER_GROUP
    #  standby 20 priority 120
    #  standby 20 name IPV6_GROUP
    #  standby 20 mac-address 0000.0c07.ac14

    # interface Vlan100
    #  no ip address
    #  standby bfd
    #  standby delay minimum 100 reload 200
    #  standby version 2
    #  standby 5 ip 192.168.1.1
    #  standby 5 timers 5 15
    #  standby 5 priority 150
    #  standby 5 preempt
    #  standby 5 authentication hello_secret
    #  standby 5 name BACKUP_GROUP
    #  standby 5 track 10 decrement 30

    # interface GigabitEthernet3
    #  standby use-bia
    #  standby 1 ip 172.16.1.1
    #  standby 1 priority 100

    # interface GigabitEthernet2
    #  standby follow VLAN70_GROUP
    #  standby 2 ip 172.16.2.1 secondary
    #  standby 2 authentication md5 key-chain AUTH_CHAIN

    # - name: Parse the provided configuration
    #   cisco.ios.ios_hsrp_interfaces:
    #     running_config: "{{ lookup('file', 'parsed.cfg') }}"
    #     state: parsed

    # Task Output
    # -----------
    #
    # parsed:
    # -   delay:
    #         minimum: 5555
    #         reload: 556
    #     mac_refresh: 45
    #     name: Vlan70
    #     redirect:
    #         advertisement:
    #             authentication:
    #                 key_chain: HSRP_CHAIN
    #         timers:
    #             adv_timer: 10
    #             holddown_timer: 55
    #     standby_options:
    #     -   authentication:
    #             encryption: 7
    #             key_string: 0123456789ABCDEF
    #         follow: MASTER_GROUP
    #         group_name: PRIMARY_GROUP
    #         group_no: 10
    #         ip:
    #         -   virtual_ip: 10.0.10.1
    #         -   secondary: true
    #             virtual_ip: 10.0.10.2
    #         -   secondary: true
    #             virtual_ip: 10.0.10.3
    #         mac_address: 0000.0c07.ac0a
    #         preempt:
    #             delay: true
    #             enabled: true
    #             minimum: 100
    #             reload: 50
    #             sync: 30
    #         priority: 110
    #         timers:
    #             hold_time: 250
    #             msec:
    #                 hello_interval: 200
    #         track:
    #         -   decrement: 20
    #             track_no: 1
    #         -   shutdown: true
    #             track_no: 2
    #     -   follow: MASTER_GROUP
    #         group_name: IPV6_GROUP
    #         group_no: 20
    #         ipv6:
    #             addresses:
    #             - 2001:db8:10::1/64
    #             - 2001:db8:20::1/64
    #             autoconfig: true
    #         mac_address: 0000.0c07.ac14
    #         priority: 120
    #     version: 2
    # -   delay:
    #         minimum: 100
    #         reload: 200
    #     name: Vlan100
    #     standby_options:
    #     -   authentication:
    #             password_text: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
    #         group_name: BACKUP_GROUP
    #         group_no: 5
    #         ip:
    #         -   virtual_ip: 192.168.1.1
    #         preempt:
    #             enabled: true
    #         priority: 150
    #         timers:
    #             hello_interval: 5
    #             hold_time: 15
    #         track:
    #         -   decrement: 30
    #             track_no: 10
    #     version: 2
    # -   name: GigabitEthernet3
    #     standby_options:
    #     -   group_no: 1
    #         ip:
    #         -   virtual_ip: 172.16.1.1
    #         priority: 100
    #     use_bia:
    #         set: true
    # -   name: GigabitEthernet2
    #     standby_options:
    #     -   authentication:
    #             key_chain: AUTH_CHAIN
    #         group_no: 2
    #         ip:
    #         -   secondary: true
    #             virtual_ip: 172.16.2.1
    #         priority: 100



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;standby 22 ip 10.0.0.1 secondary&#x27;, &#x27;standby 0 priority 5&#x27;, &#x27;standby mac-refresh 21&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;standby 22 ip 10.0.0.1 secondary&#x27;, &#x27;standby 0 priority 5&#x27;, &#x27;standby mac-refresh 21&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
- Nikhil Bhasin (@nickbhasin)
