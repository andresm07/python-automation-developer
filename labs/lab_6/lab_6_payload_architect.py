import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

API_FOLDER = ROOT / "api"

sys.path.insert(0, str(API_FOLDER))

from fake_api import FakeAPI  # type: ignore

api = FakeAPI(api_key="training-key")


def create_customer(customer):
    return api.customers.create(customer)


def main():
    customer = {
        "first_name": "John",
        "last_name": "Doe",
        # "email": "john.doe@example.com",
        "country": "US",
        "status": "ACTIVE",
        "risk_level": "LOW",
        "credit_score": 745,
        "contact": {
            "phone": "+1-555-123-4567",
            "preferred_language": "English",
        },
        "address": {
            "street": "100 Main Street",
            "city": "Austin",
            "state": "Texas",
            "zip_code": "78701",
        },
        "employment": {
            "company": "Experian",
            "position": "Automation Engineer",
            "years": 5,
        },
        "products": [
            {
                "type": "Credit Card",
                "status": "ACTIVE",
                "limit": 10000,
            },
            {
                "type": "Mortgage",
                "status": "ACTIVE",
                "balance": 250000,
            },
        ],
    }

    response = create_customer(customer)

    print(f"Status Code : {response.status_code}")
    print(f"Request ID  : {response.request_id}")
    print(f"Latency     : {response.processing_time_ms} ms")

    print()

    if response.status_code == 201:
        print("Customer created successfully.")
        print(response.json())
    elif response.status_code == 400:
        print("Validation Error")
        print(response.error["message"])
        print()
        print("Missing Required Fields")

        for field in response.error["missing_fields"]:
            print(f" - {field}")
    else:
        print("Unexpected Error")
        print(response.error)


if __name__ == "__main__":
    main()
