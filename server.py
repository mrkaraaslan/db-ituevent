from flask import Flask
from flask_login import LoginManager

import pages
from database import Database
from event import Event

from _py.user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(email):
    return get_user(email)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/sign_in", view_func=pages.sign_in_page, methods=["GET","POST"])
    app.add_url_rule("/sign_up", view_func=pages.sign_up_page, methods=["GET","POST"])
    app.add_url_rule("/forgot_password", view_func=pages.forgot_password_page)
    app.add_url_rule("/logout", view_func=pages.logout_page)

    app.add_url_rule("/", view_func=pages.search_events_page)
    app.add_url_rule("/attended_events", view_func=pages.attended_events_page)
    app.add_url_rule("/profile", view_func=pages.profile_page)
    app.add_url_rule("/settings", view_func=pages.settings_page)
    app.add_url_rule("/my_events", view_func=pages.my_events_page)
    app.add_url_rule("/create_event", view_func=pages.create_event_page)

    lm.init_app(app)
    lm.login_view = "sign_in_page"

    db = Database()
    app.config["db"] = db

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT")
    debug = app.config.get("DEBUG")
    app.run(host="0.0.0.0", port=port, debug=debug)