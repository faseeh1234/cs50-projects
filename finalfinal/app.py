import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
import pytz
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import matplotlib.pyplot as plt

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# taken from helpers for finance
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route ('/')
def landing():
    return render_template ("landingpage.html")

@app.route ('/index')
@login_required
def index():
    if request.method =="GET":
        biceps_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "biceps")
        biceps_plan = biceps_1[0]["count"]
        bicepsplan = int(biceps_plan)
        if bicepsplan ==0:
            biceps = "not possible to calculate the "
        else:
            biceps_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "biceps")
            biceps_count = biceps_2[0]["count"]
            biceps = (biceps_count/bicepsplan)*100.0
        legs_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "legs")
        legs_plan = legs_1[0]["count"]
        if legs_plan ==0:
            legs = "not possible to calculate the "
        else:
            legs_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "legs")
            legs_count = legs_2[0]["count"]
            legs = (legs_count/legs_plan)*100.0
        shoulders_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "shoulders")
        shoulders_plan = shoulders_1[0]["count"]
        if shoulders_plan ==0:
            shoulders = "not possible to calculate the "
        else:
            shoulders_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "shoulders")
            shoulders_count = shoulders_2[0]["count"]
            shoulders = (shoulders_count/shoulders_plan)*100
        back_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "back")
        back_plan = back_1[0]["count"]
        if back_plan ==0:
            back = "not possible to calculate the "
        else:
            back_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "back")
            back_count = back_2[0]["count"]
            back = (back_count/back_plan)*100.0
        abs_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "abs")
        abs_plan = abs_1[0]["count"]
        if abs_plan ==0:
            abs = "not possible to calculate the "
        else:
            abs_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "abs")
            abs_count = abs_2[0]["count"]
            abs = (abs_count/abs_plan)*100.0
        chest_1 = db.execute ("SELECT * FROM splitplanned WHERE musclegroup = ?", "chest")
        chest_plan = chest_1[0]["count"]
        if chest_plan ==0:
            chest = "not possible to calculate the "
        else:
            chest_2 = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "chest")
            chest_count = chest_2[0]["count"]
            chest = (chest_count/chest_plan)*100.0
        return render_template("index.html", biceps=biceps, legs = legs, shoulders = shoulders, back=back, abs=abs, chest = chest )
    else:
        return render_template("index.html")

@app.route('/updateinfo', methods=["GET", "POST"])
@login_required
def updateinfo():
    if request.method =="GET":
        return render_template("updateinfo.html")
    else:
        weight = request.form.get("newweight")
        if not weight:
            return "Missing data"
        try:
            weight_int = int(weight)
        except ValueError:
            return "Weight must be a valid number"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute(
            "INSERT INTO weightchange (weight, date) VALUES (?, ?)",
                weight, date)

        db.execute ("UPDATE users SET weight = ?", weight)
        # Commit changes to the database after the insertion
        return redirect ("/index")

@app.route("/shoulders", methods=["GET", "POST"])
@login_required
def shoulders():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "shoulders")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("shoulders.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")

        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup,id ) VALUES (?, ?, ?, ?, ?,?)", exercise, weight_float, reps_int, date, "shoulders", session["user_id"] )
        # Commit changes to the database after the insertion
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "shoulders" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ?, id = ? WHERE musclegroup = ?", count, session["user_id"], "shoulders")
        return redirect ('/index')

@app.route("/legs", methods=["GET", "POST"])
@login_required
def legs():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "legs")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("legs.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")

        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup, id) VALUES (?, ?, ?, ?, ?, ?)", exercise, weight_float, reps_int, date, "legs", session["user_id"])
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "legs" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ?, id = ? WHERE musclegroup = ?", count, session["user_id"], "legs", )
        return redirect ('/index')
