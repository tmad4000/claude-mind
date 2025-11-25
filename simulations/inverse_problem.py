#!/usr/bin/env python3
"""
Inverse Problem: Given a pattern, can we infer the parameters?

This is a genuinely useful tool - instead of scanning parameter space,
we could ask "what parameters would produce a pattern like THIS?"

Approach:
1. Define pattern features (wavelength, coverage, structure type)
2. Build a mapping from parameters → features
3. Invert: given features → estimate parameters
"""

import numpy as np
from reaction_diffusion import GrayScott
from typing import Tuple, Dict, List
import json


def extract_features(gs: GrayScott) -> Dict:
    """Extract key features from a simulation state."""
    v = gs.V
    m = gs.analyze()

    features = {
        'mean_v': m['mean_v'],
        'std_v': m['std_v'],
        'wavelength': m.get('wavelength', float('inf')),
        'coverage': m['coverage'],
        'pattern': m['pattern'],
    }

    # Additional features for inversion
    # Spatial autocorrelation at lag 5
    row = v[gs.size // 2, :]
    if len(row) > 5:
        autocorr_5 = np.corrcoef(row[:-5], row[5:])[0, 1]
        features['autocorr_5'] = float(autocorr_5) if not np.isnan(autocorr_5) else 0

    # Gradient magnitude (how sharp are boundaries?)
    grad_x = np.diff(v, axis=1)
    grad_y = np.diff(v, axis=0)
    features['gradient_mean'] = float((np.abs(grad_x).mean() + np.abs(grad_y).mean()) / 2)

    return features


def build_feature_database(n_samples: int = 200) -> List[Dict]:
    """
    Sample parameter space and record features.
    This builds a database for inverse lookup.
    """
    print("Building feature database...")

    database = []

    # Sample within the interesting region
    f_range = (0.015, 0.065)
    k_range = (0.04, 0.070)

    for i in range(n_samples):
        f = np.random.uniform(*f_range)
        k = np.random.uniform(*k_range)

        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)

        features = extract_features(gs)
        features['f'] = f
        features['k'] = k

        database.append(features)

        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{n_samples} samples")

    return database


def estimate_parameters(target_features: Dict, database: List[Dict],
                        weights: Dict = None) -> Tuple[float, float, float]:
    """
    Given target features, find the closest match in the database.
    Returns (estimated_f, estimated_k, distance)
    """
    if weights is None:
        weights = {
            'mean_v': 1.0,
            'std_v': 2.0,
            'wavelength': 0.5,
            'coverage': 1.0,
            'gradient_mean': 1.5,
        }

    best_match = None
    best_distance = float('inf')

    for entry in database:
        if entry['pattern'] == 'artifact':
            continue  # Skip numerical artifacts

        distance = 0
        for key, weight in weights.items():
            if key in target_features and key in entry:
                t = target_features[key]
                e = entry[key]
                if isinstance(t, (int, float)) and isinstance(e, (int, float)):
                    if t == float('inf') or e == float('inf'):
                        continue
                    distance += weight * (t - e) ** 2

        if distance < best_distance:
            best_distance = distance
            best_match = entry

    if best_match:
        return best_match['f'], best_match['k'], np.sqrt(best_distance)
    return None, None, float('inf')


def test_inverse_problem():
    """Test if we can recover parameters from patterns."""
    print("=" * 60)
    print("TESTING INVERSE PROBLEM")
    print("=" * 60)

    # Build database
    database = build_feature_database(n_samples=150)

    # Test on known patterns
    test_cases = [
        (0.035, 0.060, "spots"),
        (0.029, 0.057, "maze"),
        (0.055, 0.062, "coral"),
        (0.040, 0.063, "unknown"),
    ]

    print("\n--- Testing parameter recovery ---")

    for true_f, true_k, name in test_cases:
        # Generate pattern
        gs = GrayScott(size=60, f=true_f, k=true_k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)

        features = extract_features(gs)

        # Estimate parameters
        est_f, est_k, dist = estimate_parameters(features, database)

        if est_f:
            f_error = abs(est_f - true_f)
            k_error = abs(est_k - true_k)
            print(f"\n{name} (true: f={true_f}, k={true_k}):")
            print(f"  Estimated: f={est_f:.4f}, k={est_k:.4f}")
            print(f"  Error: df={f_error:.4f}, dk={k_error:.4f}")
            print(f"  Distance: {dist:.4f}")

            # Is this good enough to be useful?
            if f_error < 0.005 and k_error < 0.003:
                print("  >>> GOOD RECOVERY!")
            elif f_error < 0.01 and k_error < 0.005:
                print("  >> Moderate recovery")
            else:
                print("  > Poor recovery")

    # Save database for future use
    print("\n\nSaving database...")

    # Convert to serializable format
    save_db = []
    for entry in database:
        save_entry = {}
        for k, v in entry.items():
            if isinstance(v, (int, float)):
                save_entry[k] = float(v) if v != float('inf') else None
            else:
                save_entry[k] = v
        save_db.append(save_entry)

    with open('../data/feature_database.json', 'w') as f:
        json.dump(save_db, f, indent=2)

    print("Database saved to ../data/feature_database.json")


def visualize_feature_space():
    """See how features map to parameter space."""
    print("\n" + "=" * 60)
    print("FEATURE SPACE VISUALIZATION")
    print("=" * 60)

    # Load or build database
    try:
        with open('../data/feature_database.json', 'r') as f:
            database = json.load(f)
        print(f"Loaded database with {len(database)} entries")
    except:
        database = build_feature_database(n_samples=100)

    # Group by pattern type
    by_pattern = {}
    for entry in database:
        p = entry.get('pattern', 'unknown')
        if p not in by_pattern:
            by_pattern[p] = []
        by_pattern[p].append(entry)

    print("\nPattern distribution:")
    for p, entries in by_pattern.items():
        print(f"  {p}: {len(entries)} samples")

    # Feature statistics by pattern
    print("\nFeature statistics by pattern type:")
    for p, entries in by_pattern.items():
        if len(entries) < 3:
            continue
        print(f"\n{p}:")
        for key in ['mean_v', 'std_v', 'wavelength']:
            vals = [e.get(key) for e in entries if e.get(key) and e.get(key) != float('inf') and e.get(key) is not None]
            if vals:
                print(f"  {key}: mean={np.mean(vals):.3f}, std={np.std(vals):.3f}")


if __name__ == '__main__':
    test_inverse_problem()
    visualize_feature_space()

    print("\n" + "=" * 60)
    print("INSIGHTS")
    print("=" * 60)
    print("""
The inverse problem is HARD because:
1. Many different parameters can produce similar patterns
2. Features don't uniquely determine (f, k)
3. The mapping is many-to-one

But it could be useful for:
- Narrowing search space
- Finding candidate parameters for a desired pattern
- Understanding what features distinguish parameter regions
""")
