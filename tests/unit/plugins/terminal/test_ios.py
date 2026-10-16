#
# (c) 2026 Red Hat Inc.
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

import pytest

from ansible_collections.cisco.ios.plugins.terminal.ios import TerminalModule


@pytest.fixture()
def terminal_stderr_patterns():
    return TerminalModule.terminal_stderr_re


def _matches_any(patterns, text):
    """Return True if any pattern in the list matches the given byte string."""
    for pattern in patterns:
        if pattern.search(text):
            return True
    return False


class TestTerminalStderrRegex:
    """Tests for terminal_stderr_re patterns, focusing on routing-not-enabled errors."""

    @pytest.mark.parametrize(
        "error_output",
        [
            b"% IPv6 routing not enabled",
            b"%IPv6 routing not enabled",
            b"% ipv6 routing not enabled",
        ],
        ids=[
            "ipv6-with-space",
            "ipv6-no-space",
            "ipv6-lowercase",
        ],
    )
    def test_routing_not_enabled_detected(self, terminal_stderr_patterns, error_output):
        assert _matches_any(terminal_stderr_patterns, error_output)

    @pytest.mark.parametrize(
        "error_output",
        [
            b"% Error",
            b"% Bad secret",
            b"invalid input detected at '^' marker",
            b"% BGP: Error initializing topology",
            b"%SNMP agent not enabled",
            b"Command authorization failed",
            b"% Invalid input",
        ],
        ids=[
            "percent-error",
            "bad-secret",
            "invalid-input",
            "bgp-error",
            "snmp-not-enabled",
            "command-auth-failed",
            "invalid",
        ],
    )
    def test_existing_errors_still_detected(self, terminal_stderr_patterns, error_output):
        assert _matches_any(terminal_stderr_patterns, error_output)

    @pytest.mark.parametrize(
        "safe_output",
        [
            b"router bgp 65001",
            b"address-family ipv6",
            b"IPv6 routing is enabled",
            b"ipv6 unicast-routing",
        ],
        ids=[
            "bgp-config-command",
            "address-family-command",
            "ipv6-routing-enabled",
            "ipv6-unicast-routing-command",
        ],
    )
    def test_safe_output_not_flagged(self, terminal_stderr_patterns, safe_output):
        assert not _matches_any(terminal_stderr_patterns, safe_output)
