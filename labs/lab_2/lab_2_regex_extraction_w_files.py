import pprint
import re


def extract_data(filepath="input.log"):
    with open(filepath, "r") as file:
        log_content = file.read()

    product_code = re.findall(r"PRD-\d+", log_content)[0]
    price_string = re.findall(r"\$(\d+\.\d+)", log_content)[0]
    date = re.findall(r"\d{4}-\d{2}-\d{2}", log_content)[0]

    structured_output = {
        "product_code": product_code,
        "price": f"${float(price_string)}",
        "date": date,
    }

    return structured_output


if __name__ == "__main__":
    result = extract_data()
    pprint.pprint(result)
