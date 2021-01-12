from flask import current_app
from flask_login import UserMixin
import psycopg2 as db_event

class User(UserMixin):
    def __init__(self, email):
        self.email = email
        self.password = ""
        self.active = True
    
    def get_id(self):
        return self.email
    
    @property
    def is_active(self):
        return self.active

def get_user(email, params):
    user = User(email)
    user.password = get_password(email, params)
    return user

def get_password(email, dsn):
    command = "SELECT password FROM security WHERE email=%s"
    connection = None

    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        (curr.execute(command, (email,)))

        db_pass = str(curr.fetchone()[0])
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

    return db_pass