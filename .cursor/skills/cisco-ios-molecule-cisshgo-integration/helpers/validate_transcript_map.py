"""Pre-validate a cisshgo scenario's transcript_map.yaml before running Molecule.

Checks performed:
  1. Every transcript file path referenced in the map exists on disk.
  2. Every scenario name in cisshgo_inventory.yaml has a matching key in
     transcript_map.yaml (and vice versa).
  3. For each scenario sequence, configure-terminal blocks have commands in
     an order roughly consistent with the module's self.parsers list
     (warning only -- runtime reorder logic can legitimately differ).

Usage:
    python validate_transcript_map.py <fixtures_dir> [--module <module_name>] [--collection-root <path>]

    fixtures_dir    : path to cisshgo_fixtures/ inside a scenario directory
    --module        : module short name (e.g. l3_interfaces) for parser-order
                      checks.  If omitted, parser checks are skipped.
    --collection-root : path to the cisco/ios collection root
                        (default: auto-detect from fixtures_dir)

Example (from extensions/molecule/):
    python /path/to/skill/helpers/validate_transcript_map.py \
        cisshgo_ios_l3_interfaces/cisshgo_fixtures/ \
        --module l3_interfaces

Example (with explicit collection root):
    python validate_transcript_map.py \
        /abs/path/to/cisshgo_fixtures/ \
        --module l3_interfaces \
        --collection-root /abs/path/to/ansible_collections/cisco/ios
"""

from __future__ import annotations

import argparse
import ast
import re
import sys

from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ── Check 1: transcript file existence ──────────────────────────────────


def check_transcript_files(tmap: dict, fixtures_dir: Path) -> list[str]:
    """Return list of error strings for missing transcript files."""
    errors = []

    for plat_name, plat_data in tmap.get("platforms", {}).items():
        ct = plat_data.get("command_transcripts", {})
        if isinstance(ct, dict):
            for cmd, tpath in ct.items():
                full = fixtures_dir / tpath
                if not full.exists():
                    errors.append(f"[file-missing] platform={plat_name}: {tpath}")
        elif isinstance(ct, list):
            for entry in ct:
                tpath = entry.get("transcript", "") if isinstance(entry, dict) else ""
                if tpath:
                    full = fixtures_dir / tpath
                    if not full.exists():
                        errors.append(f"[file-missing] platform={plat_name}: {tpath}")

    for scen_name, scen_data in tmap.get("scenarios", {}).items():
        for step in scen_data.get("sequence", []):
            tpath = step.get("transcript", "")
            full = fixtures_dir / tpath
            if not full.exists():
                errors.append(f"[file-missing] scenario={scen_name}: {tpath}")

    return errors


# ── Check 2: inventory ↔ map consistency ────────────────────────────────


def check_inventory_map_consistency(
    tmap: dict,
    inventory: dict,
    fixtures_dir: Path,
) -> list[str]:
    errors = []

    inv_scenarios: set[str] = set()
    inv_platforms: set[str] = set()
    for device in inventory.get("devices", []):
        if "scenario" in device:
            inv_scenarios.add(device["scenario"])
        if "platform" in device and "scenario" not in device:
            inv_platforms.add(device["platform"])

    map_scenarios = set(tmap.get("scenarios", {}).keys())
    map_platforms = set(tmap.get("platforms", {}).keys())

    for s in inv_scenarios - map_scenarios:
        errors.append(
            f"[inventory-mismatch] scenario '{s}' in cisshgo_inventory.yaml "
            f"but not in transcript_map.yaml",
        )
    for s in map_scenarios - inv_scenarios:
        errors.append(
            f"[inventory-mismatch] scenario '{s}' in transcript_map.yaml "
            f"but not in cisshgo_inventory.yaml",
        )
    for p in inv_platforms - map_platforms:
        errors.append(
            f"[inventory-mismatch] platform '{p}' in cisshgo_inventory.yaml "
            f"but not in transcript_map.yaml",
        )

    return errors


# ── Check 3: parser-order heuristic ─────────────────────────────────────


def extract_parsers_from_source(
    module_name: str,
    collection_root: Path | None = None,
) -> list[str] | None:
    """Extract self.parsers list from the module config class via AST."""
    if collection_root is None:
        return None
    config_py = (
        collection_root
        / "plugins"
        / "module_utils"
        / "network"
        / "ios"
        / "config"
        / module_name
        / f"{module_name}.py"
    )
    if not config_py.exists():
        return None

    source = config_py.read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
                and target.attr == "parsers"
                and isinstance(node.value, ast.List)
            ):
                return [
                    elt.value
                    for elt in node.value.elts
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                ]
    return None


