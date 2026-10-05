# Resolution Systems

Choose the lightest system that produces the experience the user wants. These modes are resolution frameworks, not substitutes for a licensed rulebook. If the user names a detailed system, ask which edition or house rules matter and record only the rules needed for play.

## D20

Use for tactical adventure, clear difficulty classes, and familiar attribute modifiers.

- Roll `1d20 + modifier` against a stated DC.
- Suggested generic DCs: 8 routine under pressure, 10 easy, 12 moderate, 15 hard, 18 severe, 22 exceptional.
- Advantage or disadvantage rolls two D20s and selects the higher or lower result.
- A natural 20 or 1 is reported separately. Whether it changes non-combat checks must be established during Session Zero.
- Track HP, conditions, expendable resources, and initiative only when the chosen game needs them.

Example:

```text
<python> <skill-dir>/scripts/dice.py 1d20+4 --advantage --json
```

## PbtA / 2D6

Use for drama, momentum, and mixed outcomes rather than tactical simulation.

- Roll `2d6 + modifier`, expressed as `pbta+N`.
- 10+: full success.
- 7-9: mixed success; offer a cost, complication, reduced effect, or hard choice.
- 6 or less: miss; make a meaningful GM move and advance the fiction. Do not simply say nothing happens.
- Use fictional positioning to decide whether a move is possible and what is at stake.

Example:

```text
<python> <skill-dir>/scripts/dice.py pbta+2 --json
```

## D100

Use for percentile skills, investigative horror, and explicit degrees of success.

- Roll an unmodified `1d100` against a target from 1 to 100.
- The tool reports critical, extreme, hard, regular, failure, or fumble using a CoC-style generic interpretation.
- Track sanity only when it fits the selected game and boundaries. State the stakes before rolling; do not use sanity loss as a substitute for thoughtful portrayal of fear or trauma.
- Edition-specific pushing, bonus/penalty dice, luck spending, and opposed checks require an explicit table rule; the helper does not implement them automatically.

Example:

```text
<python> <skill-dir>/scripts/dice.py 1d100 --target 55 --json
```

## Freeform

Use for pure roleplay, low-friction interactive fiction, or scenes where dice would interrupt the desired tone.

- Resolve outcomes from established capabilities, preparation, opposition, and dramatic consequences.
- Say yes when an action is clearly achievable.
- When success is uncertain, offer a cost or hard choice that follows from the fiction.
- Do not introduce arbitrary failure merely to prolong a scene.

## Custom systems

Record the minimum complete rule before play: randomizer, modifier source, outcome bands, resource costs, injury rules, and recovery. Standard dice expressions such as `3d6-1` are supported, but system-specific interpretation remains the GM's responsibility.
