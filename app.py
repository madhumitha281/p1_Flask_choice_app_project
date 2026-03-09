from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/choose", methods=["POST"])
def choose():
    choice = request.form["choice"]
    return f"Thanks for choosing {choice} 😊"

if __name__ == "__main__":
    app.run(debug=True)