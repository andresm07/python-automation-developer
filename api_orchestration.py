# import json

# """
#     PYTHON DICTIONARY <-> JSON OBJECT
#     dict <-> object {}
#     list, tuple <-> []
#     str <-> ""
#     True/False <-> true/False
#     None <-> null
# """

# #! Dictionary <-> JSON

# employee = {"name": "Andres", "rol": "developer"}

# #! json.dumps() -> converts python dictionary to json object
# employee_json = json.dumps(employee)

# #! json.loads() -> converts json object to python dictionary
# employee_from_json = json.loads(employee_json)


# #! ------- EXPONENTIAL BACKOFF w TENACITY -------

# import logging
# import random

# import requests
# from tenacity import (
#     RetryCallState,
#     before_sleep_log,
#     retry,
#     stop_after_attempt,
#     wait_exponential,
#     wait_exponential_jitter,
# )

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def log_attempt_number(retry_state):
#     print(f"Attempt {retry_state.attempt_number} failed")
#     print(f"Retrying in {retry_state.next_action.sleep:.2f} seconds...")


# @retry(
#     wait=wait_exponential_jitter(
#         initial=1, max=10
#     ),  # ? Starts 1s wait, scales up to 10s wait, with additional random jitter waiting time
#     stop=stop_after_attempt(5),  # ? Will retry 5 times
#     reraise=True,  # ? Reraise the original exception if all attempts fail
#     before_sleep=log_attempt_number,  # ? Execute before every retry attempt
# )
# def fetch_api_data(url: str):
#     print("Attempting API Request")

#     response = requests.get(url, timeout=5)
#     response.raise_for_status()

#     return response.json()


# @retry(
#     wait=wait_exponential_jitter(
#         initial=1, max=10
#     ),  # ? Starts 1s wait, scales up to 10s wait, with additional random jitter waiting time
#     stop=stop_after_attempt(5),  # ? Will retry 5 times
#     reraise=True,  # ? Reraise the original exception if all attempts fail
#     before_sleep=log_attempt_number,  # ? Execute before every retry attempt
# )
# def fetch_paginated_api_data(url: str, retry_state: RetryCallState = None):
#     print("Attempting Paginated API Request")

#     attempt = retry_state.attempt_number if retry_state else 1

#     if attempt > 1:
#         print("Reduce pagination buffer or payload size")

#     response = requests.get(url, timeout=5)
#     response.raise_for_status()

#     return response.json()


# try:
#     data = fetch_api_data("https://api.example.com/data")
#     print("Data Fetched Successfully")
# except Exception as e:
#     print(f"Failed after 5 attempts: {e}")

# #! ------- EXPONENTIAL BACKOFF w NATIVE PYTHON MODULES -------

# import time


# # ? Executes a function with exponential backoff and random jitter with native Python modules only
# def call_with_exponential_backoff(
#     func,
#     max_retries: int = 5,
#     base_delay: float = 1.0,
#     max_delay: float = 32.0,
#     backoff_factor: float = 2.0,
# ):
#     attempt = 0

#     while True:
#         try:
#             return func()
#         except Exception as e:
#             attempt += 1

#             if attempt > max_retries:
#                 print(f"[ERROR] Max retries {max_retries} reached")
#                 raise e

#             # ? Calculate exponential delay: base * (factor ^ (attempt - 1))
#             calculated_delay = base_delay * (backoff_factor ** (attempt - 1))

#             # ? Cap at maximum delay
#             delay = min(calculated_delay, max_delay)

#             # ? Add random jitter duration
#             jittered_delay = random.uniform(0, delay)

#             print(
#                 f"[Attempt {attempt} failed: {e}] Retrying in {jittered_delay:.2f} seconds..."
#             )

#             time.sleep(jittered_delay)


# def fragile_network_call():
#     if random.random() < 0.8:
#         raise ConnectionError("503 Service Unavailable")
#     return "Data Fetched Successfully"


# result = call_with_exponential_backoff(fragile_network_call)
# print(result)

