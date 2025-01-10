import bcrypt

class User:
    users_db = []  # Simulando um banco de dados em memória

    def __init__(self, username, email, password, balance=0.0):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.balance = balance  # Permite definir um saldo inicial opcional

    def save(self):
        User.users_db.append(self)

    @classmethod
    def find_by_username(cls, username):
        for user in cls.users_db:
            if user.username == username:
                return user
        return None

    @classmethod
    def find_by_email(cls, email):
        for user in cls.users_db:
            if user.email == email:
                return user
        return None

    @classmethod
    def verify_password(cls, hashed_password, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "balance": self.balance
        }
