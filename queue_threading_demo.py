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
            queue_size = log_queue.qsize()
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
    print("[Main] Starting writer thread...")
    writer_thread = threading.Thread(target=file_writer, daemon=True)
    writer_thread.start()

    print("[Main] Starting worker threads...")
    workers = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        workers.append(t)
        t.start()

    print("[Main] Waiting for worker threads to finish...")
    for t in workers:
        t.join()
    print("[Main] All worker threads have finished processing.")

    # 1. Wait for all real log entries to be fully written to the file
    print("[Main] Waiting for the queue to completely empty out...")
    log_queue.join()
    print("[Main] All logs processed.")

    # 2. Now that the queue is empty, safely send the shutdown signal
    print("[Main] Sending shutdown signal to the writer thread...")
    log_queue.put(SHUTDOWN_SIGNAL)

    # 3. Wait for the writer thread to detect the signal, exit its loop, and terminate
    print("[Main] Waiting for writer thread to exit...")
    writer_thread.join()

    print(
        "[Main] All logs successfully written to output.log and threads safely closed!"
    )
