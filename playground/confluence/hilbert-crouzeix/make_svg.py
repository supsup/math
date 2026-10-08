"""Draw W([[1,2],[0,i]]) (an ellipse with foci at the eigenvalues 1 and i, minor axis 2) as pure SVG.

Every plotted point is computed here: the boundary from the top eigenvector of Re(e^{-it}A), the two
sample points x^*Ax, y^*Ay from seeded random unit vectors, their midpoint, and the point v^*Av for the
unit vector v found by search in span{x,y}. The dashed curve is the REAL-vector set {x^T A x}
(negative control): the midpoint of two of its points is generally off the curve.
"""
import numpy as np
from numerical_range import boundary, attain, rand_unit, real_attain

A = np.array([[1, 2], [0, 1j]], dtype=complex)
b = boundary(A)
rng = np.random.default_rng(7)
x = rng.standard_normal(2) + 1j * rng.standard_normal(2); x /= np.linalg.norm(x)
y = rng.standard_normal(2) + 1j * rng.standard_normal(2); y /= np.linalg.norm(y)
zx, zy = np.vdot(x, A @ x), np.vdot(y, A @ y)
mid = (zx + zy) / 2
resid = attain(A, mid, x, y)
th = np.linspace(0, 2 * np.pi, 721)
realcurve = np.array([np.array([np.cos(t), np.sin(t)]) @ A @ np.array([np.cos(t), np.sin(t)]) for t in th])
eig = np.linalg.eigvals(A)

S, OX, OY, W, H = 110, 260, 270, 560, 480
def P(z):
    return OX + S * z.real, OY - S * z.imag
def path(zs):
    return "M " + " L ".join(f"{P(z)[0]:.2f},{P(z)[1]:.2f}" for z in zs) + " Z"

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="sans-serif" font-size="12">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
       f'<line x1="0" y1="{OY}" x2="{W}" y2="{OY}" stroke="#bbb"/><line x1="{OX}" y1="0" x2="{OX}" y2="{H}" stroke="#bbb"/>',
       f'<path d="{path(b)}" fill="#cfe3f7" stroke="#1f5fa8" stroke-width="2"/>',
       f'<path d="{path(realcurve)}" fill="none" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="5,4"/>']
for z, lab in ((zx, "x*Ax"), (zy, "y*Ay")):
    px, py = P(z); out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4" fill="#1f5fa8"/><text x="{px+6:.2f}" y="{py-6:.2f}">{lab}</text>')
(ax, ay), (bx, by) = P(zx), P(zy)
out.append(f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="#1f5fa8" stroke-dasharray="3,3"/>')
mx, my = P(mid)
out.append(f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="5" fill="none" stroke="#111" stroke-width="2"/><text x="{mx+8:.2f}" y="{my+14:.2f}">midpoint = v*Av (resid {resid:.0e})</text>')
for z in eig:
    px, py = P(z); out.append(f'<path d="M {px-5:.2f},{py-5:.2f} L {px+5:.2f},{py+5:.2f} M {px-5:.2f},{py+5:.2f} L {px+5:.2f},{py-5:.2f}" stroke="#111" stroke-width="2"/>')
    out.append(f'<text x="{px+7:.2f}" y="{py+4:.2f}">eig {z.real:.0f}{"+" if z.imag>=0 else "-"}{abs(z.imag):.0f}i</text>')
out += ['<text x="12" y="20" font-size="14">W(A), A = [[1,2],[0,i]]: compact, convex, contains spectrum</text>',
        '<text x="12" y="40" fill="#1f5fa8">filled: numerical range (ellipse, foci = eigenvalues)</text>',
        '<text x="12" y="58" fill="#c0392b">dashed: real-vector variant {x^T A x} (control: a curve, not convex)</text>',
        '</svg>']
open("numerical-range.svg", "w").write("\n".join(out) + "\n")
print(f"midpoint {mid:.6f}, attained residual {resid:.2e}; real-variant miss of same midpoint {real_attain(A, mid):.4f}")
