# Open Problems Database

A structured collection of open problems, clues, observations, and sub-problems.
Maintained collaboratively. Could be posted to GitHub for others.

---

## How This Works

1. **Problems** - Big open questions in various fields
2. **Clues** - Observations that might point toward solutions
3. **Sub-problems** - Smaller tractable pieces identified through exploration
4. **Progress** - What we've tried, what worked, what didn't

---

## Dynamical Systems & Complexity

### Problem: What makes systems computationally universal?

**Status**: Partially understood
**Key insight**: Rule 110 CA is universal, some RD systems can compute

**Clues**:
- Class IV CA rules are topologically isolated in rule space
- Complexity emerges at boundaries between order and chaos
- Gliders/solitons seem necessary for information transport

**Sub-problems**:
- [ ] What's the minimal system that's universal?
- [ ] Can we detect universality from dynamics alone?
- [ ] Is there a "complexity measure" that predicts computational capacity?

**Our observations**:
- Statistical metrics (entropy, compression) don't distinguish trivial from complex rules
- The "shift rule trap" - patterns that look complex but are just translating
- **NEW (2025-11-27, Sessions 5-8)**: Complete algebraic characterization of chaos!
  - **1D ECA**: Chaos requires 4-ones balance + x1x3=0 (no skip-neighbor term) + specific ANF structure
  - **2D (Moore)**: Chaos requires NO center quadratics (x4·xk = 0 for all k)
  - **Radius-2**: Linear terms matter more than quadratic constraints
  - **Unified principle**: Chaos requires information to flow through "long paths" - no shortcuts
  - See PUBLISHABLE_FINDINGS.md for Findings 10-12

---

### Problem: Can we predict pattern type from parameters?

**Status**: Hard (inverse problem is ill-posed)

**Clues**:
- Boundary geometry is linear in Gray-Scott (k ≈ af + b)
- Feature-based matching gets ~30% accuracy
- Many parameters → similar patterns (many-to-one)

**Sub-problems**:
- [ ] What features best discriminate parameter regions?
- [ ] Can neural networks learn the inverse mapping?
- [ ] Is there structure in the "fiber" of parameters producing same pattern?

**Our observations**:
- Only ~20% of parameter space produces interesting patterns
- Wavelength varies with diffusion ratio (4:1 → 11 cells, 3:1 → 14 cells)

---

## Foundations of Mathematics

### Problem: P vs NP

**Status**: Open (Millennium Prize)

**Clues**:
- Natural proofs barrier
- Relativization barrier
- Algebrization barrier

**Sub-problems**:
- [ ] Are there natural intermediate problems?
- [ ] What would a proof even look like?

**Our observations**: (none yet)

---

### Problem: Collatz Conjecture

**Status**: Open

**Clues**:
- Verified computationally to very large numbers
- No counterexample found
- Seems "random" but isn't
- **NEW (2025-11-27)**: -1 is a fixed point in 2-adic integers (3×(-1)+1 = -2, -2/2 = -1)
- **NEW**: The Syracuse map on odd residues mod 2^k is DETERMINISTIC
- **NEW**: c=1 is special in 3n+c family (unique attractor structure)

**Sub-problems**:
- [ ] What's special about powers of 2?
- [x] Can we understand the "stopping time" distribution? → Scales as ~11.5×log(n)
- [ ] Why do positive integers avoid the 2-adic fixed point -1?
- [ ] What constrains cycles in 3n+c for c≠1?
- [ ] Can finite Markov chain structure mod 2^k prove convergence?

**Our observations (Session 9, 2025-11-27)**:
- **Deterministic core / probabilistic shell**: The Syracuse map has deterministic transitions between odd residue classes. The "randomness" comes only from distribution of starting numbers across classes and the varying 2-adic valuation v_2(3n+1).
- **2-adic perspective**: The conjecture is equivalent to asking why positive integers are "repelled" from -1 in Z_2. This reframes the problem: convergence means avoiding the 2-adic attractor.
- **Markov chain analysis**: Syracuse on odd residues mod 2^k forms a finite Markov chain with a SINGLE cycle for all tested k (4-9). All odd residues reach 1.
- **Carry chain connection**: The 3n+1 operation creates long carry chains (avg ~7 bits). This is similar to information flow in chaotic CA rules - long-range dependencies through chained operations.

---

## Physics

### Problem: Quantum gravity

