# GitHub Issue Triage & Reproduction

## Step 1: Fetch the issue
```
gh issue view <issue_number> --repo ansible-collections/cisco.ios
```

## Step 2: Understand the issue
- What module is affected?
- What state is being used (merged/replaced/deleted/etc.)?
- What IOS version is the reporter using?
- What is the expected behavior vs actual behavior?
- Is there a playbook and running config provided?

## Step 3: Ask for device details
Prompt the user for:
- **Device type**: Router or Switch (IOS or IOS-XE)
- **IOS version**: e.g., 17.3.x, 17.6.x, 17.9.x
- **Connection method**: network_cli (default), or httpapi
- **SSH backend**: libssh or paramiko
- If they have access to a device or are using CISSHGO simulator

## Step 4: Analyze the code path
1. Read the module's argspec to understand valid parameters
2. Read the rm_templates to understand how CLI output is parsed (getval regex) and generated (setval)
3. Read the config class to understand state handling logic
4. Read the facts class to understand what show command is used

## Step 5: Reproduce locally
If the user has a running config sample:
- Use `state: parsed` with `running_config` to test parsing without a device
- Compare parsed output with expected structure
- Use `state: rendered` to test command generation without a device
- Write a unit test that reproduces the issue

## Step 6: Determine root cause
Common bug patterns:
- **Regex mismatch**: `getval` regex doesn't capture all variations of the CLI output
- **Setval template error**: Generated command has wrong syntax
- **Missing parser**: A CLI sub-command isn't covered by any parser
- **State logic bug**: `generate_commands()` doesn't handle a state correctly
- **Idempotency failure**: Module generates commands on second run (diff between parsed facts and desired config)
- **Version-specific CLI**: Newer IOS versions have different command syntax

## Step 7: Validate fix
- Write a unit test with the reporter's running config
- Verify all states produce correct commands
- Verify idempotency (second run should show `changed: false`)
- Check that the fix doesn't break existing tests: `python -m pytest tests/unit/modules/network/ios/test_ios_<resource>.py -v`
