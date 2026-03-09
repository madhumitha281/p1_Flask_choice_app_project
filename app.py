from flask import Flask, render_template, request, jsonify
import smtplib
import os
import sqlite3

app = Flask(__name__)

# Load email credentials from environment
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD environment variables must be set")

DB_PATH = "votes.db"

# ----------------- Database Setup -----------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                choice TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

# ----------------- Email Function -----------------
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
            print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)

# ----------------- Routes -----------------
@app.route("/")
def home():
    return render_template("index.html")  # Make sure this exists in templates folder

@app.route("/choose", methods=["POST"])
def choose():
    choice = request.form.get("choice")
    if not choice:
        return "No choice selected", 400

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO votes (choice) VALUES (?)", (choice,))
            conn.commit()
    except Exception as e:
        return f"Database error: {e}", 500

    # Send email notification (optional, remove if not needed)
    send_email(choice)

    return f"Thanks for choosing {choice} 😊"

@app.route("/results")
def results():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT choice, COUNT(*) FROM votes GROUP BY choice")
            data = c.fetchall()
            results_dict = {choice: count for choice, count in data}
            return jsonify(results_dict)
    except Exception as e:
        return f"Database error: {e}", 500

# ----------------- Main -----------------
if __name__ == "__main__":
    # Development mode, reloads automatically on code changes
    app.run(debug=True, host="0.0.0.0", port=5000)