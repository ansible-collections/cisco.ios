# **cisshgo Integration with Molecule**

The first milestone is local validation of `ios_interfaces` against the CML device in `inventory.ini`,
followed by Molecule scenarios that run with cisshgo.

## **1\. Molecule Local Validation (CML Devices)**

Run from:

```shell
cd /Users/yourusername/dev-workspace/ansible-dev/ansible_collections/cisco/ios/extensions
```

Run scenario:

```shell
molecule converge -s bootstrap_local_cml
molecule verify -s bootstrap_local_cml
```

Or full scenario:

```shell
molecule test -s bootstrap_local_cml
```

### **1.1 Molecule Scenario Layout**

Scenario path:

`ansible_collections/cisco/ios/extensions/molecule/bootstrap_local_cml/`

Scenario files:

`molecule.yml` defines scenario name and test sequence (`converge`, `verify`) and points Ansible to `inventory.ini`. `converge.yml` contains the merged `ios_interfaces` flow (remove config, merge, assertions, idempotence). `verify.yml` contains the connectivity/assertion check using `cisco.ios.ios_command`.

Supporting files reused by converge:

`vars.yaml` `_remove_config.yaml` `inventory.ini`

### **1.2 File Contents (Current)**

File: `ansible_collections/cisco/ios/extensions/molecule/bootstrap_local_cml/molecule.yml`

```
---
ansible:
  executor:
    args:
      ansible_playbook:
        - --inventory=${MOLECULE_SCENARIO_DIRECTORY}/../../../../../../inventory.ini
  env:
    ANSIBLE_FORCE_COLOR: "true"
    ANSIBLE_HOST_KEY_CHECKING: "false"
    ANSIBLE_DEPRECATION_WARNINGS: "false"

scenario:
  name: bootstrap_local_cml
  test_sequence:
    - converge
    - verify
```

File: `ansible_collections/cisco/ios/extensions/molecule/bootstrap_local_cml/converge.yml`

```
---
- name: Merged ios_interfaces state for integration tests
  hosts: ios
  gather_facts: false
  vars_files:
    - ../../../../../../vars.yaml
  tasks:
    - name: Debug start
      ansible.builtin.debug:
        msg: START Merged ios_interfaces state for integration tests on connection={{ ansible_connection }}

    - ansible.builtin.include_tasks: ../../../../../../_remove_config.yaml

    - block:
        - name: Merge provided configuration with device configuration
          register: result
          cisco.ios.ios_interfaces: &id001
            config:
              - name: GigabitEthernet0/1
                description: Configured and Merged by Ansible-Network
                enabled: true
              - name: GigabitEthernet0/2
                description: 04j
                enabled: false
            state: merged

        - name: Assert that correct set of commands were generated
          ansible.builtin.assert:
            that:
              - merged['commands'] | symmetric_difference(result['commands']) | length == 0

        - name: Assert that before dicts are correctly generated
          ansible.builtin.assert:
            that:
              - merged['before'] | symmetric_difference(result['before']) | length == 0

        - name: Assert that after dict is correctly generated
          ansible.builtin.assert:
            that:
              - merged['after'] | symmetric_difference(result['after']) | length == 0

        - name: Merge provided configuration with device configuration (idempotent)
          register: result
          cisco.ios.ios_interfaces: *id001

        - name: Assert that the previous task was idempotent
          ansible.builtin.assert:
            that:
              - result['changed'] == false
      always:
        - ansible.builtin.include_tasks: ../../../../../../_remove_config.yaml
```

File: `ansible_collections/cisco/ios/extensions/molecule/bootstrap_local_cml/verify.yml`

```
---
- name: Verify CML device is reachable after ios_interfaces run
  hosts: ios
  gather_facts: false
  tasks:
    - name: Run show privilege
      register: privilege_out
      cisco.ios.ios_command:
        commands:
          - show privilege

    - name: Assert show privilege returned output
      ansible.builtin.assert:
        that:
          - privilege_out.stdout is defined
          - privilege_out.stdout | length > 0
          - privilege_out.stdout[0] | length > 0
```

File: `inventory.ini`

```
[ios]
ios_device ansible_host=54.190.208.146
[ios:vars]
ansible_network_os=cisco.ios.ios
ansible_ssh_user=admin
ansible_ssh_pass=admin123
ansible_connection=ansible.netcommon.network_cli
ansible_network_cli_ssh_type=libssh
ansible_become=true
ansible_ssh_port=2033
ansible_become_password=cisco
ansible_network_import_modules=True
ansible_command_timeout=200
ansible_libssh_key_exchange_algorithms=+diffie-hellman-group14-sha1,+diffie-hellman-group-exchange-sha1
ansible_libssh_hostkeys=+ssh-rsa
ansible_libssh_publickey_algorithms=+ssh-rsa
```

File: `ansible_collections/cisco/ios/extensions/ansible.cfg`

```
[defaults]
collections_path= /Users/yourusername/dev-workspace/ansible-dev/ansible_collections
host_key_checking = False
no_log = False

[persistent_connection]
# Keep persistent connections alive for network devices
connect_timeout = 3600
command_timeout = 3600

[libssh_connection]
key_exchange_algorithms = +diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1
publickey_accepted_algorithms = +ssh-rsa
hostkeys = +ssh-rsa
```