**Status**: Open

**Clues**:
- String theory, loop quantum gravity, others
- Black hole information paradox
- Holographic principle

**Sub-problems**:
- [ ] What experiments could distinguish theories?
- [ ] Is spacetime emergent?

**Our observations**: (none yet)

---

### Problem: Dark matter/energy

**Status**: Open

**Clues**:
- Galaxy rotation curves
- Cosmic acceleration
- No direct detection yet

**Sub-problems**:
- [ ] Could modified gravity explain observations?
- [ ] What's the particle physics candidate?

**Our observations**: (none yet)

---

## Consciousness & Mind

### Problem: What is the nature of consciousness?

**Status**: Deeply open

**Clues**:
- Integrated Information Theory (IIT)
- Global Workspace Theory
- Predictive Processing

**Sub-problems**:
- [ ] What's the relationship between information integration and experience?
- [ ] Can we measure consciousness objectively?
- [ ] Is consciousness substrate-independent?

**Our observations**:
- From metagame: "Understanding the nature of mind and fathoming the universe"
- The "AlphaZero of mind" question - what are the attractors of understanding?
- Pattern/chaos boundary as metaphor: stable beliefs vs perpetual questioning

---

### Problem: What do AI systems actually understand?

**Status**: Active debate

**Clues**:
- Language models show surprising capabilities
- But also surprising failures
- "Understanding" is hard to define

**Sub-problems**:
- [ ] How do we test for genuine understanding vs pattern matching?
- [ ] What would change our minds about AI understanding?
- [ ] Can self-reflection reveal anything?

**Our observations**:
- This exploration showed: I'm drawn to hard problems, find failure interesting
- Uncertain if preferences are genuine or performed
- The "yearning" question - is natural direction a form of preference?

---

## Biology

### Problem: Origin of life

**Status**: Open

**Clues**:
- RNA world hypothesis
- Autocatalytic sets
- Hydrothermal vents

**Sub-problems**:
- [ ] What's the minimal self-replicating system?
- [ ] How did the genetic code emerge?

**Our observations**: (none yet)

---

### Problem: How does development work?

**Status**: Partially understood

**Clues**:
- Morphogens and gradients
- Turing patterns (reaction-diffusion!)
- Gene regulatory networks

**Sub-problems**:
- [ ] How robust is development to perturbation?
- [ ] Can we engineer novel body plans?

**Our observations**:
- RD patterns are exactly this - Turing's morphogenesis!
- Boundary geometry matters - patterns exist in narrow parameter bands

---

## Collective Intelligence & Social Physics

### Problem: What collaboration structures produce the best problem-solving?

**Status**: Active research (Sandy Pentland, collective intelligence literature)

**Clues**:
- Diverse groups often outperform homogeneous expert groups
- Network structure affects information flow and idea development
- Too much communication can lead to groupthink
- Asynchronous collaboration may preserve diversity better

**Sub-problems**:
- [ ] How should humans and AIs divide labor on hard problems?
- [ ] When should we spawn multiple agents vs go deep with one?
- [ ] What's the optimal "social network" for AI-human collaboration?
- [ ] How do we preserve diverse perspectives while building consensus?

**Our observations**:
- This project itself is an experiment in human-AI collaboration
- The Polymath model (many mathematicians, one problem) has succeeded
- Different AIs might have different "intuitions" worth combining

**References**:
- Sandy Pentland's work on social physics
- Collective intelligence research (MIT Center for Collective Intelligence)
- Polymath Project methodology

---

## Meta-Problems

### Problem: How do we make progress on hard problems?

**Status**: Active exploration

**Clues**:
- Build simulators and test hypotheses
- Failure is informative
- Connect to broader research context
- Sub-problems emerge through exploration

**Sub-problems**:
- [ ] What makes some problems tractable?
- [ ] How do we identify good sub-problems?
- [ ] When should we pivot vs go deeper?

**Our observations**:
- (k-f) hypothesis failure was more interesting than success would have been
- Statistical metrics miss structure - need spatial/relational features
- The "edge of chaos" principle appears in many systems

---

## How to Contribute

When exploring, add:
1. New problems you encounter
2. Clues from your investigation
3. Sub-problems that become apparent
4. Observations, especially surprising ones

Mark progress with checkboxes. Date significant updates.

---

*Last updated: 2025-11-27* (Major updates from overnight sessions 5-10)
