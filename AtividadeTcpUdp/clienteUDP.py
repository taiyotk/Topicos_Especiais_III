# clienteUDP.py
# Cliente UDP que envia um datagrama ao servidor e aguarda resposta com timeout.
# Não há conexão em UDP, foi usado: sendto() e recvfrom().

import socket

HOST = 'localhost'  # Endereço do servidor UDP
PORT = 12345        # Porta do servidor UDP
# Timeout em segundos para aguardar resposta (evita bloqueio indefinido)
TIMEOUT = 5

# Cria socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Define timeout para operações de leitura (recvfrom). Opcional mas recomendado.
client_socket.settimeout(TIMEOUT)

try:
    mensagem = "Olá, servidor, meu nome é Taiyo."
    # sendto envia os bytes diretamente para o endereço (host,port)
    client_socket.sendto(mensagem.encode('utf-8'), (HOST, PORT))
    # Aguarda resposta do servidor (max 1024 bytes)
    data, server_addr = client_socket.recvfrom(1024)
    print(f"Resposta do servidor ({server_addr}): {data.decode('utf-8')}")
except socket.timeout:
    print(
        f"Nenhuma resposta em {TIMEOUT} segundos. Verifique se o servidor UDP está rodando.")
except Exception as e:
    print(f"Erro no cliente UDP: {e}")
finally:
    client_socket.close()
