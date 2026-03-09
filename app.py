from flask import Flask, render_template, request
import smtplib
import os

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
        print("Email failed:", e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/choose", methods=["POST"])
def choose():
    choice = request.form["choice"]

    send_email(choice)

    return f"Thanks for choosing {choice} 😊"


if __name__ == "__main__":
    app.run()