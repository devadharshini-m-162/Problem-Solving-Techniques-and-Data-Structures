# Problem Solving Techniques and Data Structures

[![Language](https://img.shields.io/badge/language-Python-blue)](https://www.python.org/)
[![Topics](https://img.shields.io/badge/topics-Algorithms%20%26%20Data%20Structures-green)](https://github.com/devadharshini-m-162/Problem-Solving-Techniques-and-Data-Structures)

A practical set of Python exercises covering algorithm basics, core data structures, searching, sorting, hashing, greedy methods, divide-and-conquer, dynamic programming, and problem-solving techniques.

Repository: https://github.com/devadharshini-m-162/Problem-Solving-Techniques-and-Data-Structures

## Overview

The repository is organized by training day and business scenario. Each exercise is implemented as a standalone Python solution and includes sample data or deterministic test input, console output, and a complexity note.

## Repository Structure

```text
Problem-Solving-Techniques-and-Data-Structures/
├── README.md
└── Day-1/
    ├── Set 1 – Retail Order Desk/
    │   └── solution.py
    ├── Set 2 – Retail Banking Transaction Review/
    │   └── solution.py
    └── Set 3 – Hospital Appointment Desk/
        └── solution.py
├── Day-2/
    ├── Set 1 – E-Commerce Catalogue and Traffic Analysis/
    ├── Set 2 – Insurance Claims Processing/
    └── Set 3 – Logistics Network and Delivery Windows/
```

## Day 1 – Problem Solving Techniques and Data Structures – I

**Topics covered:** Algorithm Basics, Data Structures Basics, Sorting Techniques, Searching Techniques, Hands-on Problem Solving

| Set | Business scenario | Key implementations |
|---|---|---|
| [Set 1 – Retail Order Desk](./Day-1/Set%201%20%E2%80%93%20Retail%20Order%20Desk/) | Online order lookup, ranking, duplicate detection, dispatch, and refunds | Linear and binary search, insertion and merge sort, hash-based duplicate detection, stack, queue, greedy and dynamic programming |
| [Set 2 – Retail Banking Transaction Review](./Day-1/Set%202%20%E2%80%93%20Retail%20Banking%20Transaction%20Review/) | Transaction lookup, statement ordering, duplicate postings, backlog review, and extrema finding | Binary and linear search, insertion and merge sort, hash-based duplicate detection, queue, stack, divide-and-conquer |
| [Set 3 – Hospital Appointment Desk](./Day-1/Set%203%20%E2%80%93%20Hospital%20Appointment%20Desk/) | Patient lookup, appointment ranking, slot validation, token handling, and scheduling | Linear and binary search, selection and quick sort, hash set, queue, stack, dynamic programming |

## Day 2 – Problem Solving Techniques and Data Structures – II

**Topics covered:** Trees, Hashing and HashMaps, Graphs, Two-Pointer and Sliding Window patterns, Hands-on Problem Solving

| Set | Business scenario | Key implementations |
|---|---|---|
| [Set 1 – E-Commerce Catalogue and Traffic Analysis](./Day-2/Set%201%20%E2%80%93%20E-Commerce%20Catalogue%20and%20Traffic%20Analysis/) | Category browsing, SKU lookup, service deployment, traffic peaks, and gift-card matching | BST traversals and search, hash table chaining, hash map, BFS/DFS graph traversal, cycle detection, sliding window, two pointers |
| [Set 2 – Insurance Claims Processing](./Day-2/Set%202%20%E2%80%93%20Insurance%20Claims%20Processing/) | Claim routing, duplicate detection, approval stages, claim spikes, and regional merge | BST, normalized hashing, BFS shortest path, DFS cycle detection, sliding window, two-pointer merge |
| [Set 3 – Logistics Network and Delivery Windows](./Day-2/Set%203%20%E2%80%93%20Logistics%20Network%20and%20Delivery%20Windows/) | Hub storage, parcel tracking, delivery routing, delivery windows, and route validation | BST height/search, hash map duplicate scans, adjacency-list BFS/DFS, sliding window, two-pointer palindrome check |

### Day 2 Decision Table

| Problem | Structure or pattern used | Reason |
|---|---|---|
| Category and claim or hub lookup | Binary Search Tree | Organizes ordered keys; supports search and sorted inorder traversal |
| Category traversal | Recursive inorder, preorder, and postorder traversal | Visits nodes in the required recursive orders |
| SKU lookup and duplicate scans | Hash table chaining or hash map | Average O(1) key lookup and efficient duplicate-key detection |
| Duplicate claims | Normalized tuple key in a hash map | Letter case and whitespace normalize before the hash key is created |
| Deployment dependencies | Directed graph | Models prerequisite and approval relationships |
| Deployment order | BFS/Kahn-style topological traversal | Repeatedly exposes nodes with no remaining dependencies |
| Approval shortest path | BFS | Finds a minimum-hop path in an unweighted directed graph |
| Circular dependencies or approval loops | DFS with visiting/visited states | Detects a back edge and reconstructs the loop |
| Busiest traffic or parcel window | Sliding window | Reuses and removes window values instead of recalculating every window |
| Gift-card and route pairing | Two pointers | Exploits sorted values or mirrored code positions |
| Merge regional claim lists | Two pointers | Merges two sorted lists in one linear pass |

## Requirements

- Python 3.10 or newer
- No third-party Python packages are required

## How to Run

Run any solution from its set folder:

```bash
cd "Day-1/Set 1 – Retail Order Desk"
python solution.py

cd "../Set 2 – Retail Banking Transaction Review"
python solution.py

cd "../Set 3 – Hospital Appointment Desk"
python solution.py

cd "../../../Day-2/Set 1 – E-Commerce Catalogue and Traffic Analysis"
python solution.py

cd "../Set 2 – Insurance Claims Processing"
python solution.py

cd "../Set 3 – Logistics Network and Delivery Windows"
python solution.py
```

On Windows, the same scripts can be run from a terminal with:

```powershell
py solution.py
```

The scripts print search, sorting, duplicate-detection, stack/queue, and optimization results to the console. Timing values vary according to the machine.

## Deliverables

For the current deliverables:

- A working Python implementation
- Sample input, generated test data, or a CSV data file where required
- Captured console output where required
- Supporting CSV or text documents for generated test data and graph definitions
- Complexity and design decisions documented in this common repository README

## Core Complexity Summary

| Technique / structure | Typical best case | Typical average case | Typical worst case | Common extra space |
|---|---:|---:|---:|---:|
| Linear search | O(1) | O(n) | O(n) | O(1) |
| Binary search | O(1) | O(log n) | O(log n) | O(1) |
| Insertion sort / selection sort | O(n) / O(n²) | O(n²) | O(n²) | O(1) |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) average |
| Hash set / hash map lookup | O(1) | O(1) | O(n) | O(n) |
| Stack / queue operations | O(1) | O(1) | O(1) amortized | O(n) |
| Divide-and-conquer extrema | O(n) | O(n) | O(n) | O(log n) recursive |
| Dynamic programming interval scheduling | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Binary search tree operations | O(log n) average | O(log n) average | O(n) | O(n) |
| BST inorder, preorder, postorder traversal | O(n) | O(n) | O(n) | O(h) |
| Chained hash table lookup | O(1) | O(1) | O(n) | O(n) |
| BFS / DFS graph traversal | O(V + E) | O(V + E) | O(V + E) | O(V) |
| Sliding window | O(n) | O(n) | O(n) | O(1) |
| Two-pointer processing / merge | O(n) | O(n) | O(n) | O(1) / O(n) merge |

## Algorithm and Data-Structure Choices

- **Linear search** is simple but requires repeated record-by-record examination.
- **Binary search** needs sorted IDs and is suitable for repeated lookups.
- **Insertion sort** is stable and efficient on small or nearly sorted statements.
- **Merge sort** provides predictable O(n log n) performance and preserves equal-key order.
- **Selection sort** makes the minimum number of element moves practical to observe, although comparisons remain quadratic.
- **Quick sort** is faster on average and illustrates divide-and-conquer partitioning.
- **Hash structures** provide fast duplicate-key detection for large record volumes.
- **Stacks** implement last-in, first-out undo behavior.
- **Queues** implement first-in, first-out review and dispatch behavior.
- **Dynamic programming** finds an optimal non-overlapping interval schedule or an optimal denomination combination.



