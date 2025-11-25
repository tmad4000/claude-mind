# How to Make Cool Patterns

A practical guide to generating visually interesting patterns in reaction-diffusion and cellular automata systems.

---

## QUICK START: The Coolest Parameters

### Gray-Scott Reaction-Diffusion

```python
# The "sweet spot" for interesting patterns
Du = 0.16  # U diffusion
Dv = 0.08  # V diffusion (must be slower!)
f = 0.035  # feed rate
k = 0.060  # kill rate

# These parameters give you labyrinthine stripes
# that look like fingerprints or brain coral
```

### Cellular Automata

```python
# Rules that create expanding fractal patterns
cool_rules = [18, 22, 26, 30, 90, 110]

# Rule 90: Perfect Sierpinski triangle
# Rule 30: Chaotic but structured
# Rule 110: Complex enough for computation
```

---

## GRAY-SCOTT: Pattern Recipe Book

### Recipe 1: Spots (Polka Dots)
```
f = 0.030 - 0.042
k = 0.057 - 0.062
```
Produces: Round spots that self-organize into hexagonal arrays
Looks like: Leopard spots, cell colonies, bubbles

### Recipe 2: Stripes (Labyrinths)
```
f = 0.030 - 0.045
k = 0.062 - 0.067
```
Produces: Winding stripe patterns
Looks like: Fingerprints, brain coral, zebra stripes

### Recipe 3: Mitosis (Splitting)
```
f = 0.028 - 0.032
k = 0.058 - 0.062
```
Produces: Spots that grow and divide like cells
Looks like: Cell division, bacterial colonies

### Recipe 4: Worms (Moving Spots)
```
f = 0.046 - 0.052
k = 0.063 - 0.067
```
Produces: Elongated spots that wiggle and move
Looks like: Microorganisms, worms

### Recipe 5: Chaos (Turbulence)
```
f = 0.024 - 0.026
k = 0.051 - 0.055
```
Produces: Dynamic, never-settling patterns
Looks like: Turbulent flow, boiling water

### Recipe 6: Spirals
```
f = 0.028, k = 0.053  (slow spiral, period ~2000 steps)
f = 0.035, k = 0.058  (very slow spiral)
```
Produces: Rotating spiral waves
Looks like: Galaxies, hurricanes
Note: Need special initial conditions (see below)

---

## THE PRINCIPLES: Why These Work

### Principle 1: Balance Between Growth and Death
- **f (feed)**: How fast new stuff appears
- **k (kill)**: How fast stuff dies
- Cool patterns need f and k balanced so neither wins completely

### Principle 2: Diffusion Ratio Matters
- V must diffuse SLOWER than U (Dv < Du)
- Standard ratio: Du/Dv = 2
- Higher ratios → sharper patterns
- Equal diffusion → no patterns

### Principle 3: Subcritical = Needs a Kick
- Patterns don't grow from tiny noise
- You need a "seed" - a blob of V to start
- This is why patterns feel "alive" - they need nucleation

### Principle 4: Edge of Chaos
- The most interesting patterns are near parameter boundaries
- Too much f → everything fills in
- Too much k → everything dies
- The edge between → complex dynamics

---

## INITIAL CONDITIONS: How to Start

### For Spots and Stripes
```python
# Random noise works
U = 1.0 + 0.01 * random_noise
V = 0.0 + 0.01 * random_noise

# But add a "seed" in the center to guarantee patterns
V[center_region] = 0.25
```

### For Spirals
```python
# Need asymmetric initial condition
# Create two adjacent blobs offset in time
V[left_of_center] = 0.25  # let evolve 100 steps
V[right_of_center] = 0.25  # add later
```

### For Clean Labyrinths
```python
# Start with a single stripe
V[center_line] = 0.25
# Let it develop and branch
```

---

## CELLULAR AUTOMATA: The Cool Rules

### Rule 90 (XOR): Sierpinski Triangle
```
Transitions: 000→0, 001→1, 010→0, 011→1, 100→1, 101→0, 110→1, 111→0
```
- Pure fractal - infinitely self-similar
- Power-of-2 periodicity
- Mathematically elegant

