#!/usr/bin/env bash
# run_scenario.sh — Molecule wrapper that enforces best practices
#
# Usage:  run_scenario.sh <scenario_name> [molecule-test-args...]
#
# What it does:
#   1. Verifies CISSHGO_BIN_PATH is set and the binary exists.
#   2. Sets ANSIBLE_COLLECTIONS_PATH relative to the extensions/ directory.
#   3. Sets PYTHONHASHSEED=0 if not already set (stable dict_merge order).
#   4. Runs molecule destroy first (prevents stale cisshgo process).
#   5. Runs molecule test -s <scenario>.
#   6. On failure: tails .cisshgo.log for quick diagnosis.
#
# Run from: ansible_collections/cisco/ios/extensions/
# Or set EXTENSIONS_DIR to point there explicitly.

set -euo pipefail

# Resolve extensions directory: env override or auto-detect from cwd
if [[ -n "${EXTENSIONS_DIR:-}" ]]; then
    EXTENSIONS_DIR="$(cd "$EXTENSIONS_DIR" && pwd)"
elif [[ -d "molecule" && -f "molecule/README.md" ]]; then
    EXTENSIONS_DIR="$(pwd)"
elif [[ "$(basename "$(pwd)")" == "molecule" && -f "README.md" ]]; then
    EXTENSIONS_DIR="$(cd .. && pwd)"
else
    echo "ERROR: Cannot detect extensions/ directory."
    echo "  Either cd to ansible_collections/cisco/ios/extensions/"
    echo "  or set EXTENSIONS_DIR=/path/to/extensions"
    exit 1
fi

MOLECULE_DIR="${EXTENSIONS_DIR}/molecule"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <scenario_name> [extra molecule args...]"
    echo "Run from ansible_collections/cisco/ios/extensions/"
    exit 1
fi

SCENARIO="$1"
shift
EXTRA_ARGS=("$@")

SCENARIO_DIR="${MOLECULE_DIR}/${SCENARIO}"

# ── Pre-flight checks ───────────────────────────────────────────────────

if [[ -z "${CISSHGO_BIN_PATH:-}" && -z "${CISSHGO_REPO_PATH:-}" ]]; then
    echo "ERROR: Neither CISSHGO_BIN_PATH nor CISSHGO_REPO_PATH is set."
    echo "  export CISSHGO_BIN_PATH=/path/to/cisshgo"
    exit 1
fi

if [[ -n "${CISSHGO_BIN_PATH:-}" && ! -x "${CISSHGO_BIN_PATH}" ]]; then
    echo "ERROR: CISSHGO_BIN_PATH=${CISSHGO_BIN_PATH} is not executable."
    exit 1
fi

if [[ ! -d "${SCENARIO_DIR}" ]]; then
    echo "ERROR: Scenario directory not found: ${SCENARIO_DIR}"
    exit 1
fi

# ── Environment ──────────────────────────────────────────────────────────

export ANSIBLE_COLLECTIONS_PATH="${EXTENSIONS_DIR}/../../..:${ANSIBLE_COLLECTIONS_PATH:-}"
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"

echo "=== run_scenario.sh ==="
echo "Scenario:                ${SCENARIO}"
echo "Extensions dir:          ${EXTENSIONS_DIR}"
echo "CISSHGO_BIN_PATH:        ${CISSHGO_BIN_PATH:-<repo build>}"
echo "ANSIBLE_COLLECTIONS_PATH: ${ANSIBLE_COLLECTIONS_PATH}"
echo "PYTHONHASHSEED:          ${PYTHONHASHSEED}"
echo "========================"

cd "${EXTENSIONS_DIR}"

# ── Destroy stale cisshgo (prevents port/map staleness) ──────────────────

echo ""
echo ">>> molecule destroy -s ${SCENARIO} (clean slate)"
molecule destroy -s "${SCENARIO}" 2>&1 || true

# ── Run molecule test ────────────────────────────────────────────────────

echo ""
echo ">>> molecule test -s ${SCENARIO} ${EXTRA_ARGS[*]:-}"
if molecule test -s "${SCENARIO}" "${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}"; then
    echo ""
    echo "=== PASSED: molecule test -s ${SCENARIO} ==="
    exit 0
fi

EXIT_CODE=$?

# ── Failure diagnosis ────────────────────────────────────────────────────

echo ""
echo "=== FAILED: molecule test -s ${SCENARIO} (exit ${EXIT_CODE}) ==="
echo ""

LOG_FILE="${SCENARIO_DIR}/.cisshgo.log"
if [[ -f "${LOG_FILE}" ]]; then
    echo "--- .cisshgo.log: first 'Unknown command' ---"
    grep -m5 "Unknown command" "${LOG_FILE}" 2>/dev/null || echo "(none found)"
    echo ""
    echo "--- .cisshgo.log: last 20 lines ---"
    tail -20 "${LOG_FILE}"
else
    echo "(no .cisshgo.log found at ${LOG_FILE})"
fi

exit "${EXIT_CODE}"
