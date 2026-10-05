#!/usr/bin/env python3
"""Strict, agent-friendly dice roller for narrative RPG systems."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from typing import Any


DICE_RE = re.compile(r"(?P<count>\d{1,3})d(?P<sides>\d{1,6})(?P<modifier>[+-]\d{1,6})?", re.IGNORECASE)
PBTA_RE = re.compile(r"pbta(?P<modifier>[+-]\d{1,3})?", re.IGNORECASE)
MAX_DICE = 100
MAX_SIDES = 1_000_000


class DiceError(ValueError):
    """A user-facing dice expression error."""


def parse_expression(expression: str) -> tuple[int, int, int, str]:
    normalized = re.sub(r"\s+", "", expression)
    pbta_match = PBTA_RE.fullmatch(normalized)
    if pbta_match:
        return 2, 6, int(pbta_match.group("modifier") or 0), "pbta"
    match = DICE_RE.fullmatch(normalized)
    if not match:
        raise DiceError("Invalid format; use XdY+Z (for example 1d20+5) or pbta+Z.")
    count = int(match.group("count"))
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or 0)
    if not 1 <= count <= MAX_DICE:
        raise DiceError(f"Dice count must be between 1 and {MAX_DICE}.")
    if not 2 <= sides <= MAX_SIDES:
        raise DiceError(f"Die size must be between 2 and {MAX_SIDES} sides.")
    return count, sides, modifier, "standard"


def coc_outcome(total: int, target: int) -> str:
    if not 1 <= target <= 100:
        raise DiceError("D100 target must be between 1 and 100.")
    if total == 1:
        return "critical_success"
    if total == 100 or (total >= 96 and target < 50):
        return "fumble"
    if total <= max(1, target // 5):
        return "extreme_success"
    if total <= max(1, target // 2):
        return "hard_success"
    if total <= target:
        return "regular_success"
    return "failure"


def roll(
    expression: str,
    *,
    advantage: bool = False,
    disadvantage: bool = False,
    target: int | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    if advantage and disadvantage:
        raise DiceError("Advantage and disadvantage cannot be used together.")
    count, sides, modifier, mode = parse_expression(expression)
    if (advantage or disadvantage) and not (mode == "standard" and count == 1 and sides == 20):
        raise DiceError("Advantage/disadvantage is supported only for a single d20 roll.")
    if target is not None and not (mode == "standard" and count == 1 and sides == 100 and modifier == 0):
        raise DiceError("--target is supported only with an unmodified 1d100 roll.")

    rng: random.Random = random.Random(seed) if seed is not None else random.SystemRandom()

    def one_roll() -> dict[str, Any]:
        dice = [rng.randint(1, sides) for _ in range(count)]
        return {"dice": dice, "modifier": modifier, "total": sum(dice) + modifier}

    candidates = [one_roll()]
    selected = 0
    roll_mode = "normal"
    if advantage or disadvantage:
        candidates.append(one_roll())
        selected = max(range(2), key=lambda index: candidates[index]["total"]) if advantage else min(
            range(2), key=lambda index: candidates[index]["total"]
        )
        roll_mode = "advantage" if advantage else "disadvantage"

    chosen = candidates[selected]
    result: dict[str, Any] = {
        "ok": True,
        "expression": expression,
        "mode": mode,
        "roll_mode": roll_mode,
        "candidates": candidates,
        "selected": selected,
        "dice": chosen["dice"],
        "modifier": modifier,
        "total": chosen["total"],
    }
    if mode == "pbta":
        total = chosen["total"]
        result["outcome"] = "full_success" if total >= 10 else "mixed_success" if total >= 7 else "miss"
    elif count == 1 and sides == 20:
        face = chosen["dice"][0]
        result["natural"] = face
        result["critical"] = "success" if face == 20 else "failure" if face == 1 else None
    if target is not None:
        result["target"] = target
        result["outcome"] = coc_outcome(chosen["total"], target)
    if seed is not None:
        result["seeded"] = True
    return result


def render_text(result: dict[str, Any]) -> str:
    lines = [f"Expression: {result['expression']}", f"Mode: {result['roll_mode']}"]
    for index, candidate in enumerate(result["candidates"]):
        marker = " <- selected" if index == result["selected"] else ""
        lines.append(f"Roll {index + 1}: {candidate['dice']} {candidate['modifier']:+} = {candidate['total']}{marker}")
    if result.get("critical"):
        lines.append(f"Critical: {result['critical']}")
    if result.get("outcome"):
        lines.append(f"Outcome: {result['outcome']}")
    if "target" in result:
        lines.append(f"Target: {result['target']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Roll standard, D20, PbtA, or D100 checks")
    parser.add_argument("expression", help="Dice expression, e.g. 1d20+5, 2d6-1, 1d100, or pbta+2")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-a", "--advantage", action="store_true", help="Roll two d20s and keep the higher total")
    mode.add_argument("-d", "--disadvantage", action="store_true", help="Roll two d20s and keep the lower total")
    parser.add_argument("--target", type=int, help="Evaluate an unmodified 1d100 roll against a CoC-style skill target")
    parser.add_argument("--seed", type=int, help="Deterministic seed for testing/replays; omit during normal play")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON for an agent to consume")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = roll(
            args.expression,
            advantage=args.advantage,
            disadvantage=args.disadvantage,
            target=args.target,
            seed=args.seed,
        )
    except DiceError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
