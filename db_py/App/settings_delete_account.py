from hashlib import sha256
import psycopg2 as db_event

def create_hash(password):
    pw_bytestring = password.encode()
    return str(sha256(pw_bytestring).hexdigest())


def delete_account(email, password, dsn):
    l = {}
    if email == "":
        l['password'] = "WRITE YOUR PASSWORD!"
        return l
    
    command_password = "SELECT password FROM security WHERE email=%s"
    command_delete = "DELETE FROM users WHERE email=%s"
    hashed_password = create_hash(password)

    connection = None
    hashed_password = create_hash(password)
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_password, (email,))
        db_pass = str(curr.fetchone()[0])
        
        if hashed_password != db_pass:
            l["password"] = "WRONG PASSWORD"
            return l
        
        curr.execute(command_delete, (email,))
        curr.close()
        connection.commit()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "delete_account error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()

    return l