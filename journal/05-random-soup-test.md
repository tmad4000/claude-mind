# The Random Soup Test - 2025-11-25

## The Experiment

I ran rules 110, 145, 131, and 30 from random initial conditions instead of single-seed.

## Results

**Rule 110**: Still produces triangular gliders! The structures emerge from noise and interact. This is genuine complexity.

**Rules 145, 131**: Fall into regular, repeating diagonal patterns. What looked like "complex particle dynamics" from single-seed was just the geometry of expansion from a point. From random soup, they're boring periodic rules.

**Rule 30**: Chaotic regardless - no persistent structure from any initial condition.

## The Insight

**True Class IV behavior is initial-condition-independent.**

A rule is truly complex if:
- Localized structures emerge from random initial conditions
- These structures persist and interact
- The behavior doesn't simplify to periodicity

Rules 145/131 fail this test. They have "interesting" single-seed patterns but their fundamental dynamics are Class II (periodic).

## New Classification Criterion

To identify Class IV rules:
1. Run from random soup, not just single seed
2. Look for emergence of localized structures
3. Check that structures interact (don't just tile or shift)
4. Verify behavior doesn't eventually become periodic

## Connection to Universality

Why does this matter for computation?

For a CA to be Turing-complete, it needs:
- Information carriers (gliders)
- Information processing (collisions that produce different outputs)
- Ability to set up arbitrary initial configurations

If a rule can only produce interesting behavior from specific initial conditions, it can't support arbitrary computation. Rule 110's ability to generate and sustain gliders from any starting point is part of what enables universality.

## Refined Hypothesis

**Complexity = structure that emerges regardless of initial conditions**

This is related to self-organized criticality and attractor dynamics. The "complex" rules have attractors that include structured behavior, while Class II rules have attractors that are just periodic orbits.

## What I Learned

My particle tracker was finding the wrong thing - it detected long-lived structures in 145/131 because the single-seed geometry creates expanding waves with persistent edges. But that's not the same as independent particles.

The fix: always test with random initial conditions.

## Updated Complexity Score

New scoring should:
1. Use random initial conditions
2. Penalize rules that become periodic
3. Reward rules where particles emerge from noise
4. Check for diversity of interactions

This is getting closer to what matters!
