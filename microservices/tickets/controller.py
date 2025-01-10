from flask import Blueprint, request, jsonify
from model import Ticket

ticket_controller = Blueprint('ticket_controller', __name__)

# Banco de dados em memória para bilhetes
tickets_db = []

# Rota para criar bilhetes (POST)
@ticket_controller.route("/tickets", methods=["POST"])
def create_ticket():
    """Cria um novo bilhete."""
    data = request.json

    # Verificar se os dados obrigatórios estão presentes
    if not all(key in data for key in ("event_name", "ticket_type", "price", "quantity")):
        return jsonify({"message": "Invalid data"}), 400

    try:
        price = float(data["price"])
        quantity = int(data["quantity"])
        if price <= 0 or quantity <= 0:
            return jsonify({"message": "Price and quantity must be greater than zero"}), 400

        # Criar e salvar o novo bilhete
        ticket = Ticket(data["event_name"], data["ticket_type"], price, quantity)
        tickets_db.append(ticket)
        return jsonify({"message": "Ticket created successfully!"}), 201
    except ValueError:
        return jsonify({"message": "Price and quantity must be valid numbers"}), 400

# Rota para listar todos os bilhetes (GET)
@ticket_controller.route("/tickets", methods=["GET"])
def list_tickets():
    """Lista todos os bilhetes."""
    return jsonify([ticket.to_dict() for ticket in tickets_db]), 200
