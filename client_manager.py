import requests

# Endereço base dos serviços
USER_SERVICE_URL = "http://localhost:5002"
TICKET_SERVICE_URL = "http://localhost:5004"
PAYMENT_SERVICE_URL = "http://localhost:5003"

current_user = None  # Armazena o email do usuário logado


def menu_principal():
    """Exibe o menu principal para o cliente."""
    while True:
        print("\n=== Menu do Cliente ===")
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
    """Registra um novo usuário."""
    username = input("\nDigite seu nome de usuário: ")
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")

    payload = {"username": username, "email": email, "password": password}
    try:
        response = requests.post(f"{USER_SERVICE_URL}/users/register", json=payload)
        if response.status_code == 201:
            print("\nUsuário registrado com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Email já registrado.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)


def fazer_login():
    """Realiza o login do usuário."""
    global current_user  # Declaração global no início da função
    email = input("\nDigite seu email: ")
    password = input("Digite sua senha: ")

    payload = {"email": email, "password": password}
    try:
        response = requests.post(f"{USER_SERVICE_URL}/users/login", json=payload)
        if response.status_code == 200:
            print("\nLogin bem-sucedido!")
            current_user = email
            menu_cliente_logado()
        elif response.status_code == 401:
            print("\nErro: Email ou senha inválidos.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)



def menu_cliente_logado():
    """Exibe o menu para o cliente logado."""
    global current_user  # A declaração global precisa ser feita no início da função
    while True:
        print(f"\n=== Bem-vindo, {current_user} ===")
        print("1. Depositar dinheiro")
        print("2. Listar bilhetes disponíveis")
        print("3. Comprar bilhete")
        print("4. Fazer logout")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            depositar_dinheiro()
        elif escolha == "2":
            listar_bilhetes()
        elif escolha == "3":
            comprar_bilhete()
        elif escolha == "4":
            print("\nLogout realizado com sucesso!")
            current_user = None
            break
        else:
            print("Opção inválida. Tente novamente.")



def depositar_dinheiro():
    """Permite ao usuário depositar dinheiro na conta."""
    if not current_user:
        print("\nVocê precisa fazer login antes de depositar dinheiro.")
        return

    try:
        amount = float(input("\nDigite o valor a ser depositado: "))
        if amount <= 0:
            print("O valor deve ser maior que zero.")
            return

        payload = {"email": current_user, "amount": amount}
        response = requests.post(f"{USER_SERVICE_URL}/users/add_money", json=payload)
        if response.status_code == 200:
            print(f"\n{amount:.2f} adicionados com sucesso à sua conta!")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira um valor numérico válido.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)


def listar_bilhetes():
    """Lista todos os bilhetes disponíveis."""
    try:
        response = requests.get(f"{TICKET_SERVICE_URL}/tickets")
        if response.status_code == 200:
            bilhetes = response.json()
            if not bilhetes:
                print("\nNão há bilhetes disponíveis.")
                return  # Retorna ao menu principal se não houver bilhetes

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

    evento_nome = input("\nDigite o nome do evento do bilhete que deseja comprar: ").strip().lower()
    tipo_bilhete = input("Digite o tipo do bilhete (normal, VIP, etc.): ").strip().lower()
    quantidade = input("Digite a quantidade de bilhetes que deseja comprar: ")

    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

        # Verificar se o bilhete existe antes de tentar a compra
        response = requests.get(f"{TICKET_SERVICE_URL}/tickets")
        if response.status_code == 200:
            bilhetes = response.json()
            print("\n=== Bilhetes recebidos da API ===")
            print(bilhetes)  # Log para depuração

            # Comparação padronizando os valores
            ticket_exists = any(
                ticket["event_name"].strip().lower() == evento_nome and
                ticket["ticket_type"].strip().lower() == tipo_bilhete
                for ticket in bilhetes
            )
            if not ticket_exists:
                print("\nErro: O bilhete especificado não existe. Verifique o nome do evento e o tipo de bilhete.")
                return

        # Enviar a requisição de compra ao microserviço de pagamentos
        payload = {
            "user_email": current_user,
            "event_name": evento_nome,
            "ticket_type": tipo_bilhete,
            "quantity": quantidade
        }
        response = requests.post(f"{PAYMENT_SERVICE_URL}/payments", json=payload)
        if response.status_code == 200:
            print("\nCompra realizada com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Não foi possível processar a compra. Verifique o saldo ou a disponibilidade dos bilhetes.")
        elif response.status_code == 404:
            print("\nErro: Bilhete ou evento não encontrado.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira um valor numérico válido para a quantidade.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)



if __name__ == "__main__":
    menu_principal()
