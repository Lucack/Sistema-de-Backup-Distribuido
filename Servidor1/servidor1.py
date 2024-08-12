import socket
import os

# Configurações do servidor de base
BASE_SERVER_HOST = "localhost"
BASE_SERVER_PORT = 8081
SAVE_DIRECTORY = "Servidor1/"

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

        # Criar diretório se não existir
        if not os.path.exists(SAVE_DIRECTORY):
            os.makedirs(SAVE_DIRECTORY)

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

        # Salvar o arquivo recebido
        file_path = os.path.join(SAVE_DIRECTORY, file_name)
        with open(file_path, 'wb') as f:
            f.write(data)

        print(f"Conteúdo do Arquivo Recebido e salvo como '{file_path}'")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        # Garantir que a conexão seja fechada após o processamento
        client_socket.close()

def start_server():
    base_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    base_server_socket.bind((BASE_SERVER_HOST, BASE_SERVER_PORT))
    base_server_socket.listen(5)

    print(f"Servidor de base escutando na porta {BASE_SERVER_PORT}...")

    try:
        while True:
            client_socket, addr = base_server_socket.accept()
            print(f"Conexão aceita de {addr}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        # Fechar o socket do servidor ao encerrar
        base_server_socket.close()

if __name__ == "__main__":
    start_server()
