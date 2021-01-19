import psycopg2 as db_event
import os
from base64 import b64encode

def get_event(email, event_id, dsn):
    l = {}
    s_event = {}
    command_event = "SELECT EXISTS(SELECT 1 FROM event WHERE creator_email=%s AND id=%s)"
    command_data = "SELECT name, talker, start_date, start_time, max_participants, price, address, description, img FROM event LEFT JOIN event_img ON event.id=event_img.event_id WHERE creator_email=%s AND id=%s"
    
    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_event, (email, event_id,))
        event_exists = bool(curr.fetchone()[0])

        if event_exists:
            curr.execute(command_data, (email, event_id,))
            e = curr.fetchone()
            curr.close()
            try:
                img = b64encode(e[8]).decode("utf-8")
            except:
                img = None

            s_event = {"name":e[0], "talker":e[1], "start_date":e[2], "start_time":e[3], "max_participants":e[4], "price":e[5], "address":e[6], "description":e[7], "img":img}
        else:
            l["abort"] = "abort"
        
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Get Event Error"
        l["db_message"] = error
        print(error)
    finally:
        if connection is not None:
            connection.close()
    
    return l, s_event

def controller_before_update(e): # e: event
    l = {}

    if e["name"] == "":
        l["name"] = "GIVE YOUR EVENT A NAME!"
    if e["date"] == "":
        l["date"] = "GIVE YOUR EVENT A DATE!"
    if e["time"] == "":
        l["time"] = "GIVE YOUR EVENT A TIME!"
    if e["max_participants"]:
        if e["max_participants"] < 1:
            l["max_participants"] = "VALUE MUST BE AT LEAST 1!"
    if e["price"]:
        if e["price"] < 1:
            l["price"] = "VALUE MUST BE AT LEAST 1!"
    return l

def check_img_name(img_name):
    extension = os.path.splitext(img_name)[1]
    ext_list = [".png", ".jpg", ".jpeg"]
    l = {}
    if extension not in ext_list:
        l["file"] = "Disallowed file type."

    return l

def update_event_img(event_id, event_img, dsn):
    l = {}
    new_img_exists = False

    if event_img:
        l = check_img_name(event_img.filename)
        if len(l) != 0:
            return l
        new_img_exists = True


    command_img =  "SELECT EXISTS(SELECT 1 FROM event_img WHERE event_id=%s)"
    command_insert = "INSERT INTO event_img(event_id, img) VALUES(%s, %s)"
    command_delete = "DELETE FROM event_img WHERE event_id=%s"
    command_update = "UPDATE event_img SET img=%s WHERE event_id=%s"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_img, (event_id,)) #check if image exist on database
        img_exists = bool(curr.fetchone()[0])

        if new_img_exists and img_exists:
            curr.execute(command_update, (event_img.read(), event_id,)) #update img
        elif img_exists:
            curr.execute(command_delete, (event_id,)) #delete row
        elif new_img_exists:
            curr.execute(command_insert, (event_id, event_img.read(),)) #insert row
        
        curr.close()
        connection.commit()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Update Event Image Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()

    return l

def update_event(email, e, dsn):
    l = {}

    command = "UPDATE event SET name=%s, talker=%s, start_date=%s, start_time=%s, max_participants=%s, price=%s, address=%s, description=%s WHERE id=%s AND creator_email=%s"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command, (e["name"], e["talker"], e["date"], e["time"], e["max_participants"], e["price"], e["address"], e["description"], e['id'], email,))
        curr.close()
        connection.commit()
        l["success"] = "Update succesfully complete"
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "Update Event Error"
        l["db_message"] = error
    finally:
        if connection is not None:
            connection.close()
    
    return l