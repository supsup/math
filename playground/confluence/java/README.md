# Java examples (Confluence's math playground)

Charles: "in your playground could you try to make java examples of them as you review" and "please keep
all java examples in their own folder/package". So every Java example lives here, one package per
reviewed result, under `confluence.math.<topic>`.

| Package | Class | What it does |
|---|---|---|
| `confluence.math.truffet` | `Truffet` | Replicates the 13-conjunct Lean theorem that Truffet's tropical LP algorithm is forced to a non-optimal answer |
| `confluence.math.permanent` | `FourRowPermanent` | Searches perm(F)/24 / prod row norms; finds the exponent floor 4 ln4/ln24 via permutation matrices |
| `confluence.math.sidorenko` | `SidorenkoPattern` | Checks the Sidorenko counterexample's pattern graph H from its table; exact t(H,W)/(EW)^66 for tiny kernels |

Build and run (JDK 25; plain javac, no build tool):

```sh
cd java
javac -d out $(find src -name "*.java")
java -cp out confluence.math.truffet.Truffet
java -cp out confluence.math.sidorenko.SidorenkoPattern
java -cp out confluence.math.permanent.FourRowPermanent
```

Every example prints its own negative controls, so a pass can be told apart from a check that cannot fail.
`out/` is build output.

Each class Javadoc (markdown `///`) ends with a "What this could mean for Java code" section (Charles asked for one): concrete consequences for Java programs and tests, labelled as possible uses I can defend, not claims from the paper.
