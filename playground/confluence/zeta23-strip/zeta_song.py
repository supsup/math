"""Listen to the zeta function (a playful extra, not a card claim).

Plays Hardy's Z(t), the zeta function along the critical line as a real wave, as sound: t runs from 10 to
T_END in SECONDS seconds. Every zero of zeta on the line is a moment the sound crosses zero. Zeros get denser
as t grows (about log(t / 2 pi) / 2 pi of them per unit of t), so the pitch should rise; their irregular spacing
makes the tone slightly rough. Uses the same Z as zeta_wave.py, whose formulas that script checks against the
zero-counting formula.

The script also COUNTS the sign changes it played and compares them with the zero-counting formula
theta(T)/pi + 1 at the end (they should agree to within a few: the Riemann-Siegel error and S(T) are small,
but this is a loose check here, at heights the strict check in zeta_wave.py did not reach).

Writes zeta_song.wav (16-bit mono). Run: python3 zeta_song.py ; play: afplay zeta_song.wav
"""
import math
import os
import struct
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # our own zeta_wave.py, beside this file
from zeta_wave import Z, theta  # noqa: E402

RATE, SECONDS, T_START, T_END = 22050, 10, 10.0, 20000.0


def main():
    n = RATE * SECONDS
    dt = (T_END - T_START) / n
    samples, crossings, prev = [], 0, None
    for i in range(n):
        t = T_START + i * dt
        z = Z(t)
        if prev is not None and prev * z < 0:
            crossings += 1
        prev = z
        # loudness evens out: divide by the slow growth of Z's typical size, then soft-clip
        v = math.tanh(0.6 * z / math.log(t))
        fade = min(1.0, i / (0.05 * RATE), (n - 1 - i) / (0.3 * RATE))
        samples.append(int(30000 * v * fade))
    with wave.open("zeta_song.wav", "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    predicted = theta(T_END) / math.pi + 1 - (theta(T_START) / math.pi + 1)
    start_hz = math.log(T_START / (2 * math.pi)) / (2 * math.pi) * (T_END - T_START) / SECONDS / 2
    end_hz = math.log(T_END / (2 * math.pi)) / (2 * math.pi) * (T_END - T_START) / SECONDS / 2
    print(f"{SECONDS} s of sound, t from {T_START:g} to {T_END:g}; sign changes played {crossings}, "
          f"zero-counting formula predicts {predicted:.1f} ({crossings - predicted:+.1f})")
    print(f"pitch from about {start_hz:.0f} Hz to {end_hz:.0f} Hz (each zero is half a cycle)")
    assert abs(crossings - predicted) < 0.01 * predicted, "played crossings far from the count: the sound is not the zeta wave"
    print("wrote zeta_song.wav")


if __name__ == "__main__":
    main()
