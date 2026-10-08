package confluence.math.naimark;

import java.util.ArrayList;
import java.util.List;

/// Finite-dimensional illustration of the definitions behind OAI.NaimarkZFC.main
/// (lean/ComparatorChallenges/Naimark.lean). It does NOT replicate the theorem: that theorem
/// builds an infinite-dimensional algebra by a recursion of length c^+ (c = 2^aleph0), which no
/// program can enumerate. What can be run is the finite-dimensional meaning of the words.
///
/// - `IsIrreducible` in the challenge: a representation is nonzero and has no closed invariant
///   subspace except 0 and H. In finite dimension this is equivalent (Schur, plus the double
///   commutant theorem) to: the only matrices commuting with every pi(a) are scalars.
/// - The defining representation of M_2 (2x2 complex matrices acting on C^2) passes: its
///   commutant has dimension 1. M_2 is exactly K(C^2), the compact operators on C^2, which is
///   why finite-dimensional algebras are excluded by the theorem's `¬ FiniteDimensional ℂ A`.
/// - Controls that must FAIL irreducibility: the diagonal representation of C^2 = C ⊕ C on C^2
///   (commutant dimension 2), and the doubled representation a -> diag(a, a) of M_2 on C^4
///   (commutant dimension 4 = M_2 again). C ⊕ C also has two inequivalent irreducible
///   representations (its two coordinate characters), so it fails the uniqueness hypothesis.
///
/// The commutant dimension is the nullity of the linear map X -> (X T - T X) over the generators
/// T. All generators here are real matrices, so the complex commutant is the complexification of
/// the real one and has the same dimension; the code therefore does real Gaussian elimination.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.naimark.Naimark
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **"Irreducible" is a computable test in finite dimension.** A Java library that represents
///   an algebra of operators or symmetries by matrices (a quantum-circuit simulator, a physics
///   code using group representations) can decide whether its representation splits into
///   independent blocks by computing the commutant dimension, exactly as `commutantDim` does. A
///   result above 1 means a nontrivial block decomposition exists and could be exploited to
///   shrink the state space.
/// - **A block-diagonal speed-up detector.** The doubled control shows the signature of
///   redundancy: commutant M_k means k identical copies. A simulator could use this to detect
///   that it is carrying k copies of the same subsystem and run one.
/// - **Tolerance is part of the answer.** The rank is computed with a numerical pivot tolerance;
///   generators that are only approximately commuting will be classified by that threshold. A
///   production version should take exact (rational) entries or report the singular values
///   rather than a bare yes/no.
/// - **What Java cannot do here.** Naimark's problem only becomes interesting for
///   infinite-dimensional, in this theorem nonseparable, algebras. No finite matrix computation
///   bears on whether the Lean theorem is true; that rests on the Lean kernel check.
public class Naimark {

    static final double TOL = 1e-10;

    /// d x d real matrix units E_ij.
    static List<double[][]> matrixUnits(int d) {
        List<double[][]> out = new ArrayList<>();
        for (int i = 0; i < d; i++)
            for (int j = 0; j < d; j++) {
                double[][] e = new double[d][d];
                e[i][j] = 1;
                out.add(e);
            }
        return out;
    }

    static double[][] blockDiag(double[][] a, int copies) {
        int n = a.length, d = n * copies;
        double[][] m = new double[d][d];
        for (int c = 0; c < copies; c++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) m[c * n + i][c * n + j] = a[i][j];
        return m;
    }

    /// dim of { X : X T = T X for every T in gens }.
    static int commutantDim(List<double[][]> gens) {
        int d = gens.get(0).length, unknowns = d * d;
        List<double[]> rows = new ArrayList<>();
        for (double[][] t : gens)
            for (int r = 0; r < d; r++)
                for (int c = 0; c < d; c++) {
                    // (XT - TX)[r][c] = sum_k X[r][k] T[k][c] - T[r][k] X[k][c]
                    double[] row = new double[unknowns];
                    for (int k = 0; k < d; k++) {
                        row[r * d + k] += t[k][c];
                        row[k * d + c] -= t[r][k];
                    }
                    rows.add(row);
                }
        return unknowns - rank(rows, unknowns);
    }

