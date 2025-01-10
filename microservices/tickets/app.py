from flask import Flask
from controller import ticket_controller

app = Flask(__name__)

# Rota principal
app.register_blueprint(ticket_controller)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)