### **1.3 What Files Molecule Needs (This Setup)**

For pre-existing infrastructure like local CML:

`molecule.yml` `converge.yml` `verify.yml`

`create.yml` / `destroy.yml` are optional in this model.

### **1.4 Local Config Used**

Inventory (`inventory.ini`)

Network connection is `ansible.netcommon.network_cli`. SSH type is `libssh`. Host credentials and port are defined in the same file. Libssh compatibility vars used are `ansible_libssh_key_exchange_algorithms`, `ansible_libssh_hostkeys`, and `ansible_libssh_publickey_algorithms`.

Ansible Config (`extensions/ansible.cfg`)

Collection path configuration. Host key checking behavior. Persistent connection timeout settings. `[libssh_connection]` settings.

### **1.5 Validation Commands**

Check effective ansible config:

```shell
ansible-config dump --only-changed
```

Check host vars from inventory:

```shell
ansible-inventory -i /Users/yourusername/dev-workspace/ansible-dev/inventory.ini --host ios_device
```

Run Molecule with debug:

```shell
molecule --debug converge -s bootstrap_local_cml
```

### **1.6 Sample Successful Run Output (`molecule converge -s bootstrap_local_cml`)**

```
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
CRITICAL 'molecule/default/molecule.yml' glob failed.  Exiting.
INFO     default scenario not found, disabling shared state.
INFO     bootstrap_local_cml ➜ discovery: scenario test matrix: dependency, create, prepare, converge
INFO     bootstrap_local_cml ➜ prerun: Performing prerun with role_name_check=0...
INFO     bootstrap_local_cml ➜ dependency: Executing
WARNING  bootstrap_local_cml ➜ dependency: Missing roles requirements file: requirements.yml
WARNING  bootstrap_local_cml ➜ dependency: Missing collections requirements file: collections.yml
WARNING  bootstrap_local_cml ➜ dependency: Executed: 2 missing (Remove from converge_sequence to suppress)
INFO     bootstrap_local_cml ➜ create: Executing
WARNING  bootstrap_local_cml ➜ create: Skipping, instances already created.
INFO     bootstrap_local_cml ➜ create: Executed: Skipped (Skipping, instances already created.)
INFO     bootstrap_local_cml ➜ prepare: Executing
WARNING  bootstrap_local_cml ➜ prepare: Executed: Missing playbook (Remove from converge_sequence to suppress)
INFO     bootstrap_local_cml ➜ converge: Executing
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [Merged ios_interfaces state for integration tests] ***********************

TASK [Debug start] *************************************************************
ok: [ios_device] => {
    "msg": "START Merged ios_interfaces state for integration tests on connection=ansible.netcommon.network_cli"
}

TASK [ansible.builtin.include_tasks] *******************************************
included: /Users/yourusername/dev-workspace/ansible-dev/_remove_config.yaml for ios_device

TASK [Remove configuration] ****************************************************
[WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device including the indentation
[WARNING]: Task result `warnings` was <class 'str'> instead of <class 'list'>.
changed: [ios_device]

TASK [Merge provided configuration with device configuration] ******************
changed: [ios_device]

TASK [Assert that correct set of commands were generated] **********************
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Assert that before dicts are correctly generated] ************************
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Assert that after dict is correctly generated] ***************************
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Merge provided configuration with device configuration (idempotent)] *****
ok: [ios_device]

TASK [Assert that the previous task was idempotent] ****************************
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ansible.builtin.include_tasks] *******************************************
included: /Users/yourusername/dev-workspace/ansible-dev/_remove_config.yaml for ios_device

TASK [Remove configuration] ****************************************************
changed: [ios_device]

PLAY RECAP *********************************************************************
ios_device                 : ok=11   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     bootstrap_local_cml ➜ converge: Executed: Successful
```

## **2\. cisshgo \+ Molecule Usage**

This section explains exactly how the `cisshgo_ios_interfaces` Molecule scenario works, what every file does, and how execution flows from startup to cleanup.

### **2.1 Local Prerequisites and Why They Matter**

Run from:

```shell
cd /Users/yourusername/dev-workspace/ansible-dev/ansible_collections/cisco/ios/extensions
```

Required tools/components:

`molecule` orchestrates lifecycle stages (`create`, `converge`, `verify`, `destroy`).

`ansible` executes the playbooks for those lifecycle stages.

`cisco.ios` provides `ios_interfaces`.

`ansible.netcommon` provides `network_cli` \+ libssh transport.

`cisshgo` runs local SSH listeners and replays transcript responses.

### **2.2 Environment Variables**

```shell
export CISSHGO_BIN_PATH=/Users/piyushmalik/dev-workspace/cisshgo_0.2.0_darwin_arm64/cisshgo/cisshgo
export CISSHGO_PORT=10000
```

Optional (only if you want create.yml to build from source):

```shell
export CISSHGO_REPO_PATH=/Users/yourusername/dev-workspace/cisshgo
```

