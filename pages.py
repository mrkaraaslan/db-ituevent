from flask import render_template, request
from datetime import datetime

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

def create_event_page():
    return render_template("App/create_event.html", user_name= "Mehmet Karaaslan")
"""
event_name = request.form["name"]
    event_talker = request.form["talker"]
    event_create_date = datetime.now()
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_max_participants = request.form["maxparticipants"]
    event_price = request.form["price"]
    event_address = request.form["address"]
    event_ = request.form[""]


    self.creator_email = ""
    self.id = ""
    self.name = ""
    self.talker = ""
    self.create_date = datetime.now()
    self.date = datetime.date()
    self.time = datetime.time()
    self.max_participants = 0
    self.price = 0
    self.address = ""
    self.description = ""
"""