"""Laboratory Work 7 - Task 4A: Real thread deadlock simulation."""

import threading
import time


lock_A = threading.Lock()
lock_B = threading.Lock()


def thread_one():
    print("Thread 1: attempting to acquire lock A")
    lock_A.acquire()
    print("Thread 1: acquired lock A")

    # This pause makes the deadlock easier to reproduce: it gives Thread 2
    # time to acquire lock B before Thread 1 requests it.
    time.sleep(0.1)

    print("Thread 1: waiting for lock B")
    lock_B.acquire()
    print("Thread 1: acquired lock B")


def thread_two():
    print("Thread 2: attempting to acquire lock B")
    lock_B.acquire()
    print("Thread 2: acquired lock B")

    # This pause creates the opposite half of the circular wait.
    time.sleep(0.1)

    print("Thread 2: waiting for lock A")
    lock_A.acquire()
    print("Thread 2: acquired lock A")


def main():
    print("Starting real deadlock simulation...")
    t1 = threading.Thread(target=thread_one, name="Thread-1", daemon=True)
    t2 = threading.Thread(target=thread_two, name="Thread-2", daemon=True)

    t1.start()
    t2.start()

    t1.join(timeout=3)
    t2.join(timeout=3)

    if t1.is_alive() and t2.is_alive():
        print("Deadlock detected: both threads are still alive after timeout.")
        print("Thread 1 holds lock A and waits for lock B.")
        print("Thread 2 holds lock B and waits for lock A.")
    else:
        print("No deadlock detected: at least one thread completed.")


if __name__ == "__main__":
    main()
