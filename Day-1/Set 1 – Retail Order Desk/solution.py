import csv
import random
import time
from collections import deque
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def load_orders(path):
    with path.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))
    for row in rows:
        row["amount"] = Decimal(row["amount"])
        row["createdAt"] = datetime.fromisoformat(row["createdAt"])
    return rows


def linear_search(orders, order_id):
    for order in orders:
        if order["orderId"] == order_id:
            return order
    return None


def binary_search(orders_by_id, order_id):
    low, high = 0, len(orders_by_id) - 1
    while low <= high:
        middle = (low + high) // 2
        current_id = orders_by_id[middle]["orderId"]
        if current_id == order_id:
            return orders_by_id[middle]
        if current_id < order_id:
            low = middle + 1
        else:
            high = middle - 1
    return None


def insertion_sort(values, key):
    result = list(values)
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and key(result[position]) < key(current):
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(values, key):
    if len(values) < 2:
        return list(values)
    middle = len(values) // 2
    left = merge_sort(values[:middle], key)
    right = merge_sort(values[middle:], key)
    merged = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) >= key(right[right_index]):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def trace_insertion_sort(values):
    result = list(values)
    trace = []
    for index in range(1, min(4, len(result))):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] < current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
        trace.append(list(result))
    return trace


def find_duplicate_orders(orders):
    buckets = {}
    duplicates = []
    for order in orders:
        minute = order["createdAt"].replace(second=0, microsecond=0)
        key = (order["customerId"], order["amount"], minute)
        if key in buckets:
            duplicates.append((buckets[key], order["orderId"]))
        else:
            buckets[key] = order["orderId"]
    return duplicates


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()