@app.route("/biceps", methods=["GET", "POST"])
@login_required
def biceps():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "biceps")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("biceps.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")
        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup, id) VALUES (?, ?, ?, ?, ?, ?)", exercise, weight_float, reps_int, date, "biceps", session["user_id"] )
        # Commit changes to the database after the insertion
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "biceps" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ? WHERE musclegroup = ?", count, session["user_id"], "biceps" )
        return redirect ('/index')

@app.route("/chest", methods=["GET", "POST"])
@login_required
def chest():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "chest")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("chest.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")

        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup,id ) VALUES (?, ?, ?, ?, ?,?)", exercise, weight_float, reps_int, date, "chest", session["user_id"] )
        # Commit changes to the database after the insertion
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "chest" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ?, id = ? WHERE musclegroup = ?", count, session["user_id"],  "chest" )
        return redirect ('/index')

@app.route("/back", methods=["GET", "POST"])
@login_required
def back():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "back")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("back.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")
        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup, id) VALUES (?, ?, ?, ?, ?, ?)", exercise, weight_float, reps_int, date, "back", session["user_id"] )
        # Commit changes to the database after the insertion
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "back" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ?, id = ? WHERE musclegroup = ?", count, session["user_id"],  "back" )
        return redirect ('/index')
@app.route("/abs", methods=["GET", "POST"])
@login_required
def abs():
    print(request.method)
    if request.method == "GET":
        exercises = db.execute(
            "SELECT exercise FROM exercisestypes WHERE musclegroup = ?", "abs")
        info = [x["exercise"] for x in exercises]
        print(info)
        return render_template("abs.html", exercises=info)
    else:
        print(request.form)
        exercise = request.form.get("exercise")
        weight = request.form.get("weight")
        reps = request.form.get("reps")
        if exercise is None:
            return "Missing exercise data"
        if not weight:
            return "Missing weight data"
        if not reps:
            return "Missing reps data"
        try:
            weight_float = float(weight)
            reps_int = int(reps)
            if weight_float <= 0 or reps_int <= 0:
                return "Invalid weight or reps"
        except ValueError:
            return "Weight and reps must be valid numbers"
        date = datetime.now(pytz.timezone("US/Eastern"))
        db.execute("INSERT INTO exercisesperformed (exercise, weight, reps, date, musclegroup, id) VALUES (?, ?, ?, ?, ?, ?)", exercise, weight_float, reps_int, date, "abs", session["user_id"] )
        # Commit changes to the database after the insertion
        count = db.execute ("SELECT * FROM splitcount WHERE musclegroup = ?", "abs" )
        count = count[0]["count"]
        count +=1
        db.execute ("UPDATE splitcount SET count = ?, id = ? WHERE musclegroup = ?", count, session["user_id"], "abs")
        return redirect ('/index')
@app.route('/addexercise', methods=["GET", "POST"])
@login_required
def addexercise():
    print(request.method)
    if request.method == "GET":
        musclegroups = db.execute(
            "SELECT DISTINCT musclegroup FROM exercisestypes")
        info = [x["musclegroup"] for x in musclegroups]
        print(info)
        return render_template("addexercise.html", musclegroups=info)
    else:
        musclegroup = request.form.get("musclegroup")
        exercise = request.form.get("newexercise")
        if not musclegroup:
            return "Missing info"
        if not exercise:
            return "Missing info"
        db.execute(
            "INSERT INTO exercisestypes (musclegroup, exercise) VALUES (?, ?)",
            musclegroup, exercise)
        return redirect ("/index")

@app.route('/history', methods = ["GET", "POST"])
@login_required
def history():
    if request.method =="POST":
        return render_template("history.html")
    else:
        rows = db.execute("SELECT * FROM exercisesperformed WHERE id = ?", session["user_id"] )
        print(rows)
        # Pass the history data to the history.html template
        return render_template("history.html", history=rows)

