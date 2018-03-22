import flask
import time
from func import server
from func import database

app = flask.Flask(__name__)
app.secret_key = '\xddIHij\x90\xc3\x89\xc9\xae\t0\xe0 \xbbz\xc5\xe7\x14o\xd1\ra\x0e'

db = database.Database("CCOSMR.db")


@app.route("/")
def default():
    if 'id' in flask.session:
        return 'Logged in as %s' % flask.escape(flask.session['id'])
    return flask.redirect("https://github.com/CCOSMR/College-Campus-Oriented-Social-Media-Resolution")


@app.route("/test", methods=["GET", "POST"])
def test():
    if flask.request.method == "GET":
        return flask.request.remote_addr
    elif flask.request.method == "POST":
        data = server.get_json()
        return str(data)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "GET":
        return "Under development"
    elif flask.request.method == "POST":
        # data = flask.request.get_json()
        data = server.get_json()
        status = server.signup(db, data)
        return str(status)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if flask.request.method == "GET":
        return "Under development"
    elif flask.request.method == "POST":
        # data = flask.request.get_json()
        data = server.get_json()
        status = server.signin(db, data)
        if status == 200:
            flask.session["id"] = data["id"]
            flask.session["time_signed"] = int(time.time())
            return flask.redirect("/")
        return str(status)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    pass


@app.route("/myfriends", methods=["GET", "POST"])
def myfriends():
    pass


@app.route("/addfriend", methods=["GET", "POST"])
def addfriend():
    pass


@app.route("/search", methods=["GET", "POST"])
def search():
    pass


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run()
