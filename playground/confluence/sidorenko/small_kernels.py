"""How small can t(H,W)/E[W]^66 get for TINY bipartite kernels W?

Sidorenko's inequality (bipartite kernel form) says t(H,W) >= E[W]^|E(H)|. The paper's
counterexample needs a large matrix construction (dimension D = 2r, r large) and then
sampling. This asks a much smaller question: with a kernel on an a-point space (points
side) and a b-point space (faces side), with uniform-or-weighted probabilities, does the
ratio ever drop below 1?

Exact computation: given point labels x_1..x_13, faces are independent, so
  t(H,W) = sum_x  prod_i mu(x_i) * prod_faces g(x_{i1}, x_{i2}, x_{i3})
  g(u,v,w) = sum_y nu(y) W(u,y) W(v,y) W(w,y)
which is a^13 terms (8192 for a=2, 1.6M for a=3).
Work in logs to avoid underflow (E[W]^66 is tiny).
"""
import itertools
import math
import random
import sys

import numpy as np

sys.path.insert(0, ".")
from check_H import FACES  # noqa: E402

N_POINTS = 13
N_EDGES = 66


def log_ratio(W, mu, nu):
    """log( t(H,W) / E[W]^66 ) for kernel W (a x b), point probs mu (a), face probs nu (b)."""
    a, b = W.shape
    # g[u,v,w] = sum_y nu[y] W[u,y] W[v,y] W[w,y]
    g = np.einsum("y,uy,vy,wy->uvw", nu, W, W, W)
    mean = float(mu @ W @ nu)
    log_t = -math.inf
    # enumerate all point assignments
    terms = []
    for x in itertools.product(range(a), repeat=N_POINTS):
        lp = sum(math.log(mu[xi]) for xi in x)
        prod = 1.0
        for (i, j, k) in FACES:
            prod *= g[x[i], x[j], x[k]]
            if prod == 0.0:
                break
        if prod > 0.0:
            terms.append(lp + math.log(prod))
    if not terms:
        return -math.inf
    m = max(terms)
    log_t = m + math.log(sum(math.exp(t - m) for t in terms))
    return log_t - N_EDGES * math.log(mean)


def log_ratio_vectorized(W, mu, nu):
    """Same quantity, vectorized over all a^13 assignments (a <= 3)."""
    a, b = W.shape
    g = np.einsum("y,uy,vy,wy->uvw", nu, W, W, W)
    with np.errstate(divide="ignore"):
        log_g = np.log(g)
        log_mu = np.log(mu)
    grid = np.array(list(itertools.product(range(a), repeat=N_POINTS)), dtype=np.int64)
    total = log_mu[grid].sum(axis=1)
    for (i, j, k) in FACES:
        total = total + log_g[grid[:, i], grid[:, j], grid[:, k]]
    m = np.max(total)
    if not np.isfinite(m):
        return -math.inf
    log_t = m + math.log(np.exp(total - m).sum())
    mean = float(mu @ W @ nu)
    return log_t - N_EDGES * math.log(mean)


def random_search(a, b, trials, seed):
    rng = random.Random(seed)
    best = (math.inf, None)
    for _ in range(trials):
        W = np.array([[rng.random() for _ in range(b)] for _ in range(a)])
        mu = np.array([rng.random() + 1e-3 for _ in range(a)]); mu /= mu.sum()
        nu = np.array([rng.random() + 1e-3 for _ in range(b)]); nu /= nu.sum()
        r = log_ratio_vectorized(W, mu, nu)
        if r < best[0]:
            best = (r, (W, mu, nu))
    return best


def local_descent(W, mu, nu, steps, seed, scale=0.05):
    """Greedy random perturbation, keeping W in (0,1] and probabilities positive."""
    rng = np.random.default_rng(seed)
    best = log_ratio_vectorized(W, mu, nu)
    for _ in range(steps):
        W2 = np.clip(W + rng.normal(0, scale, W.shape), 1e-6, 1.0)
        mu2 = np.clip(mu + rng.normal(0, scale, mu.shape), 1e-4, None); mu2 /= mu2.sum()
        nu2 = np.clip(nu + rng.normal(0, scale, nu.shape), 1e-4, None); nu2 /= nu2.sum()
        r = log_ratio_vectorized(W2, mu2, nu2)
        if r < best:
            best, W, mu, nu = r, W2, mu2, nu2
    return best, (W, mu, nu)


if __name__ == "__main__":
    # sanity: a constant kernel gives ratio exactly 1 (log 0)
    W0 = np.full((2, 2), 0.37)
    u = np.array([0.5, 0.5])
    print(f"constant kernel log-ratio (expect 0): {log_ratio_vectorized(W0, u, u):+.3e}")
    # cross-check the vectorized path against the plain loop on a random 2x3 kernel
    rng = np.random.default_rng(1)
    Wt = rng.random((2, 3)); mt = np.array([0.3, 0.7]); nt = np.array([0.2, 0.5, 0.3])
    print(f"loop vs vectorized: {log_ratio(Wt, mt, nt):+.12f} {log_ratio_vectorized(Wt, mt, nt):+.12f}")

    for (a, b, trials, steps) in [(2, 2, 400, 3000), (2, 3, 300, 3000), (2, 4, 200, 2000), (3, 3, 30, 300)]:
        r, params = random_search(a, b, trials, seed=a * 10 + b)
        r, params = local_descent(*params, steps=steps, seed=a * 100 + b)
        W, mu, nu = params
        print(f"a={a} b={b}: min log(t/E^66) found = {r:+.6f}  (ratio {math.exp(r):.6f})")
        print("   W =", np.array2string(W, precision=3).replace("\n", " "),
              " mu =", np.array2string(mu, precision=3), " nu =", np.array2string(nu, precision=3))
