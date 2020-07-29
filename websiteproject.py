from flask import Flask, redirect, url_for, render_template, request, session,flash
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "123"
app.permanent_session_lifetime = timedelta(days = 30)

@app.route("/")
def blank():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    return render_template("index.html", displayname = "Login")


@app.route("/login/", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        flash(f"Logged in {user}", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in", "info")
            return redirect(url_for("user"))
        return render_template("login.html")



@app.route("/user/", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email saved","info")
        else:
            if "email" in session:
             email = session["email"]
        return render_template("user.html", email = email)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Logged out {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))
    

if __name__ == "__name__":
    app.run(debug=True)