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
    │   ├── solution.py
    │   ├── orders.csv
    │   ├── sample_output.txt
    ├── Set 2 – Retail Banking Transaction Review/
    │   ├── solution.py
    │   ├── sample_output.txt
    └── Set 3 – Hospital Appointment Desk/
        ├── solution.py
        ├── sample_output.txt
      
```

## Day 1 – Problem Solving Techniques and Data Structures – I

**Topics covered:** Algorithm Basics, Data Structures Basics, Sorting Techniques, Searching Techniques, Hands-on Problem Solving

| Set | Business scenario | Key implementations |
|---|---|---|
| [Set 1 – Retail Order Desk](./Day-1/Set%201%20%E2%80%93%20Retail%20Order%20Desk/) | Online order lookup, ranking, duplicate detection, dispatch, and refunds | Linear and binary search, insertion and merge sort, hash-based duplicate detection, stack, queue, greedy and dynamic programming |
| [Set 2 – Retail Banking Transaction Review](./Day-1/Set%202%20%E2%80%93%20Retail%20Banking%20Transaction%20Review/) | Transaction lookup, statement ordering, duplicate postings, backlog review, and extrema finding | Binary and linear search, insertion and merge sort, hash-based duplicate detection, queue, stack, divide-and-conquer |
| [Set 3 – Hospital Appointment Desk](./Day-1/Set%203%20%E2%80%93%20Hospital%20Appointment%20Desk/) | Patient lookup, appointment ranking, slot validation, token handling, and scheduling | Linear and binary search, selection and quick sort, hash set, queue, stack, dynamic programming |

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
```

On Windows, the same scripts can be run from a terminal with:

```powershell
py solution.py
```

The scripts print search, sorting, duplicate-detection, stack/queue, and optimization results to the console. Timing values vary according to the machine.

## Deliverables

Each set provides:

- A working Python implementation
- Sample input, generated test data, or a CSV data file where required
- Console output captured in `sample_output.txt`
- A complexity and design rationale in a set-level `README.md`

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

## Learning Outcomes

After completing this day, students should be able to:

- Compare search and sort algorithms using complexity and measured execution time.
- Explain stability and identify situations where equal-key ordering matters.
- Choose appropriate built-in or custom data structures for real workflows.
- Use hashing to detect duplicates efficiently.
- Apply divide-and-conquer, greedy, and dynamic-programming approaches.
- Explain the trade-offs between time complexity, space complexity, and implementation complexity.

