<div align="center">

# 🤖 SRE-Copilot: AIOps Incident Gateway

**Transformando Alertas de Monitoramento em Resoluções Acionáveis com IA Local**

![Python](https://img.shields.io/badge/Python-3.10-0F172A?style=for-the-badge&logo=python&logoColor=00E5FF)
![Flask](https://img.shields.io/badge/Flask-API-0F172A?style=for-the-badge&logo=flask&logoColor=00E5FF)
![Ollama](https://img.shields.io/badge/Local_LLM-Ollama-0F172A?style=for-the-badge&logo=ollama&logoColor=00E5FF)
![Docker](https://img.shields.io/badge/Docker-Ready-0F172A?style=for-the-badge&logo=docker&logoColor=00E5FF)

[![CI](https://github.com/Erickson45/sre-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/Erickson45/sre-copilot/actions/workflows/ci.yml)

</div>

---

## 🎯 O Problema

Equipes de NOC e SRE frequentemente sofrem com a **fadiga de alertas**. O monitoramento (Zabbix, Prometheus, Datadog) dispara dezenas de incidentes, mas o operador ainda precisa parar, ler o alerta, procurar a documentação (Runbook) e decidir o que fazer. Isso eleva o **MTTR** (Tempo Médio de Resolução) e gera *toil* (trabalho manual repetitivo).

## 🚀 A Solução (SRE-Copilot)

O **SRE-Copilot** é um middleware inteligente (*AIOps Gateway*) projetado para interceptar webhooks de ferramentas de monitoramento. Ele utiliza **Busca Semântica (RAG)** em manuais de infraestrutura locais (`.md`) e cruza esses dados com **LLMs Open-Source rodando localmente (Ollama)**. 

O resultado? O sistema mastiga o alerta e entrega no chat da equipe (Teams/Discord/Slack) um diagnóstico cirúrgico com a causa provável e os comandos exatos de mitigação. **Tudo isso com zero exposição de dados para a nuvem externa.**

---

## 🧠 Arquitetura do Fluxo

1. 📡 **Monitoramento:** Zabbix/Prometheus detecta a falha e envia um POST genérico.
2. 🛬 **API Gateway (Flask):** O SRE-Copilot recebe o JSON do incidente.
3. 📚 **Retrieval-Augmented Generation (RAG):** O motor busca na pasta `/runbooks` o documento Markdown correspondente à falha.
4. 🤖 **Inferência Local (Ollama):** A IA lê o alerta cru + a documentação corporativa e gera um plano de ação.
5. 💬 **Notificação:** O alerta enriquecido é disparado no chat da equipe operacional.

---

## ✅ CI/CD (GitHub Actions)

A cada push/PR na `main`, o pipeline [`ci.yml`](.github/workflows/ci.yml) executa:

1. **Lint** com `ruff`.
2. **Testes** com `pytest` (API Flask, busca de runbooks e resiliência quando o Ollama está fora do ar).
3. **Build da imagem Docker** e **smoke test** do container (sobe a API e valida o `POST /webhook/alert`).
4. **Publicação** da imagem no GitHub Container Registry: `ghcr.io/erickson45/sre-copilot:latest`.

Rodando os testes localmente:

```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest -v
```

---

## 📂 Estrutura do Projeto

```text
📦 sre-copilot
 ┣ 📂 runbooks/             # Base de Conhecimento (POPs e Manuais em Markdown)
 ┃ ┗ 📜 nginx_502.md        # Exemplo de runbook mapeado pela IA
 ┣ 📂 src/
 ┃ ┣ 📜 main.py             # API Flask (Webhook Receiver)
 ┃ ┣ 📜 llm_engine.py       # Motor RAG e conexão com Ollama
 ┃ ┗ 📜 notifier.py         # Orquestrador de disparos (Discord/Teams)
 ┣ 📜 simulate_alert.py     # 🚀 Script rápido para testar a aplicação
 ┣ 📜 docker-compose.yml    # Orquestração da API + Ollama Server
 ┣ 📜 Dockerfile
 ┗ 📜 requirements.txt
