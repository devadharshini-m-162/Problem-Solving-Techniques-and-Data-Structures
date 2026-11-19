

import random
import time
from bisect import bisect_right


def linear_search(records, patient_id):
    for record in records:
        if record["patientId"] == patient_id:
            return record
    return None


def binary_search(records_by_id, patient_id):
    low, high = 0, len(records_by_id) - 1
    while low <= high:
        middle = (low + high) // 2
        current_id = records_by_id[middle]["patientId"]
        if current_id == patient_id:
            return records_by_id[middle]
        if current_id < patient_id:
            low = middle + 1
        else:
            high = middle - 1
    return None


def selection_sort_appointments(records):
    result = list(records)
    swaps = 0
    comparisons = 0
    for start in range(len(result) - 1):
        minimum = start
        for index in range(start + 1, len(result)):
            comparisons += 1
            if (result[index]["urgency"], result[index]["arrivalTime"]) < (
                result[minimum]["urgency"], result[minimum]["arrivalTime"]
            ):
                minimum = index
        if minimum != start:
            result[start], result[minimum] = result[minimum], result[start]
            swaps += 1
    return result, comparisons, swaps


def quick_sort_appointments(records):
    result = list(records)
    comparisons = 0
    swaps = 0

    def key(record):
        return record["urgency"], record["arrivalTime"]

    def sort(low, high):
        nonlocal comparisons, swaps
        if low >= high:
            return
        pivot = key(result[high])
        boundary = low
        for index in range(low, high):
            comparisons += 1
            if key(result[index]) <= pivot:
                if boundary != index:
                    result[boundary], result[index] = result[index], result[boundary]
                    swaps += 1
                boundary += 1
        if boundary != high:
            result[boundary], result[high] = result[high], result[boundary]
            swaps += 1
        sort(low, boundary - 1)
        sort(boundary + 1, high)

    sort(0, len(result) - 1)
    return result, comparisons, swaps


def find_double_bookings(appointments):
    seen = set()
    duplicates = []
    for appointment in appointments:
        key = appointment["patientId"], appointment["slot"]
        if key in seen:
            duplicates.append(key)
        else:
            seen.add(key)
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


def maximum_non_overlapping_dp(appointments):
    ordered = sorted(appointments, key=lambda item: item["end"])
    ends = [appointment["end"] for appointment in ordered]
    best = [0] * (len(ordered) + 1)
    predecessor_counts = [0] * (len(ordered) + 1)
    for count, appointment in enumerate(ordered, start=1):
        compatible_count = bisect_right(ends, appointment["start"], 0, count - 1)
        predecessor_counts[count] = compatible_count
        best[count] = max(best[count - 1], 1 + best[compatible_count])

    selected = []
    index = len(ordered)
    while index:
        compatible_count = predecessor_counts[index]
        if 1 + best[compatible_count] > best[index - 1]:
            selected.append(ordered[index - 1])
            index = compatible_count
        else:
            index -= 1
    selected.reverse()
    return selected


def greedy_shortest_duration(appointments):
    selected = []
    for appointment in sorted(
        appointments, key=lambda item: (item["end"] - item["start"], item["start"])
    ):
        if not selected or appointment["start"] >= selected[-1]["end"]:
            selected.append(appointment)
    return selected


def main():
    patients = [{"patientId": f"P{index:05d}", "name": f"Patient {index}"} for index in range(20_000)]
    patients_by_id = sorted(patients, key=lambda patient: patient["patientId"])
    rng = random.Random(23)
    targets = [patients[rng.randrange(len(patients))]["patientId"] for _ in range(1_000)]
    start = time.perf_counter()
    for target in targets:
        linear_search(patients, target)
    linear_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    for target in targets:
        binary_search(patients_by_id, target)
    binary_ms = (time.perf_counter() - start) * 1_000
    print(f"1,000 lookups in 20,000 patient records: linear={linear_ms:.2f} ms, "
          f"binary={binary_ms:.2f} ms")

    appointments = [
        {"appointmentId": f"A{index:04d}", "urgency": rng.randint(1, 5),
         "arrivalTime": rng.randrange(480, 1_080)}
        for index in range(500)
    ]
    start = time.perf_counter()
    selection_result, selection_comparisons, selection_swaps = selection_sort_appointments(appointments)
    selection_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    quick_result, quick_comparisons, quick_swaps = quick_sort_appointments(appointments)
    quick_ms = (time.perf_counter() - start) * 1_000
    key = lambda item: (item["urgency"], item["arrivalTime"])
    print(f"Appointment sorting (500 records; urgency ascending, arrival ascending):")
    print(f"  Selection: {selection_ms:.2f} ms, comparisons={selection_comparisons}, swaps={selection_swaps}")
    print(f"  Quick sort: {quick_ms:.2f} ms, comparisons={quick_comparisons}, swaps={quick_swaps}")
    print(f"  Same ordering: {[key(item) for item in selection_result] == [key(item) for item in quick_result]}")
    print(f"  First 5 appointments: "
          f"{[(item['appointmentId'], item['urgency'], item['arrivalTime']) for item in quick_result[:5]]}")

    roster = [
        {"patientId": "P001", "slot": "09:00"},
        {"patientId": "P002", "slot": "09:00"},
        {"patientId": "P001", "slot": "09:00"},
    ]
    print(f"Double-booked patient slots: {find_double_bookings(roster)}")

    walk_ins = Queue()
    walk_ins.enqueue("token-1")
    walk_ins.enqueue("token-2")
    viewed = Stack()
    viewed.push("patient-P010")
    viewed.push("patient-P020")
    print(f"Walk-in FIFO: {walk_ins.dequeue()}, then {walk_ins.dequeue()}")
    print(f"Most recently viewed patient: {viewed.pop()}")

    shift_appointments = [
        {"id": "A", "start": 0, "end": 5},
        {"id": "B", "start": 5, "end": 10},
        {"id": "S", "start": 4, "end": 6},
        {"id": "C", "start": 10, "end": 12},
        {"id": "D", "start": 12, "end": 15},
    ]
    optimal = maximum_non_overlapping_dp(shift_appointments)
    greedy = greedy_shortest_duration(shift_appointments)
    print(f"DP maximum appointment count: {len(optimal)}; schedule={[item['id'] for item in optimal]}")
    print(f"Shortest-duration greedy count: {len(greedy)}; schedule={[item['id'] for item in greedy]}")


if __name__ == "__main__":
    main()
