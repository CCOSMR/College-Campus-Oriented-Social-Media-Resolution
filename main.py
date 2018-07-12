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
            return flask.redirect("/home")
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
            id = flask.request.args.get('id')
            return flask.render_template('home.html', id=id)
        else:
            return flask.redirect("/login")


@app.route("/self", methods=["POST"])
def self():
    result = flask.jsonify({'id': flask.session['id'], 'name': server.personalinfo(db, flask.session['id'])['name']})
    return result


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return flask.render_template('profile.html')


@app.route("/course", methods=["GET", "POST"])
def searchcourse():
    if flask.request.method == "GET":
        id = flask.request.args.get('courseid')
        if not id:
            return flask.render_template('course.html')
        else:
            data = server.course_detail(db, id)
            if data:
                return flask.render_template('courseinformation.html', id=data["id"], name=data["name"],
                                             location=data["location"], teachername=data["teacher"], desc=data["dscr"],
                                             avg=data["ave_rating"], teacherid=data["teacher_id"])
            else:
                pass
    elif flask.request.method == "POST":
        data = server.get_json()
        result = server.searchcourse(db, data["search"])
        return flask.jsonify(result)


@app.route("/request_posts", methods=["POST"])
def request_posts():
    data = server.get_json()

    result = server.request_posts(db, flask.session['id'], data['type'], 0, 5)

    return flask.jsonify(result)


@app.route("/get_comments", methods=["POST"])
def get_comments():
    data = server.get_json()
    result = server.get_comments(db, flask.session["id"], data["post_id"])
    return flask.jsonify(result)


@app.route("/comment", methods=["POST"])
def comment():
    data = server.get_json()
    result = server.comment(db, flask.session["id"], data["parent_id"], data["time_stamp"], data["content"],
                            data["visibility"])
    re = {
        "status": True,
        "id": result
    }
    return flask.jsonify(re)


@app.route("/post", methods=["POST"])
def post():
    data = server.get_json()
    result = {'id': server.post(db, flask.session["id"], data['content'], '1'), 'status': True}
    return flask.jsonify(result)


@app.route("/follow", methods=["POST"])
def follow():
    data = server.get_json()
    result = server.follow(db, flask.session["id"], data["id"], data["follow"])
    re = {
        "status": result,
    }
    return flask.jsonify(re)


@app.route("/followers", methods=["POST"])
def followers():
    data = server.get_json()
    result = server.followers(db, data["id"])
    return flask.jsonify(result)


@app.route("/followings", methods=["POST"])
def followings():
    data = server.get_json()
    result = server.followings(db, data["id"])
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
    server.like(db, flask.session["id"], data["post_id"], data["like"])
    server.dislike(db, flask.session["id"], data["post_id"], data["dislike"])
    result = {
        "status": True
    }
    return flask.jsonify(result)


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


@app.route('/review', methods=["GET", "POST"])
def review():
    if flask.request.method == "GET":
        id = flask.request.args.get('courseid')
        re = server.request_reviews(db, id)
        return flask.jsonify(re)
    elif flask.request.method == "POST":
        data = server.get_json()
        status = server.review(db, flask.session["id"], data["id"], data["review"], data["rating"])
        re = {
            "id": flask.session["id"],
            "name": server.personalinfo(db, flask.session["id"])["name"]
        }
        return flask.jsonify(re)


@app.route('/attend', methods=["POST"])
def attend():
    data = server.get_json()
    server.attend(db, data["courseid"], flask.session["id"])
    return "123"


@app.route('/teacherinfo', methods=["GET"])
def teacherinfo():
    id = flask.request.args.get('teacherid')
    result = server.teacher(db, id)
    return flask.render_template("teacherinformation.html", name=result["name"], desc=result["dscr"],
                                 college=result["college"])


@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)


@app.route('/javascript/<path:filename>')
def serve_static(filename):
    return send_from_directory('javascript', filename)


@app.route("/user=<int:user_id>", methods=["GET"])
def user(user_id):
    return flask.render_template("profile.html", id=user_id)


@app.route("/user_info", methods=["POST"])
def user_info():
    data = server.get_json()
    personal_info = server.personalinfo(db, data['id'])
    result = {
        "name": personal_info['id'],
        "followings": server.followings(db, data['id']),
        "followed": server.follows(db, data['id'], flask.session["id"]),
        "followers": server.followers(db, data['id']),
        "following": server.follows(db, flask.session["id"], data['id']),
        "courses": server.courses(db, data['id']),
        "dscr": personal_info['dscr'],
    }
    print(server.follows(db, '123', '123'))
    return flask.jsonify(result)


@app.route('/static/pictures/<path:filename>')
def picture(filename):
    return send_from_directory('static/pictures', 'example.png', mimetype='image/png')


@app.route('/tool', methods=["GET", "POST"])
def tool():
    if flask.session["id"] == "admin":
        if flask.request.method == "GET":
            return flask.render_template("adtool.html")
        elif flask.request.method == "POST":
            if flask.session["id"] == "admin":
                data = server.get_json()
                server.tool(db, data["courseid"], flask.session["id"])
                return "123"
    else:
        return "Invalid access"


if __name__ == "__main__":
    # This is for test
    # app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
