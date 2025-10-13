==================================
Cisco Ios Collection Release Notes
==================================

.. contents:: Topics

v11.1.1
=======

Bugfixes
--------

- cisco.ios.ios_bgp_address_family - Encrypted strings as password are not evaluated rather treated as string forcefully.
- cisco.ios.ios_hsrp_interfaces - Fixed default values for version and priority.
- cisco.ios.ios_hsrp_interfaces - Fixed overridden state to be idempotent with ipv6 configuration.
- cisco.ios.ios_hsrp_interfaces - Fixed parsers to group HSRP configuration and optimize parsing time.
- cisco.ios.ios_hsrp_interfaces - Fixed removal of HSRP configuration when state is deleted, replaced, overridden.
- cisco.ios.ios_hsrp_interfaces - Fixed rendered output for standby redirect advertisement authentication key-chain.
- cisco.ios.ios_hsrp_interfaces - Fixed rendered output for standby redirect advertisement authentication key-string with encryption.
- cisco.ios.ios_hsrp_interfaces - Fixed rendered output for standby redirect advertisement authentication.
- cisco.ios.ios_hsrp_interfaces - Handle operation of list attributes like ipv6, ip, track.
- cisco.ios.ios_l2_interfaces - Add private-vlan support to switchport.

Documentation Changes
---------------------

- Updated documentation for cisco.ios.ios_hsrp_interfaces module, with examples for all parameters.

v11.1.0
=======

Minor Changes
-------------

- ios_config - added answering prompt functionality while working in config mode on ios device
- ios_facts - Add chassis_id value to ansible_net_neighbors dictionary for lldp neighbours.

Bugfixes
--------

- Fixed an issue where configuration within an address family (ipv6) was ignored by the parser.
- cisco.ios.ios_vrf_global - fixed issue preventing idempotent configuration of multiple import/export route-targets for a VRF.
- ios_hsrp_interfaces - Device defaults version to 1 if standby_groups is present but version is not configured. and module would also consider priority as 100 if not configured, to maintain idempotency.
- ios_hsrp_interfaces - Fixed operation for ipv6 standby configuration.
- ios_static_routes - Fix parsing of static routes with interface and distance in gathered state

v11.0.0
=======

Release Summary
---------------

With this release, the minimum required version of `ansible.netcommon` for this collection is `>=8.1.0`. The last version known to be compatible with `ansible-core<=2.18.x` is ansible.netcommon `v8.0.1` and cisco.ios `v10.1.1`.

Major Changes
-------------

- Bumping `dependencies` of ansible.netcommon to `>=8.1.0`, since previous versions of the dependency had compatibility issues with `ansible-core>=2.19`.

Bugfixes
--------

- ios_vrf_address_family - fixed an issue where the module failed to gather `mdt` configuration options.

v10.1.1
=======

Bugfixes
--------

- cisco.ios.ios_acls - Added default acls to not get updated/removed in any state.
- cisco.ios.ios_hsrp_interfaces - Fix module operation around the preempt attributes, also addressed issues around command ordering.
- cisco.ios.ios_l3_interfaces - Fixed Helper Address command support for l3 interface.
- cisco.ios.ios_ospfv2 - Fix ospf admin distance parameter and fix other distance specific attributes to be optional.
- cisco.ios.ios_vlans - Fixed errors during VLAN overrides where primary VLANs have private VLAN associations referencing non-existent or higher VLAN IDs, ensuring smoother private VLAN handling and preventing module failures.
- ios_bgp_address_family - Refined state handling for `replaced` and `overridden` modes and enhanced address-family parsing to accurately differentiate between types such as unicast, multicast, and others.
- ios_static_routes - Add missing interface names in parser
- ios_vrf_address_family - Added support for parsing the `stitching` attribute under route targets when gathering facts. Enhanced handling of `import_config` and `export` and renamed them to `imports` and `exports` to consistently represent them as lists of dictionaries during fact collection.

Documentation Changes
---------------------

- ios_hsrp_interfaces - Corrected the version_added information and enhanced the documentation for subnet-related parameters.

v10.1.0
=======

Minor Changes
-------------

- ios_hsrp_interfaces - Added support for cisco.ios.hsrp_interfaces module (standby commands).

Bugfixes
--------

- cisco.ios.ios_interfaces - Improved handling of the `enabled` state to prevent incorrect `shutdown` or `no shutdown` commands during configuration changes.
- ios_acls - Fix issue where commands were not being parsed correctly and incorrect commands were being generated.
- ios_bgp_address_family - fix configuration of neighbor's as-override split-horizon.

