# Cisco IOS Collection

[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.ios)
[![Codecov](https://codecov.io/gh/ansible-collections/cisco.ios/branch/main/graph/badge.svg)](https://codecov.io/gh/ansible-collections/cisco.ios)
[![CI](https://github.com/ansible-collections/cisco.ios/actions/workflows/tests.yml/badge.svg?branch=main&event=schedule)](https://github.com/ansible-collections/cisco.ios/actions/workflows/tests.yml)

The Ansible Cisco IOS collection includes a variety of Ansible content to help automate the management of Cisco IOS and Cisco IOS XE network appliances.

This collection has been tested against Cisco IOS XE Version 17.3 on CML.

## Support

As a Red Hat Ansible [Certified Content](https://catalog.redhat.com/software/search?target_platforms=Red%20Hat%20Ansible%20Automation%20Platform), this collection is entitled to [support](https://access.redhat.com/support/) through [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible) (AAP).

If a support case cannot be opened with Red Hat and the collection has been obtained either from [Galaxy](https://galaxy.ansible.com/ui/) or [GitHub](https://github.com/ansible-collections/cisco.ios), there is community support available at no charge.

You can join us on [#network:ansible.com](https://matrix.to/#/#network:ansible.com) room or the [Ansible Forum Network Working Group](https://forum.ansible.com/g/network-wg).

For more information you can check the communication section below.

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  * [Posts tagged with 'network'](https://forum.ansible.com/tag/network): subscribe to participate in collection-related conversations.
  * [Ansible Network Automation Working Group](https://forum.ansible.com/g/network-wg/): by joining the team you will automatically get subscribed to the posts tagged with [network](https://forum.ansible.com/tags/network).
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.15.0**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections

The Cisco IOS collection supports `network_cli` connections. A detailed platform guide can be found [here](https://github.com/ansible-collections/cisco.ios/blob/main/platform_guide.rst).

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[cisco.ios.ios](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_cliconf.rst)|Use ios cliconf to run command on Cisco IOS platform

### Modules
Name | Description
--- | ---
[cisco.ios.ios_acl_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_acl_interfaces_module.rst)|Resource module to configure ACL interfaces.
[cisco.ios.ios_acls](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_acls_module.rst)|Resource module to configure ACLs.
[cisco.ios.ios_banner](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_banner_module.rst)|Module to configure multiline banners.
[cisco.ios.ios_bgp_address_family](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_bgp_address_family_module.rst)|Resource module to configure BGP Address family.
[cisco.ios.ios_bgp_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_bgp_global_module.rst)|Resource module to configure BGP.
[cisco.ios.ios_command](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_command_module.rst)|Module to run commands on remote devices.
[cisco.ios.ios_config](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_config_module.rst)|Module to manage configuration sections.
[cisco.ios.ios_evpn_ethernet](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_evpn_ethernet_module.rst)|Resource module to configure L2VPN EVPN Ethernet Segment.
[cisco.ios.ios_evpn_evi](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_evpn_evi_module.rst)|Resource module to configure L2VPN EVPN EVI.
[cisco.ios.ios_evpn_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_evpn_global_module.rst)|Resource module to configure L2VPN EVPN.
[cisco.ios.ios_facts](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_facts_module.rst)|Module to collect facts from remote devices.
[cisco.ios.ios_hostname](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_hostname_module.rst)|Resource module to configure hostname.
[cisco.ios.ios_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_interfaces_module.rst)|Resource module to configure interfaces.
[cisco.ios.ios_l2_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_l2_interfaces_module.rst)|Resource module to configure L2 interfaces.
[cisco.ios.ios_l3_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_l3_interfaces_module.rst)|Resource module to configure L3 interfaces.
[cisco.ios.ios_lacp](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_lacp_module.rst)|Resource module to configure LACP.
[cisco.ios.ios_lacp_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_lacp_interfaces_module.rst)|Resource module to configure LACP interfaces.
[cisco.ios.ios_lag_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_lag_interfaces_module.rst)|Resource module to configure LAG interfaces.
[cisco.ios.ios_lldp_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_lldp_global_module.rst)|Resource module to configure LLDP.
[cisco.ios.ios_lldp_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_lldp_interfaces_module.rst)|Resource module to configure LLDP interfaces.
[cisco.ios.ios_logging_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_logging_global_module.rst)|Resource module to configure logging.
[cisco.ios.ios_ntp_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_ntp_global_module.rst)|Resource module to configure NTP.
[cisco.ios.ios_ospf_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_ospf_interfaces_module.rst)|Resource module to configure OSPF interfaces.
[cisco.ios.ios_ospfv2](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_ospfv2_module.rst)|Resource module to configure OSPFv2.
[cisco.ios.ios_ospfv3](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_ospfv3_module.rst)|Resource module to configure OSPFv3.
[cisco.ios.ios_ping](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_ping_module.rst)|Tests reachability using ping from IOS switch.
[cisco.ios.ios_prefix_lists](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_prefix_lists_module.rst)|Resource module to configure prefix lists.
[cisco.ios.ios_route_maps](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_route_maps_module.rst)|Resource module to configure route maps.
[cisco.ios.ios_service](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_service_module.rst)|Resource module to configure service.
[cisco.ios.ios_snmp_server](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_snmp_server_module.rst)|Resource module to configure snmp server.
[cisco.ios.ios_static_routes](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_static_routes_module.rst)|Resource module to configure static routes.
[cisco.ios.ios_system](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_system_module.rst)|Module to manage the system attributes.
[cisco.ios.ios_user](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_user_module.rst)|Module to manage the aggregates of local users.
[cisco.ios.ios_vlans](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vlans_module.rst)|Resource module to configure VLANs.
[cisco.ios.ios_vrf](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vrf_module.rst)|Module to configure VRF definitions.
[cisco.ios.ios_vrf_address_family](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vrf_address_family_module.rst)|Resource module to configure VRF definitions.
[cisco.ios.ios_vrf_global](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vrf_global_module.rst)|Resource module to configure global VRF definitions.
[cisco.ios.ios_vrf_interfaces](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vrf_interfaces_module.rst)|Manages VRF configuration on interfaces.
[cisco.ios.ios_vxlan_vtep](https://github.com/ansible-collections/cisco.ios/blob/main/docs/cisco.ios.ios_vxlan_vtep_module.rst)|Resource module to configure VXLAN VTEP interface.

<!--end collection content-->

## Installing this collection

You can install the Cisco IOS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cisco.ios

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cisco.ios
```

## Using this collection

This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Cisco IOS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `cisco.ios.ios_l2_interfaces`.
The following example task replaces configuration changes in the existing configuration on a Cisco IOS network device, using the FQCN:

```yaml
---
- name: Replace device configuration of specified L2 interfaces with provided configuration.
  cisco.ios.ios_l2_interfaces:
    config:
      - name: GigabitEthernet0/2
        trunk:
          - allowed_vlans: 20-25,40
            native_vlan: 20
            pruning_vlans: 10
            encapsulation: isl
    state: replaced
```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.

### See Also:

- [Cisco IOS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Cisco IOS collection repository](https://github.com/ansible-collections/cisco.ios). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- IRC - the `#ansible-network` [libera.chat](https://libera.chat/) channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

Release notes are available [here](https://github.com/ansible-collections/cisco.ios/blob/main/CHANGELOG.rst).

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
