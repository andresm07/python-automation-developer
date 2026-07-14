# import re
# from typing import Annotated

# from pydantic import BaseModel, Field, StringConstraints

# # user_input = "   Rpt_2023-FINAL.csv  "
# # print(f"String without normalization: {user_input}")

# # #! str.strip() removes whitespaces
# # # ? Equivalent to TRIM on databases
# # user_input = user_input.strip()
# # print(f"String after executing .strip(): {user_input}")

# # #! str.upper() converts every letter to uppercase
# # user_input = user_input.upper()
# # print(f"String after executing .upper(): {user_input}")

# # #! str.lower() converts every letter to lowercase
# # user_input = user_input.lower()
# # print(f"String after executing .lower(): {user_input}")

# # #! str.replace(existing_value, replace_value) allows me to replace values with other values
# # user_input = user_input.replace("-final", "")
# # print(f"String after executing .replace(): {user_input}")

# # #! str.split(splitting_value) breaks the string into a list of N items, depending on how many splits it does based on the splitting_value
# # user_input = user_input.split("_")
# # print(f"String after executing .split(): {user_input}")


# # #! --- Converting a str to camelCase ---
# # full_name = "andres miranda arias"
# # full_name = full_name.split(" ")
# # print(full_name)

# # camel_case_full_name_format = ""

# # for word in full_name:
# #     if word == full_name[0]:
# #         camel_case_full_name_format += word
# #         continue
# #     camel_case_full_name_format += word.capitalize()

# # print(camel_case_full_name_format)

# # #! AndrÃ©s -> Andrés
# # raw_name = "Andr\u00c3\u00a9s"

# # fixed_name = raw_name.encode("latin1").decode("utf-8")

# # print(f"Raw Name: {raw_name}, Fixed Name: {fixed_name}")


# #! ---------------- REGEX ----------------

# # # * user@domain.com

# # email_regex = r"^[a-zA-Z0-9.-_+]+@[a-zA-Z0-9.-_]+\.[a-zA-Z]{2,}$"

# # email = "user@domain.com"

# # print(bool(re.match(email_regex, email)))

# # ? re.search(regex_pattern, search_string)
# # ? Functionality: Scans the entire string for the FIRST match only
# # ? Uses: When you just need to find if a pattern exists inside a string

# search_string = "The price is $100 dollars."
# regex_pattern = r"\$\d{3}"

# regex_match = re.search(regex_pattern, search_string)

# if regex_match:
#     print(regex_match.group())

# # ? re.findall(regex_pattern, search_string)
# # ? Functionality: Finds all non-overlapping matches in the string
# # ? Uses: When you want to extract every instance of a pattern in a string

# search_string = "You can reach me at "
# regex_pattern = r"\d{3}-\d{3}-\d{4}"

# regex_match = re.findall(regex_pattern, search_string)

# if regex_match:
#     print(regex_match)

# # ? re.finditer(regex_pattern, search_string)
# # ? Functionality: Works exactly like re.findall(), but instead of a list, return an iterator of Match objects
# # ? Uses: When you need to more than just the matched string (start/end positions of each match) or when processing large string where a list would consume too much memory.

# search_string = "Error at line 10. Error at line 60."
# regex_pattern = r"Error"

# for match in re.finditer(regex_pattern, search_string):
#     print(f"Found 'Error' at index {match.start()}")

# # ? re.sub(regex_pattern, replacement_string, search_string)
# # ? Functionality: Replaces matches of a pattern with the replacement_string
# # ? Uses: Cleaning data, masking sensitive information, formatting strings

# search_string = "My card number is 4242 4242 4242 4242"
# regex_pattern = r"\d{4}"
# replacement_string = "****"

# masked_string = re.sub(regex_pattern, replacement_string, search_string)
# print(masked_string)

# # ? re.split(regex_pattern, search_string)
# # ? Functionality: Splits a string by the occurrences of a pattern
# # ? Uses: When the standard string.split(...) isn't powerful enough

# search_string = "apples, oranges; bananas  grapes! pears"
# search_string.split(",")  #! Manual, "not powerful enough" process

# regex_pattern = r"[,;\s!]+"

# fruits = re.split(regex_pattern, search_string)
# print(fruits)

# # ? re.compile(regex_pattern)
# # ? Functionality: Compiles a regex pattern into a regex object
# # ? Uses: If you are using the same regex in different locations. It saves Python from having to re-translate the regex string into machine code on every use

# regex_pattern = re.compile(r"[a-zA-Z0-9.-_+]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}")

# emails = [
#     "test@test.com",
#     "john.doe@email.com",
#     "invalid_test",
#     "hello@world.net",
#     "this_is_not_an_email",
# ]

# valid_emails = [email for email in emails if regex_pattern.search(email)]
# print(valid_emails)

# #! ---------- REGEX w PYDANTIC EXAMPLE ----------


# class User(BaseModel):
#     username: str = Field(pattern=r"^[a-zA-Z0-9._]{3,16}$")
#     password: str = Field(pattern=r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


# """ (?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,} EXPLANATION

# Section 1 >>> (?=.*[a-zA-Z]) Must contain at least one letter

# ?= Look from the very beginning of the string to see if the following pattern exists
# .* Scan past any number of characters
# [a-zA-Z] Find a letter, upper or lowercase

# Section 2 >>> (?=.*\d) Must contain at least one digit

# ?= Look from the very beginning of the string to see if the following pattern exists
# .* Scan past any number of characters
# \d Find a digit (0-9)

# Section 3 >>> [a-zA-Z\d]{8,} Only letters and number, at least 8 characters

# [a-zA-Z\d] Match any letters, upper or lowercase, or numbers
# {8,} Quantifier looking for at least 8 characters
# """

# USPhoneNumber = Annotated[
#     str,
#     StringConstraints(
#         pattern=r"^\+1-\d{3}-\d{3}-\d{4}$", strip_whitespace=True
#     ),
# ]


# class Contact(BaseModel):
#     mobile: USPhoneNumber
#     office: USPhoneNumber
#     home: USPhoneNumber


#! ---------- FILES ----------

# ? opening method -> r (read)
with open("example.txt", "r") as file:
    full_file = file.read()  # ? reads the entire file as a single string -> best for regex pattern matching
    print(full_file)
    file.seek(0)  # ? reset cursor position to beginning of file
    print("---------------------")
    lines = file.readlines()  # ? read file line by line, returns list of lines
    print(lines)
    file.seek(0)
    print("---------------------")
    first_line = file.readline()  # ? reads the file, one line at a time
    second_line = file.readline()
    print(first_line)
    print(second_line)

# ? opening method -> w (write)
# * [WARNING] 'w' rewrites the entire file!!
with open("example2.txt", "w") as file:
    file.write(
        "hello world from python\n"
    )  # ? writes a single string (line) to the file. It does NOT add "\n" (Enter) by default, you must do so manually if needed
    file.writelines(
        ["line 1\n", "line 2\n", "line 3\n"]
    )  # ? writes multiple strings (lines) to the file. It does NOT add "\n" (Enter) by default, you must do so manually if needed

# ? opening method -> a (append)
# * [INFO] does not rewrite the file, but rather appends new content
with open("example3.txt", "a") as file:
    text = "I'm appending content instead of rewriting the file\n"
    file.write(text)

# ? Handling two or more files at the same time
with (
    open("input.log", "r") as file_in,
    open("input2.log", "r") as file_in_two,
    open("output.log", "w") as file_out,
):
    content_file_one = file_in.read()
    content_file_two = file_in_two.read()
    file_out.write(content_file_one)
    file_out.write(content_file_two)
