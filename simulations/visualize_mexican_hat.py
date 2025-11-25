"""
Visualize the Mexican Hat / RD Connection

Shows how the same mathematical structure creates patterns in both:
1. Neural fields (Mexican-hat coupling)
2. Reaction-diffusion (activator-inhibitor)

This is the QRI connection - why psychedelic visuals look like Turing patterns!
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, laplace

def mexican_hat_kernel(size=31, sigma_e=3.0, sigma_i=7.0, A_e=1.0, A_i=0.5):
    """Mexican hat = difference of Gaussians"""
    x = np.linspace(-size//2, size//2, size)
    X, Y = np.meshgrid(x, x)
    R2 = X**2 + Y**2

    excitation = A_e * np.exp(-R2 / (2 * sigma_e**2))
    inhibition = A_i * np.exp(-R2 / (2 * sigma_i**2))

    return excitation - inhibition

def simulate_neural_field(N=128, steps=800, kernel=None):
    """Neural field with Mexican-hat coupling"""
    if kernel is None:
        kernel = mexican_hat_kernel()

    # Normalize kernel
    kernel = kernel / np.abs(kernel).sum() * 15

    # Start with noise
    u = np.random.randn(N, N) * 0.5

    for _ in range(steps):
        # Sigmoid activation
        activity = 1 / (1 + np.exp(-5 * (u - 0.3)))
        # Coupling
        coupling = convolve(activity, kernel, mode='wrap')
        # Update with leak
        u = 0.9 * u + 0.1 * coupling + 0.01 * np.random.randn(N, N)

    return u

def simulate_gray_scott(N=128, steps=8000, f=0.035, k=0.060):
    """Standard Gray-Scott for comparison"""
    Du, Dv = 0.16, 0.08
    dt = 1.0

    U = np.ones((N, N))
    V = np.zeros((N, N))

    # Seed
    r = 15
    cx, cy = N//2, N//2
    V[cx-r:cx+r, cy-r:cy+r] = 0.25 + 0.1 * np.random.rand(2*r, 2*r)

    for _ in range(steps):
        uvv = U * V * V
        U += dt * (Du * laplace(U) - uvv + f * (1 - U))
        V += dt * (Dv * laplace(V) + uvv - (f + k) * V)

    return V

# Generate visualizations
print("Generating Mexican Hat kernel...")
kernel = mexican_hat_kernel(size=51, sigma_e=4, sigma_i=10, A_e=1.0, A_i=0.4)

print("Simulating neural field patterns...")
neural_pattern = simulate_neural_field(N=128, steps=1000, kernel=mexican_hat_kernel(31, 4, 10, 1.0, 0.4))

print("Simulating Gray-Scott patterns...")
gs_pattern = simulate_gray_scott(N=128, steps=10000, f=0.035, k=0.062)

# Create the figure
fig = plt.figure(figsize=(16, 10))
fig.suptitle('The Mexican Hat / Reaction-Diffusion Connection\nWhy Psychedelic Visuals Look Like Turing Patterns',
             fontsize=16, fontweight='bold')

# 1. Mexican Hat Kernel (2D)
ax1 = fig.add_subplot(2, 3, 1)
im1 = ax1.imshow(kernel, cmap='RdBu_r', extent=[-25, 25, -25, 25])
ax1.set_title('Mexican Hat Kernel\n(Neural Coupling)', fontsize=12)
ax1.set_xlabel('Distance')
ax1.set_ylabel('Distance')
plt.colorbar(im1, ax=ax1, label='Coupling strength')

# 2. Mexican Hat Profile (1D slice)
ax2 = fig.add_subplot(2, 3, 2)
center = kernel.shape[0] // 2
profile = kernel[center, :]
x = np.arange(len(profile)) - center
ax2.plot(x, profile, 'b-', linewidth=2)
ax2.axhline(0, color='k', linestyle='--', alpha=0.3)
ax2.fill_between(x, profile, 0, where=profile > 0, alpha=0.3, color='green', label='Excitation')
ax2.fill_between(x, profile, 0, where=profile < 0, alpha=0.3, color='red', label='Inhibition')
ax2.set_title('Coupling Profile\n(Cross-section)', fontsize=12)
ax2.set_xlabel('Distance from center')
ax2.set_ylabel('Coupling strength')
ax2.legend()
ax2.set_xlim(-25, 25)

# 3. The equivalence diagram
ax3 = fig.add_subplot(2, 3, 3)
ax3.axis('off')
equiv_text = """
MATHEMATICAL EQUIVALENCE

Neural Field (QRI)          Reaction-Diffusion
─────────────────          ──────────────────
Short-range excitation  ↔  Slow activator (Du)
Long-range inhibition   ↔  Fast inhibitor (Dv)
Mexican-hat kernel      ↔  Differential diffusion
Wallpaper symmetries    ↔  Turing patterns

SAME MATH → SAME PATTERNS

This is why:
• Psychedelic visuals (neural)
• Animal skins (biological RD)
• Chemical patterns (BZ reaction)

...all look similar!
"""
ax3.text(0.1, 0.9, equiv_text, transform=ax3.transAxes, fontsize=11,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax3.set_title('The Connection', fontsize=12)

# 4. Neural field pattern
ax4 = fig.add_subplot(2, 3, 4)
im4 = ax4.imshow(neural_pattern, cmap='magma')
ax4.set_title('Neural Field Pattern\n(Mexican-hat coupling)', fontsize=12)
ax4.axis('off')
plt.colorbar(im4, ax=ax4, label='Activity')

# 5. Gray-Scott pattern
ax5 = fig.add_subplot(2, 3, 5)
im5 = ax5.imshow(gs_pattern, cmap='magma')
ax5.set_title('Gray-Scott Pattern\n(Activator-inhibitor RD)', fontsize=12)
ax5.axis('off')
plt.colorbar(im5, ax=ax5, label='Concentration')

# 6. Klüver form constants
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis('off')
form_text = """
KLÜVER'S FORM CONSTANTS
(What people see on psychedelics)

1. Lattices / Grids
2. Cobwebs
3. Tunnels / Funnels
4. Spirals

ALL arise from Turing-like
instabilities in visual cortex!

(Bressloff et al. 2001)
"""
ax6.text(0.1, 0.9, form_text, transform=ax6.transAxes, fontsize=12,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax6.set_title("Psychedelic Geometry", fontsize=12)

plt.tight_layout()
plt.savefig('mexican_hat_connection.png', dpi=150, bbox_inches='tight')
print("Saved: mexican_hat_connection.png")
plt.close()

print("\nDone! The key insight:")
print("Mexican-hat coupling in neural fields IS the activator-inhibitor")
print("mechanism of Turing patterns, just in different language.")
print("This is why psychedelic visuals look like reaction-diffusion patterns!")
