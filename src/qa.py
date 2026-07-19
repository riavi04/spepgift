#!/usr/bin/env python3
"""Objective quality check on extracted clips, standing in for listening.

Flags clips that are mostly silence, dominated by low-frequency rumble,
or that appear to be cut off while still loud.
"""
import json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_clips import LOW_BIRDS, MAX_DUR, DEFAULT_MAX

SR = 22050


def decode(path):
    p = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1",
                        "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32) if p.stdout else None


def db(x):
    return 20 * np.log10(max(float(x), 1e-9))


def report(path):
    x = decode(path)
    if x is None or len(x) < 512:
        return None
    peak = float(np.abs(x).max())
    rms = float(np.sqrt((x.astype(np.float64) ** 2).mean()))

    win, hop = 1024, 256
    n = 1 + (len(x) - win) // hop
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    fr = x[idx].astype(np.float64)
    fr_rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-12)
    # How much of the clip is actually sounding. Compared against the loudest
    # frame, not the sample peak: a sharp transient has a very high crest
    # factor, so measuring against sample peak makes percussive calls like the
    # woodcock's look like silence when they are perfectly full.
    active = float((fr_rms > fr_rms.max() * 0.18).mean())

    # Spectral centroid: rumble and wind sit low, bird calls sit high.
    spec = np.abs(np.fft.rfft(fr * np.hanning(win), axis=1))
    freqs = np.fft.rfftfreq(win, 1 / SR)
    loud = fr_rms > fr_rms.max() * 0.3
    if loud.sum() == 0:
        loud = np.ones(len(fr_rms), bool)
    cen = float((spec[loud] * freqs).sum() / max(spec[loud].sum(), 1e-9))

    # Energy below 300 Hz relative to total, in the loud frames.
    lowmask = freqs < 300
    lowfrac = float(spec[loud][:, lowmask].sum() / max(spec[loud].sum(), 1e-9))

    # Is the clip still loud at its very end (a sign of a truncated call)?
    tail = float(fr_rms[-max(2, n // 12):].mean() / (fr_rms.max() + 1e-9))

    return {
        "peak_db": round(db(peak), 1), "rms_db": round(db(rms), 1),
        "active": round(active, 2), "centroid": int(cen),
        "low_frac": round(lowfrac, 2), "tail": round(tail, 2),
        "dur": round(len(x) / SR, 2),
    }


def main():
    d = sys.argv[1]
    man = json.load(open(os.path.join(d, "manifest.json")))
    print(f"{'clip':18s} {'dur':>5s} {'peak':>6s} {'rms':>6s} {'act':>5s} "
          f"{'cent':>6s} {'low':>5s} {'tail':>5s}  flags")
    problems = []
    for key, sp in man.items():
        for c in sp["clips"]:
            p = os.path.join(d, c["file"])
            r = report(p)
            if not r:
                problems.append((c["file"], "decode failed")); continue
            flags = []
            # Two classes of expected result are not defects: birds that
            # genuinely boom below 300 Hz, and long continuous calls trimmed
            # at the per-species duration cap.
            low_ok = key in LOW_BIRDS
            cap = MAX_DUR.get(key, DEFAULT_MAX)
            at_cap = r["dur"] >= cap - 0.15

            if r["active"] < 0.18: flags.append("mostly-silent")
            if r["rms_db"] < -30: flags.append("quiet")
            if r["low_frac"] > 0.55 and not low_ok: flags.append("rumble")
            # A short one-shot ending loud is a punchy clip, not a truncation.
            if r["tail"] > 0.55 and r["dur"] > 1.2 and not at_cap:
                flags.append("cut-off")
            if r["centroid"] < 220 and not low_ok: flags.append("very-low")
            print(f"{c['file']:18s} {r['dur']:5.2f} {r['peak_db']:6.1f} {r['rms_db']:6.1f} "
                  f"{r['active']:5.2f} {r['centroid']:6d} {r['low_frac']:5.2f} {r['tail']:5.2f}  "
                  f"{','.join(flags)}")
            if flags:
                problems.append((c["file"], ",".join(flags)))
    print(f"\n{len(problems)} flagged")
    for f, why in problems:
        print("  ", f, why)


if __name__ == "__main__":
    main()
