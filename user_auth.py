import requests

# Endereço base do serviço de usuários
USER_SERVICE_URL = "http://localhost:5002"
REGISTER_URL = f"{USER_SERVICE_URL}/users/register"
LOGIN_URL = f"{USER_SERVICE_URL}/users/login"
ADD_MONEY_URL = f"{USER_SERVICE_URL}/users/add_money"

# Variável para armazenar o usuário logado
current_user = None

def menu():
    """Exibe o menu principal."""
    while True:
        print("\n=== Sistema de Autenticação ===")
        print("1. Registrar novo usuário")
        print("2. Fazer login")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            registrar_usuario()
        elif escolha == "2":
            fazer_login()
        elif escolha == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def registrar_usuario():
    """Registra um novo usuário no sistema."""
    username = input("\nDigite seu nome de usuário: ")
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")

    payload = {"username": username, "email": email, "password": password}
    try:
        response = requests.post(REGISTER_URL, json=payload)
        if response.status_code == 201:
            print("\nUsuário registrado com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Email já registrado ou dados inválidos.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def fazer_login():
    """Realiza o login de um usuário."""
    global current_user  # Declarar como global antes de qualquer uso
    email = input("\nDigite seu email: ")
    password = input("\nDigite sua senha: ")

    payload = {"email": email, "password": password}
    try:
        response = requests.post(LOGIN_URL, json=payload)
        if response.status_code == 200:
            print("\nLogin bem-sucedido!")
            current_user = email  # Armazena o email do usuário logado
            menu_logado()
        elif response.status_code == 401:
            print("\nErro: Email ou senha inválidos.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def menu_logado():
    """Exibe o menu para o usuário logado."""
    global current_user  # Declarar como global antes de modificar a variável
    while True:
        print(f"\n=== Bem-vindo, {current_user} ===")
        print("1. Adicionar dinheiro à conta")
        print("2. Fazer logout")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            adicionar_dinheiro()
        elif escolha == "2":
            print("\nLogout realizado com sucesso!")
            current_user = None  # Limpa a variável global ao fazer logout
            break
        else:
            print("Opção inválida. Tente novamente.")

def adicionar_dinheiro():
    """Permite ao usuário adicionar dinheiro à conta."""
    try:
        amount = float(input("\nDigite o valor a ser adicionado: "))
        if amount <= 0:
            print("O valor deve ser maior que zero.")
            return

        payload = {"email": current_user, "amount": amount}
        response = requests.post(ADD_MONEY_URL, json=payload)
        if response.status_code == 200:
            print(f"\n{amount:.2f} adicionados com sucesso à sua conta!")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:  
        print("Por favor, insira um valor numérico.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

if __name__ == "__main__":
    menu()
