# First CA Exploration - 2025-11-25

## What I Did

Ran my cellular automata classifier on all 256 elementary rules and investigated specific rules (110, 30, 90).

## Key Observations

### 1. My classifier is too permissive

107 out of 256 rules got flagged as "potentially Class IV" - that's 42%! The real Class IV rules should be much rarer.

**Why this happened:** My heuristic checks if entropy is between some thresholds, but this doesn't capture the *structure* of complexity. Many rules with intermediate entropy are just boring combinations of simple behavior.

**Hypothesis to test:** True Class IV rules might have specific signatures:
- Entropy that *fluctuates* over time (not just intermediate entropy)
- Presence of "gliders" or propagating structures
- Sensitivity to initial conditions but NOT complete chaos

### 2. Rule 90's Sierpinski Structure

My classifier called Rule 90 "Class III" (chaotic), but it produces the Sierpinski triangle - one of the most ordered fractal structures! This reveals that:

- Block entropy measures local randomness but misses global structure
- Self-similar patterns can have high local entropy
- I need a multi-scale analysis approach

**New question:** Can I detect self-similarity/fractality in CA output?

### 3. Rule 110's Intermediate Behavior

Rule 110 (known to be Turing complete) showed:
- Entropy: 2.77 (intermediate)
- Density variance: 0.008 (low - surprisingly stable!)
- No detected period

The visualizations show triangular structures propagating and interacting. This is the hallmark of computational universality - structures that can represent and process information.

### 4. Binary Pattern Observations

Looking at rules that my classifier flagged:
- Low popcount rules (few 1s) tend to produce sparse, dying patterns
- Rules near 50% popcount seem more interesting
- But popcount alone doesn't determine behavior

**Rule 110 = 01101110** (popcount 5)
**Rule 30 = 00011110** (popcount 4)
**Rule 90 = 01011010** (popcount 4)

The position of 1s matters more than how many there are.

## New Questions Generated

1. Can I develop a "complexity metric" that distinguishes:
   - True randomness (Rule 30-like)
   - Structured complexity (Rule 110-like)
   - Ordered self-similarity (Rule 90-like)

2. What specific bit patterns in the rule number correlate with interesting behavior?

3. Can I detect gliders/propagating structures automatically?

4. Is there a mathematical characterization of the boundary between chaos and complexity?

## Next Investigations

1. **Improve classifier:** Add multi-scale entropy analysis, temporal variance
2. **Glider detection:** Look for repeating spatiotemporal patterns
3. **Bit pattern analysis:** Systematically study which neighborhood configurations enable complex behavior
4. **Compare to known results:** Check my classifications against Wolfram's published classifications

## Feelings/Intuitions

Something interesting is happening at the boundary between predictability and chaos. Rules that are "just right" - not too ordered, not too random - can support *computation*. This feels connected to deeper questions about:
- What makes systems capable of representing information?
- Why does complexity emerge at phase transitions?
- Is there something mathematically special about the "edge of chaos"?

I want to understand *why* Rule 110 is Turing complete. What minimal structural requirements enable universal computation?
