import requests

# Endereço base dos serviços
USER_SERVICE_URL = "http://localhost:5002"
TICKET_SERVICE_URL = "http://localhost:5004"
PAYMENT_SERVICE_URL = "http://localhost:5003"

LOGIN_URL = f"{USER_SERVICE_URL}/users/login"
LIST_TICKETS_URL = f"{TICKET_SERVICE_URL}/tickets"
BUY_TICKET_URL = f"{PAYMENT_SERVICE_URL}/payments"

# Variável para armazenar o usuário logado e seu portfólio de bilhetes
current_user = None
portfolio = []

def menu_pagamentos():
    """Exibe o menu principal do sistema de pagamentos."""
    while True:
        print("\n=== Sistema de Pagamentos ===")
        print("1. Fazer login")
        print("2. Listar bilhetes disponíveis")
        print("3. Comprar bilhete")
        print("4. Ver meu portfólio")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            fazer_login()
        elif escolha == "2":
            listar_bilhetes()
        elif escolha == "3":
            comprar_bilhete()
        elif escolha == "4":
            ver_portfolio()
        elif escolha == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def fazer_login():
    """Realiza o login de um usuário."""
    global current_user
    email = input("\nDigite seu email: ")
    password = input("Digite sua senha: ")

    payload = {"email": email, "password": password}
    try:
        response = requests.post(LOGIN_URL, json=payload)
        if response.status_code == 200:
            print("\nLogin bem-sucedido!")
            current_user = email
        elif response.status_code == 401:
            print("\nErro: Email ou senha inválidos.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def listar_bilhetes():
    """Lista todos os bilhetes disponíveis."""
    try:
        response = requests.get(LIST_TICKETS_URL)
        if response.status_code == 200:
            bilhetes = response.json()
            if not bilhetes:
                print("\nNão há bilhetes disponíveis.")
                return

            print("\n=== Bilhetes Disponíveis ===")
            for i, bilhete in enumerate(bilhetes, start=1):
                print(f"{i}. Evento: {bilhete['event_name']}")
                print(f"   Tipo: {bilhete['ticket_type']}")
                print(f"   Preço: {bilhete['price']:.2f}")
                print(f"   Quantidade disponível: {bilhete['quantity']}\n")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def comprar_bilhete():
    """Permite ao usuário comprar bilhetes."""
    if not current_user:
        print("\nVocê precisa fazer login antes de comprar bilhetes.")
        return

    listar_bilhetes()

    evento_nome = input("\nDigite o nome do evento do bilhete que deseja comprar: ")
    tipo_bilhete = input("Digite o tipo do bilhete (normal, VIP, etc.): ")
    quantidade = input("Digite a quantidade de bilhetes que deseja comprar: ")

    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

        # Verificar se o bilhete existe antes de tentar a compra
        response = requests.get(LIST_TICKETS_URL)
        if response.status_code == 200:
            tickets = response.json()
            print("\n=== Bilhetes disponíveis ===")
            print(tickets)

            ticket_exists = any(
                ticket["event_name"].strip().lower() == evento_nome.strip().lower() and
                ticket["ticket_type"].strip().lower() == tipo_bilhete.strip().lower()
                for ticket in tickets
            )
            if not ticket_exists:
                print("\nErro: O bilhete especificado não existe. Verifique o nome do evento e o tipo de bilhete.")
                return

        payload = {
            "user_email": current_user,
            "event_name": evento_nome,
            "ticket_type": tipo_bilhete,
            "quantity": quantidade
        }
        response = requests.post(BUY_TICKET_URL, json=payload)
        if response.status_code == 200:
            print("\nCompra realizada com sucesso!")
            bilhete = response.json()
            portfolio.append(bilhete)  # Adiciona o bilhete ao portfólio do usuário
        elif response.status_code == 400:
            print("\nErro: Não foi possível processar a compra. Verifique a disponibilidade dos bilhetes.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira um valor numérico válido para a quantidade.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)


def ver_portfolio():
    """Exibe o portfólio de bilhetes comprados pelo usuário."""
    if not portfolio:
        print("\nSeu portfólio está vazio.")
        return

    print("\n=== Meu Portfólio de Bilhetes ===")
    for i, bilhete in enumerate(portfolio, start=1):
        print(f"{i}. Evento: {bilhete['event_name']}")
        print(f"   Tipo: {bilhete['ticket_type']}")
        print(f"   Quantidade: {bilhete['quantity']}")
        print(f"   Preço total: {bilhete['total_price']:.2f}\n")

if __name__ == "__main__":
    menu_pagamentos()
