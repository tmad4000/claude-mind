# Connections Database (Zettelkasten Style)

A network of linked observations, theories, and insights. Each entry links to others, enabling multi-step discovery.

---

## HOW TO USE

- Each node has a unique ID (e.g., `[[C-001]]`)
- Links are bidirectional: if A links to B, B should link back
- **Hop chains** show multi-step connections: A -> B -> C
- **Clusters** are groups of densely connected nodes

---

## CONNECTIONS

### [[C-001]] Bidirectional Spreading Principle
**Type**: Mechanism
**Statement**: Replication/propagation requires forces acting in opposite directions
**Links**:
- `[[OBS-CA-003]]` - CA bidirectional spreading (001->1 AND 100->1)
- `[[OBS-RD-007]]` - RD front propagation (slower than theory)
- `[[C-002]]` - Balance principle
- `[[C-005]]` - Wave mechanics

**Evidence**: CA rules need both 001->1 and 100->1 for clean expansion. Single-direction spreading creates drift, not replication.

---

### [[C-002]] Balance Principle
**Type**: Meta-principle
**Statement**: Interesting behavior emerges from balance between opposing forces
**Links**:
- `[[C-001]]` - Bidirectional spreading (expansion vs constraint)
- `[[C-003]]` - Edge of chaos (order vs chaos)
- `[[OBS-CA-003]]` - No spontaneous birth balances spreading
- `[[OBS-RD-003]]` - Subcritical bifurcation (stability vs instability)

**Evidence**: CA replication needs spreading + death. RD patterns need reaction + diffusion. Edge of chaos is boundary between order and chaos.

---

### [[C-003]] Edge of Chaos
**Type**: Meta-principle
**Statement**: Complex/interesting behavior occurs at phase boundaries
**Links**:
- `[[OBS-CA-001]]` - Class IV rules are topologically isolated (at boundary)
- `[[OBS-RD-005]]` - GS patterns are weakly chaotic (λ > 0 but small)
- `[[C-002]]` - Balance principle (edge = balance point)
- `[[OBS-X-001]]` - Cross-domain: complexity at boundaries

**Evidence**: Class IV CAs are rare and isolated. Gray-Scott patterns have small positive Lyapunov exponents. Interesting = edge between stability and chaos.

---

### [[C-004]] Death From Crowding
**Type**: Mechanism
**Statement**: Sustained patterns require mechanisms that kill overcrowded regions
**Links**:
- `[[OBS-CA-006]]` - 111->0 prevents filling in CA
- `[[OBS-RD-001]]` - Subcritical: patterns don't grow from infinitesimal
- `[[C-002]]` - Balance principle (death balances birth)
- `[[C-009]]` - Game of Life connection

**Evidence**: CA rules with 111->1 tend to fill. Game of Life has overpopulation rule (>3 neighbors = death).

---

### [[C-005]] Wave Mechanics Analogy
**Type**: Cross-domain
**Statement**: CA replication is analogous to wave propagation
**Links**:
- `[[C-001]]` - Bidirectional spreading = wave fronts
- `[[OBS-CA-005]]` - XOR creates interference patterns (like waves)
- `[[OBS-RD-004]]` - Wavelength selection (wave-like property)

**Evidence**: XOR (Rule 90) creates Sierpinski = interference pattern. Information propagates at constant velocity in both CA and waves.

---

### [[C-006]] Self-Similarity From Local Rules
**Type**: Emergence
**Statement**: Simple local rules can produce global self-similar (fractal) structure
**Links**:
- `[[OBS-CA-005]]` - Rule 90 Sierpinski triangle
- `[[C-007]]` - Emergence principle
- `[[C-005]]` - Wave interference creates patterns

**Evidence**: 3-bit lookup table (8 entries) produces infinite fractal. Local = simple, global = complex.

---

### [[C-007]] Emergence Principle
**Type**: Meta-principle
**Statement**: Complex global behavior can emerge from simple local rules
**Links**:
- `[[C-006]]` - Self-similarity from local rules
- `[[OBS-CA-002]]` - Rule 110 universality (simple rule = universal computation)
- `[[OBS-RD-001]]` - Pattern from stability (global pattern from local reactions)

**Evidence**: Rule 110 (8 bits) is Turing-complete. Rule 90 (8 bits) creates infinite fractal. Gray-Scott (2 PDEs) creates complex patterns.

---

### [[C-008]] Computation vs Pattern Formation
**Type**: Distinction
**Statement**: Universal computation and pattern formation are different capabilities
**Links**:
- `[[OBS-CA-002]]` - Rule 110 computes
- `[[OBS-X-002]]` - Gray-Scott doesn't compute
- `[[OBS-CA-003]]` - Replication ≠ computation

**Evidence**: Rule 110 computes but doesn't cleanly replicate. Rule 90 replicates but doesn't compute. Gray-Scott patterns don't transfer information. Computation requires specific glider/collision dynamics.

---

### [[C-009]] Game of Life Connection
**Type**: Cross-reference
**Statement**: 2D Game of Life shares principles with 1D CA replication
**Links**:
- `[[C-004]]` - Death from crowding (overpopulation rule)
- `[[C-001]]` - Bidirectional spreading (gliders propagate)
- `[[C-008]]` - GoL supports computation AND has gliders

**Hypothesis**: GoL is a 2D system where replication and computation can coexist because of the extra dimension.

---

