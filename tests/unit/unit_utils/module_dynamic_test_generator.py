import yaml


class TestGeneratorFromModuleExamples:
    def __init__(self, module):
        self.documentation = module.DOCUMENTATION
        self.examples = module.EXAMPLES
        self.module_fqcn = self.identify_yaml(self.documentation).get("module")
        self.module_fqcn = "cisco.ios." + self.module_fqcn
        self.action_state_artifact = {}
        self.non_action_state_artifact = {}

        self.raw_asset = self.extract_test_asset_from_example()

    @property
    def get_action_state_artifact(self):
        self.action_state_artifact = self.raw_asset.get("action_state")
        return self.action_state_artifact

    @property
    def get_non_action_state_artifact(self):
        self.non_action_state_artifact = self.raw_asset.get("non_action_state")
        return self.non_action_state_artifact

    def identify_yaml(self, string_data):
        try:
            yaml_data = yaml.safe_load(string_data)
            if yaml_data is None:
                return False
            return yaml_data
        except yaml.YAMLError:
            return False

    def find_state(self, raw_example_doc):
        # function to just scrap out state
        states = [
            "merged",
            "replaced",
            "overridden",
            "purged",
            "gathered",
            "rendered",
            "parsed",
            "deleted",
            "present",
            "absent",
        ]

        for state in states:
            if state in raw_example_doc[0].lower():
                return state

    def state_helper(self, state):
        # changed parameter value
        if state in ["rendered", "gathered", "parsed"]:
            return False
        else:
            return True

    def find_device_config(self, section_before, state):
        device_config = ""
        if state != "rendered":
            section_before = section_before[1].replace("#", "")
            section_before = section_before.split(
                "\n",
            )

            for line in section_before:
                # think about this line, deeply
                # and "show running-config" not in line
                if line != "" and "show running-config" not in line:
                    line = line[1::]
                    device_config += line + "\n"
            # device_config = dedent(device_config)  # before config is stored
        return device_config[:-1]

    def find_playbook(self, section_playbook):
        probable_playbook = "- name" + section_playbook[0]
        playbook_yaml = self.identify_yaml(
            probable_playbook,
        )  # playbook is scrapped out
        if playbook_yaml:
            return playbook_yaml
        else:
            return ""

    def find_config_in_playbook(self, playbook_yaml, module_fqcn, state):
        section = "running_config" if state == "parsed" else "config"
        config = playbook_yaml[0][module_fqcn].get(section)
        return config

    def find_assert_asset(self, raw_output, state):
        if state in ["rendered", "gathered", "parsed"]:
            split_str = "# " + state + ":"
            extract_commands = (raw_output[1].split(split_str))[1]
            # if state == "gathered":
            #     extract_commands = "gathered:" + extract_commands
        else:
            extract_commands = (raw_output[1].split("# commands:"))[1]
            extract_commands = extract_commands.split("after:")[0]
            # extract_commands = "commands:" + extract_commands

        assert_asset = self.identify_yaml(
            extract_commands.replace("#", ""),
        )
        if assert_asset:
            return assert_asset
        else:
            return ""

    def section_delimiter(self, section):
        section_map = {
            "states": "# Using",
            "name": "- name",
            "dotline": "-------------",
            "taskop": "# Task Output",
        }

        return section_map[section]

    def extract_test_asset_from_example(self):
        """
        Extracts test data from documentation and returns it as a dictionary.
        """

        test_assets, pkey = {"action_state": {}, "non_action_state": {}}, ""
        examples_split = self.examples.split(self.section_delimiter("states"))

        for idx, example in enumerate(examples_split):
            if len(example) < 6:
                continue

            split_on_yaml_name = example.split(self.section_delimiter("name"))
            section_config = split_on_yaml_name[0].split(self.section_delimiter("dotline"))
            playbook_and_output = split_on_yaml_name[1].split(self.section_delimiter("taskop"))

            state = self.find_state(section_config)
            device_config = self.find_device_config(section_config, state)
            playbook_yaml = self.find_playbook(playbook_and_output)
            changed_parm = self.state_helper(state)
            config = self.find_config_in_playbook(playbook_yaml, self.module_fqcn, state)
            assert_asset = self.find_assert_asset(playbook_and_output, state)

            toggle_artifact = "action_state" if changed_parm else "non_action_state"

            pkey = state
            if test_assets[toggle_artifact].get(state):
                pkey = state + "_" + str(idx)

            test_assets[toggle_artifact][pkey] = {
                "state": state,
                "device_config": device_config,
                "playbook": playbook_yaml,
                "config": config,
                "changed": changed_parm,
                "commands": assert_asset,
            }

        return test_assets
