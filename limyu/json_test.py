import json

with open("../../json_test.json", "r", encoding='UTF8') as json_file:
    jsondata = json.load(json_file)

print(jsondata["모해"])
