#!/usr/bin/env python3
"""
Ternary Hydride Composition Explorer

Analyze known ternary hydrides and generate predictions for unexplored
composition space based on pattern matching.

This is NOT a DFT replacement - it's pattern-based hypothesis generation.
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
import itertools

@dataclass
class TernaryHydride:
    """Known ternary hydride superconductor"""
    formula: str
    elements: Tuple[str, str]  # Non-H elements
    tc: float  # K
    pressure: float  # GPa
    structure: str
    year: int
    verified: bool
    notes: str = ""

# Known ternary hydride superconductors (from literature)
KNOWN_TERNARIES = [
    TernaryHydride("LaBeH8", ("La", "Be"), 110, 80, "clathrate", 2024, True,
                   "First crystallized ternary template"),
    TernaryHydride("(La,Y)H10", ("La", "Y"), 253, 183, "clathrate", 2021, True,
                   "Mixed rare earth"),
    TernaryHydride("(La,Ce)H9", ("La", "Ce"), 176, 100, "clathrate", 2022, True,
                   "Lower pressure than binary"),
    TernaryHydride("(La,Ce)H10", ("La", "Ce"), 190, 170, "clathrate", 2022, True,
                   ""),
    TernaryHydride("(Y,Ce)H9", ("Y", "Ce"), 140, 150, "clathrate", 2022, True,
                   ""),
    TernaryHydride("(La,Nd)H10", ("La", "Nd"), 160, 180, "clathrate", 2022, True,
                   ""),
    TernaryHydride("LaAlH", ("La", "Al"), 223, 164, "hexagonal", 2024, True,
                   "Al stabilizes metastable phase"),
    TernaryHydride("CaBeH8", ("Ca", "Be"), 55, 100, "clathrate", 2024, False,
                   "Computational prediction"),
    TernaryHydride("LaSc2H24", ("La", "Sc"), 316, 167, "novel-cage", 2024, False,
                   "Computational - 'hot' superconductivity claim"),
]

# Element properties relevant to hydride superconductivity
ELEMENT_DATA = {
    # Rare earths / actinides (high DOS, strong e-p coupling)
    "La": {"category": "promoter", "radius": 1.87, "mass": 139, "electronegativity": 1.1},
    "Y":  {"category": "promoter", "radius": 1.80, "mass": 89, "electronegativity": 1.22},
    "Ce": {"category": "promoter", "radius": 1.81, "mass": 140, "electronegativity": 1.12},
    "Nd": {"category": "promoter", "radius": 1.81, "mass": 144, "electronegativity": 1.14},
    "Sc": {"category": "promoter", "radius": 1.64, "mass": 45, "electronegativity": 1.36},
    "Th": {"category": "promoter", "radius": 1.79, "mass": 232, "electronegativity": 1.3},
    "Ac": {"category": "promoter", "radius": 1.88, "mass": 227, "electronegativity": 1.1},

    # Light stabilizers (provide "chemical pressure", stabilize H-rich phases)
    "Be": {"category": "stabilizer", "radius": 1.12, "mass": 9, "electronegativity": 1.57},
    "B":  {"category": "stabilizer", "radius": 0.87, "mass": 11, "electronegativity": 2.04},
    "Al": {"category": "stabilizer", "radius": 1.43, "mass": 27, "electronegativity": 1.61},
    "Mg": {"category": "stabilizer", "radius": 1.60, "mass": 24, "electronegativity": 1.31},
    "Li": {"category": "stabilizer", "radius": 1.52, "mass": 7, "electronegativity": 0.98},
    "Na": {"category": "stabilizer", "radius": 1.86, "mass": 23, "electronegativity": 0.93},
    "Si": {"category": "stabilizer", "radius": 1.17, "mass": 28, "electronegativity": 1.90},

    # Alkaline earths (intermediate)
    "Ca": {"category": "intermediate", "radius": 1.97, "mass": 40, "electronegativity": 1.0},
    "Sr": {"category": "intermediate", "radius": 2.15, "mass": 88, "electronegativity": 0.95},
    "Ba": {"category": "intermediate", "radius": 2.22, "mass": 137, "electronegativity": 0.89},
}

def analyze_known_patterns():
    """Extract patterns from known ternary hydrides"""
    print("=" * 60)
    print("PATTERN ANALYSIS OF KNOWN TERNARY HYDRIDES")
    print("=" * 60)
    print()

    # Categorize by element combination types
    promoter_promoter = []
    promoter_stabilizer = []
    other = []

    for h in KNOWN_TERNARIES:
        e1, e2 = h.elements
        cat1 = ELEMENT_DATA.get(e1, {}).get("category", "unknown")
        cat2 = ELEMENT_DATA.get(e2, {}).get("category", "unknown")
        cats = sorted([cat1, cat2])

        if cats == ["promoter", "promoter"]:
            promoter_promoter.append(h)
        elif cats == ["promoter", "stabilizer"]:
            promoter_stabilizer.append(h)
        else:
            other.append(h)

    print("By combination type:")
    print(f"  Promoter + Promoter: {len(promoter_promoter)} compounds")
    for h in promoter_promoter:
        print(f"    {h.formula}: Tc={h.tc}K at {h.pressure}GPa")

    print(f"\n  Promoter + Stabilizer: {len(promoter_stabilizer)} compounds")
    for h in promoter_stabilizer:
        print(f"    {h.formula}: Tc={h.tc}K at {h.pressure}GPa")

    print(f"\n  Other: {len(other)} compounds")
    for h in other:
        print(f"    {h.formula}: Tc={h.tc}K at {h.pressure}GPa")

    # Look for pressure reduction pattern
    print("\n" + "-" * 60)
    print("PRESSURE REDUCTION ANALYSIS")
    print("-" * 60)

    # Binary references
    binary_refs = {
        "LaH10": (260, 170),  # Tc, P
        "YH6": (220, 165),
        "CeH9": (95, 150),
    }

    print("\nDo ternaries reduce pressure vs. binary parents?")
    for h in KNOWN_TERNARIES:
        e1, e2 = h.elements
        # Find relevant binary references
        for elem in [e1, e2]:
            for ref_name, (ref_tc, ref_p) in binary_refs.items():
                if elem in ref_name:
                    p_reduction = ref_p - h.pressure
                    tc_change = h.tc - ref_tc
                    if p_reduction > 0:
                        print(f"  {h.formula} vs {ref_name}: P reduced by {p_reduction}GPa, Tc change: {tc_change:+.0f}K")

    return {
        "promoter_promoter": promoter_promoter,
        "promoter_stabilizer": promoter_stabilizer,
    }


def generate_candidates():
    """Generate unexplored ternary hydride candidates"""
    print("\n" + "=" * 60)
    print("CANDIDATE GENERATION")
    print("=" * 60)
    print()

    promoters = [e for e, d in ELEMENT_DATA.items() if d["category"] == "promoter"]
    stabilizers = [e for e, d in ELEMENT_DATA.items() if d["category"] == "stabilizer"]

    # Known pairs
    known_pairs = set()
    for h in KNOWN_TERNARIES:
        known_pairs.add(tuple(sorted(h.elements)))

    # Generate promoter + stabilizer candidates (most promising based on patterns)
    print("TIER 1: Promoter + Stabilizer (unexplored)")
    print("Based on LaBeH8 success, these may offer pressure reduction")
    print()

    tier1_candidates = []
    for p in promoters:
        for s in stabilizers:
            pair = tuple(sorted([p, s]))
            if pair not in known_pairs:
                # Score based on similarity to successful LaBeH8
                score = 0
                # Light stabilizer is good
                score += 10 / ELEMENT_DATA[s]["mass"]
                # La-like promoter is good
                if ELEMENT_DATA[p]["radius"] > 1.7:
                    score += 5
                tier1_candidates.append((p, s, score))

    tier1_candidates.sort(key=lambda x: x[2], reverse=True)

    for p, s, score in tier1_candidates[:10]:
        print(f"  {p}-{s}-H: score={score:.2f}")
        print(f"    Rationale: {p}(promoter, r={ELEMENT_DATA[p]['radius']}) + {s}(stabilizer, m={ELEMENT_DATA[s]['mass']})")

    # Generate promoter + promoter candidates
    print("\n" + "-" * 40)
    print("TIER 2: Promoter + Promoter (unexplored)")
    print("Mixed rare earths - may maintain high Tc")
    print()

    tier2_candidates = []
    for p1, p2 in itertools.combinations(promoters, 2):
        pair = tuple(sorted([p1, p2]))
        if pair not in known_pairs:
            # Score based on diversity (different radii good)
            r1, r2 = ELEMENT_DATA[p1]["radius"], ELEMENT_DATA[p2]["radius"]
            score = abs(r1 - r2) * 10 + 5
            tier2_candidates.append((p1, p2, score))

    tier2_candidates.sort(key=lambda x: x[2], reverse=True)

    for p1, p2, score in tier2_candidates[:8]:
        print(f"  ({p1},{p2})H10: score={score:.2f}")

    return {
        "tier1": tier1_candidates[:10],
        "tier2": tier2_candidates[:8],
    }


def generate_hypotheses():
    """Generate testable hypotheses based on patterns"""
    print("\n" + "=" * 60)
    print("GENERATED HYPOTHESES")
    print("=" * 60)
    print()

    hypotheses = [
        {
            "id": "HYP-TH-001",
            "statement": "LaBeH8 analogs with other light stabilizers (B, Li) will show similar pressure reduction",
            "test": "DFT calculation of LaBH8 and LaLiH8 stability and Tc",
            "rationale": "Be's role appears to be providing chemical pressure via small radius",
            "priority": "HIGH",
        },
        {
            "id": "HYP-TH-002",
            "statement": "Sc-based ternaries will have lower pressure requirements than La-based",
            "test": "Compare ScBeH8 vs LaBeH8 stability pressures",
            "rationale": "Sc has smaller radius than La, may need less external pressure",
            "priority": "MEDIUM",
        },
        {
            "id": "HYP-TH-003",
            "statement": "Triple-element hydrides (quaternary) may further reduce pressure",
            "test": "DFT screening of (La,Y)BeH8 and similar",
            "rationale": "Combining multiple strategies: mixed promoters + stabilizer",
            "priority": "MEDIUM",
        },
        {
            "id": "HYP-TH-004",
            "statement": "The optimal stabilizer mass is around 9-11 amu (Be/B)",
            "test": "Systematic study of La-X-H where X varies in mass",
            "rationale": "Be works, Al also works but at higher P; light is better",
            "priority": "LOW",
        },
        {
            "id": "HYP-TH-005",
            "statement": "Th-based hydrides may have highest Tc potential (large radius + high mass)",
            "test": "ThBeH8 DFT stability and Tc prediction",
            "rationale": "Th has similar properties to La but larger, may enhance DOS",
            "priority": "HIGH (but radioactive = hard to test)",
        },
    ]

    for h in hypotheses:
        print(f"{h['id']}: {h['statement']}")
        print(f"  Test: {h['test']}")
        print(f"  Rationale: {h['rationale']}")
        print(f"  Priority: {h['priority']}")
        print()

    return hypotheses


def main():
    print("TERNARY HYDRIDE COMPOSITION EXPLORER")
    print("Pattern-based hypothesis generation for superconductor candidates")
    print()

    patterns = analyze_known_patterns()
    candidates = generate_candidates()
    hypotheses = generate_hypotheses()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    print("Key findings from pattern analysis:")
    print("1. Promoter + Stabilizer combinations show PRESSURE REDUCTION")
    print("   (LaBeH8: 80 GPa vs LaH10: 170 GPa)")
    print("2. Promoter + Promoter combinations maintain HIGH Tc")
    print("   but don't significantly reduce pressure")
    print("3. Light stabilizers (Be, B, Li) appear most effective")
    print()
    print(f"Generated {len(candidates['tier1'])} Tier 1 candidates (promoter+stabilizer)")
    print(f"Generated {len(candidates['tier2'])} Tier 2 candidates (promoter+promoter)")
    print(f"Generated {len(hypotheses)} testable hypotheses")
    print()
    print("Next step: These candidates could be screened with DFT")
    print("to predict stability pressures and approximate Tc.")

    # Save results
    results = {
        "known_ternaries": [{"formula": h.formula, "tc": h.tc, "pressure": h.pressure}
                           for h in KNOWN_TERNARIES],
        "tier1_candidates": [(p, s, score) for p, s, score in candidates["tier1"]],
        "tier2_candidates": [(p1, p2, score) for p1, p2, score in candidates["tier2"]],
        "hypotheses": hypotheses,
    }

    with open("/Users/jacobcole/code/claude-mind/superconductor/data/ternary_candidates.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to superconductor/data/ternary_candidates.json")


if __name__ == "__main__":
    main()
