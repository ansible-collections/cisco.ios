# Cisco IOS/IOS-XE Command Reference for Parser Generation

This file contains IOS CLI command structures organized by feature area.
When building a new resource module, use this reference to:
1. Identify the correct `show` command for facts gathering
2. Understand the CLI hierarchy (context command → sub-commands)
3. Write accurate `getval` regexes and `setval` Jinja2 templates in rm_templates

Full Cisco reference: https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe-17/products-command-reference-list.html

---

## Configuration Mode Hierarchy

```
Router> (User EXEC mode)
  │ enable
Router# (Privileged EXEC mode)
  │ configure terminal
Router(config)# (Global configuration mode)
  ├── interface GigabitEthernet1         → (config-if)#
  ├── router bgp 65000                   → (config-router)#
  │     └── address-family ipv4 unicast  → (config-router-af)#
  ├── router ospf 1                      → (config-router)#
  ├── router ospfv3 1                    → (config-router)#
  ├── router eigrp <name-or-asn>         → (config-router)#
  ├── router isis <tag>                  → (config-router)#
  ├── vrf definition <name>              → (config-vrf)#
  │     └── address-family ipv4/ipv6     → (config-vrf-af)#
  ├── ip access-list extended <name>     → (config-ext-nacl)#
  ├── ipv6 access-list <name>            → (config-ipv6-acl)#
  ├── route-map <name> permit/deny <seq> → (config-route-map)#
  ├── ip prefix-list <name>              → (inline, no sub-mode)
  ├── policy-map <name>                  → (config-pmap)#
  │     └── class <name>                 → (config-pmap-c)#
  ├── class-map <name>                   → (config-cmap)#
  ├── vlan <id>                          → (config-vlan)#
  ├── l2vpn evpn                         → (config-evpn)#
  ├── l2vpn evpn instance <id> vlan-based → (config-evpn-evi)#
  ├── bfd-template single-hop <name>     → (config-bfd)#
  ├── ip dhcp pool <name>                → (dhcp-config)#
  ├── crypto ikev2 proposal <name>       → (config-ikev2-proposal)#
  ├── crypto ikev2 profile <name>        → (config-ikev2-profile)#
  ├── crypto ipsec transform-set <name>  → (cfg-crypto-trans)#
  ├── crypto map <name> <seq>            → (config-crypto-map)#
  ├── snmp-server ...                    → (inline, no sub-mode)
  ├── logging ...                        → (inline, no sub-mode)
  ├── ntp ...                            → (inline, no sub-mode)
  ├── line console 0                     → (config-line)#
  └── line vty 0 4                       → (config-line)#
```

---

## Covered Features (existing modules → show commands → CLI sub-commands)

### Interfaces (`ios_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  description <text>
  shutdown / no shutdown
  speed <10|100|1000|auto>
  mtu <bytes>
  duplex <auto|full|half>
  mac-address <H.H.H>
  source template <name>
  service-policy input <name>
  service-policy output <name>
  service-policy type access-control input/output <name>
  service-policy type epbr input/output <name>
  service-policy type nwpi input/output <name>
  service-policy type packet-service input/output <name>
  service-policy type service-chain input/output <name>
  logging event trunk-status
  logging event subif-link-status
  logging event status
  logging event spanning-tree
  logging event nfas-status
  logging event bundle-status
  logging event link-status
  snmp trap ip verify drop-rate
  snmp trap link-status permit duplicates
  snmp trap mac-notification-added
  snmp trap mac-notification-removed
  snmp ifindex clear
  snmp ifindex persist
  switchport / no switchport
  ```

### L2 Interfaces (`ios_l2_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  switchport mode <access|trunk|dynamic auto|dynamic desirable|dot1q-tunnel|private-vlan>
  switchport access vlan <id>
  switchport trunk allowed vlan <vlan-list>
  switchport trunk native vlan <id>
  switchport trunk encapsulation <dot1q|isl|negotiate>
  switchport trunk pruning vlan <vlan-list>
  switchport voice vlan <id>
  switchport port-security
  switchport port-security maximum <max>
  switchport port-security violation <protect|restrict|shutdown>
  switchport port-security mac-address <H.H.H>
  switchport port-security mac-address sticky
  ```

### L3 Interfaces (`ios_l3_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  ip address <ip> <mask> [secondary]
  ip address dhcp
  ipv6 address <prefix>/<len>
  ipv6 address <prefix> link-local
  ipv6 address dhcp
  ipv6 address autoconfig
  ipv6 enable
  ip unnumbered <interface>
  ```

### VLANs (`ios_vlans`)
- **Show**: `show vlan`
- **Context**: `vlan <id>`
- **Sub-commands**:
  ```
  name <name>
  state <active|suspend>
  shutdown / no shutdown
  mtu <bytes>
  remote-span
  private-vlan <community|isolated|primary>
  private-vlan association <vlan-list>
  ```

### ACLs (`ios_acls`)
- **Show**: `show running-config | section access-list`
- **Context**: `ip access-list extended/standard <name>` or `access-list <number>`
- **Sub-commands** (extended):
  ```
  <seq> permit/deny <protocol> <source> <dest> [eq/gt/lt/neq/range <port>] [log] [dscp <value>] [fragments] [established] [time-range <name>]
  remark <text>
  ```

### ACL Interfaces (`ios_acl_interfaces`)
- **Show**: `show running-config | include ^interface|ip access-group|ipv6 traffic-filter`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  ip access-group <acl-name> <in|out>
  ipv6 traffic-filter <acl-name> <in|out>
  ```

