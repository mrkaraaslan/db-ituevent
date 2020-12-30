class Event:
    def __init__(self, creator_email, id, name, talker, create_date, date, time, max_participants, price, address, description):
        self.creator_email = creator_email
        self.id = id
        self.name = name
        self.talker = talker
        self.create_date = create_date
        self.date = date
        self.time = time
        self.max_participants = max_participants
        self.price = price
        self.address = address
        self.description = description