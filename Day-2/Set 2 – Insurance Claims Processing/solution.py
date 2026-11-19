
from collections import deque


class ClaimNode:
    def __init__(self, claim_id):
        self.claim_id = claim_id
        self.left = None
        self.right = None


class ClaimBST:
    def __init__(self):
        self.root = None

    def insert(self, claim_id):
        if self.root is None:
            self.root = ClaimNode(claim_id)
            return
        node = self.root
        while True:
            if claim_id == node.claim_id:
                return
            if claim_id < node.claim_id:
                if node.left is None:
                    node.left = ClaimNode(claim_id)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = ClaimNode(claim_id)
                    return
                node = node.right

    def search(self, claim_id):
        node = self.root
        while node is not None:
            if claim_id == node.claim_id:
                return True
            node = node.left if claim_id < node.claim_id else node.right
        return False

    def inorder(self):
        result = []

        def visit(node):
            if node:
                visit(node.left)
                result.append(node.claim_id)
                visit(node.right)

        visit(self.root)
        return result

    def preorder(self):
        result = []

        def visit(node):
            if node:
                result.append(node.claim_id)
                visit(node.left)
                visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        result = []

        def visit(node):
            if node:
                visit(node.left)
                visit(node.right)
                result.append(node.claim_id)

        visit(self.root)
        return result


def normalize_claim(policy_number, incident_date):
    normalized_policy = "".join(policy_number.lower().split())
    normalized_date = "".join(str(incident_date).lower().split())
    return normalized_policy, normalized_date


def find_duplicate_claims(claims):
    seen = {}
    duplicates = []
    for claim in claims:
        policy, date = normalize_claim(claim["policy"], claim["incidentDate"])
        key = (policy, date)
        if key in seen:
            duplicates.append((seen[key], claim["claimId"]))
        else:
            seen[key] = claim["claimId"]
    return duplicates


def shortest_stage_path(graph, start, target):
    queue = deque([start])
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node == target:
            break
        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    if target not in parent:
        return None
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))


def find_graph_loop_dfs(graph):
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


def longest_claim_spike(claim_counts, threshold=100):
    longest = 0
    current = 0
    longest_start = 0
    current_start = 0
    for index, count in enumerate(claim_counts):
        if count > threshold:
            if current == 0:
                current_start = index
            current += 1
            if current > longest:
                longest = current
                longest_start = current_start
        else:
            current = 0
    return longest_start, longest_start + longest - 1, longest


def merge_claim_lists(left, right):
    left_index = right_index = 0
    merged = []
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def main():
    claim_ids = [1042, 983, 1105, 901, 1000, 1201, 1075]
    tree = ClaimBST()
    for claim_id in claim_ids:
        tree.insert(claim_id)
    print("BST traversals:")
    print(f"  Inorder (sorted): {tree.inorder()}")
    print(f"  Preorder: {tree.preorder()}")
    print(f"  Postorder: {tree.postorder()}")
    print(f"  Search 1000={tree.search(1000)}, search 9999={tree.search(9999)}")

    claims = [
        {"claimId": "CLM-1", "policy": "POL 123", "incidentDate": "2026-11-01"},
        {"claimId": "CLM-2", "policy": " pol123 ", "incidentDate": "2026-11-01"},
        {"claimId": "CLM-3", "policy": "POL-999", "incidentDate": "2026-11-02"},
    ]
    print(f"Duplicate/near-duplicate claims: {find_duplicate_claims(claims)}")

    stages = {
        "registration": ["assessment"],
        "assessment": ["surveyor"],
        "surveyor": ["settlement"],
        "settlement": [],
    }
    print(f"Shortest approval path: {shortest_stage_path(stages, 'registration', 'settlement')}")
    loop_graph = {
        "registration": ["assessment"],
        "assessment": ["surveyor"],
        "surveyor": ["assessment", "settlement"],
        "settlement": [],
    }
    print(f"Approval loop detected: {find_graph_loop_dfs(loop_graph)}")

    claim_counts = [80, 75, 101, 140, 99, 120, 150, 130, 90, 105, 111]
    print(f"Longest claim spike above 100: {longest_claim_spike(claim_counts)}")
    print(f"Claim merge: {merge_claim_lists([], [])}")
    print(f"Claim merge example: {merge_claim_lists([1001, 1005, 1010], [1003, 1008, 1020])}")


if __name__ == "__main__":
    main()