### BGP Global (`ios_bgp_global`)
- **Show**: `show running-config | section ^router bgp`
- **Context**: `router bgp <asn>`
- **Sub-commands**:
  ```
  bgp router-id <id>
  bgp log-neighbor-changes
  bgp bestpath compare-routerid
  bgp confederation identifier <asn>
  bgp confederation peers <asn-list>
  neighbor <ip/peer-group> remote-as <asn>
  neighbor <ip> update-source <interface>
  neighbor <ip> ebgp-multihop <ttl>
  neighbor <ip> password <password>
  neighbor <ip> timers <keepalive> <holdtime>
  neighbor <ip> description <text>
  neighbor <ip> shutdown
  neighbor <ip> activate
  neighbor <ip> next-hop-self
  neighbor <ip> route-map <name> in/out
  neighbor <ip> prefix-list <name> in/out
  neighbor <ip> filter-list <name> in/out
  neighbor <ip> send-community [both|extended|standard]
  neighbor <ip> soft-reconfiguration inbound
  neighbor <ip> route-reflector-client
  redistribute <protocol> [route-map <name>] [metric <value>]
  network <prefix> mask <mask> [route-map <name>]
  timers bgp <keepalive> <holdtime>
  distance bgp <external> <internal> <local>
  ```

### BGP Address Family (`ios_bgp_address_family`)
- **Show**: `show running-config | section ^router bgp`
- **Context**: `router bgp <asn>` → `address-family <afi> <safi> [vrf <name>]`
- **AFI/SAFI combinations**:
  ```
  address-family ipv4 unicast
  address-family ipv4 multicast
  address-family ipv6 unicast
  address-family ipv6 multicast
  address-family l2vpn vpls
  address-family l2vpn evpn
  address-family vpnv4 unicast
  address-family vpnv6 unicast
  ```
- **Sub-commands** (within address-family):
  ```
  neighbor <ip> activate
  neighbor <ip> route-map <name> in/out
  neighbor <ip> prefix-list <name> in/out
  neighbor <ip> send-community [both|extended|standard]
  neighbor <ip> next-hop-self
  neighbor <ip> soft-reconfiguration inbound
  redistribute <protocol> [route-map <name>]
  network <prefix> mask <mask> [route-map <name>]
  aggregate-address <prefix> <mask> [summary-only] [as-set]
  default-information originate
  ```

### OSPFv2 (`ios_ospfv2`)
- **Show**: `show running-config | section ^router ospf`
- **Context**: `router ospf <process-id> [vrf <name>]`
- **Sub-commands**:
  ```
  router-id <id>
  network <ip> <wildcard> area <area-id>
  area <id> authentication [message-digest]
  area <id> nssa [no-summary] [default-information-originate]
  area <id> stub [no-summary]
  area <id> range <prefix> <mask> [advertise|not-advertise] [cost <cost>]
  area <id> filter-list prefix <name> in/out
  passive-interface <interface>
  passive-interface default
  default-information originate [always] [metric <value>] [metric-type <1|2>] [route-map <name>]
  redistribute <protocol> [subnets] [route-map <name>] [metric <value>] [metric-type <1|2>]
  distance <value>
  max-metric router-lsa [on-startup <seconds>] [include-stub] [summary-lsa] [external-lsa]
  auto-cost reference-bandwidth <mbps>
  timers throttle spf <delay> <initial> <max>
  log-adjacency-changes [detail]
  ```

