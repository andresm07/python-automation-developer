import re

user_input = "   Rpt_2023-FINAL.csv  "
print(f"String without normalization: {user_input}")

#! str.strip() removes whitespaces
# ? Equivalent to TRIM on databases
user_input = user_input.strip()
print(f"String after executing .strip(): {user_input}")

#! str.upper() converts every letter to uppercase
user_input = user_input.upper()
print(f"String after executing .upper(): {user_input}")

#! str.lower() converts every letter to lowercase
user_input = user_input.lower()
print(f"String after executing .lower(): {user_input}")

#! str.replace(existing_value, replace_value) allows me to replace values with other values
user_input = user_input.replace("-final", "")
print(f"String after executing .replace(): {user_input}")

#! str.split(splitting_value) breaks the string into a list of N items, depending on how many splits it does based on the splitting_value
user_input = user_input.split("_")
print(f"String after executing .split(): {user_input}")


#! --- Converting a str to camelCase ---
full_name = "andres miranda arias"
full_name = full_name.split(" ")
print(full_name)

camel_case_full_name_format = ""

for word in full_name:
    if word == full_name[0]:
        camel_case_full_name_format += word
        continue
    camel_case_full_name_format += word.capitalize()

print(camel_case_full_name_format)

#! AndrÃ©s -> Andrés
raw_name = "Andr\u00c3\u00a9s"

fixed_name = raw_name.encode("latin1").decode("utf-8")

print(f"Raw Name: {raw_name}, Fixed Name: {fixed_name}")


#! ---------------- REGEX ----------------

# * user@domain.com

email_regex = r"^[a-zA-Z0-9.-_+]+@[a-zA-Z0-9.-_]+\.[a-zA-Z]{2,}$"

email = "user@domain.com"

print(bool(re.match(email_regex, email)))
