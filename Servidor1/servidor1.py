#implementação de um servidor base para interpratação de métodos HTTP

import socket
import os

# nome do servidor
SERVER_NAME = "Servidor 1"

# definindo o endereço IP do host
SERVER_HOST = "localhost"

# definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8081

# diretorio do servidor
SERVER_DIRECTORY = SERVER_NAME.replace(" ", "")


def receive_from_manager(connection_socket):
         
    try:

        buffer = b''

        while b'\n\n' not in buffer:
            buffer += connection_socket.recv(1024)

        # Separando header do data
        header, data = buffer.split(b'\n\n',1)

        data = data.strip()
        header = header.decode().strip()

        list_header = header.split("\n")
        filename = list_header[0]
        serverAdress = list_header[1]
        serverPort = list_header[2]
        print(f"Itens do Header: \n{header} \nRecebido pelo {SERVER_NAME}.\n")
       
       
        # recebendo arquivo        
        print("Recebendo o arquivo do Manager...")
        while True:
            seg = connection_socket.recv(1024).strip()
            if b"<TININI>" in seg:
                seg = seg.replace(b"<TININI>", b"")
                seg.strip()                
                data += seg
                break
            data += seg

        print("Data: ", data)
        
        # Caminho completo do arquivo
        file_path = os.path.join(SERVER_DIRECTORY, filename)

        # Salvando arquivo no servidor
        with open(file_path, 'wb') as f:
            f.write(data)

    except Exception as e:
        print(f"Erro ao processar os dados do manager: {e}")


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