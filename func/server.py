import re
import flask
import json


def get_json():
    data = str(flask.request.get_data(), encoding="UTF-8")
    dict = json.loads(data)
    return dict


def register(database, data: dict):
    if database.simple_search("Users", "id = \"{}\"".format(data["id"])):
        return "same id"
    if database.simple_search("Users", "email = \"{}\"".format(data["email"])):
        return "same email"
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
    search_re = database.simple_search("Course", "id={}".format(id))
    if search_re:
        search_re = search_re[0]
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


def personalinfo(database, id):
    search_re = database.simple_search("Users", "id=\"{}\"".format(id))
    if search_re:
        info = {
            "id": search_re[0][0],
            "email": search_re[0][2],
            "time_joined": search_re[0][3],
            "type": search_re[0][4],
            "activity": search_re[0][5],
            "name": search_re[0][6],
            "dscr": search_re[0][7]
        }
        return info
    return False


def friends_of(database, id):
    friends_name = []
    search_re = database.simple_search("Follow", "follower_id=\"{}\"".format(id))
    if search_re:
        for i in search_re:
            friends_name.append(personalinfo(i[0])["name"])
    return friends_name


def courses_of(database, id):
    def idtostu(database, id):
        search_re = database.simple_search("Users_Student", "user_id=\"{}\"".format(id))
        if search_re:
            return search_re[0][3]
        return False

    courses = []
    stu_id = idtostu(database, id)
    if stu_id:
        search_re = database.simple_search("Attend", "student_id={}".format(stu_id))
        for i in search_re:
            courses.append(course_detail(i[1])["name"])
    return courses


def request_posts(id, dir, time, num=5):
    pass


def like(database, user_id, sub_id, action):
    search_re = database.simple_search("Likes", "user_id={} and sub_id={}".format(user_id, sub_id))
    if action and not search_re:
        values = {
            "sub_id": sub_id,
            "user_id": user_id,
            "action": True
        }
        database.like("Likes", values)
    elif search_re and not action:
        database.simple_delete("Likes", "user_id={} and sub_id={}".format(user_id, sub_id))


def dislike(database, user_id, sub_id, action):
    search_re = database.simple_search("Dislikes", "user_id={} and sub_id={}".format(user_id, sub_id))
    if action and not search_re:
        values = {
            "sub_id": sub_id,
            "user_id": user_id,
            "action": True
        }
        database.like("Likes", values)
    elif search_re and not action:
        database.simple_delete("Dislikes", "user_id={} and sub_id={}".format(user_id, sub_id))


def comment(database, user_id, parent_id, timestamp, content, visibility):
    id = len(database.simple_search("Sub", "id>=0"))
    data = {
        "id": str(id),
        "poster_id": str(user_id),
        "publicity": str(0),
        "likes": str(0),
        "dislikes": str(0),
        "comments": str(0)
    }
    database.sub(data)
    data = {
        "id": str(id),
        "original_id": str(parent_id),
        "content": content,
        "seen": str(True)
    }
    database.comments(data)
    return id


def get_comments(database, user_id, sub_id, timestamp):
    def STRtoTIME(string):
        import datetime
        date_time = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        time_time = time.mktime(date_time.timetuple())
        return time_time

    def checkliked(table, id):
        if database.simple_search(table, "sub_id={} and user_id={}".format(id, user_id)):
            return True
        else:
            return False

    jj = []
    search_re = database.simple_search("Comments", "original_id={}".format(sub_id))
    for comment in search_re:
        i = comment[0]
        sub_info = database.simple_search("Sub", "id={}".format(i))
        usr_info = database.simple_search("Users", "id={}".format(sub_info[1]))
        re = {
            "comment_id": i,
            "commenter_id": sub_info[1],
            "commenter_name": usr_info[6],
            "time": STRtoTIME(sub_info[2]),
            "content": comment[2],
            "likes": sub_info[4],
            "dislikes": sub_info[5],
            "liked": checkliked("Likes", i),
            "disliked": checkliked("Dislikes", i),
            "comments": sub_info[6]
        }
        if not timestamp or re["time"] < timestamp:
            jj.append(re)
        if len(jj) == 5:
            break
    return jj
