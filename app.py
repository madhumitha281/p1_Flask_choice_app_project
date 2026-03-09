from flask import Flask, render_template, request
import smtplib
import os
import sqlite3


app = Flask(__name__)

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def send_email(choice):
    subject = "Choice Selected"
    body = f"Someone selected: {choice}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, message)
            print("Email sent")

    except Exception as e:
        print("Email error:", e)

def init_db():
    conn = sqlite3.connect("votes.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        choice TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/choose", methods=["POST"])
def choose():
    choice = request.form["choice"]

    conn = sqlite3.connect("votes.db")
    c = conn.cursor()

    c.execute("INSERT INTO votes (choice) VALUES (?)", (choice,))
    conn.commit()
    conn.close()

    return f"Thanks for choosing {choice} 😊"

@app.route("/results")
def results():
    conn = sqlite3.connect("votes.db")
    c = conn.cursor()

    c.execute("SELECT choice, COUNT(*) FROM votes GROUP BY choice")
    data = c.fetchall()

    conn.close()

    return str(data)


if __name__ == "__main__":
    app.run()