### OSPFv3 (`ios_ospfv3`)
- **Show**: `show running-config | section ^router ospfv3`
- **Context**: `router ospfv3 <process-id>`
- **Sub-commands**:
  ```
  router-id <id>
  address-family ipv4 unicast
  address-family ipv6 unicast
  passive-interface <interface>
  auto-cost reference-bandwidth <mbps>
  ```

### OSPF Interfaces (`ios_ospf_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  ip ospf <process-id> area <area-id>
  ip ospf cost <cost>
  ip ospf priority <priority>
  ip ospf network <broadcast|non-broadcast|point-to-multipoint|point-to-point>
  ip ospf hello-interval <seconds>
  ip ospf dead-interval <seconds>
  ip ospf retransmit-interval <seconds>
  ip ospf authentication [message-digest|null]
  ip ospf authentication-key <key>
  ip ospf message-digest-key <id> md5 <key>
  ip ospf bfd
  ipv6 ospf <process-id> area <area-id>
  ipv6 ospf cost <cost>
  ipv6 ospf priority <priority>
  ipv6 ospf network <type>
  ```

### Static Routes (`ios_static_routes`)
- **Show**: `show running-config | include ip route`
- **Commands** (global config, no sub-mode):
  ```
  ip route <prefix> <mask> <next-hop-ip> [<distance>] [name <name>] [tag <tag>] [track <number>] [permanent]
  ip route <prefix> <mask> <interface> [<next-hop-ip>] [<distance>]
  ip route vrf <vrf> <prefix> <mask> <next-hop> [global]
  ipv6 route <prefix>/<len> <next-hop-ipv6> [<distance>]
  ipv6 route <prefix>/<len> <interface> [<next-hop-ipv6>]
  ipv6 route vrf <vrf> <prefix>/<len> <next-hop>
  ```

### Prefix Lists (`ios_prefix_lists`)
- **Show**: `show running-config | section ^ip prefix-list`
- **Commands** (global config, no sub-mode):
  ```
  ip prefix-list <name> description <text>
  ip prefix-list <name> seq <seq> permit/deny <prefix>/<len> [ge <value>] [le <value>]
  ipv6 prefix-list <name> description <text>
  ipv6 prefix-list <name> seq <seq> permit/deny <prefix>/<len> [ge <value>] [le <value>]
  ```

### Route Maps (`ios_route_maps`)
- **Show**: `show running-config | section ^route-map`
- **Context**: `route-map <name> permit/deny <seq>`
- **Sub-commands**:
  ```
  description <text>
  match ip address <acl-name-or-number>
  match ip address prefix-list <name>
  match ip next-hop <acl>
  match ip next-hop prefix-list <name>
  match ipv6 address prefix-list <name>
  match as-path <acl>
  match community <name> [exact-match]
  match interface <interface>
  match metric <value>
  match tag <value>
  match route-type <external|internal|level-1|level-2|local|nssa-external>
  set ip next-hop <ip>
  set ipv6 next-hop <ipv6>
  set local-preference <value>
  set metric <value>
  set metric-type <type-1|type-2|internal|external>
  set weight <value>
  set community <community> [additive]
  set as-path prepend <asn> [<asn>...]
  set origin <igp|egp|incomplete>
  set tag <value>
  continue <seq>
  ```

### LAG Interfaces (`ios_lag_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  channel-group <number> mode <active|passive|on|desirable|auto>
  channel-group <number> link <link-id>
  ```

### LACP (`ios_lacp`)
- **Show**: `show lacp sys-id`
- **Commands**:
  ```
  lacp system-priority <priority>
  ```

### LACP Interfaces (`ios_lacp_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  lacp port-priority <priority>
  lacp rate <fast|normal>
  ```

### LLDP Global (`ios_lldp_global`)
- **Show**: `show running-config | section ^lldp`
- **Commands** (global config):
  ```
  lldp run
  lldp timer <seconds>
  lldp holdtime <seconds>
  lldp reinit <seconds>
  lldp tlv-select <tlv-name>
  ```

### LLDP Interfaces (`ios_lldp_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  lldp transmit
  lldp receive
  lldp med-tlv-select <tlv>
  ```

### Logging Global (`ios_logging_global`)
- **Show**: `show running-config | include logging`
- **Commands** (global config):
  ```
  logging buffered [<size>] [<level>]
  logging console [<level>]
  logging monitor [<level>]
  logging host <ip> [transport <udp|tcp> port <port>] [vrf <vrf>]
  logging trap <level>
  logging facility <facility>
  logging source-interface <interface>
  logging on
  logging origin-id <hostname|ip|string <text>>
  logging discriminator <name> <facility|mnemonics|msg-body|severity> <drops|includes> <regex>
  ```

### NTP Global (`ios_ntp_global`)
- **Show**: `show running-config | section ^ntp`
- **Commands** (global config):
  ```
  ntp server <ip> [key <key-id>] [prefer] [source <interface>] [vrf <vrf>]
  ntp peer <ip> [key <key-id>] [prefer] [source <interface>]
  ntp source <interface>
  ntp access-group <peer|serve|serve-only|query-only> <acl>
  ntp authenticate
  ntp authentication-key <key-id> md5 <key>
  ntp trusted-key <key-id>
  ntp master [<stratum>]
  ntp update-calendar
  ```

### SNMP Server (`ios_snmp_server`)
- **Show**: `show running-config | section ^snmp-server`
- **Commands** (global config):
  ```
  snmp-server community <string> <RO|RW> [<acl>] [view <view>]
  snmp-server host <ip> [version <1|2c|3> [auth|noauth|priv]] <community> [udp-port <port>]
  snmp-server view <name> <oid-tree> <included|excluded>
  snmp-server group <name> <v1|v2c|v3> [auth|noauth|priv] [read <view>] [write <view>] [notify <view>] [access <acl>]
  snmp-server user <name> <group> <v1|v2c|v3> [auth <md5|sha> <auth-pass>] [priv <des|3des|aes 128|192|256> <priv-pass>]
  snmp-server location <text>
  snmp-server contact <text>
  snmp-server chassis-id <text>
  snmp-server enable traps [<trap-type>]
  snmp-server source-interface traps <interface>
  ```

### Hostname (`ios_hostname`)
- **Show**: `show running-config | include hostname`
- **Commands**: `hostname <name>`

### Service (`ios_service`)
- **Show**: `show running-config | include ^service`
- **Commands** (global config):
  ```
  service timestamps debug datetime [msec] [localtime] [show-timezone] [year]
  service timestamps log datetime [msec] [localtime] [show-timezone] [year]
  service password-encryption
  service tcp-keepalives-in
  service tcp-keepalives-out
  service pad
  service dhcp
  service config
  service compress-config
  service sequence-numbers
  service call-home
  ```

### VRF Global (`ios_vrf_global`)
- **Show**: `show running-config | section ^vrf definition`
- **Context**: `vrf definition <name>`
- **Sub-commands**:
  ```
  description <text>
  rd <asn:nn | ip:nn>
  route-target export <rt>
  route-target import <rt>
  route-target both <rt>
  ```

### VRF Address Family (`ios_vrf_address_family`)
- **Show**: `show running-config | section ^vrf definition`
- **Context**: `vrf definition <name>` → `address-family <ipv4|ipv6>`
- **Sub-commands**:
  ```
  route-target export <rt>
  route-target import <rt>
  route-target both <rt>
  ```

### VRF Interfaces (`ios_vrf_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**: `vrf forwarding <vrf-name>`

