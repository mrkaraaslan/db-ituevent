from db_py.event import Event

class Database:
    def __init__(self):
        self.my_events = []
        self.attended_events = []
        self.search_events = []

    def create_event(self, event):
        self.my_events.append(event)

    def delete_event(self, event_id):
        index = next(i for i, x in enumerate(self.my_events) if x.id == event_id)
        del self.my_events[index]