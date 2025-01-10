class Event:
    def __init__(self, name, description, seats, location):
        self.name = name
        self.description = description
        self.seats = seats
        self.location = location

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "seats": self.seats,
            "location": self.location
        }
