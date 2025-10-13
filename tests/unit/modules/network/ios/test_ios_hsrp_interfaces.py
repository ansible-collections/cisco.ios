#
# (c) 2021, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

import yaml

from ansible_collections.cisco.ios.plugins.modules import ios_hsrp_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosHSRPInterfaceModule(TestIosModule):
    module = ios_hsrp_interfaces

    def setUp(self):
        super(TestIosHSRPInterfaceModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.hsrp_interfaces.hsrp_interfaces."
            "Hsrp_interfacesFacts.get_hsrp_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosHSRPInterfaceModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_hsrp_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 follow MASTER_GROUP
             standby 10 timers msec 200 250
             standby 10 priority 110
             standby 10 preempt delay minimum 100 reload 50 sync 30
             standby 10 authentication md5 key-string 7 0123456789ABCDEF
             standby 10 name PRIMARY_GROUP
             standby 10 mac-address 0000.0c07.ac0a
             standby 10 track 1 decrement 20
             standby 10 track 2 shutdown
             standby 20 ipv6 2001:db8:10::1/64
             standby 20 priority 120
             standby 20 name IPV6_GROUP
             standby 20 mac-address 0000.0c07.ac14
            !
            interface Vlan100
             no ip address
             standby bfd
             standby delay minimum 100 reload 200
             standby version 2
             standby 5 ip 192.168.1.1
             standby 5 authentication hello_secret
             standby 5 name BACKUP_GROUP
             standby 5 track 10 decrement 30
            !
            interface GigabitEthernet3
             standby use-bia
             standby 1 ip 172.16.1.1
             standby 1 priority 100
            !
            interface GigabitEthernet2
             standby follow VLAN70_GROUP
             standby 2 ip 172.16.2.1 secondary
             standby 2 authentication md5 key-chain AUTH_CHAIN
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan70",
                        "delay": {"minimum": 5555, "reload": 556},
                        "mac_refresh": 45,
                        "redirect": {
                            "advertisement": {"authentication": {"key_chain": "HSRP_CHAIN"}},
                            "timers": {"adv_timer": 10, "holddown_timer": 55},
                        },
                        "version": 2,
                        "standby_groups": [
                            {
                                "group_no": 10,
                                "ip": [
                                    {"virtual_ip": "10.0.10.1"},
                                    {"virtual_ip": "10.0.10.2", "secondary": True},
                                    {"virtual_ip": "10.0.10.3", "secondary": True},
                                ],
                                "follow": "MASTER_GROUP",
                                "group_name": "PRIMARY_GROUP",
                                "authentication": {
                                    "key_string": "0123456789ABCDEF",
                                    "encryption": 7,
                                },
                                "mac_address": "0000.0c07.ac0a",
                                "preempt": {
                                    "enabled": True,
                                    "delay": True,
                                    "minimum": 100,
                                    "reload": 50,
                                    "sync": 30,
                                },
                                "priority": 110,
                                "timers": {"msec": {"hello_interval": 200}, "hold_time": 250},
                                "track": [
                                    {"track_no": 1, "decrement": 20},
                                    {"track_no": 2, "shutdown": True},
                                ],
                            },
                            {
                                "group_no": 20,
                                "ipv6": {
                                    "addresses": ["2001:db8:20::1/64", "2001:db8:10::1/64"],
                                    "autoconfig": True,
                                },
                                "follow": "MASTER_GROUP",
                                "group_name": "IPV6_GROUP",
                                "mac_address": "0000.0c07.ac14",
                                "priority": 120,
                            },
                        ],
                    },
                    {
                        "name": "Vlan100",
                        "delay": {"minimum": 100, "reload": 200},
                        "version": 2,
                        "standby_groups": [
                            {
                                "group_no": 5,
                                "ip": [{"virtual_ip": "192.168.1.1"}],
                                "authentication": {"password_text": "hello_secret"},
                                "group_name": "BACKUP_GROUP",
                                "preempt": {"enabled": True},
                                "priority": 150,
                                "timers": {"hello_interval": 5, "hold_time": 15},
                                "track": [{"track_no": 10, "decrement": 30}],
                            },
                        ],
                    },
                    {
                        "name": "GigabitEthernet3",
                        "version": 1,
                        "standby_groups": [
                            {"group_no": 1, "ip": [{"virtual_ip": "172.16.1.1"}], "priority": 100},
                        ],
                    },
                    {
                        "name": "GigabitEthernet2",
                        "version": 1,
                        "standby_groups": [
                            {
                                "group_no": 2,
                                "ip": [{"virtual_ip": "172.16.2.1", "secondary": True}],
                                "authentication": {"key_chain": "AUTH_CHAIN"},
                                "priority": 100,
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "interface Vlan70",
            "standby 10 ip 10.0.10.3 secondary",
            "standby 10 ip 10.0.10.2 secondary",
            "standby 20 follow MASTER_GROUP",
            "standby 20 ipv6 autoconfig",
            "standby 20 ipv6 2001:DB8:20::1/64",
            "interface Vlan100",
            "standby 5 preempt",
            "standby 5 priority 150",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_action_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 ip 10.0.10.2 secondary
             standby 10 ip 10.0.10.3 secondary
             standby 10 follow MASTER_GROUP
             standby 10 timers msec 200 250
             standby 10 priority 110
             standby 10 preempt delay minimum 100 reload 50 sync 30
             standby 10 authentication md5 key-string 7 0123456789ABCDEF
             standby 10 name PRIMARY_GROUP
             standby 10 mac-address 0000.0c07.ac0a
             standby 10 track 1 decrement 20
             standby 10 track 2 shutdown
             standby 20 ipv6 2001:db8:10::1/64
             standby 20 ipv6 2001:db8:20::1/64
             standby 20 ipv6 autoconfig
             standby 20 follow MASTER_GROUP
             standby 20 priority 120
             standby 20 name IPV6_GROUP
             standby 20 mac-address 0000.0c07.ac14
            !
            interface Vlan100
             no ip address
             standby bfd
             standby delay minimum 100 reload 200
             standby version 2
             standby 5 ip 192.168.1.1
             standby 5 timers 5 15
             standby 5 priority 150
             standby 5 preempt
             standby 5 authentication hello_secret
             standby 5 name BACKUP_GROUP
             standby 5 track 10 decrement 30
            !
            interface GigabitEthernet3
             standby use-bia
             standby 1 ip 172.16.1.1
             standby 1 priority 100
            !
            interface GigabitEthernet2
             standby follow VLAN70_GROUP
             standby 2 ip 172.16.2.1 secondary
             standby 2 authentication md5 key-chain AUTH_CHAIN
            """,
        )
        yaml_string = """
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
                    - '2001:db8:20::1/64'
                    - '2001:db8:10::1/64'
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
            use_bia:
              set: true
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
        """
        for action_state in ["merged", "overridden", "replaced"]:
            set_module_args(
                dict(
                    yaml.safe_load(yaml_string),
                    state=action_state,
                ),
            )
            result = self.execute_module(changed=False)
            self.assertEqual(result["commands"], [])

    def test_ios_hsrp_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 ip 10.0.10.2 secondary
             standby 10 ip 10.0.10.3 secondary
             standby 10 follow MASTER_GROUP
             standby 10 timers msec 200 250
             standby 10 priority 110
             standby 10 preempt delay minimum 100 reload 50 sync 30
             standby 10 authentication md5 key-string 7 0123456789ABCDEF
             standby 10 name PRIMARY_GROUP
             standby 10 mac-address 0000.0c07.ac0a
             standby 10 track 1 decrement 20
             standby 10 track 2 shutdown
             standby 20 ipv6 2001:db8:10::1/64
             standby 20 ipv6 2001:db8:20::1/64
             standby 20 ipv6 autoconfig
             standby 20 follow MASTER_GROUP
             standby 20 priority 120
             standby 20 name IPV6_GROUP
             standby 20 mac-address 0000.0c07.ac14
            !
            interface Vlan100
             no ip address
             standby bfd
             standby delay minimum 100 reload 200
             standby version 2
             standby 5 ip 192.168.1.1
             standby 5 timers 5 15
             standby 5 priority 150
             standby 5 preempt
             standby 5 authentication hello_secret
             standby 5 name BACKUP_GROUP
             standby 5 track 10 decrement 30
            !
            interface GigabitEthernet3
             standby use-bia
             standby 1 ip 172.16.1.1
             standby 1 priority 100
            !
            interface GigabitEthernet2
             standby follow VLAN70_GROUP
             standby 2 ip 172.16.2.1 secondary
             standby 2 authentication md5 key-chain AUTH_CHAIN
            """,
        )
        yaml_string = """
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
                    - '2001:db8:20::1/64'
                    - '2001:db8:10::1/64'
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
            use_bia:
              set: true
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
        """

        set_module_args(
            dict(
                yaml.safe_load(yaml_string),
                state="deleted",
            ),
        )
        commands = [
            "interface Vlan70",
            "no standby version 2",
            "no standby delay minimum 5555 reload 556",
            "no standby mac-refresh 45",
            "no standby redirect timers 10 55",
            "no standby redirect advertisement authentication md5 key-chain HSRP_CHAIN",
            "no standby 10",
            "no standby 20",
            "no standby version 2",
            "interface Vlan100",
            "no standby version 2",
            "no standby delay minimum 100 reload 200",
            "no standby 5",
            "no standby version 2",
            "interface GigabitEthernet3",
            "no standby version 1",
            "no standby use-bia",
            "no standby 1",
            "interface GigabitEthernet2",
            "no standby version 1",
            "no standby 2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_hsrp_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 ip 10.0.10.2 secondary
             standby 10 ip 10.0.10.3 secondary
             standby 10 follow MASTER_GROUP
             standby 10 timers msec 200 250
             standby 10 priority 110
             standby 10 preempt delay minimum 100 reload 50 sync 30
             standby 10 authentication md5 key-string 7 0123456789ABCDEF
             standby 10 name PRIMARY_GROUP
             standby 10 mac-address 0000.0c07.ac0a
             standby 10 track 1 decrement 20
             standby 10 track 2 shutdown
             standby 20 ipv6 2001:db8:10::1/64
             standby 20 ipv6 2001:db8:20::1/64
             standby 20 ipv6 autoconfig
             standby 20 follow MASTER_GROUP
             standby 20 priority 120
             standby 20 name IPV6_GROUP
             standby 20 mac-address 0000.0c07.ac14
            !
            interface Vlan100
             no ip address
             standby bfd
             standby delay minimum 100 reload 200
             standby version 2
             standby 5 ip 192.168.1.1
             standby 5 timers 5 15
             standby 5 priority 150
             standby 5 preempt
             standby 5 authentication hello_secret
             standby 5 name BACKUP_GROUP
             standby 5 track 10 decrement 30
            !
            interface GigabitEthernet3
             standby use-bia
             standby 1 ip 172.16.1.1
             standby 1 priority 100
            !
            interface GigabitEthernet2
             standby follow VLAN70_GROUP
             standby 2 ip 172.16.2.1 secondary
             standby 2 authentication md5 key-chain AUTH_CHAIN
            """,
        )
        yaml_string = """
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
                group_no: 30
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
                    - '2001:db8:30::1/64'
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
        """
        set_module_args(
            dict(
                yaml.safe_load(yaml_string),
                state="replaced",
            ),
        )
        commands = [
            "interface Vlan70",
            "standby 30 follow MASTER_GROUP",
            "standby 30 mac-address 0000.0c07.ac0a",
            "standby 30 name PRIMARY_GROUP",
            "standby 30 preempt delay minimum 100 reload 50 sync 30",
            "standby 30 priority 110",
            "standby 30 authentication md5 key-string 7 0123456789ABCDEF",
            "standby 30 ip 10.0.10.1",
            "standby 30 ip 10.0.10.2 secondary",
            "standby 30 ip 10.0.10.3 secondary",
            "standby 30 track 1 decrement 20",
            "standby 30 track 2 shutdown",
            "standby 20 ipv6 2001:DB8:30::1/64",
            "no standby 20 ipv6 2001:DB8:10::1/64",
            "no standby 20 ipv6 2001:DB8:20::1/64",
            "no standby 10",
            "interface GigabitEthernet3",
            "no standby use-bia",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 ip 10.0.10.2 secondary
             standby 10 ip 10.0.10.3 secondary
             standby 10 follow MASTER_GROUP
             standby 10 timers msec 200 250
             standby 10 priority 110
             standby 10 preempt delay minimum 100 reload 50 sync 30
             standby 10 authentication md5 key-string 7 0123456789ABCDEF
             standby 10 name PRIMARY_GROUP
             standby 10 mac-address 0000.0c07.ac0a
             standby 10 track 1 decrement 20
             standby 10 track 2 shutdown
             standby 20 ipv6 2001:db8:10::1/64
             standby 20 ipv6 2001:db8:20::1/64
             standby 20 ipv6 autoconfig
             standby 20 follow MASTER_GROUP
             standby 20 priority 120
             standby 20 name IPV6_GROUP
             standby 20 mac-address 0000.0c07.ac14
            !
            interface Vlan100
             no ip address
             standby bfd
             standby delay minimum 100 reload 200
             standby version 2
             standby 5 ip 192.168.1.1
             standby 5 timers 5 15
             standby 5 priority 150
             standby 5 preempt
             standby 5 authentication hello_secret
             standby 5 name BACKUP_GROUP
             standby 5 track 10 decrement 30
            !
            interface GigabitEthernet3
             standby use-bia
             standby 1 ip 172.16.1.1
             standby 1 priority 100
            !
            interface GigabitEthernet4
             description Test interface
            !
            """,
        )
        yaml_string = """
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
                group_no: 30
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
                    - '2001:db8:30::1/64'
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
        """
        set_module_args(
            dict(
                yaml.safe_load(yaml_string),
                state="overridden",
            ),
        )
        commands = [
            "interface GigabitEthernet3",
            "no standby version 1",
            "no standby use-bia",
            "no standby 1",
            "interface Vlan70",
            "standby 30 follow MASTER_GROUP",
            "standby 30 mac-address 0000.0c07.ac0a",
            "standby 30 name PRIMARY_GROUP",
            "standby 30 preempt delay minimum 100 reload 50 sync 30",
            "standby 30 priority 110",
            "standby 30 authentication md5 key-string 7 0123456789ABCDEF",
            "standby 30 ip 10.0.10.1",
            "standby 30 ip 10.0.10.2 secondary",
            "standby 30 ip 10.0.10.3 secondary",
            "standby 30 track 1 decrement 20",
            "standby 30 track 2 shutdown",
            "standby 20 ipv6 2001:DB8:30::1/64",
            "no standby 20 ipv6 2001:DB8:10::1/64",
            "no standby 20 ipv6 2001:DB8:20::1/64",
            "no standby 10",
            "interface GigabitEthernet2",
            "standby version 1",
            "standby 2 priority 100",
            "standby 2 authentication md5 key-chain AUTH_CHAIN",
            "standby 2 ip 172.16.2.1 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_hsrp_interfaces_parsed_rendered(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                interface Vlan70
                 no ip address
                 standby mac-refresh 45
                 standby redirect timers 10 55
                 standby delay minimum 5555 reload 556
                 standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
                 standby version 2
                 standby 10 ip 10.0.10.1
                 standby 10 follow MASTER_GROUP
                 standby 10 timers msec 200 250
                 standby 10 priority 110
                 standby 10 preempt delay minimum 100 reload 50 sync 30
                 standby 10 authentication md5 key-string 7 0123456789ABCDEF
                 standby 10 name PRIMARY_GROUP
                 standby 10 mac-address 0000.0c07.ac0a
                 standby 10 track 1 decrement 20
                 standby 20 ipv6 2001:db8:10::1/64
                 standby 20 ipv6 autoconfig
                 standby 20 follow MASTER_GROUP
                 standby 20 priority 120
                 standby 20 name IPV6_GROUP
                 standby 20 mac-address 0000.0c07.ac14
                !
                interface Vlan100
                 no ip address
                 standby bfd
                 standby delay minimum 100 reload 200
                 standby version 2
                 standby 5 ip 192.168.1.1
                 standby 5 timers 5 15
                 standby 5 priority 150
                 standby 5 preempt
                 standby 5 authentication hello_secret
                 standby 5 name BACKUP_GROUP
                 standby 5 track 10 decrement 30
                !
                interface GigabitEthernet3
                 standby use-bia
                 standby 1 ip 172.16.1.1
                 standby 1 priority 100
                !
                interface GigabitEthernet4
                 description Test interface
                !
                """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "Vlan70",
                "mac_refresh": 45,
                "redirect": {
                    "timers": {"adv_timer": 10, "holddown_timer": 55},
                    "advertisement": {"authentication": {"key_chain": "HSRP_CHAIN"}},
                },
                "delay": {"minimum": 5555, "reload": 556},
                "version": 2,
                "standby_options": [
                    {
                        "ip": [{"virtual_ip": "10.0.10.1"}],
                        "follow": "MASTER_GROUP",
                        "timers": {"hold_time": 250, "msec": {"hello_interval": 200}},
                        "priority": 110,
                        "preempt": {
                            "enabled": True,
                            "delay": True,
                            "minimum": 100,
                            "reload": 50,
                            "sync": 30,
                        },
                        "authentication": {"key_string": "0123456789ABCDEF", "encryption": 7},
                        "group_name": "PRIMARY_GROUP",
                        "mac_address": "0000.0c07.ac0a",
                        "track": [{"track_no": 1, "decrement": 20}],
                        "group_no": 10,
                    },
                    {
                        "ipv6": {"addresses": ["2001:db8:10::1/64"], "autoconfig": True},
                        "follow": "MASTER_GROUP",
                        "priority": 120,
                        "group_name": "IPV6_GROUP",
                        "mac_address": "0000.0c07.ac14",
                        "group_no": 20,
                    },
                ],
            },
            {
                "name": "Vlan100",
                "delay": {"minimum": 100, "reload": 200},
                "version": 2,
                "standby_options": [
                    {
                        "ip": [{"virtual_ip": "192.168.1.1"}],
                        "timers": {"hello_interval": 5, "hold_time": 15},
                        "priority": 150,
                        "preempt": {"enabled": True},
                        "authentication": {"password_text": "hello_secret"},
                        "group_name": "BACKUP_GROUP",
                        "track": [{"track_no": 10, "decrement": 30}],
                        "group_no": 5,
                    },
                ],
            },
            {
                "name": "GigabitEthernet3",
                "use_bia": {"set": True},
                "standby_options": [
                    {"ip": [{"virtual_ip": "172.16.1.1"}], "priority": 100, "group_no": 1},
                ],
            },
            {"name": "GigabitEthernet4"},
        ]
        self.assertEqual(parsed_list, result["parsed"])

        # Re-run module to test rendered operation
        set_module_args(
            {
                "config": parsed_list,
                "state": "rendered",
            },
        )
        commands = [
            "interface Vlan70",
            "standby version 2",
            "standby delay minimum 5555 reload 556",
            "standby mac-refresh 45",
            "standby redirect timers 10 55",
            "standby redirect advertisement authentication md5 key-chain HSRP_CHAIN",
            "standby 10 follow MASTER_GROUP",
            "standby 10 mac-address 0000.0c07.ac0a",
            "standby 10 name PRIMARY_GROUP",
            "standby 10 preempt delay minimum 100 reload 50 sync 30",
            "standby 10 priority 110",
            "standby 10 authentication md5 key-string 7 0123456789ABCDEF",
            "standby 10 ip 10.0.10.1",
            "standby 10 track 1 decrement 20",
            "standby 20 follow MASTER_GROUP",
            "standby 20 mac-address 0000.0c07.ac14",
            "standby 20 name IPV6_GROUP",
            "standby 20 priority 120",
            "standby 20 ipv6 autoconfig",
            "standby 20 ipv6 2001:DB8:10::1/64",
            "interface Vlan100",
            "standby version 2",
            "standby delay minimum 100 reload 200",
            "standby 5 name BACKUP_GROUP",
            "standby 5 preempt",
            "standby 5 priority 150",
            "standby 5 authentication hello_secret",
            "standby 5 ip 192.168.1.1",
            "standby 5 track 10 decrement 30",
            "interface GigabitEthernet3",
            "standby version 1",
            "standby use-bia scope interface",
            "standby 1 priority 100",
            "standby 1 ip 172.16.1.1",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_hsrp_interfaces_version_delete_end_create_first(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Vlan70
             no ip address
             standby mac-refresh 45
             standby redirect timers 10 55
             standby delay minimum 5555 reload 556
             standby redirect advertisement authentication md5 key-chain HSRP_CHAIN
             standby version 2
             standby 10 ip 10.0.10.1
             standby 10 ip 10.0.10.2 secondary
             standby 10 ip 10.0.10.3 secondary
             standby 10 track 1 decrement 20
             standby 20 ipv6 2001:DB8:10::1/64
             standby 20 ipv6 autoconfig
             standby 20 follow MASTER_GROUP
             standby 20 priority 120
            !
            """,
        )
        yaml_string = """
        config:
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
        """
        set_module_args(
            dict(
                yaml.safe_load(yaml_string),
                state="overridden",
            ),
        )
        commands = [
            "interface Vlan70",
            "no standby version 2",
            "no standby delay minimum 5555 reload 556",
            "no standby mac-refresh 45",
            "no standby redirect timers 10 55",
            "no standby redirect advertisement authentication md5 key-chain HSRP_CHAIN",
            "no standby 10",
            "no standby 20",
            "no standby version 2",
            "interface Vlan100",
            "standby version 2",
            "standby delay minimum 100 reload 200",
            "standby 5 name BACKUP_GROUP",
            "standby 5 preempt",
            "standby 5 priority 150",
            "standby 5 authentication hello_secret",
            "standby 5 ip 192.168.1.1",
            "standby 5 track 10 decrement 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
