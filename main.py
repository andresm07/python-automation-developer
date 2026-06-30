import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")

print(api_key)

list_example = []
string_example = ""

# def test():
#     x = 1 + 1
#     print(x)

# def main():
#     name = "Andres"
#     print(f"Hello {name}\n \t") #! \n -> Enter, \t -> Tab

#     addition = 1 + 1
#     subtraction = 1 - 1
#     multiplication = 1 * 1
#     division = 1 / 1
#     whole_division = 3 // 2
#     module = 3 % 2
#     power = 2 ** 3

#     greater_than = 2 > 3
#     less_than = 2 < 3
#     greater_or_equal = 3 >= 1
#     less_or_equal = 2 <= 5

#     equals = 1 == 2
#     difference = 2 != 1

#     print(addition, subtraction, multiplication, division, whole_division, module, power, greater_than, less_than, greater_or_equal, less_or_equal, equals, difference)

#     #! CLASS 06.23.2026

#     p = True
#     q = True
#     # p = 1
#     # p = "hello"
#     # p = 1.0

#     username_is_valid = True
#     password_is_valid = False
#     username_exists = True

#     p and q
#     p or q
#     not p

#     #* CONDITIONAL STATEMENTS

#     #? SIMPLE CONDITIONAL STATEMENT
#     if p:
#         print("Hello!")

#     #? DOUBLE CONDITIONAL STATEMENT
#     if username_is_valid and password_is_valid:
#         print("Hello!")
#     else:
#         print("Bye!")

#     #? MULTIPLE CONDITIONAL STATEMENTS
#     if username_is_valid and password_is_valid:
#         print("Hello!")
#     elif username_is_valid and not password_is_valid:
#         print("ERROR: Invalid Password")
#     elif not username_is_valid and password_is_valid:
#         print("ERROR: Invalid username")
#     else:
#         print("Bye!")

#     #? NESTED CONDITIONAL STATEMENTS
#     if username_exists:
#         if username_is_valid and password_is_valid:
#             print("Welcome")
#         elif username_is_valid:
#             print("Hello")
#         else:
#             print("ERROR")

#     #* ITERATION STATEMENTS

#     #? FOR LOOPS
#     for i in range(1, 10):
#         print(i)

#     #? WHILE LOOPS
#     while p:
#         print("Hello")
#         test()
#         p = False

#     #* ITERATION CONTROLS

#     #? BREAK
#     rows = []
#     for row in rows:
#         print(row)
#         break #! Fully Stops Iteration

#     #? CONTINUE
#     for row in rows:
#         if row == "":
#             continue #! Skips Current Iteration and Goes to Next One

#     for row in rows:
#         if row == "":
#             continue
#         else:
#             pass #! Syntactic Placeholder. Does Not Execute Anything


#! INVOICE PARSING CHALLENGE
# def main():
#     invoice_data = [
#         {"id": "INV-001", "amount": 1200, "status": "valid"},
#         {"id": "INV-002", "amount": 5500, "status": "valid"},
#         {},
#         {"id": "INV-003", "amount": 850, "status": "valid"},
#         {"id": "INV-004", "amount": 6200, "status": "valid"},
#         {},
#         {"id": "INV-005", "amount": 3100, "status": "valid"},
#         {"id": "INV-006", "amount": 450, "status": "valid"},
#         {"id": "INV-007", "amount": 7100, "status": "valid"},
#         {},
#         {
#             "id": "INV-008",
#             "amount": 0,
#             "status": "corrupted",
#             "error_token": "e=855N2575.3Z344b2",
#         },
#         {"id": "INV-009", "amount": 1500, "status": "valid"},
#         {"id": "INV-010", "amount": 9300, "status": "valid"},
#         {},
#         {"id": "INV-011", "amount": 2200, "status": "valid"},
#         {"id": "INV-012", "amount": 5050, "status": "valid"},
#         {"id": "INV-013", "amount": 1300, "status": "valid"},
#         {},
#         {"id": "INV-014", "amount": 4100, "status": "valid"},
#         {"id": "INV-015", "amount": 8000, "status": "valid"},
#     ]

#     flagged = [invoice for invoice in invoice_data
#                 if len(invoice)!=0
#                 if invoice["status"] == "valid"
#                 if invoice["amount"] >=5000]

#     print(flagged)

#     for invoice in invoice_data:
#         if not invoice:
#             continue

#         #! Approach 1: Validate through status
#         status = invoice.get("status")

#         if status != "valid":
#             break

#         #! Approach 2: Validate through error_token
#         error_token = invoice.get("error_token")

#         if error_token:
#             break

#         invoice_amount = invoice.get("amount")

#         if invoice_amount > 5000:
#             print(invoice)

#! CLASS 06.25.2026

