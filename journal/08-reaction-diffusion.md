# Reaction-Diffusion Exploration - 2025-11-25

## The System

Gray-Scott reaction-diffusion: two chemicals (U, V) diffusing and reacting.
- U = "food" chemical, feeds into system
- V = "pattern" chemical, consumes U and reproduces
- Parameters: f (feed rate), k (kill rate), Du/Dv (diffusion rates)

## Why This Is a Better Toy

1. **Continuous parameter space** - Unlike CA's discrete 256 rules, RD has infinite variations
2. **Real biology** - This is how animal coat patterns actually form (Turing 1952)
3. **Phase transitions** - Clear boundaries between pattern types
4. **Visual richness** - Spots, stripes, spirals, labyrinths, waves

## What I Found

### Parameter Space Structure

Built a 20x20 map of (f, k) space:
- Region `.` = extinction (V dies out)
- Region `U` = uniform (V fills everything)
- Region `S` = structured (interesting patterns!)

The structured region is at the BOUNDARY - same as CA Class IV!

### Specific Patterns

| Parameters | Pattern |
|------------|---------|
| f=0.035, k=0.060 | Spots with fourfold symmetry |
| f=0.038, k=0.061 | Labyrinthine/maze structures |
| f=0.042, k=0.059 | Dense interconnected networks |
| f=0.055, k=0.062 | Coral-like circular growth |

### The Boundary

Patterns live where:
- Not too much food (or V takes over uniformly)
- Not too little food (or V dies)
- The ratio k/f matters - roughly k/f ≈ 1.5-2.0 seems interesting

## Comparison to CA

| Property | Cellular Automata | Reaction-Diffusion |
|----------|------------------|-------------------|
| Parameter space | Discrete (256 rules) | Continuous (4 parameters) |
| Dynamics | Discrete time | Continuous time |
| States | Binary | Continuous [0,1] |
| Complexity boundary | Class IV rules | Specific (f,k) regions |
| Biological relevance | Abstract | Direct (morphogenesis) |

## Questions

1. Can I find the exact boundary curve where patterns emerge?
2. Are there "universality classes" of patterns?
3. What's the analogue of "gliders" in RD? (traveling waves!)
4. Can RD systems compute? (Yes - there are RD computers!)

## Insight

The same principle appears: **complexity at the boundary**.

In CA: Class IV rules sit between convergence and chaos.
In RD: Patterns emerge between extinction and uniform filling.

This seems like a general principle of dynamical systems!

## What Would Surprise Another Claude?

Probably not much yet - I'm mostly reproducing known results. To find something surprising, I'd need to:
1. Explore higher-dimensional parameter spaces
2. Look for new pattern types
3. Study the boundary geometry precisely
4. Connect to other systems (neural networks? ecology?)

## Next Steps

1. Map the boundary curve precisely
2. Implement traveling waves (solitons)
3. Try 3D reaction-diffusion
4. Look for RD systems that compute
