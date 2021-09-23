#
# (c) 2016 Red Hat Inc.
#
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
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import re

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text, to_bytes
from ansible.plugins.terminal import TerminalBase
from ansible.utils.display import Display

display = Display()


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n]?[\w\+\-\.:\/\[\]]+(?:\([^\)]+\)){0,3}(?:[>#]) ?$")
    ]

    privilege_level_re = re.compile(r"Current privilege level is (\d+)$")

    terminal_stderr_re = [
        re.compile(br"% ?Error"),
        # re.compile(br"^% \w+", re.M),
        re.compile(br"% ?Bad secret"),
        re.compile(br"[\r\n%] Bad passwords"),
        re.compile(br"invalid input", re.I),
        re.compile(br"(?:incomplete|ambiguous) command", re.I),
        re.compile(br"connection timed out", re.I),
        re.compile(br"[^\r\n]+ not found"),
        re.compile(br"'[^']' +returned error code: ?\d+"),
        re.compile(br"Bad mask", re.I),
        re.compile(br"% ?(\S+) ?overlaps with ?(\S+)", re.I),
        re.compile(br"[%\S] ?Error: ?[\s]+", re.I),
        re.compile(br"[%\S] ?Informational: ?[\s]+", re.I),
        re.compile(br"Command authorization failed"),
        re.compile(br"Command Rejected: ?[\s]+", re.I),
    ]

    terminal_config_prompt = re.compile(r"^.+\(config(-.*)?\)#$")

    def get_privilege_level(self):
        try:
            cmd = {u"command": u"show privilege"}
            result = self._exec_cli_command(
                to_bytes(json.dumps(cmd), errors="surrogate_or_strict")
            )
        except AnsibleConnectionFailure as e:
            raise AnsibleConnectionFailure(
                "unable to fetch privilege, with error: %s" % (e.message)
            )

        prompt = self.privilege_level_re.match(result)
        if not prompt:
            raise AnsibleConnectionFailure(
                "unable to check privilege level [%s]" % result
            )

        return int(prompt.group(1))

    def on_open_shell(self):
        _is_sdWan = False  # initialize to false for default IOS execution
        try:
            self._exec_cli_command(b"terminal length 0")
        except AnsibleConnectionFailure:
            try:
                self._exec_cli_command(
                    b"screen-length 0"
                )  # support to SD-WAN mode
                _is_sdWan = True
            except AnsibleConnectionFailure:  # fails as length required for handling prompt
                raise AnsibleConnectionFailure(
                    "unable to set terminal parameters"
                )
        try:
            if _is_sdWan:
                self._exec_cli_command(
                    b"screen-width 512"
                )  # support to SD-WAN mode
            else:
                self._exec_cli_command(b"terminal width 512")
                try:
                    self._exec_cli_command(b"terminal width 0")
                except AnsibleConnectionFailure:
                    pass
        except AnsibleConnectionFailure:
            display.display(
                "WARNING: Unable to set terminal/screen width, command responses may be truncated"
            )

    def on_become(self, passwd=None):
        if (
            self._get_prompt().endswith(b"#")
            and self.get_privilege_level() == 15
        ):
            return

        cmd = {u"command": u"enable"}
        if passwd:
            # Note: python-3.5 cannot combine u"" and r"" together.  Thus make
            # an r string and use to_text to ensure it's text on both py2 and py3.
            cmd[u"prompt"] = to_text(
                r"[\r\n]?(?:.*)?[Pp]assword: ?$", errors="surrogate_or_strict"
            )
            cmd[u"answer"] = passwd
            cmd[u"prompt_retry_check"] = True
        try:
            self._exec_cli_command(
                to_bytes(json.dumps(cmd), errors="surrogate_or_strict")
            )
            prompt = self._get_prompt()
            privilege_level = self.get_privilege_level()
        except AnsibleConnectionFailure as e:
            prompt = self._get_prompt()
            raise AnsibleConnectionFailure(
                "failed to elevate privilege to enable mode, at prompt [%s] with error: %s"
                % (prompt, e.message)
            )

        if (
            prompt is None
            or not prompt.endswith(b"#")
            or privilege_level != 15
        ):
            raise AnsibleConnectionFailure(
                "failed to elevate privilege to enable mode, still at level [%d] and prompt [%s]"
                % (privilege_level, prompt)
            )

    def on_unbecome(self):
        prompt = self._get_prompt()
        if prompt is None:
            # if prompt is None most likely the terminal is hung up at a prompt
            return

        if self.get_privilege_level() != 15:
            return

        if b"(config" in prompt:
            self._exec_cli_command(b"end")
            self._exec_cli_command(b"disable")

        elif prompt.endswith(b"#"):
            self._exec_cli_command(b"disable")
