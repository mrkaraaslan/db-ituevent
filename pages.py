from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from db_py.config import config
from db_py.user import get_user
from db_py.Sign import sign_in, sign_up
from db_py.App.profile import ShowUser
from db_py.App import settings_password
from db_py.App.settings import get_levels, get_departments, update_profile, upload_update_img


#sign pages
def sign_up_page():
    l = {}
    if request.method == "POST":
        email = request.form["inputEmail"]
        pass1 = request.form["inputPassword"]
        pass2 = request.form["inputPasswordAgain"]

        l = sign_up.controller(email, pass1, pass2)
        if len(l) == 0: #no errors
            params = config()
            l = sign_up.sign_up(email, pass1, params)
            if len(l) == 0:
                flash("Succesfully signed up.")
                return redirect(url_for("sign_in_page"))

    return render_template("Sign/sign_up.html", message_list = l)

def forgot_password_page():
    return render_template("Sign/forgot_password.html")

def sign_in_page():
    l = {}
    if request.method == "POST":
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        
        l = sign_in.controller(email, password)
        if len(l) == 0: #no errors
            params = config()
            l = sign_in.sign_in(email, password, params)
            if len(l) == 0:
                user = get_user(email)
                login_user(user)
                next_page = request.args.get("next", url_for("search_events_page"))
                if next_page == url_for("logout_page"):
                    next_page = url_for("search_events_page")
                return redirect(next_page)

    return render_template("Sign/sign_in.html", message_list = l)

@login_required
def logout_page():
    logout_user()
    flash("Succesfully logged out.")
    return redirect(url_for("sign_in_page"))

#app pages
@login_required
def search_events_page():
    return render_template("App/search_events.html")

@login_required
def attended_events_page():
    return render_template("App/attended_events.html")

@login_required
def profile_page(email):
    if not email:
        email = current_user.email
    show_user = ShowUser(email)
    params = config()
    l = show_user.get_data(params)
    return render_template("App/profile.html", show_user = show_user, message_list= l)

@login_required
def settings_page():
    email = current_user.email
    params = config()
    l = up = levels = departments = {}

    if request.method == "POST":
        img_name = request.form["img_name"]
        if img_name != "Choose Image: 'png', 'jpg', 'jpeg'":
            user_img = request.files["user_img"]
            up = upload_update_img(email, user_img, params)
        if len(up) == 0:
            name = request.form["inputName"]
            edu_level = request.form.get("level_select")
            department = request.form.get("department_select")
            about_me = request.form["about_me"]

            up = update_profile(email, name, edu_level, department, about_me, params)
    
    show_user = ShowUser(email)
    l = show_user.get_data(params)
    if len(l) == 0:
        l, levels = get_levels(params)
        if len(l) == 0:
            l, departments = get_departments(params)

    return render_template("App/settings.html", show_user = show_user, levels = levels, departments = departments, message_list = l, update_messages = up)

@login_required
def settings_password_page():
    l = {}
    if request.method == "POST":
        password = request.form["inputPassword"]
        pass1 = request.form["inputNewPassword"]
        pass2 = request.form["inputNewPasswordAgain"]
        params = config()
        
        l = settings_password.controller(password, pass1, pass2, params)
        if len(l) == 0:
            l = settings_password.change_password(pass1, params)

    return render_template("App/settings_password.html", message_list = l)

@login_required
def my_events_page():
    return render_template("App/my_events.html")

@login_required
def create_event_page():
    if request.method == "POST":
        return render_template("App/create_event.html")
        #name = request.form["name"]
        #talker = request.form["talker"]
        #date = request.form["date"]
        #time = request.form["time"]
        #maxparticipants = request.form["maxparticipants"]
        #price = request.form["price"]
        #address = request.form["address"]
        #description = request.form["description"]"""

    return render_template("App/create_event.html")
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