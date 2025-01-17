from flask import Blueprint, request, jsonify
from model import Payment
import requests

payment_controller = Blueprint('payment_controller', __name__)

# Banco de dados em memória para pagamentos
payments_db = []

# Endereço do serviço de usuários e bilhetes no Kubernetes
"""USER_SERVICE_URL = "http://users-service/users"
TICKET_SERVICE_URL = "http://tickets-service/tickets""""
#Prof. Inês Almeida - Neste momento, o url certo é com o localhost,
#depois quando ativarem o Kubernetes por completo é que voltam a utilizar o url que tinham
USER_SERVICE_URL = "http://localhost:5002/users"
TICKET_SERVICE_URL = "http://localhost:5004/tickets"
#Prof.Inês Almeida: Com alteração do prefix no app.py foi necessário alterar /payments para /
# Rota para listar todos os pagamentos (GET)
@payment_controller.route("/", methods=["GET"])
def list_payments():
    """Lista todos os pagamentos registrados."""
    return jsonify([payment.to_dict() for payment in payments_db]), 200

# Rota para processar pagamentos (POST)
@payment_controller.route("/", methods=["POST"])
def process_payment():
    data = request.json

    # Verificar se os dados obrigatórios estão presentes
    if not all(key in data for key in ("user_email", "event_name", "ticket_type", "quantity")):
        return jsonify({"message": "Invalid data"}), 400

    try:
        quantity = int(data["quantity"])
        if quantity <= 0:
            return jsonify({"message": "Quantity must be greater than zero"}), 400

        # Consultar o preço do bilhete
        ticket_price = get_ticket_price(data["event_name"], data["ticket_type"])
        if ticket_price is None:
            return jsonify({"message": "Ticket not found"}), 404

        total_price = ticket_price * quantity

        # Verificar saldo do usuário
        if not check_user_balance(data["user_email"], total_price):
            return jsonify({"message": "Insufficient balance"}), 400

        # Deduzir o saldo do usuário
        if not deduct_user_balance(data["user_email"], total_price):
            return jsonify({"message": "Failed to deduct balance"}), 500

        # Criar e salvar o novo pagamento
        payment = Payment(data["user_email"], data["event_name"], data["ticket_type"], quantity, total_price)
        payments_db.append(payment)
        return jsonify(payment.to_dict()), 200
    except ValueError:
        return jsonify({"message": "Quantity must be a valid integer"}), 400


def get_ticket_price(event_name, ticket_type):
    """Consulta o preço do bilhete no microserviço de bilhetes."""
    try:
        response = requests.get(TICKET_SERVICE_URL)
        if response.status_code == 200:
            tickets = response.json()
            print("\n=== Bilhetes recebidos da API ===")
            print(tickets)  # Log para verificar os bilhetes recebidos
            #Prof. Inês Almeida - Fizeram bem em converter os inputs para minusculas,
            #Mas para além disso também devem ter em atenção com os caracteres especiais
            #Pois temos garantir ao máximo que os nomes são examente iguais, por isso troquei o lower por casefold. Pois o casefold faz 2 em 1, 
            #para além de converter em minusculas  como o lower() tambem converte caracteres especiais
            #É preciso ter muito cuidado com os inputs pois basta um caracter errada para que o bilhete não seja encontrada.
            #event_name_input = event_name.strip().lower()
            #ticket_type_input = ticket_type.strip().lower()
            event_name_input = event_name.strip().casefold()
            ticket_type_input = ticket_type.strip().casefold()

            for ticket in tickets:
                #event_name_api = ticket["event_name"].strip().lower()
                #ticket_type_api = ticket["ticket_type"].strip().lower()
                event_name_api = ticket["event_name"].strip().lower().casefold()
                ticket_type_api = ticket["ticket_type"].strip().lower().casefold()
                
                # Log detalhado da comparação
                print(f"Comparando entrada: evento='{event_name_input}', tipo='{ticket_type_input}' "
                      f"com evento da API='{event_name_api}', tipo da API='{ticket_type_api}'")

                if event_name_input == event_name_api and ticket_type_input == ticket_type_api:
                    print(f"Bilhete encontrado: {ticket}")
                    return float(ticket["price"])

        print("\nBilhete não encontrado após a comparação.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao serviço de bilhetes: {e}")
        return None


def check_user_balance(user_email, total_price):
    """Verifica se o usuário tem saldo suficiente para a compra."""
    try:
        response = requests.get(f"{USER_SERVICE_URL}/{user_email}")
        if response.status_code == 200:
            user = response.json()
            return user["balance"] >= total_price
        return False
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao serviço de usuários: {e}")
        return False


def deduct_user_balance(user_email, total_price):
    """Deduz o saldo do usuário."""
    try:
        response = requests.post(f"{USER_SERVICE_URL}/deduct_balance", json={"email": user_email, "amount": total_price})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao serviço de usuários: {e}")
        return False
