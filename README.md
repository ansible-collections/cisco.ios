

# Cisco IOS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.ios) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/cisco.ios)-->

The Ansible Cisco IOS collection includes a variety of Ansible content to help automate the management of Cisco IOS network appliances.

This collection has been tested against Cisco IOSv version 15.2 on VIRL.

### Supported connections
The Cisco IOS collection supports ``network_cli``  connections.

## Included content

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the Cisco IOS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cisco.ios

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cisco.ios
    version: 0.0.3
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

Alternately, you can call modules by their short name if you list the `cisco.ios` collection in the playbook's `collections`, as follows:

```yaml
---
- hosts: ios01
  gather_facts: false
  connection: network_cli

  collections:
    - cisco.ios

  tasks:
    - name: Override device configuration of all interfaces with provided configuration
      ios_l3_interfaces:
        config:
          - name: GigabitEthernet0/2
            ipv4:
            - address: 192.168.0.1/24
          - name: GigabitEthernet0/3.100
            ipv6:
            - address: autoconfig
        state: overridden
```


### See Also:

* [Cisco IOS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Cisco IOS collection repository](https://github.com/ansible-collections/cisco.ios).

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


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