    static int rank(List<double[]> rowsIn, int cols) {
        double[][] m = rowsIn.toArray(new double[0][]);
        int rank = 0;
        for (int col = 0; col < cols && rank < m.length; col++) {
            int piv = rank;
            for (int i = rank; i < m.length; i++) if (Math.abs(m[i][col]) > Math.abs(m[piv][col])) piv = i;
            if (Math.abs(m[piv][col]) < TOL) continue;
            double[] tmp = m[piv]; m[piv] = m[rank]; m[rank] = tmp;
            for (int i = 0; i < m.length; i++) {
                if (i == rank) continue;
                double f = m[i][col] / m[rank][col];
                if (f != 0) for (int k = col; k < cols; k++) m[i][k] -= f * m[rank][k];
            }
            rank++;
        }
        return rank;
    }

    static int failures = 0;

    static void expect(String name, int got, int want) {
        boolean ok = got == want;
        if (!ok) failures++;
        System.out.printf("%s %-62s commutant dim = %d (expected %d)%n", ok ? "PASS" : "FAIL", name, got, want);
    }

    public static void main(String[] args) {
        System.out.println("Irreducible <=> commutant is the scalars (dimension 1), in finite dimension.");
        expect("M_2 on C^2, defining rep  (irreducible; M_2 = K(C^2))", commutantDim(matrixUnits(2)), 1);
        expect("M_3 on C^3, defining rep  (irreducible; M_3 = K(C^3))", commutantDim(matrixUnits(3)), 1);

        List<double[][]> doubled = new ArrayList<>();
        for (double[][] e : matrixUnits(2)) doubled.add(blockDiag(e, 2));
        expect("CONTROL M_2 on C^4, a -> diag(a,a)  (reducible)", commutantDim(doubled), 4);

        List<double[][]> cPlusC = List.of(new double[][]{{1, 0}, {0, 0}}, new double[][]{{0, 0}, {0, 1}});
        expect("CONTROL C(+)C on C^2, diagonal  (reducible)", commutantDim(cPlusC), 2);

        // The two characters of C(+)C: chi1(x,y) = x, chi2(x,y) = y. Each is 1-dimensional and
        // nonzero, hence irreducible. An intertwiner U : C -> C with U chi1(e) = chi2(e) U for
        // e = (1,0) forces U * 1 = 0 * U, i.e. U = 0: no unitary, so they are inequivalent.
        // In general the 1x1 intertwiners of two characters form {U : (chi1(g) - chi2(g)) U = 0
        // for all generators g}, of dimension 1 if the characters agree on every generator, else 0.
        double[][] gens = {{1, 0}, {0, 1}};               // e1 = (1,0), e2 = (0,1)
        java.util.function.ToDoubleFunction<double[]> chi1 = g -> g[0], chi2 = g -> g[1];
        int homDim = 1;
        for (double[] g : gens) if (Math.abs(chi1.applyAsDouble(g) - chi2.applyAsDouble(g)) > TOL) homDim = 0;
        int selfDim = 1;
        for (double[] g : gens) if (Math.abs(chi1.applyAsDouble(g) - chi1.applyAsDouble(g)) > TOL) selfDim = 0;
        boolean ok = homDim == 0 && selfDim == 1;
        System.out.printf("%s %-62s Hom(chi1,chi2) dim = %d, Hom(chi1,chi1) dim = %d%n", ok ? "PASS" : "FAIL",
            "CONTROL C(+)C: two inequivalent irreducible reps", homDim, selfDim);
        if (!ok) failures++;

        System.out.println(failures == 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED");
        if (failures != 0) System.exit(1);
    }
}
