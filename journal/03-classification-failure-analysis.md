# Why My Classifier Fails - 2025-11-25

## The Problem

Ran classification on all 256 rules. Got:
- 26 Class I (correct - these converge)
- 71 Class II (correct - these are periodic)
- 0 Class III or IV (WRONG)
- 159 "uncertain"

Known Class IV rules (110, 54, etc.) all ended up as "uncertain."

## What The Metrics Actually Capture

### Compression Ratio
All non-trivial rules have similar compression (0.1-0.2). zlib is too good - it finds patterns in everything. This doesn't discriminate.

### Entropy Variance
Captures rules where density changes over time. But this includes:
- Trivial shifts (Rules 14, 184) - just moving diagonally
- Banded patterns (Rule 57) - alternating high/low density bands
- Fractals (Rule 54) - Sierpinski-like self-similarity
- Complex (Rule 110) - actual interacting structures

Entropy variance is high for ALL of these, but only 110 is "complex" in the computational sense.

## The Visual Evidence

Looking at the actual patterns:

**Rule 14**: Just shifts left. Trivial.
**Rule 184**: Just shifts right. Trivial.
**Rule 57**: Creates alternating bands. Periodic-ish but weird.
**Rule 54**: Beautiful nested Sierpinski triangles. Self-similar but no interaction.
**Rule 110**: Triangular structures that PROPAGATE and COLLIDE.

## The Core Issue

My metrics are all GLOBAL STATISTICS. They measure:
- Overall density
- Overall entropy
- Overall compression

But complexity isn't about global statistics. It's about LOCAL STRUCTURE that INTERACTS.

To distinguish 110 from 54:
- Both have similar global statistics
- 54 has structure that TILES without interacting
- 110 has structure that COLLIDES and CHANGES

## What I Need

1. **Detect localized structures** (connected components? density blobs?)
2. **Track structures over time** (do they persist? move? split? merge?)
3. **Count interactions** (when structures meet, do they change?)

This is essentially a tracking problem:
- Frame 1: Find all "particles" (local structures)
- Frame 2: Match particles to previous frame
- Measure: births, deaths, collisions, splits

## Hypothesis

**True Class IV behavior** = systems where:
- Particles (localized structures) exist
- Particles persist long enough to interact
- Interactions produce NEW structures (not just annihilation)

This is what enables computation - particles encode information, interactions process it.

## New Investigation Idea

Build a "particle tracker" for CA:
1. Identify local density peaks as potential particles
2. Track them across generations
3. Detect when two particles get close (potential collision)
4. Measure what happens after collision

If particles just pass through each other: boring
If particles always annihilate: chaotic
If particles sometimes create new patterns: COMPLEX

## Reflection

I keep learning that simple statistical measures miss the point. Complexity isn't about numbers - it's about STRUCTURE and DYNAMICS. I need to actually look at the patterns, not just measure them.

The visualization showed me in seconds what hours of metric-calculating couldn't: Rule 110 has interacting particles, Rule 54 doesn't.

Maybe the lesson is: don't just measure, WATCH.
