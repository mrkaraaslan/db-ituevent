import psycopg2 as db_event
from base64 import b64encode

def get_event_details(event_id, dsn):
    l = {}
    s_event = {}
    command_event = "SELECT EXISTS(SELECT 1 FROM event WHERE id=%s)"
    command_data = "SELECT creator_email, name, talker, start_date, start_time, max_participants, price, address, description, img FROM event LEFT JOIN event_img ON event.id=event_img.event_id WHERE id=%s"
    
    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_event, (event_id,))
        event_exists = bool(curr.fetchone()[0])

        if event_exists:
            curr.execute(command_data, (event_id,))
            e = curr.fetchone()
            curr.close()
            try:
                img = b64encode(e[9]).decode("utf-8")
            except:
                img = None

            s_event = {"creator_email":e[0], "name":e[1], "talker":e[2], "start_date":e[3], "start_time":e[4], "max_participants":e[5], "price":e[6], "address":e[7], "description":e[8], "img":img}
        else:
            l["abort"] = "abort"
        
        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "get_event_details Error"
        l["db_message"] = error
        print(error)
    finally:
        if connection is not None:
            connection.close()
    
    return l, s_event

def add_to_schedule(email, event_id, dsn):
    l = {}
    command = "INSERT INTO attendence(email, event_id) VALUES(%s, %s)"
    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command, (email, event_id,))
        curr.close()
        connection.commit()
        l['success'] = "Successfull added to Schedule"
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "add_to_schedule Error"
        l["db_message"] = error
        print(error)
    finally:
        if connection is not None:
            connection.close()
    
    return l

def remove_from_schedule(email, event_id, dsn):
    l = {}
    command = "DELETE FROM attendence WHERE email=%s AND event_id=%s"
    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command, (email, event_id,))
        curr.close()
        connection.commit()
        l['success'] = "Successfull removed from Schedule"
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "remove_from_schedule Error"
        l["db_message"] = error
        print(error)
    finally:
        if connection is not None:
            connection.close()
    
    return l