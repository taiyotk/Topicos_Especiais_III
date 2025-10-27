import ntplib
from datetime import datetime
import pytz

# Servidores NTP de referência
ntp_servers = {
    "Brasil": "a.st1.ntp.br",
    "EUA": "time.google.com",
    "Reino Unido": "time.windows.com",
    "Japão": "ntp.jst.mfeed.ad.jp",
    "Alemanha": "ptbtime1.ptb.de"
}

# Função para obter a hora do servidor NTP
def get_ntp_time(server):
    client = ntplib.NTPClient()
    try:
        response = client.request(server, version=3)
        return datetime.fromtimestamp(response.tx_time)
    except Exception as e:
        print(f"Erro ao consultar o servidor {server}: {e}")
        return None

# Fuso horários de diferentes locais usando pytz
timezones = {
    "Brasil": "America/Sao_Paulo",
    "EUA": "America/New_York",
    "Reino Unido": "Europe/London",
    "Japão": "Asia/Tokyo",
    "Alemanha": "Europe/Berlin"
}

# Função principal para exibir os horários locais
def show_times():
    for country, server in ntp_servers.items():
        ntp_time = get_ntp_time(server)
        if ntp_time:
            timezone = pytz.timezone(timezones[country])
            local_time = ntp_time.astimezone(timezone)
            print(f"Horário em {country} (via {server}): {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Execução da função
if __name__ == "__main__":
    show_times()
