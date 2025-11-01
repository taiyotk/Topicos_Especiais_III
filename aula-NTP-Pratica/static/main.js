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