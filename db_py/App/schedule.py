import psycopg2 as db_event
from base64 import b64encode

def get_schedule(email, dsn):
    l = {}
    event_list = []

    command_event = "SELECT attendence.event_id, name, talker, start_date, start_time, max_participants, price, img FROM attendence LEFT JOIN event ON attendence.event_id=event.id LEFT JOIN event_img ON attendence.event_id=event_img.event_id WHERE email=%s ORDER BY start_date ASC"

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        curr.execute(command_event, (email,))
        events = curr.fetchall()
        for e in events:
            try:
                img = b64encode(e[7]).decode("utf-8")
            except:
                img = None
            
            new_event = {"id":e[0], "name":e[1], "talker":e[2], "start_date":e[3], "start_time":e[4], "max_participants":e[5], "price":e[6], "img":img}
            event_list.append(new_event)

        curr.close()
    except (Exception, db_event.DatabaseError) as error:
        l["err"] = "get_schedule_error"
        l["db_message"] = error
        print("get_schedule_error", error)
    finally:
        if connection is not None:
            connection.close()

    return l, event_list