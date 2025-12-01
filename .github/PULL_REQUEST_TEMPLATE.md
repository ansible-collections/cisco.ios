## Description
<!-- Mandatory: Provide a clear, concise description of the changes and their purpose -->
- What is being changed?
- Why is this change needed?
- How does this change address the issue?

## Type of Change
<!-- Mandatory: Check one or more boxes that apply -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] New module (adding a new module to the collection)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Test update
- [ ] Refactoring (no functional changes)
- [ ] Collection release
- [ ] CI maintenance
- [ ] Workflow maintenance
- [ ] Configuration change

## Related Issue
<!-- Optional: Link to related issue(s) -->
- Fixes #
- Related to #

## Component Name
<!-- Mandatory: Specify the module, plugin, or component being changed -->
<!-- Examples: ios_config, ios_bgp_global, cliconf plugin, terminal plugin, etc. -->

## Self-Review Checklist
<!-- These items help ensure quality - they complement our automated CI checks -->
- [ ] I have performed a self-review of my code
- [ ] I have added relevant comments to complex code sections
- [ ] I have removed all commented code (no commented code should be merged)
- [ ] I have updated documentation where needed
- [ ] I have considered the security impact of these changes
- [ ] I have considered performance implications
- [ ] I have thought about error handling and edge cases
- [ ] I have tested the changes in my local environment
- [ ] I have verified the changes work with the target IOS version(s)
- [ ] I have reviewed the acceptance criteria for related tickets

## Testing Instructions
<!-- Mandatory for all changes: Must be detailed enough for reviewers to reproduce -->
### Prerequisites
<!-- List any specific setup required (e.g., IOS version, hardware platform, test topology) -->
- IOS Version:
- Hardware Platform (if applicable):
- Test Topology:

### Steps to Test
1.
2.
3.

### Expected Results
<!-- Describe what should happen after following the steps -->

### Test Results
<!-- Paste test output or describe test results -->
```
```

## Acceptance Criteria Verification
<!-- Mandatory: Verify that all acceptance criteria from the related ticket are met -->
- [ ] All acceptance criteria have been reviewed and verified
- [ ] Acceptance criteria checklist:
  - [ ]
  - [ ]
  - [ ]

## Additional Context
<!-- Optional but helpful information -->
<!-- Include additional information to help people understand the change here -->
<!-- A step-by-step reproduction of the problem is helpful if there is no related issue -->

### Command Output / Logs
<!-- Paste verbatim command output below, e.g. before and after your change -->
```
<!-- Paste below -->
```

### Required Actions
<!-- Check if changes require work in other areas -->
<!-- Remove section if no external actions needed -->
- [ ] Requires documentation updates
  <!-- Module documentation, examples, platform guides -->
- [ ] Requires changelog fragment
  <!-- Create changelog fragment if this is a user-facing change -->
- [ ] Requires integration test updates
- [ ] Requires unit test updates
- [ ] Requires coordination with other teams
- [ ] Blocked by PR/MR: #XXX
  <!-- Reference blocking PRs/MRs with brief context -->

### Screenshots/Logs
<!-- Add if relevant to demonstrate the changes -->
<!-- Include device output, error messages, or test results -->

### Breaking Changes
<!-- If this is a breaking change, describe the impact and migration path -->
<!-- Remove section if not applicable -->
