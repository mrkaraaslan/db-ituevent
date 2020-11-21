from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def sign_in_page():
    return render_template("Sign/sign_in.html")

@app.route("/sign_up")
def sign_up_page():
    return render_template("Sign/sign_up.html")

@app.route("/forgot_password")
def forgot_password_page():
    return render_template("Sign/forgot_password.html")

@app.route("/search_events")
def search_events_page():
    return render_template("App/search_events.html")

@app.route("/attended_events")
def attended_events_page():
    return render_template("App/attended_events.html")

@app.route("/profile")
def profile_page():
    return render_template("App/profile.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)