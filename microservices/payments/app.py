from flask import Flask
from controller import payment_controller

app = Flask(__name__)

# Rota principal
#Prof. Inês Almeida - É necessário especificar o prefixo da rota
#app.register_blueprint(payment_controller)
app.register_blueprint(payment_controller, url_prefix="/payments")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)

