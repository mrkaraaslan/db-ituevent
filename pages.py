from flask import render_template

#sign pages
def sign_in_page():
    return render_template("Sign/sign_in.html")

def sign_up_page():
    return render_template("Sign/sign_up.html")

def forgot_password_page():
    return render_template("Sign/forgot_password.html")

#app pages
def search_events_page():
    return render_template("App/search_events.html", user_name= "Mehmet Karaaslan")

def attended_events_page():
    return render_template("App/attended_events.html", user_name= "Mehmet Karaaslan")

def profile_page():
    return render_template("App/profile.html", user_name= "Mehmet Karaaslan")

def settings_page():
    return render_template("App/settings.html", user_name="Mehmet Karaaslan")

def my_events_page():
    return render_template("App/my_events.html", user_name= "Mehmet Karaaslan")