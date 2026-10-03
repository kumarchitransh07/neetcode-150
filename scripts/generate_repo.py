#!/usr/bin/env python3
"""
generate_repo.py — scaffolds a NeetCode 150 practice repo.

Usage:
    python3 generate_repo.py [output_dir]

Safe to re-run: existing solution files are never overwritten.
Only README.md and config files are regenerated.
"""

import os
import re
import sys

PROBLEMS = [
    ("Arrays & Hashing", [
        "Contains Duplicate",
        "Valid Anagram",
        "Two Sum",
        "Group Anagrams",
        "Top K Frequent Elements",
        "Encode and Decode Strings",
        "Product of Array Except Self",
        "Valid Sudoku",
        "Longest Consecutive Sequence",
    ]),
    ("Two Pointers", [
        "Valid Palindrome",
        "Two Sum II Input Array Is Sorted",
        "3Sum",
        "Container With Most Water",
        "Trapping Rain Water",
    ]),
    ("Sliding Window", [
        "Best Time to Buy And Sell Stock",
        "Longest Substring Without Repeating Characters",
        "Longest Repeating Character Replacement",
        "Permutation In String",
        "Minimum Window Substring",
        "Sliding Window Maximum",
    ]),
    ("Stack", [
        "Valid Parentheses",
        "Min Stack",
        "Evaluate Reverse Polish Notation",
        "Generate Parentheses",
        "Daily Temperatures",
        "Car Fleet",
        "Largest Rectangle In Histogram",
    ]),
    ("Binary Search", [
        "Binary Search",
        "Search a 2D Matrix",
        "Koko Eating Bananas",
        "Find Minimum In Rotated Sorted Array",
        "Search In Rotated Sorted Array",
        "Time Based Key Value Store",
        "Median of Two Sorted Arrays",
    ]),
    ("Linked List", [
        "Reverse Linked List",
        "Merge Two Sorted Lists",
        "Reorder List",
        "Remove Nth Node From End of List",
        "Copy List With Random Pointer",
        "Add Two Numbers",
        "Linked List Cycle",
        "Find The Duplicate Number",
        "LRU Cache",
        "Merge K Sorted Lists",
        "Reverse Nodes In K Group",
    ]),
    ("Trees", [
        "Invert Binary Tree",
        "Maximum Depth of Binary Tree",
        "Diameter of Binary Tree",
        "Balanced Binary Tree",
        "Same Tree",
        "Subtree of Another Tree",
        "Lowest Common Ancestor of a Binary Search Tree",
        "Binary Tree Level Order Traversal",
        "Binary Tree Right Side View",
        "Count Good Nodes In Binary Tree",
        "Validate Binary Search Tree",
        "Kth Smallest Element In a Bst",
        "Construct Binary Tree From Preorder And Inorder Traversal",
        "Binary Tree Maximum Path Sum",
        "Serialize And Deserialize Binary Tree",
    ]),
    ("Tries", [
        "Implement Trie Prefix Tree",
        "Design Add And Search Words Data Structure",
        "Word Search II",
    ]),
    ("Heap / Priority Queue", [
        "Kth Largest Element In a Stream",
        "Last Stone Weight",
        "K Closest Points to Origin",
        "Kth Largest Element In An Array",
        "Task Scheduler",
        "Design Twitter",
        "Find Median From Data Stream",
    ]),
    ("Backtracking", [
        "Subsets",
        "Combination Sum",
        "Permutations",
        "Subsets II",
        "Combination Sum II",
        "Word Search",
        "Palindrome Partitioning",
        "Letter Combinations of a Phone Number",
        "N Queens",
    ]),
    ("Graphs", [
        "Number of Islands",
        "Max Area of Island",
        "Clone Graph",
        "Walls And Gates",
        "Rotting Oranges",
        "Pacific Atlantic Water Flow",
        "Surrounded Regions",
        "Course Schedule",
        "Course Schedule II",
        "Graph Valid Tree",
        "Number of Connected Components In An Undirected Graph",
        "Redundant Connection",
        "Word Ladder",
    ]),
    ("Advanced Graphs", [
        "Reconstruct Itinerary",
        "Min Cost to Connect All Points",
        "Network Delay Time",
        "Swim In Rising Water",
        "Alien Dictionary",
        "Cheapest Flights Within K Stops",
    ]),
    ("1-D Dynamic Programming", [
        "Climbing Stairs",
        "Min Cost Climbing Stairs",
        "House Robber",
        "House Robber II",
        "Longest Palindromic Substring",
        "Palindromic Substrings",
        "Decode Ways",
        "Coin Change",
        "Maximum Product Subarray",
        "Word Break",
        "Longest Increasing Subsequence",
        "Partition Equal Subset Sum",
    ]),
    ("2-D Dynamic Programming", [
        "Unique Paths",
        "Longest Common Subsequence",
        "Best Time to Buy And Sell Stock With Cooldown",
        "Coin Change II",
        "Target Sum",
        "Interleaving String",
        "Longest Increasing Path In a Matrix",
        "Distinct Subsequences",
        "Edit Distance",
        "Burst Balloons",
        "Regular Expression Matching",
    ]),
    ("Greedy", [
        "Maximum Subarray",
        "Jump Game",
        "Jump Game II",
        "Gas Station",
        "Hand of Straights",
        "Merge Triplets to Form Target Triplet",
        "Partition Labels",
        "Valid Parenthesis String",
    ]),
    ("Intervals", [
        "Insert Interval",
        "Merge Intervals",
        "Non Overlapping Intervals",
        "Meeting Rooms",
        "Meeting Rooms II",
        "Minimum Interval to Include Each Query",
    ]),
    ("Math & Geometry", [
        "Rotate Image",
        "Spiral Matrix",
        "Set Matrix Zeroes",
        "Happy Number",
        "Plus One",
        "Pow(x, n)",
        "Multiply Strings",
        "Detect Squares",
    ]),
    ("Bit Manipulation", [
        "Single Number",
        "Number of 1 Bits",
        "Counting Bits",
        "Reverse Bits",
        "Missing Number",
        "Sum of Two Integers",
        "Reverse Integer",
    ]),
]

