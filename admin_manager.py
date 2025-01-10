import requests

# Endereço base dos serviços
EVENT_SERVICE_URL = "http://localhost:5001"
TICKET_SERVICE_URL = "http://localhost:5004"

def menu_administrador():
    """Exibe o menu principal para o administrador."""
    while True:
        print("\n=== Menu do Administrador ===")
        print("1. Criar evento")
        print("2. Criar bilhete")
        print("3. Listar eventos")
        print("4. Listar bilhetes")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            criar_evento()
        elif escolha == "2":
            criar_bilhete()
        elif escolha == "3":
            listar_eventos()
        elif escolha == "4":
            listar_bilhetes()
        elif escolha == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def criar_evento():
    """Permite ao administrador criar um novo evento."""
    nome = input("\nDigite o nome do evento: ")
    descricao = input("Digite a descrição do evento: ")
    localizacao = input("Digite a localização do evento: ")
    lugares = input("Digite o número de lugares disponíveis: ")

    try:
        lugares = int(lugares)
        if lugares <= 0:
            print("O número de lugares deve ser maior que zero.")
            return

        payload = {
            "name": nome,
            "description": descricao,
            "location": localizacao,
            "seats": lugares
        }

        response = requests.post(f"{EVENT_SERVICE_URL}/events", json=payload)
        if response.status_code == 201:
            print("\nEvento criado com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Dados inválidos ou evento já existente.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira um valor numérico válido para o número de lugares.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def criar_bilhete():
    """Permite ao administrador criar bilhetes para um evento existente."""
    listar_eventos()
    evento_nome = input("\nDigite o nome do evento: ")

    # Consultar os detalhes do evento
    try:
        response = requests.get(f"{EVENT_SERVICE_URL}/events")
        if response.status_code == 200:
            eventos = response.json()
            evento = next((e for e in eventos if e["name"].strip().lower() == evento_nome.strip().lower()), None)
            if not evento:
                print("\nErro: Evento não encontrado.")
                return

            lugares_disponiveis = evento["seats"] - sum(
                ticket["quantity"] for ticket in listar_bilhetes_evento(evento_nome)
            )

            if lugares_disponiveis <= 0:
                print("\nErro: Não há lugares disponíveis para este evento.")
                return

            print(f"\nLugares disponíveis para o evento '{evento_nome}': {lugares_disponiveis}")
        else:
            print(f"\nErro ao buscar eventos: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)
        return

    tipo_bilhete = input("Digite o tipo do bilhete (normal, VIP, etc.): ")
    preco = input("Digite o preço do bilhete: ")
    quantidade = input("Digite a quantidade de bilhetes: ")

    try:
        preco = float(preco)
        quantidade = int(quantidade)
        if preco <= 0 or quantidade <= 0:
            print("O preço e a quantidade devem ser maiores que zero.")
            return

        if quantidade > lugares_disponiveis:
            print("\nErro: A quantidade de bilhetes excede os lugares disponíveis.")
            return

        payload = {
            "event_name": evento_nome,
            "ticket_type": tipo_bilhete,
            "price": preco,
            "quantity": quantidade
        }

        response = requests.post(f"{TICKET_SERVICE_URL}/tickets", json=payload)
        if response.status_code == 201:
            print("\nBilhete criado com sucesso!")
        elif response.status_code == 400:
            print("\nErro: Dados inválidos ou bilhete já existente.")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except ValueError:
        print("Por favor, insira valores numéricos válidos para o preço e a quantidade.")
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def listar_eventos():
    """Lista todos os eventos."""
    try:
        response = requests.get(f"{EVENT_SERVICE_URL}/events")
        if response.status_code == 200:
            eventos = response.json()
            if not eventos:
                print("\nNão há eventos cadastrados.")
                return

            print("\n=== Eventos Cadastrados ===")
            for i, evento in enumerate(eventos, start=1):
                print(f"{i}. Nome: {evento['name']}")
                print(f"   Descrição: {evento['description']}")
                print(f"   Localização: {evento['location']}")
                print(f"   Lugares disponíveis: {evento['seats']}\n")
        else:
            print(f"\nErro inesperado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("\nErro ao se conectar ao servidor:")
        print(e)

def listar_bilhetes():
    """Lista todos os bilhetes."""
    try:
        response = requests.get(f"{TICKET_SERVICE_URL}/tickets")
        if response.status_code == 200:
            bilhetes = response.json()
            if not bilhetes:
                print("\nNão há bilhetes cadastrados.")
                return

            print("\n=== Bilhetes Cadastrados ===")
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

def listar_bilhetes_evento(evento_nome):
    """Lista os bilhetes de um evento específico."""
    try:
        response = requests.get(f"{TICKET_SERVICE_URL}/tickets")
        if response.status_code == 200:
            bilhetes = response.json()
            return [b for b in bilhetes if b["event_name"].strip().lower() == evento_nome.strip().lower()]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

if __name__ == "__main__":
    menu_administrador()
