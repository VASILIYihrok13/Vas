import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #  дві змінні для отримання інформації з двох баз даних.
    info = db.execute("SELECT symbol, corporation, SUM(number_buy), SUM(number_sell), SUM(number_buy) - SUM(number_sell) FROM client_info WHERE id =:id GROUP BY symbol",
        id = session['user_id'])
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id = session['user_id'] )

    money = float(cash[0]['cash'])  # змінна для підрахунку всіх грошей включаючи ціну акцій ( додавання акцій трохи нижче)
    cash = int(cash[0]['cash'])  # змінна для кількості грошей на рахунку

    for names in info:
        # ці рядки для отримання поточної ціни акцій. Додаємо то словника інфо - аби мати доступ до нього в циклі на хтмл сторінці
        shares = lookup(names['symbol'])
        shares = float(shares['price'])
        names['price'] = (usd(shares))

        total = shares * float(names['SUM(number_buy) - SUM(number_sell)'])

        names['total'] = usd(total)  #  додаємо до словника
        money += total

    return render_template("index.html", info = info, cash = usd(cash), money = usd(money))  # usd -  використовується для того аби відображалися цифри як долари )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # значення що ввів користувач. символ - назва акції та акції - число акцій.
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        price = lookup(symbol) # змінна для доступу до функції локап
        if not symbol or not price:  # перевірка чи є заданий символ в списку акцій
            return apology("symbol isn`t correct")
        if not shares.isdigit():
            return apology("Shares is not a integer", 400)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)

        cash = db.execute("SELECT cash FROM users WHERE id=:id", id = session['user_id'])  # доступ до коштів в базі даних

        # цей складний рядок перевіряє чи є достатньо коштів на рахунку - переводить все в числа й порівнює
        if int(cash[0]['cash']) < int(price['price'])*int(shares):
            return apology("You don`t have enough money in your account", 403)

        # додаємо інформацію до таблиці.
        db.execute("INSERT INTO client_info (id, symbol, corporation, purchase, cost, number_buy) VALUES (:id, :symbol, :corporation, :purchase, :cost, :number_buy)",
            id = session['user_id'], symbol = price['symbol'], corporation = price['name'],purchase = 'buy', cost = price['price'], number_buy = int(shares))
        db.execute("UPDATE users SET cash = cash -:payed WHERE id =:id", id = session['user_id'], payed = (int(shares) * price['price']))

        return redirect("/")

    return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    usernames = db.execute("SELECT * FROM users WHERE username =:username", username = username)

    try:
        result = usernames[0]['username']
        if not result:
            return jsonify(True)
        else:
            return jsonify(False)
    except IndexError:
        return jsonify(True)


@app.route("/password", methods=["GET", "POST"])
def change_password():
    """Changing password if user forgot"""
    if request.method == "POST":
        new_password = request.form.get("new_password")
        username = request.form.get("username")

        if new_password != request.form.get("new_confirmation"):
            return apology("Password and confirmation not the same")
        else:
            db.execute("UPDATE users SET hash =:new_password WHERE username =:username",
                username = username, new_password = generate_password_hash(new_password))
            return redirect("/")

    else:
        return render_template("password.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    info = db.execute("SELECT * FROM client_info WHERE id =:id ORDER BY date AND TIME", id = session['user_id'])

    return render_template("history.html", info = info)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")  # отримуємо символ що ввів користувач

        if not lookup(symbol) or not symbol:  # перевірка чи користувач ввів коректно символ
            return apology ("Sumbol isn`t correct", 400)
        price = lookup(symbol)

        name = price['name']
        costs = usd(price ['price'])
        symbols = price['symbol']

        return render_template("quoted.html", name = name, costs = costs, symbols = symbols)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        #змінні для імені та пароля
        username = request.form.get('username')
        password = request.form.get('password')

        # перевірка правильності вводу
        if not username or not password:
            return apology("You must provide username and password", 400)
        if password != request.form.get('confirmation'):
            return apology("Password and confirmation not the same", 400)

        # перевірка чи є вже користувач з таким ім'ям. поки не знаю чи працює
        usernames = db.execute("SELECT * FROM users WHERE username =:username", username = username)

        # запис в базу даних
        if username and usernames:
            return apology("Your name already used, please type new name or add some character", 400)
        else:
            db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
                username = username, hash = generate_password_hash(password))
            return render_template ("index.html")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    info = db.execute("SELECT symbol, SUM(number_buy) - SUM(number_sell) FROM client_info WHERE id=:id GROUP BY symbol", id = session['user_id'])

    if request.method == "POST":
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        # цикл для знаходження кількості акцій вибраної користувачем
        for names in info:
            if symbol == names['symbol']:
                share = int(names['SUM(number_buy) - SUM(number_sell)'])
                break

        #  перевірки вводу
        if not symbol or not share:
            return apology("Symbol is not correct", 400)
        if shares < 1 or shares > share:
            return apology("Shares number is too big or too small", 400)

        price = lookup(symbol)
        db.execute("INSERT INTO client_info (id, symbol, corporation, purchase, cost, number_sell) VALUES (:id, :symbol, :corporation, :purchase, :cost, :number_sell)",
            id = session['user_id'], symbol = price['symbol'], corporation = price['name'], purchase = 'sell', cost = price['price'], number_sell = shares)

        db.execute("UPDATE users SET cash = cash +:payed WHERE id =:id", id = session['user_id'], payed = (shares * price['price']))

        return redirect("/")


    return render_template("sell.html", info = info)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
