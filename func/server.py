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
        print(teacher)
        result = {
            "id": search_re[0],
            "teacher": teacher[2],
            "teacher_id": teacher[0],
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
            friends_name.append(personalinfo(database, i[0])["name"])
    return friends_name


def courses_of(database, id):
    def idtostu(database, id):
        search_re = database.simple_search("Users_Student", "user_id=\"{}\"".format(id))
        if search_re:
            return search_re[0][3]
        return False

    courses = {}
    stu_id = idtostu(database, id)
    if stu_id:
        search_re = database.simple_search("Attend", "student_id={}".format(stu_id))
        for i in search_re:
            courses[i[1]] = course_detail(database, i[1])["name"]
    return courses


def request_posts(db, id, dir, timestamp, num=5):
    def STRtoTIME(string):
        import datetime
        import time
        date_time = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        time_time = time.mktime(date_time.timetuple())
        return time_time

    def checkliked(table, sid):
        if db.simple_search(table, "sub_id={} and user_id={}".format(sid, id)):
            return True
        else:
            return False

    sub = db.simple_search("Sub", "poster_id={}".format(id))
    result = []
    for i in sub:
        content = None
        rating = None
        course_id = None
        tre = None
        course_name = None
        teacher_name = None
        teacher_id = None
        type = None

        id = i[0]
        post = db.simple_search("Post", "id={}".format(id))
        rev = db.simple_search("Review", "id={}".format(id))
        if post:
            content = post[0][1]
            type = "post"
        elif rev:
            print(rev)
            content = rev[0][3]
            rating = rev[0][4]
            course_id = rev[0][2]
            tre = course_detail(db, course_id)
            course_name = tre["name"]
            teacher_name = tre["teacher"]
            teacher_id = tre["id"]
            type = "review"
        else:
            continue
        user = personalinfo(db, i[1])
        temp = {
            "post_id": id,
            "type": type,  # post or review
            "poster_id": i[1],
            "poster_name": user["name"],
            "time": STRtoTIME(i[2]),
            "content": content,
            "likes": i[4],
            "dislikes": i[5],
            "liked": checkliked("Likes", id),  # whether the current user has liked this post
            "disliked": checkliked("Dislikes", id),  # whether the current user has disliked this post
            "comments": i[6],
            "rating": rating,  # 0 if is not a review
            "course_id": course_id,  # -1 if is not a review
            "course_name": course_name,  # "" if is not a review
            "teacher_name": teacher_name,  # "" if is not a review
            "teacher_id": teacher_id,  # -1 if is not a review
        }
        print(i)
        result.append(temp)
    return result


def request_reviews(database, id):
    rev = database.simple_search("Review", "course_id={}".format(id))
    result = []
    for i in rev:
        id = i[0]
        time = database.simple_search("Sub", "id={}".format(id))[0][2]
        content = i[3]
        rating = i[4]
        user = personalinfo(database, i[1])
        temp = {
            "post_id": id,
            "poster_id": i[1],
            "poster_name": user["name"],
            "time": time,
            "content": content,
            "rating": rating,  # 0 if is not a review
        }
        print(i)
        result.append(temp)
    return result


def like(database, user_id, sub_id, action):
    search_re = database.simple_search("Likes", "user_id={} and sub_id={}".format(user_id, sub_id))
    if action and not search_re:
        values = {
            "sub_id": sub_id,
            "user_id": user_id,
            "action": True
        }
        database.like("Likes", values)
        database.simple_set('Sub', 'id={}'.format(sub_id), 'likes',
                            list(database.simple_search("Sub", "id={}".format(sub_id)))[0][6] + 1)
    elif search_re and not action:
        database.simple_delete("Likes", "user_id={} and sub_id={}".format(user_id, sub_id))
        database.simple_set('Sub', 'id={}'.format(sub_id), 'likes',
                            list(database.simple_search("Sub", "id={}".format(sub_id)))[0][6] - 1)


def dislike(database, user_id, sub_id, action):
    search_re = database.simple_search("Dislikes", "user_id={} and sub_id={}".format(user_id, sub_id))
    if action and not search_re:
        values = {
            "sub_id": sub_id,
            "user_id": user_id,
            "action": True
        }
        database.like("Likes", values)
        database.simple_set('Sub', 'id={}'.format(sub_id), 'dislikes',
                            list(database.simple_search("Sub", "id={}".format(sub_id)))[0][6] + 1)
    elif search_re and not action:
        database.simple_delete("Dislikes", "user_id={} and sub_id={}".format(user_id, sub_id))
        database.simple_set('Sub', 'id={}'.format(sub_id), 'dislikes',
                            list(database.simple_search("Sub", "id={}".format(sub_id)))[0][6] + 1)


def follow(database, user_id, follow_id, follow):
    if user_id == follow_id:
        return False

    if follow:
        search_re = database.simple_search("Follow", "following_id={} and follower_id={}".format(follow_id, user_id))
        if not search_re:
            values = {
                "following_id": follow_id,
                "follower_id": user_id,
                "time_followed": "DATETIME(\"now\")",
                "seen": '0',
            }
            database.insert('Follow', values)
            return True
        return False
    else:
        search_re = database.simple_search("Follow", "following_id={} and follower_id={}".format(follow_id, user_id))
        if search_re:
            database.simple_delete("Follow", "following_id={} and follower_id={}".format(follow_id, user_id))
            return True
        return False


def comment(database, user_id, parent_id, timestamp, content, visibility):
    id = len(database.simple_search("Sub", "id>=0")) + 1
    data = {
        "id": str(id),
        "poster_id": str(user_id),
        "publicity": str(0),
        "likes": str(0),
        "dislikes": str(0),
        "comments": str(0),
        'visibility': visibility,
    }
    database.sub(data)
    data = {
        "id": str(id),
        'parent_id': str(parent_id),
        "content": content,
    }
    database.comment(data)
    database.simple_set('Sub', 'id={}'.format(parent_id), 'comments',
                        list(database.simple_search("Sub", "id={}".format(parent_id)))[0][6] + 1)
    return id


def get_comments(database, user_id, sub_id, ):
    def STRtoTIME(string):
        import datetime
        import time
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
    print(search_re)
    for comment in search_re:
        i = comment[0]
        sub_info = [list(x) for x in database.simple_search("Sub", "id={}".format(i))][0]
        usr_info = [list(x) for x in database.simple_search("Users", "id={}".format(sub_info[1]))][0]
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
        jj.append(re)
    return jj


# new functions
def post(database, user_id, content, visibility):
    id = len(database.simple_search("Sub", "id>=0")) + 1
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
        "content": content,
    }
    database.post(data)
    return id


