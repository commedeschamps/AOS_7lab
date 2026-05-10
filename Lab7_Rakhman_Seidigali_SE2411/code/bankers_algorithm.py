"""Laboratory Work 7 - Task 3: Banker's Algorithm.

Process labels in this script are one-based: P1, P2, P3, ...
Internally, Python list indices remain zero-based.
"""


class BankersAlgorithm:
    """Implementation of the safety and resource-request algorithms."""

    def __init__(self, available, max_demand, allocation, resource_names=None):
        self.available = [int(value) for value in available]
        self.max_demand = [list(row) for row in max_demand]
        self.allocation = [list(row) for row in allocation]
        self.process_count = len(allocation)
        self.resource_count = len(available)
        self.resource_names = resource_names or [
            f"R{index + 1}" for index in range(self.resource_count)
        ]
        self._validate_dimensions()
        self.need = self.calculate_need()

    def _validate_dimensions(self):
        if len(self.max_demand) != self.process_count:
            raise ValueError("max_demand and allocation must have the same row count.")

        for matrix_name, matrix in (
            ("max_demand", self.max_demand),
            ("allocation", self.allocation),
        ):
            for row in matrix:
                if len(row) != self.resource_count:
                    raise ValueError(
                        f"{matrix_name} rows must match the number of resources."
                    )

    def calculate_need(self):
        """Need = Max - Allocation."""
        return [
            [
                self.max_demand[process][resource]
                - self.allocation[process][resource]
                for resource in range(self.resource_count)
            ]
            for process in range(self.process_count)
        ]

    def process_label(self, process_index):
        return f"P{process_index + 1}"

    @staticmethod
    def _vector_leq(left, right):
        return all(left_value <= right_value for left_value, right_value in zip(left, right))

    @staticmethod
    def _vector_add(left, right):
        return [left_value + right_value for left_value, right_value in zip(left, right)]

    @staticmethod
    def _vector_subtract(left, right):
        return [left_value - right_value for left_value, right_value in zip(left, right)]

    def display_state(self):
        """Print Available, Max, Allocation, and Need."""
        headers = ["Process", "Allocation", "Max", "Need"]
        print(f"{headers[0]:<10}{headers[1]:<18}{headers[2]:<18}{headers[3]:<18}")
        print("-" * 64)
        for process in range(self.process_count):
            print(
                f"{self.process_label(process):<10}"
                f"{str(self.allocation[process]):<18}"
                f"{str(self.max_demand[process]):<18}"
                f"{str(self.need[process]):<18}"
            )
        print(f"Available: {self.available}")
        print()

    def is_safe(self, verbose=True):
        """Run the safety algorithm.

        Returns:
            (is_safe_state, safe_sequence, unfinished_processes)
        """
        work = list(self.available)
        finish = [False] * self.process_count
        safe_sequence = []

        if verbose:
            print("Running safety algorithm...")
            print(f"Initial Work = Available = {work}")

        progress = True
        while progress:
            progress = False
            for process in range(self.process_count):
                if not finish[process] and self._vector_leq(self.need[process], work):
                    if verbose:
                        print(
                            f"  {self.process_label(process)} can finish: "
                            f"Need {self.need[process]} <= Work {work}"
                        )
                    work = self._vector_add(work, self.allocation[process])
                    finish[process] = True
                    safe_sequence.append(self.process_label(process))
                    progress = True
                    if verbose:
                        print(
                            f"  Work after {self.process_label(process)} releases "
                            f"resources: {work}"
                        )

        unfinished = [
            self.process_label(process)
            for process in range(self.process_count)
            if not finish[process]
        ]
        is_safe_state = all(finish)

        if verbose:
            print("Safe state:", "YES" if is_safe_state else "NO")
            if is_safe_state:
                print("Safe sequence:", " -> ".join(safe_sequence))
            else:
                print("Processes that cannot proceed:", ", ".join(unfinished))
            print()

        return is_safe_state, safe_sequence, unfinished

    def request_resources(self, process_id, request):
        """Try to grant a request using the Banker's Algorithm.

        Args:
            process_id: one-based process id, for example P1 is process_id=1.
            request: list of requested resource instances.
        """
        process_index = process_id - 1
        if process_index < 0 or process_index >= self.process_count:
            raise ValueError("process_id must be between 1 and the process count.")
        if len(request) != self.resource_count:
            raise ValueError("request length must match the number of resources.")

        label = self.process_label(process_index)
        print(f"{label} requests {request}")
        print(f"Current Need[{label}] = {self.need[process_index]}")
        print(f"Current Available = {self.available}")

        if not self._vector_leq(request, self.need[process_index]):
            print("Decision: DENIED")
            print("Reason: request exceeds the process need.")
            print()
            return False

        if not self._vector_leq(request, self.available):
            print("Decision: DENIED")
            print("Reason: request exceeds currently available resources.")
            print()
            return False

        original_available = list(self.available)
        original_allocation = [list(row) for row in self.allocation]
        original_need = [list(row) for row in self.need]

        self.available = self._vector_subtract(self.available, request)
        self.allocation[process_index] = self._vector_add(
            self.allocation[process_index], request
        )
        self.need[process_index] = self._vector_subtract(
            self.need[process_index], request
        )

        safe, sequence, unfinished = self.is_safe(verbose=False)
        if safe:
            print("Decision: GRANTED")
            print("Reason: resulting state is safe.")
            print("Safe sequence after grant:", " -> ".join(sequence))
            print()
            return True

        self.available = original_available
        self.allocation = original_allocation
        self.need = original_need
        print("Decision: DENIED")
        print("Reason: resulting state would be unsafe.")
        print("Processes blocked in simulated state:", ", ".join(unfinished))
        print()
        return False


def run_classic_example():
    print("=" * 72)
    print("Classic 5-process, 3-resource example")
    print("=" * 72)

    available = [3, 3, 2]
    max_demand = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3],
    ]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]

    banker = BankersAlgorithm(available, max_demand, allocation, ["A", "B", "C"])

    print("Test 1: Check current state safety")
    banker.display_state()
    banker.is_safe()

    print("Test 2: P1 requests [1, 0, 2]")
    banker.request_resources(1, [1, 0, 2])

    print("Test 3: P4 requests [3, 3, 0]")
    banker.request_resources(4, [3, 3, 0])

    print("Test 4: Modified unsafe state")
    unsafe_banker = BankersAlgorithm(
        available=[0, 0, 0],
        max_demand=max_demand,
        allocation=allocation,
        resource_names=["A", "B", "C"],
    )
    unsafe_banker.display_state()
    unsafe_banker.is_safe()


def run_custom_example():
    print("=" * 72)
    print("Custom 4-process, 2-resource example")
    print("=" * 72)

    custom_available = [2, 1]
    custom_max = [
        [3, 2],
        [2, 2],
        [4, 3],
        [2, 1],
    ]
    custom_allocation = [
        [1, 0],
        [1, 1],
        [2, 1],
        [1, 0],
    ]

    banker = BankersAlgorithm(
        available=custom_available,
        max_demand=custom_max,
        allocation=custom_allocation,
        resource_names=["X", "Y"],
    )
    banker.display_state()
    banker.is_safe()


def main():
    run_classic_example()
    run_custom_example()


if __name__ == "__main__":
    main()
