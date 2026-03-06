from flask import Flask, render_template, request, redirect, session
import sqlite3
from model import preprocess_text, predict_fraud
import re

app = Flask(__name__)
app.secret_key = "secretkey"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return redirect("/login")


# ---------------- Register ----------------
@app.route("/register", methods=["GET","POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        email_or_phone = request.form["contact"]

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        phone_pattern = r"^(?:\+8801|8801|01)[3-9]\d{8}$"

        if not re.match(email_pattern, email_or_phone) and not re.match(phone_pattern, email_or_phone):
            error = "Enter valid Email or  phone number"
            return render_template("register.html", error=error)

        conn = get_db()

        conn.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            (username,password)
        )

        conn.commit()

        return redirect("/login")

    return render_template("register.html", error=error)


# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM job_posts")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_posts WHERE result LIKE '%Fraud%'")
    fraud = cursor.fetchone()[0]

    real = total - fraud

    if total > 0:
        accuracy = round((real / total) * 100)
    else:
        accuracy = 0

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        fraud=fraud,
        real=real,
        accuracy=accuracy
    )

# ---------------- Job Submission ----------------
@app.route("/submit-job", methods=["GET", "POST"])
def submit():

    if "user" not in session:
        return redirect("/login")

    result = None
    processed_text = None

    if request.method == "POST":

        title = request.form["title"]
        company = request.form["company"]
        job_text = request.form["job"]
        salary = request.form["salary"]
        job_type = request.form["type"]

        processed_text = preprocess_text(job_text)

        result = predict_fraud(processed_text)

        # Save to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO job_posts(title, company, description, salary, type, result)
        VALUES(?,?,?,?,?,?)
        """,(title, company, job_text, salary, job_type, result))

        conn.commit()
        conn.close()

    return render_template(
        "submit_job.html",
        result=result,
        processed=processed_text
    )


# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