@app.route ('/split', methods = ["GET", "POST"])
@login_required
def split():
    print(request.method)
    if request.method == "GET":
        return render_template("split.html")
    else:
        shoulders = request.form.get("shoulders")
        legs = request.form.get("legs")
        biceps = request.form.get("biceps")
        chest = request.form.get ("chest")
        back = request.form.get("back")
        abs = request.form.get ("abs")
        try:
            shoulders_int = int (shoulders)
            legs_int = int(legs)
            biceps_int = int (biceps)
            chest_int = int(chest)
            back_int = int (back)
            abs_int = int(abs)
            if shoulders_int <= 0 or legs_int <= 0 or biceps_int<=0 or chest_int<=0 or back_int<=0 or abs_int<=0:
                return "Invalid numbers"
        except ValueError:
            return "Numbers in split must be valid numbers"
        db.execute("UPDATE splitplanned SET count = ?, id = ?  WHERE musclegroup = ?", shoulders_int, session["user_id"], "shoulders" )
        db.execute("UPDATE splitplanned SET count = ?, id = ? WHERE musclegroup = ? ", legs_int, session["user_id"], "legs")
        db.execute("UPDATE splitplanned SET count = ?, id = ? WHERE musclegroup = ?", biceps_int, session["user_id"], "biceps", )
        db.execute("UPDATE splitplanned SET count = ?, id =?  WHERE musclegroup = ?", chest_int, session["user_id"], "chest")
        db.execute("UPDATE splitplanned SET count = ?, id = ? WHERE musclegroup = ?", back_int, session["user_id"], "back" )
        db.execute("UPDATE splitplanned SET count = ?, id =? WHERE musclegroup = ? ", abs_int, session["user_id"], "abs")
    return redirect ("/index")
# to think - how does sesssion id work here?



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
        return redirect("/personal")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        # Ensure username was submitted
        if username is None:
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )
        if not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return "invalid username and/or password"


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/split")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    db.execute ("UPDATE splitcount SET count = ? WHERE id = ?", 0, session["user_id"] )
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/personal", methods=["GET", "POST"])
def personal():
    # to figure out - > how to apply session_id in this context ?
    if request.method == 'POST':
        print(request.form)
        try:
            db.execute("INSERT INTO personalinfo ( weight, height, gender) VALUES (?, ?, ?, ?)", request.form.get('weight'), request.form.get('height'), request.form.get('gender'))
        except Exception as e:
            print(f"Error inserting data into the database: {e}")
            flash("Please try again according to the details provided", "danger")
        return redirect("/login")
    else:
        return render_template("personal.html")


@app.route("/plot_weight_over_time", methods=["GET", "POST"])
def plot_weight_over_time():
    if request.method == "GET":
        # Fetch exercises from the database
        exercises = db.execute("SELECT DISTINCT exercise FROM exercisesperformed WHERE id = ?", session["user_id"])
        exercise_list = [exercise["exercise"] for exercise in exercises]

        return render_template("plot_weight_over_time.html", exercise_list=exercise_list, )
    else:
        selected_exercise = request.form.get("exercise")
        data = db.execute("SELECT weight, date FROM exercisesperformed WHERE exercise = ? AND id = ? ORDER BY date", selected_exercise, session["user_id"])

        weights = []
        dates = []

        for row in data:
            weight_str = str(row["weight"])  # Ensure it's a string
            if weight_str.replace('.', '', 1).isdigit():
                weights.append(float(weight_str))
                dates.append(row["date"])

        print(weights)  # Check the weights obtained
        print(dates)    # Check the dates obtained

        plt.figure(figsize=(10, 6))
        plt.plot(dates, weights, marker='o', linestyle='-', color='b')
        plt.title(f"Change of used weight over time for {selected_exercise}")
        plt.xlabel("Date")
        plt.ylabel("Weight Used")
        plt.xticks(rotation=45)

        if weights:
            min_weight = min(weights)
            max_weight = max(weights)
            plt.ylim(min_weight - 2, max_weight + 2)

        plt.tight_layout()
        plt.savefig('static/weight_over_time.png')

        return render_template("plot_weight_over_time.html")