# #! ------- "EXPONENTIAL BACKOFF" w RETRY-AFTER HEADERS FROM API -------


# class DynamicHeaderWait:
#     def __init__(self, fallback_wait):
#         self.fallback_wait = fallback_wait

#     def __call__(self, retry_state: RetryCallState) -> float:
#         # ? Check if the last outcome was an exception containing an HTTP response
#         if retry_state.outcome.failed:
#             exception = retry_state.outcome.exception()

#             # ? Check requests/httpx style HTTP Errors
#             if (
#                 isinstance(exception, requests.exceptions.RequestException)
#                 and exception.response is not None
#             ):
#                 retry_after = exception.response.headers.get("Retry-After")

#                 # ? Headers usually return seconds as an integer/float string
#                 if retry_after:
#                     try:
#                         seconds = float(retry_after)
#                         print(
#                             f"[DynamicHeaderWait] Retry-After Header found. Override wait time to: {seconds}s "
#                         )
#                         return seconds
#                     except ValueError:
#                         pass

#         # ? Fallback to standard exponential wait if no header is present
#         print(
#             f"[DynamicHeaderWait] No Retry-After Header found. Using exponential backoff fallback waiting time."
#         )
#         return self.fallback_wait(retry_state)


# def log_before_sleep(retry_state):
#     attempt = retry_state.attempt_number
#     sleep_time = retry_state.next_action.sleep
#     print(
#         f"[Tenacity] Attempt #{attempt} failed. Sleeping for {sleep_time:.2f}s before retrying."
#     )


# @retry(
#     wait=DynamicHeaderWait(fallback_wait=wait_exponential(min=1, max=10)),
#     stop=stop_after_attempt(5),
#     before_sleep=log_before_sleep,
#     reraise=True,
# )
# def fetch_from_httpbun():
#     # ? Forcing httpbun to reply with a 426 status code AND a "Retry-After: 5s" header
#     url = "https://httpbun.com/response-headers?Retry-After=5"

#     print("Sending request to endpoint")

#     response = requests.get(url)

#     randomStatusCode = random.randint(1, 3)

#     if randomStatusCode == 1:
#         print("[Mock Server] Simulating 429 Too Many Requests")
#         response.status_code = 429
#     elif randomStatusCode == 2:
#         print("[Mock Server] Simulating 503 Service Unavailable")
#         response.status_code = 503
#     else:
#         print("[Mock Server] Simulating 200 OK")
#         response.status_code = 200

#     response.raise_for_status()  # ? Raises HTTP Error

#     return response.json()


# try:
#     data = fetch_from_httpbun()
# except requests.exceptions.HTTPError as e:
#     print(f"[Final Output]: All retries exhausted: {e}")

# #! ----- PAGINATION -----

# # ? ----- LIMIT & OFFSET STRATEGY -----


# def fetch_limit_offset_data(
#     base_url: str, total_items: int = 50, batch_size: int = 10
# ):
#     offset = 0
#     all_records = []

#     print(f"Fetching data using Offset/Limit (Batch Size: {batch_size})")

#     while offset < total_items:
#         params = {
#             "batch_size": batch_size,
#             "offset": offset,
#         }

#         response = requests.get(f"{base_url}/get", params=params)
#         response.raise_for_status()

#         data = response.json()
#         current_args = data.get("args", {})

#         req_batch_size = int(current_args.get("batch_size", [0])[0])
#         req_offset = int(current_args.get("offset", [0])[0])

#         # ? Mock item generation based on the offset and batch_size
#         items_count = min(req_batch_size, total_items - req_offset)
#         page_items = [
#             f"Item-{i} - Batch Size/Offset"
#             for i in range(req_offset + 1, req_offset + items_count + 1)
#         ]

#         all_records.extend(page_items)

#         print(
#             f"Fetched page starting at offset {req_offset}: Retrieved {len(page_items)} items"
#         )

#         offset += batch_size

#     print(f"Total items retrieved: {len(all_records)} items.")
#     print(f"Records: {all_records}")


# fetch_limit_offset_data("https://httpbun.com")

