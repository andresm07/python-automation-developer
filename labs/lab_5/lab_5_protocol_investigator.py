import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

API_FOLDER = ROOT / "api"

sys.path.insert(0, str(API_FOLDER))

from fake_api import FakeAPI  # type: ignore

api = FakeAPI(api_key="training-key")


def get_customers(
    page: int = 1,
    page_size: int = 10,
    country: str | None = None,
    risk_level: str | None = None,
):
    params = {"page": page, "page_size": page_size}

    if country is not None:
        params["country"] = country

    if risk_level is not None:
        params["risk_level"] = risk_level

    return api.customers.list(**params)


def main():
    response = get_customers(
        page=1, page_size=10, country="US", risk_level="LOW"
    )

    print(f"[STATUS]: {response.status_code}")
    print(f"[EXECUTION TIME]: {response.processing_time_ms}")
    print(f"[REQUEST_ID]: {response.request_id}")

    print("\n")

    if response.ok:
        print("Customers: \n")

        for customer in response.data["data"]:
            print(f"{customer['customer_id']}")
            print(f"{customer['first_name']}")
            print(f"{customer['last_name']}")
            print(f"{customer['credit_score']}")
    else:
        print(response.error)


if __name__ == "__main__":
    main()
