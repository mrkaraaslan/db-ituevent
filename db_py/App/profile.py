import psycopg2 as db_event
from base64 import b64encode

class ShowUser:
    def __init__(self, email):
        self.img = None
        self.email = email
        self.user_name = ""
        self.edu_level = ""
        self.department = ""
        self.about_me = ""
    
    def get_data(self, dsn):

        command_user = "SELECT EXISTS(SELECT 1 FROM security WHERE email=%s)"
        command_data = "SELECT user_name, levels.name, departments.name, about_me, user_img.img_name, user_img.img FROM users LEFT JOIN levels ON edu_level=levels.id LEFT JOIN departments ON department=departments.id LEFT JOIN user_img ON users.email=user_img.email WHERE users.email=%s"

        l = {}
        connection = None
        try:
            connection = db_event.connect(**dsn)
            curr = connection.cursor()
            (curr.execute(command_user, (self.email,)))

            user_exists = bool(curr.fetchone()[0])

            if not user_exists:
                l["user"] = "USER DOES NOT EXISTS!"
                print("NOOO")
            else:
                curr.execute(command_data, (self.email,))
                data = curr.fetchone()
                curr.close()

                self.user_name = data[0]
                self.edu_level = data[1]
                self.department = data[2]
                self.about_me = data[3]
                if data[4] and data[5]:
                    self.img = {}
                    self.img["img_name"] = data[4]
                    self.img["img"] = b64encode(data[5]).decode("utf-8")
        except (Exception, db_event.DatabaseError) as error:
            l["err"] = "Database Error"
            l["db_message"] = error
            print("get user error", error)
        finally:
            if connection is not None:
                connection.close()

        return l

        