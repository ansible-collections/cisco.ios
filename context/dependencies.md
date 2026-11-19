# Dependency Chain — cisco.ios

## The Dependency Graph

```
ansible-core (upstream)
    │
    ▼
ansible.netcommon  ──────────────────────────────┐
    │  (connection plugins, base classes,         │
    │   rm_templates, cli_parse)                  │
    ▼                                             ▼
cisco.ios                                   cisco.iosxr
    │                                       cisco.nxos
    │                                       arista.eos
    │                                       (all depend on netcommon)
    ▼
ansible.utils (indirect — via netcommon)
```

## Cascade Risk

A breaking change in `ansible.netcommon` or `ansible.utils` can fail CI across all
downstream collections simultaneously. This is called a **cascade failure**.

**If netcommon CI breaks:**

1. Check if it's a Galaxy lag issue (Pattern 1 in `ci-patterns.md`)
2. Check if a recent netcommon PR introduced a regression
3. Check `ansible.utils` version — a utils bump can cascade through netcommon to ios

**If your ios PR fails only on `unit-galaxy` and `unit-source` passes:**
→ It's almost certainly a Galaxy lag. Cut a netcommon release.

---

## Release Coordination

### When cisco.ios needs a netcommon fix

1. Merge the fix in netcommon first
2. Request/cut a netcommon Galaxy release (ask @ansible-network/netcommon-maintainers)
3. Update `requirements.txt` in cisco.ios if the minimum version changed
4. Update `galaxy.yml` `dependencies` block if needed:
   ```yaml
   dependencies:
     ansible.netcommon: ">=8.1.0"
     ansible.utils: ">=5.0.0"
   ```
5. Merge cisco.ios PR only after netcommon release is live on Galaxy

### When to add `Depends-On`

If a cisco.ios PR depends on an open netcommon PR, add to the PR description:

```
Depends-On: https://github.com/ansible-collections/ansible.netcommon/pull/<number>
```

This prevents accidental merge before the dependency is ready.

---

## Current Pinned Versions

From `galaxy.yml` (as of 11.4.2):

```yaml
dependencies:
  ansible.netcommon: ">=8.1.0"
  ansible.utils: ">=5.0.0"
```

From `requirements.txt` (test installs):

```
ansible-core>=2.16
ansible.netcommon>=8.1.0
ansible.utils>=5.0.0
```

---

## netcommon Plugins Used by cisco.ios

| Plugin                                        | Purpose                           | Relevant when                  |
| --------------------------------------------- | --------------------------------- | ------------------------------ |
| `connection/network_cli.py`                   | Main connection mechanism for IOS | Any connection-level bug       |
| `connection/persistent.py`                    | Underlying persistent socket      | Timeout/state leak bugs        |
| `module_utils/network/common/rm_templates.py` | Base class for RM parsers         | Adding/fixing resource modules |
| `module_utils/network/common/utils.py`        | Utility functions                 | Parsing, comparison logic      |
| `plugins/action/network.py`                   | Network action plugin base        | Action-level failures          |
| `plugins/filter/*.py`                         | Jinja2 filters (ipaddr, etc.)     | Template-based tasks           |

When one of these breaks, all collections using them break simultaneously.

---

## ansible.utils Plugins Used

| Plugin                          | Purpose                                  |
| ------------------------------- | ---------------------------------------- |
| `validate` module               | Validate device data against JSON Schema |
| `fact_diff` module              | Show diffs in gathered/rendered output   |
| `get_path` / `set_path` filters | Navigate nested data structures          |

ansible.utils version bumps occasionally drop Python 3.9 support — check when updating.
