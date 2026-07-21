import pprint
import re

unstructured_input = """log_entry_09: proc_error %$!
item: PRD-9981 priced at
$45.99 ... user_id_none..
2023-11-01
end_log."""

product_code = re.findall(r"PRD-\d+", unstructured_input)[0]
price_string = re.findall(r"\$(\d+\.\d+)", unstructured_input)[0]
date = re.findall(r"\d{4}-\d{2}-\d{2}", unstructured_input)[0]

structured_output = {
    "product_code": product_code,
    "price": f"${float(price_string)}",
    "date": date,
}

pprint.pprint(structured_output)
