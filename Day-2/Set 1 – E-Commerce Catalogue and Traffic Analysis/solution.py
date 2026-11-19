
import csv
import time
from collections import deque
from pathlib import Path


class CategoryNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.height_value = 0

    def insert(self, value):
        if self.root is None:
            self.root = CategoryNode(value)
            return
        node = self.root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = CategoryNode(value)
                    return
                node = node.left
            elif value > node.value:
                if node.right is None:
                    node.right = CategoryNode(value)
                    return
                node = node.right
            else:
                return

    def search(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self):
        return self._walk("in")

    def preorder(self):
        return self._walk("pre")

    def postorder(self):
        return self._walk("post")

    def _walk(self, order):
        result = []

        def visit(node):
            if node is None:
                return
            if order == "pre":
                result.append(node.value)
            visit(node.left)
            if order == "in":
                result.append(node.value)
            visit(node.right)
            if order == "post":
                result.append(node.value)

        visit(self.root)
        return result


class ChainedHashTable:
    def __init__(self, size=101):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    @staticmethod
    def _text_hash(key):
        value = 0
        for character in key:
            value = (value * 31 + ord(character)) % (2**32)
        return value

    def put(self, key, value):
        bucket = self._bucket(key)
        for index, (stored_key, _) in enumerate(self.buckets[bucket]):
            if stored_key == key:
                self.buckets[bucket][index] = (key, value)
                return
        self.buckets[bucket].append((key, value))

    def get(self, key):
        bucket = self._bucket(key)
        for stored_key, value in self.buckets[bucket]:
            if stored_key == key:
                return value
        return None

    def _bucket(self, key):
        return self._text_hash(str(key)) % self.size


def deployment_bfs(graph, start):
    indegree = {node: 0 for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            indegree[neighbor] += 1
    queue = deque([node for node, degree in indegree.items() if degree == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(graph):
        return None
    return order


def deployment_dfs_cycle(graph):
    state = {node: 0 for node in graph}
    stack = []

    def visit(node):
        state[node] = 1
        stack.append(node)
        for neighbor in graph[node]:
            if state[neighbor] == 1:
                cycle_start = stack.index(neighbor)
                return stack[cycle_start:] + [neighbor]
            if state[neighbor] == 0:
                cycle = visit(neighbor)
                if cycle:
                    return cycle
        stack.pop()
        state[node] = 2
        return None

    for node in graph:
        if state[node] == 0:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def busiest_three_hour_window(requests):
    if len(requests) < 3:
        return None
    window = sum(requests[:3])
    maximum = window
    start = 0
    for index in range(3, len(requests)):
        window += requests[index] - requests[index - 3]
        if window > maximum:
            maximum = window
            start = index - 2
    return start, start + 2, maximum


def gift_card_pairs(values, target):
    left, right = 0, len(values) - 1
    pairs = []
    while left < right:
        total = values[left] + values[right]
        if total == target:
            pairs.append((values[left], values[right]))
            left += 1
            right -= 1
        elif total < target:
            left += 1
        else:
            right -= 1
    return pairs


def load_requests(path):
    with path.open(newline="", encoding="utf-8") as file:
        return [int(row["requests"]) for row in csv.DictReader(file)]


def main():
    categories = [
        "Phones", "Laptops", "Audio", "Cameras", "Wearables",
        "Gaming", "Books", "Fashion", "Beauty", "Furniture",
        "Appliances", "Sports", "Toys", "Grocery", "Garden",
    ]
    tree = BinarySearchTree()
    for category in categories:
        tree.insert(category)
    print("BST traversals:")
    print(f"  Inorder: {tree.inorder()}")
    print(f"  Preorder: {tree.preorder()}")
    print(f"  Postorder: {tree.postorder()}")
    print(f"  Search 'Gaming': {tree.search('Gaming')}; search 'Travel': {tree.search('Travel')}")

    custom_table = ChainedHashTable(size=3)
    custom_table.put("A1", "Laptop")
    custom_table.put("D4", "Camera")
    print("Hash collision demonstration:")
    print(f"  A1 and D4 bucket: {custom_table._bucket('A1')} "
          f"(size=3), lookups={custom_table.get('A1')}, {custom_table.get('D4')}")

    skus = {f"SKU{index:06d}": index for index in range(100_000)}
    chained = ChainedHashTable(size=100_003)
    start = time.perf_counter()
    for key, value in skus.items():
        chained.put(key, value)
    custom_build_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    for index in range(100_000):
        chained.get(f"SKU{index:06d}")
    custom_lookup_ms = (time.perf_counter() - start) * 1_000
    start = time.perf_counter()
    for index in range(100_000):
        skus[f"SKU{index:06d}"]
    built_in_lookup_ms = (time.perf_counter() - start) * 1_000
    print("100,000-SKU lookup benchmark:")
    print(f"  Custom chain build={custom_build_ms:.2f} ms, lookup={custom_lookup_ms:.2f} ms")
    print(f"  Built-in dict lookup={built_in_lookup_ms:.2f} ms")

    deployment_graph = {
        "cart": ["pricing", "inventory"],
        "pricing": ["database"],
        "inventory": ["database"],
        "database": [],
        "gateway": ["cart"],
    }
    print(f"Deployment order (BFS/Kahn): {deployment_bfs(deployment_graph, 'gateway')}")
    print(f"Cycle detected (DFS): {deployment_dfs_cycle(deployment_graph)}")

    requests = load_requests(Path(__file__).with_name("requests_per_hour.csv"))
    result = busiest_three_hour_window(requests)
    print(f"24-hour busiest 3-hour window: hours {result[0]}-{result[1]}, "
          f"requests={result[2]}")

    order_values = [120, 280, 450, 550, 730, 880]
    print(f"Gift-card pairs total 1000: {gift_card_pairs(order_values, 1000)}")


if __name__ == "__main__":
    main()
