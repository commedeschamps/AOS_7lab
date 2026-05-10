"""Observation helper for Task 5 Windows monitoring.

This file is not a replacement for deadlock_recovery.py. It uses the same
timeout-based lock acquisition and retry idea, but keeps the Python process
alive longer so Task Manager and Resource Monitor screenshots can be captured.
"""

import os
import random
import threading
import time


TIMEOUT = 0.4
OBSERVATION_SECONDS = 60

lock_A = threading.Lock()
lock_B = threading.Lock()

LOCKS = {
    "A": lock_A,
    "B": lock_B,
}


def backoff_delay(rng):
    return rng.uniform(0.05, 0.25)


def worker(thread_name, first_lock_name, second_lock_name, stop_time, seed):
    rng = random.Random(seed)
    attempt = 1

    while time.time() < stop_time:
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
                attempt += 1
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
                attempt += 1
                continue

            print(f"{thread_name}: acquired lock {second_lock_name}")
            print(f"{thread_name}: completed critical section")
            time.sleep(0.2)
        finally:
            if acquired_second:
                LOCKS[second_lock_name].release()
                print(f"{thread_name}: released lock {second_lock_name}")
            if acquired_first:
                LOCKS[first_lock_name].release()
                print(f"{thread_name}: released lock {first_lock_name}")

        delay = backoff_delay(rng)
        print(f"{thread_name}: observation backoff for {delay:.2f}s")
        time.sleep(delay)
        attempt += 1

    print(f"{thread_name}: observation window finished")


def main():
    stop_time = time.time() + OBSERVATION_SECONDS

    print("Starting Task 5 observation helper...")
    print(f"Python PID: {os.getpid()}")
    print(f"Observation window: {OBSERVATION_SECONDS} seconds")
    print("Open Task Manager and Resource Monitor now to capture screenshots.")

    t1 = threading.Thread(
        target=worker,
        args=("Thread 1", "A", "B", stop_time, 101),
    )
    t2 = threading.Thread(
        target=worker,
        args=("Thread 2", "B", "A", stop_time, 202),
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("Observation helper finished.")


if __name__ == "__main__":
    main()
