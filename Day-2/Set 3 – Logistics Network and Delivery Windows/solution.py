"""Day 2, Set 3: Logistics Network and Delivery Windows."""

from collections import deque


class HubNode:
    def __init__(self, code):
        self.code = code
        self.left = None
        self.right = None


class HubBST:
    def __init__(self):
        self.root = None

    def insert(self, code):
        if self.root is None:
            self.root = HubNode(code)
            return
        node = self.root
        while True:
            if code == node.code:
                return
            if code < node.code:
                if node.left is None:
                    node.left = HubNode(code)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = HubNode(code)
                    return
                node = node.right

    def search(self, code):
        node = self.root
        while node is not None:
            if code == node.code:
                return True
            node = node.left if code < node.code else node.right
        return False

    def height(self):
        def visit(node):
            if node is None:
                return 0
            return 1 + max(visit(node.left), visit(node.right))

        return visit(self.root)


def update_parcel_scans(scan_log, tracking_number, hub):
    key = (tracking_number, hub)
    if key in scan_log:
        return False
    scan_log[key] = True
    return True


def bfs_shortest_route(graph, start, target):
    queue = deque([start])
    parent = {start: None}
    while queue:
        hub = queue.popleft()
        if hub == target:
            break
        for neighbor in graph[hub]:
            if neighbor not in parent:
                parent[neighbor] = hub
                queue.append(neighbor)
    if target not in parent:
        return None
    route = []
    hub = target
    while hub is not None:
        route.append(hub)
        hub = parent[hub]
    return list(reversed(route))


def dfs_reachable(graph, start):
    visited = set()
    order = []

    def visit(hub):
        visited.add(hub)
        order.append(hub)
        for neighbor in graph[hub]:
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def highest_four_hour_average(hourly_counts):
    if len(hourly_counts) < 4:
        return None
    window_sum = sum(hourly_counts[:4])
    maximum_sum = window_sum
    start = 0
    for index in range(4, len(hourly_counts)):
        window_sum += hourly_counts[index] - hourly_counts[index - 4]
        if window_sum > maximum_sum:
            maximum_sum = window_sum
            start = index - 3
    return start, start + 3, maximum_sum / 4


def is_hub_palindrome(description):
    hubs = []
    current = []
    separators = "-/,; "
    for character in description:
        if character in separators:
            if current:
                hubs.append("".join(current).lower())
                current = []
        elif character.isalnum():
            current.append(character)
    if current:
        hubs.append("".join(current).lower())
    left, right = 0, len(hubs) - 1
    while left < right:
        if hubs[left] != hubs[right]:
            return False
        left += 1
        right -= 1
    return True


def main():
    ordered_hubs = ["H10", "H20", "H30", "H40", "H50", "H60", "H70", "H80", "H90", "H100"]
    balanced_tree = HubBST()
    for hub in ["H50", "H30", "H70", "H20", "H40", "H60", "H80", "H10", "H90"]:
        balanced_tree.insert(hub)

    sorted_tree = HubBST()
    for hub in ordered_hubs:
        sorted_tree.insert(hub)
    print("Hub BST:")
    print(f"  Search H70={balanced_tree.search('H70')}, search ZZ={balanced_tree.search('ZZ')}")
    print(f"  Balanced insertion height={balanced_tree.height()}")
    print(f"  Sorted insertion height={sorted_tree.height()} (sorted input degenerates to a chain)")

    parcel_scans = {}
    print("Parcel scan checks:")
    print(f"  First scan PKG001 at H01: {update_parcel_scans(parcel_scans, 'PKG001', 'H01')}")
    print(f"  Repeat scan PKG001 at H01: {update_parcel_scans(parcel_scans, 'PKG001', 'H01')}")
    print(f"  Scan PKG001 at H02: {update_parcel_scans(parcel_scans, 'PKG001', 'H02')}")

    graph = {
        "H01": ["H02", "H03"],
        "H02": ["H01", "H05", "H04"],
        "H03": ["H01", "H06"],
        "H04": ["H02", "H07"],
        "H05": ["H02", "H08"],
        "H06": ["H03", "H09"],
        "H07": ["H04", "H10"],
        "H08": ["H05", "H10"],
        "H09": ["H06", "H10"],
        "H10": ["H07", "H08", "H09"],
    }
    print(f"Adjacency list: {graph}")
    print(f"Fewest-hop route H01 to H10: {bfs_shortest_route(graph, 'H01', 'H10')}")
    print(f"DFS reachable from central H01: {dfs_reachable(graph, 'H01')}")

    hourly_counts = [80, 95, 120, 150, 180, 220, 210, 190, 160, 140]
    print(f"Highest 4-hour window: {highest_four_hour_average(hourly_counts)}")
    print(f"Palindrome 'H01-H10-H10-H01': {is_hub_palindrome('H01-H10-H10-H01')}")
    print(f"Palindrome 'H01, H02, H03': {is_hub_palindrome('H01, H02, H03')}")


if __name__ == "__main__":
    main()
