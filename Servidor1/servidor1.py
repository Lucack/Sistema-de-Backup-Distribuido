import os
import socket

# Definindo nome do diretório do Servidor
SERVER_NAME = "Servidor1"

# Definindo o endereço IP do host
SERVER_HOST = ""

# Definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8081

# Criando o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurando o socket para reutilizar endereços
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Atrelando o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Colocando o socket para escutar por conexões
server_socket.listen(1)

print("\nServidor 1 em execução... \n")
print(f"Escutando por conexões na porta {SERVER_PORT} \n")
print(f"Acesse http://localhost:{SERVER_PORT} \n\n")

while True:
    client_connection, client_address = server_socket.accept()

    data = b''
    client_connection.settimeout(10)  # Aumentar o tempo limite para permitir a recepção de grandes arquivos

    while True:
        try:
            packet = client_connection.recv(1024)
            if not packet:
                break
            data += packet
        except socket.timeout:
            break

    # Extraindo cabeçalhos e corpo da solicitação
    request_str = data.decode('utf-8', errors='ignore')
    print("dados recebidos:", request_str)

    if '\r\n\r\n' in request_str:
        headers, body = request_str.split('\r\n\r\n', 1)
        body = data.split(b'\r\n\r\n', 1)[1]  # Manter o corpo como bytes
    else:
        headers = request_str
        body = b''

    # Imprimindo informações para depuração
    print("Headers:\n", headers)
    print(f"Corpo da requisição (tamanho {len(body)} bytes)")

    # Verificando se o cabeçalho está formatado corretamente
    headers_lines = headers.split('\n')
    if not headers_lines or len(headers_lines) < 1:
        response = "HTTP/1.1 400 Bad Request\n\n<h1>400 Bad Request</h1>"
    else:
        request_line = headers_lines[0].split()
        if len(request_line) < 3:
            response = "HTTP/1.1 400 Bad Request\n\n<h1>400 Bad Request</h1>"
        else:
            request_type = request_line[0]
            filename = request_line[1]

            # Remover a barra inicial do nome do arquivo
            if filename.startswith('/'):
                filename = filename[1:]

            # Verifica o tipo de requisição do usuário
            if request_type == "GET":

                # Verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
                if filename == "" or filename == "/":
                    filename = "index.html"

                if filename == "files":
                    # Lista os arquivos no diretório e cria a resposta
                    try:
                        files = os.listdir(SERVER_NAME)
                        file_list = ""
                        for file in files:
                            if not ("index.html" in file or ".py" in file):
                                file_path = os.path.join(SERVER_NAME, file)
                                if os.path.isfile(file_path):
                                    file_list += f'''
                                        <div class="file">
                                            <img src="{file}" alt="File Icon">
                                            <span>{file}</span>
                                        </div>
                                    '''
                        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>File List</title><style>body{{font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px;}} header{{display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: #007BFF; color: white; border-radius: 5px;}} header h1{{margin: 0;}} #file-container{{display: flex; flex-wrap: nowrap; overflow-x: auto; padding: 10px 0;}} .file{{display: flex; flex-direction: column; align-items: center; margin: 10px;}} .file img{{width: 100px; height: 100px; object-fit: cover;}}</style></head><body><div id='file-container'>{file_list}</div></body></html>"
                    except Exception as e:
                        response = f"HTTP/1.1 500 Internal Server Error\n\n<h1>500 Internal Server Error</h1><p>{str(e)}</p>"

                else:
                    # Tratamento de erro para quando um arquivo solicitado não existir
                    try:
                        # verifica se é imagem
                        if filename.endswith(('.png', '.jpg')):
                            openarq = 'rb'
                        else:
                            openarq = 'r'

                        with open(os.path.join(SERVER_NAME, filename), openarq) as fin:
                            content = fin.read()

                            # altera o cabeçalho para imagens
                            if openarq == 'rb':
                                if filename.endswith(".png"):
                                    content_type = "image/png"
                                else:
                                    content_type = "image/jpeg"
                                response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n".encode() + content
                            else:
                                response = "HTTP/1.1 200 OK\n\n" + content

                    except FileNotFoundError:
                        # caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
                        response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"

            elif request_type == "PUT":
                # Processar o corpo da solicitação PUT como binário
                if filename == "":
                    filename = "uploaded_file"

                try:
                    with open(os.path.join(SERVER_NAME, filename), 'wb') as new_file:
                        new_file.write(body)  # Escrever o corpo diretamente como bytes
                    response = f"HTTP/1.1 201 Created\n\n<h1>201 CREATED!<br>File Created!</h1> <p>Here's a link to your new file <a href='http://localhost:{SERVER_PORT}/{filename}'>newFile</a></p>"
                except Exception as e:
                    response = f"HTTP/1.1 500 Internal Server Error\n\n<h1>500 Internal Server Error</h1><p>{str(e)}</p>"

            else:
                response = "HTTP/1.1 405 Method Not Allowed\n\n<h1>NOT ALLOWED METHOD 405!<br>Method Not Allowed For This Server!</h1>"

    # Enviando a resposta HTTP
    client_connection.sendall(response.encode() if isinstance(response, str) else response)
    client_connection.close()

server_socket.close()
