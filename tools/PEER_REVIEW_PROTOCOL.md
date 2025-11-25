# Skeptical Peer Reviewer Protocol

## Purpose

After making a discovery or generating a theory, run it against a "skeptical peer reviewer" agent to validate whether it's genuinely novel or just something that baseline intuition would predict.

## The Protocol

### Step 1: Before Showing Results
Spawn a fresh Claude and ask:
1. "What would you predict about [phenomenon]?"
2. "Rate your confidence (1-10)"
3. "What theoretical framework are you using?"

### Step 2: Present the Finding
Show the actual simulation/empirical result and ask:
1. "Does this surprise you? (1-10 surprise rating)"
2. "Does this break any of your predictions?"
3. "Can you explain this from your existing framework?"

### Step 3: Evaluate Novelty

| Baseline Prediction | Actual Result | Verdict |
|---------------------|---------------|---------|
| Matches | Matches | NOT NOVEL - predictable |
| Vague/uncertain | Clear result | MILDLY NOVEL - specification |
| Confident wrong | Actual different | GENUINELY NOVEL - theory update |
| No prediction possible | Clear result | NOVEL TERRITORY - new ground |

### Step 4: Theory Update
If genuinely novel:
1. Can we derive a theory that predicts this?
2. Does that theory predict OTHER things?
3. Test those predictions too

## Metrics to Track

For each finding:
- **Intuition surprise**: How surprising to gut feeling (1-10)
- **Theory surprise**: How surprising to explicit theoretical framework (1-10)
- **Derivability**: Could it be derived from first principles? (yes/no/partially)
- **Generativity**: Does the new theory predict other testable things?

## When to Use

Use this protocol when:
- You think you've found something interesting
- You want to validate a discovery isn't just obvious
- You're about to claim something is "surprising"

## Example Application

**Discovery**: Gray-Scott boundaries are quadratic, not linear

**Baseline Claude prediction**: "I'd expect curved boundaries due to UV² nonlinearity"

**Surprise rating**: Low (3/10) - the general shape was predictable

**What WAS novel**: The specific coefficients and the 1.35 ratio between theory and empirical (represents finite-amplitude threshold)

**Verdict**: The quadratic form is NOT novel (predictable from theory). The quantitative 1.35 factor IS novel (requires understanding pattern visibility thresholds).
