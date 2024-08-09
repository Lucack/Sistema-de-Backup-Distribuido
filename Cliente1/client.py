import socket
import os

# Endereço do servidor e porta do gerenciador
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080

DIRECTORY = "Cliente1/"

def initial_menu():
    print("Menu:")
    print("1. Iniciar backup")
    print("2. Sair")

def send_file(client_socket, file_path):
    try:
        # Enviar o nome do arquivo
        file_name = os.path.basename(file_path)
        content_length = os.path.getsize(file_path)
        
        # Enviar a linha de solicitação HTTP
        client_socket.sendall(f"PUT /{file_name} HTTP/1.1\r\n".encode())
        
        # Enviar os cabeçalhos HTTP
        client_socket.sendall(f"Host: {SERVER_ADDRESS}\r\n".encode())
        client_socket.sendall("Content-Type: application/octet-stream\r\n".encode())
        client_socket.sendall(f"Content-Length: {content_length}\r\n".encode())
        client_socket.sendall(b"\r\n")
        
        # Enviar o conteúdo do arquivo
        with open(file_path, 'rb') as file:
            while chunk := file.read(1024):
                client_socket.sendall(chunk)
        
        # Receber a resposta do servidor
        # response = client_socket.recv(1024).decode()
        # print("Resposta do servidor:", response)
    
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")


# Criar um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar ao gerenciador
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    
    while True:
        initial_menu()
        option = input("Escolha uma opção: ")
        
        if option == '1':
            file_name = input("Digite o nome do arquivo para backup: ")
            file_path = os.path.join(DIRECTORY, file_name)
            
            if os.path.isfile(file_path):
                send_file(client_socket, file_path)
            else:
                print("Arquivo não encontrado")
        
        elif option == '2':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")
    
finally:
    # Fechar a conexão
    client_socket.close()
