from flask import Flask , redirect, url_for, render_template, request
import wikipedia
import os
import hashlib
import random



app = Flask(__name__)
usernames = open("usrnames.txt", "r")
usernames = usernames.read()

pasword = open("pasword.txt", "r")
pasword = pasword.read()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<name>")
def endles(name):
    try:
        results = wikipedia.summary(name, sentences=2)
    except:
        results = f"cant find data on {name}"
    return render_template("endles.html", name_web=name, results=results)

@app.route("/how_to_use")
def how_to_use():
    return render_template("how_to_use.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    usernames = open("usrnames.txt", "r")
    usernames = usernames.read()
    pasword = open("pasword.txt", "r")
    pasword = pasword.read()
    login_or_signin = "Login"
    if request.method == "POST":
        user = request.form["nm"]
        psw = request.form["psw"]
        if user in usernames:
            if psw >= "a" or psw > "0":
                if psw in pasword:
                    return redirect(url_for("user", usr=user))
                else:
                    return render_template("login.html", login_or_signin = login_or_signin, respon="the password not in the list", title="log in")
            else:
                return render_template("login.html", login_or_signin = login_or_signin, respon="you didn't type", title="log in")
        else:
            return  render_template("login.html", login_or_signin = login_or_signin, respon="the user name not in the list", title="log in")
    else:
        return render_template("login.html", login_or_signin = login_or_signin, title="log in")

@app.route("/user/<usr>")
def user(usr):
    usernames = open("usrnames.txt", "r")
    usernames = usernames.read()
    if usr in usernames:
        return f"<h1>{usr}</h1>"
    else:
        return"<h1>user not found</h1>"

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    usernames = open("usrnames.txt", "r")
    usernames = usernames.read()
    pasword = open("pasword.txt", "r")
    pasword = pasword.read()
    login_or_signin = "Signin"
    if request.method == "POST":
        user = request.form["nm"]
        psw = request.form["psw"]
        if not user in usernames:
            with open("usrnames.txt", "a") as a_file:
                a_file.write("\n")
                a_file.write(user)
            with open("pasword.txt", "a") as a_file:
                a_file.write("\n")
                a_file.write(psw)
            return render_template("created_your_user.html")
            return redirect(url_for("user", usr=user, psw=psw))
        else:
            return render_template("login.html", login_or_signin = login_or_signin, respon="the user name is already taken", title="sign in")
    else:
        return render_template("login.html", login_or_signin = login_or_signin, title="sign in")

@app.route("/user_list")
def user_list():
    usernames = open("usrnames.txt", "r")
    usernames = usernames.read()
    return render_template("user_list.html", usernames=usernames)

@app.route("/search_user", methods=["POST", "GET"])
def search_user():
    usernames = open("usrnames.txt", "r")
    usernames = usernames.read()
    if request.method == "POST":
        user_search = request.form["usr"]
        if user_search in usernames:
            if user_search >= "a" or user_search > "0":
                return redirect(url_for("user", usr=user_search))
            else:
                return render_template("search_user.html", search_find="you didn't type")
        else:
            return render_template("search_user.html", search_find = "user not found try again")
    return render_template("search_user.html")

@app.route("/search_endless", methods=["POST", "GET"])
def search_endless():
    if request.method == "POST":
        endlees_name_value = request.form["endless_search"]
        if endlees_name_value >= "a" or endlees_name_value > "0":
            return redirect(url_for("endles", name=endlees_name_value))
        else:
            return render_template("search_user.html", search_find="you didn't type")
    return render_template("search_endless.html")

@app.route("/edit_home_page/<usr>/<psw>", methods=["POST", "GET"])
def edit(usr, psw):
    if request.method == "POST":
        os.remove(f"home_page_{usr}.txt")
        user_file = open(f"home_page_{usr}.txt", "w")
        user_file.write("")
        user_file.close()
        img_url = request.form["img_url"]
        txt = request.form["txt"]
        with open(f"home_page_{usr}.txt", "a") as a_file:
            a_file.write("\n")
            a_file.write(img_url)
            a_file.write("\n")
            a_file.write(txt)
    return render_template("edit_home_page.html")
#the pssword is GHGgHy76Y767yt*&^7Y67T&^% user is IdanBekoHacker!#$#@133 d0aa8d87983b490e1936bbca7a180c55
@app.route("/try_to_hack_me_boss", methods=["POST", "GET"])
def try_to_hack_me_boss():
    robot_test =  str(random.randint(0, 9)) + "" + str(random.randint(0, 9)) + "" + str(random.randint(0, 9))
    robot_test_box = random.randint(0, 1)
    if robot_test_box == 0:
        text_box = "wirte 0"
    else:
        text_box = "wirte 1"
    if request.method == "POST":
        user = request.form["nm"]
        psw = request.form["psw"]
        userhash = hashlib.md5(user.encode())
        pswhash = hashlib.sha384(psw.encode())
        if user == "jhon":
            if psw == "GHGgHy76Y767yt*&^7Y67T&^%":
                return render_template("boss_got_in.html")
    else:
        return render_template("login_boss.html", login_or_signin="find the password or get into the system", title="try hack me", check = text_box)
    return render_template("login_boss.html", login_or_signin="find the password or get into the system", title="try hack me", check = text_box)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=3030)