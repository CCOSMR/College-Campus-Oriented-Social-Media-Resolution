import flask
import time
import io
import os
from func import server
from func import database
from func import captcha
from flask import send_from_directory

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = '\xddIHij\x90\xc3\x89\xc9\xae\t0\xe0 \xbbz\xc5\xe7\x14o\xd1\ra\x0e'

db = database.Database("CCOSMR.db")


@app.route("/")
def default():
    if "id" in flask.session.keys():
        return flask.redirect("/home")
    else:
        return flask.redirect("/login")


@app.route("/test", methods=["GET", "POST"])
def test():
    if flask.request.method == "GET":
        return flask.request.remote_addr
    elif flask.request.method == "POST":
        data = server.get_json()
        return str(data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "GET":
        return flask.render_template('register.html')
    elif flask.request.method == "POST":
        data = server.get_json()
        status = server.register(db, data)
        if status == True:
            result = {"status": True, "message": None}
            return flask.jsonify(result)
        result = {"status": False, "message": status}
        return flask.jsonify(result)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template('login.html')
    elif flask.request.method == "POST":
        data = server.get_json()
        status = server.login(db, data)
        print(flask.session, status)
        if status:
            flask.session["id"] = data["id"]
            flask.session["time_signed"] = int(time.time())
            result = {
                "status": status,
                "url": flask.url_for("home")
            }
            return flask.jsonify(result)
        else:
            result = {
                "status": status,
                "url": None
            }
            return flask.jsonify(result)


@app.route("/home", methods=["GET", "POST"])
def home():
    if flask.request.method == "GET":
        if "id" in flask.session.keys():
            return flask.render_template('home.html')
        else:
            return flask.redirect("/login")


@app.route("/course", methods=["GET", "POST"])
def searchcourse():
    if flask.request.method == "GET":
        id = flask.request.args.get('courseid')
        if not id:
            return flask.render_template('course.html')
        else:
            data = server.course_detail(db, id)
            if data:
                return flask.render_template('courseinformation.html', name=data["name"], location=data["location"],
                                             teachername=data["teacher"], desc=data["dscr"], avg=data["ave_rating"])
            else:
                pass
    elif flask.request.method == "POST":
        data = server.get_json()
        result = server.searchcourse(db, data["search"])
        # result = [
        #     {"id": 1, "name": "1", "avg": 7.5},
        #     {"id": 2, "name": "2", "avg": 2.8},
        #     {"id": 3, "name": "3", "avg": 1.9}
        # ]
        return flask.jsonify(result)


@app.route("/request_posts", methods=["POST"])
def request_posts():
    import random
    data = server.get_json()
    # result = server.request_posts(id=flask.session["id"], dir=data["type"], time=data["time_stamp"], num=5)
    result = []
    for i in range(4):
        temp = {
            "post_id": random.randint(1, 999999),
            "poster_id": random.randint(1, 999999),
            "poster_name": names.split()[random.randint(0, 19)],
            "time": random.randint(1521043208, 1531043208),
            "content": sentences[random.randint(0, 49)],
            "likes": random.randint(0, 99),
            "dislikes": random.randint(0, 25),
            "comments": random.randint(0, 25),
        }
        result.append(temp)
    return flask.jsonify(result)


@app.route("/personalinfo", methods=["GET"])
def personalinfo():
    id = flask.request.args.get('id')
    return flask.render_template("personalpage.html", id=id)


@app.route("/personaldetail", methods=["GET"])
def personaldetail():
    id = flask.request.args.get('id')
    person = server.personalinfo(db, id)
    friends = server.friends_of(db, id)
    courses = server.courses_of(db, id)
    person = {
        "name": "dadfas",
        "email": "sdfadsfa"
    }
    friends = ["12312", "213123", "dsfdf"]
    courses = ["12312", "213123", "dsfdf"]
    result = {
        "user_name": person["name"],
        "user_email": person["email"],
        "friends": friends,
        "courses": courses
    }
    return flask.jsonify(result)


@app.route("/like", methods=["POST"])
def like():
    data = server.get_json()

    return flask.render_template("personalpage.html", id=id)


@app.route("/captcha", methods=["GET"])
def gen_captcha():
    params = flask.request.args.items()
    dic = {
        "bits": 4,
        "height": 100,
        "width": 60,
        "minlines": 3,
        "maxlines": 4
    }
    for item in params:
        key, value = item
        dic[key] = int(value)
    text, image = captcha.gene_code(dic["bits"], (dic["height"], dic["width"]), (dic["minlines"], dic["maxlines"]))
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/png', cache_timeout=0)


@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)


@app.route('/javascript/<path:filename>')
def serve_static(filename):
    return send_from_directory('javascript', filename)


if __name__ == "__main__":
    # This is for test
    # app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
