from hashlib import sha256
import psycopg2 as db_event

def create_hash(password):
    pw_bytestring = password.encode()
    return str(sha256(pw_bytestring).hexdigest())

def controller(email, pass1, pass2):
    errors = {}

    l11 = email[-10:]

    if l11 != "itu.edu.tr":
        errors["email"] = "INVALID EMAIL ADDRESS"
    elif pass1 != pass2:
        errors["password"] = "PASSWORDS DO NOT MATCH"
    
    return errors

def sign_up(email, password, dsn):
    l = {}

    command_user = "INSERT INTO users(email) VALUES(%s)"
    command_security = "INSERT INTO security(email, password) VALUES(%s,%s)"

    connection = None
    hashed_password = create_hash(password)
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_user, (email,))
        curr.execute(command_security, (email, hashed_password))
        curr.close()
        connection.commit()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()
    
    return l