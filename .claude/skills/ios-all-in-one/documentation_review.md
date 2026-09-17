# Documentation Review & Typo Fixing

## Where documentation lives
Module documentation is in the `DOCUMENTATION`, `EXAMPLES`, and `RETURN` docstrings at the top of each module file (`plugins/modules/ios_<resource>.py`).

## Common documentation issues to check

**DOCUMENTATION block:**
- `module:` must match filename (e.g., `ios_interfaces` for `ios_interfaces.py`)
- `short_description:` should be concise, end with a period
- `description:` must accurately describe what the module does
- `version_added:` must be correct for when the module was added
- `author:` list must include original authors
- `notes:` should mention tested IOS version and connection type
- All `options:` must match the argspec exactly (type, choices, required, default)
- `suboptions:` nesting must match argspec nesting
- Check for typos in description text, option names, and choice values
- Ensure `type:` is specified for every option
- Check `choices:` lists are complete and correct

**EXAMPLES block:**
- Must show valid, runnable playbook tasks
- Should cover all states (merged, replaced, overridden, deleted, gathered, rendered, parsed)
- Must use fully qualified collection name (`cisco.ios.ios_<resource>`)
- Variable names should be clear and descriptive
- Should demonstrate common use cases
- Register results with `register:` for states that return useful data

**RETURN block:**
- Must document `before_state`, `after_state`, `commands`
- Types must be accurate (list, dict, str, bool)

## Fixing documentation typos
When you find a typo:
1. Fix it in the `DOCUMENTATION` string in the module file
2. If the fix changes option descriptions or types, verify the argspec still matches
3. The argspec is auto-generated from DOCUMENTATION by `ansible.content_builder` — if you change option structure in DOCUMENTATION, regenerate the argspec or update it manually
4. Run `ansible-test sanity --test validate-modules plugins/modules/ios_<resource>.py` to verify docs match argspec

## Adding missing examples
When adding examples to a module:
```yaml
EXAMPLES = """
- name: Merge <resource> configuration
  cisco.ios.ios_<resource>:
    config:
      - <key>: <value>
        <nested_option>:
          <sub_key>: <sub_value>
    state: merged

- name: Replace <resource> configuration
  cisco.ios.ios_<resource>:
    config:
      - <key>: <value>
    state: replaced

- name: Delete <resource> configuration
  cisco.ios.ios_<resource>:
    config:
      - <key>: <value>
    state: deleted

- name: Gather <resource> facts
  cisco.ios.ios_<resource>:
    state: gathered

- name: Parse <resource> from file
  cisco.ios.ios_<resource>:
    running_config: "{{ lookup('file', './running_config.txt') }}"
    state: parsed

- name: Render <resource> commands
  cisco.ios.ios_<resource>:
    config:
      - <key>: <value>
    state: rendered
"""
```
