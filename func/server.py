import re
import flask
import time
import json
from func import verified_code


def signup(database, data: dict):
    if database.simple_search("Users", "id = \"{}\"".format(data["id"])):
        return 101
    if data["password"] != data["confirm"]:
        return 102
    if len(data["email"]) > 7:
        pattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        if not re.match(pattern, data["email"]):
            return 104
    # if data["verifiedcode"]:
    data = {
        "id": data["id"],
        "password": data["password"],
        "email": data["email"],
        "nickname": data["name"],
    }
    database.add_new_user(data)


def signin(database, data: dict):
    search_re = database.simple_search("Users", "id=\"{}\"".format(data["id"]))
    if search_re:
        id, password, email, time_joined, _, name, _ = search_re[0]
    else:
        return 101
    if password == data["password"]:
        return 200
    else:
        return 101
