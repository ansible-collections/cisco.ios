.. _cisco.ios.ios_ntp_global_module:


************************
cisco.ios.ios_ntp_global
************************

**Resource module to configure NTP.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of ntp on Cisco IOS devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary of ntp options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Control NTP access</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide full access</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name or number of access list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
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
                        <div>ipv4 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>ipv6 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>kod</b>
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
                        <div>Send a Kiss-o-Death packet for failing peers</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Allow only control queries</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name or number of access list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
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
                        <div>ipv4 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>ipv6 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>kod</b>
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
                        <div>Send a Kiss-o-Death packet for failing peers</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serve</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide server and query access</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name or number of access list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
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
                        <div>ipv4 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>ipv6 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>kod</b>
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
                        <div>Send a Kiss-o-Death packet for failing peers</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serve_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide only server access</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name or number of access list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
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
                        <div>ipv4 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>ipv6 access lists (Default not idempotent)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>kod</b>
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
                        <div>Send a Kiss-o-Death packet for failing peers</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Allow processing of packets</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>control</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Allow processing control mode packets</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rate_limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Rate-limit delay.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private</b>
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
                        <div>Allow processing private mode packets</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authenticate</b>
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
                        <div>Authenticate time sources</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key for trusted time sources</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>algorithm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication type</div>
                </td>
            </tr>
            <tr>
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
                        <div>Authentication key encryption type</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Key number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>broadcast_delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Estimated round-trip delay</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>clock_period</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Length of hardware clock tick, clock period in 2^-32 seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>logging</b>
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
                        <div>Enable NTP message logging</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>master</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Act as NTP master clock</div>
                </td>
            </tr>
                                <tr>
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
                        <div>Enable master clock</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>stratum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Stratum number</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_associations</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set maximum number of associations</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum Distance for synchronization</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min_distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum distance to consider for clockhop</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>orphan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Threshold Stratum for orphan mode</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>panic_update</b>
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
                        <div>Reject time updates &gt; panic threshold (default 1000Sec)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive</b>
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
                        <div>NTP passive mode</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure NTP peer</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>burst</b>
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
                        <div>Send a burst when peer is reachable (Default)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>iburst</b>
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
                        <div>Send a burst when peer is unreachable (Default)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure peer authentication key</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: key</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maxpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum poll interval Poll value in Log2</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum poll interval Poll value in Log2</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>normal_sync</b>
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
                        <div>Disable rapid sync at startup</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ipv4/ipv6 address or hostname of the peer</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefer</b>
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
                        <div>Prefer this peer when possible</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface for source address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_ipv4</b>
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
                        <div>Use IP for DNS resolution</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_ipv6</b>
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
                        <div>Use IPv6 for DNS resolution</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure NTP version</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VPN Routing/Forwarding Information</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>servers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure NTP server</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>burst</b>
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
                        <div>Send a burst when peer is reachable (Default)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>iburst</b>
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
                        <div>Send a burst when peer is unreachable (Default)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure peer authentication key</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: key</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maxpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum poll interval Poll value in Log2</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum poll interval Poll value in Log2</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>normal_sync</b>
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
                        <div>Disable rapid sync at startup</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefer</b>
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
                        <div>Prefer this peer when possible</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ipv4/ipv6 address or hostname of the server</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface for source address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_ipv4</b>
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
                        <div>Use IP for DNS resolution</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_ipv6</b>
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
                        <div>Use IPv6 for DNS resolution</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure NTP version</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VPN Routing/Forwarding Information</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure interface for source address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trusted_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Key numbers for trusted time sources</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range_end</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>End key number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range_start</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Start / key number</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>update_calendar</b>
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
                        <div>Periodically update calendar with NTP time</div>
                </td>
            </tr>

            <tr>
                <td colspan="4">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^ntp</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
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
                        <div>The states <em>replaced</em> and <em>overridden</em> have identical behaviour for this module.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^ntp</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSXE Version 17.3 on CML.
   - This module works with connection ``network_cli``.



Examples
--------

