from flask import Blueprint, request, jsonify
from model import User

user_controller = Blueprint('user_controller', __name__)

# Rota para listar todos os usuários (GET)
@user_controller.route("/users", methods=["GET"])
def list_users():
    users = [user.to_dict() for user in User.users_db]
    return jsonify(users), 200

# Rota para registrar novo usuário (POST)
@user_controller.route("/users/register", methods=["POST"])
def register_user():
    data = request.json

    # Verificar se o email já está registrado
    if User.find_by_email(data['email']):
        return jsonify({"message": "User already exists"}), 400

    # Criar e salvar o novo usuário com saldo inicial zero
    user = User(data['username'], data['email'], data['password'], balance=0)
    user.save()
    return jsonify({"message": "User registered successfully!"}), 201

# Rota para fazer login (POST)
@user_controller.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    user = User.find_by_email(data['email'])

    if not user or not User.verify_password(user.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": f"Welcome {user.username}!"}), 200

# Rota para adicionar dinheiro à conta do usuário (POST)
@user_controller.route("/users/add_money", methods=["POST"])
def add_money():
    data = request.json
    user = User.find_by_email(data['email'])

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"message": "Amount must be greater than zero"}), 400
        user.balance += amount
        return jsonify({"message": f"{amount:.2f} added to account"}), 200
    except (ValueError, KeyError):
        return jsonify({"message": "Invalid amount"}), 400

# Rota para deduzir saldo do usuário (POST)
@user_controller.route("/users/deduct_balance", methods=["POST"])
def deduct_balance():
    data = request.json
    user = User.find_by_email(data['email'])

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"message": "Amount must be greater than zero"}), 400

        if user.balance < amount:
            return jsonify({"message": "Insufficient balance"}), 400

        user.balance -= amount
        return jsonify({"message": "Balance deducted successfully"}), 200
    except (ValueError, KeyError):
        return jsonify({"message": "Invalid amount"}), 400

# Rota para obter um usuário específico por email (GET)
@user_controller.route("/users/<email>", methods=["GET"])
def get_user(email):
    user = User.find_by_email(email)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