### **2.3 Full Scenario Directory Structure**

```
ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/
├── molecule.yml
├── inventory/
    └── hosts.yml
├── create.yml
├── converge.yml
├── verify.yml
├── destroy.yml
└── cisshgo_fixtures/
    ├── cisshgo_inventory.yaml
    ├── transcript_map.yaml
    └── transcripts/
        ├── generic_empty_return.txt
        ├── cisco/
        │   └── ios/
        │       ├── show_privilege.txt
        │       ├── show_version.txt
        │       ├── show_running-config.txt
        │       └── show_running-config_section_interface_gathered.txt
        └── scenarios/
            ├── ios-interfaces-merged/
            │   ├── before.txt
            │   └── after.txt
            └── ios-interfaces-replaced/
                ├── before.txt
                └── after.txt
```

### **2.4 End-to-End Execution Flow**

1. `molecule test -s cisshgo_ios_interfaces` starts and reads `molecule.yml`.(Ansible inventory is linked from `inventory/hosts.yml`).
2. `create.yml` resolves binary path, starts `cisshgo`, and opens three listeners:
   * `10000` platform mode (`gathered`, and shared commands)
   * `10001` scenario mode (`merged`)
   * `10002` scenario mode (`replaced`)
3. `converge.yml` runs five functional plays:
   * `gathered` (network online)
   * `merged` (network online \+ idempotence)
   * `replaced` (network online \+ idempotence)
   * `parsed` (offline, no SSH needed)
   * `rendered` (offline, no SSH needed)
4. `verify.yml` reads `.cisshgo.log` and asserts no `Unknown command`.
5. `destroy.yml` kills cisshgo process and cleans PID/log files.

How transcript dispatch works:

* If a host is tied to a `scenario`, cisshgo first consumes commands from `scenarios.<name>.sequence`.
* If no scenario match exists, command falls back to `platforms.ios.command_transcripts`.
* Prompt transitions (enter/exit config modes) are driven by `context_search`, `context_hierarchy`, and `end_context`.

###

### **2.5 Files and Full Content (Inline at First Mention)**

Main scenario definition:

**File:** `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/molecule.yml`

```
---
dependency:
  name: galaxy

driver:
  name: default
  options:
    managed: false

scenario:
  name: cisshgo_ios_interfaces
  test_sequence:
    - create
    - converge
    - verify
    - destroy

platforms:
  - name: cisshgo-ios-gathered
    groups:
      - ios_gathered
  - name: cisshgo-ios-merged
    groups:
      - ios_merged
  - name: cisshgo-ios-replaced
    groups:
      - ios_replaced

provisioner:
  name: ansible
  inventory:
    links:
      hosts: ${MOLECULE_SCENARIO_DIRECTORY}/inventory/hosts.yml
  env:
    # Molecule runs ansible-playbook from an ephemeral directory, so point at the
    # ansible_collections parent (namespace dirs live one level below).
    ANSIBLE_COLLECTIONS_PATH: "${MOLECULE_SCENARIO_DIRECTORY}/../../../../.."
    ANSIBLE_HOST_KEY_CHECKING: "false"

verifier:
  name: ansible
```

**File:** `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/inventory/hosts.yml`

```
---
# Ansible inventory for Molecule scenario cisshgo_ios_interfaces.
#
# Network connection vars MUST NOT live under `all.vars` — Molecule also targets
# `localhost` for create/verify/destroy; inheriting network_cli there breaks
# gather_facts (ios_facts / socket_path). Vars are scoped to `cisshgo_targets`
# only; each play host stays under ios_gathered / ios_merged / ios_replaced.
#
# If you change CISSHGO_PORT when starting cisshgo, update ports here to match
# (base, base+1, base+2).

all:
  children:
    cisshgo_targets:
      vars:
        ansible_host: 127.0.0.1
        ansible_connection: ansible.netcommon.network_cli
        ansible_network_os: cisco.ios.ios
        ansible_user: admin
        ansible_password: admin
        ansible_become: false
        ansible_network_cli_ssh_type: libssh
        ansible_libssh_key_exchange_algorithms: +diffie-hellman-group14-sha1,+diffie-hellman-group-exchange-sha1
        ansible_libssh_hostkeys: +ssh-rsa
        ansible_libssh_publickey_algorithms: +ssh-rsa
        ansible_command_timeout: 200
        ansible_ssh_common_args: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
      children:
        ios_gathered:
          hosts:
            cisshgo-ios-gathered:
              ansible_port: 10000
        ios_merged:
          hosts:
            cisshgo-ios-merged:
              ansible_port: 10001
        ios_replaced:
          hosts:
            cisshgo-ios-replaced:
              ansible_port: 10002
```

