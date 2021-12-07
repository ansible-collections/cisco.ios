==================================
Cisco Ios Collection Release Notes
==================================

.. contents:: Topics


v2.6.0
======

Minor Changes
-------------

- `ios_acls` - feature: Remarks can be configured for ACLs.
- `ios_snmp_server` - New Resource module added.

Bugfixes
--------

- 'ios_banner' - Bugfix for presence of multiple delimitation chars in the banner's declaration and idempotence improvement.
- Fix ntp_global - remove no_log for key_id under peer and server attributes.
- Fix ntp_global - to handle when attribute value is false.
- `ios_acls` - bugfixes and optimization for ACLs.
- `ios_l2_interfaces` - fix unable to set switchport mode properly.
- `ios_logging_global` - fix host ipv6 commands not parsed correctly.
- `ios_logging_global` - fix wrong ordering of commands fired on replaced state.

Documentation Changes
---------------------

- Added connection network_cli in note for missing modules.
- Fixed ios_commands module example as per documentation.

New Modules
-----------

- ios_snmp_server - snmp_server resource module

v2.5.0
======

Minor Changes
-------------

- Added ios_ntp_global resource module.
- Terminal plugin to support IOS device running in SD-WAN mode.

Deprecated Features
-------------------

- Deprecated ios_ntp modules.

Bugfixes
--------

- Fixed bgp_address_family, for rendering multiple neighbors when available in config.
- fixed become functionality on privilege level not 15.
- ios_facts - fix for devices which have no support for VLANs, such as L3 devices.
- ios_vlans - for playbook execution module fails with an error when target device does not support VLANs, The offline states rendered and parsed will work as expected.

Documentation Changes
---------------------

- Doc fix for ios_acl_interfaces.
- Doc fix for ios_logging_global.

New Modules
-----------

- ios_ntp_global - ntp_global resource module

v2.4.0
======

Minor Changes
-------------

- Add support for VRF configuration under NTP server.

Deprecated Features
-------------------

- Deprecated ios_bgp in favor of ios_bgp_global and ios_bgp_address_family.
- Remove testing with provider for ansible-test integration jobs. This helps prepare us to move to network-ee integration tests.

Bugfixes
--------

- Logging command template fixed supporting Jinja version for centos-8 EEs.
- Updated ios_l3_interface as the newer Resource Module implementation and added features.

Documentation Changes
---------------------

- Sample commands added for l3_interfaces.
- Updated ios_logging_global Resource Module documentation with proper examples.

v2.3.1
======

Bugfixes
--------

- Updated ios_command module doc example section with appropriate punctuation.
- ios_user fails to add password when configured in separate task with update_password.

Documentation Changes
---------------------

- Broken link in documentation fixed.

v2.3.0
======

Minor Changes
-------------

