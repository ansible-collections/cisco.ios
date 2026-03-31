# ios_interfaces Integration Tests with CISSHGO

This Molecule scenario runs `cisco.ios.ios_interfaces` integration tests against
[CISSHGO](https://github.com/nleiva/cisshgo) — a Go-based SSH fixture server that
emulates Cisco IOS devices using pre-recorded transcripts.

## Why CISSHGO?

| Aspect | CML Labs | CISSHGO |
|--------|----------|---------|
| Startup time | 2-5 minutes | < 1 second |
| Licensing | Required | None |
| Determinism | Variable (network, timing) | 100% deterministic |
| Parallelism | Limited by lab resources | Unlimited (just ports) |
| CI cost | CML infrastructure | Single Go binary |
| Stack tested | Full (SSH → module) | Full (SSH → module) |

## Prerequisites

- Python 3.x with `molecule` and `ansible` installed
- Go 1.19+ (to build cisshgo) — or a pre-built `cisshgo` binary
- `cisco.ios` and `ansible.netcommon` collections installed

```bash
pip install molecule ansible
ansible-galaxy collection install cisco.ios ansible.netcommon
```

## Quick Start

```bash
# From the cisco.ios collection root
cd /path/to/ansible_collections/cisco/ios

# Set the path to your cisshgo repo (or binary)
export CISSHGO_REPO_PATH=/path/to/cisshgo

# Run the full test lifecycle (create → converge → verify → destroy)
molecule test -s cisshgo_ios_interfaces

# Or run individual phases:
molecule create -s cisshgo_ios_interfaces    # Build & start cisshgo
molecule converge -s cisshgo_ios_interfaces  # Run tests
molecule verify -s cisshgo_ios_interfaces    # Check for unknown commands
molecule destroy -s cisshgo_ios_interfaces   # Stop & cleanup
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CISSHGO_REPO_PATH` | `../../cisshgo` (relative) | Path to cisshgo source repo |
| `CISSHGO_BIN_PATH` | (none) | Path to pre-built binary (skips build) |
| `CISSHGO_PORT` | `10000` | Starting port for cisshgo listeners |

## Test Coverage

| State | Mode | Port | What's Tested |
|-------|------|------|---------------|
| `gathered` | Platform (stateless) | 10000 | Facts gathering from running config |
| `merged` | Scenario (stateful) | 10001 | Config merge + idempotency |
| `replaced` | Scenario (stateful) | 10002 | Config replace + idempotency |
| `parsed` | Offline (no device) | — | Config file parsing |
| `rendered` | Offline (no device) | — | CLI command rendering |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Molecule                                                     │
│                                                              │
│  create.yml ──► Build cisshgo ──► Start on ports 10000-10002 │
│                                                              │
│  converge.yml ──► Run 5 test plays:                          │
│    │  gathered ──► port 10000 (platform mode, stateless)     │
│    │  merged   ──► port 10001 (scenario mode, stateful)      │
│    │  replaced ──► port 10002 (scenario mode, stateful)      │
│    │  parsed   ──► no device needed (offline)                │
│    │  rendered ──► no device needed (offline)                │
│    │                                                         │
│    │  Each test uses vars from:                              │
│    │    tests/integration/targets/ios_interfaces/vars/main.yaml
│    │  Same assertions as original integration tests          │
│                                                              │
│  verify.yml ──► Check cisshgo logs for unknown commands      │
│  destroy.yml ──► Kill cisshgo, remove temp files             │
└─────────────────────────────────────────────────────────────┘

CISSHGO Command Dispatch:
┌──────────────────────────────────────┐
│  SCENARIO LAYER (if scenario mode)   │
│  sequence[pointer] matches command?  │
│    YES → return transcript, advance  │
│    NO  → fall through                │
└──────────────────────────────────────┘
          ↓ (no match)
┌──────────────────────────────────────┐
│  PLATFORM LAYER (always available)   │
│  command_transcripts{} lookup        │
│  Serves: show privilege, terminal    │
│  length 0, show version, etc.        │
└──────────────────────────────────────┘
```

## Adding a New Test State

To add support for a new state (e.g., `deleted` or `overridden`):

1. **Create transcript files** in `cisshgo_fixtures/transcripts/scenarios/ios-interfaces-<state>/`:
   - `before.txt` — Device config before the module runs
   - `after.txt` — Device config after the module applies changes

2. **Add scenario to `transcript_map.yaml`**:
   ```yaml
   scenarios:
     ios-interfaces-deleted:
       platform: ios
       sequence:
         - command: "show running-config | section ^interface"
           transcript: "scenarios/ios-interfaces-deleted/before.txt"
         # ... config commands from vars/main.yaml deleted.commands ...
         - command: "show running-config | section ^interface"
           transcript: "scenarios/ios-interfaces-deleted/after.txt"
   ```

3. **Add device to `cisshgo_inventory.yaml`**:
   ```yaml
   devices:
     - scenario: ios-interfaces-deleted
       count: 1
   ```

4. **Add platform to `molecule.yml`** with the next port number.

5. **Add test play to `converge.yml`** following the existing pattern.

## Troubleshooting

**"Unknown command" in verify step:**
Check `.cisshgo.log` to see which command Ansible sent that wasn't in the transcript map.
Add it to the platform's `command_transcripts` or the scenario's `sequence`.

**Port already in use:**
```bash
lsof -ti:10000 | xargs kill  # Kill process on port 10000
```

**Assertion failures:**
Compare `result['before']` / `result['after']` with `vars/main.yaml` expected values.
The transcript `.txt` files must produce output that the `ios_interfaces` module parses
into the exact same structured data.

## Relationship to Original Tests

This scenario adapts the tests from `tests/integration/targets/ios_interfaces/`.
The key differences from running against real devices:

| Original Test | CISSHGO Adaptation |
|---------------|-------------------|
| `_remove_config.yaml` runs to clean device | Not needed — cisshgo starts fresh |
| `_populate_config.yaml` sets up baseline | Baked into scenario `before.txt` |
| Tests run against single device | Each state gets its own port/scenario |
| Requires CML lab + credentials | Requires only `cisshgo` binary |
| Assertions from `vars/main.yaml` | Same assertions, same expected values |
