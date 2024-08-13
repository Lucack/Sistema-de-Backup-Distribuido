import socket
import os

# Configurações do manager
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8080
DIRECTORY = "Cliente1/"

def initial_menu():
    print("Menu:")
    print("1. Iniciar backup")
    print("2. Sair")

def send_file(client_socket, file_path):

   
    try:
        # Enviar o nome do arquivo e o tamanho do conteúdo
        file_name = os.path.basename(file_path)
        
        # Criar e enviar o cabeçalho
        header = f"{file_name}\n"
        client_socket.sendall(header.encode())
        
        # Ler o conteúdo do arquivo e enviar
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                client_socket.sendall(chunk)

        end = b"<TININI>"
        client_socket.sendall(end)
        
        print("Arquivo enviado.")

        

    
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")


while True:
    initial_menu()
    option = input("Escolha uma opção: ")
    
    if option == '1':
        filename = input("Digite o nome do arquivo para backup: ")
        file_path = os.path.join(DIRECTORY, filename)
         
        # Criar um socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar ao gerente
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
            
        if os.path.isfile(file_path):
            send_file(client_socket, file_path)
        else:
            print("Arquivo não encontrado")
    
    elif option == '2':
        print("Saindo...")
        break
    
    else:
        print("Opção inválida. Tente novamente.")