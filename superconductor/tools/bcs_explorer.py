#!/usr/bin/env python3
"""
BCS Theory Explorer

A toy simulation to build intuition about superconductivity parameters.
NOT for real predictions - just to understand the relationships.

BCS Theory basics:
- Tc ~ ω_D * exp(-1/(N(E_F)*V))
- ω_D = Debye frequency (related to atomic mass, bond stiffness)
- N(E_F) = density of states at Fermi level
- V = electron-phonon coupling strength

McMillan-Allen-Dynes formula (more realistic):
- Tc = (ω_log/1.2) * exp(-1.04*(1+λ) / (λ - μ*(1+0.62*λ)))
- λ = electron-phonon coupling constant
- μ* = Coulomb pseudopotential (~0.1-0.15)
- ω_log = logarithmic average phonon frequency
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Physical constants
k_B = 8.617e-5  # eV/K

def bcs_tc(omega_D, N_Ef, V):
    """
    Simple BCS Tc estimate
    omega_D: Debye frequency in meV
    N_Ef: density of states at Fermi level (states/eV/atom)
    V: electron-phonon coupling (eV)
    """
    exponent = -1 / (N_Ef * V) if N_Ef * V > 0 else -100
    # Convert omega_D from meV to K (1 meV ≈ 11.6 K)
    omega_D_K = omega_D * 11.6
    return 1.13 * omega_D_K * np.exp(exponent)

def mcmillan_tc(omega_log, lambda_ep, mu_star=0.1):
    """
    McMillan-Allen-Dynes formula for Tc
    omega_log: logarithmic average phonon frequency (K)
    lambda_ep: electron-phonon coupling constant (dimensionless)
    mu_star: Coulomb pseudopotential
    """
    if lambda_ep <= mu_star * (1 + 0.62 * lambda_ep):
        return 0  # No superconductivity

    prefactor = omega_log / 1.2
    numerator = -1.04 * (1 + lambda_ep)
    denominator = lambda_ep - mu_star * (1 + 0.62 * lambda_ep)

    return prefactor * np.exp(numerator / denominator)

def explore_parameter_space():
    """
    Visualize how Tc depends on parameters
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Tc vs lambda for different omega_log
    ax1 = axes[0, 0]
    lambdas = np.linspace(0.3, 3, 100)
    for omega in [100, 300, 500, 1000, 2000]:  # K
        tcs = [mcmillan_tc(omega, l) for l in lambdas]
        ax1.plot(lambdas, tcs, label=f'ω_log = {omega} K')
    ax1.set_xlabel('λ (electron-phonon coupling)')
    ax1.set_ylabel('Tc (K)')
    ax1.set_title('Effect of Phonon Frequency')
    ax1.legend()
    ax1.axhline(y=300, color='r', linestyle='--', alpha=0.5, label='Room temp')
    ax1.set_ylim(0, 350)

    # Plot 2: Tc vs omega_log for different lambda
    ax2 = axes[0, 1]
    omegas = np.linspace(100, 3000, 100)  # K
    for l in [0.5, 1.0, 1.5, 2.0, 2.5]:
        tcs = [mcmillan_tc(o, l) for o in omegas]
        ax2.plot(omegas, tcs, label=f'λ = {l}')
    ax2.set_xlabel('ω_log (K)')
    ax2.set_ylabel('Tc (K)')
    ax2.set_title('Effect of Coupling Strength')
    ax2.legend()
    ax2.axhline(y=300, color='r', linestyle='--', alpha=0.5)
    ax2.set_ylim(0, 350)

    # Plot 3: Effect of mu* (Coulomb repulsion)
    ax3 = axes[1, 0]
    mu_stars = [0.05, 0.10, 0.13, 0.15, 0.20]
    for mu in mu_stars:
        tcs = [mcmillan_tc(500, l, mu) for l in lambdas]
        ax3.plot(lambdas, tcs, label=f'μ* = {mu}')
    ax3.set_xlabel('λ (electron-phonon coupling)')
    ax3.set_ylabel('Tc (K)')
    ax3.set_title('Effect of Coulomb Repulsion (ω_log=500K)')
    ax3.legend()
    ax3.set_ylim(0, 200)

    # Plot 4: What's needed for room temperature?
    ax4 = axes[1, 1]
    # Find lambda needed for Tc=300K at various omega_log
    target_tc = 300
    omegas_check = np.linspace(500, 5000, 50)
    required_lambdas = []
    for omega in omegas_check:
        # Binary search for lambda that gives Tc=300
        for l in np.linspace(0.1, 10, 1000):
            if mcmillan_tc(omega, l) >= target_tc:
                required_lambdas.append(l)
                break
        else:
            required_lambdas.append(np.nan)

    ax4.plot(omegas_check, required_lambdas, 'b-', linewidth=2)
    ax4.fill_between(omegas_check, required_lambdas, 10, alpha=0.3, label='Room-temp SC possible')
    ax4.set_xlabel('ω_log (K)')
    ax4.set_ylabel('Required λ for Tc=300K')
    ax4.set_title('What Parameters Give Room-Temp SC?')
    ax4.set_ylim(0, 5)
    ax4.axhline(y=2, color='orange', linestyle='--', alpha=0.7, label='Typical max λ')
    ax4.legend()

    plt.tight_layout()
    plt.savefig('/Users/jacobcole/code/claude-mind/superconductor/bcs_parameter_space.png', dpi=150)
    plt.close()
    print("Saved: bcs_parameter_space.png")

