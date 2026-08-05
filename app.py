from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_language", methods=["GET","POST"])
def add_one_language():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into language (name,short_name) values (:name,:short_name)",hey)
        user = query_db('select * from language')

        return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")


    user = query_db('select * from language')
    one_user = query_db("select * from language limit 1", one=True)
    return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")

@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_place", methods=["GET","POST"])
def add_one_place():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into place (name) values (:name)",hey)
        user = query_db('select * from place')

        return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")


    user = query_db('select * from place')
    one_user = query_db("select * from place limit 1", one=True)
    return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")

@app.route("/add_one_stage", methods=["GET","POST"])
def add_one_stage():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into stage (name) values (:name)",hey)
        user = query_db('select * from stage')

        return render_template("stageform.html", stages=user, one_user=one_user, the_title="add new stage")


    user = query_db('select * from stage')
    one_user = query_db("select * from stage limit 1", one=True)
    return render_template("stageform.html", stages=user, one_user=one_user, the_title="add new stage")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into user (username,email,password,country_id,language_id) values (:username,:email,:password,:country_id,:language_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','country_id','language_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, tousleslanguage=tousleslanguage)


    touslescountry= query_db("select * from country")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, tousleslanguage=tousleslanguage)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','country_id','language_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','country_id','language_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_chatmode", methods=["GET","POST"])
def add_one_chatmode():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        tousleslanguage= query_db("select * from language")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into chatmode (language_id,content,user_id,did_you_mean) values (:language_id,:content,:user_id,:did_you_mean)",hey)
        user = query_db('select * from chatmode')

        return render_template("chatmodeform.html", chatmodes=user, one_user=one_user, the_title="add new chatmode", tousleslanguage=tousleslanguage, touslesuser=touslesuser)


    tousleslanguage= query_db("select * from language")

    touslesuser= query_db("select * from user")

    user = query_db('select * from chatmode')
    one_user = query_db("select * from chatmode limit 1", one=True)
    return render_template("chatmodeform.html", chatmodes=user, one_user=one_user, the_title="add new chatmode", tousleslanguage=tousleslanguage, touslesuser=touslesuser)

@app.route("/add_one_post", methods=["GET","POST"])
def add_one_post():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesplace= query_db("select * from place")

        tousleslanguage= query_db("select * from language")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into post (place_id,language_id,content,user_id,did_you_mean) values (:place_id,:language_id,:content,:user_id,:did_you_mean)",hey)
        user = query_db('select * from post')

        return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesplace=touslesplace, tousleslanguage=tousleslanguage, touslesuser=touslesuser)


    touslesplace= query_db("select * from place")

    tousleslanguage= query_db("select * from language")

    touslesuser= query_db("select * from user")

    user = query_db('select * from post')
    one_user = query_db("select * from post limit 1", one=True)
    return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesplace=touslesplace, tousleslanguage=tousleslanguage, touslesuser=touslesuser)

@app.route("/add_one_fakepost", methods=["GET","POST"])
def add_one_fakepost():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesstage= query_db("select * from stage")

        tousleslanguage= query_db("select * from language")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into fakepost (stage_id,language_id,content,user_id,did_you_mean) values (:stage_id,:language_id,:content,:user_id,:did_you_mean)",hey)
        user = query_db('select * from fakepost')

        return render_template("fakepostform.html", fakeposts=user, one_user=one_user, the_title="add new fakepost", touslesstage=touslesstage, tousleslanguage=tousleslanguage, touslesuser=touslesuser)


    touslesstage= query_db("select * from stage")

    tousleslanguage= query_db("select * from language")

    touslesuser= query_db("select * from user")

    user = query_db('select * from fakepost')
    one_user = query_db("select * from fakepost limit 1", one=True)
    return render_template("fakepostform.html", fakeposts=user, one_user=one_user, the_title="add new fakepost", touslesstage=touslesstage, tousleslanguage=tousleslanguage, touslesuser=touslesuser)

