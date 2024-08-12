import socket

# Configurações do gerente
MANAGER_HOST = "localhost"  # Ou "0.0.0.0" para aceitar conexões de qualquer IP
MANAGER_PORT = 8080

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

        # Salvar o arquivo recebido para verificar
        with open(file_name, 'wb') as f:
            f.write(data)

        print(f"Conteúdo do Arquivo Recebido e salvo como '{file_name}'")

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