def main():
    print("Class 06.25.2026")

    #? LISTS

    my_list = [1, 5.0, "test-id", True, [1, 2, 3], 1, 5.0, {"key": "value"}]

    print(my_list)
    print(my_list[0]) #! 1
    print(my_list[1]) #! 5.0

    my_list[3] = False

    print(my_list)

    my_list[3] = "Hello"

    print(my_list)

    # string = "Hello  1 !"

    # for character in string:
    #     print(character)

    for item in my_list:
        print("FOR", item)

    #print(my_list[10]) #! IndexError: list index out of range

    # #? TUPLES

    my_tuple = ("This is a Tuple", 1, False, [1, 2, 3], {"key": "value"})

    print(my_tuple[0])

    # print(my_tuple[10]) #! IndexError: tuple index out of range

    # my_tuple[2] = "Attempted Value Change for Tuples" #! TypeError: 'tuple' object does not support item assignment

    print(my_tuple)

    for item in my_tuple:
        print("FOR - TUPLE", item)

    for index, item in enumerate(my_tuple):
        print(f"Index {index}: {item}")

    # #? DICTIONARIES

    my_dictionary = {
        "first_name": "value",
        "last_name": 1,
        "address": True,
        "job_description": {},
        "phone_number": [1, 2, 3],
        "email": "value"
    }

    print(my_dictionary)

    print(my_dictionary.get("email"))

    my_dictionary["email"] = "andres@email.com"
    my_dictionary.update({"first_name": "Andres"})

    print(my_dictionary)

    my_second_dictionary = {
        "active": True
    }

    merged_dictionary = my_dictionary | my_second_dictionary

    print("MERGED: ", merged_dictionary)

    for keys in my_dictionary.keys():
        print("KEYS", keys)

    for values in my_dictionary.values():
        print("VALUES:", values)

    for key, value in my_dictionary.items():
        print(f"{key}: {value}")

    # #? SETS

    numbers = [1, 2, 3, 1, 5, 2, 4, 3, 2, 7, 8, 9]
    unique_numbers = set(numbers)
    print(unique_numbers)

    cars = {"audi", "ford", "chevrolet", "ferrari"}

    print(cars)

    cars.add("nissan")

    # cars[0] #! TypeError: 'set' object is not subscriptable

    print(cars)

    cars.remove("ford")
    # cars.remove("mclaren") #! KeyError: 'mclaren'
    cars.discard("mclaren") #! Safe Alternative to Removing Possibly Unexistent Items

    print(cars)

    car = cars.pop() #! Returns Back Arbitrary Item, No Control Over It, and Removes the Item

    print(car)

    immutable_cars = frozenset(cars)

    # immutable_cars.add("ford") #! AttributeError: 'frozenset' object has no attribute 'add'

    print(immutable_cars)

    finance_emails = {"johndoe@company.com", "janedoe@company.com", "andres@company.com"}
    dev_emails = {"roberto@company.com", "jose@company.com", "dayana@company.com", "johndoe@company.com"}

    union_emails = finance_emails | dev_emails

    print("UNION", union_emails)

    intersection_emails = finance_emails & dev_emails

    print("INTERSECTION", intersection_emails)

    difference_emails = finance_emails - dev_emails

    print("DIFFERENCE", difference_emails)

    for car in cars:
        print("FOR - SET", car)

    for index, car in enumerate(cars):
        print(f"{index}: {car}")

    for sorted_cars in sorted(cars):
        print("SORT", sorted_cars)

    #? FUNCTIONS

    def greet_user(user: str) -> str:
        # return "Hello " + str(user)
        return f"Hello {user}" #! "Hello" + user

    greet = greet_user("Andres")
    print(greet)

    name: str = 12 #! Type Annotations Ignored During Runtime
    print(type(name)) #! Output: <class 'int'> even if defined as str

    stored_username = "admin"
    stored_password = "admin1234"

    def login(username: str, password: str) -> bool:
        # x = True
        if username == stored_username and password == stored_password:
            return True
        else:
            return False

    login("admin", "admin")
    login("username", "1234")

    # print(username) #! username is locally scoped to login function
    # print(x) #! x in enclosed within login function

    def print_list():
        global list_example

        for item in list_example:
            print(item)

    def login_args(*args): #! *args are Positional Arguments as Tuple
        print(args)

    def login_kwargs(**kwargs): #! **kwargs are Keyword Arguments as Dictionary
        print(kwargs)

    login_args("admin", "admin1234")
    login_args("admin", "admin1234", "superadmin", "Andres")
    login_kwargs(user="admin", password="admin1234")
    login_kwargs(user="admin", password="admin1234", role="superadmin", name="Andres")

if __name__ == "__main__":
    main()
