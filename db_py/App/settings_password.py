from hashlib import sha256
import psycopg2 as db_event
from flask_login import current_user

def create_hash(password):
    pw_bytestring = password.encode()
    return str(sha256(pw_bytestring).hexdigest())

def controller(password, pass1, pass2, dsn):
    err = {}
    password = create_hash(password)

    err, db_pass = get_password(dsn)
    if len(err) == 0:
        if password == db_pass:
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

def get_password(dsn):
    email = current_user.email
    command = "SELECT password FROM security WHERE email=%s"
    connection = None
    db_pass = None
    l = {}
    
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        (curr.execute(command, (email,)))

        db_pass = str(curr.fetchone()[0])
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()

    return l, db_pass