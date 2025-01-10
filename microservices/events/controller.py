from flask import Blueprint, request, jsonify
from model import Event

event_controller = Blueprint('event_controller', __name__)

# Banco de dados em memória para eventos
events_db = []

# Rota para criar um novo evento (POST)
@event_controller.route("/events", methods=["POST"])
def create_event():
    """Cria um novo evento."""
    data = request.json

    # Verificar se os dados obrigatórios estão presentes
    if not all(key in data for key in ("name", "description", "seats", "location")):
        return jsonify({"message": "Invalid data"}), 400

    try:
        seats = int(data["seats"])
        if seats <= 0:
            return jsonify({"message": "Seats must be greater than zero"}), 400

        # Verifica se o evento já existe
        if any(event.name.lower() == data["name"].strip().lower() for event in events_db):
            return jsonify({"message": "Event already exists"}), 400

        # Criar e salvar o novo evento
        event = Event(data["name"], data["description"], seats, data["location"])
        events_db.append(event)
        return jsonify({"message": "Event created successfully!"}), 201
    except ValueError:
        return jsonify({"message": "Seats must be a valid integer"}), 400

# Rota para listar todos os eventos (GET)
@event_controller.route("/events", methods=["GET"])
def list_events():
    """Lista todos os eventos."""
    return jsonify([event.to_dict() for event in events_db]), 200
