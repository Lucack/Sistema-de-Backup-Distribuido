import socket

# Manager Server Configuration
MANAGER_ADRESS = ""
MANAGER_PORT = 8080

# Worker Servers Configuration
WORKER_SERVERS = [('localhost', 8081),('localhost', 8082),('localhost', 8083),('localhost', 8084)]
carga = [0,0,0,0]

def handle_client(client_socket):
    # temos que arrumar depois, e faremos baseado no vetor carga
    
    try:


        buffer = b''

        while b'\n\n' not in buffer:
            buffer += client_socket.recv(1024)

        # Separando header do data
        filename, data = buffer.split(b'\n\n',1)

        print(f"Arquivo {filename.decode()} recebido.")

        filename= filename.decode()
        data = data.rstrip()

        # receber dados do arquivo        
        while True:
            seg = client_socket.recv(1024)
            # if b"<TININI>" == seg:
            if b"<TININI>" in seg:
                seg = seg.replace(b"<TININI>", b"")
                data += seg.strip()
                break
            data += seg
            
        client_socket.close()

    except Exception as e:
        print(f"Erro ao processar os dados do cliente: {e}")

    return filename, data   

def choose_sv(carga):
    principal = -1
    replica = -1
    #lembrar de fazer uma escolha pelo mínimo, e acessar o si correspondente no vetor de servidores
    min_carga = float('inf')
    for i in range(len(carga)):
        if carga[i] < min_carga:
            min_carga = carga[i]
            principal = i

    min_carga = float('inf')
    for i in range(len(carga)):
        if i == principal:
            continue
        if carga[i] < min_carga:
            min_carga = carga[i]
            replica = i

    return principal, replica

def sendto_server(filename, data, principal, replica):

    principal_adress, principal_port = WORKER_SERVERS[principal][0], WORKER_SERVERS[principal][1]
    replica_adress, replica_port = WORKER_SERVERS[replica][0], WORKER_SERVERS[replica][1]

    try:
        toserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        toserver_socket.connect((principal_adress, principal_port))
        header = f"{filename}\n{replica_adress}\n{replica_port}\n\n"
        print("PRINTANDO HEADER:\n",header)
        toserver_socket.sendall(header.encode())
        print(f"Header enviado para porta {principal_port}")

        toserver_socket.sendall(data)
        print(f"Conteúdo {filename} enviado para {principal_port}")

        end = b"<TININI>"
        toserver_socket.sendall(end)
        

    except Exception as e:
        print(f"Erro no envio do arquivo: {e}")

    carga[principal] += 1
    carga[replica] += 1

def start_manager():
    
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.bind((MANAGER_ADRESS, MANAGER_PORT))
    manager_socket.listen(1)
    
    print(f"Manager Server listening on port {MANAGER_PORT}...")
    
    while True:
        client_socket, addr = manager_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle the client request (sequentially)
        filename, data = handle_client(client_socket)
        print(filename)
        principal, replica = choose_sv(carga)
        print(principal,replica)
        #sendto_server(filename, data, WORKER_SERVERS[principal][0], WORKER_SERVERS[principal][1], WORKER_SERVERS[replica][0], WORKER_SERVERS[replica][1])
        sendto_server(filename, data, principal, replica)


start_manager()