### VXLAN VTEP (`ios_vxlan_vtep`)
- **Show**: `show running-config | section ^interface nve`
- **Context**: `interface nve <id>`
- **Sub-commands**:
  ```
  source-interface <interface>
  host-reachability protocol bgp
  member vni <id> [mcast-group <ip>] [ingress-replication]
  member vni <id> vrf <name>
  ```

### EVPN Global (`ios_evpn_global`)
- **Show**: `show running-config | section ^l2vpn evpn`
- **Context**: `l2vpn evpn`
- **Sub-commands**:
  ```
  replication-type <ingress|static>
  router-id <interface>
  default-gateway advertise
  flooding-suppression address-resolution disable
  ip local-learning disable
  ```

### EVPN EVI (`ios_evpn_evi`)
- **Show**: `show running-config | section ^l2vpn evpn instance`
- **Context**: `l2vpn evpn instance <id> vlan-based`
- **Sub-commands**:
  ```
  encapsulation vxlan
  rd <rd-value>
  route-target export <rt>
  route-target import <rt>
  route-target both <rt>
  replication-type <ingress|static>
  ```

### EVPN Ethernet Segment (`ios_evpn_ethernet`)
- **Show**: `show running-config | section ^l2vpn evpn ethernet-segment`
- **Context**: `l2vpn evpn ethernet-segment <id>`
- **Sub-commands**:
  ```
  identifier type <0|3> <system-mac> <local-discriminator>
  redundancy <all-active|single-active>
  df-election wait-time <seconds>
  ```

