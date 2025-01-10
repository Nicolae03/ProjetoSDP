class Ticket:
    def __init__(self, event_name, ticket_type, price, quantity):
        self.event_name = event_name
        self.ticket_type = ticket_type
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "event_name": self.event_name,
            "ticket_type": self.ticket_type,
            "price": self.price,
            "quantity": self.quantity
        }