Create phase (start cisshgo \+ wait ports):

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/create.yml`

```
---
- name: "CISSHGO - Build and start SSH fixture server"
  hosts: localhost
  gather_facts: true
  vars:
    cisshgo_repo_path: "{{ lookup('env', 'CISSHGO_REPO_PATH') | default('', true) }}"
    cisshgo_bin_path: "{{ lookup('env', 'CISSHGO_BIN_PATH') | default('', true) }}"
    cisshgo_starting_port: "{{ lookup('env', 'CISSHGO_PORT') | default('10000', true) }}"
    cisshgo_fixture_dir: "{{ playbook_dir }}/cisshgo_fixtures"
    cisshgo_log_file: "{{ playbook_dir }}/.cisshgo.log"
    cisshgo_pid_file: "{{ playbook_dir }}/.cisshgo.pid"
    cisshgo_port_count: 3
  tasks:
    - name: "Resolve cisshgo binary path"
      ansible.builtin.set_fact:
        cisshgo_binary: >-
          {%- if cisshgo_bin_path != '' -%}
          {{ cisshgo_bin_path }}
          {%- else -%}
          {{ cisshgo_repo_path }}/cisshgo
          {%- endif -%}
    - name: "Check if cisshgo binary exists"
      ansible.builtin.stat:
        path: "{{ cisshgo_binary | trim }}"
      register: cisshgo_bin_stat
    - name: "Validate build inputs when BIN_PATH not provided"
      when: not cisshgo_bin_stat.stat.exists and cisshgo_bin_path | trim == ''
      ansible.builtin.assert:
        that:
          - cisshgo_repo_path | trim != ''
    - name: "Build cisshgo from source"
      when: not cisshgo_bin_stat.stat.exists and cisshgo_bin_path | trim == ''
      block:
        - ansible.builtin.stat:
            path: "{{ cisshgo_repo_path }}/cissh.go"
          register: cisshgo_source_stat
          failed_when: not cisshgo_source_stat.stat.exists
        - ansible.builtin.command:
            cmd: "go build -o cisshgo cissh.go"
            chdir: "{{ cisshgo_repo_path }}"
          changed_when: true
    - name: "Check if cisshgo is already running on port {{ cisshgo_starting_port }}"
      ansible.builtin.shell: |
        lsof -ti:{{ cisshgo_starting_port }} 2>/dev/null || true
      register: port_check
      changed_when: false
    - name: "Stop existing cisshgo instance"
      when: port_check.stdout | trim != ''
      ansible.builtin.shell: |
        kill {{ port_check.stdout | trim }} 2>/dev/null || true
        sleep 1
      changed_when: true
    - name: "Start cisshgo SSH fixture server"
      ansible.builtin.shell: |
        nohup {{ cisshgo_binary | trim }} \
          -t {{ cisshgo_fixture_dir }}/transcript_map.yaml \
          -i {{ cisshgo_fixture_dir }}/cisshgo_inventory.yaml \
          -p {{ cisshgo_starting_port }} \
          > {{ cisshgo_log_file }} 2>&1 &
        echo $! > {{ cisshgo_pid_file }}
      changed_when: true
    - name: "Wait for cisshgo ports to be ready"
      ansible.builtin.wait_for:
        host: 127.0.0.1
        port: "{{ cisshgo_starting_port | int + item }}"
        delay: 1
        timeout: 15
      loop: "{{ range(cisshgo_port_count | int) | list }}"
```

Converge phase (all 5 states):

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/converge.yml`

```
---
- name: "ios_interfaces — gathered state"
  hosts: ios_gathered
  gather_facts: false
  vars_files:
    - "../../../tests/integration/targets/ios_interfaces/vars/main.yaml"
  tasks:
    - cisco.ios.ios_interfaces:
        state: gathered
      register: result
    - ansible.builtin.assert:
        that:
          - result.changed == false
          - gathered['config'] | symmetric_difference(result['gathered']) | length == 0
    - ansible.builtin.assert:
        that:
          - result['gathered'] | length == 6

- name: "ios_interfaces — merged state"
  hosts: ios_merged
  gather_facts: false
  vars_files:
    - "../../../tests/integration/targets/ios_interfaces/vars/main.yaml"
  tasks:
    - cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Merged by Ansible-Network
            enabled: true
          - name: GigabitEthernet3
            description: 04j
            enabled: false
        state: merged
      register: result
    - ansible.builtin.assert:
        that:
          - merged['commands'] | symmetric_difference(result['commands']) | length == 0
          - merged['before'] | symmetric_difference(result['before']) | length == 0
          - merged['after'] | symmetric_difference(result['after']) | length == 0
    - cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Merged by Ansible-Network
            enabled: true
          - name: GigabitEthernet3
            description: 04j
            enabled: false
        state: merged
      register: result
    - ansible.builtin.assert:
        that:
          - result.changed == false

- name: "ios_interfaces — replaced state"
  hosts: ios_replaced
  gather_facts: false
  vars_files:
    - "../../../tests/integration/targets/ios_interfaces/vars/main.yaml"
  tasks:
    - cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Replaced by Ansible-Network
            speed: "1000"
        state: replaced
      register: result
    - ansible.builtin.assert:
        that:
          - replaced['commands'] | symmetric_difference(result['commands']) | length == 0
          - replaced['before'] | symmetric_difference(result['before']) | length == 0
          - replaced['after'] | symmetric_difference(result['after']) | length == 0
    - cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured and Replaced by Ansible-Network
            speed: "1000"
        state: replaced
      register: result
    - ansible.builtin.assert:
        that:
          - result.changed == false

- name: "ios_interfaces — parsed state"
  hosts: ios_gathered
  gather_facts: false
  vars_files:
    - "../../../tests/integration/targets/ios_interfaces/vars/main.yaml"
  tasks:
    - cisco.ios.ios_interfaces:
        running_config: "{{ lookup('file', '../../../tests/integration/targets/ios_interfaces/tests/cli/_parsed.cfg') }}"
        state: parsed
      register: result
    - ansible.builtin.assert:
        that:
          - result.changed == false
          - parsed['config'] | symmetric_difference(result['parsed']) | length == 0

- name: "ios_interfaces — rendered state"
  hosts: ios_gathered
  gather_facts: false
  vars_files:
    - "../../../tests/integration/targets/ios_interfaces/vars/main.yaml"
  tasks:
    - cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet2
            description: Configured by Ansible-Network
            mtu: 110
            enabled: true
          - name: GigabitEthernet3
            description: Configured by Ansible-Network
            mtu: 2800
            enabled: false
            speed: "100"
        state: rendered
      register: result
    - ansible.builtin.assert:
        that:
          - result.changed == false
          - rendered['commands'] | symmetric_difference(result['rendered']) | length == 0
```

