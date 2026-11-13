# Resource Module Flow & Want/Have State Logic

(Source: https://github.com/ansible-community/ansible.content_builder/blob/main/docs/rm_dev_guide.md)

## How a Resource Module Works — Plain Language

Imagine you write this in a playbook:
```yaml
- cisco.ios.ios_interfaces:
    config:
      - name: GigabitEthernet1
        description: "My uplink"
        enabled: true
    state: merged
```

Here's what happens step by step:

1. **Ansible connects to the device** using SSH (network_cli connection). The action plugin validates that you're using the right connection type.

2. **The module starts up** and passes your input (`config` + `state`) to the Config class.

3. **Facts gathering ("What does the device have now?")**: The Facts class runs a `show running-config` command on the device and gets back raw text like:
   ```
   interface GigabitEthernet1
    description Old description
    no shutdown
   ```

4. **Parsing ("Turn text into data")**: The RM Template's `getval` regexes scan each line of that text and build a structured Python dictionary:
   ```python
   {"name": "GigabitEthernet1", "description": "Old description", "enabled": True}
   ```
   This becomes `self.have` — what the device has right now.

5. **Your input becomes `self.want`** — what you want the device to look like.

6. **Comparison ("What needs to change?")**: The Config class compares `want` vs `have`:
   - `description` changed from "Old description" to "My uplink" → needs update
   - `enabled` is already True → no change needed

7. **Command generation**: For each difference, the RM Template's `setval` Jinja2 template generates the CLI command:
   ```
   interface GigabitEthernet1
   description My uplink
   ```

8. **Apply changes**: The generated commands are sent to the device.

9. **Return results**: The module returns `changed: true`, the list of commands it ran, and the before/after state.

### The states in plain language:

- **merged**: "Add or update these settings, but don't touch anything else"
- **replaced**: "Make this specific resource look exactly like this — remove anything extra on it"
- **overridden**: "Make ALL resources of this type match my list — remove anything not in my list"
- **deleted**: "Remove the specified settings (or all settings if no config given)"
- **purged**: "Delete the entire resource entry (e.g., remove the interface completely)"
- **gathered**: "Just tell me what's on the device right now — don't change anything"
- **rendered**: "Show me what CLI commands would be generated — don't talk to any device"
- **parsed**: "Parse this config text I'm giving you — don't talk to any device"

### The 5 files in plain language:

1. **Module** (`ios_<resource>.py`): The front door — validates input, kicks off the process
2. **Argspec**: The bouncer — defines what input is valid (what keys, what types, what choices)
3. **RM Template**: The translator — converts between CLI text and Python dicts (both directions)
4. **Config**: The brain — decides what commands to generate based on current vs desired state
5. **Facts**: The reporter — asks the device "what do you have?" and parses the answer

---

## Want vs Have — State Comparison Tables

The core of every resource module is the comparison between `want` (what the user asked for)
and `have` (what the device currently has). The tables below use set notation:
- `{A, B, C}` = config attributes present
- `nX` = negate/remove attribute X
- `rX` = replace attribute X

### MERGED

Only pushes items in WANT that are missing from HAVE. Additive — never removes anything.

```
|     WANT      |     HAVE      |    Output     |  Comment  |
| :-----------: | :-----------: | :-----------: | :-------: |
| {A, B, C, D}  |   {A, B, E}   |    {C, D}     |  Changed  |
|      {}       | {A,B,C,D,E}   |      {}       | No change |
| {A, B, C, D}  |      {}       | {A, B, C, D}  |  Changed  |
```

Example: WANT={desc: "new", mtu: 1500}, HAVE={desc: "old", speed: 100}
→ Output: `description new`, `mtu 1500` (speed 100 is NOT removed)

### REPLACED

Replaces matching items, removes items in HAVE not in WANT. Scoped to specified resources only.

```
|    WANT     |     HAVE       |        Output          |    Comment     |
| :---------: | :------------: | :--------------------: | :------------: |
| {A, C, D}   | {A, B, E, F}   | {rA, nB, nE, nF, C, D} | Changed A,C,D |
```

Example: WANT={desc: "new"}, HAVE={desc: "old", mtu: 1500, speed: 100}
→ Output: `description new`, `no mtu 1500`, `no speed 100`
Note: resources NOT listed in WANT are left completely alone.

### OVERRIDDEN

Like replaced but across ALL resource instances. Removes entire entries not in WANT.

```
|     WANT      |    HAVE     |           Output            |  Comment  |
| :-----------: | :---------: | :-------------------------: | :-------: |
| {A, B, C, D}  |  {A, B, E}  |     {A, B, nE, C, D}        |  Changed  |
| {A, B, C, D}  |     {}      |      {A, B, C, D}           |  Changed  |
| {A, B, C, D}  |  {E, F, G}  | {nE, nF, nG, A, B, C, D}    |  Changed  |
```

Example: WANT specifies GE1 and GE2. Device has GE1, GE2, GE3.
→ GE3 gets all its config removed (reset to defaults).
Warning: This can remove config from resources the user didn't mention!

### DELETED

Negates/removes specified config items.

```
|     WANT      |    HAVE       |       Output        |  Comment  |
| :-----------: | :-----------: | :-----------------: | :-------: |
|      {}       | {A,B,C,D,E}   | {nA,nB,nC,nD,nE}   |  Changed  |
| {A, B, C, D}  |      {}       |        {}           | No Change |
| {A, B, C, D}  |   {E, F, G}   |        {}           | No Change |
```

When WANT is empty, ALL resources get deleted.
When WANT specifies items not in HAVE, nothing changes.

### PURGED

Deletes the entire top-level resource entry:
```
Similar to deleted, but removes the context command itself.
→ Example: "no interface Loopback999" (deletes the whole interface)
vs deleted which just removes config under the interface.
```

### RENDERED

Pass in a config with rendered state, it tells you all the CLI commands that would
be formed from the supplied config, without connecting to the target device. Different from check mode.

### PARSED

Opposite of rendered. Supply raw `running_config` text from a device, get back
structured data showing how the invocation/facts would look. No device connection needed.

### GATHERED

Connects to device, runs show commands, returns current config as structured data.
No changes are made to the device.

---

## How the Config Code Implements State Logic

The config class (`generate_commands()`) translates these tables into code:

```python
def generate_commands(self):
    wantd = {entry["<key>"]: entry for entry in self.want}   # playbook config
    haved = {entry["<key>"]: entry for entry in self.have}    # device facts

    # MERGED: overlay want on have, then compare
    if self.state == "merged":
        wantd = dict_merge(haved, wantd)

    # DELETED/PURGED: swap — have becomes the target, want is empty
    if self.state in ["deleted", "purged"]:
        haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
        wantd = {}

    # OVERRIDDEN/DELETED: remove items in have but not in want
    if self.state in ["overridden", "deleted"]:
        for k, have in haved.items():
            if k not in wantd:
                self._compare(want={}, have=have)

    # PURGED: remove entire resource entries
    if self.state == "purged":
        for k, have in haved.items():
            self.purge(have)
    else:
        # All other states: compare each want item with its have counterpart
        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))
```

---

## list_to_dict — Critical for Comparison

The `compare()` method works best with dictionaries of dictionaries, NOT lists of dictionaries.
Before comparison, convert all list attributes to dicts using a unique key.

```python
# BAD — lists are hard to compare
want = [{"name": "GE1", "desc": "a"}, {"name": "GE2", "desc": "b"}]
have = [{"name": "GE2", "desc": "b"}, {"name": "GE1", "desc": "old"}]

# GOOD — dicts keyed by unique identifier
wantd = {"GE1": {"name": "GE1", "desc": "a"}, "GE2": {"name": "GE2", "desc": "b"}}
haved = {"GE1": {"name": "GE1", "desc": "old"}, "GE2": {"name": "GE2", "desc": "b"}}
```

This applies to EVERY list attribute in the data model, not just the top level.
Implement `list_to_dict` on every list attribute at the entry point of config code,
before it starts getting processed on the basis of states.

A comparison of two dictionary of dictionaries is easier and more efficient than
a comparison of two lists of dictionaries. To optimally leverage the RMEngineBase,
convert all lists to dicts of dicts before starting the comparison process.

Reference implementations:
- cisco.nxos.route_maps: `config/route_maps/route_maps.py`
- arista.eos.bgp_global: `config/bgp_global/bgp_global.py`
- cisco.iosxr.bgp_global: `config/bgp_global/bgp_global.py`

---

## Parser Namespace and compval

The `self.parsers` list in config code uses dot-notation to control comparison depth.

```python
# Parser named "key1" → compares the whole dict under key1
haved = {"key1": {"key2": 100}}
wantd = {"key1": {"key2": 10}}
# → Compares {"key2": 100} vs {"key2": 10} → changed

# Parser named "key1.key2" → compares only the value at key2
# → Compares 100 vs 10 → changed
```

Adding parser names in namespace format helps the `compare()` method reduce
the namespace based on the dictionary it is looking at and compute the setval
on that basis.

### compval override

The `compval` parser template key overrides the default namespace extraction:

```python
want = {"k1": {"k2": {"k3": "newval", "k4": "anotherval"}}}
have = {"k1": {"k2": {"k3": "oldval", "k4": "anotherval"}}}

# Parser name "k1.k2.k3" → extracts and compares k3 values:
#   "newval" vs "oldval" → changed

# But with compval: "k1.k2" → extracts and compares k2 dicts:
#   {"k3": "newval", "k4": "anotherval"} vs {"k3": "oldval", "k4": "anotherval"} → changed
```

Use `compval` when parsers are broken down into multiple ones and referenced
as namespaces, but you want comparison at a different level than the parser name suggests.

There is no direct relation between the `result` key and `setval` key in parsers.
The data available at setvals to generate commands may or may not align with facts/results.
It depends on the flattening logic in config code which molds `wantd` and `haved` for comparison.
