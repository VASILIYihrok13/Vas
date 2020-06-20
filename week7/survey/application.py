import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    # визначаємо чи користувач ввів ім'я, гуртожиток, додаткове заняття.
    name = request.form.get("name")
    dorm = request.form.get("dorm")
    subject = request.form.get("subject")
    if not name or not dorm or not subject:
        return render_template("error.html", message="Ви не вказали ім'я або/і гуртожиток або/і додатковий заняття")

    # запис інформації до survey.csv
    file = open("survey.csv", "a")  # відкриття для "a" - append - додавання до списку.
    writer = csv.writer(file)
    writer.writerow((name, dorm, subject))  # записує в один рядок через кому
    file.close()

    return render_template("success.html")



@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        students = list(reader)
    n = 0
    n +=1
    return render_template("sheet.html", students = students, n = n)
