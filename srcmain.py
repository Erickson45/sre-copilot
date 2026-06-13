from flask import Flask, request, jsonify
from llm_engine import analyze_incident
from notifier import send_alert_notification

app = Flask(__name__)

@app.route('/webhook/alert', methods=['POST'])
def receive_alert():
    """Endpoint que o Zabbix/Prometheus vai chamar."""
    data = request.json
    
    if not data:
        return jsonify({"error": "Nenhum dado recebido"}), 400

    # Extrai os dados enviados pela ferramenta de monitoramento
    host = data.get("host", "Desconhecido")
    trigger = data.get("trigger", "Alerta Genérico")
    severity = data.get("severity", "High")
    opdata = data.get("opdata", "Sem informações adicionais")

    print(f"📥 Recebido alerta: {trigger} no host {host}. Processando com IA...")

    # Roda a inteligência do AIOps
    ia_analysis = analyze_incident(host, trigger, severity, opdata)
    
    # Dispara a notificação para a equipe
    send_alert_notification(host, trigger, ia_analysis)

    return jsonify({
        "status": "success",
        "message": "Alerta processado e equipe notificada.",
        "ai_analysis": ia_analysis
    }), 200

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000)