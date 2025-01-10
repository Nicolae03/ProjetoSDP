class Payment:
    def __init__(self, user_email, event_name, ticket_type, quantity, total_price):
        self.user_email = user_email
        self.event_name = event_name
        self.ticket_type = ticket_type
        self.quantity = quantity
        self.total_price = total_price

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "event_name": self.event_name,
            "ticket_type": self.ticket_type,
            "quantity": self.quantity,
            "total_price": self.total_price
        }