- Deprecated next_hop_self type bool and introduced nexthop_self as dict under bgp_address_family.
- Move ios_config idempotent warning message with the task response under `warnings` key if `changed` is `True`
- PR adds the implementation of object group param to acls source and destination parameters (https://github.com/ansible-collections/cisco.ios/issues/339).
- PR to fix the bgp global activate rendering and fix bgp address family round trip failure (https://github.com/ansible-collections/cisco.ios/issues/353).
- To add ospfv2 passive_interfaces param with added functionality (https://github.com/ansible-collections/cisco.ios/issues/336).
- To add updated prefix lists and route maps params to Bgp AF RM (https://github.com/ansible-collections/cisco.ios/issues/267).
- To update prefix list and acls merge behaviour and update prefix list description position in model (https://github.com/ansible-collections/cisco.ios/issues/345).

Bugfixes
--------

- Add support for autoconfig and dhcp keywords for IPv6 addresses in l3_interfaces (https://github.com/ansible-collections/cisco.ios/pull/269).
- Reordering names of interface for proper value assignment
- fixes Serial interface configuration for l3_interfaces module and Unit Test cases added.
- fixes banner module with new attribute introduced
- fixes soft_reconfiguration and prefix_list command formation.

v2.2.0
======

Minor Changes
-------------

- Add ios_logging_global module.
- IOS Prefix list resource module.

Bugfixes
--------

- Fix IOS bgp global RM tracback while there's no bestpath/nopeerup_delay configured.
- Fix logging commands for v12 versions (https://github.com/ansible-collections/cisco.ios/issues/207).
- To fix IOS vlans RM where traceback was thrown if show vlan wasn't supported on the device and also fix replace and overridden state behaviour.
- To fix Spelling glitch.
- To fix ios acls overridden and replaced state of their inconsistent behaviour (https://github.com/ansible-collections/cisco.ios/issues/250).
- To fix ios_bgp_address_family neighbor next_hop_self param (https://github.com/ansible-collections/cisco.ios/issues/319).

New Modules
-----------

- ios_logging_global - Logging resource module.
- ios_prefix_lists - Prefix Lists resource module.

v2.1.0
======

Minor Changes
-------------

- Add ios_route_maps Resource Module (https://github.com/ansible-collections/cisco.ios/pull/297).
- Add support for ansible_network_resources key allows to fetch the available resources for a platform (https://github.com/ansible-collections/cisco.ios/pull/292).

Security Fixes
--------------

- To fix Cisco IOS no log issue and add ignore txt for 2.12 (https://github.com/ansible-collections/cisco.ios/pull/304).

Bugfixes
--------

- To fix the wrong arg being passed in acls template function (https://github.com/ansible-collections/cisco.ios/pull/305).

New Modules
-----------

- ios_route_maps - Route Maps resource module.

v2.0.1
======

Minor Changes
-------------

- Remove tests/sanity/requirements.txt (https://github.com/ansible-collections/cisco.ios/pull/261).

Bugfixes
--------

- Doc update to update users WRT to idempotence issue in ios_logging when logging is ON (https://github.com/ansible-collections/cisco.ios/pull/287).
- PR to fix ios_l2_interfaces issue where it wasn't working with range of vlans as expected (https://github.com/ansible-collections/cisco.ios/pull/264).
- To add support for TwoGigabitEthernet interface option from IOS standpoint (https://github.com/ansible-collections/cisco.ios/pull/262).
- To fix ios_acls Nonetype error when aces are empty (https://github.com/ansible-collections/cisco.ios/pull/260).
- To fix ios_acls log and log_input params (https://github.com/ansible-collections/cisco.ios/pull/265).
- To fix ios_acls resource module acl_name traceback over some switches (https://github.com/ansible-collections/cisco.ios/pull/285).
- To fix ios_vlans traceback error when empty line with just Ports information is available in config (https://github.com/ansible-collections/cisco.ios/pull/273).

v2.0.0
======

Major Changes
-------------

- Please refer to ansible.netcommon `changelog <https://github.com/ansible-collections/ansible.netcommon/blob/main/changelogs/CHANGELOG.rst#ansible-netcommon-collection-release-notes>`_ for more details.
- Requires ansible.netcommon v2.0.0+ to support `ansible_network_single_user_mode` and `ansible_network_import_modules`.

Minor Changes
-------------

- Add ios_bgp_address_family Resource Module. (https://github.com/ansible-collections/cisco.ios/pull/219).
- Adds support for `single_user_mode` command output caching. (https://github.com/ansible-collections/cisco.ios/pull/204).

Bugfixes
--------

- To fix ios_acls parsed state example under module doc (https://github.com/ansible-collections/cisco.ios/pull/244).
- fix error when comparing two vlan using string instead of the int value (https://github.com/ansible-collections/cisco.ios/pull/249).

New Modules
-----------

- ios_bgp_address_family - BGP Address Family resource module.

v1.3.0
======

Minor Changes
-------------

- Add ios_bgp_global module.

Bugfixes
--------

- Add support size and df_bit options for ios_ping (https://github.com/ansible-collections/cisco.ios/pull/228).
- IOS resource modules minor doc updates (https://github.com/ansible-collections/cisco.ios/pull/233).
- IOS_CONFIG, incorrectly claims success when Command Rejected (https://github.com/ansible-collections/cisco.ios/pull/215).
- To fix ios_static_routes facts parsing in presence of interface (https://github.com/ansible-collections/cisco.ios/pull/225).
- Update doc to clarify on input config pattern (https://github.com/ansible-collections/cisco.ios/pull/220).
- Updating ios acls module to use newer CLI RM approach to resolve all of the ACL related bugs (https://github.com/ansible-collections/cisco.ios/pull/211).

New Modules
-----------

- ios_bgp_global - BGP Global resource module

v1.2.1
======

Bugfixes
--------

- Add version key to galaxy.yaml to work around ansible-galaxy bug.
- To fix ios_ospf_interfaces resource module authentication param behaviour (https://github.com/ansible-collections/cisco.ios/issues/209).

v1.2.0
======

Minor Changes
-------------

- Add ios_ospf_interfaces module.

Bugfixes
--------

- To enable ios ospfv3 integration tests (https://github.com/ansible-collections/cisco.ios/pull/165).
- To fix IOS static routes idempotency issue coz of netmask to cidr conversion (https://github.com/ansible-collections/cisco.ios/pull/177).
- To fix ios_static_routes where interface ip route-cache config was being parsed and resulted traceback (https://github.com/ansible-collections/cisco.ios/pull/176).
- To fix ios_vlans traceback bug when the name had Remote in it and added unit TC for the module (https://github.com/ansible-collections/cisco.ios/pull/179).
- To fix the traceback issue for longer vlan name having more than 32 characters (https://github.com/ansible-collections/cisco.ios/pull/182).

New Modules
-----------

- ios_ospf_interfaces - OSPF Interfaces resource module

v1.1.0
======

Minor Changes
-------------

- Add ios_ospfv3 module.

Bugfixes
--------

- Add support for interface type Virtual-Template (https://github.com/ansible-collections/cisco.ios/pull/154).
- Added support for interface Tunnel (https://github.com/ansible-collections/cisco.ios/pull/145).
- Fix element type of ios_command's command parameter (https://github.com/ansible-collections/cisco.ios/pull/151).
- To fix the incorrect command displayed under ios_l3_interfaces resource module docs (https://github.com/ansible-collections/cisco.ios/pull/149).

New Modules
-----------

- ios_ospfv3 - OSPFv3 resource module

v1.0.3
======

Release Summary
---------------

Releasing 1.0.3 with updated readme with changelog link, galaxy description, and bugfix.

Bugfixes
--------

- To fix IOS l2 interfaces for traceback error and merge operation not working as expected (https://github.com/ansible-collections/cisco.ios/pull/103).
- To fix the issue where ios acls was complaining in absence of protocol option value (https://github.com/ansible-collections/cisco.ios/pull/124).

v1.0.2
======

Release Summary
---------------

Re-releasing 1.0.1 with updated changelog.

v1.0.1
======

Minor Changes
-------------

- Removes IOS sanity ignores and sync for argspec and docstring (https://github.com/ansible-collections/cisco.ios/pull/114).
- Updated docs.

Bugfixes
--------

- Make `src`, `backup` and `backup_options` in ios_config work when module alias is used (https://github.com/ansible-collections/cisco.ios/pull/107).

v1.0.0
======

New Plugins
-----------

Cliconf
~~~~~~~

- ios - Use ios cliconf to run command on Cisco IOS platform

New Modules
-----------

- ios_acl_interfaces - ACL interfaces resource module
- ios_acls - ACLs resource module
- ios_banner - Manage multiline banners on Cisco IOS devices
- ios_bgp - Configure global BGP protocol settings on Cisco IOS.
- ios_command - Run commands on remote devices running Cisco IOS
- ios_config - Manage Cisco IOS configuration sections
- ios_facts - Collect facts from remote devices running Cisco IOS
- ios_interface - (deprecated, removed after 2022-06-01) Manage Interface on Cisco IOS network devices
- ios_interfaces - Interfaces resource module
- ios_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco IOS devices.
- ios_l2_interfaces - L2 interfaces resource module
- ios_l3_interface - (deprecated, removed after 2022-06-01) Manage Layer-3 interfaces on Cisco IOS network devices.
- ios_l3_interfaces - L3 interfaces resource module
- ios_lacp - LACP resource module
- ios_lacp_interfaces - LACP interfaces resource module
- ios_lag_interfaces - LAG interfaces resource module
- ios_linkagg - Manage link aggregation groups on Cisco IOS network devices
- ios_lldp - Manage LLDP configuration on Cisco IOS network devices.
- ios_lldp_global - LLDP resource module
- ios_lldp_interfaces - LLDP interfaces resource module
- ios_logging - Manage logging on network devices
- ios_ntp - Manages core NTP configuration.
- ios_ospfv2 - OSPFv2 resource module
- ios_ping - Tests reachability using ping from Cisco IOS network devices
- ios_static_route - (deprecated, removed after 2022-06-01) Manage static IP routes on Cisco IOS network devices
- ios_static_routes - Static routes resource module
- ios_system - Manage the system attributes on Cisco IOS devices
- ios_user - Manage the aggregate of local users on Cisco IOS device
- ios_vlan - (deprecated, removed after 2022-06-01) Manage VLANs on IOS network devices
- ios_vlans - VLANs resource module
- ios_vrf - Manage the collection of VRF definitions on Cisco IOS devices
