from hashlib import sha256
import psycopg2 as db_event

def create_hash(password):
    pw_bytestring = password.encode()
    return str(sha256(pw_bytestring).hexdigest())


def controller(email, password):
    errors = {}

    l11 = email[-10:]
    if l11 != "itu.edu.tr":
        errors["email"] = "INVALID EMAIL ADDRESS"
    elif password == "":
        errors["password"] = "WRITE YOUR PASSWORD"
    
    return errors

def sign_in(email, password, dsn):
    l = {}

    command_user = "SELECT EXISTS(SELECT 1 FROM security WHERE email=%s)"
    command_password = "SELECT password FROM security WHERE email=%s"

    connection = None
    hashed_password = create_hash(password)
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        (curr.execute(command_user, (email,)))

        user_exists = bool(curr.fetchone()[0])
        if not user_exists:
            l["email"] = "USER DOES NOT EXISTS!"
        else:
            curr.execute(command_password, (email,))
            db_pass = str(curr.fetchone()[0])
            curr.close()

            if hashed_password != db_pass:
                l["password"] = "WRONG PASSWORD"
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()

    return l