def review(database, user_id, course_id, content, rating):
    id = len(database.simple_search("Sub", "id>=0")) + 1
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
        "user_id": str(user_id),
        "course_id": str(course_id),
        "content": content,
        "rating": str(rating),
        "anonymous": str(False),
        "seen": str(True),
        "quality": str(None)
    }
    database.review(data)
    update_rating(database, course_id)
    return True


def update_rating(database, id):
    re = database.simple_search("Review", "course_id={}".format(id))
    sum = 0
    for i in re:
        sum += i[4]
    avg = round(sum / len(re), 1)
    database.simple_set("Course", "id={}".format(id), "ave_rating", avg)


def followers(database, user_id):
    re = database.simple_search("Follow", "following_id={}".format(user_id))
    id = [i[1] for i in re]
    name = [personalinfo(database, i)["name"] for i in id]
    re = {
        "id": id,
        "name": name
    }
    return re


def followings(database, user_id):
    re = database.simple_search("Follow", "follower_id={}".format(user_id))
    id = [i[1] for i in re]
    name = [personalinfo(database, i)["name"] for i in id]
    re = {
        "id": id,
        "name": name
    }
    print(re)
    return re


def attend(database, id, usr_id):
    def idtostu(database, id):
        search_re = database.simple_search("Users_Student", "user_id=\"{}\"".format(id))
        if search_re:
            return search_re[0][3]
        return False

    data = {
        "student_id": idtostu(database, usr_id),
        "course_id": id
    }
    database.insert("Attend", data)


def courses(database, user_id):
    return 100


def follows(database, follower_id, following_id):
    if database.simple_search("Follow", "following_id={} and follower_id={}".format(following_id, follower_id)):
        return True
    return False


def teacher(database, id):
    def IDtoCOLLEGE(database, cid):
        re = database.simple_search("College", "id={}".format(cid))[0]
        return re[2]

    re = database.simple_search("Teacher", "id={}".format(id))[0]
    temp = {
        "name": re[2],
        "dscr": re[3],
        "college": IDtoCOLLEGE(database, re[1])
    }
    return temp


def tool(database, func, values):
    database[func](*values)
    return True