class _QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self._head = None
        self._tail = None

    def enqueue(self, item):
        node = _QueueNode(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        item = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        return item


def refund_greedy(amount, denominations):
    notes = []
    remainder = amount
    for denomination in sorted(denominations, reverse=True):
        count, remainder = divmod(remainder, denomination)
        notes.extend([denomination] * count)
    if remainder:
        raise ValueError("amount cannot be represented by these denominations")
    return notes


def refund_dynamic_programming(amount, denominations):
    best = [0] + [float("inf")] * amount
    previous_coin = [None] * (amount + 1)
    for value in range(1, amount + 1):
        for coin in denominations:
            if coin <= value and best[value - coin] + 1 < best[value]:
                best[value] = best[value - coin] + 1
                previous_coin[value] = coin
    if best[amount] == float("inf"):
        raise ValueError("amount cannot be represented by these denominations")
    coins = []
    remainder = amount
    while remainder:
        coin = previous_coin[remainder]
        coins.append(coin)
        remainder -= coin
    return coins


def benchmark():
    rng = random.Random(7)
    order_count = 50_000
    orders = [
        {"orderId": f"O{index:06d}", "amount": Decimal(rng.randrange(100, 100_000)) / 100}
        for index in range(order_count)
    ]
    queries = [orders[index]["orderId"] for index in range(0, order_count, 1_000)]
    sorted_orders = sorted(orders, key=lambda order: order["orderId"])

    start = time.perf_counter()
    for query in queries:
        linear_search(orders, query)
    linear_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    for query in queries:
        binary_search(sorted_orders, query)
    binary_ms = (time.perf_counter() - start) * 1_000

    amounts = sorted(
        (rng.randrange(1, 1_000_000) for _ in range(10_000)),
        reverse=True,
    )
    for index in range(0, len(amounts) - 1, 100):
        amounts[index], amounts[index + 1] = amounts[index + 1], amounts[index]
    results = []
    for name, sorter in (
        ("insertion sort", lambda values: insertion_sort(values, key=lambda value: value)),
        ("merge sort", lambda values: merge_sort(values, key=lambda value: value)),
        ("built-in sorted", lambda values: sorted(values, reverse=True)),
    ):
        start = time.perf_counter()
        sorted_values = sorter(amounts)
        elapsed_ms = (time.perf_counter() - start) * 1_000
        results.append((name, elapsed_ms, sorted_values == sorted(amounts, reverse=True)))
    return len(queries), linear_ms, binary_ms, results


def compare_stack_and_queue():
    count = 5_000
    custom_stack = Stack()
    start = time.perf_counter()
    for value in range(count):
        custom_stack.push(value)
    for _ in range(count):
        custom_stack.pop()
    custom_stack_ms = (time.perf_counter() - start) * 1_000

    builtin_stack = []
    start = time.perf_counter()
    for value in range(count):
        builtin_stack.append(value)
    for _ in range(count):
        builtin_stack.pop()
    builtin_stack_ms = (time.perf_counter() - start) * 1_000

    custom_queue = Queue()
    start = time.perf_counter()
    for value in range(count):
        custom_queue.enqueue(value)
    for _ in range(count):
        custom_queue.dequeue()
    custom_queue_ms = (time.perf_counter() - start) * 1_000

    builtin_queue = deque()
    start = time.perf_counter()
    for value in range(count):
        builtin_queue.append(value)
    for _ in range(count):
        builtin_queue.popleft()
    builtin_queue_ms = (time.perf_counter() - start) * 1_000
    return custom_stack_ms, builtin_stack_ms, custom_queue_ms, builtin_queue_ms


def main():
    orders = load_orders(Path(__file__).with_name("orders.csv"))
    orders_by_id = sorted(orders, key=lambda order: order["orderId"])
    target_id = orders[0]["orderId"]
    print(f"Loaded {len(orders)} sample orders from orders.csv")
    print(f"Search {target_id}: linear={linear_search(orders, target_id) is not None}, "
          f"binary={binary_search(orders_by_id, target_id) is not None}")

    queries, linear_ms, binary_ms, sort_results = benchmark()
    print(f"Search benchmark (50,000 records; {queries} lookups): "
          f"linear={linear_ms:.2f} ms, binary={binary_ms:.2f} ms")
    print("Descending sort trace for [7, 3, 5, 2, 9]: "
          + " | ".join(str(pass_state) for pass_state in trace_insertion_sort([7, 3, 5, 2, 9])))
    print("Sort benchmark (10,000 near-sorted amounts; 100 adjacent swaps):")
    for name, elapsed_ms, correct in sort_results:
        print(f"  {name}: {elapsed_ms:.2f} ms; correct={correct}")
    print(f"Duplicate order pairs (same customer, amount, and minute): "
          f"{find_duplicate_orders(orders)}")

    stack_ms, builtin_stack_ms, queue_ms, builtin_queue_ms = compare_stack_and_queue()
    stack = Stack()
    stack.push("edited order")
    print(f"Undo last edit: {stack.pop()}")
    dispatch = Queue()
    dispatch.enqueue("O1001")
    dispatch.enqueue("O1002")
    print(f"Dispatch FIFO: {dispatch.dequeue()}, then {dispatch.dequeue()}")
    print(f"Stack 5,000 push/pop: custom={stack_ms:.2f} ms, list={builtin_stack_ms:.2f} ms")
    print(f"Queue 5,000 enqueue/dequeue: custom={queue_ms:.2f} ms, "
          f"deque={builtin_queue_ms:.2f} ms")

    standard = refund_greedy(93, [100, 50, 20, 10, 5, 2, 1])
    failed_greedy = refund_greedy(6, [4, 3, 1])
    optimal = refund_dynamic_programming(6, [4, 3, 1])
    print(f"Refund 93 with standard denominations: {standard} ({len(standard)} pieces)")
    print(f"Greedy failure for 6 with [4, 3, 1]: {failed_greedy} ({len(failed_greedy)} pieces)")
    print(f"Dynamic-programming solution: {optimal} ({len(optimal)} pieces)")


if __name__ == "__main__":
    main()
