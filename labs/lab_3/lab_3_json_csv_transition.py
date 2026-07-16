import csv
import json

try:
    with open("input.json", "r", encoding="utf-8") as file:
        api_response = json.load(file)
except FileNotFoundError:
    print(f"[ERROR] File input.json was not found.")
    exit(1)

flattened_data = []

for consumer in api_response.get("results"):
    flat_record = {
        "page": api_response.get("page"),
        "total_pages": api_response.get("total_pages"),
        "consumer_id": consumer.get("consumer_id"),
        "name": consumer.get("name"),
        "credit_score": consumer.get("credit_score"),
        "risk_band": consumer.get("risk_band"),
        "delinquent_accounts": consumer.get("delinquent_accounts"),
    }

    flattened_data.append(flat_record)

for record in flattened_data:
    assert isinstance(record.get("consumer_id"), str), (
        f"Invalid ID type: {record.get('consumer_id')}"
    )
    assert isinstance(record.get("name"), str), (
        f"Invalid Name type: {record.get('name')}"
    )
    assert isinstance(record.get("credit_score"), int), (
        f"Invalid Credit Score type: {record.get('credit_score')}"
    )
    assert isinstance(record.get("risk_band"), str), (
        f"Invalid Risk Band type: {record.get('risk_band')}"
    )
    assert isinstance(record.get("delinquent_accounts"), int), (
        f"Invalid Delinquent Accounts type: {record.get('delinquent_accounts')}"
    )

print("Data Integrity Check Passed")

with open("output.json", "w", encoding="utf-8") as output_file:
    json.dump(flattened_data, output_file, indent=2, ensure_ascii=False)

print("Successfully exported JSON data to output.json")

fieldnames = [
    "page",
    "total_pages",
    "consumer_id",
    "name",
    "credit_score",
    "risk_band",
    "delinquent_accounts",
]

with open("output.csv", "w", newline="\n", encoding="utf-8") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(flattened_data)

print("Successfully exported data to output.csv")
