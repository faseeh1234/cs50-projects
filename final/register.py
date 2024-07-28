import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///register.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Gets the username from the text input box
        username = request.form.get("username")
        if not username:
            return "Insert a username"
        # Checks whether its a unique username
        past_user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username,
        )
        if past_user:
            return "Username already taken"
        # Gets the password from user
        password = request.form.get("password")
        if not password:
            return "Insert a password"
        # Checks whether the password is strong enough
        digits = 0
        specialcharacters = 0
        upperletters = 0
        lenght = len(password)

        for element in password:
            if element.isupper():
                upperletters += 1
            elif element.isdigit():
                digits += 1
            else:
                specialcharacters += 1
        if specialcharacters < 1 or digits < 1 or upperletters < 1 or lenght < 8:
            return "Your password has to include an upperletter, a digit, and a special character and have at least 8 characters"
        # Checks whether the password is the same as the confirmation
        if password != request.form.get("confirmation"):
            return "Passwords don't match"
        # Hashes the password
        hash = generate_password_hash(password)
        # Inserts the password into the table
        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash
        )
        if not user_id:
            return "Registration failed"
        # Hashes the password
        hash = generate_password_hash(password)
        # Inserts the password into the table
        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash
        )
        return redirect("/login")
