import requests

# Endereço base do serviço de bilhetes e eventos
TICKET_SERVICE_URL = "http://localhost:5004"
EVENT_SERVICE_URL = "http://localhost:5001"
CREATE_TICKET_URL = f"{TICKET_SERVICE_URL}/tickets/create"
LIST_TICKETS_URL = f"{TICKET_SERVICE_URL}/tickets"
LIST_EVENTS_URL = f"{EVENT_SERVICE_URL}/events"

def menu_bilhetes():
    """Exibe o menu principal do sistema de bilhetes."""
    while True:
        print("\n=== Sistema de Gestão de Bilhetes ===")
        print("1. Criar bilhetes para um evento")
        print("2. Listar todos os bilhetes")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            criar_bilhete()
        elif escolha == "2":
            listar_bilhetes()
        elif escolha == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def listar_eventos():
    """Lista todos os eventos cadastrados e retorna uma lista com os nomes dos eventos."""
    try:
        response = requests.get(LIST_EVENTS_URL)
        if response.status_code == 200:
            eventos = response.json()
            if not eventos:
                print("\nNão há eventos cadastrados.")
                return []

            print("\n=== Lista de Eventos ===")
            for i, evento in enumerate(eventos, start=1):
                print(f"{i}. Nome: {evento['name']}")
                print(f"   Descrição: {evento['description']}")
                print(f"   Localização: {evento['location']}")
                print(f"   Lugares disponíveis: {evento['seats']}\n")
            return eventos
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
            return []
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)
        return []

def obter_bilhetes_existentes(evento_nome):
    """Obtém o número total de bilhetes já criados para um evento específico."""
    try:
        response = requests.get(LIST_TICKETS_URL)
        if response.status_code == 200:
            bilhetes = response.json()
            total_bilhetes = sum(bilhete['quantity'] for bilhete in bilhetes if bilhete['event_name'] == evento_nome)
            return total_bilhetes
        else:
            print(f"\nErro ao listar bilhetes: {response.status_code}")
            return 0
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)
        return 0

def criar_bilhete():
    """Cria bilhetes associados a um evento existente."""
    eventos = listar_eventos()
    if not eventos:
        return

    evento_nome = input("\nDigite o nome do evento para o qual deseja criar bilhetes: ")
    evento = next((ev for ev in eventos if ev["name"] == evento_nome), None)
    if not evento:
        print("Evento não encontrado. Certifique-se de digitar o nome corretamente.")
        return

    total_lugares = evento["seats"]
    bilhetes_existentes = obter_bilhetes_existentes(evento_nome)
    lugares_disponiveis = total_lugares - bilhetes_existentes

    if lugares_disponiveis <= 0:
        print("\nNão há mais lugares disponíveis para este evento.")
        return

    print(f"\nTotal de lugares do evento: {total_lugares}")
    print(f"Lugares já ocupados por bilhetes: {bilhetes_existentes}")
    print(f"Lugares ainda disponíveis: {lugares_disponiveis}")

    tipo = input("Digite o tipo de bilhete (normal, VIP, etc.): ")
    preco = input("Digite o preço do bilhete: ")
    quantidade = input("Digite a quantidade de bilhetes a ser criada: ")

    try:
        preco = float(preco)
        quantidade = int(quantidade)
        if preco <= 0 or quantidade <= 0:
            print("O preço e a quantidade devem ser maiores que zero.")
            return

        if quantidade > lugares_disponiveis:
            print("A quantidade de bilhetes excede o número de lugares disponíveis.")
            return

        payload = {"event_name": evento_nome, "ticket_type": tipo, "price": preco, "quantity": quantidade}
        response = requests.post(CREATE_TICKET_URL, json=payload)
        if response.status_code == 201:
            print("\nBilhetes criados com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Dados inválidos.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira valores numéricos válidos para o preço e a quantidade.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def listar_bilhetes():
    """Lista todos os bilhetes cadastrados."""
    try:
        response = requests.get(LIST_TICKETS_URL)
        if response.status_code == 200:
            bilhetes = response.json()
            if not bilhetes:
                print("\nNão há bilhetes cadastrados.")
                return

            print("\n=== Lista de Bilhetes ===")
            for i, bilhete in enumerate(bilhetes, start=1):
                print(f"{i}. Evento: {bilhete['event_name']}")
                print(f"   Tipo: {bilhete['ticket_type']}")
                print(f"   Preço: {bilhete['price']:.2f}")
                print(f"   Quantidade: {bilhete['quantity']}\n")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

if __name__ == "__main__":
    menu_bilhetes()
