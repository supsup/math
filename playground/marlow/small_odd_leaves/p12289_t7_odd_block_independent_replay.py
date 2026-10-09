"""Independently parse and replay the t=7 odd-block certificate.

Reads the Markdown tables; does not import the certificate's checker.
"""

from collections import Counter
from pathlib import Path
import re


CERTIFICATE = Path(__file__).with_name("p12289_t7_odd_block_certificate.md")


def table_rows(text, start, end):
    section = text.split(start, 1)[1].split(end, 1)[0]
    rows = []
    for line in section.splitlines():
        cells = re.findall(r"`([0-9]+(?: [0-9]+)+)`", line)
        if len(cells) == 2:
            rows.append(tuple(tuple(map(int, cell.split())) for cell in cells))
    return rows


def replay(hub_count, cycles, claimed_singletons):
    universe = {(h, l) for h in range(hub_count) for l in range(7)}
    cycle_edges = Counter()
    for hubs, leaves in cycles:
        assert len(hubs) == len(leaves) and len(hubs) >= 2
        assert len(set(hubs)) == len(hubs), "repeated hub in cycle"
        assert len(set(leaves)) == len(leaves), "repeated leaf in cycle"
        vertices = [v for pair in zip(
            (("H", h) for h in hubs), (("L", l) for l in leaves)
        ) for v in pair]
        for u, v in zip(vertices, vertices[1:] + vertices[:1]):
            assert u[0] != v[0]
            edge = (u[1], v[1]) if u[0] == "H" else (v[1], u[1])
            cycle_edges[edge] += 1
    assert set(cycle_edges) <= universe, "out-of-range edge"
    assert set(cycle_edges.values()) == {1}, "repeated cycle edge"
    singletons = universe - set(cycle_edges)
    assert singletons == claimed_singletons, "singleton complement mismatch"
    assert Counter(h for h, _ in singletons) == Counter(range(hub_count))
    return cycle_edges, singletons


def main():
    text = CERTIFICATE.read_text()
    six = table_rows(text, "An auxiliary `K_(6,7)`", "The needed `K_(11,7)`")
    eleven = table_rows(text, "The needed `K_(11,7)`", "Partition the 12,289 hubs")
    assert len(six) == 3 and len(eleven) == 5

    six_singletons = {(0, 2), (1, 1), (2, 0), (3, 2), (4, 1), (5, 0)}
    eleven_singletons = {
        (0, 5), (1, 2), (2, 5), (3, 3), (4, 1), (5, 5),
        (6, 0), (7, 6), (8, 6), (9, 6), (10, 4),
    }
    seven = [
        (tuple(-k % 7 for k in range(7)),
         tuple((-k + a) % 7 for k in range(7)))
        for a in (1, 3, 5)
    ]
    seven_edges, seven_residual = replay(7, seven, {(h, h) for h in range(7)})
    six_edges, _ = replay(6, six, six_singletons)
    eleven_edges, eleven_residual = replay(11, eleven, eleven_singletons)
    assert len(six_edges) == 36
    assert len(seven_edges) == 42
    assert len(eleven_edges) == 66
    assert [2 * len(h) for h, _ in six] == [12] * 3
    assert [2 * len(h) for h, _ in eleven] == [14] * 3 + [12] * 2

    all_edges = Counter()
    for block in range(1754):
        for (h, l), count in seven_edges.items():
            all_edges[(7 * block + h, l)] += count
        for h, l in seven_residual:
            all_edges[(7 * block + h, l)] += 1
    for (h, l), count in eleven_edges.items():
        all_edges[(1754 * 7 + h, l)] += count
    for h, l in eleven_residual:
        all_edges[(1754 * 7 + h, l)] += 1

    p = 12289
    assert 1754 * 7 + 11 == p
    assert all_edges == Counter({(h, l): 1 for h in range(p) for l in range(7)})
    assert len(all_edges) == 86023
    assert 1754 * 3 + 5 == (3 * p + 6) // 7 == 5267
    assert p + 5267 == 17556
    print("PASS: K_(6,7), K_(7,7), K_(11,7); 86,023 global edges once; 17,556 parts")


if __name__ == "__main__":
    main()
