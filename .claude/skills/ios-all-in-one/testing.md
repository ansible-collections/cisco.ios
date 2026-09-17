# Testing Patterns & Test Coverage

## Unit Test Pattern

```python
class TestIos<Resource>Module(TestIosModule):
    module = ios_<resource>

    def setUp(self):
        super().setUp()
        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils."
            "network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()
        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios."
            "facts.<resource>.<resource>.<Resource>Facts.get_<resource>_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super().tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_<resource>_merged(self):
        self.execute_show_command.return_value = dedent("""\
            <running config output here>
        """)
        set_module_args({"config": [...], "state": "merged"})
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted([
            "<expected>", "<commands>",
        ]))

    def test_ios_<resource>_merged_idempotent(self):
        self.execute_show_command.return_value = dedent("""\
            <config that already matches desired state>
        """)
        set_module_args({"config": [...], "state": "merged"})
        self.execute_module(changed=False)
```

## Molecule Test Pattern

Each scenario has platforms for each state, each connected to a CISSHGO instance
on a unique port. The CISSHGO transcript map defines what CLI output each
simulated device returns for each command.

---

## Test Coverage Gap Detection

### How to find missing test cases

**Unit tests** — check coverage for each module:
```bash
# Check which states are tested
grep -c "def test_ios_<resource>_" tests/unit/modules/network/ios/test_ios_<resource>.py

# Expected test methods per module (minimum):
# test_ios_<resource>_merged
# test_ios_<resource>_merged_idempotent
# test_ios_<resource>_replaced
# test_ios_<resource>_replaced_idempotent
# test_ios_<resource>_overridden
# test_ios_<resource>_overridden_idempotent
# test_ios_<resource>_deleted
# test_ios_<resource>_deleted_idempotent
# test_ios_<resource>_gathered
# test_ios_<resource>_parsed
# test_ios_<resource>_rendered
```

**What to check in each test:**
- Does the test cover all options in the argspec?
- Does the running config fixture include all possible sub-commands?
- Are edge cases covered (empty config, partial config, negated commands)?
- Is idempotency tested for each state?

**Molecule tests** — check coverage:
```bash
# List which states are covered in converge.yml
grep "state:" extensions/molecule/<resource>/converge.yml

# Check if RTT (round-trip test) exists
grep -l "rtt\|round.trip\|RTT" extensions/molecule/<resource>/converge.yml
```

**Finding modules with missing tests:**
```bash
# Modules without unit tests
for mod in plugins/modules/ios_*.py; do
  name=$(basename "$mod" .py)
  test="tests/unit/modules/network/ios/test_${name}.py"
  [ ! -f "$test" ] && echo "MISSING: $test"
done

# Modules without molecule tests
for mod in plugins/modules/ios_*.py; do
  name=$(basename "$mod" .py | sed 's/^ios_//')
  dir="extensions/molecule/$name"
  [ ! -d "$dir" ] && echo "MISSING: $dir"
done
```

### Writing missing test cases

When you identify a missing test case:
1. Look at an existing test for a similar module as a template
2. Create a running config fixture that exercises the missing feature
3. Write the test method following the naming convention
4. Assert both `commands` and `changed` status
5. Always include an idempotency test
