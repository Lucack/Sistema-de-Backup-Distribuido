#implementação de um servidor base para interpratação de métodos HTTP

import socket
import os

# nome do servidor
SERVER_NAME = "Servidor 4"

# definindo o endereço IP do host
SERVER_HOST = "localhost"

# definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8084

# diretorio do servidor
SERVER_DIRECTORY = SERVER_NAME.replace(" ", "")


def receive_from_any(connection_socket):
         
    try:

        buffer = b''

        while b'\n\n' not in buffer:
            buffer += connection_socket.recv(1024)

        # Separando header do data
        header, data = buffer.split(b'\n\n',1)

        print(f"Itens do Header: \n{header} \n")

        data = data.rstrip()
        header = header.decode().strip()

        list_header = header.split("\n")
        filename = list_header[0]
        replicaAdress = list_header[1]
        
        replicaPort = int(list_header[2])

        print(f"Itens do Header: \n{header} \n")
       
        # recebendo arquivo        
        print("Recebendo o arquivo do Manager...")
        while True:
            seg = connection_socket.recv(1024)
            if b"<TININI>" in seg:
                seg = seg.replace(b"<TININI>", b"")
                seg.strip()                
                data += seg
                break
            data += seg

        print("Arquivo", filename, "recebido com sucesso")
        
        # Caminho completo do arquivo
        file_path = os.path.join(SERVER_DIRECTORY, filename)

        # Salvando arquivo no servidor
        with open(file_path, 'wb') as f:
            f.write(data)

        print("Arquivo", filename, "salvo com sucesso")
    
        connection_socket.close()
        return(filename, replicaAdress, replicaPort, data)


    except Exception as e:
        print(f"Erro ao processar os dados do manager: {e}")

def sendto_replica_server(filename, replicaAdress, replicaPort, data):


    try:
        
        replica_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        replica_socket.connect((replicaAdress, replicaPort))
        header = f"{filename}\n{replicaAdress}\n{replicaPort}\n\n"
        replica_socket.sendall(header.encode())
        print(f"Header enviado para o servidor de replica porta {replicaPort}")

        replica_socket.sendall(data)
        print(f"Conteúdo {filename} enviado para o servidor de replica porta {replicaPort}")

        end = b"<TININI>"
        replica_socket.sendall(end)

    except Exception as e:
        print(f"Erro no envio do arquivo para servidor replica ({replicaAdress}:{replicaPort}): {e}")

    
    return 

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
        
        filename, replicaAdress, replicaPort, data = receive_from_any(connection_socket)
        if (replicaPort != SERVER_PORT ): 
            sendto_replica_server(filename, replicaAdress, replicaPort, data)


main_server()