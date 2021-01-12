from hashlib import sha256
import psycopg2 as db_event
from flask_login import current_user

def create_hash(password):
    pw_bytestring = password.encode()
    return str(sha256(pw_bytestring).hexdigest())

def controller(password, pass1, pass2):
    err = {}
    password = create_hash(password)
    if password == current_user.password:
        if pass1 != pass2:
            err["news"] = "PASSWORDS DO NOT MATCH!"
    else:
        err["pass"] = "WRONG PASSWORD"
    
    return err

def change_password(password, dsn):
    l = {}
    password = create_hash(password)
    email = current_user.email

    command = "UPDATE security Set password=%s WHERE email =%s"
    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        (curr.execute(command, (password,email)))
        curr.close()
        connection.commit()
        l["success"] = "Password is successfully updated."
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()

    return l