### HSRP Interfaces (`ios_hsrp_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  standby <group> ip <ip>
  standby <group> priority <priority>
  standby <group> preempt [delay minimum <seconds>]
  standby <group> timers <hello> <hold>
  standby <group> authentication [md5 key-string <key>] [text <string>]
  standby <group> track <object-id> [decrement <value>]
  standby <group> name <name>
  standby version <1|2>
  ```

### BFD Interfaces (`ios_bfd_interfaces`)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  bfd interval <msec> min_rx <msec> multiplier <value>
  bfd template <name>
  bfd echo
  ```

### BFD Templates (`ios_bfd_templates`)
- **Show**: `show running-config | section ^bfd-template`
- **Context**: `bfd-template single-hop <name>` or `bfd-template multi-hop <name>`
- **Sub-commands**:
  ```
  interval min-tx <msec> min-rx <msec> multiplier <value>
  echo
  dampening <half-life> <reuse> <suppress> <max-suppress>
  authentication <sha-1|md5> keychain <name>
  ```

### Banner (`ios_banner`)
- **Show**: `show running-config | section banner`
- **Commands**:
  ```
  banner motd <delimiter><text><delimiter>
  banner login <delimiter><text><delimiter>
  banner exec <delimiter><text><delimiter>
  banner incoming <delimiter><text><delimiter>
  ```

### User (`ios_user`)
- **Show**: `show running-config | section ^username`
- **Commands**:
  ```
  username <name> privilege <level>
  username <name> password <type> <password>
  username <name> secret <type> <secret>
  username <name> view <view>
  username <name> sshkey <key>
  username <name> nopassword
  ```

---

## Uncovered Features (no module yet — CLI reference for future development)

### AAA (`ios_aaa` — not yet implemented)
- **Show**: `show running-config | section ^aaa`
- **Commands** (global config):
  ```
  aaa new-model
  aaa authentication login <list-name> <method1> [<method2>...]
    methods: local, enable, group <name>, line, none
  aaa authentication enable default <method1> [<method2>...]
  aaa authorization exec <list-name> <method1> [<method2>...]
  aaa authorization commands <level> <list-name> <method1>
  aaa authorization network <list-name> <method1>
  aaa accounting exec <list-name> start-stop <method1>
  aaa accounting commands <level> <list-name> start-stop <method1>
  aaa accounting network <list-name> start-stop <method1>
  aaa session-id common
  ```

### RADIUS Server (`ios_radius_server` — not yet implemented)
- **Show**: `show running-config | section ^radius server`
- **Context**: `radius server <name>`
- **Sub-commands**:
  ```
  address ipv4 <ip> auth-port <port> acct-port <port>
  key <key>
  timeout <seconds>
  retransmit <count>
  ```

### TACACS Server (`ios_tacacs_server` — not yet implemented)
- **Show**: `show running-config | section ^tacacs server`
- **Context**: `tacacs server <name>`
- **Sub-commands**:
  ```
  address ipv4 <ip>
  key <key>
  port <port>
  timeout <seconds>
  ```

### Crypto IKEv2 (`ios_crypto_ikev2` — not yet implemented)
- **Show**: `show running-config | section ^crypto ikev2`
- **Context**: `crypto ikev2 proposal <name>`
- **Sub-commands**:
  ```
  encryption <aes-cbc-128|aes-cbc-256|aes-gcm-128|aes-gcm-256>
  integrity <sha1|sha256|sha384|sha512>
  group <1|2|5|14|15|16|19|20|21|24>
  ```