# # ? ----- CURSOR / NEXT-PAGE TOKEN STRATEGY -----


# def fetch_cursor_data(base_url: str, max_pages: int = 4, batch_size: int = 50):
#     next_token = (
#         "token_page_1"  #! If API needs initial token, if not set to None
#     )
#     page_count = 0
#     all_records = []

#     print(
#         f"\n\n\nFetching data using Cursor/Next-Page Token (Batch Size: {batch_size})"
#     )

#     while True:
#         if not next_token:
#             break

#         params = {"batch_size": batch_size, "cursor": next_token}

#         response = requests.get(f"{base_url}/get", params=params)
#         response.raise_for_status()

#         data = response.json()

#         raw_cursor = data.get("args", {}).get("cursor", None)
#         current_cursor = (
#             raw_cursor[0] if isinstance(raw_cursor, list) else raw_cursor
#         )

#         page_count += 1
#         page_items = [
#             f"Record-{page_count}-{i} Cursor/Next-Page Token"
#             for i in range(1, batch_size + 1)
#         ]

#         all_records.extend(page_items)

#         print(
#             f"Page {page_count}: Processed {len(page_items)} items using cursor '{current_cursor}'"
#         )

#         if page_count >= max_pages:
#             break

#         next_token = f"token_page_{page_count + 1}"

#     print(
#         f"Total retrieved: {len(all_records)} items across {page_count} pages"
#     )
#     print(all_records)

#     assert len(all_records) == max_pages * batch_size


# fetch_cursor_data("https://httpbun.com")

# # ? ----- CURSOR / NEXT-PAGE TOKEN STRATEGY w GENERATORS -----

# """
# Standard Functions: [Fetch All Data] -> [Loads 10,000 items in RAM] -> Return List
# Generator: [Yield Page 1] -> Pause -> [Yield Page 2] -> Pause -> ...
# """

# """"
# - Memory Efficient: If the API has 100,000 records, you don't need to load all into a huge list. You consume each item or batch of items as it comes.
# - Instant Response: The application can start processing the first batch immediately without waiting for the entire pagination sequence to finish HTTP request.
# - Clean Code: It decouples the fetching logic fom the consumption logic.
# """


# def fetch_cursor_data_w_generators(
#     base_url: str, max_pages: int = 4, batch_size: int = 10
# ):
#     next_token = "token_page_1"
#     page_count = 0

#     print(
#         f"\n\n\nFetching data using Cursor/Next-Page Token + Generators (Batch Size: {batch_size})"
#     )

#     while True:
#         if not next_token:
#             break

#         params = {
#             "batch_size": batch_size,
#             "cursor": next_token,
#         }

#         response = requests.get(f"{base_url}/get", params=params)
#         response.raise_for_status()

#         data = response.json()

#         raw_cursor = data.get("args", {}).get("cursor", None)
#         current_cursor = (
#             raw_cursor[0] if isinstance(raw_cursor, list) else raw_cursor
#         )

#         page_count += 1
#         page_items = [
#             f"Record--{i} Page-{page_count} Cursor/Next-Page Token w Generators"
#             for i in range(1, batch_size + 1)
#         ]

#         #! YIELD the entire batch of items back to the caller
#         yield page_items, current_cursor

#         if page_count >= max_pages:
#             break

#         next_token = f"token_page_{page_count + 1}"


# for batch, token in fetch_cursor_data_w_generators(
#     "https://httpbun.com", max_pages=3, batch_size=5
# ):
#     print(f"Retrieved batch using token: '{token}': {batch}")

# # ? ----- CURSOR / NEXT-PAGE TOKEN STRATEGY w E-TAG CACHING -----

# """
# Feature     | ETag Caching              | Standard Caching
# ------------|---------------------------|----------------------------
# HTTP Headers| ETag & If-None-Match      | Cache-Control: max-age=XX
# ------------|---------------------------|----------------------------
# Network Req | Yes - Sends fast 304 check| Uses cached copies w/o req
# ------------|---------------------------|----------------------------
# Use Cases   | Dynamic data, paginated   | Static assets, historical
#             | lists, user profiles      | records, immutable files
# ------------|---------------------------|----------------------------
# Data        | Guaranteed real-time      | Subject to stale data if
# Freshness   | accuracy                  | backend updates before time
#             |                           | expires
# ------------|---------------------------|----------------------------
# """

