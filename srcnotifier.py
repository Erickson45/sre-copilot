import requests
import os

# Para testar local, você pode colocar a URL de um webhook do Discord ou Teams
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

def send_alert_notification(host, trigger, ia_analysis):
    """Envia o diagnóstico formatado para o canal da equipe."""
    
    # Se não tiver URL configurada no .env, apenas printa no console (Modo Teste)
    if not WEBHOOK_URL:
        print("\n" + "="*50)
        print(f"🚨 NOVO INCIDENTE: {trigger} no host {host}")
        print("-" * 50)
        print(f"🤖 ANÁLISE DA IA (SRE-Copilot):\n{ia_analysis}")
        print("="*50 + "\n")
        return True

    # Exemplo de payload para Discord (Pode ser adaptado para Teams)
    payload = {
        "content": f"🚨 **Incidente:** {trigger} | **Host:** {host}",
        "embeds": [{
            "title": "🤖 Diagnóstico AIOps (SRE-Copilot)",
            "description": ia_analysis,
            "color": 15158332 # Vermelho
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return True
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        return False