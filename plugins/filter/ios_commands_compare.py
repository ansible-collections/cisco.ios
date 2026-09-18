# Copyright (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Block-aware comparison of IOS module command lists for integration tests."""

from __future__ import annotations

import re

from collections import Counter
from typing import Any


BLOCK_PARENT_PATTERNS: dict[str, list[str]] = {
    "interface": [r"^interface "],
    "router": [
        r"^router ",
        r"^vrf definition ",
        r"^vrf member ",
        r"^address-family ",
        r"^exit-address-family$",
        r"^template ",
        r"^neighbor ",
    ],
    "acl": [
        r"^ip access-list ",
        r"^ipv6 access-list ",
        r"^ip prefix-list ",
        r"^ipv6 prefix-list ",
        r"^route-map ",
        r"^no ip access-list ",
        r"^no ipv6 access-list ",
        r"^no route-map ",
        r"^no ip prefix-list ",
        r"^no ipv6 prefix-list ",
    ],
    "vlan": [r"^vlan ", r"^vlan configuration "],
    "evpn": [r"^l2vpn ", r"^evpn "],
    "logging": [r"^logging ", r"^no logging "],
    "route": [
        r"^(no )?ip route ",
        r"^(no )?ipv6 route ",
        r"^vrf ",
    ],
    "flat": [],
}

_COMPILED: dict[str, list[re.Pattern[str]]] = {
    family: [re.compile(p) for p in patterns] for family, patterns in BLOCK_PARENT_PATTERNS.items()
}


def _is_parent(line: str, compiled: list[re.Pattern[str]]) -> bool:
    return any(pat.match(line) for pat in compiled)


def _partition_commands(
    commands: list[str] | None,
    family: str,
) -> Counter[tuple[str, tuple[str, ...]]]:
    if commands is None:
        commands = []
    if not isinstance(commands, list):
        commands = list(commands)

    if family == "flat" or not BLOCK_PARENT_PATTERNS.get(family):
        normalized = tuple(sorted(str(c) for c in commands))
        return Counter({("__flat__", normalized): 1})

    compiled = _COMPILED[family]
    blocks: list[tuple[str, tuple[str, ...]]] = []
    current_parent: str | None = None
    current_children: list[str] = []

    for raw in commands:
        line = str(raw)
        if _is_parent(line, compiled):
            if current_parent is not None:
                blocks.append(
                    (current_parent, tuple(sorted(current_children))),
                )
            current_parent = line
            current_children = []
        elif current_parent is None:
            blocks.append(("__orphan__", (line,)))
        else:
            current_children.append(line)

    if current_parent is not None:
        blocks.append((current_parent, tuple(sorted(current_children))))

    return Counter(blocks)


def commands_blocks_equal(
    expected: list[str] | None,
    actual: list[str] | None,
    family: str = "flat",
) -> bool:
    if family not in BLOCK_PARENT_PATTERNS:
        family = "flat"
    return _partition_commands(expected, family) == _partition_commands(
        actual,
        family,
    )


class FilterModule:
    def filters(self) -> dict[str, Any]:
        return {"commands_blocks_equal": commands_blocks_equal}
