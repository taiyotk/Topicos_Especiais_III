# clienteTCP.py
# Cliente TCP se conecta a um servidor TCP, envia uma mensagem e aguarda resposta.
# Execute após iniciar o servidor TCP (servidorTCPThreads.py).

import socket

# Endereço do servidor (pode ser '127.0.0.1' ou IP da máquina)
HOST = 'localhost'
PORT = 12345         # Porta em que o servidor TCP está escutando

# Cria um socket TCP usando IPv4 (AF_INET) e SOCK_STREAM (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta estabelecer conexão com o servidor
    # connect() lança exceção se o servidor não estiver rodando/aceitando conexões
    client_socket.connect((HOST, PORT))
    # Mensagem a ser enviada. Em Python sockets enviamos bytes, então codificamos com UTF-8.
    mensagem = "Olá, servidor, meu nome é Taiyo."
    # sendall garante envio completo dos bytes
    client_socket.sendall(mensagem.encode('utf-8'))
    # Aguarda resposta do servidor. O argumento 1024 é o tamanho máximo do buffer (bytes)
    data = client_socket.recv(1024)
    # Decodifica os bytes recebidos para string
    print(f"Resposta do servidor: {data.decode('utf-8')}")

except ConnectionRefusedError:
    print(
        f"Não foi possível conectar em {HOST}:{PORT} -- verifique se o servidor está rodando.")
except Exception as e:
    print(f"Erro no cliente TCP: {e}")
finally:
    # Garante que o socket será fechado, mesmo em caso de erro
    client_socket.close()