.. code-block:: yaml

    # Using state: merged

    # Before state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # --------------------- EMPTY -----------------

    # Merged play:
    # ------------

    - name: Apply the provided configuration
      cisco.ios.ios_ntp_global:
        config:
          access_group:
            peer:
              - access_list: DHCP-Server
                ipv4: true
                kod: true
              - access_list: preauth_ipv6_acl
                ipv6: true
                kod: true
              - access_list: "2"
                kod: true
            query_only:
              - access_list: "10"
          allow:
            control:
              rate_limit: 4
            private: true
          authenticate: true
          authentication_keys:
            - algorithm: md5
              encryption: 22
              id: 2
              key: SomeSecurePassword
          broadcast_delay: 22
          clock_period: 5
          logging: true
          master:
            stratum: 4
          max_associations: 34
          max_distance: 3
          min_distance: 10
          orphan: 4
          panic_update: true
          peers:
            - peer: 172.16.1.10
              version: 2
            - key: 2
              minpoll: 5
              peer: 172.16.1.11
              prefer: true
              version: 2
            - peer: checkPeerDomainIpv4.com
              prefer: true
              use_ipv4: true
            - peer: checkPeerDomainIpv6.com
              use_ipv6: true
            - peer: testPeerDomainIpv6.com
              prefer: true
              use_ipv6: true
          servers:
            - server: 172.16.1.12
              version: 2
            - server: checkServerDomainIpv6.com
              use_ipv6: true
            - server: 172.16.1.13
              source: GigabitEthernet0/1
          source: GigabitEthernet0/1
          trusted_keys:
            - range_end: 3
              range_start: 3
            - range_start: 21
        state: merged

    # Commands Fired:
    # ---------------

    # "commands": [
    #     "ntp allow mode control 4",
    #     "ntp allow mode private",
    #     "ntp authenticate",
    #     "ntp broadcastdelay 22",
    #     "ntp clock-period 5",
    #     "ntp logging",
    #     "ntp master 4",
    #     "ntp max-associations 34",
    #     "ntp maxdistance 3",
    #     "ntp mindistance 10",
    #     "ntp orphan 4",
    #     "ntp panic update",
    #     "ntp source GigabitEthernet0/1",
    #     "ntp access-group ipv4 peer DHCP-Server kod",
    #     "ntp access-group ipv6 peer preauth_ipv6_acl kod",
    #     "ntp access-group peer 2 kod",
    #     "ntp access-group query-only 10",
    #     "ntp authentication-key 2 md5 SomeSecurePassword 22",
    #     "ntp peer 172.16.1.10 version 2",
    #     "ntp peer 172.16.1.11 key 2 minpoll 5 prefer  version 2",
    #     "ntp peer ip checkPeerDomainIpv4.com prefer",
    #     "ntp peer ipv6 checkPeerDomainIpv6.com",
    #     "ntp peer ipv6 testPeerDomainIpv6.com prefer",
    #     "ntp server 172.16.1.12 version 2",
    #     "ntp server ipv6 checkServerDomainIpv6.com",
    #     "ntp server 172.16.1.13 source GigabitEthernet0/1",
    #     "ntp trusted-key 3 - 3",
    #     "ntp trusted-key 21"
    # ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^ntp
    # ntp max-associations 34
    # ntp logging
    # ntp allow mode control 4
    # ntp panic update
    # ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
    # ntp authenticate
    # ntp trusted-key 3 - 3
    # ntp trusted-key 21
    # ntp orphan 4
    # ntp mindistance 10
    # ntp maxdistance 3
    # ntp broadcastdelay 22
    # ntp source GigabitEthernet0/1
    # ntp access-group peer 2 kod
    # ntp access-group ipv6 peer preauth_ipv6_acl kod
    # ntp master 4
    # ntp peer 172.16.1.10 version 2
    # ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
    # ntp server 172.16.1.12 version 2
    # ntp server 172.16.1.13 source GigabitEthernet0/1
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp peer ipv6 checkPeerDomainIpv6.com
    # ntp peer ipv6 testPeerDomainIpv6.com prefer
    # ntp server ipv6 checkServerDomainIpv6.com

    # Using state: deleted

    # Before state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # ntp max-associations 34
    # ntp logging
    # ntp allow mode control 4
    # ntp panic update
    # ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
    # ntp authenticate
    # ntp trusted-key 3 - 3
    # ntp trusted-key 21
    # ntp orphan 4
    # ntp mindistance 10
    # ntp maxdistance 3
    # ntp broadcastdelay 22
    # ntp source GigabitEthernet0/1
    # ntp access-group peer 2 kod
    # ntp access-group ipv6 peer preauth_ipv6_acl kod
    # ntp master 4
    # ntp peer 172.16.1.10 version 2
    # ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
    # ntp server 172.16.1.12 version 2
    # ntp server 172.16.1.13 source GigabitEthernet0/1
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp peer ipv6 checkPeerDomainIpv6.com
    # ntp peer ipv6 testPeerDomainIpv6.com prefer
    # ntp server ipv6 checkServerDomainIpv6.com

    # Deleted play:
    # -------------

    - name: Remove all existing configuration
      cisco.ios.ios_ntp_global:
        state: deleted

    # Commands Fired:
    # ---------------

    # "commands": [
    #     "no ntp allow mode control 4",
    #     "no ntp authenticate",
    #     "no ntp broadcastdelay 22",
    #     "no ntp logging",
    #     "no ntp master 4",
    #     "no ntp max-associations 34",
    #     "no ntp maxdistance 3",
    #     "no ntp mindistance 10",
    #     "no ntp orphan 4",
    #     "no ntp panic update",
    #     "no ntp source GigabitEthernet0/1",
    #     "no ntp access-group peer 2 kod",
    #     "no ntp access-group ipv6 peer preauth_ipv6_acl kod",
    #     "no ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7",
    #     "no ntp peer 172.16.1.10 version 2",
    #     "no ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
    #     "no ntp peer ip checkPeerDomainIpv4.com prefer",
    #     "no ntp peer ipv6 checkPeerDomainIpv6.com",
    #     "no ntp peer ipv6 testPeerDomainIpv6.com prefer",
    #     "no ntp server 172.16.1.12 version 2",
    #     "no ntp server 172.16.1.13 source GigabitEthernet0/1",
    #     "no ntp server ipv6 checkServerDomainIpv6.com",
    #     "no ntp trusted-key 21",
    #     "no ntp trusted-key 3 - 3"
    # ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^ntp
    # --------------------- EMPTY -----------------

    # Using state: overridden

    # Before state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # ntp panic update
    # ntp authentication-key 2 md5 00371C0B01680E051A33497E080A16001D1908 7
    # ntp authenticate
    # ntp trusted-key 3 - 4
    # ntp trusted-key 21
    # ntp source GigabitEthernet0/1
    # ntp peer 172.16.1.10 version 2
    # ntp server 172.16.1.12 version 2
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp server ipv6 checkServerDomainIpv6.com

    # Overridden play:
    # ----------------

    - name: Override commands with provided configuration
      cisco.ios.ios_ntp_global:
        config:
          peers:
            - peer: ipv6DomainNew.com
              use_ipv6: true
            - peer: 172.16.1.100
              prefer: true
              use_ipv4: true
          access_group:
            peer:
              - access_list: DHCP-Server
                ipv6: true
        state: overridden

    # Commands Fired:
    # ---------------
    # "commands": [
    #       "no ntp authenticate",
    #       "no ntp panic update",
    #       "no ntp source GigabitEthernet0/1",
    #       "ntp access-group ipv6 peer DHCP-Server",
    #       "no ntp authentication-key 2 md5 00371C0B01680E051A33497E080A16001D1908 7",
    #       "ntp peer ipv6 ipv6DomainNew.com",
    #       "ntp peer 172.16.1.100 prefer",
    #       "no ntp peer 172.16.1.10 version 2",
    #       "no ntp peer ip checkPeerDomainIpv4.com prefer",
    #       "no ntp server 172.16.1.12 version 2",
    #       "no ntp server ipv6 checkServerDomainIpv6.com",
    #       "no ntp trusted-key 21",
    #       "no ntp trusted-key 3 - 4"
    #     ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^ntp
    # ntp access-group ipv6 peer DHCP-Server
    # ntp peer ipv6 ipv6DomainNew.com
    # ntp peer 172.16.1.100 prefer

    # Using state: replaced

    # Before state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # ntp access-group ipv6 peer DHCP-Server
    # ntp peer ipv6 ipv6DomainNew.com
    # ntp peer 172.16.1.100 prefer

    # Replaced play:
    # --------------

    - name: Replace commands with provided configuration
      cisco.ios.ios_ntp_global:
        config:
          broadcast_delay: 22
          clock_period: 5
          logging: true
          master:
            stratum: 4
          max_associations: 34
          max_distance: 3
          min_distance: 10
          orphan: 4
        state: replaced

    # Commands Fired:
    # ---------------

    # "commands": [
    #        "ntp broadcastdelay 22",
    #        "ntp clock-period 5",
    #        "ntp logging",
    #        "ntp master 4",
    #        "ntp max-associations 34",
    #        "ntp maxdistance 3",
    #        "ntp mindistance 10",
    #        "ntp orphan 4",
    #        "no ntp access-group ipv6 peer DHCP-Server",
    #        "no ntp peer 172.16.1.100 prefer",
    #        "no ntp peer ipv6 ipv6DomainNew.com"
    #     ],

    # After state:
    # ------------

    # router-ios#show running-config | section ^ntp
    # ntp max-associations 34
    # ntp logging
    # ntp orphan 4
    # ntp mindistance 10
    # ntp maxdistance 3
    # ntp broadcastdelay 22
    # ntp master 4

    # Using state: gathered

    # Before state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # ntp max-associations 34
    # ntp logging
    # ntp allow mode control 4
    # ntp panic update
    # ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
    # ntp authenticate
    # ntp trusted-key 3 - 3
    # ntp trusted-key 21
    # ntp orphan 4
    # ntp mindistance 10
    # ntp maxdistance 3
    # ntp broadcastdelay 22
    # ntp source GigabitEthernet0/1
    # ntp access-group peer 2 kod
    # ntp access-group ipv6 peer preauth_ipv6_acl kod
    # ntp master 4
    # ntp update-calendar
    # ntp peer 172.16.1.10 version 2
    # ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
    # ntp server 172.16.1.12 version 2
    # ntp server 172.16.1.13 source GigabitEthernet0/1
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp peer ipv6 checkPeerDomainIpv6.com
    # ntp peer ipv6 testPeerDomainIpv6.com prefer
    # ntp server ipv6 checkServerDomainIpv6.com

    # Gathered play:
    # --------------

    - name: Gather listed ntp config
      cisco.ios.ios_ntp_global:
        state: gathered

    # Module Execution Result:
    # ------------------------

    # "gathered": {
    #   "access_group": {
    #       "peer": [
    #           {
    #               "access_list": "2",
    #               "kod": true
    #           },
    #           {
    #               "access_list": "preauth_ipv6_acl",
    #               "ipv6": true,
    #               "kod": true
    #           }
    #       ]
    #   },
    #   "allow": {
    #       "control": {
    #           "rate_limit": 4
    #       }
    #   },
    #   "authenticate": true,
    #   "authentication_keys": [
    #       {
    #           "algorithm": "md5",
    #           "encryption": 7,
    #           "id": 2,
    #           "key": "0635002C497D0C1A1005173B0D17393C2B3A37"
    #       }
    #   ],
    #   "broadcast_delay": 22,
    #   "logging": true,
    #   "master": {
    #       "stratum": 4
    #   },
    #   "max_associations": 34,
    #   "max_distance": 3,
    #   "min_distance": 10,
    #   "orphan": 4,
    #   "panic_update": true,
    #   "peers": [
    #       {
    #           "peer": "172.16.1.10",
    #           "version": 2
    #       },
    #       {
    #           "key": 2,
    #           "minpoll": 5,
    #           "peer": "172.16.1.11",
    #           "prefer": true,
    #           "version": 2
    #       },
    #       {
    #           "peer": "checkPeerDomainIpv4.com",
    #           "prefer": true,
    #           "use_ipv4": true
    #       },
    #       {
    #           "peer": "checkPeerDomainIpv6.com",
    #           "use_ipv6": true
    #       },
    #       {
    #           "peer": "testPeerDomainIpv6.com",
    #           "prefer": true,
    #           "use_ipv6": true
    #       }
    #   ],
    #   "servers": [
    #       {
    #           "server": "172.16.1.12",
    #           "version": 2
    #       },
    #       {
    #           "server": "172.16.1.13",
    #           "source": "GigabitEthernet0/1"
    #       },
    #       {
    #           "server": "checkServerDomainIpv6.com",
    #           "use_ipv6": true
    #       }
    #   ],
    #   "source": "GigabitEthernet0/1",
    #   "trusted_keys": [
    #       {
    #           "range_start": 21
    #       },
    #       {
    #           "range_end": 3,
    #           "range_start": 3
    #       }
    #   ],
    #   "update_calendar": true
    # },

    # After state:
    # -------------

    # router-ios#show running-config | section ^ntp
    # ntp max-associations 34
    # ntp logging
    # ntp allow mode control 4
    # ntp panic update
    # ntp authentication-key 2 md5 0635002C497D0C1A1005173B0D17393C2B3A37 7
    # ntp authenticate
    # ntp trusted-key 3 - 3
    # ntp trusted-key 21
    # ntp orphan 4
    # ntp mindistance 10
    # ntp maxdistance 3
    # ntp broadcastdelay 22
    # ntp source GigabitEthernet0/1
    # ntp access-group peer 2 kod
    # ntp access-group ipv6 peer preauth_ipv6_acl kod
    # ntp master 4
    # ntp update-calendar
    # ntp peer 172.16.1.10 version 2
    # ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
    # ntp server 172.16.1.12 version 2
    # ntp server 172.16.1.13 source GigabitEthernet0/1
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp peer ipv6 checkPeerDomainIpv6.com
    # ntp peer ipv6 testPeerDomainIpv6.com prefer
    # ntp server ipv6 checkServerDomainIpv6.com

    # Using state: rendered

    # Rendered play:
    # --------------

    - name: Render the commands for provided configuration
      cisco.ios.ios_ntp_global:
        config:
          access_group:
            peer:
              - access_list: DHCP-Server
                ipv4: true
                kod: true
              - access_list: preauth_ipv6_acl
                ipv6: true
                kod: true
              - access_list: "2"
                kod: true
            query_only:
              - access_list: "10"
          allow:
            control:
              rate_limit: 4
            private: true
          authenticate: true
          authentication_keys:
            - algorithm: md5
              encryption: 22
              id: 2
              key: SomeSecurePassword
          broadcast_delay: 22
          clock_period: 5
          logging: true
          master:
            stratum: 4
          max_associations: 34
          max_distance: 3
          min_distance: 10
          orphan: 4
          panic_update: true
          peers:
            - peer: 172.16.1.10
              version: 2
            - key: 2
              minpoll: 5
              peer: 172.16.1.11
              prefer: true
              version: 2
            - peer: checkPeerDomainIpv4.com
              prefer: true
              use_ipv4: true
            - peer: checkPeerDomainIpv6.com
              use_ipv6: true
            - peer: testPeerDomainIpv6.com
              prefer: true
              use_ipv6: true
          servers:
            - server: 172.16.1.12
              version: 2
            - server: checkServerDomainIpv6.com
              use_ipv6: true
            - server: 172.16.1.13
              source: GigabitEthernet0/1
          source: GigabitEthernet0/1
          trusted_keys:
            - range_end: 3
              range_start: 10
            - range_start: 21
          update_calendar: true
        state: rendered

    # Module Execution Result:
    # ------------------------

    # "rendered": [
    #       "ntp allow mode control 4",
    #       "ntp allow mode private",
    #       "ntp authenticate",
    #       "ntp broadcastdelay 22",
    #       "ntp clock-period 5",
    #       "ntp logging",
    #       "ntp master 4",
    #       "ntp max-associations 34",
    #       "ntp maxdistance 3",
    #       "ntp mindistance 10",
    #       "ntp orphan 4",
    #       "ntp panic update",
    #       "ntp source GigabitEthernet0/1",
    #       "ntp update-calendar",
    #       "ntp access-group ipv4 peer DHCP-Server kod",
    #       "ntp access-group ipv6 peer preauth_ipv6_acl kod",
    #       "ntp access-group peer 2 kod",
    #       "ntp access-group query-only 10",
    #       "ntp authentication-key 2 md5 SomeSecurePassword 22",
    #       "ntp peer 172.16.1.10 version 2",
    #       "ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2",
    #       "ntp peer ip checkPeerDomainIpv4.com prefer",
    #       "ntp peer ipv6 checkPeerDomainIpv6.com",
    #       "ntp peer ipv6 testPeerDomainIpv6.com prefer",
    #       "ntp server 172.16.1.12 version 2",
    #       "ntp server ipv6 checkServerDomainIpv6.com",
    #       "ntp server 172.16.1.13 source GigabitEthernet0/1",
    #       "ntp trusted-key 3 - 3",
    #       "ntp trusted-key 21"
    #     ]

    # Using state: parsed

    # File: parsed.cfg
    # ----------------

    # ntp allow mode control 4
    # ntp allow mode private
    # ntp authenticate
    # ntp broadcastdelay 22
    # ntp clock-period 5
    # ntp logging
    # ntp master 4
    # ntp max-associations 34
    # ntp maxdistance 3
    # ntp mindistance 10
    # ntp orphan 4
    # ntp panic update
    # ntp source GigabitEthernet0/1
    # ntp update-calendar
    # ntp access-group ipv4 peer DHCP-Server kod
    # ntp access-group ipv6 peer preauth_ipv6_acl kod
    # ntp access-group peer 2 kod
    # ntp access-group query-only 10
    # ntp authentication-key 2 md5 SomeSecurePassword 22
    # ntp peer 172.16.1.10 version 2
    # ntp peer 172.16.1.11 key 2 minpoll 5 prefer version 2
    # ntp peer ip checkPeerDomainIpv4.com prefer
    # ntp peer ipv6 checkPeerDomainIpv6.com
    # ntp peer ipv6 testPeerDomainIpv6.com prefer
    # ntp server 172.16.1.12 version 2
    # ntp server ipv6 checkServerDomainIpv6.com
    # ntp server 172.16.1.13 source GigabitEthernet0/1
    # ntp trusted-key 3 - 13
    # ntp trusted-key 21

    # Parsed play:
    # ------------

    - name: Parse the provided configuration with the existing running configuration
      cisco.ios.ios_ntp_global:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------

    # "parsed": {
    #     "access_group": {
    #         "peer": [
    #             {
    #                 "access_list": "2",
    #                 "kod": true
    #             },
    #             {
    #                 "access_list": "DHCP-Server",
    #                 "ipv4": true,
    #                 "kod": true
    #             },
    #             {
    #                 "access_list": "preauth_ipv6_acl",
    #                 "ipv6": true,
    #                 "kod": true
    #             }
    #         ],
    #         "query_only": [
    #             {
    #                 "access_list": "10"
    #             }
    #         ]
    #     },
    #     "allow": {
    #         "control": {
    #             "rate_limit": 4
    #         },
    #         "private": true
    #     },
    #     "authenticate": true,
    #     "authentication_keys": [
    #         {
    #             "algorithm": "md5",
    #             "encryption": 22,
    #             "id": 2,
    #             "key": "SomeSecurePassword"
    #         }
    #     ],
    #     "broadcast_delay": 22,
    #     "clock_period": 5,
    #     "logging": true,
    #     "master": {
    #         "stratum": 4
    #     },
    #     "max_associations": 34,
    #     "max_distance": 3,
    #     "min_distance": 10,
    #     "orphan": 4,
    #     "panic_update": true,
    #     "peers": [
    #         {
    #             "peer": "172.16.1.10",
    #             "version": 2
    #         },
    #         {
    #             "peer": "checkPeerDomainIpv6.com",
    #             "use_ipv6": true
    #         }
    #     ],
    #     "servers": [
    #         {
    #             "server": "172.16.1.12",
    #             "version": 2
    #         },
    #         {
    #             "server": "172.16.1.13",
    #             "source": "GigabitEthernet0/1"
    #         },
    #         {
    #             "server": "checkServerDomainIpv6.com",
    #             "use_ipv6": true
    #         }
    #     ],
    #     "source": "GigabitEthernet0/1",
    #     "trusted_keys": [
    #         {
    #             "range_start": 21
    #         },
    #         {
    #             "range_end": 13,
    #             "range_start": 3
    #         }
    #     ],
    #     "update_calendar": true
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ntp peer 20.18.11.3 key 6 minpoll 15 prefer version 2&#x27;, &#x27;ntp access-group ipv4 peer DHCP-Server kod&#x27;, &#x27;ntp trusted-key 9 - 96&#x27;, &#x27;ntp master stratum 2&#x27;, &#x27;ntp orphan 4&#x27;, &#x27;ntp panic update&#x27;]</div>
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
                <td>when state is <em>rendered</em></td>
                <td>
                            <div>The provided configuration in the task rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ntp master stratum 2&#x27;, &#x27;ntp server ip testserver.com prefer&#x27;, &#x27;ntp authentication-key 2 md5 testpass 22&#x27;, &#x27;ntp allow mode control 4&#x27;, &#x27;ntp max-associations 34&#x27;, &#x27;ntp broadcastdelay 22&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
