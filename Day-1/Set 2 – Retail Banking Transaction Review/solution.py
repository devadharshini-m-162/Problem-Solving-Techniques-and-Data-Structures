import random
import time
from bisect import bisect_right
from collections import deque
from datetime import datetime, timedelta


def binary_search_count(values, target):
    low, high = 0, len(values) - 1
    comparisons = 0
    while low <= high:
        middle = (low + high) // 2
        comparisons += 1
        if values[middle] == target:
            return middle, comparisons
        comparisons += 1
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1, comparisons


def insertion_sort(records, key):
    result = list(records)
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and key(result[position]) > key(current):
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(records, key):
    if len(records) < 2:
        return list(records)
    middle = len(records) // 2
    left = merge_sort(records[:middle], key)
    right = merge_sort(records[middle:], key)
    merged = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) <= key(right[right_index]):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def find_duplicate_postings(transactions):
    ordered = sorted(transactions, key=lambda item: item["postedAt"])
    latest_by_key = {}
    duplicates = []
    for transaction in ordered:
        key = (transaction["account"], transaction["amount"], transaction["merchant"])
        previous = latest_by_key.get(key)
        if previous is not None and transaction["postedAt"] - previous["postedAt"] <= timedelta(seconds=60):
            duplicates.append((previous["transactionId"], transaction["transactionId"]))
        latest_by_key[key] = transaction
    return duplicates


class _Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self._head = None
        self._tail = None

    def enqueue(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        return value


class Stack:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()


def divide_and_conquer_min_max(values):
    if not values:
        raise ValueError("values must not be empty")

    def solve(low, high):
        if low == high:
            return values[low], values[low], 0
        middle = (low + high) // 2
        left_min, left_max, left_comparisons = solve(low, middle)
        right_min, right_max, right_comparisons = solve(middle + 1, high)
        return (
            min(left_min, right_min),
            max(left_max, right_max),
            left_comparisons + right_comparisons + 2,
        )

    return solve(0, len(values) - 1)


def brute_force_min_max(values):
    if not values:
        raise ValueError("values must not be empty")
    minimum = maximum = values[0]
    comparisons = 0
    for value in values[1:]:
        comparisons += 1
        if value < minimum:
            minimum = value
        comparisons += 1
        if value > maximum:
            maximum = value
    return minimum, maximum, comparisons


def main():
    transaction_ids = list(range(100_000))
    _, best = binary_search_count(transaction_ids, transaction_ids[(len(transaction_ids) - 1) // 2])
    successful_counts = [
        binary_search_count(transaction_ids, value)[1]
        for value in transaction_ids
    ]
    average = sum(successful_counts) / len(successful_counts)
    worst = max(
        max(successful_counts),
        binary_search_count(transaction_ids, -1)[1],
        binary_search_count(transaction_ids, len(transaction_ids))[1],
    )
    print("Search comparisons for 100,000 sorted IDs:")
    print(f"  Binary search: best={best}, average successful={average:.2f}, worst including misses={worst}")
    print("  Linear search: best=1, average successful=50000.50, worst=100000")

    stamp = datetime(2026, 11, 18, 10, 0)
    statement = [
        {"id": "T1", "postedAt": stamp, "amount": 25.00},
        {"id": "T2", "postedAt": stamp + timedelta(minutes=1), "amount": -4.00},
        {"id": "T3", "postedAt": stamp, "amount": -10.00},
        {"id": "T4", "postedAt": stamp + timedelta(minutes=2), "amount": 70.00},
        {"id": "T5", "postedAt": stamp + timedelta(minutes=1), "amount": -2.50},
    ]
    key = lambda item: item["postedAt"]
    insertion_result = insertion_sort(statement, key)
    merge_result = merge_sort(statement, key)
    ids_by_time = lambda records: [(item["postedAt"].strftime("%H:%M"), item["id"]) for item in records]
    stable = all(
        [item["id"] for item in records if item["postedAt"] == stamp]
        == ["T1", "T3"]
        for records in (insertion_result, merge_result)
    )
    print(f"Statement by posting time (insertion): {ids_by_time(insertion_result)}")
    print(f"Statement by posting time (merge): {ids_by_time(merge_result)}")
    print(f"Stable for equal timestamps (original T1 before T3): {stable}")

    duplicate_transactions = [
        {"transactionId": "P1", "account": "A10", "amount": 19.95, "merchant": "Cafe",
         "postedAt": stamp},
        {"transactionId": "P2", "account": "A10", "amount": 19.95, "merchant": "Cafe",
         "postedAt": stamp + timedelta(seconds=45)},
        {"transactionId": "P3", "account": "A10", "amount": 19.95, "merchant": "Cafe",
         "postedAt": stamp + timedelta(seconds=90)},
        {"transactionId": "P4", "account": "A11", "amount": 19.95, "merchant": "Cafe",
         "postedAt": stamp + timedelta(seconds=50)},
    ]
    print(f"Duplicate postings within 60 seconds: {find_duplicate_postings(duplicate_transactions)}")

    review_queue = Queue()
    review_queue.enqueue("case-101")
    review_queue.enqueue("case-102")
    adjustment_stack = Stack()
    adjustment_stack.push("adjustment-1")
    adjustment_stack.push("adjustment-2")
    print(f"Manual-review FIFO: {review_queue.dequeue()}, then {review_queue.dequeue()}")
    print(f"Reverse last adjustment: {adjustment_stack.pop()}")
    builtin_queue = deque(["case-101", "case-102"])
    builtin_stack = ["adjustment-1", "adjustment-2"]
    print(f"Built-in equivalents: queue={builtin_queue.popleft()}, stack={builtin_stack.pop()}")

    rng = random.Random(19)
    amounts = [rng.randrange(-5_000, 50_000) / 100 for _ in range(10_000)]
    start = time.perf_counter()
    divide_result = divide_and_conquer_min_max(amounts)
    divide_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    brute_result = brute_force_min_max(amounts)
    brute_ms = (time.perf_counter() - start) * 1_000
    print(f"10,000 amounts: divide-and-conquer min/max={divide_result[:2]}, "
          f"comparisons={divide_result[2]}, time={divide_ms:.2f} ms")
    print(f"10,000 amounts: brute-force min/max={brute_result[:2]}, "
          f"comparisons={brute_result[2]}, time={brute_ms:.2f} ms")


if __name__ == "__main__":
    main()