- **Context**: `crypto ikev2 policy <name>`
- **Sub-commands**:
  ```
  proposal <name>
  match fvrf <vrf>
  match address local <ip>
  ```
- **Context**: `crypto ikev2 profile <name>`
- **Sub-commands**:
  ```
  match identity remote address <ip> <mask>
  match identity remote fqdn domain <domain>
  authentication remote pre-share [key <key>]
  authentication local pre-share [key <key>]
  keyring local <name>
  dpd <interval> <retry> <on-demand|periodic>
  ```

### Crypto IPsec (`ios_crypto_ipsec` — not yet implemented)
- **Show**: `show running-config | section ^crypto ipsec`
- **Context**: `crypto ipsec transform-set <name> <transform1> [<transform2>...]`
- **Sub-commands**: `mode <tunnel|transport>`
- **Context**: `crypto ipsec profile <name>`
- **Sub-commands**:
  ```
  set transform-set <name>
  set ikev2-profile <name>
  set pfs <group>
  set security-association lifetime seconds <seconds>
  ```

### QoS Policy Map (`ios_qos_policy_map` — not yet implemented)
- **Show**: `show running-config | section ^policy-map`
- **Context**: `policy-map <name>`
- **Sub-commands**:
  ```
  class <class-name>
    police <bps> <burst-normal> <burst-max> conform-action <action> exceed-action <action> violate-action <action>
    police cir <bps> bc <bytes> [pir <bps> be <bytes>]
    shape average <bps> [<burst>]
    bandwidth <kbps>
    bandwidth percent <percent>
    bandwidth remaining percent <percent>
    priority [<kbps>] [level <1|2>]
    queue-limit <packets>
    random-detect
    set dscp <value>
    set cos <value>
    set precedence <value>
    service-policy <child-policy>
  ```

### QoS Class Map (`ios_qos_class_map` — not yet implemented)
- **Show**: `show running-config | section ^class-map`
- **Context**: `class-map [match-all|match-any] <name>`
- **Sub-commands**:
  ```
  match access-group <acl-number-or-name>
  match dscp <value> [<value>...]
  match cos <value> [<value>...]
  match precedence <value> [<value>...]
  match protocol <protocol>
  match ip rtp <start-port> <port-range>
  match input-interface <interface>
  match vlan <vlan-id>
  match class-map <name>
  description <text>
  ```

### MPLS (`ios_mpls` — not yet implemented)
- **Show**: `show running-config | include mpls`
- **Commands** (global config):
  ```
  mpls ip
  mpls label protocol <ldp|tdp>
  mpls ldp router-id <interface> [force]
  mpls ldp neighbor <ip> password <password>
  mpls ldp session protection [duration <seconds>]
  mpls traffic-eng tunnels
  ```
- **Interface sub-commands**:
  ```
  mpls ip
  mpls traffic-eng tunnels
  ```

### Multicast / PIM (`ios_multicast` — not yet implemented)
- **Show**: `show running-config | include multicast|ip pim|ip igmp`
- **Commands** (global config):
  ```
  ip multicast-routing [distributed]
  ip multicast-routing vrf <vrf>
  ip pim rp-address <ip> [<acl>] [override]
  ip pim bsr-candidate <interface> [<hash-mask-length>] [<priority>]
  ip pim rp-candidate <interface> [group-list <acl>]
  ip pim spt-threshold <kbps> [group-list <acl>]
  ip pim ssm range <acl>
  ```
- **Interface sub-commands**:
  ```
  ip pim sparse-mode
  ip pim dense-mode
  ip pim sparse-dense-mode
  ip igmp join-group <group>
  ip igmp version <2|3>
  ip igmp snooping
  ```

### DHCP (`ios_dhcp` — not yet implemented)
- **Show**: `show running-config | section ^ip dhcp`
- **Context**: `ip dhcp pool <name>`
- **Sub-commands**:
  ```
  network <ip> <mask>
  network <ip> /<prefix-length>
  default-router <ip> [<ip>...]
  dns-server <ip> [<ip>...]
  domain-name <name>
  lease <days> [<hours> [<minutes>]]
  lease infinite
  option <code> <value>
  class <name>
  ```
