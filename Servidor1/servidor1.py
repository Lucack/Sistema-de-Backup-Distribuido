#implementação de um servidor base para interpratação de métodos HTTP

import socket

#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s \n" % SERVER_PORT)
print("Acesse http://localhost:%s \n\n" %SERVER_PORT)

#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    data = b''
    
    client_connection.settimeout(0.1)

    while True:
        try:
            packet = client_connection.recv(1024)
            if not packet:
                break
            data += packet
        except socket.timeout:
            break

    #pega a solicitação do cliente
    request = data.decode()
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        print(request)


        #analisa a solicitação HTTP
        headers = request.split("\n")
        print("headers ----> ",headers[0])
        #print(headers)#impressão dos cabeçalhos

        #pega o nome do arquivo sendo solicitado        
        filename = headers[0].split()[1]
        # print("filename ----> ", filename)
        
        
        requestType = headers[0].split()[0]
        # print("requestType ----> ", requestType)
        # body = request[request.find("\r\n\r\n"):]
        # print("bodyy --->> ",body)


        # print("\n\n")
        
        
        #verifica o tipo de requisicao do usuario
        if requestType == "GET":

            #verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
            if filename == "/":
                filename = "/index.html"

            #try e except para tratamento de erro quando um arquivo solicitado não existir
            try:
                
                # verifica se é imagem
                if filename.endswith(('.png', '.jpg')):
                    openarq = 'rb'
                else:
                    openarq = 'r'

                fin = open("Servidor1/htdocs" + filename, openarq)
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
        
        elif requestType == "PUT":

            body = request[request.find("\r\n\r\n"):]


            try:
                # pega o nome do arquivo
                filename = filename[1:]

                # escrita em modo binário para evitar erros
                newFile = open("Servidor1/htdocs/" + filename, "wb") 

                # cria arquivo com o body passado
                newFile.write(body.encode())
                newFile.close()

                # responde 201
                response = f"HTTP/1.1 201 Created\n\n<h1>201 CREATED!<br>File Created!</h1> <p>Here's a link to your new file <a href='http://localhost:{SERVER_PORT}/{filename}'>newFile</a></p>"


            except Exception as e:

                # respsta para tratamento do erro
                response = "HTTP/1.1 500 Internal Server Error\n\n" + str(e)

        elif requestType == "POST":
            if '/upload' in filename:
                # Extrai os dados binários do corpo da requisição
                body = data[data.find(b"\r\n\r\n") + 4:]

                # Extraia o nome do arquivo do cabeçalho do conteúdo
                headers_dict = {}
                for header in headers:
                    if ': ' in header:
                        key, value = header.split(': ', 1)
                        headers_dict[key] = value

                content_disposition = headers_dict.get("Content-Disposition", "")
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[1].strip().replace('"', '')

                # Salva o arquivo no diretório desejado
                try:
                    with open(f"Servidor1/htdocs/{filename}", "wb") as file:
                        file.write(body)
                    response = "HTTP/1.1 201 Created\n\n<h1>File Uploaded Successfully</h1>"
                except Exception as e:
                    response = f"HTTP/1.1 500 Internal Server Error\n\n<h1>Error: {str(e)}</h1>"

        else:

            response = "HTTP/1.1 405 Method Not Allowed\n\n<h1>NOT ALLOWED METHOD 405!<br>Method Not Allowed For This Server!</h1>"

        #envia a resposta HTTP

        if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                    
            client_connection.sendall(response)
        else:
            client_connection.sendall(response.encode())

        client_connection.close()

server_socket.close()