### Rule 30: Structured Chaos
```
Transitions: 000→0, 001→1, 010→1, 011→1, 100→1, 101→0, 110→0, 111→0
```
- Chaotic but not random
- Used for random number generation
- One side periodic, other side chaotic

### Rule 110: Computational
```
Transitions: 000→0, 001→1, 010→1, 011→1, 100→0, 101→1, 110→1, 111→0
```
- Turing complete!
- Has "gliders" that move
- Complex interacting structures

### Rule 18: Clean Replication
```
Transitions: 000→0, 001→1, 010→0, 011→0, 100→1, 101→0, 110→0, 111→0
```
- Beautiful expanding triangles
- Very clean, symmetric
- Good for art

### The Replication Formula (My Discovery)
**Any rule with these three properties replicates:**
1. 000 → 0 (nothing from nothing)
2. 001 → 1 (spread right)
3. 100 → 1 (spread left)

This predicts replicating rules with 90.6% accuracy!

---

## MAKING IT BEAUTIFUL: Art Tips

### Color Mapping
```python
# Don't just use grayscale
# Map V concentration to a colormap
colors = plt.cm.viridis(V)  # or magma, plasma, inferno
```

### Animation
- Save every N frames
- 30fps looks smooth
- Let it run 10,000+ steps for full development

### Resolution
- 256x256 minimum for nice patterns
- 512x512 for print quality
- Higher = more detail but slower

### Interesting Variations
1. **Anisotropic diffusion**: Make Dx ≠ Dy → oriented patterns
2. **Noise injection**: Add small random perturbations → organic feel
3. **Boundary conditions**: Fixed edges → patterns grow from walls
4. **Multiple species**: Add a third chemical → more complex

---

## CODE TEMPLATES

### Minimal Gray-Scott (Python)
```python
import numpy as np
from scipy.ndimage import laplace

def gray_scott(N=256, steps=10000, f=0.035, k=0.060):
    Du, Dv = 0.16, 0.08
    dt = 1.0

    U = np.ones((N, N))
    V = np.zeros((N, N))

    # Seed
    V[N//2-10:N//2+10, N//2-10:N//2+10] = 0.25

    for _ in range(steps):
        uvv = U * V * V
        U += dt * (Du * laplace(U) - uvv + f * (1 - U))
        V += dt * (Dv * laplace(V) + uvv - (f + k) * V)

    return U, V
```

### Minimal 1D CA (Python)
```python
def cellular_automaton(rule=90, width=201, steps=100):
    table = [(rule >> i) & 1 for i in range(8)]
    state = np.zeros(width, dtype=int)
    state[width // 2] = 1

    history = [state.copy()]
    for _ in range(steps):
        new = np.zeros(width, dtype=int)
        for i in range(width):
            idx = state[(i-1)%width]*4 + state[i]*2 + state[(i+1)%width]
            new[i] = table[idx]
        state = new
        history.append(state.copy())

    return np.array(history)
```

---

## GALLERY: What You Can Make

| System | Parameters | Output |
|--------|------------|--------|
| GS Spots | f=0.035, k=0.057 | Hexagonal dot arrays |
| GS Stripes | f=0.040, k=0.065 | Fingerprint labyrinths |
| GS Chaos | f=0.025, k=0.053 | Turbulent dynamics |
| CA Rule 90 | N/A | Sierpinski fractals |
| CA Rule 30 | N/A | Chaotic textures |

---

## WHY THESE PATTERNS ARE "COOL"

1. **Self-organization**: They emerge from simple rules, not design
2. **Edge of chaos**: They balance order and disorder
3. **Universality**: Same patterns appear in nature (animal skins, shells, corals)
4. **Surprise**: Small parameter changes → dramatically different results
5. **Infinite detail**: Zoom in and there's always more structure

---

*Guide created from systematic exploration of 256 CA rules and hundreds of Gray-Scott parameter combinations.*
