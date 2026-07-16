import queue
import threading
import time

# ? Create a thread-safe FIFO queue
# ? FIFO: First In, First Out
log_queue = queue.Queue()

# ? Flag value to signal the writer thread to shut down safely
SHUTDOWN_SIGNAL = None


# ? Dedicated file writer worker/thread
def file_writer(filepath="output.log"):
    print("[WRITER] Started and waiting for logs...")
    # ? The file is opened ONCE and managed by a single thread
    with open(filepath, "a") as file:
        while True:
            # ? Check current queue size before grabbing an item
            queue_size = log_queue.size()
            print(f"[WRITER] Queue size before fetch: {queue_size}")

            # ? This blocks until an item is available in the queue
            log_entry = log_queue.get()

            # ? Check if we received the SHUTDOWN_SIGNAL to stop
            if log_entry is SHUTDOWN_SIGNAL:
                print(
                    "[WRITER] Received SHUTDOWN_SIGNAL. Closing writer thread."
                )
                log_queue.task_done()
                break

            # ? Write the data and immediately flush the file to ensure it saves
            print(f"[WRITER] Writing to file: {log_entry!r}")
            file.write(log_entry + "\n")
            file.flush()

            # ? Tell the queue that the processing of this task is done
            log_queue.task_done()


# ? Define Worker Thread
def worker(worker_id):
    print(f"[WORKER {worker_id}] Started working...")
    for i in range(3):
        time.sleep(0.5)  # ? Simulating heavy work (ie: regex processing)
        log_message = f"Worker {worker_id} - Log entry {i} completed"

        # ? Thread-safe put: multiple workers can call this simultaneously
        print(f"[WORKER {worker_id}] Putting entry into queue...")
        log_queue.put(log_message)

    print(f"[WORKER {worker_id}] Finished all work.")


if __name__ == "__main__":
    print("[MAIN] Starting writer thread...")
    # ? Start the writer thread as a background daemon
    writer_thread = threading.Thread(target=file_writer, daemon=True)

    print("[MAIN] Starting worker threads...")
    # ? Start 3 worker threads
    workers = []
    for i in range(3):
        thread = threading.Thread(target=worker, args=(i,))
        workers.append(thread)
        thread.start()

    print("[MAIN] Waiting for worker threads to finish...")
    # ? Wait for all the workers to finish their job respectively
    for thread in workers:
        thread.join()
    print("[MAIN] All worker threads have finished processing...")

    print("[MAIN] Waiting for the queue to completely empty out...")
    # ? Once workers are done, wait for the queue to completely empty out
    log_queue.join()
    print("[MAIN] Queue is empty...")

    print("[MAIN] Sending SHUTDOWN_SIGNAL to the writer thread...")
    # ? Send the SHUTDOWN_SIGNAL to stop the writer loop and exit the script cleanly
    log_queue.put(SHUTDOWN_SIGNAL)
    writer_thread.join()

    print("All logs successfully written to output.log")
