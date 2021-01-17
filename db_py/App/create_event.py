import psycopg2 as db_event
import os

def check_img_name(img_name):
    extension = os.path.splitext(img_name)[1]
    ext_list = [".png", ".jpg", ".jpeg"]
    l = {}
    if extension not in ext_list:
        l["file"] = "Disallowed file type."

    return l

def controller(n): # n: new_event
    l = {}

    if n["name"] == "":
        l["name"] = "GIVE YOUR EVENT A NAME!"
    if n["date"] == "":
        l["date"] = "GIVE YOUR EVENT A DATE!"
    if n["time"] == "":
        l["time"] = "GIVE YOUR EVENT A TIME!"
    if n["max_participants"]:
        if n["max_participants"] < 1:
            l["max_participants"] = "VALUE MUST BE AT LEAST 1!"
    if n["price"]:
        if n["price"] < 1:
            l["price"] = "VALUE MUST BE AT LEAST 1!"
    if n["img"]:
        l = check_img_name(n["img"].filename)
    return l

def create_event(n, dsn): # n: new_event
    l = {}
    event_id = None

    command_event = """INSERT INTO event(
        creator_email, name, talker, start_date, start_time, max_participants, price, address, description) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""
    
    command_image = "INSERT INTO event_img(event_id, img) VALUES(%s, %s)"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_event, (n["creator_email"], n["name"], n["talker"], n["date"], n["time"], n["max_participants"], n["price"], n["address"], n["description"],))
        event_id = curr.fetchone()[0]
        if n["img"]:
            curr.execute(command_image, (event_id, n["img"].read()))
        curr.close()
        connection.commit()
        l['success'] = "Successfully created new event."
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Database Error"
        l["db_message"] = error
        print(error)
    finally:
        if connection is not None:
            connection.close()

    return l