import socket
import os
import random

# Configurações do gerente
MANAGER_HOST = "localhost"
MANAGER_PORT = 8080
BASE_SERVERS = [("localhost", 8081)]

# BASE_SERVERS = [("localhost", 8081), ("localhost", 8082), ("localhost", 8083)]

def forward_to_base_server(file_name, data):
    try:
        # Escolher aleatoriamente um servidor de base
        base_server = random.choice(BASE_SERVERS)
        
        # Criar um socket para o servidor de base
        base_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        base_server_socket.connect(base_server)
        
        # Criar e enviar o cabeçalho
        content_length = len(data)
        header = f"{file_name}\n{content_length}\n"
        base_server_socket.sendall(header.encode())
        
        # Enviar o corpo
        base_server_socket.sendall(data)
        
        # Enviar um finalizador para indicar que o envio está completo
        base_server_socket.sendall(b'END_OF_FILE\n')
        base_server_socket.close()

        print(f"Encaminhado para o servidor de base {base_server[1]}")

    except Exception as e:
        print(f"Erro ao encaminhar para o servidor de base: {e}")

def handle_client(client_socket):
    try:
        # Receber o cabeçalho
        header_data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        if not header_data:
            raise ValueError("Cabeçalho não recebido")

        header_lines = header_data.split('\n')
        if len(header_lines) < 2:
            raise ValueError("Cabeçalho inválido")

        file_name = header_lines[0]
        content_length = int(header_lines[1])
        print(f"Recebido:\nNome do Arquivo: {file_name}\nTamanho do Conteúdo: {content_length} bytes")

        # Receber o corpo
        data = b''
        while len(data) < content_length:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet

        # Verificar o finalizador
        if data.endswith(b'END_OF_FILE\n'):
            data = data[:-len(b'END_OF_FILE\n')]

        # Encaminhar para o servidor de base
        forward_to_base_server(file_name, data)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        client_socket.close()

def start_manager():
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.bind((MANAGER_HOST, MANAGER_PORT))
    manager_socket.listen(5)

    print(f"Gerente escutando na porta {MANAGER_PORT}...")

    while True:
        client_socket, addr = manager_socket.accept()
        print(f"Conexão aceita de {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_manager()
