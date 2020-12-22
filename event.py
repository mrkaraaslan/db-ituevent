class Event:
    def __init__(self, creator_email, id, name, talker, create_date, start_date, end_date, max_participants, price, address, description):
        self.creator_email = creator_email
        self.id = id
        self.name = name
        self.talker = talker
        self.create_date = create_date
        self.start_date = start_date
        self.end_date = end_date
        self.max_participants = max_participants
        self.price = price
        self.address = address
        self.description = description