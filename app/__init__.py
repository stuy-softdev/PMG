from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/edit_profile")
def edit_profile():
    return render_template("edit.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
