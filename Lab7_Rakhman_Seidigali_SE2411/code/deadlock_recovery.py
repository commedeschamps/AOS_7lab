"""Laboratory Work 7 - Task 4C: Detection and recovery with timeouts."""

import random
import threading
import time


TIMEOUT = 0.4
MAX_ATTEMPTS = 8

lock_A = threading.Lock()
lock_B = threading.Lock()

LOCKS = {
    "A": lock_A,
    "B": lock_B,
}


def backoff_delay(rng):
    return rng.uniform(0.05, 0.25)


def worker(thread_name, first_lock_name, second_lock_name, result, seed):
    rng = random.Random(seed)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        acquired_first = False
        acquired_second = False

        print(
            f"{thread_name}: attempt {attempt}, order "
            f"{first_lock_name} -> {second_lock_name}"
        )

        try:
            acquired_first = LOCKS[first_lock_name].acquire(timeout=TIMEOUT)
            if not acquired_first:
                delay = backoff_delay(rng)
                print(
                    f"{thread_name}: timeout on lock {first_lock_name}; "
                    f"backing off for {delay:.2f}s"
                )
                time.sleep(delay)
                continue

            print(f"{thread_name}: acquired lock {first_lock_name}")
            time.sleep(0.1)

            acquired_second = LOCKS[second_lock_name].acquire(timeout=TIMEOUT)
            if not acquired_second:
                delay = backoff_delay(rng)
                print(
                    f"{thread_name}: timeout on lock {second_lock_name}; "
                    f"releasing {first_lock_name}"
                )
                LOCKS[first_lock_name].release()
                acquired_first = False
                print(f"{thread_name}: released lock {first_lock_name}")
                print(f"{thread_name}: backing off for {delay:.2f}s")
                time.sleep(delay)
                continue

            print(f"{thread_name}: acquired lock {second_lock_name}")
            print(f"{thread_name}: completed critical section")
            result[thread_name] = "completed"
            return
        finally:
            if acquired_second:
                LOCKS[second_lock_name].release()
                print(f"{thread_name}: released lock {second_lock_name}")
            if acquired_first:
                LOCKS[first_lock_name].release()
                print(f"{thread_name}: released lock {first_lock_name}")

    result[thread_name] = "failed after retries"
    print(f"{thread_name}: failed after {MAX_ATTEMPTS} attempts")


def main():
    print("Starting timeout-based deadlock detection and recovery demo...")
    result = {}

    t1 = threading.Thread(
        target=worker,
        args=("Thread 1", "A", "B", result, 101),
    )
    t2 = threading.Thread(
        target=worker,
        args=("Thread 2", "B", "A", result, 202),
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("Final result:")
    for thread_name in sorted(result):
        print(f"  {thread_name}: {result[thread_name]}")


if __name__ == "__main__":
    main()
