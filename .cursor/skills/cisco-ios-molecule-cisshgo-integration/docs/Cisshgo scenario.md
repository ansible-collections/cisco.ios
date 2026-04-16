# **Scenarios and Integration Tests**

If you are setting up cisshgo for the first time (install, inventory, listeners, Ansible connection), use [**Getting started with cisshgo**](https://docs.google.com/document/d/11kJDbAKBfHHT0K6Y8WXzmEKJITyejYolSo-DdszYuk0/edit?tab=t.0#heading=h.pv5xnanconku) as a walkthrough before or alongside this document.

This document explains how cisshgo **scenarios** work and how to set one up so you can run Ansible (or other) integration tests against cisshgo without real hardware.

---

## **1\. What is a scenario?**

A **scenario** is an **ordered sequence of (command → transcript)** steps layered on top of a **platform**. Unlike a plain platform (where each command always returns the same transcript), a scenario returns **different output for the same command** depending on **position in the sequence**.

That lets you simulate **before/after** behavior: for example, the first time the client runs show running-config | section ^interface they get a "before" transcript, and after a simulated config change the next time they get an "after" transcript.

* **Platform:** Supplies the base device (hostname, password, command\_transcripts, context\_search, etc.).
* **Sequence:** A list of steps. Each step has a command (exact string to match) and a transcript (path to the file to return when that command is received). Commands must be sent **in the exact order** of the sequence; the device keeps a **per-session pointer** that advances one step per matching command.

Scenarios are defined in the same transcript map as platforms, under a top-level scenarios: key.

---

## **2\. When is a scenario used?**

A scenario is used **only** when:

1. **You start cisshgo with an inventory file:**

./cisshgo \--inventory path/to/inventory.yaml ... 2\. **An inventory entry specifies a scenario (not a platform):**
In the inventory YAML, a device entry must have scenario:

and must **not** have platform set for that entry.

If you run cisshgo **without** \--inventory, every listener uses the default **platform** (e.g. csr1000v) and **no** scenario. If the inventory only has platform: entries, again no scenario is used. So the **trigger** is: inventory file \+ at least one entry with scenario:

.

For each such entry, cisshgo:

* Loads the scenario by name from the transcript map.
* Builds a device from the scenario's platform and preloads the sequence (command → transcript content) from the transcript paths.
* Starts one or more listeners (according to count) that use **ScenarioListener** and the sequence. All other listeners use the generic platform handler and no sequence.

---

## **3\. How the handler uses the sequence**

In **interactive** mode (one SSH session, multiple commands over the same connection):

1. Each new SSH connection gets its **own** sequence pointer, starting at step 0\.
2. When the client sends a line, the handler first checks whether it **matches the current sequence step** (word-based prefix match; see matchSequenceStep in the code). If it matches:
   * The transcript for that step is sent to the client.
   * The pointer advances to the next step.
   * If the command also appears in the platform's context\_search (e.g. enable, configure terminal, interface), the **context switch is applied** (prompt and internal state update). So enable both returns empty and moves the prompt to \#.
3. If the input **does not** match the current step:
   * **Context switches** (e.g. enable, configure terminal) are **not** applied while the scenario is active—so those commands can be reported as unknown or return the wrong behavior unless they are **in** the sequence.
   * The handler then falls through to normal dispatch: platform command\_transcripts (e.g. for no description) or unknown-command handling.

So for a scenario to behave correctly, **every command that the client sends** (and that must change context or return a specific response) should appear in the sequence **in the exact order** the client sends it. Commands that only need to return empty can be sequence steps with generic\_empty\_return.txt; commands that must return different content at different times (e.g. show running-config | section ^interface) must appear multiple times in the sequence with different transcript paths.

**Important:** Scenarios apply only in **interactive** mode. If the client uses **exec** mode (one command per connection, no PTY), the handler uses only the platform's SupportedCommands and never runs the sequence. So integration tests that rely on before/after must use a **persistent connection** (e.g. Ansible network\_cli with a single session per play).

---

## **4\. How to set up a scenario for an integration test**

### **4.1 Decide the command order**

You must know the **exact order** of commands your test sends. Options:

* Run the test against a **real device** (or against cisshgo) with **verbose** output (-vvv for Ansible) and inspect the log for the commands sent to the device.
* Or derive the order from the test: e.g. gather facts (enable, show privilege, show version), then task 1 (e.g. remove config: configure terminal, interface …, end), then task 2 (e.g. gather, then merge config, then gather again), etc.

Spacing and exact strings (e.g. GigabitEthernet 0/1 vs GigabitEthernet0/1) matter; the matcher is word-based.

### **4.2 Add or reuse a platform**

The scenario's platform field must name a platform in the same transcript map. That platform's command\_transcripts are used for any command that is **not** in the sequence (or after the sequence is exhausted). Ensure the platform has entries for every command the test might send that you do **not** want in the sequence (e.g. terminal length 0). For commands that **are** in the sequence, the sequence overrides.

Do **not** put a "same command, different output" key (e.g. show running-config | section ^interface) in the platform if you want the scenario to control its response; only the sequence should serve it.

### **4.3 Create transcript files**

* For steps that should return **empty** (e.g. enable, configure terminal, interface …, end), use generic\_empty\_return.txt or your existing empty transcript.
* For steps that must return **specific content** (e.g. interface section "before" vs "after"), create one file per response (e.g. section\_before.txt, section\_after.txt) under a folder like transcripts/scenarios/
  /. The content must match what the client's parser expects (e.g. Cisco-style interface blocks for ios\_interfaces).

Transcript paths in the scenario are **relative to the directory that contains the transcript map file** (e.g. transcripts/ when the map is transcripts/transcript\_map.yaml).

### **4.4 Define the scenario in the transcript map**

In transcripts/transcript\_map.yaml, under scenarios:, add an entry:

scenarios:

  my\_scenario\_name:

    platform: csr1000v   \# or the platform you use

    sequence:

      \- command: "first exact command string"

        transcript: "path/to/transcript1.txt"

      \- command: "second command"

        transcript: "path/to/transcript2.txt"

      \# ... in the exact order the client sends

Use the **exact** command strings (including pipes, e.g. show running-config | section ^interface). Repeat the same command string with different transcripts when the client sends it multiple times (e.g. before merge, after merge, idempotent gather).

### **4.5 Create a cisshgo inventory**

Create a YAML file (e.g. cisshgo\_inventory.yaml) that references the scenario:

devices:

  \- scenario: my\_scenario\_name

    count: 1

Use scenario: (not platform:). count is how many listeners to start for this entry; for a single integration test host, 1 is enough.

### **4.6 Run cisshgo with the inventory**

./cisshgo \--inventory cisshgo\_inventory.yaml \--listeners 1 \--starting-port 10000

(If your transcript map is elsewhere, add \--transcript-map path/to/transcript\_map.yaml.) This starts one listener on port 10000 that serves the scenario.

### **4.7 Point your test at cisshgo**

Configure the integration test (e.g. Ansible inventory) so the target host is the machine running cisshgo and the port is the one you used (e.g. 10000). Use the same connection and become settings as for a real device (e.g. ansible\_connection=[ansible.netcommon.network](http://ansible.netcommon.network)\_cli, ansible\_become, ansible\_become\_pass). No change is needed to the test playbook or vars; only the host/port (and optionally inventory) point at cisshgo.

### **4.8 If something fails**

* **"Unknown command" or "Invalid input" for a command:** Either add that exact command as the **next** step in the sequence (with the correct transcript), or add it to the platform's command\_transcripts. For context-changing commands (enable, configure terminal, interface, end), they must be **in the sequence** so that the context switch is applied (see section 3).
* **Wrong "before" or "after":** The order of steps in the sequence does not match the order the client sends. Adjust the sequence (or add/remove steps) so it matches the verbose log. Or the transcript content does not parse as the test expects—fix the transcript file.
* **Section command not matched:** The scenario step command must match the string sent by the client exactly (including |, ^, spaces). Capture it with \-vvv and align the YAML.

---

## **5\. Example: ios\_interfaces\_merged scenario**

Upstream: [cisco.ios ios\_interfaces merged integration test](https://github.com/ansible-collections/cisco.ios/blob/main/tests/integration/targets/ios_interfaces/tests/cli/merged.yaml).

This scenario was built so the **cisco.ios ios\_interfaces** "merged" integration test (gather → remove config → merge → assert before/after → idempotent merge → teardown) can run against cisshgo.

### **5.1 Purpose**

* The test expects **before** and **after** interface lists (e.g. from show running-config | section ^interface).
* The first time the module runs that command it should get a "clean" interface list; after the merge task it should get the same list with the new descriptions/shutdown. The idempotent run should see the same "after" again.
* So we need **three** responses for show running-config | section ^interface: one "before", two "after" (merge and idempotent).

### **5.2 Sequence shape**

The test sends many commands in a fixed order. The scenario models that full order so that:

1. **Facts:** enable, show privilege, show version (so the test can gather facts and verify privilege).
2. **Remove config:** configure terminal, then interface GigabitEthernet 0/1, no description, no shutdown, then the same pattern for 0/2 and 0/3, then end.
3. **First gather:** show running-config | section ^interface → return **section\_before.txt** (interfaces without the merge).
4. **Merge:** configure terminal, interface GigabitEthernet0/1, description…, interface GigabitEthernet0/2, description 04j, shutdown, end.
5. **Second gather:** show running-config | section ^interface → return **section\_after.txt**.
6. **Idempotent gather:** show running-config | section ^interface again → return **section\_after.txt**.
7. **Teardown:** configure terminal and the same remove-config block again, then end.

So the scenario has **dozens of steps** (one per command in that order), with the three "section" steps pointing to the two transcript files (before, after, after).

### **5.3 Transcript files**

Paths are relative to the directory that contains **`transcripts/transcript_map.yaml`** (i.e. under **`transcripts/`**).

**`scenarios/ios_interfaces_merged/section_before.txt`** — returned for the **first** **`show running-config | section ^interface`** (after initial remove config). Parses to the test's "before" list: GigabitEthernet0/0–0/3, Loopback888, Loopback999 with duplex/speed, no merge descriptions.

```
interface GigabitEthernet0/0
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 duplex auto
 speed auto
!
interface GigabitEthernet0/2
 duplex auto
 speed auto
!
interface GigabitEthernet0/3
 duplex auto
 speed auto
!
interface Loopback888
!
interface Loopback999
!
```

**`scenarios/ios_interfaces_merged/section_after.txt`** — returned for the **second and third** **`show running-config | section ^interface`** (after merge and on idempotent merge). Same layout with merged descriptions and Ge0/2 shutdown.

```
interface GigabitEthernet0/0
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 description Configured and Merged by Ansible-Network
 duplex auto
 speed auto
!
interface GigabitEthernet0/2
 description 04j
 shutdown
 duplex auto
 speed auto
!
interface GigabitEthernet0/3
 duplex auto
 speed auto
!
interface Loopback888
!
interface Loopback999
!
```

All other scenario steps use **`generic_empty_return.txt`** or existing platform transcripts (e.g. **`cisco/ios/show_privilege.txt`**, **`cisco/csr1000v/show_version.txt`**).

### **5.4 Scenario definition in `transcripts/transcript_map.yaml`**

Complete **`ios_interfaces_merged`** entry. **Every** command the playbook sends must appear in this order; the three **`show running-config | section ^interface`** steps map to **before**, **after**, **after**.

```
  ios_interfaces_merged:
    platform: csr1000v
    sequence:
      - command: "enable"
        transcript: "generic_empty_return.txt"
      - command: "show privilege"
        transcript: "cisco/ios/show_privilege.txt"
      - command: "show version"
        transcript: "cisco/csr1000v/show_version.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/1"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/2"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/3"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "show running-config | section ^interface"
        transcript: "scenarios/ios_interfaces_merged/section_before.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet0/1"
        transcript: "generic_empty_return.txt"
      - command: "description Configured and Merged by Ansible-Network"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet0/2"
        transcript: "generic_empty_return.txt"
      - command: "description 04j"
        transcript: "generic_empty_return.txt"
      - command: "shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "show running-config | section ^interface"
        transcript: "scenarios/ios_interfaces_merged/section_after.txt"
      - command: "show running-config | section ^interface"
        transcript: "scenarios/ios_interfaces_merged/section_after.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/1"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/2"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/3"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
```

### **5.5 cisshgo inventory**

**cisshgo\_inventory.yaml:**

devices:

  \- scenario: ios\_interfaces\_merged

    count: 1

### **5.6 Running the integration test**

1. Start cisshgo from the repo root:
   /cisshgo \--inventory cisshgo\_inventory.yaml \--listeners 1 \--starting-port 10000

(Expected Output)

2026/03/26 17:32:30 Starting listener on :10000 \[scenario=ios\_interfaces\_merged hostname=cisshgo1000v user=admin\]

1. Point Ansible at that host and port (e.g. ansible\_host: [localhost](http://localhost), ansible\_ssh\_port: 10000\) with the same connection and become vars as for a real IOS device.
2. Run the playbook:
   nsible-playbook \-i inventory.ini test.yml

**Expected Outcome from ansible after running the playbook \-**

""""
ok: \[ios\_device\]

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Debug start\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:8

ok: \[ios\_device\] \=\> {

    "msg": "START Merged ios\_interfaces state for integration tests on connection=[ansible.netcommon.network](http://ansible.netcommon.network)\_cli"

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[ansible.builtin.include\_tasks\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:12

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

included: /Users/piyushmalik/dev-workspace/ansible-dev/\_remove\_config.yaml for ios\_device

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Remove configuration\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/\_remove\_config.yaml:2

\[WARNING\]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device including the indentation

\[WARNING\]: Task result `warnings` was \<class 'str'\> instead of \<class 'list'\>.

changed: \[ios\_device\] \=\> {

    "changed": true,

    "commands": \[

        "interface GigabitEthernet 0/1",

        "no description",

        "no shutdown",

        "interface GigabitEthernet 0/2",

        "no description",

        "no mtu",

        "no speed",

        "no shutdown",

        "interface GigabitEthernet 0/3",

        "no description",

        "no mtu",

        "no speed",

        "no shutdown"

    \],

    "invocation": {

        "module\_args": {

            "backup": false,

            "backup\_options": null,

            "commit": null,

            "commit\_comment": null,

            "config": "interface GigabitEthernet 0/1\\nno description\\nno shutdown\\ninterface GigabitEthernet 0/2\\nno description\\nno mtu\\nno speed\\nno shutdown\\ninterface GigabitEthernet 0/3\\nno description\\nno mtu\\nno speed\\nno shutdown\\n",

            "defaults": false,

            "diff\_ignore\_lines": null,

            "diff\_match": null,

            "diff\_replace": null,

            "multiline\_delimiter": null,

            "replace": null,

            "rollback": null

        }

    }

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Merge provided configuration with device configuration\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:15

changed: \[ios\_device\] \=\> {

    "after": \[

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/0",

            "speed": "auto"

        },

        {

            "description": "Configured and Merged by Ansible-Network",

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/1",

            "speed": "auto"

        },

        {

            "description": "04j",

            "duplex": "auto",

            "enabled": false,

            "name": "GigabitEthernet0/2",

            "speed": "auto"

        },

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/3",

            "speed": "auto"

        },

        {

            "enabled": true,

            "name": "Loopback888"

        },

        {

            "enabled": true,

            "name": "Loopback999"

        }

    \],

    "before": \[

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/0",

            "speed": "auto"

        },

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/1",

            "speed": "auto"

        },

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/2",

            "speed": "auto"

        },

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/3",

            "speed": "auto"

        },

        {

            "enabled": true,

            "name": "Loopback888"

        },

        {

            "enabled": true,

            "name": "Loopback999"

        }

    \],

    "changed": true,

    "commands": \[

        "interface GigabitEthernet0/1",

        "description Configured and Merged by Ansible-Network",

        "interface GigabitEthernet0/2",

        "description 04j",

        "shutdown"

    \],

    "invocation": {

        "module\_args": {

            "config": \[

                {

                    "description": "Configured and Merged by Ansible-Network",

                    "duplex": null,

                    "enabled": true,

                    "logging": null,

                    "mac\_address": null,

                    "mode": null,

                    "mtu": null,

                    "name": "GigabitEthernet0/1",

                    "service\_policy": null,

                    "snmp": null,

                    "speed": null,

                    "template": null

                },

                {

                    "description": "04j",

                    "duplex": null,

                    "enabled": false,

                    "logging": null,

                    "mac\_address": null,

                    "mode": null,

                    "mtu": null,

                    "name": "GigabitEthernet0/2",

                    "service\_policy": null,

                    "snmp": null,

                    "speed": null,

                    "template": null

                }

            \],

            "running\_config": null,

            "state": "merged"

        }

    }

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Assert that correct set of commands were generated\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:28

\[DEPRECATION WARNING\]: Conditionals should not be surrounded by templating delimiters such as {{ }} or {% %}. This feature will be removed from ansible-core version 2.23.

Origin: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:31:17

29           ansible.builtin.assert:

30             that:

31               \- "{{ merged\['commands'\] | symmetric\_difference(result\['commands'\]) | length \== 0 }}"

                   ^ column 17

ok: \[ios\_device\] \=\> {

    "changed": false,

    "msg": "All assertions passed"

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Assert that before dicts are correctly generated\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:33

\[DEPRECATION WARNING\]: Conditionals should not be surrounded by templating delimiters such as {{ }} or {% %}. This feature will be removed from ansible-core version 2.23.

Origin: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:36:17

34           ansible.builtin.assert:

35             that:

36               \- "{{ merged\['before'\] | symmetric\_difference(result\['before'\]) | length \== 0 }}"

                   ^ column 17

ok: \[ios\_device\] \=\> {

    "changed": false,

    "msg": "All assertions passed"

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Assert that after dict is correctly generated\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:38

\[DEPRECATION WARNING\]: Conditionals should not be surrounded by templating delimiters such as {{ }} or {% %}. This feature will be removed from ansible-core version 2.23.

Origin: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:41:17

39           ansible.builtin.assert:

40             that:

41               \- "{{ merged\['after'\] | symmetric\_difference(result\['after'\]) | length \== 0 }}"

                   ^ column 17

ok: \[ios\_device\] \=\> {

    "changed": false,

    "msg": "All assertions passed"

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Merge provided configuration with device configuration (idempotent)\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:43

ok: \[ios\_device\] \=\> {

    "before": \[

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/0",

            "speed": "auto"

        },

        {

            "description": "Configured and Merged by Ansible-Network",

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/1",

            "speed": "auto"

        },

        {

            "description": "04j",

            "duplex": "auto",

            "enabled": false,

            "name": "GigabitEthernet0/2",

            "speed": "auto"

        },

        {

            "duplex": "auto",

            "enabled": true,

            "name": "GigabitEthernet0/3",

            "speed": "auto"

        },

        {

            "enabled": true,

            "name": "Loopback888"

        },

        {

            "enabled": true,

            "name": "Loopback999"

        }

    \],

    "changed": false,

    "commands": \[\],

    "invocation": {

        "module\_args": {

            "config": \[

                {

                    "description": "Configured and Merged by Ansible-Network",

                    "duplex": null,

                    "enabled": true,

                    "logging": null,

                    "mac\_address": null,

                    "mode": null,

                    "mtu": null,

                    "name": "GigabitEthernet0/1",

                    "service\_policy": null,

                    "snmp": null,

                    "speed": null,

                    "template": null

                },

                {

                    "description": "04j",

                    "duplex": null,

                    "enabled": false,

                    "logging": null,

                    "mac\_address": null,

                    "mode": null,

                    "mtu": null,

                    "name": "GigabitEthernet0/2",

                    "service\_policy": null,

                    "snmp": null,

                    "speed": null,

                    "template": null

                }

            \],

            "running\_config": null,

            "state": "merged"

        }

    }

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Assert that the previous task was idempotent\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:46

ok: \[ios\_device\] \=\> {

    "changed": false,

    "msg": "All assertions passed"

}

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[ansible.builtin.include\_tasks\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/test.yml:51

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

included: /Users/piyushmalik/dev-workspace/ansible-dev/\_remove\_config.yaml for ios\_device

Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK \[Remove configuration\] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

task path: /Users/piyushmalik/dev-workspace/ansible-dev/\_remove\_config.yaml:2

changed: \[ios\_device\] \=\> {

    "changed": true,

    "commands": \[

        "interface GigabitEthernet 0/1",

        "no description",

        "no shutdown",

        "interface GigabitEthernet 0/2",

        "no description",

        "no mtu",

        "no speed",

        "no shutdown",

        "interface GigabitEthernet 0/3",

        "no description",

        "no mtu",

        "no speed",

        "no shutdown"

    \],

    "invocation": {

        "module\_args": {

            "backup": false,

            "backup\_options": null,

            "commit": null,

            "commit\_comment": null,

            "config": "interface GigabitEthernet 0/1\\nno description\\nno shutdown\\ninterface GigabitEthernet 0/2\\nno description\\nno mtu\\nno speed\\nno shutdown\\ninterface GigabitEthernet 0/3\\nno description\\nno mtu\\nno speed\\nno shutdown\\n",

            "defaults": false,

            "diff\_ignore\_lines": null,

            "diff\_match": null,

            "diff\_replace": null,

            "multiline\_delimiter": null,

            "replace": null,

            "rollback": null

        }

    }

}

PLAY RECAP \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

ios\_device                 : ok=12   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

"""

The test playbook and vars (e.g. expected merged.before / merged.after) stay unchanged; only the target is cisshgo.

### **5.7 Why "enable" is the first step**

Ansible sends enable to escalate privilege. In scenario mode, **context switches** (like enable → \#) are applied only when the current input **matches the current sequence step**. If enable were not in the sequence, it would not match the first step (show running-config | section ^interface), so the context would not switch and the handler would treat enable as unknown. So the first step is **enable** with an empty transcript; that way the sequence advances and the prompt moves to \# as expected.

---

## **6\. Example: ios\_interfaces\_gathered scenario**

Upstream reference: [cisco.ios ios\_interfaces gathered integration test](https://github.com/ansible-collections/cisco.ios/blob/main/tests/integration/targets/ios_interfaces/tests/cli/gathered.yaml).

This scenario supports the **gathered** state: **remove baseline → populate interfaces with `ios_config` → `ios_interfaces` with `state: gathered` → assert → teardown**. Unlike **merged**, there is only **one** `show running-config | section ^interface` that must return the populated running config.

### **6.1 Purpose**

* After `_populate_config.yaml`, the module gathers interface facts from **`show running-config | section ^interface`**.
* cisshgo must return a single interface section transcript that parses to the list in **`vars.yaml`** under **`gathered.config`** (asserted with `symmetric_difference` against `result.gathered`).
* Teardown repeats **`_remove_config.yaml`** (same command shape as the merged example).

### **6.2 Supporting task files**

**`_populate_config.yaml`** (three `ios_config` tasks; each opens config mode, applies lines under one interface, then exits):

```
---
- name: Configure interface settings GigabitEthernet0/1
  cisco.ios.ios_config:
    lines:
      - description Management interface do not change
    parents: interface GigabitEthernet0/1

- name: Configure interface settings GigabitEthernet0/2
  cisco.ios.ios_config:
    lines:
      - description this is interface1
      - mtu 1500
      - speed 1000
      - no shutdown
    parents: interface GigabitEthernet0/2

- name: Configure interface settings GigabitEthernet0/3
  cisco.ios.ios_config:
    lines:
      - description this is interface for testing
      - speed 1000
      - shutdown
    parents: interface GigabitEthernet0/3
```

**`vars.yaml`** (expected gathered list; keys must match what the module returns after parsing the section transcript):

```
gathered:
  config:
    - duplex: auto
      enabled: true
      name: GigabitEthernet0/0
      speed: auto
    - description: Management interface do not change
      duplex: auto
      enabled: true
      name: GigabitEthernet0/1
      speed: auto
    - description: this is interface1
      duplex: auto
      enabled: true
      name: GigabitEthernet0/2
      speed: "1000"
    - description: this is interface for testing
      duplex: auto
      enabled: false
      name: GigabitEthernet0/3
      speed: "1000"
```

### **6.3 Playbook**

```
---
- name: Gather ios_interfaces state for integration tests
  hosts: ios
  vars_files:
    - vars.yaml
  tasks:
    - ansible.builtin.debug:
        msg: START ios_interfaces gathered integration tests on connection={{ ansible_connection }}

    - ansible.builtin.include_tasks: _remove_config.yaml
    - ansible.builtin.include_tasks: _populate_config.yaml

    - block:
        - name: Gather the provided configuration with the existing running configuration
          register: result
          cisco.ios.ios_interfaces:
            config:
            state: gathered

        - name: Debug gathered result
          ansible.builtin.debug:
            var: result.gathered

        - name: Assert
          ansible.builtin.assert:
            that:
              - gathered['config'] | symmetric_difference(result.gathered) == []
              - result['changed'] == false
      always:
        - ansible.builtin.include_tasks: _remove_config.yaml
```

### **6.4 Sequence shape**

1. **Facts:** `enable`, `show privilege`, `show version`.
2. **First remove (`_remove_config`):** `configure terminal`, per-interface cleanup for `GigabitEthernet 0/1` … `0/3` (spacing as in the merged scenario), `end`.
3. **Populate:** three blocks: `configure terminal` → `interface GigabitEthernet0/1` → description → `end`; then `GigabitEthernet0/2` (description, `mtu 1500`, `speed 1000`, `no shutdown`) → `end`; then `GigabitEthernet0/3` (description, `speed 1000`, `shutdown`) → `end`.
4. **Gather:** `show running-config | section ^interface` → **`scenarios/ios_interfaces_gathered/section_gathered.txt`** (interface blocks that yield the expected `gathered` list).
5. **Teardown:** same remove-config block as step 2, then `end`.

The full ordered command list is in **`transcripts/transcript_map.yaml`** under **`scenarios.ios_interfaces_gathered`** (see §6.6).

### **6.5 Transcript file (`section_gathered.txt`)**

Path (relative to the transcript map directory): **`transcripts/scenarios/ios_interfaces_gathered/section_gathered.txt`**.

This is the exact text returned for **`show running-config | section ^interface`** after populate. It must parse to the same structure Ansible expects in **`gathered.config`** (see §6.2).

```
interface GigabitEthernet0/0
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 description Management interface do not change
 duplex auto
 speed auto
!
interface GigabitEthernet0/2
 description this is interface1
 mtu 1500
 duplex auto
 speed 1000
!
interface GigabitEthernet0/3
 description this is interface for testing
 duplex auto
 speed 1000
 shutdown
!
```

All other scenario steps use **`generic_empty_return.txt`** or existing platform transcripts (e.g. **`cisco/ios/show_privilege.txt`**, **`cisco/csr1000v/show_version.txt`**).

### **6.6 Scenario definition in `transcripts/transcript_map.yaml`**

Full **`ios_interfaces_gathered`** entry (platform **`csr1000v`**). Each **`command`** must match what Ansible sends, in this order:

```
  ios_interfaces_gathered:
    platform: csr1000v
    sequence:
      - command: "enable"
        transcript: "generic_empty_return.txt"
      - command: "show privilege"
        transcript: "cisco/ios/show_privilege.txt"
      - command: "show version"
        transcript: "cisco/csr1000v/show_version.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/1"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/2"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/3"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet0/1"
        transcript: "generic_empty_return.txt"
      - command: "description Management interface do not change"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet0/2"
        transcript: "generic_empty_return.txt"
      - command: "description this is interface1"
        transcript: "generic_empty_return.txt"
      - command: "mtu 1500"
        transcript: "generic_empty_return.txt"
      - command: "speed 1000"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet0/3"
        transcript: "generic_empty_return.txt"
      - command: "description this is interface for testing"
        transcript: "generic_empty_return.txt"
      - command: "speed 1000"
        transcript: "generic_empty_return.txt"
      - command: "shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
      - command: "show running-config | section ^interface"
        transcript: "scenarios/ios_interfaces_gathered/section_gathered.txt"
      - command: "configure terminal"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/1"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/2"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "interface GigabitEthernet 0/3"
        transcript: "generic_empty_return.txt"
      - command: "no description"
        transcript: "generic_empty_return.txt"
      - command: "no mtu"
        transcript: "generic_empty_return.txt"
      - command: "no speed"
        transcript: "generic_empty_return.txt"
      - command: "no shutdown"
        transcript: "generic_empty_return.txt"
      - command: "end"
        transcript: "generic_empty_return.txt"
```

The **`csr1000v`** platform in the same file also lists extra **`command_transcripts`** keys (e.g. **`description Management interface do not change`**, **`mtu 1500`**, **`speed 1000`**, **`interface GigabitEthernet0/3`**) so unmatched lines can still resolve when not on a sequence step.

### **6.7 cisshgo inventory**

Use **`scenario: ios_interfaces_gathered`** (same pattern as merged). The repo includes **`cisshgo_inventory_gathered.yaml`** next to **`cisshgo_inventory.yaml`**:

```
---
# Run: ./cisshgo --inventory cisshgo_inventory_gathered.yaml --listeners 1 --starting-port 10000
devices:
  - scenario: ios_interfaces_gathered
    count: 1
```

You can merge multiple device entries in one inventory if you run listeners on different ports; the scenario name must match the playbook you run.

### **6.8 Running the integration test**

1. Start cisshgo from the repo root (or the directory where **`cisshgo`** and **`transcripts/`** live):
   `./cisshgo --inventory cisshgo_inventory_gathered.yaml --listeners 1 --starting-port 10000`
    **(Expected output)**
    `Starting listener on :10000 [scenario=ios_interfaces_gathered hostname=cisshgo1000v user=admin]`
    (Timestamp prefix may differ.)
2. Point Ansible at that host and port (e.g. **`ansible_host: localhost`**, **`ansible_port: 10000`** or **`ansible_ssh_port`**, depending on your inventory plugin) with the same connection and become vars as for a real IOS device (**`ansible_connection=ansible.netcommon.network_cli`**, etc.).
3. Run the playbook (name it as you like, e.g. **`gathertest.yml`**):
   `ansible-playbook -i inventory.ini gathertest.yml`

**Expected outcome from Ansible after running the playbook** (representative; paths and **`vars_file`** locations reflect your workspace):

```
ok: [ios_device]
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [ansible.builtin.debug] **************************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:7
ok: [ios_device] => {
    "msg": "START ios_interfaces gathered integration tests on connection=ansible.netcommon.network_cli"
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [ansible.builtin.include_tasks] ******************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:10
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
included: /Users/piyushmalik/dev-workspace/ansible-dev/_remove_config.yaml for ios_device
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Remove configuration] ***************************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/_remove_config.yaml:2
[WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device including the indentation
[WARNING]: Task result `warnings` was <class 'str'> instead of <class 'list'>.
changed: [ios_device] => {
    "changed": true,
    "commands": [
        "interface GigabitEthernet 0/1",
        "no description",
        "no shutdown",
        "interface GigabitEthernet 0/2",
        "no description",
        "no mtu",
        "no speed",
        "no shutdown",
        "interface GigabitEthernet 0/3",
        "no description",
        "no mtu",
        "no speed",
        "no shutdown"
    ],
    "invocation": {
        "module_args": {
            "backup": false,
            "backup_options": null,
            "commit": null,
            "commit_comment": null,
            "config": "interface GigabitEthernet 0/1\nno description\nno shutdown\ninterface GigabitEthernet 0/2\nno description\nno mtu\nno speed\nno shutdown\ninterface GigabitEthernet 0/3\nno description\nno mtu\nno speed\nno shutdown\n",
            "defaults": false,
            "diff_ignore_lines": null,
            "diff_match": null,
            "diff_replace": null,
            "multiline_delimiter": null,
            "replace": null,
            "rollback": null
        }
    }
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [ansible.builtin.include_tasks] ******************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:11
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
included: /Users/piyushmalik/dev-workspace/ansible-dev/_populate_config.yaml for ios_device
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Configure interface settings GigabitEthernet0/1] ************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/_populate_config.yaml:2
[WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device
changed: [ios_device] => {
    "banners": {},
    "changed": true,
    "commands": [
        "interface GigabitEthernet0/1",
        "description Management interface do not change"
    ],
    "invocation": {
        "module_args": {
            "after": null,
            "backup": false,
            "backup_options": null,
            "before": null,
            "defaults": false,
            "diff_against": null,
            "diff_ignore_lines": null,
            "intended_config": null,
            "lines": [
                "description Management interface do not change"
            ],
            "match": "line",
            "multiline_delimiter": "@",
            "parents": [
                "interface GigabitEthernet0/1"
            ],
            "replace": "line",
            "running_config": null,
            "save_when": "never",
            "src": null
        }
    },
    "updates": [
        "interface GigabitEthernet0/1",
        "description Management interface do not change"
    ]
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Configure interface settings GigabitEthernet0/2] ************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/_populate_config.yaml:8
changed: [ios_device] => {
    "banners": {},
    "changed": true,
    "commands": [
        "interface GigabitEthernet0/2",
        "description this is interface1",
        "mtu 1500",
        "speed 1000",
        "no shutdown"
    ],
    "invocation": {
        "module_args": {
            "after": null,
            "backup": false,
            "backup_options": null,
            "before": null,
            "defaults": false,
            "diff_against": null,
            "diff_ignore_lines": null,
            "intended_config": null,
            "lines": [
                "description this is interface1",
                "mtu 1500",
                "speed 1000",
                "no shutdown"
            ],
            "match": "line",
            "multiline_delimiter": "@",
            "parents": [
                "interface GigabitEthernet0/2"
            ],
            "replace": "line",
            "running_config": null,
            "save_when": "never",
            "src": null
        }
    },
    "updates": [
        "interface GigabitEthernet0/2",
        "description this is interface1",
        "mtu 1500",
        "speed 1000",
        "no shutdown"
    ]
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Configure interface settings GigabitEthernet0/3] ************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/_populate_config.yaml:17
changed: [ios_device] => {
    "banners": {},
    "changed": true,
    "commands": [
        "interface GigabitEthernet0/3",
        "description this is interface for testing",
        "speed 1000",
        "shutdown"
    ],
    "invocation": {
        "module_args": {
            "after": null,
            "backup": false,
            "backup_options": null,
            "before": null,
            "defaults": false,
            "diff_against": null,
            "diff_ignore_lines": null,
            "intended_config": null,
            "lines": [
                "description this is interface for testing",
                "speed 1000",
                "shutdown"
            ],
            "match": "line",
            "multiline_delimiter": "@",
            "parents": [
                "interface GigabitEthernet0/3"
            ],
            "replace": "line",
            "running_config": null,
            "save_when": "never",
            "src": null
        }
    },
    "updates": [
        "interface GigabitEthernet0/3",
        "description this is interface for testing",
        "speed 1000",
        "shutdown"
    ]
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Gather the provided configuration with the existing running configuration] **********************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:14
ok: [ios_device] => {
    "changed": false,
    "gathered": [
        {
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/0",
            "speed": "auto"
        },
        {
            "description": "Management interface do not change",
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/1",
            "speed": "auto"
        },
        {
            "description": "this is interface1",
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/2",
            "speed": "1000"
        },
        {
            "description": "this is interface for testing",
            "duplex": "auto",
            "enabled": false,
            "name": "GigabitEthernet0/3",
            "speed": "1000"
        }
    ],
    "invocation": {
        "module_args": {
            "config": null,
            "running_config": null,
            "state": "gathered"
        }
    }
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Debug gathered result] **************************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:20
ok: [ios_device] => {
    "result.gathered": [
        {
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/0",
            "speed": "auto"
        },
        {
            "description": "Management interface do not change",
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/1",
            "speed": "auto"
        },
        {
            "description": "this is interface1",
            "duplex": "auto",
            "enabled": true,
            "name": "GigabitEthernet0/2",
            "speed": "1000"
        },
        {
            "description": "this is interface for testing",
            "duplex": "auto",
            "enabled": false,
            "name": "GigabitEthernet0/3",
            "speed": "1000"
        }
    ]
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Assert] *****************************************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:24
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [ansible.builtin.include_tasks] ******************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/gathertest.yml:30
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.
included: /Users/piyushmalik/dev-workspace/ansible-dev/_remove_config.yaml for ios_device
Read `vars_file` '/Users/piyushmalik/dev-workspace/ansible-dev/vars.yaml'.

TASK [Remove configuration] ***************************************************************************
task path: /Users/piyushmalik/dev-workspace/ansible-dev/_remove_config.yaml:2
changed: [ios_device] => {
    "changed": true,
    "commands": [
        "interface GigabitEthernet 0/1",
        "no description",
        "no shutdown",
        "interface GigabitEthernet 0/2",
        "no description",
        "no mtu",
        "no speed",
        "no shutdown",
        "interface GigabitEthernet 0/3",
        "no description",
        "no mtu",
        "no speed",
        "no shutdown"
    ],
    "invocation": {
        "module_args": {
            "backup": false,
            "backup_options": null,
            "commit": null,
            "commit_comment": null,
            "config": "interface GigabitEthernet 0/1\nno description\nno shutdown\ninterface GigabitEthernet 0/2\nno description\nno mtu\nno speed\nno shutdown\ninterface GigabitEthernet 0/3\nno description\nno mtu\nno speed\nno shutdown\n",
            "defaults": false,
            "diff_ignore_lines": null,
            "diff_match": null,
            "diff_replace": null,
            "multiline_delimiter": null,
            "replace": null,
            "rollback": null
        }
    }
}

PLAY RECAP ********************************************************************************************
ios_device                 : ok=13   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

The test playbook and **`vars.yaml`** (expected **`gathered.config`**) stay the same as upstream; only the Ansible inventory target (host/port) points at cisshgo.

If the sequence drifts (extra lines from Ansible, different interface spacing, or **`terminal length 0`** before **`enable`**), capture traffic with **`ansible-playbook … -vvv`** and align **`transcripts/transcript_map.yaml`** the same way as for **ios\_interfaces\_merged**. The first step remains **`enable`** for the same reason as §5.7.

---

##

## **7\. Example: Simple show command (`show privilege`, platform mode)**

Upstream reference for `**cisco.ios.ios_command`\*\*: \[cisco.ios ios\_command `output.yaml](https://github.com/ansible-collections/cisco.ios/blob/main/tests/integration/targets/ios_command/tests/cli/output.yaml)`.

This example uses a **platform** listener (**not** `**scenarios:`\*\*). cisshgo looks up each line the client sends in that platform's `**command_transcripts**` map and returns the matching transcript file. That is enough for a single `**show privilege**` after Ansible runs `**enable**` (privilege is handled via the platform `**context_search**` keys—see `**platforms.csr1000v**` in `**transcripts/transcript_map.yaml**`).

### **7.1 Purpose**

* Show how to **add a new command response** (here `**show privilege`**) for a platform and run `**cisco.ios.ios_command`** against cisshgo without defining a scenario.
* Assert `**stdout**` contains the expected line (e.g. `**Current privilege level is 15**`).

### **7.2 Platform behavior (no scenario)**

1. Start cisshgo with an inventory entry `**platform: csr1000v`\*\* (not `**scenario:**`).
2. On each SSH line, the device uses `**platforms.csr1000v.command_transcripts**` to choose the transcript. The command string must match the map **key** exactly (e.g. `**show privilege`\*\*, not `**show privelege**`).
3. Commands Ansible sends before your task (e.g. `**terminal length 0**`) must either exist under `**command_transcripts**` for that platform or be handled by the generic device logic—if Ansible reports unknown output, capture `**ansible-playbook -vvv**` and add the missing key.

### **7.3 Create the transcript file**

Paths in the map are relative to the directory that contains `**transcripts/transcript_map.yaml`\*\* (the `**transcripts/**` tree next to that file).

1. Create a text file, for example `**transcripts/cisco/ios/show_privilege.txt**` (you can use any subdirectory under `**transcripts/**` that keeps your layout clear).
2. Put the exact device output you want Ansible to parse—one line is enough for a privilege check:

```
Current privilege level is 15
```

Save the file. This repo already ships that file for **csr1000v**; the steps above are what you follow when `**show privilege`\*\* (or any other command) is **not** in your map yet.

### **7.4 Register the command under `command_transcripts`**

Open `**transcripts/transcript_map.yaml**`. Under the platform you use (here `**platforms.csr1000v**`), find the `**command_transcripts:**` block. Add a **key** equal to the command line Ansible sends and a **value** equal to the transcript path **relative to the `transcripts/` directory**.

Example (this matches the current **csr1000v** map; only the `**show privilege`\*\* line is required for this example):

```
platforms:
  csr1000v:
    vendor: "cisco"
    hostname: "cisshgo1000v"
    username: "admin"
    password: "admin"
    command_transcripts:
      "show ip interface brief": "cisco/csr1000v/show_ip_interface_brief.txt"
      "show running-config": "cisco/csr1000v/show_running-config.txt"
      "show version": "cisco/csr1000v/show_version.txt"
      "show privilege": "cisco/ios/show_privilege.txt"
      "terminal length 0": "generic_empty_return.txt"
      # ... other commands ...
```

Rules:

* The key must match what appears on the wire (`**show privilege**`).
* The value is a path under `**transcripts/**` (here `**cisco/ios/show_privilege.txt**` → file `**transcripts/cisco/ios/show_privilege.txt**`).

If your playbook uses a different platform name in cisshgo inventory, add the same `**command_transcripts**` entry under `**platforms.<that_name>**` instead.

### **7.5 cisshgo inventory (platform)**

Use `**platform:`\*\*, not `**scenario:**`. The repo includes `**cisshgo_inventory_simple_show_command.yaml**`:

```
---
# Run: ./cisshgo --inventory cisshgo_inventory_simple_show_command.yaml --listeners 1 --starting-port 10000
devices:
  - platform: csr1000v
    count: 1
```

### **7.6 Sample playbook and running the test**

**Sample playbook** (e.g. `**simple_show_command.yml`\*\*). Set `**hosts**`, `**ansible_host**`, port, `**ansible_connection=ansible.netcommon.network_cli**`, credentials, and `**ansible_become**` / `**ansible_become_password**` like for a real router.

```
---
- name: Simple show command (show privilege) against cisshgo
  hosts: ios
  gather_facts: false
  tasks:
    - name: Run show privilege
      register: result
      cisco.ios.ios_command:
        commands:
          - show privilege

    - name: Assert privilege output
      ansible.builtin.assert:
        that:
          - result.changed == false
          - result.stdout is defined
          - result.stdout | length >= 1
          - "'Current privilege level is 15' in result.stdout[0]"
```

1.
   Start cisshgo:
   `./cisshgo --inventory cisshgo_inventory_simple_show_command.yaml --listeners 1 --starting-port 10000` **(Expected output)** `Starting listener on :10000 [platform=csr1000v hostname=cisshgo1000v user=admin]`
2. Point Ansible at the listener and run:
   `ansible-playbook -i inventory.ini simple_show_command.yml`

**Expected outcome (abbreviated):**

```
TASK [Run show privilege]
ok: [ios_device] => {
    "changed": false,
    "stdout": [
        "Current privilege level is 15"
    ],
    "stdout_lines": [
        [
            "Current privilege level is 15"
        ]
    ],
    ...
}

TASK [Assert privilege output]
ok: [ios_device] => {
    "changed": false,
    "msg": "All assertions passed"
}
```

---

##

## **8\. Gaps and customizations**

### **8.1 Missing transcripts (command coverage gaps)**

* What: Certain commands expected by Ansible (e.g. show privilege during enable, or other operational/config queries) may not have corresponding transcripts in cisshgo. When a command is missing, cisshgo returns "Unknown command," which can cause Ansible tasks to fail (e.g. privilege checks, config tasks, backups) or behave unexpectedly.
* Fix: Add transcripts for all required commands and register them in the transcript map (see "[How to add new transcripts](https://docs.google.com/document/d/11kJDbAKBfHHT0K6Y8WXzmEKJITyejYolSo-DdszYuk0/edit?tab=t.0#heading=h.jzzc4joe0t3m)" below). Each transcript should return output that matches real IOS behavior so that Ansible can correctly parse and validate responses. For example, show privilege must return Current privilege level is 15, but the same principle applies to any command used in playbooks or integration tests.

### **8.2 Unknown-command response format (integration test "invalid command" task)**

* **What:** The cisco.ios integration test sends an **invalid command** (e.g. `show foo`) and **asserts that the task fails** (`result.failed == true`). On real IOS, the device prints something like `% Invalid input detected at '^' marker.` and the Ansible stack treats that as a **failed** task. cisshgo's default was `% Unknown command: "show foo"`, and Ansible did **not** treat that as a failure, so the task **succeeded** and the assertion failed.
* **Fix:** Change cisshgo's **unknown-command** response to match the IOS-style error format (e.g. "Invalid input detected at '^' marker") so that Ansible fails the task and the integration test assertion passes. This is done in the handler/code that generates the unknown-command message, not via a per-command transcript.

### **8.3 Scenario sequencing requirements**

* What: For a scenario to behave correctly, every command that the client sends (and that must change context or return a specific response) must appear in the sequence in the exact order the client sends it. If commands are missing, out of order, or reused incorrectly, the interaction can desynchronize and produce unexpected results in playbooks or tests.
* Details: Commands that only need to return empty output can use generic\_empty\_return.txt as sequence steps. Commands that must return different outputs at different times (e.g. show running-config | section ^interface) must appear multiple times in the sequence with different transcript paths.
* Important: Scenarios apply only in interactive mode. If the client uses exec mode (one command per connection, no PTY), the handler uses only the platform's SupportedCommands and does not execute the sequence. Therefore, integration tests that rely on before/after state must use a persistent connection (e.g. Ansible network\_cli with a single session per play).

### **8.4 Vendor parity (handlers, errors, and per-OS work)**

* What: cisshgo's interactive SSH path is built around Cisco-style CLI behavior: IOS-like prompts, context handling (enable, config modes), and generic error lines such as % Invalid input detected at '^' marker. and % Ambiguous command: … when a command does not match the map. Platforms listed in transcript\_map.yaml (e.g. csr1000v, eos, junos, nxos) are primarily data-driven—command\_transcripts, context\_search, prompts—not separate full emulators of each vendor's shell. Supporting arista.eos, junipernetworks.junos, or other collections end-to-end is not "reuse IOS transcripts as-is"; it requires substantial per-OS work: transcripts that match what those modules parse, vendor-accurate error strings for negative tests where asserted, and privilege / configuration flows that match that NOS (not IOS enable \+ show privilege alone).
* Fix / approach: Treat each target OS as its own integration effort: add and maintain command → transcript entries (and scenarios where order matters) under the appropriate platforms.\* (or scenarios.\*) blocks; align failure output with what each collection's tests expect (IOS-style % errors may not satisfy Junos- or EOS-shaped asserts). Where cisshgo's fixed unknown-command string is IOS-oriented, document or extend behavior for other vendors if those tests are in scope. Scope documentation honestly: cisshgo is a strong fit for bounded, CLI-heavy Cisco-style suites; full parity across all Ansible Network collections requires ongoing per-vendor transcript and validation work, not a single shared profile.
* Important: Negative tests are especially sensitive: many suites assert on vendor-specific error text. A message shaped for cisco.ios (see §8.2) may not match tests written for other NOSes—those may need different transcript or handler behavior, not only more command\_transcripts keys.

##

##

## **9\. Summary**

|  |  |
| ----- | ----- |
|  |  |
| **Topic** | **Detail** |
| **What** | A scenario is an ordered list of (command → transcript) steps on top of a platform. |
| **When** | Used only when cisshgo is started with \--inventory and an entry has `scenario: <name>`. |
| **How** | Per-session pointer; each matching command advances the pointer and returns that step's transcript; context switches apply only when the step matched. |
| **Setup** | 1\) Get exact command order (e.g. from \-vvv). 2\) Add transcripts. 3\) Define scenario in transcript map. 4\) Create cisshgo inventory with scenario:. 5\) Run cisshgo with \--inventory. 6\) Point test at host/port. |
| **Example** | **ios\_interfaces\_merged:** scenario; section before/after transcripts. **ios\_interfaces\_gathered:** scenario; **section\_gathered**. **Simple show command:** **platform** `**csr1000v`\*\*; `**command_transcripts**` key `**show privilege**` → transcript file; `**ios_command**`. |
