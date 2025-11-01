from flask import Flask, jsonify, render_template
import ntplib
from datetime import datetime
import pytz
import time

app = Flask(__name__)

# Servidores NTP de referência (mesma lista que você forneceu)
ntp_servers = {
    "Brasil": "a.st1.ntp.br",
    "EUA": "time.google.com",
    "Reino Unido": "time.windows.com",
    "Japão": "ntp.jst.mfeed.ad.jp",
    "Alemanha": "ptbtime1.ptb.de"
}

# Fusos (pytz) — inclui vários fusos do Brasil
timezones = {
    "America/Sao_Paulo": "São Paulo (Horário de Brasília)",
    "America/Manaus": "Manaus",
    "America/Cuiaba": "Cuiabá",
    "America/Fortaleza": "Fortaleza",
    "America/Noronha": "Fernando de Noronha",
    # outros mencionados no código original (externos)
    "America/New_York": "EUA - New York",
    "Europe/London": "Reino Unido - London",
    "Asia/Tokyo": "Japão - Tokyo",
    "Europe/Berlin": "Alemanha - Berlin"
}

ntp_client = ntplib.NTPClient()


def query_ntp(server, timeout=5):
    """Consulta o servidor NTP e retorna um dicionário com tempo UTC e diferença em segundos."""
    try:
        resp = ntp_client.request(server, version=3, timeout=timeout)
        # tx_time: instante de transmissão do servidor em segundos epoch
        ntp_utc = datetime.fromtimestamp(resp.tx_time, tz=pytz.utc)

        # tempo local no instante de recebimento (UTC) — cria um timestamp comparável
        local_utc = datetime.now(pytz.utc)

        offset_seconds = (ntp_utc - local_utc).total_seconds()

        return {
            "server": server,
            "ntp_utc_iso": ntp_utc.isoformat(),
            "local_utc_iso": local_utc.isoformat(),
            "offset_seconds": offset_seconds,
            "stratum": getattr(resp, 'stratum', None),
            "delay": getattr(resp, 'delay', None),
        }
    except Exception as e:
        return {"server": server, "error": str(e)}

@app.route('/api/times')
def api_times():
    """Retorna um JSON com os tempos NTP por servidor e conversões para fusos locais."""
    results = []
    for name, server in ntp_servers.items():
        data = query_ntp(server)
        # para cada timezone desejado, converta o ntp_utc (se disponível)
        if 'ntp_utc_iso' in data:
            ntp_utc = datetime.fromisoformat(data['ntp_utc_iso'])
            tz_map = {}
            for tz_name, label in timezones.items():
                try:
                    tz = pytz.timezone(tz_name)
                    tz_map[label] = ntp_utc.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                except Exception:
                    tz_map[label] = None
            data['converted'] = tz_map
        results.append({"server_name": name, **data})
    # também forneça o horário local do sistema (UTC e zonas BR)
    local_utc = datetime.now(pytz.utc).isoformat()
    br_zones = {}
    for tz_name, label in timezones.items():
        try:
            tz = pytz.timezone(tz_name)
            br_zones[label] = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        except Exception:
            br_zones[label] = None

    return jsonify({
        "queried_at_local_utc": local_utc,
        "servers": results,
        "local_zones": br_zones
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Em Codespaces, exponha em 0.0.0.0 e porta 8080 (ou como preferir)
    app.run(host='0.0.0.0', port=8080, debug=True)