v10.0.0
=======

Release Summary
---------------

With this release, the minimum required version of `ansible-core` for this collection is `2.16.0`. The last version known to be compatible with `ansible-core` versions below `2.16` is v9.2.0.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.16.0`, since previous ansible-core versions are EoL now.

Minor Changes
-------------

- ios_interfaces - Added service-policy, logging and snmp configuration options for interface.
- ios_l2_interfaces - Added a few switchport and spanning-tree configuration options for interface.
- ios_l3_interfaces - Added a few ip configuration options for interface.

v9.2.0
======

Minor Changes
-------------

- Add ios_evpn_ethernet resource module.

Deprecated Features
-------------------

- ios_vlans - deprecate mtu, please use ios_interfaces to configure mtu to the interface where vlans is applied.

Bugfixes
--------

- ios_logging_global - Fixed issue where cisco.ios.logging_global module was not showing idempotent behaviour when trap was set to informational.
- ios_vlans - Defaut mtu would be captured (1500) and no configuration for mtu is allowed via ios_vlans module.
- ios_vlans - Fixed an issue in the `cisco.ios.ios_vlans` module on Cisco Catalyst 9000 switches where using state:purged generated an incorrect command syntax (`no vlan configuration <vlan_id>` instead of `no vlan <vlan_id>`).
- ios_vlans - Resolved a failure in the `cisco.ios.ios_vlans` module when using state:deleted, where the module incorrectly attempted to remove VLANs using `no mtu <value>`, causing an invalid input error. The fix ensures that the module does not generate `no mtu` commands during VLAN deletion, aligning with the correct VLAN removal behavior on Catalyst 9000 switches.

New Modules
-----------

- ios_evpn_ethernet - Resource module to configure L2VPN EVPN Ethernet Segment.

v9.1.2
======

Bugfixes
--------

- ios_acls - Fixed issue where cisco.ios.ios_acls module failed to process IPv6 ACL remarks, causing unsupported parameter errors.
- ios_route_maps - Fixes an issue where 'no description value' is an invalid command on the latest devices.

v9.1.1
======

Bugfixes
--------

- Added support for FourHundredGigE, FiftyGigE and FourHundredGigabitEthernet.

v9.1.0
======

Minor Changes
-------------

- Added ios_vrf_interfaces resource module,that helps with configuration of vrfs within interface
- Adds a new module `ios_vrf_address_family` to manage VRFs address families on Cisco IOS devices.

Bugfixes
--------

- Added a test to validate the gathered state for VLAN configuration context, improving reliability.
- Cleaned up unit tests that were passing for the wrong reasons. The updated tests now ensure the right config sections are verified for VLAN configurations.
- Fix overridden state operations to ensure excluded VLANs in the provided configuration are removed, thus overriding the VLAN configuration.
- Fix purged state operation to enable users to completely remove VLAN configurations.
- Fixed an issue with VLAN configuration gathering where pre-filled data was blocking proper fetching of dynamic VLAN details. Now VLAN facts are populated correctly for all cases.
- Fixes an issue with facts gathering failing when an sub interface is in a deleted state.
- Improve documentation to provide clarity on the "shutdown" variable.
- Improve unit tests to align with the changes made.
- Made improvements to ensure VLAN facts are gathered properly, both for specific configurations and general VLAN settings.
- ios_route_maps - Fix removal of ACLs in replaced state to properly remove unspecified ACLs while leaving specified ones intact.
- ios_route_maps - Fix removal of ACLs logic in replaced state to properly remove unspecified ACLs while leaving specified ones intact.

v9.0.3
======

Bugfixes
--------

- ios_bgp_address_family - fix parsing of password_options while gathering password configuration from appliance.
- ios_bgp_global - fix parsing of password_options while gathering password configuration from appliance.

Documentation Changes
---------------------

- Includes a new support related section in the README.
- Removed the Roadmap section from the README.

v9.0.2
======

Bugfixes
--------

- ios_bgp_address_family - Add support for maximum-paths configuration.
- ios_bgp_address_family - Add support for maximum-secondary-paths configuration.
- ios_interfaces - Fixes rendering of FiftyGigabitEthernet as it was wrongly rendering FiftyGigabitEthernet as FiveGigabitEthernet.
- ios_snmp_server - Fixes an issue where enabling the read-only (ro) attribute in communities was not idempotent.
- ios_static_routes - Fix processing of metric_distance as it was wrongly populated under the forward_router_address attribute.

v9.0.1
======

Bugfixes
--------

- bgp_global - fix ebgp_multihop recognnition and hop_count settings
- ios_service - Fix a typo causing log timestamps not being configurable
- ios_vlans - Make the module fail when vlan name is longer than 32 characters with configuration as VTPv1 and VTPv2.
- static_routes - add TenGigabitEthernet as valid interface

Documentation Changes
---------------------

- ios_facts - update documentation for ansible_net_memtotal_mb, ansible_net_memfree_mb return values as mebibytes (MiB), not megabits (Mb)

v9.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.15.0`. The last known version compatible with ansible-core<2.15 is v8.0.0.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.15.0`, since previous ansible-core versions are EoL now.

Minor Changes
-------------

- Add ios_vrf_global resource module in favor of ios_vrf module (fixes - https://github.com/ansible-collections/cisco.ios/pull/1055)

Deprecated Features
-------------------

- ios_bgp_address_family - deprecated attribute password in favour of password_options within neigbhors.
- ios_bgp_global - deprecated attributes aggregate_address, bestpath, inject_map, ipv4_with_subnet, ipv6_with_subnet, nopeerup_delay, distribute_list, address, tag, ipv6_addresses, password, route_map, route_server_context and scope
- ios_linkagg - deprecate legacy module ios_linkagg
- ios_lldp - deprecate legacy module ios_lldp

Bugfixes
--------

- ios_acls - fix incorrect mapping of port 135/udp to msrpc.
- ios_l3_interfaces - Fix gathering wrong facts for source interface in ipv4.
- ios_service - Add tcp_small_servers and udp_small_servers attributes, to generate configuration.
- ios_service - Fix timestamps attribute, to generate right configuration.
- ios_static_routes - Fix gathering facts by properly distinguising routes.
- l2_interfaces - If a large number of VLANs are affected, the configuration will now be correctly split into several commands.
- snmp_server - Fix configuration command for snmp-server host.
- snmp_server - Fix wrong syntax of snmp-server host command generation.

Documentation Changes
---------------------

- logging_global - update documentation for severity attribute within buffered.

v8.0.0
======

Major Changes
-------------

- Update the netcommon base version 6.1.0 to support cli_restore plugin.

Minor Changes
-------------

- Add support for cli_restore functionality.
- Please refer the PR to know more about core changes (https://github.com/ansible-collections/ansible.netcommon/pull/618).
- cli_restore module is part of netcommon.

v7.0.0
======

Major Changes
-------------

- ios_ntp - Remove deprecated ntp legacy module

Removed Features (previously deprecated)
----------------------------------------

- Deprecated ios_ntp module in favor of ios_ntp_global.

v6.1.4
======

Bugfixes
--------

- ios_acls - update module to apply remarks entry with sequence numbers.
- ios_bgp_address_family - description attribute, evalutated as complex object casted to string.
- ios_bgp_global - description attribute, evalutated as complex object casted to string.
- ios_interfaces - description attribute, evalutated as complex object casted to string.
- ios_prefix_lists - description attribute, evalutated as complex object casted to string.
- ios_route_maps - description attribute, evalutated as complex object casted to string.

v6.1.3
======

Bugfixes
--------

- ios_acls - Adds back existing remarks for an ace entry when updated with replaced or overridden state, as all remarks for a specific sequence gets removed when ace entry is updated.
- ios_bgp_global - Shutdown attributes generates negate command on set as false.
- ios_vrf - Update and add missing argspec keys that define the attributes.

Documentation Changes
---------------------

- ios_vrf - Update and add missing documentation for ios_vrf module.

v6.1.2
======

Bugfixes
--------

- ios_acls - Fix replaced state to consider remarks and ace entries while comparing configuration.
- ios_acls - correctly match the different line for ACL without sequence number
- ios_acls - take correctly in case where we want to push an ACL from a different type
- ios_ospfv2 - Fix improper rendering of admin_distance attribute.
- ios_snmp_server - fixed config issue with snmp user password update being idempotent on consecutive runs.
- ios_user - Fix configuration of hashed passwords and secrets.

v6.1.1
======

Bugfixes
--------

- Prevents module_defaults from were being incorrectly applied to the platform action, instead of the concerned module.
- ios_vlans - fixes behaviour of shutdown attribute with action states.

v6.1.0
======

Minor Changes
-------------

- ios_bgp_global - added 'bgp.default.ipv4_unicast' and 'bgp.default.route_target.filter' key
- ios_l3_interfaces - added 'autostate', 'mac_address', 'ipv4.source_interface', and 'ipv6.enable' key
- ios_vlans - Add purged state to deal with toplevel vlan and vlan configuration config.

Bugfixes
--------

- ios_bgp_global - fix template attribute to generate configuration commands.
- ios_l3_interfaces - remove validation from ipv6 address parameter.
- ios_snmp_server - fix group and user IPv6 ACL commands.
- ios_user - fix configuration of user with hashed password.
- ios_user - fixed configuration removal of ssh users using purge.
- ios_vlans - Make behaviour of the action states consistent.
- ios_vlans - Top level configuration attribute is not required, the module works with vlan and vlan configuration both.

v6.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. The last known version compatible with ansible-core<2.14 is `v5.3.0`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

Removed Features (previously deprecated)
----------------------------------------

- Removed previously deprecated ios_bgp module in favor of ios_bgp_global and ios_bgp_address_family.

v5.3.0
======

Minor Changes
-------------

- Added ios_evpn_evi resource module.
- Added ios_evpn_global resource module.
- Added ios_vxlan_vtep resource module.
- Fixed ios_evpn_evi resource module integration test failure - code to remove VLAN config.
- ios_bgp_address_family - Fixed an issue with inherit peer-policy CLI
- ios_bgp_address_family - added 'advertise' key
- ios_vlans - added vlan config CLI feature.
- ios_vrf - added MDT related keys

Bugfixes
--------

- Updated the ios_ping ping module to support size param.
- ios_acls - make sequence optional for rendering of standard acls.
- ios_bgp_global - Explicitly add neighbor address to every parser.
- ios_bgp_global - remote_as not mendatory for neighbors.
- ios_vrf - added MDT related keys

New Modules
-----------

- ios_evpn_evi - Resource module to configure L2VPN EVPN EVI.
- ios_evpn_global - Resource module to configure L2VPN EVPN.
- ios_vxlan_vtep - Resource module to configure VXLAN VTEP interface.

v5.2.0
======

Minor Changes
-------------

- ios_acls - make remarks ordered and to be applied per ace basis.
- ios_acls - remarks in replaced and overridden state to be negated once per ace.
- ios_config - Relax restrictions on I(src) parameter so it can be used more like I(lines).
- ios_snmp_server - Fix an issue with cbgp2 to take in count correctly the bgp traps
- ios_snmp_server - Update the module to manage correctly a lot of traps not take in count

Deprecated Features
-------------------

- ios_snmp_server - deprecate traps.envmon.fan with traps.envmon.fan_enable
- ios_snmp_server - deprecate traps.mpls_vpn with traps.mpls

Bugfixes
--------

- Fix invalid password length not being recognized by the error parser.

v5.1.0
======

Minor Changes
-------------

- Fixe an issue with some files that doesn't pass the PEP8 sanity check because `type(<obj>) == <type>` is not allowed. We need to use `isinstance(<obj>,<type>)` function in place
- ios_snmp_user - update the user part to compare correctly the auth and privacy parts.
- ospfv2 - added more tests to improve coverage for the rm_template
- ospfv2 - aliased passive_interface to passive_interfaces that supports a list of interfaces
- ospfv2 - fix area ranges rendering
- ospfv2 - fix passive interfaces rendering
- ospfv2 - optimized all the regex to perform better
- ospfv2 - optimized the config side code for quicker comparison and execution

Deprecated Features
-------------------

- ospfv2 - removed passive_interface to passive_interfaces that supports a list of interfaces

Bugfixes
--------

- The regex looking for errors in the terminal output was matching anything with '\S+ Error:'. Caused issues with 'show runnning-config' if this string appeared in the output. Updated the regex to require the % anchor.
- bgp_address_family - fix deleted string with int concat issue in bgp_address_family.
- ios_acls - Fix protocol_options rendering corrects processing of overridden/ replaced state.
- ios_acls - Fix standard acls rendering.
- ios_bgp_address_family - fix rendering of remote_as configuration with period.
- ios_logging_global - fix configuration order to configure discriminator before buffer.
- ios_prefix_lists - fix deleted state to remove exisiting prefix lists from configuration.
- ios_service - Put condition to add `private_config_encryption` in default services

Documentation Changes
---------------------

- Fix prefix_lists docs.
- Update examples for ospf_interfaces
- Update examples for ospfv2
- Update examples for ospfv3
- ios_acls - update examples and use YAML output in them for better readibility.
- ios_command - Fix formatting of examples.

v5.0.0
======

Major Changes
-------------

- This release removes a previously deprecated modules, and a few attributes from this collection. Refer to **Removed Features** section for details.

Minor Changes
-------------

- ios_facts - Add CPU utilization. (https://github.com/ansible-collections/cisco.ios/issues/779)

Removed Features (previously deprecated)
----------------------------------------

- Deprecated ios_logging module in favor of ios_logging_global.
- Deprecated next_hop_self attribute for bgp_address_family with nexthop_self.

Bugfixes
--------

- ios_facts - Fix facts gathering when memory statistics head is not hexadecimal. (https://github.com/ansible-collections/cisco.ios/issues/776)
- ios_snmp_server - Fixes error handling for snmp user when snmp agent is not enabled
- ios_static_routes - Fix non vlan entries to have unique group identifier.
- ios_static_routes - Fix parsers to parse interface attribute correctly.

Documentation Changes
---------------------

- ios_facts - Add ansible_net_cpu_utilization.

v4.6.1
======

Bugfixes
--------

- ios_l3_interfaces - account for secondary/primary when comparing ipv4 addresses. (https://github.com/ansible-collections/cisco.ios/issues/826)
- ios_lag_interfaces - Fix empty facts to be a list.
- ios_ospf_interface - Fix configuration rendering for ipv4 and ipv6 configurations.
- ios_ospf_interface - Fix replaced and overridden state, action to negate superfluous configuration.
- ios_snmp_server - Add default versions to version 3 users.
- snmp_server - update module to get snmp_server user configuration.

Documentation Changes
---------------------

- Lint examples as per ansible-lint.

v4.6.0
======

Minor Changes
-------------

- ios_interfaces - Add template attribute to provide support for cisco ios templates.
- ios_service - Create module to manage service configuration on IOS switches

Bugfixes
--------

- ios_facts - fix calculation of memory from bytes to megabytes; grab correct output element for free memory (https://github.com/ansible-collections/cisco.ios/issues/763)
- ospfv2 - Fixed rendering of capability command with vrf_lite.
- ospfv3 - Fixed rendering of capability command with vrf_lite.

Documentation Changes
---------------------

- ios_bgp_address_family - Fixed examples formatting.
- ios_bgp_global - Fixed examples formatting.
- ios_interfaces - Corrected inteface names in documentation.
- ios_interfaces - Fixed module documentation and examples.
- ios_l2_interfaces - Fixed module documentation and examples.
- ios_l3_interfaces - Fixed module documentation and examples.
- ios_l3_interfaces - Fixed module examples, update tasks to generate address and not network interface.
- ios_static_routes - Corrected static routes before state in documentation.
- ios_static_routes - Fixed examples formatting.

New Modules
-----------

- ios_service - Resource module to configure service.

v4.5.0
======

Minor Changes
-------------

- ios_bgp_address_family - add option redistribute.ospf.include_connected when redistributing OSPF in IPv6 AFI
- ios_bgp_address_family - add option redistribute.ospf.match.externals.type_1 to allow
- ios_bgp_address_family - add option redistribute.ospf.match.externals.type_2 to allow
- specification of OSPF E1 routes
- specification of OSPF E2 routes

Deprecated Features
-------------------

- ios_bgp_address_family - deprecate redistribute.ospf.match.external with redistribute.ospf.match.externals which enables attributes for OSPF type E1 and E2 routes
- ios_bgp_address_family - deprecate redistribute.ospf.match.nssa_external with redistribute.ospf.match.nssa_externals which enables attributes for OSPF type N1 and N2 routes
- ios_bgp_address_family - deprecate redistribute.ospf.match.type_1 with redistribute.ospf.match.nssa_externals.type_1
- ios_bgp_address_family - deprecate redistribute.ospf.match.type_2 with redistribute.ospf.match.nssa_externals.type_2

Bugfixes
--------

- ios_bgp_address_family - fix issue where no commands are generated when redistributing OSPFv2 and OSPFv3
- ios_bgp_address_family - fix missing negations in overridden and replaced states when redistributing OSPF
- ios_bgp_address_family - fix option and syntax for OSPF E1 and E2 routes
- ios_bgp_address_family - fix option and syntax for OSPF N1 and N2 routes
- ios_bgp_address_family - fix order of generated OSPF redistribution command options to achieve idempotency
- ios_bgp_global - fix configuration of timers under neighbor. (https://github.com/ansible-collections/cisco.ios/issues/794)
- ios_l3_interfaces - prevent configuration line generation when enable is false.
- ios_logging_global - logging history configuration command fixed for supported appliance versions.

Documentation Changes
---------------------

- Update examples for bgp_address family.
- bgp_global - Updated documentation with examples and task output.

v4.4.1
======

Bugfixes
--------

- Fix parser to read groups in snmp-server.
- Fix parser to read transceiver in snmp-server.
- ios_acls - fix processing of source information on extended acls entries.
- ios_acls - prevent rendering of mac access-lists in facts.
- ios_static_routes - fix configure generation order for ipv4 and ipv6 routes.
- ios_static_routes - fix module to be idempotent with replaced and overridden state.

Documentation Changes
---------------------

- ios_banner - Enhance example with comment.

v4.4.0
======

Minor Changes
-------------

- ios_facts - Add ip value to ansible_net_neighbors dictionary for cdp neighbours. (https://github.com/ansible-collections/cisco.ios/pull/748)
- ios_facts - Add ip value to ansible_net_neighbors dictionary for lldp neighbours. (https://github.com/ansible-collections/cisco.ios/pull/760)
- ios_interfaces - Add mode attribute in ios_interfaces, which supports layer2 and layer3 as options.

Bugfixes
--------

- ios_acls - fix rendering of object-groups in source and destination at ace level.
- ios_bgp_address_family - fix facts generation of default originate option.
- ios_bgp_global - fix neighbor shutdown command on set value being false.
- ios_command - Run & evaluate commands at least once even when retries is set to 0 (https://github.com/ansible-collections/cisco.nxos/issues/607).
- ios_ospf_interfaces - fix dead-interval rendering wrong facts when hello-multiplier is configured.

Documentation Changes
---------------------

- ospfv2 - fix documentation for ospfv2 module (networks parameter).

v4.3.1
======

Bugfixes
--------

- ios_bgp_address_family - Reorder parsers to generate correct oder of configuration lines.

v4.3.0
======

Minor Changes
-------------

- ios_route_maps - added 32-bit number support (https://github.com/ansible-collections/cisco.ios/pull/692)

Bugfixes
--------

- ios_acls - fix parsers to accept precedence value in correct format.
- ios_acls - fix precedence attribute to take a string value as input.
- ios_route_maos - fix replaced state support. (https://github.com/ansible-collections/cisco.ios/issues/680)
- ios_route_maps - fix idempotency for `set community` operations. (https://github.com/ansible-collections/cisco.ios/issues/635)
- ios_vrf - fix issue where assigning interfaces to existing vrfs doesn't work (https://github.com/ansible-collections/cisco.ios/issues/707)

v4.2.0
======

Minor Changes
-------------

- cliconf - Added support for commit confirm functionality and rollback based on timeout.
- ios_facts - default facts to show operating state data autonomous or controller mode.
- ios_l2_interfaces - more options for modes attribute added.

Bugfixes
--------

- ios_acls - fix acl commands order on replaced and overridden state.
- ios_acls - fix eq to process protocol number as protocol name.
- ios_acls - fix object group for extended acls.
- ios_l2_interfaces - fix command to remove allowed_vlans and pruning_vlans from configuration.
- ios_l2_interfaces - fix dynamic option for mode attribute.
- ios_l2_interfaces - fix state operation for existing vlans.
- ios_l3_interfaces - fix command generation on attribute value being false.
- ios_vlans - Added support for private VLAN configuration

Documentation Changes
---------------------

- ios_command - add examples for complex variables while using command module.

v4.1.0
======

Deprecated Features
-------------------

- ios_bgp_address_family - deprecate neighbors.address/tag/ipv6_adddress with neighbor_address which enables common attributes for facts rendering
- ios_bgp_address_family - deprecate neighbors.password with password_options which allows encryption and password
- ios_bgp_address_family - deprecate slow_peer with slow_peer_options which supports a dict attribute

Bugfixes
--------

- ios_bgp_address_family - aliased aggregate_address to aggregate_addresses that supports a list of dict attributes
- ios_bgp_address_family - aliased neighbor to neighbors that supports a list of dict attributes
- ios_bgp_address_family - aliased network to networks that supports a list of dict attributes
- ios_bgp_address_family - fix facts rendering with optimal parsers
- ios_bgp_address_family - fix fliter_list rendering
- ios_bgp_address_family - fix path_attribute to support float parameter
- ios_lag_interfaces - fix deleted state to delete only sub attribute values.
- ios_route_maps - fix idempotency issues with as-path prepend (https://github.com/ansible-collections/cisco.ios/issues/678)
- ios_route_maps - fix idempotency issues with set community none (https://github.com/ansible-collections/cisco.ios/issues/679
- ios_route_maps - fix merge issues with route-maps where wanted config is not deployed if route map has existing sequence numbers (https://github.com/ansible-collections/cisco.ios/issues/641)

Documentation Changes
---------------------

- ios_acls - fix documentation with proper description.

v4.0.0
======

Major Changes
-------------

- Only valid connection types for this collection is network_cli.
- This release drops support for `connection: local` and provider dictionary.

Removed Features (previously deprecated)
----------------------------------------

- ios_interface - use ios_interfaces instead.
- ios_l2_interface - use ios_l2_interfaces instead.
- ios_l3_interface - use ios_l3_interfaces instead.
- ios_static_route - use ios_static_routes instead.
- ios_vlan - use ios_vlans instead.

Bugfixes
--------

- facts - fix operstatus having a white space after value.
- ios_static_routes - fix vrf for ipv6 static routes (https://github.com/ansible-collections/cisco.ios/issues/660).

Documentation Changes
---------------------

- Update supported IOSXE version for modules.

v3.3.2
======

Bugfixes
--------

- cliconf - get_device_info now tries to exit config mode if necessary before requesting device info. (https://github.com/ansible-collections/cisco.ios/pull/654)
- prefix_lists - fix prefix list facts generation to handle empty configuration correctly.

v3.3.1
======

Bugfixes
--------

- l2_interfaces - vlan_tag options fix.
- snmp_server - add envmon options for traps.

v3.3.0
======

Minor Changes
-------------

- ios_l2_interfaces - Add vlan_name attribute to access.
- ios_l2_interfaces - Add vlan_name, vlan_tag attribute to voice.

Bugfixes
--------

- ios_acls - Fix regex to parse echo-reply command.
- ios_route_maps - Fix route maps failing on config parsed with tailing space.
- ios_snmp_server - Fix parsers for views and host + acl doc

v3.2.0
======

Minor Changes
-------------

- ios_ping - Add ipv6 options.

Bugfixes
--------

- ios_interfaces - Fix enable attribute.

v3.1.0
======

Minor Changes
-------------

- Also collect a list of serial numbers comprised in a vss system as virtual_switch_serialnums
- Fixing Detection of Virtual Switch System to facts (https://github.com/ansible-collections/cisco.ios/pull/471)
- ios_interfaces - Add purged state to ios_interfaces.

Deprecated Features
-------------------

- Deprecated ios_linkagg_module in favor of ios_lag_interfaces.

Bugfixes
--------

- ios_acl - Handle ACL config parsing when match/matches are present.
- ios_bgp_global - Parse local_as commands correctly.
- ios_interfaces - Parse interface shutdown config correctly.
- ios_lag_interfaces - Fix commands generation on action states.
- ios_lag_interfaces - Module functionality not restricted to GigabitEthernet.
- ios_logging_global - Parse monitor and buffered config correctly.
- ios_ntp - Handle regex matching server attributes gracefully.
- ios_snmp_server - Render group and views commands correctly when having common names.

v3.0.0
======

Major Changes
-------------

- Minimum required ansible.netcommon version is 2.5.1.
- Updated base plugin references to ansible.netcommon.
- facts - default value for gather_subset is changed to min instead of !config.

Bugfixes
--------

- Fix become raises error when exec prompt timestamp is configured.
- acl_interfaces - optimization and bugfixes.
- acls parser didn't only checked if the proto_options variable existed without validating that it was a dictionary before trying to use it as one.
- ios_l3_interface - config code to generate proper ordering of commands on action states.
- ios_logging_global - Added alias to render host under hosts not hostname.

v2.8.1
======

Deprecated Features
-------------------

- Deprecates lldp module.

Bugfixes
--------

- Add symlink of modules under plugins/action.
- ios_acls - Fix commands sequencing for replaced state.
- ios_acls - Fix remarks breaking idempotent behavior.
- ios_bgp_address_family - Fix multiple bgp_address_family issues. Add set option in send_community to allow backwards compatibility with older configs. Add set option in redistribute.connected to allow ospf redistribution. Fix issue with ipv6 and peer-group neighbor identification. Add ability to pull redistribute information for address families to conform to argspec. Fix issue with not pulling local_as when defined for neighbors.
- ios_facts - Fix Line protocol parser for legacy facts where state information per interface is present.
- ios_route_maps - Fix parsers for correct rendering of as_number as list.
- ios_snmp_server - Fix parsers for views facts collection.

v2.8.0
======

Minor Changes
-------------

- ios_bgp_global - Deprecate aggregate_address with aggregate_address which supports list of dict attributes.
- ios_bgp_global - Deprecate bestpath with bestpath_options which supports a dict attribute.
- ios_bgp_global - Deprecate distribute_list with distributes which supports list of dict attributes.
- ios_bgp_global - Deprecate inject_map with inject_maps which supports list of dict attributes.
- ios_bgp_global - Deprecate listen.ipv4_with_subnet/ipv6_with_subnet with host_with_subnet which enables common attribute for facts rendering.
- ios_bgp_global - Deprecate neighbors.address/tag/ipv6_adddress with neighbor_address which enables common attribute for facts rendering.
- ios_bgp_global - Deprecate neighbors.password with password_options which allows encryption and password.
- ios_bgp_global - Deprecate neighbors.route_map with route_maps which supports list of dict attributes.
- ios_bgp_global - Deprecate nopeerup_delay with nopeerup_delay_options which supports a dict attribute.
- ios_bgp_global - Deprecates route_server_context, scope, template as they were not implemented with the scope of the module.

Bugfixes
--------

- ios_bgp_global - Added bmp.server_options.
- ios_bgp_global - Added capability of configure network options.
- ios_bgp_global - Added community and local_preference for route_reflector_client.
- ios_bgp_global - Added update_source for neighbors.
- ios_bgp_global - Correct misspelled attributes with alternates/alias.
- ios_bgp_global - Facts and config code optimized for using rm_templates.
- ios_bgp_global - Parsers added for non-implemented attributes.
- ios_bgp_global - client_to_client.cluster_id corrected to take string input.
- ios_bgp_global - neighbors.path_attribute to support float format.
- ios_static_routes - Consider only config containing routes to render facts.

v2.7.2
======

Bugfixes
--------

- 'ios_acls'- filters out dynamically generated reflexive type acls.

v2.7.1
======

Release Summary
---------------

Re-releasing 2.7.0 due to Automation Hub uploading issue.

v2.7.0
======

Minor Changes
-------------

- ios_acls - Added enable_fragment attribute to enable fragments under ace.
- ios_hostname - New Resource module added.
- ios_snmp_server - Enables configuration of v3 auth and encryption password for each user.

Deprecated Features
-------------------

- ios_acls - Deprecated fragment attribute added boolean alternate as enable_fragment.

Bugfixes
--------

- ios_acls - Fixes protocol_options not rendering command properly when range is specified.
- ios_acls - Fixes standard acls getting wrongly parsed in v2.6.0
- ios_l2_interfaces - fix unable to identify FiveGigabitEthernet names on facts gathering.
- ios_snmp_server - Change key from users to views in rm template to fix failure when collecting snmp server facts from devices that have a view defined in the configuration (https://github.com/ansible-collections/cisco.ios/issues/491).
- ios_static_routes - Fixes static routes unable to identify interface names when supplied with destination attribute.
- ios_vlans - fix parsing of VLAN names with spaces.
- ios_vlans - fix parsing of VLAN ranges under remote span.

Documentation Changes
---------------------

- fixes fqcn in older module documentation.
- ios_acls - Documentation updated with commands used for fetching remarks data under aces.

New Modules
-----------

- ios_hostname - hostname resource module

v2.6.0
======

Minor Changes
-------------

- ios_acls - feature: Remarks can be configured for ACLs.
- ios_snmp_server - New Resource module added.

Bugfixes
--------

- 'ios_banner' - Bugfix for presence of multiple delimitation chars in the banner's declaration and idempotence improvement.
- Fix ntp_global - remove no_log for key_id under peer and server attributes.
- Fix ntp_global - to handle when attribute value is false.
- ios_acls - bugfixes and optimization for ACLs.
- ios_l2_interfaces - fix unable to set switchport mode properly.
- ios_logging_global - fix host ipv6 commands not parsed correctly.
- ios_logging_global - fix wrong ordering of commands fired on replaced state.

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
- Move ios_config idempotent warning message with the task response under warnings key if changed is True
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
- Requires ansible.netcommon v2.0.0+ to support ansible_network_single_user_mode and ansible_network_import_modules.

Minor Changes
-------------

- Add ios_bgp_address_family Resource Module. (https://github.com/ansible-collections/cisco.ios/pull/219).
- Adds support for single_user_mode command output caching. (https://github.com/ansible-collections/cisco.ios/pull/204).

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

- Make src, backup and backup_options in ios_config work when module alias is used (https://github.com/ansible-collections/cisco.ios/pull/107).

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
