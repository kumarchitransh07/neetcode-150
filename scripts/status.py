#!/usr/bin/env python3
"""Print progress across the NeetCode 150 repo. Run: python3 scripts/status.py"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

total = solved = review = 0
per_pattern = {}

for folder in sorted(os.listdir(ROOT)):
    fpath = os.path.join(ROOT, folder)
    if not os.path.isdir(fpath) or not folder[0].isdigit():
        continue
    done = count = rev = 0
    for fname in sorted(os.listdir(fpath)):
        if not fname.endswith(".py"):
            continue
        count += 1
        text = open(os.path.join(fpath, fname)).read()
        m = re.search(r"Status\s*:\s*(\S+)", text)
        status = m.group(1) if m else "unsolved"
        if status == "solved":
            done += 1
        elif status == "needs-review":
            rev += 1
    per_pattern[folder] = (done, rev, count)
    total += count
    solved += done
    review += rev

width = max(len(k) for k in per_pattern)
for folder, (done, rev, count) in per_pattern.items():
    bar = "#" * done + "." * (count - done)
    flag = f"  ({rev} to review)" if rev else ""
    print(f"{folder:<{width}}  {done:>2}/{count:<2} {bar}{flag}")

pct = (solved / total * 100) if total else 0
print(f"\nTOTAL: {solved}/{total} solved ({pct:.1f}%), {review} flagged for review")