- **Global commands**:
  ```
  ip dhcp excluded-address <start-ip> [<end-ip>]
  ip dhcp snooping
  ip dhcp snooping vlan <vlan-list>
  ip dhcp snooping information option
  ```

### NAT (`ios_nat` — not yet implemented)
- **Show**: `show running-config | include ip nat`
- **Commands** (global config):
  ```
  ip nat inside source list <acl> interface <interface> overload
  ip nat inside source list <acl> pool <pool-name> [overload]
  ip nat inside source static <local-ip> <global-ip>
  ip nat inside source static tcp <local-ip> <local-port> <global-ip> <global-port>
  ip nat pool <name> <start-ip> <end-ip> netmask <mask>
  ip nat pool <name> <start-ip> <end-ip> prefix-length <length>
  ```
- **Interface sub-commands**:
  ```
  ip nat inside
  ip nat outside
  ```

### Spanning Tree (`ios_stp` — not yet implemented)
- **Show**: `show running-config | include spanning-tree`
- **Commands** (global config):
  ```
  spanning-tree mode <pvst|rapid-pvst|mst>
  spanning-tree vlan <vlan-list> priority <priority>
  spanning-tree vlan <vlan-list> root primary [diameter <dia>]
  spanning-tree vlan <vlan-list> root secondary
  spanning-tree portfast default
  spanning-tree portfast bpduguard default
  spanning-tree etherchannel guard misconfig
  spanning-tree extend system-id
  spanning-tree loopguard default
  spanning-tree mst configuration
    name <name>
    revision <number>
    instance <id> vlan <vlan-list>
  spanning-tree mst <instance> priority <priority>
  ```
- **Interface sub-commands**:
  ```
  spanning-tree portfast [trunk]
  spanning-tree bpduguard enable
  spanning-tree guard root
  spanning-tree link-type <point-to-point|shared>
  spanning-tree cost <cost>
  spanning-tree port-priority <priority>
  spanning-tree vlan <vlan-list> cost <cost>
  ```

### Line (`ios_line` — not yet implemented)
- **Show**: `show running-config | section ^line`
- **Context**: `line console <number>` or `line vty <start> <end>` or `line aux <number>`
- **Sub-commands**:
  ```
  transport input <all|none|ssh|telnet>
  transport output <all|none|ssh|telnet>
  login [local|authentication <list>]
  password <password>
  exec-timeout <minutes> [<seconds>]
  privilege level <level>
  logging synchronous
  history size <size>
  length <lines>
  width <columns>
  access-class <acl> <in|out> [vrf-also]
  authorization exec <list>
  accounting exec <list>
  stopbits <1|1.5|2>
  speed <bps>
  ```

### EIGRP (`ios_eigrp` — not yet implemented)
- **Show**: `show running-config | section ^router eigrp`
- **Context**: `router eigrp <asn>` (classic) or `router eigrp <name>` (named mode)
- **Sub-commands** (classic):
  ```
  network <ip> [<wildcard>]
  no auto-summary
  passive-interface <interface>
  passive-interface default
  redistribute <protocol> [route-map <name>] [metric <bw> <delay> <reliability> <load> <mtu>]
  eigrp router-id <id>
  variance <multiplier>
  distance eigrp <internal> <external>
  ```
- **Named mode context**: `router eigrp <name>` → `address-family ipv4/ipv6 autonomous-system <asn>`

### IS-IS (`ios_isis` — not yet implemented)
- **Show**: `show running-config | section ^router isis`
- **Context**: `router isis [<tag>]`
- **Sub-commands**:
  ```
  net <net-address>
  is-type <level-1|level-1-2|level-2-only>
  metric-style <narrow|transition|wide> [level-1|level-2]
  passive-interface <interface>
  redistribute <protocol> [route-map <name>] [metric <value>] [level-1|level-2]
  address-family ipv6
    redistribute <protocol>
  ```
- **Interface sub-commands**:
  ```
  ip router isis [<tag>]
  ipv6 router isis [<tag>]
  isis circuit-type <level-1|level-1-2|level-2-only>
  isis metric <value> [level-1|level-2]
  isis network point-to-point
  ```

