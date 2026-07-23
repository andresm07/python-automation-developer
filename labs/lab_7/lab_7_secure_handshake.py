import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

API_FOLDER = ROOT / "api"

sys.path.insert(0, str(API_FOLDER))

import os

from dotenv import load_dotenv
from fake_api import FakeAPI  # type: ignore


def main():
    print("=" * 60)
    print("LAB 7 - SECURE HANDSHAKE")
    print("=" * 60)

    # ----------------------------------------------------------
    # Load credentials
    # ----------------------------------------------------------

    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("ERROR")
        print("CLIENT_ID or CLIENT_SECRET not found in .env")

        return

    print("\nCredentials successfully loaded.")

    # ----------------------------------------------------------
    # Create API client
    # ----------------------------------------------------------

    api = FakeAPI()

    # ----------------------------------------------------------
    # Authenticate
    # ----------------------------------------------------------

    print("\nAuthenticating with Fake Enterprise API...")

    auth = api.authenticate(
        client_id=client_id,
        client_secret=client_secret,
    )

    if auth.status_code == 401:
        print("\nAuthentication Failed")
        print(f"Status Code : {auth.status_code}")
        print(f"Message     : {auth.error}")

        return

    print("Authentication Successful")
    print(f"Access Token Received {auth.data.get('access_token')}")

    # ----------------------------------------------------------
    # Call protected endpoint
    # ----------------------------------------------------------

    print("\nRetrieving customers...\n")

    response = api.customers.list(
        page=1,
        page_size=10,
        sort="credit_score",
        order="desc",
    )

    if not response.ok:
        print("Request Failed")
        print(f"Status Code : {response.status_code}")
        print(f"Message     : {response.error}")

        return

    print(f"Status Code : {response.status_code}")
    print(f"Latency     : {response.processing_time_ms} ms")

    print()

    print("Top Customers")
    print("-" * 75)

    for customer in response.data["data"]:
        print(
            f"{customer['customer_id']:>4} | "
            f"{customer['first_name']} "
            f"{customer['last_name']:<20} | "
            f"{customer['country']:<5} | "
            f"Credit Score: {customer['credit_score']}"
        )

    print("\nRequest completed successfully.")


if __name__ == "__main__":
    main()
