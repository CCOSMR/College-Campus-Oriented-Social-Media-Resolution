import re
import flask
import json


def get_json():
    data = str(flask.request.get_data(), encoding="UTF-8")
    dict = json.loads(data)
    return dict


def register(database, data: dict):
    if database.simple_search("Users", "id = \"{}\"".format(data["id"])):
        return "Invalid id"
    if database.simple_search("Users", "email = \"{}\"".format(data["email"])):
        return "Invalid email"
    if len(data["email"]) > 7:
        pattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        if not re.match(pattern, data["email"]):
            return "Invalid email"
    # if data["verifiedcode"]:
    data = {
        "id": data["id"],
        "password": data["password"],
        "email": data["email"],
        "name": data["name"],
    }
    database.add_new_user(data)
    return True


def login(database, data: dict):
    search_re = database.simple_search("Users", "id=\"{}\"".format(data["id"]))
    if search_re:
        id, password, email, time_joined, _, _, name, _ = search_re[0]
    else:
        return False
    if password == data["password"]:
        return True
    else:
        return False


def searchcourse(database, name: str):
    result = []
    search_re = database.simple_search("Course", "name like \"%{}%\"".format(name))
    if search_re:
        for course in search_re:
            temp = {
                "id": course[0],
                # "teacher_id": course[1],
                "name": course[2],
                # "_": course[3],
                "ave_rating": course[4],
                # "location": course[5],
                # "schedule": course[6]
            }
            result.append(temp)
    return result


def course_detail(database, id):
    search_re = database.simple_search("Course", "id={}".format(id))[0]
    if search_re:
        teacher = database.simple_search("Teacher", "id={}".format(search_re[1]))[0]
        result = {
            "id": search_re[0],
            "teacher": teacher[3],
            "name": search_re[2],
            "dscr": search_re[3],
            "ave_rating": search_re[4],
            "location": search_re[5],
            "schedule": search_re[6]
        }
        return result
    return False


def request_posts(id, dir, time, num=5):
    pass
