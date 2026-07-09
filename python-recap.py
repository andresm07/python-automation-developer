import json

user: str = "I don't like ice cream"
age: int = 25
bank_account_balance: float = 151.74
is_user_valid: bool = True  #! or False

#! if condition_is_true:
if is_user_valid:
    print("Welcome")
#! elif condition_is_true == else if condition_is_true
elif not is_user_valid:
    print("Permission Denied")
#! else: when condition is False
else:
    print("Error")

user_logged_in: bool = True

#! while condition_is_true:
# ? If you do not update the condition or break, you face an infinite loop
# ? Manual control is required to exit the loop and advance to next iteration
while user_logged_in:
    print("Bank App Menu ...")

    sign_out = input("Enter Y to sign out: ")

    if sign_out.upper() == "Y":
        #! break -> breaks the loop and exits
        break

credit_scores = [740, 500, 120, 300]

#! for item in iterable:
#! iterables: lists, sets, tuples, dictionaries, strings
# ? No manual control required, iterations advance automatically
for credit_score in credit_scores:
    if credit_score > 650:
        print("High Credit Score")

#! lists []
credit_scores: list = [740, 500, 120, 300]
credit_scores[0] = 470  #! replace value at [i] index
last_credit_score_value = credit_scores[
    -1
]  #! get a value, in this case last one

#! tuples ()
login_info: tuple = ("user_one", "myStrong_passw0rd")
user_name: str = login_info[0]  #! extract value at [i] index
#! login_info[0] = "user_two" WILL break the code since tuples are immutable

#! dictionaries {}
api_response: dict = {
    "id": "EXP-01",
    "first_name": "John",
    "last_name": "Doe",
    "ssn": "XXXXXXXXX",
}
first_name: str = api_response.get(
    "first_name"
)  #! dict.get("key") retrieves value associated to the key
api_response["ssn"] = (
    "X-XXXX-XXXX"  #! dict["key"] = "" allows me to rewrite values
)

#! sets {}
dti_values: set = {1.85, 2.0, 0.74}

#! python dict -> json
api_response: dict = {
    "id": "EXP-01",
    "first_name": "John",
    "last_name": "Doe",
    "ssn": "XXXXXXXXX",
}

"""
    PYTHON DICTIONARY <-> JSON OBJECT
    dict <-> object {}
    list, tuple <-> []
    str <-> ""
    True/False <-> true/False
    None <-> null
"""

#! json.dumps(dict) generates a JSON object from a Python Dictionary
# ? indent=4 sets four spaces as indentation per level
"""
{
    "id": "7894654" -> indent=4
  "first_name": "John" -> indent=2
}
"""
api_response_json = json.dumps(api_response, indent=4)

#! json.loads(json_object) generates a Python Dictionary from a JSON object
api_response_back_to_dict = json.loads(api_response_json)


#! def function_name(parameter_one: type, ..., parameter_n: type) -> type:
#!     ... code block ...
#!     return value
# ? Parameters are not always needed, they are optional
def calculate_loan_application(
    ssn: str, age: int, name: str, income_level: str
) -> str:
    if age > 18 and income_level > 2500:
        return f"Loan Application Successful for {name} with SSN {ssn}"
    else:
        return f"Loan Application Denied for {name} with SSN {ssn}"
