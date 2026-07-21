import json

"""
    PYTHON DICTIONARY <-> JSON OBJECT
    dict <-> object {}
    list, tuple <-> []
    str <-> ""
    True/False <-> true/False
    None <-> null
"""

#! Dictionary <-> JSON

employee = {"name": "Andres", "rol": "developer"}

#! json.dumps() -> converts python dictionary to json object
employee_json = json.dumps(employee)

#! json.loads() -> converts json object to python dictionary
employee_from_json = json.loads(employee_json)
