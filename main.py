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
            result = {"status": status, "url": flask.url_for('login')}
            return flask.jsonify(result)
        result = {"status": status, "url": None}
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
        return flask.render_template('home.html')


@app.route("/course", methods=["GET", "POST"])
def searchcourse():
    if flask.request.method == "GET":
        id = flask.request.args.get('courseid')
        if not id:
            return flask.render_template('course.html')
        else:
            # data = server.course_detail(db, id)
            data = {
                "id": 1231231,
                "teacher": "SSS",
                "name": "Dajiba",
                "dscr": "chui niu bi",
                "ave_rating": 10,
                "location": "sushe",
                "schedule": "wan"
            }
            if data:
                return flask.render_template('courseinformation.html', name=data["name"], location=data["location"],
                                             teachername=data["teacher"], desc=data["dscr"], avg=data["ave_rating"])
            else:
                pass
    elif flask.request.method == "POST":
        data = server.get_json()
        # result = server.searchcourse(db, data["search"]
        result = [
            {"id": 1, "name": "1", "avg": 7.5},
            {"id": 2, "name": "2", "avg": 2.8},
            {"id": 3, "name": "3", "avg": 1.9}
        ]
        return flask.jsonify(result)


@app.route("/request_posts", methods=["POST"])
def request_posts():
    import random
    data = server.get_json()
    # result = server.request_posts(id=flask.session["id"], dir=data["type"], time=data["time_stamp"], num=5)
    result = []

    ####################################################
    ### The following content is only for prototype: ###
    ####################################################

    names = '''Kelley
Tatiana
Wesley
Wilfred
Vernetta
Francene
Cira
Murray
Seema
Arlean
Jacelyn
Darleen
Thea
Minna
Georgetta
Elke
Adelia
Lyda
Fumiko
Latarsha'''

    sentences = '''If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.
My Mum tries to be cool by saying that she likes all the same things that I do.
Two seats were vacant.
I hear that Nancy is very pretty.
A glittering gem is not enough.
He didn’t want to go to the dentist, yet he went anyway.
I want to buy a onesie… but know it won’t suit me.
Wow, does that work?
He turned in the research paper on Friday; otherwise, he would have not passed the class.
Please wait outside of the house.
I currently have 4 windows open up… and I don’t know why.
Everyone was busy, so I went to the movie alone.
This is the last random sentence I will be writing and I am going to stop mid-sent
Is it free?
He told us a very exciting adventure story.
I often see the time 11:11 or 12:34 on clocks.
The lake is a long way from here.
The river stole the gods.
The memory we used to share is no longer coherent.
Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind.
The shooter says goodbye to his love.
Abstraction is often one floor above you.
I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.
Yeah, I think it's a good environment for learning English.
He said he was not there yesterday; however, many people saw him there.
She was too short to see over the fence.
They got there early, and they got really good seats.
A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.
We have never been to Asia, nor have we visited Africa.
I love eating toasted cheese and tuna sandwiches.
Malls are great places to shop; I can find everything I need under one roof.
I'd rather be a bird than a fish.
Writing a list of random sentences is harder than I initially thought it would be.
It was getting dark, and we weren’t there yet.
He ran out of money, so he had to stop playing poker.
She wrote him a long letter, but he didn't read it.
She borrowed the book from him many years ago and hasn't yet returned it.
Where do random thoughts come from?
The sky is clear; the stars are twinkling.
Cats are good pets, for they are clean and are not noisy.
We have a lot of rain in June.
The clock within this blog and the clock on my laptop are 1 hour different from each other.
She folded her handkerchief neatly.
Sometimes, all you need to do is completely make an ass of yourself and laugh it off to realise that life isn’t so bad after all.
How was the math test?
If the Easter Bunny and the Tooth Fairy had babies would they take your teeth and leave chocolate for you?
The quick brown fox jumps over the lazy dog.
She always speaks to him in a loud voice.
I would have gotten the promotion, but my attendance wasn’t good enough.
Sixty-Four comes asking for bread.'''.splitlines()

    for i in range(5):
        temp = {
            "post_id": random.randint(1, 999999),
            "poster_id": random.randint(1, 999999),
            "poster_name": names.split()[random.randint(0,19)],
            "time": random.randint(1521043208, 1531043208),
            "content": sentences[random.randint(0,49)],
            "likes": random.randint(0, 99),
            "dislikes": random.randint(0, 25),
            "comments": random.randint(0, 25),
        }
        result.append(temp)
    return flask.jsonify(result)


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
def send_static(path):
    return app.send_static_file(path)


@app.route('/javascript/<path:filename>')
def serve_static(filename):
    return send_from_directory('javascript', filename)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