def analyze_known_superconductors():
    """
    Plot known superconductors in parameter space
    """
    # Data for known superconductors (approximate values)
    # Format: (name, Tc, omega_log estimate, lambda estimate)
    superconductors = [
        ("Pb", 7.2, 105, 1.55),
        ("Nb", 9.3, 277, 0.98),
        ("Al", 1.2, 428, 0.43),
        ("MgB2", 39, 670, 0.87),
        ("H3S (150 GPa)", 203, 1500, 2.2),
        ("LaH10 (170 GPa)", 260, 1800, 2.5),
        # Cuprates don't fit BCS, but including for comparison
        ("YBCO*", 93, None, None),  # *not BCS mechanism
        ("HgBa2Ca2Cu3O8*", 135, None, None),  # *not BCS mechanism
    ]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot lambda vs omega_log, color by Tc
    for name, tc, omega, lam in superconductors:
        if omega is not None and lam is not None:
            ax.scatter(omega, lam, s=tc*3, c='blue', alpha=0.6, edgecolors='black')
            ax.annotate(f'{name}\nTc={tc}K', (omega, lam), fontsize=8,
                       xytext=(5, 5), textcoords='offset points')

    # Show where Tc=300K would be
    omegas = np.linspace(100, 3000, 100)
    lambdas_for_300K = []
    for o in omegas:
        for l in np.linspace(0.1, 10, 500):
            if mcmillan_tc(o, l) >= 300:
                lambdas_for_300K.append(l)
                break
        else:
            lambdas_for_300K.append(np.nan)

    ax.plot(omegas, lambdas_for_300K, 'r--', linewidth=2, label='Tc=300K boundary')
    ax.fill_between(omegas, lambdas_for_300K, 5, alpha=0.2, color='red')

    ax.set_xlabel('ω_log (K) - related to atomic mass')
    ax.set_ylabel('λ - electron-phonon coupling')
    ax.set_title('Known Superconductors in BCS Parameter Space')
    ax.set_xlim(0, 3000)
    ax.set_ylim(0, 4)
    ax.legend()

    # Add annotations
    ax.annotate('Lighter atoms\n(higher phonon freq)', xy=(2500, 0.5), fontsize=9, style='italic')
    ax.annotate('Stronger\ncoupling', xy=(200, 3.5), fontsize=9, style='italic')
    ax.annotate('Room-temp region\n(conventional BCS)', xy=(2000, 3), fontsize=10,
               color='red', weight='bold')

    plt.tight_layout()
    plt.savefig('/Users/jacobcole/code/claude-mind/superconductor/known_superconductors.png', dpi=150)
    plt.close()
    print("Saved: known_superconductors.png")

def main():
    print("BCS Theory Explorer")
    print("=" * 40)
    print()
    print("Key insight: To get room-temperature Tc with BCS mechanism:")
    print("  - Need high phonon frequency (light atoms like H)")
    print("  - Need strong electron-phonon coupling (λ > 2)")
    print("  - This is why hydrides under pressure work!")
    print()
    print("But BCS has limits:")
    print("  - McMillan showed ~40K ceiling for normal metals")
    print("  - Getting λ > 2 is physically difficult")
    print("  - Cuprates work via different mechanism (superexchange)")
    print()

    explore_parameter_space()
    analyze_known_superconductors()

    print()
    print("The key question: Can we find materials with:")
    print("  1. Very light atoms (high ω_log) - like hydrogen")
    print("  2. Strong coupling (high λ)")
    print("  3. WITHOUT needing extreme pressure")
    print()
    print("Or: Find a different mechanism (like cuprates) that doesn't")
    print("have these BCS limitations.")

if __name__ == "__main__":
    main()
