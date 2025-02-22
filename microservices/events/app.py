from flask import Flask
from controller import event_controller

app = Flask(__name__)

# Rota principal
app.register_blueprint(event_controller)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)