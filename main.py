import flask
import time
import io
from func import server
from func import database
from func import captcha

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = '\xddIHij\x90\xc3\x89\xc9\xae\t0\xe0 \xbbz\xc5\xe7\x14o\xd1\ra\x0e'

db = database.Database("CCOSMR.db")


@app.route("/")
def default():
    if 'id' in flask.session:
        return 'Logged in as %s' % flask.escape(flask.session['id'])
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
        return str(status)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template('login.html')
    elif flask.request.method == "POST":
        data = server.get_json()
        status = server.login(db, data)
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
def send_js(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run()
