.. _cisco.ios.ios_acls_module:


******************
cisco.ios.ios_acls
******************

**Resource module to configure ACLs.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the named or numbered ACLs on IOS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="7">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="7">
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
                        <div>A list of ACL configuration options.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>acls</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of Access Control Lists (ACL) attributes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>aces</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The entries within the ACL.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Specify the packet destination.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Host address to match, or any single host address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>any</b>
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
                        <div>Match any source address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A single destination host</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>object_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination network object group</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port_protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the destination port along with protocol.</div>
                        <div>Note, Valid with TCP/UDP protocol_options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets on a given port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a greater port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a lower port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets not on a given port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Port group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>end</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the end of the port range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the start of the port range.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wildcard_bits</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination wildcard bits, valid with IPV4 address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dscp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match packets with given dscp value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enable_fragments</b>
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
                        <div>Enable non-initial fragments.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evaluate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Evaluate an access list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>grant</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>permit</li>
                                    <li>deny</li>
                        </ul>
                </td>
                <td>
                        <div>Specify the action.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>log</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Log matches against this entry.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
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
                        <div>Enable Log matches against this entry</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user_cookie</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>User defined cookie (max of 64 char)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>log_input</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Log matches against this entry, including input interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
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
                        <div>Enable Log matches against this entry, including input interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user_cookie</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>User defined cookie (max of 64 char)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>option</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match packets with given IP Options value.</div>
                        <div>Valid only for named acls.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>add_ext</b>
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
                        <div>Match packets with Address Extension Option (147).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>any_options</b>
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
                        <div>Match packets with ANY Option.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>com_security</b>
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
                        <div>Match packets with Commercial Security Option (134).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dps</b>
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
                        <div>Match packets with Dynamic Packet State Option (151).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encode</b>
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
                        <div>Match packets with Encode Option (15).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eool</b>
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
                        <div>Match packets with End of Options (0).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ext_ip</b>
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
                        <div>Match packets with Extended IP Option (145).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ext_security</b>
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
                        <div>Match packets with Extended Security Option (133).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>finn</b>
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
                        <div>Match packets with Experimental Flow Control Option (205).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>imitd</b>
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
                        <div>Match packets with IMI Traffic Desriptor Option (144).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lsr</b>
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
                        <div>Match packets with Loose Source Route Option (131).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtup</b>
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
                        <div>Match packets with MTU Probe Option (11).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtur</b>
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
                        <div>Match packets with MTU Reply Option (12).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_op</b>
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
                        <div>Match packets with No Operation Option (1).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nsapa</b>
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
                        <div>Match packets with NSAP Addresses Option (150).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>record_route</b>
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
                        <div>Match packets with Record Route Option (7).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_alert</b>
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
                        <div>Match packets with Router Alert Option (148).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sdb</b>
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
                        <div>Match packets with Selective Directed Broadcast Option (149).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>security</b>
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
                        <div>Match packets with Basic Security Option (130).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssr</b>
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
                        <div>Match packets with Strict Source Routing Option (137).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>stream_id</b>
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
                        <div>Match packets with Stream ID Option (136).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timestamp</b>
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
                        <div>Match packets with Time Stamp Option (68).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>traceroute</b>
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
                        <div>Match packets with Trace Route Option (82).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ump</b>
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
                        <div>Match packets with Upstream Multicast Packet Option (152).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>visa</b>
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
                        <div>Match packets with Experimental Access Control Option (142).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>zsu</b>
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
                        <div>Match packets with Experimental Measurement Option (10).</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>precedence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match packets with given precedence value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the protocol to match.</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>protocol type.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ahp</b>
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
                        <div>Authentication Header Protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eigrp</b>
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
                        <div>Cisco&#x27;s EIGRP routing protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>esp</b>
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
                        <div>Encapsulation Security Payload.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gre</b>
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
                        <div>Cisco&#x27;s GRE tunneling.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hbh</b>
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
                        <div>Hop by Hop options header. Valid for IPV6</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>icmp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Internet Control Message Protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>administratively_prohibited</b>
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
                        <div>Administratively prohibited</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>alternate_address</b>
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
                        <div>Alternate address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>conversion_error</b>
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
                        <div>Datagram conversion</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dod_host_prohibited</b>
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
                        <div>Host prohibited</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dod_net_prohibited</b>
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
                        <div>Net prohibited</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
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
                        <div>Echo (ping)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>echo_reply</b>
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
                        <div>Echo reply</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>general_parameter_problem</b>
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
                        <div>Parameter problem</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_isolated</b>
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
                        <div>Host isolated</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_precedence_unreachable</b>
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
                        <div>Host unreachable for precedence</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_redirect</b>
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
                        <div>Host redirect</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_tos_redirect</b>
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
                        <div>Host redirect for TOS</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_tos_unreachable</b>
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
                        <div>Host unreachable for TOS</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_unknown</b>
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
                        <div>Host unknown</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_unreachable</b>
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
                        <div>Host unreachable</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>information_reply</b>
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
                        <div>Information replies</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>information_request</b>
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
                        <div>Information requests</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mask_reply</b>
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
                        <div>Mask replies</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mask_request</b>
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
                        <div>mask_request</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mobile_redirect</b>
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
                        <div>Mobile host redirect</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>net_redirect</b>
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
                        <div>Network redirect</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>net_tos_redirect</b>
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
                        <div>Net redirect for TOS</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>net_tos_unreachable</b>
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
                        <div>Network unreachable for TOS</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>net_unreachable</b>
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
                        <div>Net unreachable</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network_unknown</b>
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
                        <div>Network unknown</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_room_for_option</b>
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
                        <div>Parameter required but no room</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>option_missing</b>
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
                        <div>Parameter required but not present</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>packet_too_big</b>
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
                        <div>Fragmentation needed and DF set</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parameter_problem</b>
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
                        <div>All parameter problems</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port_unreachable</b>
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
                        <div>Port unreachable</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>precedence_unreachable</b>
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
                        <div>Precedence cutoff</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol_unreachable</b>
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
                        <div>Protocol unreachable</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reassembly_timeout</b>
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
                        <div>Reassembly timeout</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redirect</b>
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
                        <div>All redirects</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_advertisement</b>
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
                        <div>Router discovery advertisements</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_solicitation</b>
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
                        <div>Router discovery solicitations</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_quench</b>
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
                        <div>Source quenches</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_route_failed</b>
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
                        <div>Source route failed</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>time_exceeded</b>
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
                        <div>All time exceededs</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timestamp_reply</b>
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
                        <div>Timestamp replies</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timestamp_request</b>
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
                        <div>Timestamp requests</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>traceroute</b>
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
                        <div>Traceroute</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ttl_exceeded</b>
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
                        <div>TTL exceeded</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unreachable</b>
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
                        <div>All unreachables</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igmp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Internet Gateway Message Protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dvmrp</b>
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
                        <div>Distance Vector Multicast Routing Protocol(2)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_query</b>
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
                        <div>IGMP Membership Query(0)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtrace_resp</b>
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
                        <div>Multicast Traceroute Response(7)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtrace_route</b>
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
                        <div>Multicast Traceroute(8)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pim</b>
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
                        <div>Protocol Independent Multicast(3)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trace</b>
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
                        <div>Multicast trace(4)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>v1host_report</b>
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
                        <div>IGMPv1 Membership Report(1)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>v2host_report</b>
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
                        <div>IGMPv2 Membership Report(5)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>v2leave_group</b>
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
                        <div>IGMPv2 Leave Group(6)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>v3host_report</b>
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
                        <div>IGMPv3 Membership Report(9)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
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
                        <div>Any Internet Protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipinip</b>
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
                        <div>IP in IP tunneling.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
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
                        <div>Any IPv6.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nos</b>
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
                        <div>KA9Q NOS compatible IP over IP tunneling.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ospf</b>
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
                        <div>OSPF routing protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pcp</b>
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
                        <div>Payload Compression Protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pim</b>
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
                        <div>Protocol Independent Multicast.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>An IP protocol number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sctp</b>
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
                        <div>Stream Control Transmission Protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tcp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match TCP packet flags</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ack</b>
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
                        <div>Match on the ACK bit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>established</b>
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
                        <div>Match established connections</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fin</b>
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
                        <div>Match on the FIN bit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>psh</b>
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
                        <div>Match on the PSH bit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rst</b>
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
                        <div>Match on the RST bit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>syn</b>
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
                        <div>Match on the SYN bit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>urg</b>
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
                        <div>Match on the URG bit</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>udp</b>
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
                        <div>User Datagram Protocol.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remarks</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The remarks/description of the ACL.</div>
                        <div>The remarks attribute used within an ace with or without a sequence number will produce remarks that are pushed before the ace entry.</div>
                        <div>Remarks entry used as the only key in as the list option will produce non ace specific remarks, these remarks would be pushed at the end of all the aces for an acl.</div>
                        <div>Remarks is treated a block, for every single remarks updated for an ace all the remarks are negated and added back to maintain the order of remarks mentioned.</div>
                        <div>As the appliance deletes all the remarks once the ace is updated, the set of remarks would be re-applied that is an expected behavior.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Sequence Number for the Access Control Entry(ACE).</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the packet source.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source network address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>any</b>
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
                        <div>Match any source address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A single source host</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>object_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source network object group</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port_protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the source port along with protocol.</div>
                        <div>Note, Valid with TCP/UDP protocol_options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets on a given port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a greater port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a lower port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets not on a given port number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Port group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>end</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the end of the port range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the start of the port range.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wildcard_bits</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source wildcard bits, valid with IPV4 address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>time_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify a time-range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tos</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match packets with given TOS value.</div>
                        <div>Note, DSCP and TOS are mutually exclusive</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_reliability</b>
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
                        <div>Match packets with max reliable TOS (2).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_throughput</b>
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
                        <div>Match packets with max throughput TOS (4).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_delay</b>
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
                        <div>Match packets with min delay TOS (8).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_monetary_cost</b>
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
                        <div>Match packets with min monetary cost TOS (1).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>normal</b>
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
                        <div>Match packets with normal TOS (0).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>service_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Type of service value</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ttl</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match packets with given TTL value.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets on a given TTL number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a greater TTL number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets with a lower TTL number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets not on a given TTL number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match only packets in the range of TTLs.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>end</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the end of the port range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the start of the port range.</div>
                </td>
            </tr>



            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>acl_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>extended</li>
                                    <li>standard</li>
                        </ul>
                </td>
                <td>
                        <div>ACL type</div>
                        <div>Note, it&#x27;s mandatory and required for Named ACL, but for Numbered ACL it&#x27;s not mandatory.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>The name or the number of the ACL.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>The Address Family Indicator (AFI) for the Access Control Lists (ACL).</div>
                </td>
            </tr>

            <tr>
                <td colspan="7">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>sh access-list</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="7">
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
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The state <em>merged</em> is the default state which merges the want and have config, but for ACL module as the IOS platform doesn&#x27;t allow update of ACE over an pre-existing ACE sequence in ACL, same way ACLs resource module will error out for respective scenario and only addition of new ACE over new sequence will be allowed with merge state.</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of commands <em>sh running-config | section access-list</em> for all acls related information and <em>sh access-lists | include access list</em> to obtain configuration specific of an empty acls, the following commands are executed on device. Config data from both the commands should be kept together one after another for the parsers to pick the commands correctly. For state <em>parsed</em> active connection to remote host is not required.</div>
                        <div>The state <em>overridden</em>, modify/add the ACLs defined, deleted all other ACLs.</div>
                        <div>The state <em>replaced</em>, modify/add only the ACEs of the ACLs defined only. It does not perform any other change on the device.</div>
                        <div>The state <em>deleted</em>, deletes only the specified ACLs, or all if not specified.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.3 on CML.
   - Module behavior is not idempotent when sequence for aces are not mentioned
   - This module works with connection ``network_cli``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
   - Default ACLs don't get updated, replaced or overridden. Added Defaults - implicit_deny_v6, implicit_permit_v6, preauth_v6, IP-Adm-V4-Int-ACL-global, implicit_deny, implicit_permit, preauth_v4, sl_def_acl



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list extended 110
    #    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: std_acl
                acl_type: standard
                aces:
                  - grant: deny
                    source:
                      address: 192.168.1.200
                  - grant: deny
                    source:
                      address: 192.168.2.0
                      wildcard_bits: 0.0.0.255
              - name: 110
                aces:
                  - sequence: 10
                    protocol_options:
                      icmp:
                        traceroute: true
                    source:
                      address: 192.168.3.0
                      wildcard_bits: 255.255.255.0
                    destination:
                      any: true
                    grant: permit
                  - grant: deny
                    protocol_options:
                      tcp:
                        ack: true
                    source:
                      host: 198.51.100.0
                    destination:
                      host: 198.51.110.0
                      port_protocol:
                        eq: telnet
              - name: extended_acl_1
                acl_type: extended
                aces:
                  - grant: deny
                    protocol_options:
                      tcp:
                        fin: true
                    source:
                      address: 192.0.2.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 192.0.3.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    option:
                      traceroute: true
                    ttl:
                      eq: 10
              - name: 123
                aces:
                  - remarks:
                      - "remarks for extended ACL 1"
                      - "check ACL"
                  - grant: deny
                    protocol_options:
                      tcp:
                        ack: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 198.51.101.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    tos:
                      service_value: 12
                  - grant: deny
                    protocol_options:
                      tcp:
                        ack: true
                    source:
                      address: 192.0.3.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 192.0.4.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    dscp: ef
                    ttl:
                      lt: 20
          - afi: ipv6
            acls:
              - name: R1_TRAFFIC
                aces:
                  - grant: deny
                    protocol_options:
                      tcp:
                        ack: true
                    source:
                      any: true
                      port_protocol:
                        eq: www
                    destination:
                      any: true
                      port_protocol:
                        eq: telnet
                    dscp: af11
        state: merged

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            echo: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: '100'
    #    afi: ipv4
    # commands:
    #  - ip access-list extended 110
    #  - deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    #  - 30 permit icmp 192.168.3.0 255.255.255.0 any traceroute
    #  - ip access-list extended extended_acl_1
    #  - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    #  - ip access-list standard std_acl
    #  - deny 192.168.1.20
    #  - deny 192.168.2.0 0.0.0.255
    #  - ip access-list extended 123
    #  - deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #  - deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    #  - remark remarks for extended ACL 1
    #  - remark check ACL
    #  - ipv6 access-list R1_TRAFFIC
    #  - deny tcp any eq www any eq telnet ack dscp af11
    # after:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            echo: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      - destination:
    #          any: true
    #        grant: permit
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 30
    #        source:
    #          address: 0.0.0.0
    #          wildcard_bits: 255.255.255.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      - remarks:
    #        - remarks for extended ACL 1
    #        - check ACL
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: extended_acl_1
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.20
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    afi: ipv4
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6

    # After state:
    # ------------
    #
    # vios#sh running-config | section access-list
    # ip access-list standard std_acl
    #    10 deny   192.168.1.200
    #    20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 100
    #    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    # ip access-list extended 110
    #    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended test
    #    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ipv6 access-list R1_TRAFFIC
    #    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    # vios#show running-config | include ip(v6)* access-list|remark
    # ip access-list standard std_acl
    # ip access-list extended extended_acl_1
    # ip access-list extended 110
    # ip access-list extended 123
    #  remark remarks for extended ACL 1
    #  remark check ACL
    # ipv6 access-list R1_TRAFFIC

    # Using merged (update existing ACE - will fail)

    # Before state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list extended 100
    #    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: 100
                aces:
                  - sequence: 10
                    protocol_options:
                      icmp:
                        traceroute: true
        state: merged

    # After state:
    # ------------
    #
    # Play Execution fails, with error:
    # Cannot update existing sequence 10 of ACLs 100 with state merged.
    # Please use state replaced or overridden.

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list standard std_acl
    #     10 deny   192.168.1.200
    #     20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended R1_TRAFFIC
    #     10 deny tcp any eq www any eq telnet ack dscp af11
    # ip access-list extended test
    #     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

    - name: Replaces device configuration of listed acls with provided configuration
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: 110
                aces:
                  - grant: deny
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 192.0.2.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 192.0.3.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    dscp: ef
                    ttl:
                      eq: 10
              - name: 150
                aces:
                  - grant: deny
                    sequence: 20
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    destination:
                      address: 198.51.110.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    dscp: ef
                    ttl:
                      eq: 10
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      acl_type: extended
    #      name: R1_TRAFFIC
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4
    # commands:
    #  - ip access-list extended 110
    #  - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #  - no 20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    #  - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
    #  - ip access-list extended 150
    #  - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
    # after:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            syn: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - destination:
    #          address: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            syn: true
    #        sequence: 20
    #        source:
    #          address: 198.51.100.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: '150'
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      acl_type: extended
    #      name: R1_TRAFFIC
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4

    # After state:
    # -------------
    #
    # vios#sh access-lists
    # ip access-list standard std_acl
    #    10 deny   192.168.1.200
    #    20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
    # ip access-list extended 123
    #    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended 150
    #    20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
    # ip access-list extended test
    #    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ipv6 access-list R1_TRAFFIC
    #    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    # Using replaced - example remarks specific

    # Before state:
    # -------------
    #
    # vios#show running-config | section access-list
    # ip access-list extended TEST
    #  10 remark FIRST REMARK BEFORE LINE 10
    #  10 remark ============
    #  10 remark ALLOW HOST FROM TEST 10
    #  10 permit ip host 1.1.1.1 any
    #  20 remark FIRST REMARK BEFORE LINE 20
    #  20 remark ============
    #  20 remark ALLOW HOST remarks AFTER LINE  20
    #  20 permit ip host 2.2.2.2 any
    #  30 remark FIRST REMARK BEFORE LINE 30
    #  30 remark ============
    #  30 remark ALLOW HOST remarks AFTER LINE  30
    #  30 permit ip host 3.3.3.3 any

    - name: Replace remarks of ace with sequence 10
      # check_mode: true
      cisco.ios.ios_acls:
        state: replaced
        config:
          - acls:
              - aces:
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - The new first remarks before 10
                      - ============new
                      - The new second remarks before 10
                    sequence: 10
                    source:
                      host: 1.1.1.1
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - FIRST REMARK BEFORE LINE 20
                      - ============
                      - ALLOW HOST remarks AFTER LINE  20
                    sequence: 20
                    source:
                      host: 2.2.2.2
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - FIRST REMARK BEFORE LINE 30
                      - ============
                      - ALLOW HOST remarks AFTER LINE  30
                    sequence: 30
                    source:
                      host: 3.3.3.3
                acl_type: extended
                name: TEST
            afi: ipv4

    # Task Output
    # -----------
    #
    # before:
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 10
    #       - ===========1=
    #       - ALLOW HOST FROM TEST 10
    #       sequence: 10
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 20
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  20
    #       sequence: 20
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 30
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  30
    #       sequence: 30
    #       source:
    #         host: 3.3.3.3
    #     acl_type: extended
    #     name: TEST
    #   afi: ipv4
    # commands:
    # - ip access-list extended TEST
    # - no 10 remark
    # - 10 remark The new first remarks before 10
    # - 10 remark ============new
    # - 10 remark The new second remarks before 10
    # after:
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - The new first remarks before 10
    #       - ============new
    #       - The new second remarks before 10
    #       sequence: 10
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 20
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  20
    #       sequence: 20
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 30
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  30
    #       sequence: 30
    #       source:
    #         host: 3.3.3.3
    #     acl_type: extended
    #     name: TEST
    #   afi: ipv4

    # After state:
    # -------------
    #
    # foo#show running-config | section access-list
    # ip access-list extended TEST
    #  10 remark The new first remarks before 10
    #  10 remark ============new
    #  10 remark The new second remarks before 10
    #  10 permit ip host 1.1.1.1 any
    #  20 remark FIRST REMARK BEFORE LINE 20
    #  20 remark ============
    #  20 remark ALLOW HOST remarks AFTER LINE  20
    #  20 permit ip host 2.2.2.2 any
    #  30 remark FIRST REMARK BEFORE LINE 30
    #  30 remark ============
    #  30 remark ALLOW HOST remarks AFTER LINE  30
    #  30 permit ip host 3.3.3.3 any

    # Using replaced - example remarks specific on targeted sequence

    # Before state:
    # -------------
    #
    # vios#show running-config | section access-list
    # ip access-list extended TEST
    #  10 permit ip host 1.1.1.1 any
    #  20 remark FIRST REMARK BEFORE LINE 20
    #  20 remark ============
    #  20 remark ALLOW HOST remarks AFTER LINE  20
    #  20 permit ip host 2.2.2.2 any
    #  30 remark FIRST REMARK BEFORE LINE 30
    #  30 remark ============
    #  30 remark ALLOW HOST remarks AFTER LINE  30
    #  30 permit ip host 3.3.3.3 any

    - name: Replace remarks of ace with sequence 10
      # check_mode: true
      cisco.ios.ios_acls:
        state: replaced
        config:
          - acls:
              - aces:
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - The new first remarks before 10
                      - ============new
                      - The new second remarks before 10
                    sequence: 10
                    source:
                      host: 1.1.1.1
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - FIRST REMARK BEFORE LINE 20
                      - ============
                      - ALLOW HOST remarks AFTER LINE  20
                    sequence: 20
                    source:
                      host: 2.2.2.2
                  - destination:
                      any: true
                    grant: permit
                    protocol: ip
                    remarks:
                      - FIRST REMARK BEFORE LINE 30
                      - ============
                      - ALLOW HOST remarks AFTER LINE  30
                    sequence: 30
                    source:
                      host: 3.3.3.3
                acl_type: extended
                name: TEST
            afi: ipv4

    # Task Output
    # -----------
    #
    # before:
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       sequence: 10
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 20
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  20
    #       sequence: 20
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 30
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  30
    #       sequence: 30
    #       source:
    #         host: 3.3.3.3
    #     acl_type: extended
    #     name: TEST
    #   afi: ipv4
    # commands:
    # - ip access-list extended TEST
    # - 10 remark The new first remarks before 10
    # - 10 remark ============new
    # - 10 remark The new second remarks before 10
    # after:
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - The new first remarks before 10
    #       - ============new
    #       - The new second remarks before 10
    #       sequence: 10
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 20
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  20
    #       sequence: 20
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE LINE 30
    #       - ============
    #       - ALLOW HOST remarks AFTER LINE  30
    #       sequence: 30
    #       source:
    #         host: 3.3.3.3
    #     acl_type: extended
    #     name: TEST
    #   afi: ipv4

    # After state:
    # -------------
    #
    # foo#show running-config | section access-list
    # ip access-list extended TEST
    #  10 remark The new first remarks before 10
    #  10 remark ============new
    #  10 remark The new second remarks before 10
    #  10 permit ip host 1.1.1.1 any
    #  20 remark FIRST REMARK BEFORE LINE 20
    #  20 remark ============
    #  20 remark ALLOW HOST remarks AFTER LINE  20
    #  20 permit ip host 2.2.2.2 any
    #  30 remark FIRST REMARK BEFORE LINE 30
    #  30 remark ============
    #  30 remark ALLOW HOST remarks AFTER LINE  30
    #  30 permit ip host 3.3.3.3 any

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#sh access-lists
    # ip access-list standard std_acl
    #     10 deny   192.168.1.200
    #     20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended R1_TRAFFIC
    #     10 deny tcp any eq www any eq telnet ack dscp af11
    # ip access-list extended test
    #     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

    - name: Override device configuration of all acls with provided configuration
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: 110
                aces:
                  - grant: deny
                    sequence: 20
                    protocol_options:
                      tcp:
                        ack: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    destination:
                      address: 198.51.110.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    dscp: ef
                    ttl:
                      eq: 10
              - name: 150
                aces:
                  - grant: deny
                    sequence: 10
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    destination:
                      address: 198.51.110.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    dscp: ef
                    ttl:
                      eq: 10
              - name: implicit_deny
                aces:
                  - grant: deny
                    sequence: 10
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    destination:
                      address: 198.51.110.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    dscp: ef
                    ttl:
                      eq: 10
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      acl_type: extended
    #      name: R1_TRAFFIC
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4
    # commands:
    #  - ip access-list extended 110
    #  - no 20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    #  - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #  - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10
    #  - ip access-list extended 150
    #  - 10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
    #  - no ip access-list extended 123
    #  - no ip access-list extended R1_TRAFFIC
    #  - no ip access-list standard std_acl
    #  - no ip access-list extended test
    # after:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 198.51.110.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 198.51.100.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            syn: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: '150'
    #    afi: ipv4

    # After state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list extended 110
    #     20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10
    # ip access-list extended 150
    #     10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

    # Using overridden - example remarks specific on multiple sequence

    # Before state:
    # -------------
    #
    # vios#show running-config | section access-list
    # ip access-list extended TEST
    #  10 remark FIRST REMARK BEFORE SEQUENCE 10
    #  10 remark ============
    #  10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
    #  20 remark FIRST REMARK BEFORE SEQUENCE 20
    #  20 remark ============
    #  20 remark ALLOW HOST FROM SEQUENCE 20
    #  20 permit ip host 1.1.1.1 any
    #  30 remark FIRST REMARK BEFORE SEQUENCE 30
    #  30 remark ============
    #  30 remark ALLOW HOST FROM SEQUENCE 30
    #  30 permit ip host 2.2.2.2 any
    #  40 remark FIRST REMARK BEFORE SEQUENCE 40
    #  40 remark ============
    #  40 remark ALLOW NEW HOST FROM SEQUENCE 40
    #  40 permit ip host 3.3.3.3 any
    #  remark Remark not specific to sequence
    #  remark ============
    #  remark End Remarks
    # ip access-list extended test_acl
    #  10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ip access-list extended 110
    #  10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    # ip access-list extended 123
    #  10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #  20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ipv6 access-list R1_TRAFFIC
    #  sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    - name: Override remarks and ace configurations
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: TEST
                acl_type: extended
                aces:
                  - sequence: 10
                    remarks:
                      - "FIRST REMARK BEFORE SEQUENCE 10"
                      - "============"
                      - "REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE"
                    grant: permit
                    protocol: ip
                    source:
                      host: 1.1.1.1
                    destination:
                      any: true
                  - sequence: 20
                    remarks:
                      - "FIRST REMARK BEFORE SEQUENCE 20"
                      - "============"
                      - "ALLOW HOST FROM SEQUENCE 20"
                    grant: permit
                    protocol: ip
                    source:
                      host: 192.168.0.1
                    destination:
                      any: true
                  - sequence: 30
                    remarks:
                      - "FIRST REMARK BEFORE SEQUENCE 30"
                      - "============"
                      - "ALLOW HOST FROM SEQUENCE 30 updated"
                    grant: permit
                    protocol: ip
                    source:
                      host: 2.2.2.2
                    destination:
                      any: true
                  - sequence: 40
                    remarks:
                      - "FIRST REMARK BEFORE SEQUENCE 40"
                      - "============"
                      - "ALLOW NEW HOST FROM SEQUENCE 40"
                    grant: permit
                    protocol: ip
                    source:
                      host: 3.3.3.3
                    destination:
                      any: true
                  - remarks:
                      - "Remark not specific to sequence"
                      - "============"
                      - "End Remarks 1"
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    # - acls:
    #   - aces:
    #     - destination:
    #         address: 192.0.3.0
    #         wildcard_bits: 0.0.0.255
    #       dscp: ef
    #       grant: deny
    #       protocol: icmp
    #       protocol_options:
    #         icmp:
    #           echo: true
    #       sequence: 10
    #       source:
    #         address: 192.0.2.0
    #         wildcard_bits: 0.0.0.255
    #       ttl:
    #         eq: 10
    #     acl_type: extended
    #     name: '110'
    #   - aces:
    #     - destination:
    #         address: 198.51.101.0
    #         port_protocol:
    #           eq: telnet
    #         wildcard_bits: 0.0.0.255
    #       grant: deny
    #       protocol: tcp
    #       protocol_options:
    #         tcp:
    #           ack: true
    #       sequence: 10
    #       source:
    #         address: 198.51.100.0
    #         wildcard_bits: 0.0.0.255
    #       tos:
    #         service_value: 12
    #     - destination:
    #         address: 192.0.4.0
    #         port_protocol:
    #           eq: www
    #         wildcard_bits: 0.0.0.255
    #       dscp: ef
    #       grant: deny
    #       protocol: tcp
    #       protocol_options:
    #         tcp:
    #           ack: true
    #       sequence: 20
    #       source:
    #         address: 192.0.3.0
    #         wildcard_bits: 0.0.0.255
    #       ttl:
    #         lt: 20
    #     acl_type: extended
    #     name: '123'
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 20
    #       - ============
    #       - ALLOW HOST FROM SEQUENCE 20
    #       sequence: 20
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 30
    #       - ============
    #       - ALLOW HOST FROM SEQUENCE 30
    #       sequence: 30
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 40
    #       - ============
    #       - ALLOW NEW HOST FROM SEQUENCE 40
    #       sequence: 40
    #       source:
    #         host: 3.3.3.3
    #     - remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 10
    #       - ============
    #       - REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
    #       sequence: 10
    #     - remarks:
    #       - Remark not specific to sequence
    #       - ============
    #       - End Remarks
    #     acl_type: extended
    #     name: TEST
    #   - aces:
    #     - destination:
    #         address: 192.0.3.0
    #         port_protocol:
    #           eq: www
    #         wildcard_bits: 0.0.0.255
    #       grant: deny
    #       option:
    #         traceroute: true
    #       protocol: tcp
    #       protocol_options:
    #         tcp:
    #           fin: true
    #       sequence: 10
    #       source:
    #         address: 192.0.2.0
    #         wildcard_bits: 0.0.0.255
    #       ttl:
    #         eq: 10
    #     acl_type: extended
    #     name: test_acl
    #   afi: ipv4
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #         port_protocol:
    #           eq: telnet
    #       dscp: af11
    #       grant: deny
    #       protocol: tcp
    #       protocol_options:
    #         tcp:
    #           ack: true
    #       sequence: 10
    #       source:
    #         any: true
    #         port_protocol:
    #           eq: www
    #     name: R1_TRAFFIC
    #   afi: ipv6
    # commands:
    # - no ipv6 access-list R1_TRAFFIC
    # - ip access-list extended TEST
    # - no 10  # removes all remarks and ace entry for sequence 10
    # - no 20 permit ip host 1.1.1.1 any  # removing the ace automatically removes the remarks
    # - no 30 remark  # just remove remarks for sequence 30
    # - no remark  # remove all remarks at end of acl, that has no sequence
    # - 10 remark FIRST REMARK BEFORE SEQUENCE 10
    # - 10 remark ============
    # - 10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
    # - 10 permit ip host 1.1.1.1 any
    # - 20 remark FIRST REMARK BEFORE SEQUENCE 20
    # - 20 remark ============
    # - 20 remark ALLOW HOST FROM SEQUENCE 20
    # - 20 permit ip host 192.168.0.1 any
    # - 30 remark FIRST REMARK BEFORE SEQUENCE 30
    # - 30 remark ============
    # - 30 remark ALLOW HOST FROM SEQUENCE 30 updated
    # - remark Remark not specific to sequence
    # - remark ============
    # - remark End Remarks 1
    # - no ip access-list extended 110
    # - no ip access-list extended 123
    # - no ip access-list extended test_acl
    # after:
    # - acls:
    #   - aces:
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 10
    #       - ============
    #       - REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
    #       sequence: 10
    #       source:
    #         host: 1.1.1.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 20
    #       - ============
    #       - ALLOW HOST FROM SEQUENCE 20
    #       sequence: 20
    #       source:
    #         host: 192.168.0.1
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 30
    #       - ============
    #       - ALLOW HOST FROM SEQUENCE 30 updated
    #       sequence: 30
    #       source:
    #         host: 2.2.2.2
    #     - destination:
    #         any: true
    #       grant: permit
    #       protocol: ip
    #       remarks:
    #       - FIRST REMARK BEFORE SEQUENCE 40
    #       - ============
    #       - ALLOW NEW HOST FROM SEQUENCE 40
    #       sequence: 40
    #       source:
    #         host: 3.3.3.3
    #     - remarks:
    #       - Remark not specific to sequence
    #       - ============
    #       - End Remarks 1
    #     acl_type: extended
    #     name: TEST
    #   afi: ipv4

    # After state:
    # -------------
    #
    # foo#show running-config | section access-list
    # ip access-list extended TEST
    #  10 remark FIRST REMARK BEFORE SEQUENCE 10
    #  10 remark ============
    #  10 remark REMARKS FOR SEQUENCE 10 NO FOLLOWING ACE
    #  10 permit ip host 1.1.1.1 any
    #  20 remark FIRST REMARK BEFORE SEQUENCE 20
    #  20 remark ============
    #  20 remark ALLOW HOST FROM SEQUENCE 20
    #  20 permit ip host 192.168.0.1 any
    #  30 remark FIRST REMARK BEFORE SEQUENCE 30
    #  30 remark ============
    #  30 remark ALLOW HOST FROM SEQUENCE 30 updated
    #  30 permit ip host 2.2.2.2 any
    #  40 remark FIRST REMARK BEFORE SEQUENCE 40
    #  40 remark ============
    #  40 remark ALLOW NEW HOST FROM SEQUENCE 40
    #  40 permit ip host 3.3.3.3 any
    #  remark Remark not specific to sequence
    #  remark ============
    #  remark End Remarks 1

    # Using deleted - delete ACL(s)

    # Before state:
    # -------------
    #
    # vios#sh access-lists
    # ip access-list standard std_acl
    #     10 deny   192.168.1.200
    #     20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended extended_acl_1
    #     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10

    - name: "Delete ACLs (Note: This won't delete the all configured ACLs)"
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: extended_acl_1
                acl_type: extended
              - name: 110
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: extended_acl_1
    #    afi: ipv4
    # commands:
    #  - no ip access-list extended 110
    #  - no ip access-list extended extended_acl_1
    # after:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    afi: ipv4

    # After state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list standard std_acl
    #    10 deny   192.168.1.200
    #    20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 123
    #    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20

    # Using deleted - delete ACLs based on AFI

    # Before state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ip access-list standard std_acl
    #     10 deny   192.168.1.200
    #     20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended test
    #     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ipv6 access-list R1_TRAFFIC
    #     sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    - name: "Delete ACLs based on AFI (Note: This won't delete the all configured ACLs)"
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6
    # commands:
    #  - no ip access-list extended 110
    #  - no ip access-list extended 123
    #  - no ip access-list standard std_acl
    #  - no ip access-list extended test
    # after:
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6

    # After state:
    # -------------
    #
    # vios#sh running-config | section access-list
    # ipv6 access-list R1_TRAFFIC
    #    sequence 10 deny tcp any eq www any eq telnet ack dscp af11


    # Using deleted - delete all ACLs

    # Before state:
    # -------------
    #
    # vios#sh access-lists
    # ip access-list standard std_acl
    #     10 deny   192.168.1.200
    #     20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #     10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #     20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #     10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #     20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended test
    #     10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ipv6 access-list R1_TRAFFIC
    #     sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    - name: Delete ALL of configured ACLs
      cisco.ios.ios_acls:
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6
    # commands:
    #  - no ip access-list extended test
    #  - no ip access-list extended 110
    #  - no ip access-list extended 123
    #  - no ip access-list extended test
    #  - no ipv6 access-list R1_TRAFFIC
    # after: []

    # After state:
    # -------------
    #
    # vios#sh running-config | section access-list


    # Using gathered

    # Before state:
    # -------------
    #
    # vios#sh access-lists
    # ip access-list standard std_acl
    #    10 deny   192.168.1.200
    #    20 deny   192.168.2.0 0.0.0.255
    # ip access-list extended 110
    #    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
    # ip access-list extended 123
    #    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
    #    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
    # ip access-list extended test
    #    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
    # ipv6 access-list R1_TRAFFIC
    #    sequence 10 deny tcp any eq www any eq telnet ack dscp af11

    - name: Gather ACLs configuration from target device
      cisco.ios.ios_acls:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # before:
    #  - acls:
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: icmp
    #        protocol_options:
    #          icmp:
    #            traceroute: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      - destination:
    #          host: 198.51.110.0
    #          port_protocol:
    #            eq: telnet
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          host: 198.51.100.0
    #      acl_type: extended
    #      name: '110'
    #    - aces:
    #      - destination:
    #          address: 198.51.101.0
    #          port_protocol:
    #            eq: telnet
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          address: 198.51.100.0
    #          wildcard_bits: 0.0.0.255
    #        tos:
    #          service_value: 12
    #      - destination:
    #          address: 192.0.4.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        dscp: ef
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 20
    #        source:
    #          address: 192.0.3.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          lt: 20
    #      acl_type: extended
    #      name: '123'
    #    - aces:
    #      - grant: deny
    #        sequence: 10
    #        source:
    #          host: 192.168.1.200
    #      - grant: deny
    #        sequence: 20
    #        source:
    #          address: 192.168.2.0
    #          wildcard_bits: 0.0.0.255
    #      acl_type: standard
    #      name: std_acl
    #    - aces:
    #      - destination:
    #          address: 192.0.3.0
    #          port_protocol:
    #            eq: www
    #          wildcard_bits: 0.0.0.255
    #        grant: deny
    #        option:
    #          traceroute: true
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            fin: true
    #        sequence: 10
    #        source:
    #          address: 192.0.2.0
    #          wildcard_bits: 0.0.0.255
    #        ttl:
    #          eq: 10
    #      acl_type: extended
    #      name: test
    #    afi: ipv4
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6

    # Using rendered

    - name: Render the provided configuration into platform specific configuration lines
      cisco.ios.ios_acls:
        config:
          - afi: ipv4
            acls:
              - name: 110
                aces:
                  - grant: deny
                    sequence: 10
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 192.0.2.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 192.0.3.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    dscp: ef
                    ttl:
                      eq: 10
              - name: 150
                aces:
                  - grant: deny
                    protocol_options:
                      tcp:
                        syn: true
                    source:
                      address: 198.51.100.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    destination:
                      address: 198.51.110.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: telnet
                    dscp: ef
                    ttl:
                      eq: 10
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # rendered:
    #  - ip access-list extended 110
    #  - 10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
    #  - ip access-list extended 150
    #  - deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # IPv6 access-list R1_TRAFFIC
    # deny tcp any eq www any eq telnet ack dscp af11

    - name: Parse the commands for provided configuration
      cisco.ios.ios_acls:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # parsed:
    #  - acls:
    #    - aces:
    #      - destination:
    #          any: true
    #          port_protocol:
    #            eq: telnet
    #        dscp: af11
    #        grant: deny
    #        protocol: tcp
    #        protocol_options:
    #          tcp:
    #            ack: true
    #        sequence: 10
    #        source:
    #          any: true
    #          port_protocol:
    #            eq: www
    #      name: R1_TRAFFIC
    #    afi: ipv6



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip access-list extended 110&#x27;, &#x27;deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10&#x27;, &#x27;permit ip host 2.2.2.2 host 3.3.3.3&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip access-list extended test&#x27;, &#x27;permit ip host 2.2.2.2 host 3.3.3.3&#x27;, &#x27;permit tcp host 1.1.1.1 host 5.5.5.5 eq www&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
- Sagar Paul (@KB-perByte)