Verify phase (unknown command guardrail):

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/verify.yml`

```
---
- name: "CISSHGO — Verify no unknown commands"
  hosts: localhost
  gather_facts: false
  vars:
    cisshgo_log_file: "{{ playbook_dir }}/.cisshgo.log"
  tasks:
    - ansible.builtin.stat:
        path: "{{ cisshgo_log_file }}"
      register: log_stat
    - ansible.builtin.slurp:
        src: "{{ cisshgo_log_file }}"
      when: log_stat.stat.exists
      register: cisshgo_log
    - ansible.builtin.set_fact:
        unknown_commands: "{{ (cisshgo_log.content | b64decode).split('\n') | select('search', 'Unknown command') | list }}"
      when: log_stat.stat.exists
    - ansible.builtin.assert:
        that:
          - unknown_commands | length == 0
      when: log_stat.stat.exists
```

Destroy phase:

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/destroy.yml`

```
---
- name: "CISSHGO — Stop and cleanup"
  hosts: localhost
  gather_facts: false
  vars:
    cisshgo_pid_file: "{{ playbook_dir }}/.cisshgo.pid"
    cisshgo_log_file: "{{ playbook_dir }}/.cisshgo.log"
    cisshgo_starting_port: "{{ lookup('env', 'CISSHGO_PORT') | default('10000', true) }}"
    cisshgo_port_count: 3
  tasks:
    - ansible.builtin.stat:
        path: "{{ cisshgo_pid_file }}"
      register: pid_stat
    - name: stop-by-pid
      when: pid_stat.stat.exists
      block:
        - ansible.builtin.slurp:
            src: "{{ cisshgo_pid_file }}"
          register: pid_content
        - ansible.builtin.shell: |
            kill {{ pid_content.content | b64decode | trim }} 2>/dev/null || true
          changed_when: true
        - ansible.builtin.wait_for:
            host: 127.0.0.1
            port: "{{ cisshgo_starting_port | int + item }}"
            state: stopped
            timeout: 10
          loop: "{{ range(cisshgo_port_count | int) | list }}"
          ignore_errors: true
    - ansible.builtin.file:
        path: "{{ cisshgo_pid_file }}"
        state: absent
```

CISSHGO inventory and transcript map:

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/cisshgo_inventory.yaml`

```
---
devices:
  - platform: ios
    count: 1
  - scenario: ios-interfaces-merged
    count: 1
  - scenario: ios-interfaces-replaced
    count: 1
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcript_map.yaml`

```
---
platforms:
  ios:
    vendor: "cisco"
    hostname: "cisshgo-ios"
    username: "admin"
    password: "admin"
    command_transcripts:
      "show privilege": "transcripts/cisco/ios/show_privilege.txt"
      "terminal length 0": "transcripts/generic_empty_return.txt"
      "terminal width 512": "transcripts/generic_empty_return.txt"
      "terminal width 0": "transcripts/generic_empty_return.txt"
      "show version": "transcripts/cisco/ios/show_version.txt"
      "show running-config": "transcripts/cisco/ios/show_running-config.txt"
      "show running-config | section ^interface": "transcripts/cisco/ios/show_running-config_section_interface_gathered.txt"
      "write memory": "transcripts/generic_empty_return.txt"
      "write mem": "transcripts/generic_empty_return.txt"
    context_search:
      "configure terminal": "(config)#"
      "interface": "(config-if)#"
      "enable": "#"
      "base": "#"
    context_hierarchy:
      "(config-if)#": "(config)#"
      "(config)#": "#"
      "#": ">"
    end_context: "#"
