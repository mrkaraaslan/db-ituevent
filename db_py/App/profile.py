import psycopg2 as db_event

class ShowUser:
    def __init__(self, email):
        self.img = ""  #how will I store image
        self.email = email
        self.user_name = ""
        self.edu_level = ""
        self.department = ""
        self.about_me = ""
    
    def get_data(self, dsn):

        command_user = "SELECT EXISTS(SELECT 1 FROM security WHERE email=%s)"
        command_data = "SELECT user_name, edu_level, department, about_me FROM users WHERE email=%s"

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
        except (Exception, db_event.DatabaseError) as error:
            l["err"] = "Database Error"
            l["db_message"] = error
        finally:
            if connection is not None:
                connection.close()

        return l

        