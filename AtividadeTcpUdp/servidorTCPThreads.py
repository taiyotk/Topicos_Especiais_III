# servidorTCPThreads.py
# Servidor TCP simples que aceita múltiplas conexões usando threads.
# Cada cliente é tratado em uma thread separada.
# Execute este servidor antes de rodar clienteTCP.py.

import socket
import threading

HOST = 'localhost'  # Endereço para bind ('' para todas as interfaces)
PORT = 12345        # Porta para ouvir conexões TCP


def manipula_cliente(conn, addr):
    """
    Função executada em uma thread para tratar a conexão com um cliente.
    conn: objeto socket da conexão com o cliente
    addr: tupla (host, porta) do cliente
    """
    try:
        print(f"[{addr}] Conexão estabelecida.")
        # Recebe dados do cliente (até 1024 bytes)
        data = conn.recv(1024)
        # Em TCP, recv() retorna b'' quando o cliente fecha a conexão
        if not data:
            print(f"[{addr}] Cliente desconectou sem enviar dados.")
            return
        mensagem = data.decode('utf-8')
        print(f"[{addr}] Mensagem recebida: {mensagem}")

        # Envia confirmação de volta ao cliente
        resposta = "Mensagem recebida"
        conn.sendall(resposta.encode('utf-8'))

    except Exception as e:
        print(f"[{addr}] Erro ao tratar cliente: {e}")
    finally:
        # Fecha a conexão com o cliente ao terminar
        conn.close()
        print(f"[{addr}] Conexão encerrada.")


def main():
    # Cria socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar o endereço/porta rapidamente (evita "Address already in use" ao reiniciar)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # backlog de 5 conexões pendentes
    print(
        f"Servidor TCP aguardando conexões em {HOST}:{PORT}... (CTRL+C para encerrar)")

    try:
        while True:
            # accept() bloqueia até uma nova conexão chegar
            conn, addr = server_socket.accept()
            # Cria thread para tratar o cliente. daemon=True facilita encerramento com CTRL+C
            thread = threading.Thread(
                target=manipula_cliente, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        # Tratamento de CTRL+C para parar o servidor de forma limpa
        print("\nServidor interrompido manualmente.")
    except Exception as e:
        print(f"Erro no servidor TCP: {e}")
    finally:
        server_socket.close()
        print("Servidor TCP encerrado.")


if __name__ == "__main__":
    main()
