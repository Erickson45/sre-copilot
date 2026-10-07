import llm_engine
import main


def make_client():
    main.app.config["TESTING"] = True
    return main.app.test_client()


def test_webhook_sem_payload_retorna_400():
    response = make_client().post("/webhook/alert", json={})
    assert response.status_code == 400


def test_webhook_processa_alerta(monkeypatch):
    monkeypatch.setattr(main, "analyze_incident", lambda *args: "diagnostico de teste")
    monkeypatch.setattr(main, "send_alert_notification", lambda *args: True)

    response = make_client().post(
        "/webhook/alert",
        json={"host": "srv-prod-web-01", "trigger": "Nginx 502 Bad Gateway Detected"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "success"
    assert body["ai_analysis"] == "diagnostico de teste"


def test_runbook_nginx_502_encontrado():
    conteudo = llm_engine.get_runbook_content("Nginx 502 Bad Gateway Detected")
    assert "502" in conteudo


def test_runbook_inexistente():
    conteudo = llm_engine.get_runbook_content("Disco cheio em /var")
    assert "Nenhum runbook" in conteudo


def test_ollama_indisponivel_nao_derruba_api(monkeypatch):
    def falha(*args, **kwargs):
        raise ConnectionError("ollama offline")

    monkeypatch.setattr(llm_engine.requests, "post", falha)
    resultado = llm_engine.analyze_incident("host", "Nginx 502", "High", "-")
    assert "Erro de conexão com Ollama" in resultado
