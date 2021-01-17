import psycopg2 as db_event
import os

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

def check_img_name(img_name):
    extension = os.path.splitext(img_name)[1]
    ext_list = [".png", ".jpg", ".jpeg"]
    l = {}
    if extension not in ext_list:
        l["file"] = "Disallowed file type."

    return l

def upload_update_img(email, user_img, dsn):
    l = {}
    new_img_exists = False

    if user_img:
        l = check_img_name(user_img.filename)
        if len(l) != 0:
            return l
        new_img_exists = True
    else:
        print("no img given")


    command_img =  "SELECT EXISTS(SELECT 1 FROM user_img WHERE email=%s)"
    command_insert = "INSERT INTO user_img(email, img) VALUES(%s, %s)"
    command_delete = "DELETE FROM user_img WHERE email=%s"
    command_update = "UPDATE user_img SET img=%s WHERE email=%s"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_img, (email,)) #check if image exist on database
        img_exists = bool(curr.fetchone()[0])

        print("img", new_img_exists)
        print("db_img", img_exists)

        if new_img_exists and img_exists:
            print("update")
            curr.execute(command_update, (user_img.read(), email,)) #update img
        elif img_exists:
            print("delete")
            curr.execute(command_delete, (email,)) #delete row
        elif new_img_exists:
            print("insert")
            curr.execute(command_insert, (email, user_img.read(),)) #insert row
        else:
            print("nothing")
        
        curr.close()
        connection.commit()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
        print("db_error")
        print(error)
    finally:
        if connection is not None:
            connection.close()

    return l