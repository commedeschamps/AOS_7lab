"""Laboratory Work 7 - Task 4B: Deadlock prevention by lock ordering."""

import threading
import time


LOCKS = {
    "A": (1, threading.Lock()),
    "B": (2, threading.Lock()),
}


def acquire_locks_in_global_order(thread_name, requested_lock_names):
    """Acquire all requested locks in the same global order."""
    ordered_locks = sorted(requested_lock_names, key=lambda name: LOCKS[name][0])
    acquired = []

    print(
        f"{thread_name}: requested {requested_lock_names}, "
        f"acquiring in global order {ordered_locks}"
    )

    try:
        for lock_name in ordered_locks:
            print(f"{thread_name}: attempting to acquire lock {lock_name}")
            LOCKS[lock_name][1].acquire()
            acquired.append(lock_name)
            print(f"{thread_name}: acquired lock {lock_name}")
            time.sleep(0.1)

        print(f"{thread_name}: completed critical section")
    finally:
        for lock_name in reversed(acquired):
            LOCKS[lock_name][1].release()
            print(f"{thread_name}: released lock {lock_name}")


def main():
    print("Starting deadlock prevention demo with global lock ordering...")
    t1 = threading.Thread(
        target=acquire_locks_in_global_order,
        args=("Thread 1", ["A", "B"]),
    )
    t2 = threading.Thread(
        target=acquire_locks_in_global_order,
        args=("Thread 2", ["B", "A"]),
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("Both threads completed successfully.")
    print("Circular wait is removed because every thread acquires A before B.")


if __name__ == "__main__":
    main()
