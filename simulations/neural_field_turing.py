"""
Neural Field Model with Mexican-Hat Coupling

Demonstrates how the same mathematical structure that creates Turing patterns
in reaction-diffusion systems also creates patterns in neural field models.

Key insight: Mexican-hat coupling in neural fields IS the activator-inhibitor
mechanism of Turing patterns, just expressed in different terms.

Connection to QRI/psychedelic research:
- QRI proposes that psychedelics modify coupling kernels
- Mexican-hat = short-range inhibition + medium-range excitation
- This creates the same instability as activator-inhibitor RD systems
"""

import numpy as np
from scipy.ndimage import convolve
from scipy.ndimage import laplace
import json

def mexican_hat_kernel(size=21, sigma_e=2.0, sigma_i=4.0, A_e=1.0, A_i=0.5):
    """
    Create a Mexican hat (difference of Gaussians) coupling kernel.

    This is the neural field equivalent of the activator-inhibitor mechanism:
    - Excitation (positive) at short range (sigma_e)
    - Inhibition (negative) at medium range (sigma_i)

    Note: QRI describes this with reversed signs (negative short, positive medium)
    but the pattern-forming dynamics are mathematically equivalent.
    """
    x = np.linspace(-size//2, size//2, size)
    y = np.linspace(-size//2, size//2, size)
    X, Y = np.meshgrid(x, y)
    R2 = X**2 + Y**2

    # Difference of Gaussians
    excitation = A_e * np.exp(-R2 / (2 * sigma_e**2))
    inhibition = A_i * np.exp(-R2 / (2 * sigma_i**2))

    kernel = excitation - inhibition

    # Normalize
    kernel = kernel / np.abs(kernel).sum() * 10

    return kernel

def sigmoid(x, steepness=10, threshold=0.5):
    """Sigmoid activation function for neural activity."""
    return 1 / (1 + np.exp(-steepness * (x - threshold)))

def simulate_neural_field(N=128, steps=500, dt=0.1, tau=10.0,
                          sigma_e=3.0, sigma_i=8.0, A_e=1.0, A_i=0.6,
                          noise_strength=0.1, input_strength=0.0):
    """
    Simulate a 2D neural field with Mexican-hat coupling.

    The equation is:
    tau * du/dt = -u + W * f(u) + noise + input

    where W is the Mexican-hat coupling kernel and f is sigmoid activation.

    Parameters:
    -----------
    sigma_e, sigma_i : Excitation and inhibition spread
    A_e, A_i : Excitation and inhibition strength

    Returns:
    --------
    Final activity pattern and history
    """
    # Create coupling kernel
    kernel = mexican_hat_kernel(21, sigma_e, sigma_i, A_e, A_i)

    # Initialize with noise
    u = np.random.randn(N, N) * 0.1

    history = []

    for step in range(steps):
        # Apply coupling (convolution with Mexican hat)
        coupling = convolve(sigmoid(u), kernel, mode='wrap')

        # Add small noise
        noise = np.random.randn(N, N) * noise_strength * np.sqrt(dt)

        # Neural field dynamics
        du = (-u + coupling + noise + input_strength) / tau
        u = u + dt * du

        # Record history periodically
        if step % 50 == 0:
            history.append(u.copy())

    return u, history, kernel

def simulate_grayscott_for_comparison(N=128, steps=5000, f=0.035, k=0.060):
    """
    Standard Gray-Scott for comparison.
    Shows same pattern types emerge from different equations.
    """
    Du, Dv = 0.16, 0.08
    dt = 1.0

    U = np.ones((N, N))
    V = np.zeros((N, N))

    # Seed
    r = N // 10
    cx, cy = N // 2, N // 2
    V[cx-r:cx+r, cy-r:cy+r] = 0.25

    for _ in range(steps):
        uvv = U * V * V
        U += dt * (Du * laplace(U) - uvv + f * (1 - U))
        V += dt * (Dv * laplace(V) + uvv - (f + k) * V)

    return U, V

def analyze_pattern(field):
    """Analyze pattern characteristics."""
    # FFT to get dominant wavelength
    fft = np.fft.fft2(field)
    power = np.abs(fft)**2

    # Find peak (excluding DC)
    power[0, 0] = 0
    N = field.shape[0]

    # Radial averaging
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - N//2)**2 + (y - N//2)**2)
    r = r.astype(int)

    power_shifted = np.fft.fftshift(power)
    radial_profile = np.bincount(r.ravel(), power_shifted.ravel()) / np.bincount(r.ravel())

    # Find peak wavelength (excluding first few bins)
    peak_k = np.argmax(radial_profile[3:]) + 3
    wavelength = N / peak_k if peak_k > 0 else np.inf

    return {
        'wavelength': float(wavelength),
        'mean': float(np.mean(field)),
        'std': float(np.std(field)),
        'max': float(np.max(field)),
        'min': float(np.min(field))
    }

def test_coupling_parameters():
    """
    Test how different coupling parameters affect pattern formation.

    This parallels how f,k parameters affect Gray-Scott:
    - sigma_i/sigma_e ratio ~ Du/Dv ratio (diffusion ratio)
    - A_i/A_e ratio ~ k/f ratio (reaction balance)
    """
    results = []

    # Test different inhibition/excitation ratios
    for sigma_ratio in [1.5, 2.0, 2.5, 3.0, 4.0]:
        for A_ratio in [0.4, 0.5, 0.6, 0.7, 0.8]:
            sigma_e = 3.0
            sigma_i = sigma_e * sigma_ratio
            A_e = 1.0
            A_i = A_e * A_ratio

            try:
                u, history, _ = simulate_neural_field(
                    N=64, steps=300, dt=0.1,
                    sigma_e=sigma_e, sigma_i=sigma_i,
                    A_e=A_e, A_i=A_i,
                    noise_strength=0.05
                )

                analysis = analyze_pattern(u)

                results.append({
                    'sigma_ratio': sigma_ratio,
                    'A_ratio': A_ratio,
                    'wavelength': analysis['wavelength'],
                    'pattern_std': analysis['std'],
                    'has_pattern': analysis['std'] > 0.1
                })

                print(f"σ_i/σ_e={sigma_ratio:.1f}, A_i/A_e={A_ratio:.1f}: "
                      f"wavelength={analysis['wavelength']:.1f}, "
                      f"pattern_std={analysis['std']:.3f}")
            except Exception as e:
                print(f"Failed at σ_i/σ_e={sigma_ratio}, A_i/A_e={A_ratio}: {e}")

    return results

def compare_neural_vs_rd():
    """
    Direct comparison: neural field patterns vs Gray-Scott patterns.

    Key insight: Both produce similar pattern geometries because
    they share the same mathematical structure:
    - Local positive feedback (activation/excitation)
    - Longer-range negative feedback (inhibition)
    """
    print("="*60)
    print("COMPARING NEURAL FIELD AND GRAY-SCOTT PATTERNS")
    print("="*60)

    # Neural field - tuned for spots
    print("\n1. Neural Field (Mexican-hat coupling):")
    u_neural, _, kernel = simulate_neural_field(
        N=128, steps=500, dt=0.1,
        sigma_e=3.0, sigma_i=8.0, A_e=1.0, A_i=0.55,
        noise_strength=0.05
    )
    neural_analysis = analyze_pattern(u_neural)
    print(f"   Wavelength: {neural_analysis['wavelength']:.1f}")
    print(f"   Pattern strength: {neural_analysis['std']:.3f}")

    # Gray-Scott - spots
    print("\n2. Gray-Scott (activator-inhibitor RD):")
    U_gs, V_gs = simulate_grayscott_for_comparison(N=128, steps=5000, f=0.035, k=0.060)
    gs_analysis = analyze_pattern(V_gs)
    print(f"   Wavelength: {gs_analysis['wavelength']:.1f}")
    print(f"   Pattern strength: {gs_analysis['std']:.3f}")

    print("\n" + "="*60)
    print("KEY INSIGHT:")
    print("Both systems produce patterns via the SAME mechanism:")
    print("- Short-range positive feedback (activation/excitation)")
    print("- Long-range negative feedback (inhibition)")
    print("This is why psychedelic visuals (neural) look like RD patterns!")
    print("="*60)

    return {
        'neural': {
            'pattern': u_neural.tolist(),
            'analysis': neural_analysis,
            'kernel': kernel.tolist()
        },
        'grayscott': {
            'pattern': V_gs.tolist(),
            'analysis': gs_analysis
        }
    }

if __name__ == "__main__":
    print("Neural Field Pattern Formation")
    print("="*50)

    # Run comparison
    comparison = compare_neural_vs_rd()

    print("\n\nTesting parameter space...")
    param_results = test_coupling_parameters()

    # Save results
    results = {
        'comparison': {
            'neural_wavelength': comparison['neural']['analysis']['wavelength'],
            'grayscott_wavelength': comparison['grayscott']['analysis']['wavelength'],
            'neural_std': comparison['neural']['analysis']['std'],
            'grayscott_std': comparison['grayscott']['analysis']['std']
        },
        'parameter_scan': param_results,
        'key_finding': (
            "Mexican-hat neural coupling and Gray-Scott RD produce similar patterns "
            "because they share the same mathematical structure: local positive feedback "
            "with longer-range negative feedback. This explains why QRI's work on "
            "psychedelic geometry connects to Turing patterns."
        )
    }

    with open('neural_field_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to neural_field_results.json")
