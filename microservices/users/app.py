from flask import Flask
from controller import user_controller

app = Flask(__name__)

# Registro do Blueprint
app.register_blueprint(user_controller)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
