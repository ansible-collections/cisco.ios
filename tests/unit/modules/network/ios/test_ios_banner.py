# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_banner
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule, load_fixture


class TestIosBannerModule(TestIosModule):
    module = ios_banner

    def setUp(self):
        super(TestIosBannerModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_banner.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.ios.plugins.modules.ios_banner.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestIosBannerModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_banner_show_running_config_ios12.txt")

        self.get_config.side_effect = load_from_file

    def test_ios_banner_create(self):
        for banner_type in ("login", "motd", "exec", "incoming", "slip-ppp"):
            set_module_args(dict(banner=banner_type, text="test\nbanner\nstring"))
            commands = ["banner {0} @\ntest\nbanner\nstring\n@".format(banner_type)]
            self.execute_module(changed=True, commands=commands)

    def test_ios_banner_remove(self):
        set_module_args(dict(banner="login", state="absent"))
        commands = ["no banner login"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_banner_nochange(self):
        banner_text = load_fixture("ios_banner_show_banner.txt")
        set_module_args(dict(banner="login", text=banner_text[:-1]))
        self.execute_module()

    def test_ios_banner_idemp(self):
        banner_text = ""
        set_module_args(dict(banner="login", text=banner_text))
        self.execute_module()

    def test_ios_banner_create_delimiter(self):
        for banner_type in ("login", "motd", "exec", "incoming", "slip-ppp"):
            set_module_args(
                dict(
                    banner=banner_type,
                    text="test\nbanner\nstring",
                    multiline_delimiter="c",
                ),
            )
            commands = ["banner {0} c\ntest\nbanner\nstring\nc".format(banner_type)]
            self.execute_module(changed=True, commands=commands)

    def test_ios_banner_empty_lines_preserved(self):
        """Test preserve_empty_lines=True - leading empty lines are preserved"""
        banner_text = "\n\n              _   _   _                 _   _   _\n             | |_| |_| |          Network Test              | |_| |_| |"
        set_module_args(dict(banner="login", text=banner_text, preserve_empty_lines=True))
        expected_commands = [
            "banner login @\n\n\n              _   _   _                 _   _   _\n             | |_| |_| |          Network Test              | |_| |_| |\n@",
        ]
        self.execute_module(changed=True, commands=expected_commands)

    def test_ios_banner_empty_lines_default_behavior(self):
        """Test default behavior - leading empty lines are stripped (preserve_empty_lines=False)"""
        banner_text = "\n\n     _   _   _          _   _   _\n             | |_| |_| |          Network Test              | |_| |_| |"
        set_module_args(dict(banner="login", text=banner_text))
        expected_commands = [
            "banner login @\n     _   _   _          _   _   _\n             | |_| |_| |          Network Test              | |_| |_| |\n@",
        ]
        self.execute_module(changed=True, commands=expected_commands)

    def test_ios_banner_only_empty_lines_preserved(self):
        """Test preserve_empty_lines=True with banner containing only empty lines"""
        banner_text = "\n\n\n"
        set_module_args(dict(banner="motd", text=banner_text, preserve_empty_lines=True))
        expected_commands = [
            "banner motd @\n\n\n\n\n@",
        ]
        self.execute_module(changed=True, commands=expected_commands)


class TestIosBannerIos12Module(TestIosBannerModule):
    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_banner_show_running_config_ios12.txt")

        self.get_config.side_effect = load_from_file

    def test_ios_banner_nochange(self):
        banner_text = load_fixture("ios_banner_show_banner.txt")
        set_module_args(dict(banner="exec", text=banner_text[:-1]))
        self.execute_module()
