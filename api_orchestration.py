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
    wait_exponential,
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


# try:
#     data = fetch_api_data("https://api.example.com/data")
#     print("Data Fetched Successfully")
# except Exception as e:
#     print(f"Failed after 5 attempts: {e}")

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


# result = call_with_exponential_backoff(fragile_network_call)
# print(result)

#! ------- "EXPONENTIAL BACKOFF" w RETRY-AFTER HEADERS FROM API -------


class DynamicHeaderWait:
    def __init__(self, fallback_wait):
        self.fallback_wait = fallback_wait

    def __call__(self, retry_state: RetryCallState) -> float:
        # ? Check if the last outcome was an exception containing an HTTP response
        if retry_state.outcome.failed:
            exception = retry_state.outcome.exception()

            # ? Check requests/httpx style HTTP Errors
            if (
                isinstance(exception, requests.exceptions.RequestException)
                and exception.response is not None
            ):
                retry_after = exception.response.headers.get("Retry-After")

                # ? Headers usually return seconds as an integer/float string
                if retry_after:
                    try:
                        seconds = float(retry_after)
                        print(
                            f"[DynamicHeaderWait] Retry-After Header found. Override wait time to: {seconds}s "
                        )
                        return seconds
                    except ValueError:
                        pass

        # ? Fallback to standard exponential wait if no header is present
        print(
            f"[DynamicHeaderWait] No Retry-After Header found. Using exponential backoff fallback waiting time."
        )
        return self.fallback_wait(retry_state)


def log_before_sleep(retry_state):
    attempt = retry_state.attempt_number
    sleep_time = retry_state.next_action.sleep
    print(
        f"[Tenacity] Attempt #{attempt} failed. Sleeping for {sleep_time:.2f}s before retrying."
    )


@retry(
    wait=DynamicHeaderWait(fallback_wait=wait_exponential(min=1, max=10)),
    stop=stop_after_attempt(5),
    before_sleep=log_before_sleep,
    reraise=True,
)
def fetch_from_httpbun():
    # ? Forcing httpbun to reply with a 426 status code AND a "Retry-After: 5s" header
    url = "https://httpbun.com/response-headers?Retry-After=5"

    print("Sending request to endpoint")

    response = requests.get(url)
    response.status_code = 429
    response.raise_for_status()  # ? Raises HTTP Error

    return response.json()


try:
    data = fetch_from_httpbun()
except requests.exceptions.HTTPError as e:
    print(f"[Final Output]: All retries exhausted: {e}")
