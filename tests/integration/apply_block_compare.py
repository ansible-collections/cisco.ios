"""Replace command symmetric_difference asserts with commands_blocks_equal."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
TARGETS = ROOT / "targets"
CONFIG = yaml.safe_load((ROOT / "command_compare_config.yaml").read_text())

PATTERNS = [
    (
        re.compile(
            r"""\{\{\s*(\w+)\['commands'\]\s*\|\s*symmetric_difference\(result\['commands'\]\)\s*\|\s*length\s*==\s*0\s*\}\}"""
        ),
        lambda m, fam: (
            f"{{{{ {m.group(1)}['commands'] "
            f"| cisco.ios.commands_blocks_equal(result['commands'], '{fam}') }}}}"
        ),
    ),
    (
        re.compile(
            r"""result\.commands\|symmetric_difference\((\w+)\.commands\)\s*==\s*\[\]"""
        ),
        lambda m, fam: (
            f"{{{{ {m.group(1)}.commands "
            f"| cisco.ios.commands_blocks_equal(result.commands, '{fam}') }}}}"
        ),
    ),
    (
        re.compile(
            r"""(\w+)\.commands\|symmetric_difference\((\w+)\.commands\)\s*==\s*\[\]"""
        ),
        lambda m, fam: (
            f"{{{{ {m.group(1)}.commands "
            f"| cisco.ios.commands_blocks_equal({m.group(2)}.commands, '{fam}') }}}}"
        ),
    ),
]


def module_from_path(path: Path) -> str:
    for part in path.parts:
        if part.startswith("ios_"):
            return part
    raise ValueError(f"cannot infer module from {path}")


def family_for(path: Path) -> str:
    mod = module_from_path(path)
    return CONFIG.get(mod, "flat")


def process_file(path: Path) -> bool:
    text = path.read_text()
    fam = family_for(path)
    new = text
    changed = False
    for regex, repl in PATTERNS:
        def _sub(m: re.Match[str]) -> str:
            return repl(m, fam)

        updated, n = regex.subn(_sub, new)
        if n:
            changed = True
            new = updated
    if changed and new != text:
        path.write_text(new)
    return changed


def main() -> int:
    changed_files = []
    for yml in sorted(TARGETS.glob("**/tests/**/*.yaml")):
        if process_file(yml):
            changed_files.append(yml)
    print(f"Updated {len(changed_files)} files")
    for p in changed_files:
        print(f"  {p.relative_to(ROOT.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
