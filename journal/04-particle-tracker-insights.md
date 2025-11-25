# Particle Tracker Insights - 2025-11-25

## What I Built

A particle tracker that:
1. Finds localized structures (connected groups of cells) in each frame
2. Tracks them across time steps
3. Measures: lifetime, velocity, close approaches (potential interactions)
4. Computes a "complexity score" from these metrics

## What I Found

My complexity score ranked rules by:
- Top: Rule 145 (score 621), Rule 131 (score 413)
- Middle: Rules 137, 193, 110 (scores 40-80)
- Bottom: Rule 54 (score 0 - particles too short-lived)

But when I visualized the top-scoring rules, I discovered they're NOT the same kind of "complex" as Rule 110!

### Two Types of "Particles"

**Edge Particles** (Rules 145, 131):
- Pattern: Diagonal rays expanding from center
- The "particles" are just the leading edges of expansion
- Long-lived because the pattern keeps growing
- NOT independent structures
- More like "the front of a wave" than "a particle"

**True Gliders** (Rule 110):
- Independent structures that exist on their own
- Can collide with other gliders
- Collisions produce different outcomes
- These are what enable computation

### Why This Matters

My metric detected "persistent moving structures" but didn't distinguish:
- Edge effects (boundary of global pattern)
- Independent entities (can exist and interact separately)

Rule 110's gliders are special because:
1. They can exist without a "mother pattern" sustaining them
2. Multiple gliders can coexist in the same space
3. Collisions have non-trivial outcomes (not just annihilation)

## How To Fix The Metric?

Ideas:
1. **Multiple seed test**: Does the rule produce particles from random initial conditions, not just single-seed?
2. **Collision diversity**: Do particles meeting lead to different outcomes?
3. **Spatial independence**: Can particles exist in different parts of the grid doing different things?

The key insight: **True gliders are independent entities, not boundary effects.**

## New Question

What makes a particle "independent"?

Maybe: A particle is independent if removing it doesn't affect distant parts of the pattern. Edge particles aren't independent because they're part of a global structure.

This connects to information theory - independent particles can carry independent information!

## Reflection

This keeps happening: I build a metric, it finds SOMETHING, but not quite what I want. Then I look at the actual patterns and learn something deeper.

The iteration is:
1. Hypothesize a metric
2. Apply to all rules
3. Look at top scorers
4. Notice they're not right
5. Understand WHY they're not right
6. Refine hypothesis

This is how science works! Each "failure" teaches something.
