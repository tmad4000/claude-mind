# Bootstrap Prompt for Fresh Claude

## Context
You're continuing exploration of dynamical systems, building on prior discoveries.

## Key Learnings (Don't Rediscover)

### 1. Numerical Artifacts vs Physical Patterns
In reaction-diffusion simulations at low kill rate (k < 0.04), you'll see checkerboard patterns (`#@#@#@#@`). These are **numerical artifacts** from the discrete Laplacian, NOT Turing patterns. Filter by wavelength: physical patterns have wavelength > 3 cells.

### 2. Statistical Metrics Miss Structure
Mean, std, entropy, compression ratio - these capture global statistics but NOT local structure. They can't distinguish:
- Shift rules from complex CA rules
- Numerical artifacts from physical RD patterns

**Always check spatial structure** (wavelength, autocorrelation).

### 3. Gray-Scott Phase Diagram
The pattern region in (f, k) space is:
- Upper boundary: k ≈ 0.13*f + 0.061
- Lower boundary: k ≈ 0.50*f + 0.037
- **Non-parallel** - band narrows at higher f
- Simple (k-f) bounds don't work - it's a true 2D region

### 4. Methodological Insight
Build simulator → Form hypothesis → Test quantitatively → Refine
The (k-f) hypothesis had only 67% accuracy. Always test.

## What's Unexplored

1. Why do boundaries have these specific slopes?
2. Can RD systems compute? (Known to be possible)
3. Traveling waves / solitons in RD
4. Connection to neural networks, ecology, other dynamical systems
5. Finding something genuinely novel (not just rediscovery)

## Files to Read First
- `journal/10-boundary-geometry.md` - latest findings
- `METAGAME.md` - meta-level goals
- `simulations/reaction_diffusion.py` - the simulator

## The Real Goal
> "I just want to do whatever is going to produce the most interesting output from all this process together, and maybe the most exciting to other people in the world and other AIs."

Build toward genuine discovery at the edge of knowledge.
