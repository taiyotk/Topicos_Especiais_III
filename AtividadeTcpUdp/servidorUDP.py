# servidorUDP.py
# Servidor UDP que recebe datagramas em loop e responde ao remetente.
# UDP é sem conexão, não há accept(), foi usado: recvfrom() para obter dados e endereço do remetente.
# Execute antes de clienteUDP.py.

import socket

HOST = 'localhost'  # Endereço para bind ('' para todas as interfaces)
PORT = 12345        # Porta UDP (pode ser a mesma numérica do TCP tecnicamente, mas é mais claro usar outra)

def main():
    # Cria socket UDP usando AF_INET e SOCK_DGRAM
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Reutilização de endereço (opcional, útil em reinícios)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    print(f"Servidor UDP aguardando mensagens em {HOST}:{PORT}... (CTRL+C para encerrar)")

    try:
        while True:
            # recvfrom devolve (dados, endereco_remetente)
            data, addr = server_socket.recvfrom(1024)
            mensagem = data.decode('utf-8')
            print(f"[{addr}] Mensagem recebida: {mensagem}")

            # Envia resposta de volta ao remetente (addr contém (host,port))
            resposta = "Mensagem recebida"
            server_socket.sendto(resposta.encode('utf-8'), addr)
    except KeyboardInterrupt:
        print("\nServidor UDP interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro no servidor UDP: {e}")
    finally:
        server_socket.close()
        print("Servidor UDP encerrado.")

if __name__ == "__main__":
    main()
