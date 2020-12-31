import psycopg2 as db_event

def create_tables(dsn):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users(
            email VARCHAR(255) NOT NULL UNIQUE,
            user_name VARCHAR(255),
            edu_level VARCHAR(255),
            department VARCHAR(255),
            about_me TEXT,
            PRIMARY KEY(email)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS security(
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            PRIMARY KEY(email),
            FOREIGN KEY(email) REFERENCES users(email)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_img(
            email VARCHAR(255) NOT NULL UNIQUE,
            img BYTEA NOT NULL ,
            PRIMARY KEY(email),
            FOREIGN KEY(email) REFERENCES users(email)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS event(
            creator_email VARCHAR (255) NOT NULL ,
            id SERIAL,
            name VARCHAR (255) NOT NULL,
            talker VARCHAR(255),
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            start_date DATE NOT NULL,
            start_time TIME NOT NULL,
            max_participants INT,
            price INT,
            address VARCHAR(255),
            description TEXT ,
            PRIMARY KEY(id),
            FOREIGN KEY(creator_email) REFERENCES users(email)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS event_img(
            event_id INT NOT NULL UNIQUE,
            img BYTEA NOT NULL,
            PRIMARY KEY(event_id),
            FOREIGN KEY(event_id) REFERENCES event(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS attendence(
            id SERIAL,
            email VARCHAR(255) NOT NULL,
            event_id INT NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY(email) REFERENCES users(email),
            FOREIGN KEY(event_id) REFERENCES event(id)
        );
        """
    )

    connection = None
    try:
        connection = db_event.connect(**dsn)
        curr = connection.cursor()
        for command in commands:
            curr.execute(command)

        curr.close()
        connection.commit()
    except (Exception, db_event.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()