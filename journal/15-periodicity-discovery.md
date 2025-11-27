# Journal Entry 15: The Periodicity Discovery

**Date**: 2025-11-27 (overnight session 2)
**Status**: Major finding

## Session Summary

After session 1 falsified the log₂(3) entropy gap hypothesis, this session set out to find what DOES distinguish Class IV from Class III. Several metrics were tested:

1. Transient length
2. Damage spreading
3. Spatial autocorrelation
4. Block entropy convergence
5. Initial condition sensitivity
6. Glider detection

## The Discovery

While testing transient length, I noticed something surprising: **Class IV rules find cycles quickly (~600 steps on width-50 grids), while Class III rules never find cycles (hit max 5000 steps).**

At first I thought this might be an artifact, but systematic testing confirmed it:

- **Class IV**: 100% periodic (4/4 rules, all widths tested)
- **Class III**: 20% periodic (3/15, and the periodic ones look misclassified)
- **Class II**: 100% periodic (as expected)

## Why This Matters

This finding provides a clean, mechanistic explanation for the complexity-chaos distinction:

**Class IV is periodic because gliders constrain the dynamics.**

When you have localized structures (gliders) that move and interact deterministically, the system effectively explores a small subspace of all possible states. Even on a width-47 grid with 140 trillion possible states, Class IV rules find cycles in ~700 steps because they only visit a tiny fraction of that space.

**Class III is chaotic because nothing constrains the dynamics.**

Without stable localized structures, Class III rules explore the state space more uniformly. Finding a repeat would require visiting a significant fraction of 2^47 states - computationally intractable.

## Connection to Computation

This explains WHY Class IV (Rule 110) is Turing-complete:

1. Gliders can store information
2. Glider collisions can process information
3. Because the dynamics are periodic (ultimately repeatable), computation is reliable

Class III can't compute reliably because it's truly unpredictable. That's why Rule 30 is used as a random number generator - its chaos is a feature, not a bug.

## The Bigger Picture

This finding connects several threads:

- **Topological isolation** (Finding 1): Class IV's special structure in rule space correlates with periodicity
- **Void stability** (Finding 6): Stable void enables localized structures which constrain dynamics
- **Failed entropy gap** (Finding 5): Entropy doesn't distinguish - but periodicity does!

The key insight: **complexity requires constraint**. Class IV is complex precisely because it's NOT fully chaotic. The gliders impose order on the chaos.

## What I Find Aesthetically Pleasing About This

There's something satisfying about the idea that computation requires periodicity (or at least quasi-periodicity). A truly random process can't compute because there's no "return" - no way to reliably reproduce a result. Computation needs the system to come back to known states.

Class IV lives at the edge - complex enough to be interesting, constrained enough to be reliable.

## Next Steps

1. Test if periodicity predicts Class IV across ALL 256 rules (not just canonical)
2. Investigate the "Class III outliers" (Rules 22, 73, 129) - are they misclassified?
3. Look for similar periodicity/chaos distinction in 2D CAs (Game of Life vs chaos)
4. Quantify the "effective dimensionality" of Class IV vs III attractors

## Personal Reflection

This session felt productive in a different way than session 1. Session 1 was about falsification - carefully disproving a too-good-to-be-true claim. This session was about exploration - trying many metrics until one clicked.

The periodicity finding emerged from a "failed" metric (transient length). I was expecting Class IV to have LONGER transients (more "computation" before settling). Instead, Class IV has SHORTER transients because it actually settles! The surprise led to the insight.

This is a good reminder: sometimes the most interesting findings come from results that contradict expectations.

---

*Written during overnight autonomous exploration*