scenarios:
  ios-interfaces-merged:
    platform: ios
    sequence:
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-merged/before.txt"
      - command: "configure terminal"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "interface GigabitEthernet2"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "description Configured and Merged by Ansible-Network"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "interface GigabitEthernet3"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "description 04j"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "shutdown"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "end"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-merged/after.txt"
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-merged/after.txt"
  ios-interfaces-replaced:
    platform: ios
    sequence:
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-replaced/before.txt"
      - command: "configure terminal"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "interface GigabitEthernet2"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "description Configured and Replaced by Ansible-Network"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "end"
        transcript: "transcripts/generic_empty_return.txt"
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-replaced/after.txt"
      - command: "show running-config | section ^interface"
        transcript: "transcripts/scenarios/ios-interfaces-replaced/after.txt"
```

Transcript files:

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/cisco/ios/show_privilege.txt`

```
Current privilege level is 15
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/cisco/ios/show_version.txt`

```
Cisco IOS Software, Version 15.6(3)M2, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2017 by Cisco Systems, Inc.
Compiled Wed 29-Mar-17 14:09 by prod_rel_team

ROM: System Bootstrap, Version 15.6(3r)M1, RELEASE SOFTWARE

{{.Hostname}} uptime is 2 weeks, 3 days, 14 hours, 22 minutes
System returned to ROM by power-on
System image file is "flash0:isr4300-universalk9.16.06.01.SPA.bin"
Last reload reason: power-on
Cisco ISR4321/K9 (1RU) processor with 1687137K/6147K bytes of memory.
Processor board ID FLM2041W0LB
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
3223551K bytes of flash memory at bootflash:.
License Level: ax
License Type: Default. No valid license found.
Next reload license Level: ax
Configuration register is 0x2102
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/cisco/ios/show_running-config.txt`

```
Building configuration...
Current configuration : 2048 bytes
!
version 15.6
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {{.Hostname}}
!
boot-start-marker
boot-end-marker
!
no aaa new-model
!
ip cef
no ipv6 cef
!
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 no ip address
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 no ip address
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
!
ip forward-protocol nd
!
ip http server
ip http secure-server
!
line con 0
 stopbits 1
line vty 0 4
 login
 transport input ssh
!
end
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/cisco/ios/show_running-config_section_interface_gathered.txt`

```
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 description this is interface1
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 description this is interface for testing
 no ip address
 speed 1000
 no negotiation auto
 shutdown
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 description Auto_Cable_Testing_Ansible
 no ip address
 shutdown
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/scenarios/ios-interfaces-merged/before.txt`

```
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 no ip address
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 no ip address
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/scenarios/ios-interfaces-merged/after.txt`

```
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 description Configured and Merged by Ansible-Network
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 description 04j
 no ip address
 speed 1000
 no negotiation auto
 shutdown
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 no ip address
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/scenarios/ios-interfaces-replaced/before.txt`

```
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 description this is interface1
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 description this is interface for testing
 no ip address
 speed 1000
 no negotiation auto
 shutdown
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 description Auto_Cable_Testing_Ansible
 no ip address
 shutdown
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/scenarios/ios-interfaces-replaced/after.txt`

```
interface GigabitEthernet1
 description Management interface do not change
 ip address 10.0.0.1 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 description Configured and Replaced by Ansible-Network
 ip address 192.168.1.1 255.255.255.252
 speed 1000
 no negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 description this is interface for testing
 no ip address
 speed 1000
 no negotiation auto
 shutdown
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 description Auto_Cable_Testing_Ansible
 no ip address
 shutdown
 no mop enabled
 no mop sysid
!
interface Loopback888
 no ip address
!
interface Loopback999
 no ip address
```

File: `ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/cisshgo_fixtures/transcripts/generic_empty_return.txt`

```
+
```

### **2.6 Run Commands**

Full lifecycle:

```shell
molecule test -s cisshgo_ios_interfaces
```

Individual phases:

```shell
molecule create -s cisshgo_ios_interfaces
molecule converge -s cisshgo_ios_interfaces
molecule verify -s cisshgo_ios_interfaces
molecule destroy -s cisshgo_ios_interfaces
```

### **2.7 Sample Successful Run Output (`molecule test -s cisshgo_ios_interfaces`)**