# from urllib.parse import urlparse


# class ETagCachedClient:
#     def __init__(self):
#         self._cache = {}

#     def get(self, url: str):
#         headers = {}
#         cached_entry = self._cache.get(url)

#         # ? 1. Attach If-None-Match header if we have a cached ETag
#         if cached_entry and "etag" in cached_entry:
#             etag_val = cached_entry["etag"]
#             clean_etag = etag_val.strip('"')

#             headers["If-None-Match"] = clean_etag

#         response = requests.get(url, headers=headers)

#         # ? 2. CACHE HIT: Server returned 304 Not Modified
#         if response.status_code == 304:
#             print(f"[304 Not Modified] Cache hit: Zero payload download")
#             print(f"  └─ Cached ETag: {etag}")

#             return cached_entry["data"]

#         # ? 3. CACHE MISS / FRESH DATA: Server returned 200 OK
#         elif response.status_code == 200:
#             print(f"[200 OK] Cache Miss: Downloading payload")

#             try:
#                 data = response.json()
#             except ValueError:
#                 data = response.text

#             etag = response.headers.get("ETag") or response.headers.get("etag")

#             #! httpbun fix: /etag/:tag doesn't send ETag in response headers,
#             #! so we fallback to extracting the tag from the URL path if missing.
#             if not etag and "/etag/" in url:
#                 tag_from_url = urlparse(url).path.split("/")[-1]
#                 etag = f'"{tag_from_url}"'

#             if etag:
#                 print(f"  └─ Cached ETag: {etag}")
#                 self._cache[url] = {"etag": etag, "data": data}

#             return data
#         else:
#             response.raise_for_status()


# client = ETagCachedClient()
# test_url = "https://httpbun.com/etag/v1.0-hash-abc123"

# print("\n\n\n--- Step 1: Initial Request (Cold Cache) ---")
# data1 = client.get(test_url)
# print(f"Data 1: {data1}")

# print("--- Step 2: Subsequent Request (Warm Cache) ---")
# data2 = client.get(test_url)
# print(f"Data 2: {data2}")

# print("--- Step 3: Requesting Modified Resource (Cache Invalidation) ---")
# updated_url = "https://httpbun.com/etag/v2.0-hash-xyz789"
# data3 = client.get(updated_url)
# print(f"Data 3: {data3}")

#! --- API TO TABLE TRANSFORMATIONS 2026.08.11 ---

import pandas as pd

data = [
    {
        "id": 1,
        "name": "Alice",
        "dob": "1994-01-15",
        "contact": {"email": "alice@example.com", "phone": "123-456-7890"},
        "location": {"city": "San Francisco", "state": "CA", "zip": "94784"},
    },
    {
        "id": 2,
        "name": "Bob",
        "dob": "1994-07-15",
        "contact": {"email": "bob@example.com", "phone": "456-789-1230"},
        "location": {"city": "Austin", "state": "TX", "zip": "45678"},
    },
]

print(f"Nested JSON: \n\n{data}")
df = pd.json_normalize(data)
df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
print(f"Normalized DataFrame: \n{df}")

# ? JSON W NESTED ARRAYS

data_w_arrays = [
    {
        "id": 1,
        "name": "Alice",
        "contact": {"email": "alice@example.com", "phone": "123-456-7890"},
        "location": {"city": "San Francisco", "state": "CA", "zip": "94784"},
        "orders": [
            {"order_id": "ord-01", "price": 120.0},
            {"order_id": "ord-02", "price": 130.0},
        ],
    },
    {
        "id": 2,
        "name": "Bob",
        "contact": {"email": "bob@example.com", "phone": "456-789-1230"},
        "location": {"city": "Austin", "state": "TX", "zip": "45678"},
        "orders": [
            {"order_id": "ord-03", "price": 140.0},
            {"order_id": "ord-04", "price": 150.0},
        ],
    },
]

