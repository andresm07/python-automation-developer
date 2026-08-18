import gc
import random
import time
import tracemalloc

import requests


def get_function_time(func, *args, **kwargs):
    gc.disable()

    start_time = time.perf_counter()

    result = func(*args, **kwargs)

    elapsed_time = time.perf_counter() - start_time

    gc.enable()

    print(f"[{func.__name__}] Execution Time: {elapsed_time:.6f} seconds")

    return result


def get_function_memory(func, *args, **kwargs):
    tracemalloc.start()

    result = func(*args, **kwargs)

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    print(
        f"[{func.__name__}] Net Allocated Memory: {current / (1024 * 1024):.2f} MB"
    )
    print(
        f"[{func.__name__}] Peak Memory Allocation: {peak / (1024 * 1024):.2f} MB"
    )

    return result


RISK_LEVELS = ["HIGH", "MEDIUM", "LOW"]


def fetch_cursor_data_stream(
    base_url: str, max_pages: int = 100, batch_size: int = 50
):
    next_token = "token_page_1"
    page_count = 0

    print(
        f"Fetching data using Cursor/Next-Page Token (Batch Size: {batch_size})"
    )

    while next_token and page_count < max_pages:
        params = {"batch_size": batch_size, "cursor": next_token}

        response = requests.get(f"{base_url}/get", params=params)
        response.raise_for_status()

        data = response.json()

        raw_cursor = data.get("args", {}).get("cursor", None)
        current_cursor = (
            raw_cursor[0] if isinstance(raw_cursor, list) else raw_cursor
        )

        page_count += 1

        page_items = [
            {
                "client_id": f"Client-{page_count}-{i}",
                "cursor": current_cursor,
                "risk_level": random.choice(RISK_LEVELS),
            }
            for i in range(1, batch_size + 1)
        ]

        print(
            f"Page {page_count}: Processed {len(page_items)} using cursor '{current_cursor}'"
        )

        yield from page_items

        next_token = f"token_page_{page_count + 1}"


if __name__ == "__main__":
    BASE_URL = "https://httpbun.com"
    MAX_PAGES = 10
    BATCH_SIZE = 50

    print("\n--- Timing Profile ---")
    high_risk_time_res = get_function_time(
        lambda *args, **kwargs: list(
            fetch_cursor_data_stream(*args, **kwargs)
        ),
        BASE_URL,
        max_pages=MAX_PAGES,
        batch_size=BATCH_SIZE,
    )

    print("\n --- Memory Profile ---")
    high_risk_memory_res = get_function_memory(
        lambda *args, **kwargs: list(
            fetch_cursor_data_stream(*args, **kwargs)
        ),
        BASE_URL,
        max_pages=MAX_PAGES,
        batch_size=BATCH_SIZE,
    )

    high_risk_clients = []
    total_processed = 0

    for client in fetch_cursor_data_stream(
        BASE_URL, max_pages=MAX_PAGES, batch_size=BATCH_SIZE
    ):
        total_processed += 1
        if client["risk_level"] == "HIGH":
            high_risk_clients.append(client)

    print("\n" + "=" * 50)
    print(f"Total Processed Clients: {total_processed}")
    print(f"High Risk Clients Found: {len(high_risk_clients)}")
    print("+" * 50)

    if high_risk_clients:
        print("\nSample High Risk Record")
        print(high_risk_clients[0])

    assert total_processed == MAX_PAGES * BATCH_SIZE
