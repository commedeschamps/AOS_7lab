"""Laboratory Work 7 - Task 2: Deadlock detection using a RAG.

The program models a Resource Allocation Graph (RAG) as a directed graph:
- Resource -> Process means the resource is allocated to the process.
- Process -> Resource means the process is requesting the resource.

For single-instance resources, a cycle in the RAG indicates deadlock.
"""

from collections import defaultdict


class ResourceAllocationGraph:
    """Directed graph with DFS-based cycle detection."""

    def __init__(self):
        self.adjacency = defaultdict(list)
        self._nodes = set()

    def add_edge(self, source, destination):
        """Add a directed edge to the graph."""
        self.adjacency[source].append(destination)
        self._nodes.add(source)
        self._nodes.add(destination)

    @property
    def nodes(self):
        return sorted(self._nodes)

    @property
    def edges(self):
        graph_edges = []
        for source in sorted(self.adjacency):
            for destination in sorted(self.adjacency[source]):
                graph_edges.append((source, destination))
        return graph_edges

    def detect_cycle(self):
        """Return (cycle_exists, cycle_path)."""
        color = {node: "white" for node in self._nodes}
        stack = []
        stack_index = {}

        def dfs(node):
            color[node] = "gray"
            stack_index[node] = len(stack)
            stack.append(node)

            for neighbor in sorted(self.adjacency[node]):
                if color[neighbor] == "white":
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
                elif color[neighbor] == "gray":
                    start = stack_index[neighbor]
                    return stack[start:] + [neighbor]

            stack.pop()
            stack_index.pop(node)
            color[node] = "black"
            return None

        for node in self.nodes:
            if color[node] == "white":
                cycle = dfs(node)
                if cycle:
                    return True, cycle

        return False, []


def build_graph(edges):
    graph = ResourceAllocationGraph()
    for source, destination in edges:
        graph.add_edge(source, destination)
    return graph


def print_scenario(title, edges):
    graph = build_graph(edges)
    deadlock_detected, cycle_path = graph.detect_cycle()

    print("=" * 72)
    print(title)
    print("-" * 72)
    print("Graph nodes:")
    print("  " + ", ".join(graph.nodes))
    print("Graph edges:")
    for source, destination in graph.edges:
        print(f"  {source} -> {destination}")
    print("Deadlock detected:", "YES" if deadlock_detected else "NO")

    if deadlock_detected:
        print("Cycle path:")
        print("  " + " -> ".join(cycle_path))
    else:
        print("Cycle path:")
        print("  None")
    print()


def main():
    scenarios = [
        (
            "Scenario 1: Classic three-process deadlock",
            [
                ("R1", "P1"),
                ("R2", "P2"),
                ("R3", "P3"),
                ("P1", "R2"),
                ("P2", "R3"),
                ("P3", "R1"),
            ],
        ),
        (
            "Scenario 2: No deadlock",
            [
                ("R1", "P1"),
                ("P2", "R1"),
            ],
        ),
        (
            "Scenario 3: Chain dependency without cycle",
            [
                ("R1", "P1"),
                ("R2", "P2"),
                ("P2", "R1"),
                ("P3", "R2"),
            ],
        ),
        (
            "Scenario 4: Only two processes are deadlocked",
            [
                ("R1", "P1"),
                ("R2", "P2"),
                ("R3", "P3"),
                ("P1", "R2"),
                ("P2", "R1"),
                ("P4", "R3"),
            ],
        ),
    ]

    for title, edges in scenarios:
        print_scenario(title, edges)


if __name__ == "__main__":
    main()