# Problems that live behind LeetCode Premium (or aren't on LeetCode at all).
PREMIUM = {
    "Encode and Decode Strings",
    "Walls And Gates",
    "Graph Valid Tree",
    "Number of Connected Components In An Undirected Graph",
    "Alien Dictionary",
    "Meeting Rooms",
    "Meeting Rooms II",
}


def slug(text: str) -> str:
    """'Pow(x, n)' -> 'powx-n' (matches LeetCode URL style)."""
    text = text.lower().replace("(", "").replace(")", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


FOLDER_NAMES = {
    "1-D Dynamic Programming": "dp_1d",
    "2-D Dynamic Programming": "dp_2d",
    "Heap / Priority Queue": "heap_priority_queue",
}


def snake(text: str, ident: bool = False) -> str:
    """ident=True guarantees a valid Python identifier (for method names)."""
    text = re.sub(r"[^A-Za-z0-9]+", "_", text.lower()).strip("_")
    if ident and text and text[0].isdigit():
        text = "solve_" + text
    return text


SOLUTION_TEMPLATE = '''"""
{num:03d}. {title}

Pattern : {pattern}
Link    : {link}
Status  : unsolved          # unsolved | solved | needs-review
Attempts: 0
Last done:

--------------------------------------------------------------------
Problem (write it in your own words):
    TODO

Brute force:
    TODO

Key insight / optimal approach:
    TODO

Complexity:
    Time  : O(?)
    Space : O(?)

Gotchas / what tripped me up:
    TODO
--------------------------------------------------------------------
"""

from typing import List, Optional, Dict, Set, Tuple  # noqa: F401


class Solution:
    def {method}(self):
        pass


if __name__ == "__main__":
    s = Solution()
    # quick sanity checks — add your own
    # assert s.{method}(...) == ...
    print("ok")
'''


def build(root: str) -> None:
    counter = 0
    section_rows = []

    for p_idx, (pattern, titles) in enumerate(PROBLEMS, start=1):
        folder = f"{p_idx:02d}_{FOLDER_NAMES.get(pattern, snake(pattern))}"
        os.makedirs(os.path.join(root, folder), exist_ok=True)
        rows = []
        for title in titles:
            counter += 1
            fname = f"{counter:03d}_{snake(title)}.py"
            path = os.path.join(root, folder, fname)
            link = (
                "LeetCode Premium — solve on neetcode.io"
                if title in PREMIUM
                else f"https://leetcode.com/problems/{slug(title)}/"
            )
            if not os.path.exists(path):  # never clobber your work
                with open(path, "w") as f:
                    f.write(
                        SOLUTION_TEMPLATE.format(
                            num=counter,
                            title=title,
                            pattern=pattern,
                            link=link,
                            method=snake(title, ident=True),
                        )
                    )
            rows.append((counter, title, f"{folder}/{fname}"))
        section_rows.append((pattern, folder, rows))

    write_readme(root, section_rows, counter)
    write_configs(root)


def write_readme(root, section_rows, total):
    lines = [
        "# NeetCode 150",
        "",
        f"My solutions to the [NeetCode 150](https://neetcode.io/practice) list — "
        f"{total} problems, grouped by pattern.",
        "",
        "Each file carries the problem link, my approach notes, complexity, and the mistakes I made.",
        "Tick the box when a problem is solved *and* the notes in the file are filled in.",
        "",
        "```bash",
        "python3 scripts/status.py     # progress report",
        "```",
        "",
        "---",
        "",
    ]
    for pattern, folder, rows in section_rows:
        lines.append(f"### {pattern} ({len(rows)})")
        lines.append("")
        for num, title, rel in rows:
            lines.append(f"- [ ] {num:03d}. [{title}]({rel})")
        lines.append("")

    with open(os.path.join(root, "README.md"), "w") as f:
        f.write("\n".join(lines))


GITIGNORE = """# Python
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# macOS
.DS_Store

# VS Code (keep shared settings, ignore local junk)
.vscode/*.log
"""

VSCODE_SETTINGS = """{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "explorer.sortOrder": "default",
  "search.exclude": {
    "**/__pycache__": true
  }
}
"""

VSCODE_EXTENSIONS = """{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "yzhang.markdown-all-in-one",
    "eamodio.gitlens"
  ]
}
"""

SNIPPETS = r"""{
  "Problem notes header": {
    "prefix": "nc",
    "body": [
      "\"\"\"",
      "${1:000}. ${2:Title}",
      "",
      "Pattern : ${3:Arrays & Hashing}",
      "Link    : ${4:url}",
      "Status  : solved",
      "",
      "Approach:",
      "    $5",
      "",
      "Complexity:",
      "    Time  : O($6)",
      "    Space : O($7)",
      "\"\"\""
    ],
    "description": "NeetCode problem header"
  },
  "Test main block": {
    "prefix": "main",
    "body": [
      "if __name__ == \"__main__\":",
      "    s = Solution()",
      "    assert s.${1:method}($2) == $3",
      "    print(\"ok\")"
    ]
  }
}
"""

STATUS_SCRIPT = '''#!/usr/bin/env python3
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
        m = re.search(r"Status\\s*:\\s*(\\S+)", text)
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
print(f"\\nTOTAL: {solved}/{total} solved ({pct:.1f}%), {review} flagged for review")
'''


def write_configs(root):
    os.makedirs(os.path.join(root, ".vscode"), exist_ok=True)
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)

    files = {
        ".gitignore": GITIGNORE,
        ".vscode/settings.json": VSCODE_SETTINGS,
        ".vscode/extensions.json": VSCODE_EXTENSIONS,
        ".vscode/neetcode.code-snippets": SNIPPETS,
        "scripts/status.py": STATUS_SCRIPT,
    }
    for rel, content in files.items():
        with open(os.path.join(root, rel), "w") as f:
            f.write(content)
    os.chmod(os.path.join(root, "scripts", "status.py"), 0o755)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "neetcode-150"
    build(out)
    print(f"Scaffolded into ./{out}")
