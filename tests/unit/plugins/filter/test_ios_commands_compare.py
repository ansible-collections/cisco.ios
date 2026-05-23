from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from plugins.filter.ios_commands_compare import commands_blocks_equal


def test_interface_reorder():
    expected = ["interface GigabitEthernet2", " shutdown", "interface GigabitEthernet3", " no shutdown"]
    actual = ["interface GigabitEthernet3", " no shutdown", "interface GigabitEthernet2", " shutdown"]
    assert commands_blocks_equal(expected, actual, "interface")


def test_phantom_shutdown():
    expected = ["interface GigabitEthernet2", " shutdown", "interface GigabitEthernet3", " shutdown"]
    actual = ["interface GigabitEthernet2", " shutdown", "interface GigabitEthernet3"]
    assert not commands_blocks_equal(expected, actual, "interface")
