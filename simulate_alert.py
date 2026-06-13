import requests

# URL da nossa API AIOps
URL = "http://localhost:5000/webhook/alert"

# JSON simulando um webhook saindo do Zabbix/Prometheus
mock_zabbix_payload = {
    "host": "srv-prod-web-01",
    "trigger": "Nginx 502 Bad Gateway Detected",
    "severity": "High",
    "opdata": "upstream prematurely closed connection while reading response header from upstream"
}

print("🚀 Disparando alerta simulado para o SRE-Copilot...")

try:
    response = requests.post(URL, json=mock_zabbix_payload)
    print("\n✅ Resposta da API:")
    print(response.json())
except Exception as e:
    print(f"❌ Erro ao conectar na API. O servidor Flask (main.py) está rodando?\nDetalhes: {e}")