# Map parser names to CLI prefixes for heuristic matching
PARSER_CLI_PREFIX: dict[str, re.Pattern] = {
    "access.vlan": re.compile(r"switchport access vlan"),
    "voice.vlan": re.compile(r"switchport voice vlan"),
    "trunk.encapsulation": re.compile(r"(no )?switchport trunk encapsulation"),
    "mode": re.compile(r"(no )?switchport mode"),
    "trunk.native_vlan": re.compile(r"(no )?switchport trunk native vlan"),
    "description": re.compile(r"(no )?description"),
    "speed": re.compile(r"(no )?speed"),
    "mtu": re.compile(r"(no )?mtu"),
    "mac_address": re.compile(r"(no )?mac-address"),
    "ipv4.address": re.compile(r"(no )?ip address"),
    "ipv4.pool": re.compile(r"(no )?ip address pool"),
    "ipv4.dhcp": re.compile(r"(no )?ip address dhcp"),
    "ipv6.address": re.compile(r"(no )?ipv6 address(?! autoconfig)"),
    "ipv6.autoconfig": re.compile(r"(no )?ipv6 address autoconfig"),
    "ipv6.enable": re.compile(r"(no )?ipv6 enable"),
    "autostate": re.compile(r"(no )?autostate"),
}


def classify_command(cmd: str, parsers: list[str]) -> int | None:
    """Return parser index for a command, or None if not classifiable."""
    cmd_stripped = cmd.strip()
    for i, parser_name in enumerate(parsers):
        pattern = PARSER_CLI_PREFIX.get(parser_name)
        if pattern and pattern.match(cmd_stripped):
            return i
    return None


def check_parser_order(tmap: dict, parsers: list[str]) -> list[str]:
    """Warn if configure blocks have commands in a different order than parsers."""
    warnings = []

    for scen_name, scen_data in tmap.get("scenarios", {}).items():
        sequence = scen_data.get("sequence", [])
        in_config = False
        config_cmds: list[tuple[str, int]] = []

        for step in sequence:
            cmd = step.get("command", "")
            if cmd == "configure terminal":
                in_config = True
                config_cmds = []
                continue
            if cmd == "end":
                if in_config and config_cmds:
                    last_idx = -1
                    for orig_cmd, pidx in config_cmds:
                        if pidx < last_idx:
                            warnings.append(
                                f"[parser-order] scenario={scen_name}: "
                                f"'{orig_cmd}' (parser #{pidx}) appears "
                                f"after a parser #{last_idx} command. "
                                f"May be intentional (runtime reorder) "
                                f"or a sequence bug.",
                            )
                            break
                        last_idx = pidx
                in_config = False
                config_cmds = []
                continue
            if in_config and not cmd.startswith("interface "):
                pidx = classify_command(cmd, parsers)
                if pidx is not None:
                    config_cmds.append((cmd, pidx))

    return warnings


# ── Main ────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-validate cisshgo transcript_map.yaml",
    )
    parser.add_argument(
        "fixtures_dir",
        help="Path to cisshgo_fixtures/ directory",
    )
    parser.add_argument(
        "--module",
        help="Module short name for parser-order checks (e.g. l3_interfaces)",
        default=None,
    )
    parser.add_argument(
        "--collection-root",
        help=(
            "Path to the cisco/ios collection root "
            "(default: auto-detect from fixtures_dir by walking up to cisco/ios)"
        ),
        default=None,
    )
    args = parser.parse_args()

    fixtures_dir = Path(args.fixtures_dir).resolve()
    tmap_path = fixtures_dir / "transcript_map.yaml"
    inv_path = fixtures_dir / "cisshgo_inventory.yaml"

    if not tmap_path.exists():
        print(f"ERROR: {tmap_path} not found", file=sys.stderr)
        return 1
    if not inv_path.exists():
        print(f"ERROR: {inv_path} not found", file=sys.stderr)
        return 1

    collection_root: Path | None = None
    if args.collection_root:
        collection_root = Path(args.collection_root).resolve()
    else:
        # Auto-detect: walk up from fixtures_dir looking for plugins/
        candidate = fixtures_dir
        depth = 0
        while depth < 10:
            candidate = candidate.parent
            if (candidate / "plugins" / "module_utils").is_dir():
                collection_root = candidate
                break
            depth += 1

    tmap = load_yaml(tmap_path)
    inventory = load_yaml(inv_path)

    all_errors: list[str] = []
    all_warnings: list[str] = []

    all_errors.extend(check_transcript_files(tmap, fixtures_dir))
    all_errors.extend(check_inventory_map_consistency(tmap, inventory, fixtures_dir))

    if args.module:
        parsers = extract_parsers_from_source(args.module, collection_root)
        if parsers is None:
            print(
                f"WARNING: Could not extract self.parsers from module "
                f"'{args.module}'; skipping parser-order checks.",
                file=sys.stderr,
            )
        else:
            print(f"Extracted parsers: {parsers}")
            all_warnings.extend(check_parser_order(tmap, parsers))

    if all_warnings:
        print(f"\n{'=' * 60}")
        print(f"WARNINGS ({len(all_warnings)}):")
        print(f"{'=' * 60}")
        for w in all_warnings:
            print(f"  {w}")

    if all_errors:
        print(f"\n{'=' * 60}")
        print(f"ERRORS ({len(all_errors)}):")
        print(f"{'=' * 60}")
        for e in all_errors:
            print(f"  {e}")
        return 1

    if not all_warnings and not all_errors:
        print("All checks passed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