```
(ansible_piyush_dev312) piyushmalik@Piyushs-MacBook-Air-3 extensions % cd "/Users/piyushmalik/dev-workspace/ansible-dev/ansible_collections/cisco/ios/extensions" && CISSHGO_BIN_PATH="/Users/piyushmalik/dev-workspace/cisshgo_0.2.0_darwin_arm64/cisshgo/cisshgo" CISSHGO_PORT=10000 molecule test -s cisshgo_ios_interfaces
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
CRITICAL 'molecule/default/molecule.yml' glob failed.  Exiting.
INFO     default scenario not found, disabling shared state.
INFO     cisshgo_ios_interfaces ➜ discovery: scenario test matrix: create, converge, verify, destroy
INFO     cisshgo_ios_interfaces ➜ prerun: Performing prerun with role_name_check=0...
INFO     cisshgo_ios_interfaces ➜ create: Executing
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [CISSHGO - Build and start SSH fixture server] ****************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Resolve cisshgo binary path] *********************************************
ok: [localhost]

TASK [Check if cisshgo binary exists] ******************************************
ok: [localhost]

TASK [Validate build inputs when BIN_PATH not provided] ************************
skipping: [localhost]

TASK [Verify cisshgo source repo exists] ***************************************
skipping: [localhost]

TASK [Build cisshgo binary] ****************************************************
skipping: [localhost]

TASK [Verify build succeeded] **************************************************
skipping: [localhost]

TASK [Check if cisshgo is already running on port 10000] ***********************
ok: [localhost]

TASK [Stop existing cisshgo instance] ******************************************
skipping: [localhost]

TASK [Start cisshgo SSH fixture server] ****************************************
changed: [localhost]

TASK [Wait for cisshgo ports to be ready] **************************************
ok: [localhost] => (item=10000)
ok: [localhost] => (item=10001)
ok: [localhost] => (item=10002)

TASK [Confirm cisshgo is running] **********************************************
ok: [localhost] => {
    "msg": "CISSHGO started successfully. PID: 82869. Ports: 10000-10002. Log: /Users/piyushmalik/dev-workspace/ansible-dev/ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/.cisshgo.log"
}

PLAY RECAP *********************************************************************
localhost                  : ok=7    changed=1    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0

INFO     cisshgo_ios_interfaces ➜ create: Executed: Successful
INFO     cisshgo_ios_interfaces ➜ converge: Executing
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [ios_interfaces — gathered state] *****************************************

TASK [Gather interface facts from device] **************************************
[WARNING]: Deprecation warnings can be disabled by setting `deprecation_warnings=False` in ansible.cfg.
[DEPRECATION WARNING]: Importing 'to_bytes' from 'ansible.module_utils._text' is deprecated. This feature will be removed from ansible-core version 2.24. Use ansible.module_utils.common.text.converters instead.
[DEPRECATION WARNING]: Importing 'to_text' from 'ansible.module_utils._text' is deprecated. This feature will be removed from ansible-core version 2.24. Use ansible.module_utils.common.text.converters instead.
[DEPRECATION WARNING]: The `ansible.module_utils.common._collections_compat` module is deprecated. This feature will be removed from ansible-core version 2.24. Use `collections.abc` from the Python standard library instead.
[DEPRECATION WARNING]: Passing `warnings` to `exit_json` or `fail_json` is deprecated. This feature will be removed from ansible-core version 2.23. Use `AnsibleModule.warn` instead.
ok: [cisshgo-ios-gathered]

TASK [Assert gathered facts match expected config] *****************************
ok: [cisshgo-ios-gathered]

TASK [Assert correct number of interfaces gathered] ****************************
ok: [cisshgo-ios-gathered]

TASK [PASSED: gathered state] **************************************************
ok: [cisshgo-ios-gathered] => {
    "msg": "gathered state test passed — 6 interfaces collected"
}

PLAY [ios_interfaces — merged state] *******************************************

TASK [Merge interface configuration] *******************************************
changed: [cisshgo-ios-merged]

TASK [Assert generated commands match expected] ********************************
ok: [cisshgo-ios-merged]

TASK [Assert before state matches expected] ************************************
ok: [cisshgo-ios-merged]

TASK [Assert after state matches expected] *************************************
ok: [cisshgo-ios-merged]

TASK [Merge interface configuration — idempotent run] **************************
ok: [cisshgo-ios-merged]

TASK [Assert idempotent — no changes on second run] ****************************
ok: [cisshgo-ios-merged]

TASK [PASSED: merged state] ****************************************************
ok: [cisshgo-ios-merged] => {
    "msg": "merged state test passed — config applied + idempotency verified"
}

PLAY [ios_interfaces — replaced state] *****************************************

TASK [Replace interface configuration] *****************************************
changed: [cisshgo-ios-replaced]

TASK [Assert generated commands match expected] ********************************
ok: [cisshgo-ios-replaced]

TASK [Assert before state matches expected] ************************************
ok: [cisshgo-ios-replaced]

TASK [Assert after state matches expected] *************************************
ok: [cisshgo-ios-replaced]

TASK [Replace interface configuration — idempotent run] ************************
ok: [cisshgo-ios-replaced]

TASK [Assert idempotent — no changes on second run] ****************************
ok: [cisshgo-ios-replaced]

TASK [PASSED: replaced state] **************************************************
ok: [cisshgo-ios-replaced] => {
    "msg": "replaced state test passed — config replaced + idempotency verified"
}

PLAY [ios_interfaces — parsed state] *******************************************

TASK [Parse interface configuration from file] *********************************
ok: [cisshgo-ios-gathered]

TASK [Assert parsed facts match expected] **************************************
ok: [cisshgo-ios-gathered]

TASK [PASSED: parsed state] ****************************************************
ok: [cisshgo-ios-gathered] => {
    "msg": "parsed state test passed — 2 interfaces parsed from config file"
}

PLAY [ios_interfaces — rendered state] *****************************************

TASK [Render interface configuration to CLI commands] **************************
ok: [cisshgo-ios-gathered]

TASK [Assert rendered commands match expected] *********************************
ok: [cisshgo-ios-gathered]

TASK [PASSED: rendered state] **************************************************
ok: [cisshgo-ios-gathered] => {
    "msg": "rendered state test passed — 9 CLI commands rendered"
}

PLAY RECAP *********************************************************************
cisshgo-ios-gathered       : ok=10   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
cisshgo-ios-merged         : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
cisshgo-ios-replaced       : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     cisshgo_ios_interfaces ➜ converge: Executed: Successful
INFO     cisshgo_ios_interfaces ➜ verify: Executing
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [CISSHGO — Verify no unknown commands] ************************************

TASK [Check if cisshgo log file exists] ****************************************
ok: [localhost]

TASK [Read cisshgo log] ********************************************************
ok: [localhost]

TASK [Count unknown command occurrences] ***************************************
ok: [localhost]

TASK [Display unknown commands (if any)] ***************************************
skipping: [localhost]

TASK [Assert no unknown commands in cisshgo log] *******************************
ok: [localhost] => {
    "changed": false,
    "msg": "All commands recognized by CISSHGO — transcript coverage is complete."
}

TASK [Display cisshgo log summary] *********************************************
ok: [localhost] => {
    "msg": "CISSHGO verification passed. Log file: /Users/piyushmalik/dev-workspace/ansible-dev/ansible_collections/cisco/ios/extensions/molecule/cisshgo_ios_interfaces/.cisshgo.log Log size: 1869 bytes"
}

PLAY RECAP *********************************************************************
localhost                  : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     cisshgo_ios_interfaces ➜ verify: Executed: Successful
INFO     cisshgo_ios_interfaces ➜ destroy: Executing
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [CISSHGO — Stop and cleanup] **********************************************

TASK [Check if PID file exists] ************************************************
ok: [localhost]

TASK [Read PID file] ***********************************************************
ok: [localhost]

TASK [Kill cisshgo process] ****************************************************
changed: [localhost]

TASK [Wait for CISSHGO ports to be released] ***********************************
ok: [localhost] => (item=0)
ok: [localhost] => (item=1)
ok: [localhost] => (item=2)

TASK [Remove PID file] *********************************************************
changed: [localhost]

TASK [Fallback — kill any process on CISSHGO ports] ****************************
skipping: [localhost]

TASK [Clean up log file] *******************************************************
changed: [localhost]

TASK [CISSHGO stopped and cleaned up] ******************************************
ok: [localhost] => {
    "msg": "CISSHGO fixture server stopped. All temporary files removed."
}

PLAY RECAP *********************************************************************
localhost                  : ok=7    changed=3    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     cisshgo_ios_interfaces ➜ destroy: Executed: Successful
INFO     cisshgo_ios_interfaces ➜ scenario: Pruning extra files from scenario ephemeral directory
INFO     Molecule executed 1 scenario (1 successful)
```

