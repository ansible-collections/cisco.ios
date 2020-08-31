==================================
Cisco Ios Collection Release Notes
==================================

.. contents:: Topics

v1.0.3
======

Release Summary
---------------

- Releasing 1.0.3 with updated readme with changelog link, galaxy description, and bugfix.

Bugfixes
--------

- To fix the issue where ios acls was complaining in absence of protocol option value (https://github.com/ansible-collections/cisco.ios/pull/124).
- To fix IOS l2 interfaces for traceback error and merge operation not working as expected (https://github.com/ansible-collections/cisco.ios/pull/103).

v1.0.2
======

Release Summary
---------------

- Re-releasing 1.0.1 with updated changelog.

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
