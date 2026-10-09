package confluence.math.seymour;

/// Java replication of the DEFINITIONS behind OAI.SeymourSecondNeighborhood.exists_goodVertex
/// (lean/ComparatorChallenges/SeymourSecondNeighborhood.lean).
///
/// The theorem says: every nonempty finite ORIENTED graph (no loops, no 2-cycles) has a vertex v
/// whose second out-neighbourhood (vertices at directed distance exactly 2: not v, not an
/// out-neighbour of v, but reachable by v -> u -> w) is at least as large as its first
/// out-neighbourhood. That is Seymour's second-neighbourhood conjecture (1990). Java cannot check
/// every finite graph, but it can check EVERY oriented graph on up to six labelled vertices
/// exhaustively: each unordered pair is absent, one way, or the other, so there are 3^C(n,2) of
/// them (14,348,907 for n = 6).
///
/// The definitions are transcribed literally: `firstNeighbors`, `secondNeighbors` (w != v, not
/// r v w, and some u with r v u and r u w), and `GoodVertex` (|first| <= |second|).
///
/// Controls: dropping the ORIENTED hypothesis breaks it. The complete symmetric digraph (every
/// ordered pair an arc) has no good vertex, because every vertex is already a first neighbour, so
/// none is a second neighbour. A wrong second neighbourhood that forgets to exclude first neighbours
/// is also reported, by counting how often it would change which vertices are good.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.seymour.SecondNeighborhood
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Two-hop reach never loses to one-hop reach somewhere.** In any one-way relation with no
///   mutual pairs (who-beat-whom in a tournament, one-directional follows, a dependency DAG, task
///   precedence), some node reaches at least as many nodes at exactly two hops as at one. A Java
///   service that ranks "influence" by two-hop reach can rely on a node whose second ring is no
///   smaller than its first, which is a sanity bound for recommender or propagation heuristics.
/// - **The hypothesis is the whole point.** Allow mutual pairs and the guarantee is gone (the
///   symmetric control). Code that applies the bound must check for two-cycles first, and that is
///   cheap: one pass over the adjacency.
/// - **Exhaustive small cases as a regression net.** 14 million graphs on six vertices run in
///   seconds with bitmasks. That is a pattern worth keeping for any graph algorithm with a
///   combinatorial guarantee: test it on every small instance, not a few hand-picked ones.
public class SecondNeighborhood {

    static int failures = 0;

    static void check(String name, boolean ok) {
        System.out.println((ok ? "ok   " : "FAIL ") + name);
        if (!ok) failures++;
    }

    /// out[v] is the bitmask of v's out-neighbours.
    static int first(int[] out, int v) { return Integer.bitCount(out[v]); }

    static int second(int[] out, int v, boolean excludeFirst) {
        int reach = 0;
        for (int u = 0; u < out.length; u++) if ((out[v] >> u & 1) != 0) reach |= out[u];
        reach &= ~(1 << v);
        if (excludeFirst) reach &= ~out[v];
        return Integer.bitCount(reach);
    }

    static boolean hasGoodVertex(int[] out) {
        for (int v = 0; v < out.length; v++) if (first(out, v) <= second(out, v, true)) return true;
        return false;
    }

    public static void main(String[] args) {
        for (int n = 1; n <= 6; n++) {
            int pairs = n * (n - 1) / 2;
            int[] pu = new int[pairs], pv = new int[pairs];
            for (int a = 0, k = 0; a < n; a++)
                for (int b = a + 1; b < n; b++, k++) { pu[k] = a; pv[k] = b; }
            long total = 1;
            for (int k = 0; k < pairs; k++) total *= 3;
            long bad = 0, wrongDiffers = 0;
            int[] out = new int[n];
            int[] digit = new int[pairs];
            for (long code = 0; code < total; code++) {
                // decode code in base 3: 0 = no arc, 1 = a -> b, 2 = b -> a
                java.util.Arrays.fill(out, 0);
                long c = code;
                for (int k = 0; k < pairs; k++) {
                    digit[k] = (int) (c % 3); c /= 3;
                    if (digit[k] == 1) out[pu[k]] |= 1 << pv[k];
                    else if (digit[k] == 2) out[pv[k]] |= 1 << pu[k];
                }
                if (!hasGoodVertex(out)) bad++;
                for (int v = 0; v < n; v++) {
                    boolean right = first(out, v) <= second(out, v, true);
                    boolean wrong = first(out, v) <= second(out, v, false);
                    if (right != wrong) { wrongDiffers++; break; }
                }
            }
            check("n = " + n + ": all " + total + " oriented graphs have a good vertex (failures: " + bad + ")", bad == 0);
            if (n == 6)
                check("control: forgetting to exclude first neighbours changes the verdict at some vertex in "
                    + wrongDiffers + " of them", wrongDiffers > 0);
        }

        // control: the complete symmetric digraph is not oriented and has no good vertex
        for (int n = 2; n <= 6; n++) {
            int[] out = new int[n];
            for (int v = 0; v < n; v++) out[v] = ((1 << n) - 1) & ~(1 << v);
            check("control: complete symmetric digraph on " + n + " vertices (2-cycles allowed) has NO good vertex",
                !hasGoodVertex(out));
        }

        System.out.println(failures == 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED");
        if (failures != 0) System.exit(1);
    }
}
