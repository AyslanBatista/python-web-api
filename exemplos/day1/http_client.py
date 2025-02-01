import socket

# AF_INET = IPV4
# SOCK_STREAM = Protocolos baseados em texto
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Abrindo conexão com o site "example.com" no protocolo HTTP
cliente.connect(("localhost", 9000))

# request
# \r é o recuo, \n é uma nova linha
# encode() vai serealizar em um formato de texto mais basico
cmd = "GET /index.html HTTP/1.0\r\nHost: localhost\r\n\r\n".encode()

# Enviando o request
cliente.send(cmd)

# Coletando informações do site por partes
while True:
    # Recebendo 512 bytes
    data = cliente.recv(512)

    # Verificando se ainda existe partes do site para serem baixadas
    if len(data) < 1:
        break

    # decode() transforando as informações em UTF8
    # end="" para eliminar as quebras de linhas que o print coloca
    print(data.decode(), end="")

# Fexando a conexão
cliente.close()
