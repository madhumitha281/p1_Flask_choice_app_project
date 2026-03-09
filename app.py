from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


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

# ----------------- Routes -----------------
@app.route("/")
def home():
    return render_template("index.html")  # Make sure this exists in templates folder

@app.route("/choose", methods=["POST"])
def choose():
    username = request.form.get("username")
    choice = request.form.get("choice")

    if not username or not choice:
        return "Name or choice missing", 400

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO votes (username, choice) VALUES (?, ?)",
                (username, choice)
            )
            conn.commit()
    except Exception as e:
        return f"Database error: {e}", 500

    # optional: send_email(choice)  # you can keep or remove
    return f"Thanks {username}, you chose {choice} 😊"

@app.route("/results")
def results():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT username, choice FROM votes")
            data = c.fetchall()

        # return JSON with username → choice
        results_dict = {username: choice for username, choice in data}
        return jsonify(results_dict)
    except Exception as e:
        return f"Database error: {e}", 500

# ----------------- Main -----------------
if __name__ == "__main__":
    # Development mode, reloads automatically on code changes
    app.run(debug=True, host="0.0.0.0", port=5000)