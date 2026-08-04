import json

"""
    PYTHON DICTIONARY <-> JSON OBJECT
    dict <-> object {}
    list, tuple <-> []
    str <-> ""
    True/False <-> true/False
    None <-> null
"""

#! Dictionary <-> JSON

employee = {"name": "Andres", "rol": "developer"}

#! json.dumps() -> converts python dictionary to json object
employee_json = json.dumps(employee)

#! json.loads() -> converts json object to python dictionary
employee_from_json = json.loads(employee_json)


#! ------- EXPONENTIAL BACKOFF w TENACITY -------

import logging

import requests
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_attempt_number(retry_state):
    print(f"Attempt {retry_state.attempt_number} failed")
    print(f"Retrying in {retry_state.next_action.sleep:.2f} seconds...")


@retry(
    wait=wait_exponential_jitter(
        initial=1, max=10
    ),  # ? Starts 1s wait, scales up to 10s wait, with additional random jitter waiting time
    stop=stop_after_attempt(5),  # ? Will retry 5 times
    reraise=True,  # ? Reraise the original exception if all attempts fail
    before_sleep=log_attempt_number,  # ? Execute before every retry attempt
)
def fetch_api_data(url: str):
    print("Attempting API Request")

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    return response.json()


@retry(
    wait=wait_exponential_jitter(
        initial=1, max=10
    ),  # ? Starts 1s wait, scales up to 10s wait, with additional random jitter waiting time
    stop=stop_after_attempt(5),  # ? Will retry 5 times
    reraise=True,  # ? Reraise the original exception if all attempts fail
    before_sleep=log_attempt_number,  # ? Execute before every retry attempt
)
def fetch_paginated_api_data(url: str, retry_state: RetryCallState = None):
    print("Attempting Paginated API Request")

    attempt = retry_state.attempt_number if retry_state else 1

    if attempt > 1:
        print("Reduce pagination buffer or payload size")

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    return response.json()


try:
    data = fetch_api_data("https://api.example.com/data")
    print("Data Fetched Successfully")
except Exception as e:
    print(f"Failed after 5 attempts: {e}")

#! ------- EXPONENTIAL BACKOFF w NATIVE PYTHON MODULES -------

import random
import time


# ? Executes a function with exponential backoff and random jitter with native Python modules only
def call_with_exponential_backoff(
    func,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 32.0,
    backoff_factor: float = 2.0,
):
    attempt = 0

    while True:
        try:
            return func()
        except Exception as e:
            attempt += 1

            if attempt > max_retries:
                print(f"[ERROR] Max retries {max_retries} reached")
                raise e

            # ? Calculate exponential delay: base * (factor ^ (attempt - 1))
            calculated_delay = base_delay * (backoff_factor ** (attempt - 1))

            # ? Cap at maximum delay
            delay = min(calculated_delay, max_delay)

            # ? Add random jitter duration
            jittered_delay = random.uniform(0, delay)

            print(
                f"[Attempt {attempt} failed: {e}] Retrying in {jittered_delay:.2f} seconds..."
            )

            time.sleep(jittered_delay)


def fragile_network_call():
    if random.random() < 0.8:
        raise ConnectionError("503 Service Unavailable")
    return "Data Fetched Successfully"


result = call_with_exponential_backoff(fragile_network_call)
print(result)
