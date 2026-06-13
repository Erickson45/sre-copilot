import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3") # Pode usar qwen2.5, phi3, etc.

def get_runbook_content(alert_name):
    """Busca um runbook baseado em palavras-chave do alerta."""
    alert_lower = alert_name.lower()
    
    # Lógica simples de RAG (Busca de arquivos baseada no nome do alerta)
    if "nginx" in alert_lower and "502" in alert_lower:
        file_path = "runbooks/nginx_502.md"
    else:
        return "Nenhum runbook específico encontrado para este alerta."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Arquivo de runbook não encontrado no sistema."

def analyze_incident(host, trigger, severity, opdata):
    """Cruza os dados do alerta com o Runbook usando a IA local."""
    
    runbook_context = get_runbook_content(trigger)
    
    prompt = f"""Você é um Engenheiro de Confiabilidade (SRE) Sênior.
Analise o incidente abaixo e gere um resumo acionável baseado no Runbook oficial.

DADOS DO ALERTA:
- Host: {host}
- Falha: {trigger}
- Severidade: {severity}
- Detalhes (OpData): {opdata}

RUNBOOK OFICIAL:
{runbook_context}

Gere uma resposta curta e profissional contendo:
1. Uma breve análise da falha.
2. O que o operador deve fazer imediatamente (Comandos).
Não use saudações, vá direto ao ponto.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "Erro ao processar resposta da IA.")
        return f"Erro na IA: HTTP {response.status_code}"
    except Exception as e:
        return f"Erro de conexão com Ollama: {str(e)}"