# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Python 3 stdlib target harness compiler package.
"""Reference target harness compilers for the PPA semantic knowledge suite."""
from __future__ import annotations

ADAPTER_TARGETS = (
    "claude-code",
    "gemini-cli",
    "codex-agents",
    "cursor-ide",
    "knowledge-wiki",
)

__all__ = ["ADAPTER_TARGETS"]