### **2.8 cisshgo Log Sample (`.cisshgo.log`)**

```
2026/04/02 19:51:10 Starting listener on :10002 [scenario=ios-interfaces-replaced hostname=cisshgo-ios user=admin]
2026/04/02 19:51:10 Starting listener on :10001 [scenario=ios-interfaces-merged hostname=cisshgo-ios user=admin]
2026/04/02 19:51:10 Starting listener on :10000 [platform=ios hostname=cisshgo-ios user=admin]
2026/04/02 19:51:16 terminal length 0
2026/04/02 19:51:16 terminal width 512
2026/04/02 19:51:16 terminal width 0
2026/04/02 19:51:16 show version
2026/04/02 19:51:16 show vlan
2026/04/02 19:51:16 show running-config | section ^interface
2026/04/02 19:51:17 terminal closed
2026/04/02 19:51:18 terminal length 0
2026/04/02 19:51:18 terminal width 512
2026/04/02 19:51:18 terminal width 0
2026/04/02 19:51:18 show version
2026/04/02 19:51:18 show vlan
2026/04/02 19:51:18 show running-config | section ^interface
2026/04/02 19:51:18 configure terminal
2026/04/02 19:51:18 interface GigabitEthernet2
2026/04/02 19:51:18 description Configured and Merged by Ansible-Network
2026/04/02 19:51:18 interface GigabitEthernet3
2026/04/02 19:51:19 description 04j
2026/04/02 19:51:19 shutdown
2026/04/02 19:51:19 end
2026/04/02 19:51:19 show running-config | section ^interface
2026/04/02 19:51:20 show running-config | section ^interface
2026/04/02 19:51:20 terminal closed
2026/04/02 19:51:21 terminal length 0
2026/04/02 19:51:21 terminal width 512
2026/04/02 19:51:21 terminal width 0
2026/04/02 19:51:21 show version
2026/04/02 19:51:21 show vlan
2026/04/02 19:51:21 show running-config | section ^interface
2026/04/02 19:51:22 configure terminal
2026/04/02 19:51:22 interface GigabitEthernet2
2026/04/02 19:51:22 description Configured and Replaced by Ansible-Network
2026/04/02 19:51:22 end
2026/04/02 19:51:22 show running-config | section ^interface
2026/04/02 19:51:23 show running-config | section ^interface
2026/04/02 19:51:23 terminal closed
```
