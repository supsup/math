# Independent audit of the seven-leaf odd-block certificate

**Verdict: passes the stated edge-partition claim.** I read the cycle rows in [the certificate](p12289_t7_odd_block_certificate.md) and replayed each as the alternating closed walk specified there. [This independent replay](p12289_t7_odd_block_independent_replay.py) parses the Markdown tables and never imports [the original checker](p12289_t7_odd_block_check.py). Its run reports `PASS: K_(6,7), K_(7,7), K_(11,7); 86,023 global edges once; 17,556 parts`.

The lower bound follows directly. Every hub has degree seven, so its odd degree requires an odd, hence positive, number of incident singleton edges: `s >= p`. A simple cycle in `K_(p,7)` uses at most seven leaves and seven hubs, hence at most fourteen edges. Therefore `c >= ceil((7p-s)/14)`. The function `s + ceil((7p-s)/14)` is nondecreasing as integer `s` rises, so every partition has at least `p + ceil(3p/7)` parts. For `p=12289`, `3p=36867=7·5266+5`, giving `12289+5267=17556`.

For each listed walk I checked equal hub/leaf list lengths, no repeated hub or leaf within a walk, valid labels, and each consecutive edge including the closing edge. The resulting local counts are:

| Block | Cycle lengths | Distinct cycle edges | Complementary singletons |
|---|---|---:|---:|
| `K_(6,7)` | `12,12,12` | 36 | 6, exactly the six claimed pairs |
| `K_(7,7)` | `14,14,14` | 42 | 7, exactly `(h,h)` for `h=0,...,6` |
| `K_(11,7)` | `14,14,14,12,12` | 66 | 11, exactly the eleven claimed pairs |

No cycle edge repeats within or across rows. Every complementary set has one edge at each hub. The six-hub block is valid but is not used in the 12,289-hub construction.

Finally, `1754·7=12278`, so `1754·7+11=12289`. Translating each seven-hub block to its own hub interval, then the eleven-hub block to the last interval, gives exactly one copy of every `(hub,leaf)` edge: hubs distinguish edges even when cycles in different blocks share leaves. Sharing vertices across *different* cycles is allowed in an edge partition and does not affect simplicity of any individual cycle. The expansion has `1754·3+5=5267` cycles, `12289` singletons, and `7·12289=86023` distinct edges. I found no gap in the certificate's claimed exact value.
