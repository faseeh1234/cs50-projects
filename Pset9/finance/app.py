import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_portfolio = db.execute(
        "SELECT id, stock_id, user_id, SUM(quantity) FROM portfolio WHERE user_id = ? GROUP BY stock_id",
        session["user_id"],
    )

    user_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    if not user_cash:
        return apology("Error with cash")
    cash = user_cash[0]["cash"]
    current_worth = cash
    stock_dic = []
    for share in user_portfolio:
        quote = lookup(share["stock_id"])
        if quote:
            stock_row = {
                "name": quote["name"],
                "quantity": share["SUM(quantity)"],
                "price": quote["price"],
                "total": quote["price"] * share["SUM(quantity)"],
            }
        stock_dic.append(stock_row)
        current_worth += stock_row["total"]

    return render_template(
        "index.html",
        stock_dic=stock_dic,
        cash=cash,
        current_worth=current_worth,
    )
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    symbol = request.form.get("symbol")
    num_of_shares = request.form.get("shares")
    try:
        shares = int(num_of_shares)
        if shares < 1:
            return apology("Number of shares has to be a positive number")
    except ValueError:
        return apology("Number of shares must be an integer")

    stock = lookup(symbol)
    if not stock:
        return apology("Please enter a valid symbol", 400)

    total_cost = shares * stock["price"]
    current_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )
    if not current_cash:
        return apology("Error retrieving user's cash")
    current_cash = current_cash[0]["cash"]

    if total_cost > current_cash:
        return apology("Unaffordable", 400)


    # Inserting stock into portfolio
    portfolio_row = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND stock_id = ?", session["user_id"], symbol)
    if len(portfolio_row) == 0:
        db.execute(
            "INSERT INTO portfolio (user_id, stock_id, quantity) VALUES(?, ?, ?)", session["user_id"], symbol, num_of_shares
        )
    else:
        db.execute(
                "UPDATE portfolio SET stock_id = ?, quantity = quantity + ? WHERE user_id = ?", symbol, num_of_shares, session["user_id"]
            )

    db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"]
        )


    # Logging transaction in history
    db.execute("INSERT INTO history (user_id, stock_id, quantity, price, action, time) VALUES(?, ?, ?, ?, ?, ?)",
               session["user_id"], symbol, shares, stock["price"], "Bought", datetime.now())


    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT stock_id, quantity, price, action, time FROM history WHERE user_id = ?",
                                  session["user_id"])


    return render_template(
        "history.html",
        transactions=transactions
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = lookup(request.form.get("symbol"))
        # quote = lookup(symbol)
        if symbol == None:
            return apology("There is no stock with this symbol")
        return render_template("quoted.html", symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # post method for submitting a form
    if request.method == "POST":

        starting_cash = 10_000
        # submission from user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure password == confirmation
        if not (password == confirmation):
            return apology("the passwords do not match", 400)

        # Ensure password not blank
        if password == "" or confirmation == "" or username == "":
            return apology("input is blank", 400)

        # Ensure username does not exists already
        if len(rows) == 1:
            return apology("username already exist", 400)
        else:
            hashcode = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            db.execute(
                "INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)", username, hashcode, starting_cash
            )

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # Get list of current shares
        portfolio = db.execute(
            "SELECT DISTINCT stock_id FROM portfolio WHERE user_id = ? AND quantity > 0 ORDER BY stock_id",
            session["user_id"])

        return render_template("sell.html", portfolio=portfolio)

    symbol = request.form.get("symbol")
    sell_quantity = request.form.get("shares")
    try:
        sell_quantity = int(sell_quantity)
        if sell_quantity < 1:
            return apology("Number of shares has to be a positive number")
    except ValueError:
        return apology("Number of shares must be an integer")

    sell_quantity = int(sell_quantity)
    stock = lookup(symbol)
    if not stock:
        return apology("Please enter a valid symbol", 400)

    portfolio_row = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND stock_id = ?", session["user_id"], symbol)[0]

    print(f"SQ = {sell_quantity}\n current_shares = {int(portfolio_row["quantity"])}")
    if sell_quantity > int(portfolio_row["quantity"]):
        return apology("You do not have enough shares :(")

    total_revenue = sell_quantity * stock["price"]
    current_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )
    if not current_cash:
        return apology("Error retrieving user's cash")
    current_cash = current_cash[0]["cash"]


    # Removing stock from portfolio
    if int(portfolio_row["quantity"]) == sell_quantity:
        db.execute(
            "DELETE FROM portfolio WHERE user_id = ? AND stock_id = ?",
            session["user_id"], symbol
            )
    else:
        db.execute(
                "UPDATE portfolio SET quantity = quantity - ? WHERE user_id = ? AND stock_id = ?",
                sell_quantity, session["user_id"], symbol
            )


    db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
             total_revenue, session["user_id"]
        )

    # Logging transaction into history
    db.execute("INSERT INTO history (user_id, stock_id, quantity, price, action, time) VALUES(?, ?, ?, ?, ?, ?)",
            session["user_id"], symbol, sell_quantity, stock["price"], "Sold", datetime.now())

    return redirect("/")
