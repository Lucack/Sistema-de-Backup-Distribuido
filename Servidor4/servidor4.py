#implementação de um servidor base para interpratação de métodos HTTP

import socket

# nome do servidor
SERVER_NAME = "Servidor 4"

# definindo o endereço IP do host
SERVER_HOST = "localhost"

# definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8084

# diretorio do servidor
SERVER_DIRECTORY = SERVER_NAME.replace(" ", "")


def receive_from_manager(connection_socket):
         
    try:
        header = connection_socket.recv(1024).decode().strip()
        print(f"Arquivo {header} recebido pelo {SERVER_NAME}.")

        # recebendo arquivo
        data = b""
        while True:
            seg = connection_socket.recv(1024)
            if not seg:
                break
            data += seg

    except Exception as e:
        print(f"Erro ao processar os dados do cliente: {e}")


def main_server():
    
    # configuraçoes do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    print(f"{SERVER_NAME} em execução...")
    print("Escutando por conexões na porta %s \n" % SERVER_PORT)

    while True:
        # espera por conexões
        connection_socket, address = server_socket.accept()
        print("Conexão aceita pelo endereço", address)
        
        replica = receive_from_manager(connection_socket)

main_server()