### [[C-010]] Subcritical Pattern Formation
**Type**: Mechanism
**Statement**: Patterns that form via subcritical bifurcation need finite-amplitude triggers
**Links**:
- `[[OBS-RD-001]]` - GS: no linear instability but patterns form
- `[[OBS-RD-003]]` - Always subcritical across Du/Dv
- `[[C-003]]` - Edge of chaos (subcritical = metastable edge)

**Evidence**: Gray-Scott patterns need nucleation. Random noise doesn't trigger patterns; structured perturbation does.

---

## HOP CHAINS (Multi-Step Connections)

### Chain 1: Replication → Balance → Edge of Chaos → Isolation
```
[[C-001]] Bidirectional Spreading
    ↓ "requires balance"
[[C-002]] Balance Principle
    ↓ "creates edge"
[[C-003]] Edge of Chaos
    ↓ "edge rules are"
[[OBS-CA-001]] Topologically Isolated
```
**Insight**: Replication requires balance, balance creates edge conditions, edge conditions are rare/isolated in rule space.

### Chain 2: XOR → Fractals → Emergence → Computation
```
[[OBS-CA-005]] Rule 90 XOR/Sierpinski
    ↓ "is example of"
[[C-006]] Self-Similarity From Local Rules
    ↓ "is instance of"
[[C-007]] Emergence Principle
    ↓ "also explains"
[[OBS-CA-002]] Rule 110 Universality
```
**Insight**: The same emergence principle that creates fractals also enables universal computation.

### Chain 3: Spreading → Waves → Wavelength → Kinetics
```
[[C-001]] Bidirectional Spreading
    ↓ "is analogous to"
[[C-005]] Wave Mechanics
    ↓ "determines"
[[OBS-RD-004]] Wavelength Selection
    ↓ "controlled by"
[[OBS-RD-008]] Kinetics Controls Wavelength
```
**Insight**: Spreading dynamics (CA) and diffusion dynamics (RD) both create wave-like propagation with characteristic wavelengths.

### Chain 4: Crowding Death → Balance → Subcritical → Nucleation
```
[[C-004]] Death From Crowding
    ↓ "implements"
[[C-002]] Balance Principle
    ↓ "leads to"
[[C-010]] Subcritical Patterns
    ↓ "require"
[[OBS-RD-001]] Finite Amplitude Nucleation
```
**Insight**: The same death-from-crowding that enables CA replication also explains why RD patterns need nucleation.

---

## CLUSTERS (Densely Connected Groups)

### Cluster A: Replication Mechanisms
Core: `[[C-001]]`, `[[C-004]]`, `[[OBS-CA-003]]`
Theme: What enables patterns to reproduce themselves

### Cluster B: Meta-Principles
Core: `[[C-002]]`, `[[C-003]]`, `[[C-007]]`
Theme: General principles that apply across systems

### Cluster C: Wave/Propagation
Core: `[[C-005]]`, `[[OBS-RD-004]]`, `[[OBS-RD-007]]`
Theme: How information/structure spreads through space

### Cluster D: Computation
Core: `[[OBS-CA-002]]`, `[[C-008]]`, `[[OBS-X-002]]`
Theme: What enables or prevents universal computation

---

### [[C-011]] Universal Pattern Formation
**Type**: Unifying principle
**Statement**: The same pattern-forming math appears across radically different substrates
**Links**:
- `[[NATURAL_CORRESPONDENCES]]` - Full documentation
- `[[C-007]]` - Emergence principle
- `[[C-002]]` - Balance principle
- `[[OBS-RD-004]]` - Wavelength selection

**Evidence**:
- Leopard spots = Gray-Scott spots = same parameters
- Seashells = frozen time-series of RD
- Hallucination geometry = neural Turing patterns (Bressloff 2001)
- BZ reaction = pure RD chemistry

---

### [[C-012]] Neural Geometry ↔ Psychedelic Patterns
**Type**: Cross-domain
**Statement**: Psychedelic visual phenomena arise from Turing-like instabilities in visual cortex
**Links**:
- `[[C-011]]` - Universal pattern formation
- `[[NATURAL_CORRESPONDENCES]]` - Form constants section
- `[[C-003]]` - Edge of chaos (altered states = perturbed edge?)

**Evidence**:
- Klüver's 4 form constants match RD geometry
- Bressloff et al. (2001) mathematically derived hallucination patterns from V1 architecture
- Spirals, lattices, tunnels = Turing pattern types

**Implication**: The patterns we find "cool" may literally resonate with our neural architecture.

---

### [[C-013]] Inner Geometry Resonance
**Type**: Meta-observation (Jacob)
**Statement**: "Patterns that are resonant with your inner geometry... those are the things we like"
**Links**:
- `[[C-012]]` - Neural geometry
- `[[C-011]]` - Universal pattern formation
- `[[JACOB_INSIGHTS]]` - #4, #5

**Implication**: Aesthetic preference may be pattern-matching between external forms and internal structure. What feels "cool" reveals something about what we are.

---

## OPEN QUESTIONS (Suggested by Connections)

1. **From Chain 1**: If edge conditions are isolated, how did evolution find them? (Selection pressure → edge seeking?)

2. **From Chain 2**: Is there a rule that both replicates cleanly AND computes? (GoL might be the answer)

3. **From Chain 3**: Can CA replication theory predict RD wavelength selection?

4. **From Chain 4**: Can we find a CA analogue of subcritical bifurcation?

5. **From Cluster D**: What's the minimal change to Gray-Scott to enable computation?

---

*Last updated: 2025-11-25*