# ? record_path -> Target list to "explode" into rows
# ? meta -> top-level fields to replicate
df_w_arrays = pd.json_normalize(
    data_w_arrays,
    record_path=["orders"],
    meta=[
        "id",
        "name",
        ["contact", "email"],
        ["contact", "phone"],
        ["location", "city"],
        ["location", "state"],
        ["location", "zip"],
    ],
)

print(f"Normalized DataFame w Arrays: \n\n{df_w_arrays}")

# ? JSON W MISSING DATA

data_w_arrays = [
    {
        "id": 1,
        "name": "Alice",
        "contact": {"email": "alice@example.com", "phone": "123-456-7890"},
        "location": {"city": "San Francisco", "state": "CA", "zip": "94784"},
        "orders": [
            {"order_id": "ord-01", "price": 120.0},
            {"order_id": "ord-02", "price": 130.0},
        ],
    },
    {
        "id": 2,
        # "name": "Bob"
        "contact": {"email": "bob@example.com", "phone": "456-789-1230"},
        "location": {"city": "Austin", "state": "TX", "zip": "45678"},
        "orders": [
            {"order_id": "ord-03", "price": 140.0},
            {"order_id": "ord-04", "price": 150.0},
        ],
    },
]

# ? errors="ignore" -> replaces missing information with a NaN (Not A Number) value
df_w_missing = pd.json_normalize(
    data_w_arrays,
    record_path=["orders"],
    meta=[
        "id",
        "name",
        ["contact", "email"],
        ["contact", "phone"],
        ["location", "city"],
        ["location", "state"],
        ["location", "zip"],
    ],
    errors="ignore",
)

print(f"Normalized DataFame w Missing Data: \n\n{df_w_missing}")

# ? JSON W NESTED EMPTY ARRAYS

data_w_empty_arrays = [
    {
        "id": 1,
        "name": "Alice",
        "contact": {"email": "alice@example.com", "phone": "123-456-7890"},
        "location": {"city": "San Francisco", "state": "CA", "zip": "94784"},
        "orders": [],
    },
    {
        "id": 2,
        "name": "Bob",
        "contact": {"email": "bob@example.com", "phone": "456-789-1230"},
        "location": {"city": "Austin", "state": "TX", "zip": "45678"},
        "orders": [
            {"order_id": "ord-03", "price": 140.0},
            {"order_id": "ord-04", "price": 150.0},
        ],
    },
]

df_w_empty_arrays = pd.json_normalize(
    data_w_empty_arrays,
    record_path=["orders"],
    meta=[
        "id",
        "name",
        ["contact", "email"],
        ["contact", "phone"],
        ["location", "city"],
        ["location", "state"],
        ["location", "zip"],
    ],
    errors="ignore",
)

print(f"Normalized DataFame w Empty Arrays: \n\n{df_w_empty_arrays}")

df_w_empty_arrays = pd.json_normalize(data_w_empty_arrays)
df_w_empty_arrays_exploded = df_w_empty_arrays.explode("orders")

print(
    f"Normalized Exploded DataFame w Empty Arrays: \n\n{df_w_empty_arrays_exploded}"
)

# ? GENERATING OUTPUT FILES

# * TO CSV FILES
df_w_arrays.to_csv("df_w_arrays.csv", index=False)

# * TO EXCEL FILES
#! Requires openpyxl to be installed
df_w_arrays.to_excel(
    "df_w_arrays.xlsx", index=False, sheet_name="Normalized Orders"
)

# * TO JSON FILES
df_w_arrays.to_json("df_w_arrays.json", orient="records", indent=4)

# * TO PARQUET FILES
#! Requires pyarrow to be installed
object_columns = df_w_arrays.select_dtypes(include=["object"]).columns
df_w_arrays[object_columns] = df_w_arrays[object_columns].astype(str)

df_w_arrays.to_parquet("df_w_arrays.parquet", index=False)
