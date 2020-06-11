

# Cisco IOS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.ios) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/cisco.ios)-->

The Ansible Cisco IOS collection includes a variety of Ansible content to help automate the management of Cisco IOS network appliances.

This collection has been tested against Cisco IOSv version 15.2 on VIRL.

### Supported connections
The Cisco IOS collection supports ``network_cli``  connections.

## Included content

<!--start collection content-->
## Cliconf plugins
Name | Description
--- | ---
[cisco.ios.ios](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios.rst)|Use ios cliconf to run command on Cisco IOS platform
## Terminal plugins
Name | Description
--- | ---
## Modules
Name | Description
--- | ---
[cisco.ios.ios_acl_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_acl_interfaces.rst)|ACL interfaces resource module
[cisco.ios.ios_acls](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_acls.rst)|ACLs resource module
[cisco.ios.ios_banner](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_banner.rst)|Manage multiline banners on Cisco IOS devices
[cisco.ios.ios_bgp](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_bgp.rst)|Configure global BGP protocol settings on Cisco IOS.
[cisco.ios.ios_command](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_command.rst)|Run commands on remote devices running Cisco IOS
[cisco.ios.ios_config](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_config.rst)|Manage Cisco IOS configuration sections
[cisco.ios.ios_facts](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_facts.rst)|Collect facts from remote devices running Cisco IOS
[cisco.ios.ios_interface](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_interface.rst)|(deprecated) Manage Interface on Cisco IOS network devices
[cisco.ios.ios_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_interfaces.rst)|Interfaces resource module
[cisco.ios.ios_l2_interface](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_l2_interface.rst)|(deprecated) Manage Layer-2 interface on Cisco IOS devices.
[cisco.ios.ios_l2_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_l2_interfaces.rst)|Layer-2 interface resource module
[cisco.ios.ios_l3_interface](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_l3_interface.rst)|(deprecated) Manage Layer-3 interfaces on Cisco IOS network devices.
[cisco.ios.ios_l3_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_l3_interfaces.rst)|Layer-3 interface resource module
[cisco.ios.ios_lacp](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lacp.rst)|LACP resource module
[cisco.ios.ios_lacp_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lacp_interfaces.rst)|LACP interfaces resource module
[cisco.ios.ios_lag_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lag_interfaces.rst)|LAG interfaces resource module
[cisco.ios.ios_linkagg](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_linkagg.rst)|Manage link aggregation groups on Cisco IOS network devices
[cisco.ios.ios_lldp](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lldp.rst)|Manage LLDP configuration on Cisco IOS network devices.
[cisco.ios.ios_lldp_global](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lldp_global.rst)|LLDP global resource module
[cisco.ios.ios_lldp_interfaces](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_lldp_interfaces.rst)|LLDP interfaces resource module
[cisco.ios.ios_logging](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_logging.rst)|Manage logging on network devices
[cisco.ios.ios_ntp](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_ntp.rst)|Manages core NTP configuration.
[cisco.ios.ios_ospfv2](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_ospfv2.rst)|OSPF_v2 resource module.
[cisco.ios.ios_ping](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_ping.rst)|Tests reachability using ping from Cisco IOS network devices
[cisco.ios.ios_static_route](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_static_route.rst)|(deprecated) Manage static IP routes on Cisco IOS network devices
[cisco.ios.ios_static_routes](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_static_routes.rst)|Static routes resource module
[cisco.ios.ios_system](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_system.rst)|Manage the system attributes on Cisco IOS devices
[cisco.ios.ios_user](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_user.rst)|Manage the aggregate of local users on Cisco IOS device
[cisco.ios.ios_vlan](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_vlan.rst)|(deprecated) Manage VLANs on IOS network devices
[cisco.ios.ios_vlans](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_vlans.rst)|VLANs resource module
[cisco.ios.ios_vrf](https://github.com/ansible-collections/cisco.ios/blob/master/docs/cisco.ios.ios_vrf.rst)|Manage the collection of VRF definitions on Cisco IOS devices
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

* [Cisco IOS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Cisco IOS collection repository](https://github.com/ansible-collections/cisco.ios). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Changelogs
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