### VRRP (`ios_vrrp` — not yet implemented)
- **Show**: `show running-config | section ^interface`
- **Context**: `interface <type><number>`
- **Sub-commands**:
  ```
  vrrp <group> address-family <ipv4|ipv6>
    address <ip> [primary|secondary]
    priority <priority>
    preempt [delay minimum <seconds>]
    timers advertise <msec>
    track <object-id> decrement <value>
    vrrs leader <name>
  ```

### 802.1X / Identity (`ios_dot1x` — not yet implemented)
- **Show**: `show running-config | include dot1x|authentication`
- **Commands** (global config):
  ```
  dot1x system-auth-control
  dot1x critical eapol
  ```
- **Interface sub-commands**:
  ```
  authentication port-control <auto|force-authorized|force-unauthorized>
  authentication order <dot1x|mab|webauth> [<method>...]
  authentication priority <dot1x|mab|webauth> [<method>...]
  authentication event fail action <authorize vlan <id>|next-method>
  authentication host-mode <single-host|multi-auth|multi-domain|multi-host>
  authentication open
  authentication periodic
  authentication timer reauthenticate <seconds>
  dot1x pae authenticator
  dot1x timeout tx-period <seconds>
  mab
  mab eap
  ```

---

## Parser Generation Guide

When creating a new parser from these commands, follow this pattern:

### Step 1: Identify the context command
The context command creates a new entry in the parsed data. It uses `"shared": True`.
```python
{
    "name": "<context>",  # e.g., "interface", "router_bgp", "vrf_definition"
    "getval": re.compile(r'''^<context-regex>\s(?P<name>\S+)$''', re.VERBOSE),
    "setval": "<context-cli> {{ name }}",
    "result": {
        "{{ name }}": {
            "name": "{{ name }}",
        },
    },
    "shared": True,
}
```

### Step 2: Create parsers for each sub-command
Each sub-command gets its own parser entry. Match indented lines with `\s+` prefix.
```python
{
    "name": "<attribute>",
    "getval": re.compile(r'''
        \s+<cli-keyword>
        \s(?P<value>\S+)
        $''', re.VERBOSE),
    "setval": "<cli-keyword> {{ <attribute> }}",
    "result": {
        "{{ name }}": {
            "<attribute>": "{{ value }}",
        },
    },
}
```

### Step 3: Handle boolean/negatable commands
Commands like `shutdown`/`no shutdown`:
```python
{
    "name": "enabled",
    "getval": re.compile(r'''
        (?P<negate>\sno)?
        (?P<shutdown>\sshutdown)
        $''', re.VERBOSE),
    "setval": "shutdown",
    "result": {
        "{{ name }}": {
            "enabled": "{{ False if shutdown is defined and negate is not defined else True }}",
        },
    },
}
```

### Step 4: Handle commands with multiple options
```python
{
    "name": "some_feature",
    "getval": re.compile(r'''
        \s+some-feature
        (\s(?P<opt1>option1))?
        (\s(?P<opt2>option2))?
        (\s(?P<value>\S+))?
        $''', re.VERBOSE),
    "setval": "some-feature"
              "{{ ' option1' if some_feature.opt1 is defined else '' }}"
              "{{ ' option2' if some_feature.opt2 is defined else '' }}"
              "{{ ' ' ~ some_feature.value if some_feature.value is defined else '' }}",
    "result": {
        "{{ name }}": {
            "some_feature": {
                "opt1": "{{ not not opt1 }}",
                "opt2": "{{ not not opt2 }}",
                "value": "{{ value }}",
            },
        },
    },
}
```

### Step 5: Handle nested contexts (e.g., address-family under router bgp)
For commands within sub-contexts, the result structure nests deeper:
```python
{
    "name": "address_family",
    "getval": re.compile(r'''
        \s+address-family
        \s(?P<afi>ipv4|ipv6)
        (\s(?P<safi>unicast|multicast))?
        $''', re.VERBOSE),
    "setval": "address-family {{ afi }}{{ ' ' ~ safi if safi is defined else '' }}",
    "result": {
        "address_families": {
            "{{ afi }}_{{ safi|default('unicast') }}": {
                "afi": "{{ afi }}",
                "safi": "{{ safi|default('unicast') }}",
            },
        },
    },
    "shared": True,
}
```
