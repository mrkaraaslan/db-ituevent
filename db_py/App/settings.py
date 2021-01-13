import psycopg2 as db_event

def get_levels(dsn):
    l = {}
    levels = []

    command = "SELECT name FROM levels"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command)
        levels = curr.fetchall()
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["level"] = "Database Error"
        l["level_message"] = error
    finally:
        if connection is not None:
            connection.close()
    
    return l, levels

def get_departments(dsn):
    l = {}
    departments = []

    command = "SELECT name FROM departments"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command)
        departments = curr.fetchall()
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["dep"] = "Database Error"
        l["dep_message"] = error
    finally:
        if connection is not None:
            connection.close()
    
    return l, departments


def update_profile(email, name, edu_level, department, about_me, dsn):
    l = {}

    command = "UPDATE users SET user_name=%s, edu_level=(SELECT id FROM levels WHERE name=%s), department=(SELECT id FROM departments WHERE name=%s), about_me=%s WHERE email=%s"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command, (name, edu_level, department, about_me, email,))
        curr.close()
        connection.commit()
        l["success"] = "Update succesfully complete"
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()
    
    return l

