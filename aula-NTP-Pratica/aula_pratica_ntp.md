# Aula prática: Verificando diferenças entre horário NTP e horário local

> Objetivo: criar uma interface web simples (rodando em GitHub Codespaces) que consulte servidores NTP, calcule a diferença (offset) entre o horário obtido via NTP e o horário do computador, e apresente também outros fusos horários do Brasil e fusos usados de outros países.

---

## Visão geral do projeto

Estrutura do projeto (sugestão):

```
ntp-pratica/
├─ app.py                # Backend Flask que consulta servidores NTP
├─ requirements.txt      # Dependências Python
├─ templates/
│  └─ index.html         # Frontend (interface web)
└─ static/
   └─ main.js            # JS que consome a API e atualiza a UI
```

---

## Arquivos e código (copie para o repositório no Codespace)

### requirements.txt

```
Flask>=2.0
ntplib>=0.3
pytz
```

### app.py

```python
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
```

---

### templates/index.html

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Aula prática NTP</title>
  </head>
  <body>
    <h1>Aula prática: NTP vs Relógio local</h1>
    <p id="status">Carregando...</p>

    <h2>Horários por servidor</h2>
    <div id="servers"></div>

    <h2>Horários locais / fusos do Brasil</h2>
    <div id="local_zones"></div>

    <script src="/static/main.js"></script>
  </body>
</html>
```

---

### static/main.js

```javascript
async function fetchTimes() {
  const res = await fetch('/api/times');
  const data = await res.json();
  document.getElementById('status').textContent = 'Última consulta (UTC): ' + data.queried_at_local_utc;

  const serversDiv = document.getElementById('servers');
  serversDiv.innerHTML = '';

  data.servers.forEach(s => {
    const el = document.createElement('div');
    if (s.error) {
      el.innerHTML = `<strong>${s.server_name} (${s.server}):</strong> Erro: ${s.error}`;
    } else {
      el.innerHTML = `<strong>${s.server_name} (${s.server}):</strong> NTP UTC ${s.ntp_utc_iso} — Offset (s): ${s.offset_seconds.toFixed(3)}<br>`;
      // mostrar conversões
      const conv = document.createElement('ul');
      for (const [label, timestr] of Object.entries(s.converted)) {
        const li = document.createElement('li');
        li.textContent = `${label}: ${timestr}`;
        conv.appendChild(li);
      }
      el.appendChild(conv);
    }
    serversDiv.appendChild(el);
  });

  // local zones
  const lz = document.getElementById('local_zones');
  lz.innerHTML = '';
  for (const [label, tstr] of Object.entries(data.local_zones)) {
    const p = document.createElement('p');
    p.textContent = `${label}: ${tstr}`;
    lz.appendChild(p);
  }
}

fetchTimes();
setInterval(fetchTimes, 20_000); // atualiza a cada 20s
```

---

## Explicação passo-a-passo e mapeamento com conceitos do NTP

### O que o backend faz

1. **Consulta servidores NTP**: `ntplib.NTPClient().request(server)` faz um request UDP para o servidor NTP e obtém um pacote com campos como `tx_time` (momento em que o servidor transmitiu o pacote). No nosso código pegamos `resp.tx_time` e o transformamos em `datetime` em UTC (Tempo Universal Coordenado).

2. **Calcula offset**: a diferença `ntp_utc - local_utc` retorna quantos segundos o relógio do sistema está adiantado ou atrasado, no instante da consulta. Esse valor equivale ao deslocamento (offset) estimado.

3. **Converte para fusos locais**: usando `pytz` convertemos o `ntp_utc` para fusos como `America/Sao_Paulo`, `America/Manaus` etc.

4. **Fornece um JSON** com os resultados, para que o frontend possa exibir de forma amigável.

> Observação: este exemplo é educativo e usa consultas pontuais. Implementações completas do NTP (ntpd, Chrony, NTPSec) fazem várias amostragens, aplicam filtros, estimam jitter/delay e tomam decisões de seleção (selection) e combinação (combination) que asseguram maior robustez.


### Relação com a página do NTP.br (referências conceituais)

- O NTP define algoritmos para consultar servidores, calcular deslocamento e estimar erro. No tutorial estamos apenas demonstrando a etapa de **consulta** e **cálculo de deslocamento** a partir de uma amostra (idealmente múltiplas amostras deveriam ser usadas).

- O conceito de **estratos (strata)** e a recomendação de ter múltiplas referências aparece na página, por isso consultamos vários servidores no exemplo para comparar resultados.

- O site também recomenda formas de operação (cliente/servidor, uso de `iburst` para acelerar sincronização inicial) .

---

## Como rodar no Codespace (passo a passo)

1. Abra um GitHub Codespace a partir do repositório que contenha os arquivos acima.
2. No terminal do Codespace crie um ambiente virtual (opcional):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
python app.py
```

4. No Codespaces, abra a porta 8080 (a interface do Codespaces geralmente mostra um botão "PORTAS") e clique para abrir o site.

---

## Extensões e dependências recomendadas para Codespaces / VS Code

- **Extensão VS Code** (instale no Codespace):
  - Python (ms-python.python)

- **Dependências Python**: `Flask`, `ntplib`, `pytz` (já listadas em requirements.txt)

---